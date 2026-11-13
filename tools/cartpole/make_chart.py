"""Draw RL 1's figure 1.5 chart (average score per round) from docs/assets/data/rl01-cartpole.json and write it into
the page between <!-- run-chart:start --> and <!-- run-chart:end -->. Run from the repo root after train_and_film.py."""
import json, statistics as st, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGE = ROOT / "docs/learn/rl-01-learning-from-a-score.html"
d = json.load(open(ROOT / "docs/assets/data/rl01-cartpole.json"))
avg = {s: [round(st.mean(r), 1) for r in rounds] for s, rounds in d["scores"].items()}
main, others = avg[str(d["filmed_seed"])], [v for s, v in avg.items() if s != str(d["filmed_seed"])]
W, H, x0, x1, y0, y1, MAX = 640, 272, 52, 616, 236, 22, 500
n = len(main)
X = lambda i: x0 + i / (n - 1) * (x1 - x0)
Y = lambda v: y0 - v / MAX * (y0 - y1)
pts = lambda ys: " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(ys))
g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="f15t f15d">',
     '<title id="f15t">Average score per round, 300 rounds</title>',
     f'<desc id="f15d">The average score of each round of 16 tries. The run we filmed starts at {main[0]} in round 1 and ends at '
     f'{main[-1]} in round {n}. Two more runs of the same rule end at {others[0][-1]} and {others[1][-1]}. The most a try can score is 500.</desc>']
for v in range(0, MAX + 1, 100):
    g.append(f'<line class="grid" x1="{x0}" x2="{x1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>')
    g.append(f'<text x="{x0 - 8}" y="{Y(v) + 4:.1f}" text-anchor="end">{v}</text>')
for r in (1, 100, 200, 300):
    g.append(f'<text x="{X(r - 1):.1f}" y="{y0 + 20}" text-anchor="middle">{"round " if r == 1 else ""}{r}</text>')
for o in others:
    g.append(f'<polyline class="other" points="{pts(o)}"/>')
g.append(f'<polyline class="main" points="{pts(main)}"/>')
g.append(f'<text class="lab-main" x="{X(0) + 6:.1f}" y="{Y(main[0]) - 10:.1f}">{main[0]}</text>')
g.append(f'<text class="lab-main" x="{x1}" y="{y1 - 8}" text-anchor="end">round {n}: {main[-1]}</text>')
lx, ly = x0 + 16, y1 + 24
g.append(f'<g class="lgd"><line class="main" x1="{lx}" x2="{lx + 26}" y1="{ly}" y2="{ly}"/><text x="{lx + 34}" y="{ly + 4}">the run we filmed</text>')
g.append(f'<line class="other" x1="{lx}" x2="{lx + 26}" y1="{ly + 26}" y2="{ly + 26}"/><text x="{lx + 34}" y="{ly + 30}">the same rule, two more runs</text></g>')
g.append(f'<text class="ttl" x="{x0}" y="{y1 - 8}">average score of the round\'s 16 tries</text>')
g.append('</svg>')
g.append('<script type="application/json">' + json.dumps({"frame": {"x0": x0, "x1": x1, "y0": y0, "y1": y1, "max": MAX}, "main": main}) + '</script>')
html = PAGE.read_text()
new = re.sub(r"(<!-- run-chart:start -->).*?(<!-- run-chart:end -->)", lambda m: m.group(1) + "\n" + "\n".join(g) + "\n" + m.group(2), html, flags=re.S)
assert new != html or "run-chart:start" in html, "markers missing"
PAGE.write_text(new)
print("chart written:", main[0], "->", main[-1], "| others end", [o[-1] for o in others])
