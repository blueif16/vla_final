"""Make chapter 4's footage and stills from experiment 1's recorded runs (stage1/runs/exp1-shared-table/).

Run from the repo root:  python3 tools/ch4/make_assets.py
Needs ffmpeg on the PATH and the local videos in stage1/runs/exp1-shared-table/videos/ (gitignored, so this runs only on
the machine that recorded them). Python standard library only.

What it makes, and the rule each pick follows (so no frame is chosen by eye):
- docs/assets/video/ch4-same-start.{mp4,jpg}: figure 4.1. LIBERO-Spatial task 9 ("... the black bowl on the wooden
  cabinet ..."), starting state 2, run twice: with its own sentence (left) and with an empty string (right). Table camera
  only, the two runs side by side in one file so they stay in step. This pick is a choice, not a sample: of the
  starting states 0-9 of both tasks, state 2 of task 9 is the first whose blank run ended with the other bowl on the
  plate (checked by the simulator), which shows the change most plainly. That ending is the most common one in task 9's
  counted blank runs (the stove bowl, 5 of 10), but across all 40 blank episodes a bowl reached the plate only 15 times,
  so the page says this and shows every ending in figure 4.2.
- docs/assets/img/ch4/ending-{stove,cabinet,cookie,none}.jpg: figure 4.2. For each ending of the counted blank run
  (starting states 10-19), the first episode with that ending, task 7 before task 9, lowest starting state first. The
  frame is the step the object first reached the plate (from episodes.jsonl), or the last frame when nothing did.
- docs/assets/img/ch4/spatial-t0-start.png: the first picture of LIBERO-Spatial task 0 as the model received it, copied
  from our recorded run (stage1/runs/recorded-call-spatial0/call_00_table.png) for figures 4.3 to 4.5.

Frames are exactly what the model received: openpi's client turns both camera pictures 180 degrees before sending
them (stage1/run_libero.py records them after that turn). The recordings were saved at 10 frames a second, one frame
per simulator step; LIBERO's environment steps at 20 a second (control_freq=20 in libero/envs/env_wrapper.py, which
openpi's examples/libero/main.py doesn't override), so the clip is written at 20 frames a second: simulated real time,
twice the speed of the saved recording.
"""
import json, pathlib, shutil, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
RUN = ROOT / "stage1/runs/exp1-shared-table"
VID = RUN / "videos"
OUT_V = ROOT / "docs/assets/video"
OUT_I = ROOT / "docs/assets/img/ch4"
FPS = 20          # simulator steps per second
HOLD = 1.0        # seconds the last frame is held at the end of the clip
CAM = "crop=224:224:0:0"   # the recordings are table | wrist, 224 px each; keep the table camera

def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)

def frames(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_frames", "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return int(r.stdout.strip())

def video(label, task, trial):
    hits = list(VID.glob(f"{label}_t{task}_trial{trial:02d}_*.mp4"))
    assert len(hits) == 1, (label, task, trial, hits)
    return hits[0]

eps = [json.loads(l) for l in open(RUN / "episodes.jsonl")]
def ep(label, task, trial):
    return next(e for e in eps if e["label"] == label and e["task_id"] == task and e["trial"] == trial)

# In both task files akita_black_bowl_1 is the bowl the task names (LIBERO's bddl files for this pair differ only in the
# sentence and in which bowl starts where), so the stove bowl is bowl_1 in task 7 and bowl_2 in task 9.
STOVE = {7: "akita_black_bowl_1", 9: "akita_black_bowl_2"}
CABINET = {7: "akita_black_bowl_2", 9: "akita_black_bowl_1"}

def ending(e):
    """What reached the plate first in a counted episode, and at which step; ('none', None) if nothing checked did."""
    t = e["task_id"]
    on = {k.split()[1]: v for k, v in e["also_true"].items() if k.startswith("on ") and k.endswith(" plate_1")}
    hits = sorted((s, name) for name, s in on.items())
    if not hits:
        return "none", None
    s, name = hits[0]
    kind = {STOVE[t]: "stove", CABINET[t]: "cabinet", "cookies_1": "cookie"}[name]
    return kind, s

def main():
    OUT_V.mkdir(parents=True, exist_ok=True)
    OUT_I.mkdir(parents=True, exist_ok=True)

    # ---- figure 4.1: the same start, the sentence and an empty string ----
    a, b = video("original", 9, 2), video("blank", 9, 2)
    ea, eb = ep("original", 9, 2), ep("blank", 9, 2)
    assert ea["success"] and not eb["success"] and eb["also_true"] == {"on akita_black_bowl_2 plate_1": 125}
    n = max(frames(a), frames(b))
    clip = OUT_V / "ch4-same-start.mp4"
    graph = (f"[0:v]{CAM},setpts=N/({FPS}*TB),fps={FPS},tpad=stop_mode=clone:stop={n - frames(a) + int(HOLD * FPS)}[l];"
             f"[1:v]{CAM},setpts=N/({FPS}*TB),fps={FPS},tpad=stop_mode=clone:stop={n - frames(b) + int(HOLD * FPS)}[r];"
             f"[l][r]hstack=inputs=2,scale=896:448:flags=lanczos,fps={FPS},format=yuv420p[v]")
    ff("-i", str(a), "-i", str(b), "-filter_complex", graph, "-map", "[v]", "-r", str(FPS), "-c:v", "libx264",
       "-crf", "28", "-preset", "slow", "-movflags", "+faststart", "-an", "-map_metadata", "-1", str(clip))
    ff("-i", str(clip), "-frames:v", "1", "-q:v", "3", str(clip.with_suffix(".jpg")))
    print(f"{clip.relative_to(ROOT)}: {n} frames at {FPS} fps + {HOLD} s hold "
          f"(original {ea['steps']} steps, blank {eb['steps']} steps)")

    # ---- figure 4.2: how the counted blank episodes ended ----
    counted = sorted((e for e in eps if e["label"] == "blank-counted"), key=lambda e: (e["task_id"], e["trial"]))
    tally, first = {}, {}
    for e in counted:
        kind, step = ending(e)
        tally.setdefault(kind, {7: [], 9: []})[e["task_id"]].append((e["trial"], step, e["success"]))
        first.setdefault(kind, (e, step))
    for kind, (e, step) in first.items():
        src = video("blank-counted", e["task_id"], e["trial"])
        idx = frames(src) - 1 if step is None else min(step, frames(src) - 1)
        dst = OUT_I / f"ending-{kind}.jpg"
        ff("-i", str(src), "-vf", f"select=eq(n\\,{idx}),{CAM}", "-frames:v", "1", "-q:v", "2", str(dst))
        print(f"{dst.relative_to(ROOT)}: task {e['task_id']}, starting state {e['trial']}, frame {idx}")
    print(json.dumps({k: {t: v for t, v in d.items()} for k, d in tally.items()}))

    # ---- figures 4.3 to 4.5: LIBERO-Spatial task 0's first picture, from our recorded run ----
    shutil.copyfile(ROOT / "stage1/runs/recorded-call-spatial0/call_00_table.png", OUT_I / "spatial-t0-start.png")
    print("docs/assets/img/ch4/spatial-t0-start.png copied")

if __name__ == "__main__":
    main()
