# Stage 1: running π0.5 in LIBERO's kitchen

How we run `pi05_libero` on our own machine, and the runner our experiments use. The plan and the experiments are in
[`topic.md`](../topic.md).

## What runs where

Two programs talk over a local websocket. The policy server holds π0.5 on the GPU. The LIBERO client runs the
simulator on the CPU, sends the server two camera images and the instruction, gets back 10 actions, runs 5, and asks
again. They need different Python versions, so each has its own environment inside openpi's folder.

| Part | Folder | Python | Main pins |
|---|---|---|---|
| Policy server | `~/openpi/.venv` | 3.11 (uv) | JAX with CUDA 12, openpi |
| LIBERO client | `~/openpi/examples/libero/.venv` | 3.8 | mujoco 3.2.3, robosuite 1.4.1, torch 1.11 (cu113), LIBERO at openpi's pinned commit |

We use openpi's own pins rather than a newer LIBERO packaging, because openpi's published scores (98.8 Spatial, 98.0
Goal) came from these versions.

## Setup

```sh
git clone --recurse-submodules https://github.com/Physical-Intelligence/openpi.git ~/openpi
cd ~/openpi
GIT_LFS_SKIP_SMUDGE=1 uv sync && GIT_LFS_SKIP_SMUDGE=1 uv pip install -e .

uv venv --python 3.8 examples/libero/.venv
source examples/libero/.venv/bin/activate
uv pip sync examples/libero/requirements.txt third_party/libero/requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cu113 --index-strategy=unsafe-best-match
uv pip install -e packages/openpi-client
uv pip install -e third_party/libero
```

## Running

```sh
# terminal 1, in ~/openpi (port 8000 is taken on our machine, so we use 8011)
uv run scripts/serve_policy.py --env LIBERO --port 8011

# terminal 2, in this repo
source ~/openpi/examples/libero/.venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$HOME/openpi/third_party/libero MUJOCO_GL=glx
export LIBERO_CONFIG_PATH=$HOME/openpi/examples/libero/.libero_config   # see "Things that tripped us up"
python stage1/run_libero.py --port 8011 --label original --task-suite-name libero_spatial --task-ids 7 9 --num-trials-per-task 5
```

`run_libero.py` keeps openpi's preprocessing, replanning (5 of 10 actions), wait steps, step limits and seed, and adds
what the experiments need: choosing tasks, replacing the instruction (`--prompt blank` or any text), watching extra
predicates and other tasks' goals, one JSON line per episode in `episodes.jsonl`, and side-by-side table and wrist
videos.

## Things that tripped us up on WSL2

- **Rendering.** Use `MUJOCO_GL=glx`. EGL fails on this machine, and glx falls through to a GLFW context that works
  through WSLg. We learned this in an earlier LIBERO project on the same machine, where building a scene
  took 15–85 s and each control step 0.04–0.16 s.
- **The checkpoint download.** openpi fetches `gs://openpi-assets/checkpoints/pi05_libero` (12.44 GB, 16 files)
  with `gsutil` when it's installed, and a `gsutil` with stale Google credentials fails. The bucket is public, so we
  downloaded the files over HTTPS (`https://storage.googleapis.com/openpi-assets/checkpoints/pi05_libero/...`) into
  `~/.cache/openpi/openpi-assets/checkpoints/pi05_libero`, which is where openpi looks first. That ran at about
  34 MB/s, while the Python packages came at about 1.4 MB/s.
- **LIBERO's first import asks a question** ("Do you want to specify a custom path…") unless a config file exists. We
  write one to `~/openpi/examples/libero/.libero_config/config.yaml`, pointing at `third_party/libero/libero/libero`
  and its `bddl_files`, `init_files` and `assets`, and set `LIBERO_CONFIG_PATH` to that folder.
- **Task numbers.** LIBERO's benchmark numbers tasks differently from the Hugging Face dataset. In LIBERO-Spatial,
  the two tasks that share a starting table are 7 ("the bowl on the stove") and 9 ("the bowl on the wooden cabinet").
- **Port 8000** was already taken by another project's Docker container, so our server runs on 8011.
- **Image orientation.** openpi turns both camera images 180° before sending them, to match how the training data
  was stored, so left and right are swapped compared with the LIBERO paper's figures.
