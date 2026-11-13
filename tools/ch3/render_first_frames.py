"""Render the benchmark's own starting pictures for chapter 3's web page (docs/assets/img/ch3/).

What it makes, all from LIBERO's stored evaluation starting states (init_files), never from a policy run:
  first/<suite>-tNN.jpg     the first table-camera picture of every task in the four suites, from starting state 0
  states/spatial-t00-sNN.jpg  the first picture of LIBERO-Spatial task 0 from each of its 50 starting states
  tasks.json                the task list (suite, benchmark task id, sentence, task file) the page labels come from

"First picture" means exactly what openpi's LIBERO client sends the model at its first call (examples/libero/main.py,
copied in stage1/run_libero.py): build the scene at 256x256 with env.seed(7), set the stored starting state, run the
10 settling steps of the dummy action, then turn the table camera's image 180 degrees and resize it to 224x224 with
openpi's resize_with_pad. No policy server is started and no episode is run.

Run in openpi's LIBERO client venv (see stage1/README.md):
    source ~/openpi/examples/libero/.venv/bin/activate
    export PYTHONPATH=$PYTHONPATH:$HOME/openpi/third_party/libero MUJOCO_GL=glx
    export LIBERO_CONFIG_PATH=$HOME/openpi/examples/libero/.libero_config
    python tools/ch3/render_first_frames.py            # everything
    python tools/ch3/render_first_frames.py --only states
"""

import argparse
import json
import pathlib
import time

import numpy as np
from PIL import Image
from libero.libero import benchmark
from libero.libero import get_libero_path
from libero.libero.envs import OffScreenRenderEnv
from openpi_client import image_tools

OUT = pathlib.Path(__file__).resolve().parents[2] / "docs" / "assets" / "img" / "ch3"
SUITES = {"libero_spatial": "spatial", "libero_object": "object", "libero_goal": "goal", "libero_10": "ten"}
DUMMY = [0.0] * 6 + [-1.0]  # openpi's LIBERO_DUMMY_ACTION
WAIT = 10                   # openpi's num_steps_wait
SEED = 7                    # openpi's seed
RES = 256                   # openpi's LIBERO_ENV_RESOLUTION
SIZE = 224                  # what the model receives


def build(task):
    bddl = pathlib.Path(get_libero_path("bddl_files")) / task.problem_folder / task.bddl_file
    env = OffScreenRenderEnv(bddl_file_name=str(bddl), camera_heights=RES, camera_widths=RES)
    env.seed(SEED)
    return env


def first_picture(env, state):
    env.reset()
    obs = env.set_init_state(state)
    for _ in range(WAIT):
        obs, _, _, _ = env.step(DUMMY)
    img = np.ascontiguousarray(obs["agentview_image"][::-1, ::-1])
    return image_tools.convert_to_uint8(image_tools.resize_with_pad(img, SIZE, SIZE))


def save(arr, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(arr).save(path, quality=90)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["first", "states"], default=None)
    args = ap.parse_args()
    np.random.seed(SEED)
    bench = benchmark.get_benchmark_dict()
    tasks = []

    if args.only in (None, "first"):
        for name, short in SUITES.items():
            suite = bench[name]()
            for i in range(suite.n_tasks):
                task = suite.get_task(i)
                t0 = time.time()
                env = build(task)
                pic = first_picture(env, suite.get_task_init_states(i)[0])
                env.close()
                f = OUT / "first" / f"{short}-t{i:02d}.jpg"
                save(pic, f)
                tasks.append({"suite": name, "task_id": i, "sentence": task.language,
                              "bddl": f"{task.problem_folder}/{task.bddl_file}", "file": f"first/{f.name}"})
                print(f"{name} {i} {time.time() - t0:.1f}s  {task.language}", flush=True)
        (OUT / "tasks.json").write_text(json.dumps(tasks, indent=1))

    if args.only in (None, "states"):
        suite = bench["libero_spatial"]()
        task = suite.get_task(0)
        states = suite.get_task_init_states(0)
        env = build(task)
        for s in range(len(states)):
            save(first_picture(env, states[s]), OUT / "states" / f"spatial-t00-s{s:02d}.jpg")
        env.close()
        print(f"libero_spatial task 0: {len(states)} starting states rendered", flush=True)


if __name__ == "__main__":
    main()
