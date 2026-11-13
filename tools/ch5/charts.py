"""Chapter 5 web page: draw the two number charts as inline SVG and write them into the page.

Run from the repo root:  python3 tools/ch5/charts.py
It replaces what sits between <!-- ch5-chart:NAME:start --> and <!-- ch5-chart:NAME:end --> in
docs/learn/05-what-others-found.html, so the charts can be remade from the numbers below.

Numbers are copied from the source, never rounded (library/papers.yaml, key libero-cf and ch5_web_2026_11_13):
- LIBERO-CF (Fang et al. 2026, arXiv 2602.17659), Table I in v1 and v2, Table 1 in v3: pi0.5 success with
  vision and language (V+L) and with vision only, per LIBERO suite.
- LIBERO-CF v3, Table 3: pi0.5 on the LIBERO-CF benchmark, average over its four suites, faithful (the task asked
  for) and biased (the scene's original training task), without CAG and with training-free CAG (TF).

Each chart is drawn twice: a wide layout and a compact one for phones (teaching-interactives, step 9: a narrower
viewBox with bigger type instead of a shrunken wide one). ch5.css shows one of them by screen width.
"""
import re
from pathlib import Path

PAGE = Path("docs/learn/05-what-others-found.html")

GOLD, GOLD_EDGE = "#FBD45B", "#C9A533"
INK, INK2, INK3, TAN, LINE, BG = "#29271F", "#625C4B", "#746D58", "#AAA184", "#D7CFB6", "#F5F4EF"

# LIBERO-CF Table I (v1, v2) = Table 1 (v3); success rate in percent
SUITES = [  # (label, with instruction, vision only)
    ("Spatial", "98.8", "68.2"),
    ("Object", "98.2", "56.6"),
    ("Goal", "98.0", "10.2"),
    ("LIBERO-10", "92.4", "71.6"),
]
# LIBERO-CF v3 Table 3, pi0.5, Average column; (label, pi0.5 as released, with training-free CAG)
CF_ROWS = [
    ("asked", "touched the object named", "30.8", "40.5"),
    ("asked", "finished the task", "13.2", "16.8"),
    ("old", "touched the old task's object", "65.6", "59.8"),
    ("old", "finished the old task", "60.9", "43.5"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def axis(x0, x1, y_top, y_bot, ticks=(0, 25, 50, 75, 100), label_y=None, cls="tiny"):
    """Vertical gridlines with percent labels on top; recessive."""
    out = []
    for t in ticks:
        x = x0 + (x1 - x0) * t / 100
        out.append(f'<path d="M{x:.1f} {y_top}V{y_bot}" stroke="{LINE}" stroke-width="1"/>')
        out.append(f'<text class="{cls}" x="{x:.1f}" y="{label_y if label_y else y_top - 8}" text-anchor="middle">{t}%</text>')
    return out


def dot(x, y, kind, title, r=8):
    t = f"<title>{esc(title)}</title>"
    if kind == "gold":
        return f'<circle cx="{x:.1f}" cy="{y}" r="{r}" fill="{GOLD}" stroke="{GOLD_EDGE}" stroke-width="2">{t}</circle>'
    if kind == "ink":
        return f'<circle cx="{x:.1f}" cy="{y}" r="{r - 1}" fill="{INK}" stroke="{BG}" stroke-width="2">{t}</circle>'
    return f'<circle cx="{x:.1f}" cy="{y}" r="{r - 1}" fill="{BG}" stroke="{INK2}" stroke-width="2.5">{t}</circle>'


def suites_chart(compact):
    """Figure 5.2: pi0.5 with and without the instruction, per suite, with the one-in-ten guess on Goal."""
    if compact:
        W, x0, x1, top, gap = 360, 112, 336, 58, 70
        name_x, name_dy, val_cls, name_cls = 100, 5, "lbl-s", "lbl-s"
    else:
        W, x0, x1, top, gap = 720, 132, 690, 58, 52
        name_x, name_dy, val_cls, name_cls = 116, 5, "lbl-s", "sub"
    n = len(SUITES)
    y_last = top + gap * (n - 1)
    H = y_last + (92 if compact else 86)
    sx = lambda v: x0 + (x1 - x0) * float(v) / 100
    o = [f'<rect class="bg" width="{W}" height="{H}"/>']
    o += axis(x0, x1, top - 22 if compact else top - 24, y_last + 22, label_y=(top - 30 if compact else top - 32),
              cls="sub" if compact else "tiny")
    for i, (name, vl, vo) in enumerate(SUITES):
        y = top + gap * i
        o.append(f'<text class="{name_cls}" x="{name_x}" y="{y + name_dy}" text-anchor="end" style="font-size:13px">{name}</text>')
        if name == "Goal":  # the one-in-ten guess (chapter 3's arithmetic)
            gx = sx(10)
            o.append(f'<path d="M{gx:.1f} {y - 18}V{y + 18}" stroke="{INK}" stroke-width="1.6" stroke-dasharray="3 3"/>')
        o.append(f'<path d="M{sx(vo):.1f} {y}H{sx(vl):.1f}" stroke="{TAN}" stroke-width="2.5"/>')
        o.append(dot(sx(vo), y, "hollow", f"{name}, no instruction: {vo}% (LIBERO-CF Table I)"))
        o.append(dot(sx(vl), y, "gold", f"{name}, with the instruction: {vl}% (LIBERO-CF Table I)"))
        # direct labels: the instruction's value right of its dot, the no-instruction value left of its dot
        if compact:
            o.append(f'<text class="{val_cls}" x="{sx(vl):.1f}" y="{y + 27}" text-anchor="middle">{vl}</text>')
            o.append(f'<text class="{val_cls}" x="{sx(vo):.1f}" y="{y + 27}" text-anchor="middle" style="fill:{INK2}">{vo}</text>')
        else:
            o.append(f'<text class="{val_cls}" x="{sx(vl) + 13:.1f}" y="{y + 5}" style="font-size:13px">{vl}</text>' if float(vl) < 96 else
                     f'<text class="{val_cls}" x="{sx(vl):.1f}" y="{y - 13}" text-anchor="middle">{vl}</text>')
            o.append(f'<text class="{val_cls}" x="{sx(vo) - 13:.1f}" y="{y + 5}" text-anchor="end" style="fill:{INK2}">{vo}</text>')
        if name == "Goal":
            gx = sx(10)
            # below the row, clear of the connector: the dashed mark is 10%, a random pick among ten tasks
            if compact:
                o.append(f'<text class="sub" x="{gx - 4:.1f}" y="{y + 45}" style="fill:{INK}">↑ 1 in 10, a random pick</text>')
            else:
                o.append(f'<text class="tiny" x="{gx - 4:.1f}" y="{y + 31}" style="font-size:11.5px;fill:{INK}">↑ 1 in 10, picking one of the ten tasks at random</text>')
    # legend (two series, also labelled directly)
    ly = H - (30 if compact else 28)
    lx0 = 20 if compact else x0
    o.append(dot(lx0 + 7, ly, "gold", "with the instruction", r=7))
    o.append(f'<text class="{"sub" if compact else "tiny"}" x="{lx0 + 20}" y="{ly + 4}" style="fill:{INK}">with the instruction</text>')
    lx = lx0 + (190 if compact else 200)
    o.append(dot(lx, ly, "hollow", "no instruction", r=7))
    o.append(f'<text class="{"sub" if compact else "tiny"}" x="{lx + 13}" y="{ly + 4}" style="fill:{INK}">no instruction</text>')
    if not compact:
        o.append(f'<path d="M{lx + 150} {ly - 9}V{ly + 9}" stroke="{INK}" stroke-width="1.6" stroke-dasharray="3 3"/>')
        o.append(f'<text class="tiny" x="{lx + 160}" y="{ly + 4}" style="fill:{INK}">random guess on Goal</text>')
    desc = ("π0.5 success rate per LIBERO suite, from LIBERO-CF Table I. With the instruction: " +
            ", ".join(f"{s} {a}" for s, a, _ in SUITES) + ". With no instruction: " +
            ", ".join(f"{s} {b}" for s, _, b in SUITES) +
            ". On Goal the no-instruction result sits on the 10% mark of a random pick among ten tasks.")
    cls = "dg ch5-narrow" if compact else "dg ch5-wide"
    return (f'<svg class="{cls}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(desc)}">' + "".join(o) + "</svg>")


def cf_chart(compact):
    """Figure 5.6: pi0.5 on LIBERO-CF, the task asked for against the scene's old task, without and with TF-CAG."""
    if compact:
        W, x0, x1, top, gap, ggap = 360, 22, 330, 74, 62, 40
    else:
        W, x0, x1, top, gap, ggap = 720, 250, 690, 62, 40, 34
    sx = lambda v: x0 + (x1 - x0) * float(v) / 100
    ys, y = [], top
    for i, (grp, *_rest) in enumerate(CF_ROWS):
        if i and grp != CF_ROWS[i - 1][0]:
            y += ggap
        ys.append(y)
        y += gap
    y_last = ys[-1]
    H = y_last + (104 if compact else 80)
    o = [f'<rect class="bg" width="{W}" height="{H}"/>']
    if compact:   # gridlines start under the first heading; their labels sit at the bottom
        o += axis(x0, x1, top - 26, y_last + 16, label_y=y_last + 36, cls="sub")
    else:
        o += axis(x0, x1, top - 26, y_last + 18, label_y=top - 34, cls="tiny")
    ko = f';paint-order:stroke;stroke:{BG};stroke-width:5px;stroke-linejoin:round'   # text knocked out of the gridlines
    heads = {"asked": "THE TASK IT WAS ASKED FOR", "old": "THE SCENE'S OLD TASK, INSTEAD"}
    for i, (grp, label, a, b) in enumerate(CF_ROWS):
        y = ys[i]
        if i == 0 or grp != CF_ROWS[i - 1][0]:   # a group heading above the group's first row
            if compact:
                o.append(f'<text class="lbl-s" x="{x0}" y="{y - 38}" style="fill:{INK}{ko}">{heads[grp]}</text>')
            else:
                o.append(f'<text class="lbl-s" x="20" y="{y - 22}">{heads[grp]}</text>')
        if compact:
            o.append(f'<text class="sub" x="{x0}" y="{y - 14}" style="fill:{INK}{ko}">{esc(label)}</text>')
        else:
            o.append(f'<text class="sub" x="{x0 - 16}" y="{y + 4}" text-anchor="end" style="fill:{INK}">{esc(label)}</text>')
        xa, xb = sx(a), sx(b)
        d = 1 if xb > xa else -1
        o.append(f'<path d="M{xa + d * 10:.1f} {y}H{xb - d * 13:.1f}" stroke="{INK3}" stroke-width="2.2"/>')
        o.append(f'<path d="M{xb - d * 9:.1f} {y}l{-d * 7} -5v10z" fill="{INK3}"/>')
        o.append(dot(xa, y, "gold", f"{label}: {a}% for π0.5 as released (LIBERO-CF Table 3, average)"))
        o.append(dot(xb, y, "ink", f"{label}: {b}% with training-free CAG (LIBERO-CF Table 3, average)"))
        lo, hi = (a, b) if xa < xb else (b, a)
        xlo, xhi = min(xa, xb), max(xa, xb)
        cls = "lbl" if compact else "lbl-s"
        grey = f' style="fill:{INK2}"'   # the released model's value in secondary ink, CAG's in ink
        # labels outside the pair: the left value to the left of its dot, the right value to the right
        o.append(f'<text class="{cls}" x="{xlo - 13:.1f}" y="{y + 5}" text-anchor="end"{grey if lo == a else ""}>{lo}</text>')
        o.append(f'<text class="{cls}" x="{xhi + 13:.1f}" y="{y + 5}"{grey if hi == a else ""}>{hi}</text>')
    if compact:   # two legend lines, so neither runs past the edge
        ly, lx, ly2 = H - 44, x0 + 7, H - 20
    else:
        ly, lx, ly2 = H - 26, x0 + 190, H - 26
    o.append(dot(x0 + 7, ly, "gold", "π0.5 as released", r=7))
    o.append(f'<text class="{"sub" if compact else "tiny"}" x="{x0 + 20}" y="{ly + 4}" style="fill:{INK}">π0.5 as released</text>')
    o.append(dot(lx, ly2, "ink", "with training-free CAG", r=7))
    o.append(f'<text class="{"sub" if compact else "tiny"}" x="{lx + 13}" y="{ly2 + 4}" style="fill:{INK}">with training-free CAG</text>')
    desc = ("π0.5 on LIBERO-CF, average of its four suites, from LIBERO-CF Table 3. " +
            "; ".join(f"{'asked-for task' if g == 'asked' else 'old task'}, {l}: {a}% as released, {b}% with training-free CAG"
                      for g, l, a, b in CF_ROWS) + ".")
    cls = "dg ch5-narrow" if compact else "dg ch5-wide"
    return (f'<svg class="{cls}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(desc)}">' + "".join(o) + "</svg>")


def put(html, name, svg):
    pat = re.compile(rf"(<!-- ch5-chart:{name}:start -->).*?(<!-- ch5-chart:{name}:end -->)", re.S)
    if not pat.search(html):
        raise SystemExit(f"marker ch5-chart:{name} not found in {PAGE}")
    return pat.sub(lambda m: m.group(1) + "\n" + svg + "\n" + m.group(2), html)


if __name__ == "__main__":
    html = PAGE.read_text(encoding="utf-8")
    html = put(html, "suites", suites_chart(False) + "\n" + suites_chart(True))
    html = put(html, "cf", cf_chart(False) + "\n" + cf_chart(True))
    PAGE.write_text(html, encoding="utf-8")
    print("charts written into", PAGE)
