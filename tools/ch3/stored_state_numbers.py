"""Numbers behind chapter 3's figures on the task file and the stored starting states (section B, 2026-11-14).

Reads LIBERO-Spatial task 0's task file and its 50 stored starting states and prints:
  1. what one stored state holds (its 92 numbers, by position) and how far each loose object moves across the 50;
  2. SVG coordinates for the to-scale map of the start squares (figure b-taskfile);
  3. SVG dots for bowl 1's 50 stored centres inside a 5 cm window (the side note "What one stored state holds").

Light: it loads one small file with torch and parses one text file. No scene is built, nothing is rendered, no
simulator step runs. Run it in openpi's LIBERO client venv, which has torch:
    ~/openpi/examples/libero/.venv/bin/python -I tools/ch3/stored_state_numbers.py

Layout of a stored state, by our reading of the numbers and LIBERO's code (a MuJoCo state flattened as time, joint
positions, joint speeds): [0] the clock; [1:8] the arm's 7 joints; [8:10] the 2 finger joints; [10:45] five loose
objects x (x, y, z, then 4 numbers for which way it faces), in the order of the file's (:objects) block; [45:49] the
cabinet's 3 drawer slides and the stove's knob; [49:92] the 43 joint speeds. The cabinet's and the stove's place and
turn are not in it: LIBERO draws them at every reset (envs/bddl_base_domain.py, _reset_internal).
"""

import math
import pathlib
import re

import numpy as np
import torch

LIBERO = pathlib.Path.home() / "openpi/third_party/libero/libero/libero"
TASK = "pick_up_the_black_bowl_between_the_plate_and_the_ramekin_and_place_it_on_the_plate"
OBJECTS = ["akita_black_bowl_1", "akita_black_bowl_2", "cookies_1", "glazed_rim_porcelain_ramekin_1", "plate_1"]

# (:init) order in the file, which the figure numbers 1 to 7
INIT = [("akita_black_bowl_1", "between_plate_ramekin_region"), ("akita_black_bowl_2", "next_to_ramekin_region"),
        ("plate_1", "plate_region"), ("cookies_1", "box_region"), ("glazed_rim_porcelain_ramekin_1", "ramekin_region"),
        ("wooden_cabinet_1", "cabinet_region"), ("flat_stove_1", "stove_region")]

# map: 230 px per metre; left/right as in the model's (mirrored) picture: screen x = CX - S*y, screen y = CY + S*x
S, CX, CY = 230.0, 160.0, 149.0


def regions(text):
    out = {}
    for name, body in re.findall(r"\((\w+_region)\s*\(:target main_table\)\s*\(:ranges \(\s*\(([^)]*)\)", text):
        out[name] = [float(v) for v in body.split()]  # x_min y_min x_max y_max (envs/utils.py, rectangle2xyrange)
    return out


def main():
    text = (LIBERO / "bddl_files/libero_spatial" / f"{TASK}.bddl").read_text()
    reg = regions(text)
    states = np.asarray(torch.load(LIBERO / "init_files/libero_spatial" / f"{TASK}.pruned_init"))
    print("stored states:", states.shape, "| clock values:", np.unique(states[:, 0]),
          "| speeds all zero:", bool(np.all(states[:, 49:] == 0)), "| drawer and knob joints all zero:",
          bool(np.all(states[:, 45:49] == 0)))
    arm = states[:, 1:8]
    print("arm joints, spread across the 50 (radians):", np.round(arm.max(0) - arm.min(0), 4))

    print("\n1. loose objects across the 50 stored states (cm spans; z in m)")
    for i, name in enumerate(OBJECTS):
        b = 10 + 7 * i
        x, y, z = states[:, b], states[:, b + 1], states[:, b + 2]
        q = states[:, b + 3:b + 7]
        print(f"  {name:32s} x span {100 * np.ptp(x):.2f} cm, y span {100 * np.ptp(y):.2f} cm, z {z.min():.2f}..{z.max():.2f},"
              f" faces the same way in all 50: {bool(np.allclose(q, q[0]))}")

    print("\n2. map squares (figure b-taskfile), 2 cm =", round(0.02 * S, 2), "px")
    for k, (obj, r) in enumerate(INIT, 1):
        x0, y0, x1, y1 = reg[r]
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        X, Y = CX - S * cy, CY + S * cx
        w, h = S * (y1 - y0), S * (x1 - x0)
        print(f"  {k} {obj:32s} {r:30s} ranges {reg[r]} -> square x={X - w / 2:.1f} y={Y - h / 2:.1f} w={w:.1f} h={h:.1f}")
    yaw = re.search(r"\(:yaw_rotation \(\s*\(([^)]*)\)", text).group(1).split()
    a, b = (float(v) for v in yaw)
    print(f"  cabinet yaw range {a}..{b} rad = {math.degrees(b - a):.4f} degrees wide (our conversion)")

    print("\n3. bowl 1's 50 stored centres in a 5 cm window (40 px per cm, mirrored like the picture)")
    rx = reg["between_plate_ramekin_region"]
    mx, my = (rx[0] + rx[2]) / 2, (rx[1] + rx[3]) / 2
    K, OX, OY = 4000.0, 130.0, 120.0
    dots = []
    for x, y in states[:, 10:12]:
        dots.append(f'<circle cx="{OX - K * (y - my):.1f}" cy="{OY + K * (x - mx):.1f}" r="3"/>')
    print("  " + "".join(dots))
    print(f"  region square: x={OX - K * (rx[3] - my):.1f} y={OY + K * (rx[0] - mx):.1f} side={K * 0.02:.0f}")


if __name__ == "__main__":
    main()
