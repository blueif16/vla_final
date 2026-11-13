"""RL 1's rule on CartPole: train, record every round's scores, and film real tries.

The rule is the chapter's, exactly: every action in a try is pushed by
(the try's score - the round's average score). No discounting, no reward-to-go,
no normalising: REINFORCE with the batch average as the baseline (Williams 1992).

Policy: chance of pushing left = sigmoid(w . [cart position, cart speed,
pole angle, pole spin, 1]). It starts at w = 0, so every push is 50/50.

Needs: gymnasium[classic-control]==1.0.0, numpy, imageio, imageio-ffmpeg, pillow.
Run from the repo root:  python tools/cartpole/train_and_film.py
Writes docs/assets/data/rl01-cartpole.json and the clips in docs/assets/video/.
"""
import json, pathlib
import numpy as np
import gymnasium as gym
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont

LR, BATCH, ROUNDS, SEEDS, FILM_SEED = 0.001, 16, 300, (0, 1, 2), 0
FILM_ROUNDS = (1, ROUNDS)          # rounds whose tries we keep (states) for filming
ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "docs/assets/data"; VID = ROOT / "docs/assets/video"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def train(seed, keep=()):
    rng = np.random.default_rng(seed)
    env = gym.make("CartPole-v1")
    w = np.zeros(5)
    scores, weights, kept = [], {}, {}
    for rnd in range(1, ROUNDS + 1):
        tries = []
        for _ in range(BATCH):
            s, _ = env.reset(seed=int(rng.integers(1_000_000_000)))
            states, pushes, grad, score = [s.copy()], [], np.zeros(5), 0
            while True:
                x = np.append(s, 1.0)
                p_left = 1 / (1 + np.exp(-w @ x))
                a = 0 if rng.random() < p_left else 1            # 0 = push left, 1 = push right
                grad += ((1 - p_left) if a == 0 else -p_left) * x  # d log(chance of the push taken) / dw
                s, r, term, trunc, _ = env.step(a)
                score += r; pushes.append(a); states.append(s.copy())
                if term or trunc:
                    break
            tries.append({"score": score, "grad": grad, "states": states, "pushes": pushes, "fell": bool(term)})
        sc = np.array([t["score"] for t in tries]); avg = sc.mean()
        weights[rnd] = w.tolist()                                  # the policy these tries were run with
        if rnd in keep:
            kept[rnd] = [{k: t[k] for k in ("score", "states", "pushes", "fell")} for t in tries]
        for t in tries:                                            # the rule
            w = w + LR * (t["score"] - avg) * t["grad"] / BATCH
        scores.append(sc.astype(int).tolist())
    return scores, weights, kept


CROP = (100, 340)                       # rows of Gymnasium's 600x400 render kept: the track and the pole


def frame(env, state, top_left, top_right, note=None):
    env.unwrapped.state = np.array(state, dtype=np.float64)
    img = Image.fromarray(env.render()[CROP[0]:CROP[1]])
    d = ImageDraw.Draw(img); f = ImageFont.truetype(FONT, 20)
    d.text((16, 10), top_left, fill=(41, 39, 31), font=f)
    tw = d.textlength(top_right, font=f); d.text((600 - 16 - tw, 10), top_right, fill=(154, 74, 40), font=f)
    if note:
        nw = d.textlength(note, font=f); d.text(((600 - nw) / 2, 38), note, fill=(154, 74, 40), font=f)
    return np.asarray(img)


def film(tries, label, path, slow=1, hold_s=1.2, fps=25):
    """Write tries one after another at 1/slow of real speed (the simulation runs 50 steps a second).
    Every frame is a real simulator state from training; the last state of each try is held with a note."""
    env = gym.make("CartPole-v1", render_mode="rgb_array"); env.reset(seed=0)
    out, steps_per_frame = [], (50 / slow) / fps
    for i, t in enumerate(tries, 1):
        n = len(t["states"])
        for k in range(int(np.ceil(n / steps_per_frame))):
            st = min(int(k * steps_per_frame), n - 1)
            out.append(frame(env, t["states"][st], f"{label} · try {i}", f"score {st}"))
        end = "pole fell: try over" if t["fell"] else "500 steps: the most a try can score"
        out += [frame(env, t["states"][-1], f"{label} · try {i}", f"score {n - 1}", end)] * int(hold_s * fps)
    imageio.mimwrite(path, out, fps=fps, codec="libx264", quality=None, macro_block_size=8,  # 600x240 kept as is
                     pixelformat="yuv420p", ffmpeg_params=["-crf", "28", "-movflags", "+faststart"])
    Image.fromarray(out[0]).convert("RGB").save(str(path).replace(".mp4", ".jpg"), quality=85)  # poster: the start, score 0
    env.close()


if __name__ == "__main__":
    DATA.mkdir(parents=True, exist_ok=True); VID.mkdir(parents=True, exist_ok=True)
    runs = {}
    for seed in SEEDS:
        sc, wts, kept = train(seed, FILM_ROUNDS if seed == FILM_SEED else ())
        runs[seed] = sc
        if seed == FILM_SEED:
            film_w, film_kept = wts, kept
        print("seed", seed, "round averages", [round(float(np.mean(sc[i])), 1) for i in (0, 49, 99, 149, 199, 249, ROUNDS - 1)], flush=True)
    first4 = film_kept[1][:4]
    film(first4, "round 1", VID / "rl01-cartpole-round1.mp4", slow=2)
    film(film_kept[ROUNDS][:1], f"round {ROUNDS}", VID / f"rl01-cartpole-round{ROUNDS}.mp4")
    json.dump({
        "about": "RL 1's rule on Gymnasium CartPole-v1, made by tools/cartpole/train_and_film.py",
        "rule": "w += lr * (score - round average) * d log(chance of each push taken)/dw, summed over the try, / batch",
        "lr": LR, "batch": BATCH, "rounds": ROUNDS, "seeds": list(SEEDS), "filmed_seed": FILM_SEED,
        "scores": {str(s): runs[s] for s in SEEDS},
        "filmed": {str(r): {"scores": [t["score"] for t in film_kept[r]],
                            "p_left_first_state": [float(1 / (1 + np.exp(-np.array(film_w[r]) @ np.append(t["states"][0], 1.0)))) for t in film_kept[r]],
                            "weights": film_w[r]} for r in FILM_ROUNDS},
        "first_four_tries": [{"score": t["score"], "pushes_left": t["pushes"].count(0), "pushes_right": t["pushes"].count(1)} for t in first4],
    }, open(DATA / "rl01-cartpole.json", "w"), indent=None)
    print("first four tries:", [t["score"] for t in first4])
