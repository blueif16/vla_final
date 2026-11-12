"""Run pi05_libero on chosen LIBERO tasks under one named condition and log every episode.

Based on openpi's examples/libero/main.py (same image preprocessing, replanning, wait steps, step limits and seed),
with what our experiments need on top:
  - pick tasks by id, and the trials to run per task
  - replace the instruction: the original, a blank one, or any fixed text
  - watch extra goal predicates (e.g. "on akita_black_bowl_2 plate_1") and the goals of every other task in the suite,
    so we know what the robot did when it didn't do the task asked
  - one JSON line per episode, and side-by-side table + wrist videos

Runs in openpi's LIBERO client venv (Python 3.8), with the policy server running:
    uv run scripts/serve_policy.py --env LIBERO          # in ~/openpi
"""

import collections
import dataclasses
import json
import logging
import math
import pathlib
import time
from typing import List, Optional

import imageio
from libero.libero import benchmark
from libero.libero import get_libero_path
from libero.libero.envs import OffScreenRenderEnv
from libero.libero.envs.bddl_utils import robosuite_parse_problem
import numpy as np
from openpi_client import image_tools
from openpi_client import websocket_client_policy as _websocket_client_policy
import tyro

LIBERO_DUMMY_ACTION = [0.0] * 6 + [-1.0]
LIBERO_ENV_RESOLUTION = 256  # resolution used to render training data
MAX_STEPS = {"libero_spatial": 220, "libero_object": 280, "libero_goal": 300, "libero_10": 520, "libero_90": 400}


@dataclasses.dataclass
class Args:
    label: str  # name of the condition, e.g. "original" or "blank"; used in the output and video names
    out_dir: str = "stage1/runs/scratch"

    host: str = "0.0.0.0"
    port: int = 8000
    resize_size: int = 224
    replan_steps: int = 5

    task_suite_name: str = "libero_spatial"
    task_ids: Optional[List[int]] = None  # None = every task in the suite
    num_trials_per_task: int = 50
    first_trial: int = 0  # which of the 50 stored starting states to begin from
    num_steps_wait: int = 10

    prompt: str = "original"  # "original" = the task's own sentence, "blank" = "", anything else = sent as written

    extra_predicates: Optional[List[str]] = None  # e.g. "on akita_black_bowl_2 plate_1"
    watch_suite_goals: bool = False  # also check every other task's goal in this suite at each step
    stop_on_extra: bool = False  # end the episode as soon as an extra predicate or another task's goal holds

    save_video: str = "all"  # "all", "first" (first episode of each task) or "none"
    seed: int = 7


def run(args: Args) -> None:
    np.random.seed(args.seed)
    out = pathlib.Path(args.out_dir)
    (out / "videos").mkdir(parents=True, exist_ok=True)
    log_path = out / "episodes.jsonl"

    suite = benchmark.get_benchmark_dict()[args.task_suite_name]()
    task_ids = args.task_ids if args.task_ids is not None else list(range(suite.n_tasks))
    max_steps = MAX_STEPS[args.task_suite_name]
    extra = [p.split() for p in (args.extra_predicates or [])]

    client = _websocket_client_policy.WebsocketClientPolicy(args.host, args.port)
    logging.info("Server metadata: %s", client.get_server_metadata())

    total, wins = 0, 0
    for task_id in task_ids:
        task = suite.get_task(task_id)
        init_states = suite.get_task_init_states(task_id)
        t_build = time.time()
        env, task_sentence = _get_env(task, LIBERO_ENV_RESOLUTION, args.seed)
        build_s = time.time() - t_build
        prompt = {"original": task_sentence, "blank": ""}.get(args.prompt, args.prompt)

        other_goals = {}
        if args.watch_suite_goals:
            for j in range(suite.n_tasks):
                if j == task_id:
                    continue
                other = suite.get_task(j)
                bddl = pathlib.Path(get_libero_path("bddl_files")) / other.problem_folder / other.bddl_file
                goal = robosuite_parse_problem(str(bddl))["goal_state"]
                if all(name in env.env.object_states_dict for st in goal for name in st[1:]):
                    other_goals[other.language] = goal

        for trial in range(args.first_trial, args.first_trial + args.num_trials_per_task):
            env.reset()
            obs = env.set_init_state(init_states[trial])
            plan = collections.deque()
            frames, t, done, calls, infer_s = [], 0, False, 0, 0.0
            first_true = {}  # name -> step it first held
            t0 = time.time()
            error = None
            while t < max_steps + args.num_steps_wait:
                try:
                    if t < args.num_steps_wait:
                        obs, _, done, _ = env.step(LIBERO_DUMMY_ACTION)
                        t += 1
                        continue
                    # rotate 180 degrees to match openpi's training preprocessing
                    img = np.ascontiguousarray(obs["agentview_image"][::-1, ::-1])
                    wrist = np.ascontiguousarray(obs["robot0_eye_in_hand_image"][::-1, ::-1])
                    img = image_tools.convert_to_uint8(image_tools.resize_with_pad(img, args.resize_size, args.resize_size))
                    wrist = image_tools.convert_to_uint8(
                        image_tools.resize_with_pad(wrist, args.resize_size, args.resize_size)
                    )
                    frames.append(np.concatenate([img, wrist], axis=1))
                    if not plan:
                        element = {
                            "observation/image": img,
                            "observation/wrist_image": wrist,
                            "observation/state": np.concatenate(
                                (obs["robot0_eef_pos"], _quat2axisangle(obs["robot0_eef_quat"]), obs["robot0_gripper_qpos"])
                            ),
                            "prompt": prompt,
                        }
                        ti = time.time()
                        chunk = client.infer(element)["actions"]
                        infer_s += time.time() - ti
                        calls += 1
                        plan.extend(chunk[: args.replan_steps])
                    obs, _, done, _ = env.step(plan.popleft().tolist())
                    t += 1
                    step = t - args.num_steps_wait  # same count as "steps" in the record
                    for p in extra:
                        name = " ".join(p)
                        if name not in first_true and env.env._eval_predicate(p):
                            first_true[name] = step
                    for lang, goal in other_goals.items():
                        if lang not in first_true and all(env.env._eval_predicate(st) for st in goal):
                            first_true[lang] = step
                    if done or (args.stop_on_extra and first_true):
                        break
                except Exception as e:  # keep going like openpi's script, but record it
                    error = repr(e)
                    logging.error("Episode error: %s", error)
                    break

            total += 1
            wins += int(done)
            rec = {
                "label": args.label,
                "suite": args.task_suite_name,
                "task_id": task_id,
                "task": task_sentence,
                "prompt": prompt,
                "trial": trial,
                "success": bool(done),
                "steps": t - args.num_steps_wait,
                "also_true": first_true,
                "calls": calls,
                "infer_s_mean": round(infer_s / max(calls, 1), 4),
                "episode_s": round(time.time() - t0, 1),
                "env_build_s": round(build_s, 1),
                "replan_steps": args.replan_steps,
                "seed": args.seed,
                "error": error,
            }
            with open(log_path, "a") as f:
                f.write(json.dumps(rec) + "\n")
            if args.save_video == "all" or (args.save_video == "first" and trial == args.first_trial):
                name = f"{args.label}_t{task_id}_trial{trial:02d}_{'success' if done else 'failure'}.mp4"
                imageio.mimwrite(out / "videos" / name, frames, fps=10)
            logging.info(
                "[%s] task %d trial %d: success=%s steps=%d also_true=%s (%.0fs, %d calls, %.3fs/call) | %d/%d",
                args.label, task_id, trial, done, rec["steps"], first_true, rec["episode_s"], calls,
                rec["infer_s_mean"], wins, total,
            )
        env.close()
    logging.info("[%s] success %d/%d", args.label, wins, total)


def _get_env(task, resolution, seed):
    bddl = pathlib.Path(get_libero_path("bddl_files")) / task.problem_folder / task.bddl_file
    env = OffScreenRenderEnv(bddl_file_name=bddl, camera_heights=resolution, camera_widths=resolution)
    env.seed(seed)  # openpi: the seed affects object positions even with a fixed initial state
    return env, task.language


def _quat2axisangle(quat):
    """Copied from openpi's examples/libero/main.py (itself from robosuite)."""
    if quat[3] > 1.0:
        quat[3] = 1.0
    elif quat[3] < -1.0:
        quat[3] = -1.0
    den = np.sqrt(1.0 - quat[3] * quat[3])
    if math.isclose(den, 0.0):
        return np.zeros(3)
    return (quat[:3] * 2.0 * math.acos(quat[3])) / den


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    run(tyro.cli(Args))
