"""Draw a Go position from an SGF as an SVG: the stones after move N, with move N ringed.
Captures are applied. Used for RL 1, figure 1.10 (AlphaGo vs Lee Sedol, game 2, move 37).
Run from the repo root:  python3 tools/go/board.py tools/go/alphago-lee-sedol-game2.sgf 37 docs/assets/img/rl/alphago-game2-move37.svg
The game record is from homepages.cwi.nl/~aeb/go/games/games/AlphaGo/LeeSedol/2.sgf (checked 2026-11-13)."""
import re, sys

sgf, upto, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
moves = re.findall(r";([BW])\[([a-s]{2})\]", open(sgf).read())[:upto]
N, board = 19, {}

def group(p):
    col, seen, todo, libs = board[p], {p}, [p], set()
    while todo:
        x, y = todo.pop()
        for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if not (0 <= q[0] < N and 0 <= q[1] < N): continue
            if q not in board: libs.add(q)
            elif board[q] == col and q not in seen: seen.add(q); todo.append(q)
    return seen, libs

for c, s in moves:
    p = (ord(s[0]) - 97, ord(s[1]) - 97)
    board[p] = c
    for q in ((p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)):
        if q in board and board[q] != c:
            g, libs = group(q)
            if not libs:
                for r in g: del board[r]

S, M = 20, 34                     # spacing and margin in SVG units
W = M * 2 + S * (N - 1)
X = lambda i: M + i * S
cols = "ABCDEFGHJKLMNOPQRST"
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" role="img" aria-labelledby="gt gd">',
     f'<title id="gt">The board after move {upto}</title>',
     f'<desc id="gd">The position after move {upto} of game 2, AlphaGo (black) against Lee Sedol (white), 10 March 2016. '
     f'Move {upto}, a black stone, is ringed.</desc>',
     f'<rect width="{W}" height="{W}" rx="10" fill="#E8C98A"/>']
for i in range(N):
    o.append(f'<line x1="{X(0)}" y1="{X(i)}" x2="{X(N-1)}" y2="{X(i)}" stroke="#5E5444" stroke-width="1"/>')
    o.append(f'<line x1="{X(i)}" y1="{X(0)}" x2="{X(i)}" y2="{X(N-1)}" stroke="#5E5444" stroke-width="1"/>')
    o.append(f'<text x="{X(i)}" y="{M - 14}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="10" fill="#5E5444">{cols[i]}</text>')
    o.append(f'<text x="{M - 16}" y="{X(i) + 3.5}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="10" fill="#5E5444">{N - i}</text>')
for a in (3, 9, 15):
    for b in (3, 9, 15):
        o.append(f'<circle cx="{X(a)}" cy="{X(b)}" r="2.6" fill="#5E5444"/>')
last = (ord(moves[-1][1][0]) - 97, ord(moves[-1][1][1]) - 97)
for (x, y), c in sorted(board.items()):
    fill, edge = ("#2B2620", "#2B2620") if c == "B" else ("#FFFDF7", "#5E5444")
    o.append(f'<circle cx="{X(x)}" cy="{X(y)}" r="9.2" fill="{fill}" stroke="{edge}" stroke-width="1"/>')
lx, ly = X(last[0]), X(last[1])
o.append(f'<circle cx="{lx}" cy="{ly}" r="14.5" fill="none" stroke="#9A4824" stroke-width="3"/>')
o.append(f'<text x="{lx}" y="{ly + 3.8}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="10.5" font-weight="700" fill="#FFFDF7">{upto}</text>')
o.append("</svg>")
open(out, "w").write("\n".join(o) + "\n")
print(out, "stones on board:", len(board), "last move:", moves[-1][0], cols[last[0]] + str(N - last[1]))
