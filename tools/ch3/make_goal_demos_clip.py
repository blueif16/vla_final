"""Make chapter 3's opening clip: three human demonstrations from one LIBERO-Goal table, side by side.

Each panel is the table camera of one recorded demonstration in the physical-intelligence/libero dataset (CC BY 4.0),
at its recorded 10 frames a second. For each task we take the dataset's FIRST demonstration of that task (lowest
episode index), so no run is picked for how it looks. A shorter run holds its last frame until the longest ends.
The frames are used as the dataset stores them, which is turned 180 degrees against the LIBERO paper's figures,
the same way pi05_libero sees them.

Writes docs/assets/video/ch3-goal-three-demos.mp4 (H.264, yuv420p, +faststart, CRF 28) and its poster (first frame).
Runs with any Python 3 that has Pillow, plus ffmpeg, e.g. openpi's LIBERO client venv:
    ~/openpi/examples/libero/.venv/bin/python tools/ch3/make_goal_demos_clip.py
Rows come from the Hugging Face datasets-server rows API (documented in library/papers.yaml, key libero-dataset).
"""

import io
import json
import pathlib
import subprocess
import tempfile
import time
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "assets" / "video"
API = "https://datasets-server.huggingface.co/rows?dataset=physical-intelligence/libero&config=default&split=train"
META = "https://huggingface.co/datasets/physical-intelligence/libero/resolve/main/meta/episodes.jsonl"
TASKS = ["put the bowl on the plate", "turn on the stove", "put the wine bottle on top of the cabinet"]
UA = {"User-Agent": "course-project-figure-script"}


def get(url, tries=6):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except Exception:  # the rows API sometimes answers 502; wait and retry
            time.sleep(2 + 2 * i)
    raise RuntimeError(f"could not fetch {url}")


def main():
    eps = [json.loads(line) for line in get(META).decode().splitlines() if line.strip()]
    eps.sort(key=lambda e: e["episode_index"])
    offset, chosen = 0, {}
    for e in eps:
        e["offset"] = offset
        offset += e["length"]
        task = e["tasks"][0]
        if task in TASKS and task not in chosen:
            chosen[task] = e
    runs = []
    for task in TASKS:
        e = chosen[task]
        frames = []
        for start in range(e["offset"], e["offset"] + e["length"], 100):
            n = min(100, e["offset"] + e["length"] - start)
            rows = json.loads(get(f"{API}&offset={start}&length={n}"))["rows"]
            for r in rows:
                assert r["row"]["episode_index"] == e["episode_index"]
                frames.append(Image.open(io.BytesIO(get(r["row"]["image"]["src"]))).convert("RGB"))
        print(f"episode {e['episode_index']} ({task}): {len(frames)} frames from row {e['offset']}", flush=True)
        runs.append((e, frames))

    longest = max(len(f) for _, f in runs)
    with tempfile.TemporaryDirectory() as tmp:
        for t in range(longest):
            sheet = Image.new("RGB", (256 * len(runs) + 8 * (len(runs) - 1), 256), (14, 13, 11))
            for k, (_, frames) in enumerate(runs):
                sheet.paste(frames[min(t, len(frames) - 1)], (k * (256 + 8), 0))
            sheet.save(f"{tmp}/f{t:04d}.png")
            if t == 0:
                OUT.mkdir(parents=True, exist_ok=True)
                sheet.save(OUT / "ch3-goal-three-demos.jpg", quality=88)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "10", "-i", f"{tmp}/f%04d.png",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "28", "-movflags", "+faststart",
                        "-map_metadata", "-1", str(OUT / "ch3-goal-three-demos.mp4")], check=True)
    meta = [{"task": e["tasks"][0], "episode_index": e["episode_index"], "row_offset": e["offset"],
             "frames": e["length"], "seconds": e["length"] / 10} for e, _ in runs]
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
