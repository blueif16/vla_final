"""Record every model call of one LIBERO episode: the two images exactly as sent, the sentence, and the action chunk.

For teaching figures ("what goes in, what comes out"). Same preprocessing as run_libero.py and openpi's client.
Writes <out>/calls.json and <out>/call_NN_{table,wrist}.png.
"""

import collections
import dataclasses
import json
import pathlib

import imageio
from libero.libero import benchmark
import numpy as np
from openpi_client import image_tools
from openpi_client import websocket_client_policy as _websocket_client_policy
import tyro

from run_libero import LIBERO_DUMMY_ACTION, LIBERO_ENV_RESOLUTION, MAX_STEPS, _get_env, _quat2axisangle


@dataclasses.dataclass
class Args:
    out_dir: str
    task_suite_name: str = "libero_spatial"
    task_id: int = 0
    trial: int = 0
    host: str = "0.0.0.0"
    port: int = 8000
    replan_steps: int = 5
    resize_size: int = 224
    num_steps_wait: int = 10
    seed: int = 7


def main(args: Args) -> None:
    np.random.seed(args.seed)
    out = pathlib.Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    suite = benchmark.get_benchmark_dict()[args.task_suite_name]()
    task = suite.get_task(args.task_id)
    env, sentence = _get_env(task, LIBERO_ENV_RESOLUTION, args.seed)
    env.reset()
    obs = env.set_init_state(suite.get_task_init_states(args.task_id)[args.trial])
    client = _websocket_client_policy.WebsocketClientPolicy(args.host, args.port)

    calls, plan, t, done = [], collections.deque(), 0, False
    while t < MAX_STEPS[args.task_suite_name] + args.num_steps_wait:
        if t < args.num_steps_wait:
            obs, _, done, _ = env.step(LIBERO_DUMMY_ACTION)
            t += 1
            continue
        if not plan:
            img = np.ascontiguousarray(obs["agentview_image"][::-1, ::-1])
            wrist = np.ascontiguousarray(obs["robot0_eye_in_hand_image"][::-1, ::-1])
            img = image_tools.convert_to_uint8(image_tools.resize_with_pad(img, args.resize_size, args.resize_size))
            wrist = image_tools.convert_to_uint8(image_tools.resize_with_pad(wrist, args.resize_size, args.resize_size))
            state = np.concatenate(
                (obs["robot0_eef_pos"], _quat2axisangle(obs["robot0_eef_quat"]), obs["robot0_gripper_qpos"])
            )
            chunk = np.asarray(
                client.infer(
                    {"observation/image": img, "observation/wrist_image": wrist, "observation/state": state, "prompt": sentence}
                )["actions"]
            )
            n = len(calls)
            imageio.imwrite(out / f"call_{n:02d}_table.png", img)
            imageio.imwrite(out / f"call_{n:02d}_wrist.png", wrist)
            calls.append({"call": n, "step": t - args.num_steps_wait, "actions": np.round(chunk, 4).tolist(), "run": args.replan_steps})
            plan.extend(chunk[: args.replan_steps])
        obs, _, done, _ = env.step(plan.popleft().tolist())
        t += 1
        if done:
            break
    env.close()
    meta = {
        "suite": args.task_suite_name,
        "task_id": args.task_id,
        "trial": args.trial,
        "prompt": sentence,
        "success": bool(done),
        "steps": t - args.num_steps_wait,
        "image_size": args.resize_size,
        "action_dims": ["dx", "dy", "dz", "droll", "dpitch", "dyaw", "gripper (-1 open, +1 close)"],
        "note": "images are exactly what the model received (rotated 180 degrees and padded to 224, as in openpi's client)",
        "calls": calls,
    }
    (out / "calls.json").write_text(json.dumps(meta, indent=1))
    print(f"{len(calls)} calls, success={done}, steps={meta['steps']} -> {out}")


if __name__ == "__main__":
    main(tyro.cli(Args))
