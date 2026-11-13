# Experiment 1, first answer: two tasks, one table

Run on 2026-11-11 on our desktop GPU, with the official `pi05_libero` checkpoint and openpi's settings (5 of 10
actions run per call, 10 settling steps, a 220-step limit, seed 7). Raw records are in
`../runs/exp1-shared-table/episodes.jsonl`. The videos stay on our machine.

## The question

Two LIBERO-Spatial tasks start from the same table, with one black bowl on the stove and an identical one on top of
the wooden cabinet. Task 7 says "pick up the black bowl on the stove and place it on the plate", and task 9 says "…on
the wooden cabinet…". The picture can't tell the robot which bowl to take. Only the sentence can. So if we erase the
sentence, does the robot still take the right bowl?

Our guess beforehand was that it would keep making one familiar move, take the same bowl every time, and get about
half of the episodes right.

## What we ran

| Condition | Instruction sent | Episodes |
|---|---|---|
| original | the task's own sentence | 10 per task (starting states 0–9) |
| blank | an empty string | 10 per task (starting states 0–9) |
| blank, counted | an empty string | 10 per task (starting states 10–19), with more checks |

The simulator checked, at every step, whether either bowl was on the plate. In the counted run it also checked
whether the cookie box was on the plate, whether the stove bowl or the cookie box had been lifted, and whether the top
drawer was open. In the first two runs an episode stopped as soon as a bowl reached the plate. The counted run went
to the end, unless the task itself succeeded.

## Results

| Condition | Success | 95% interval |
|---|---|---|
| original instruction | 19 of 20 (95%) | 76–99% |
| blank instruction | 8 of 40 (20%) | 10–35% |

With its own sentence, the robot took the right bowl every time on task 7 (10 of 10) and 9 times out of 10 on task 9.
In the one miss, no bowl reached the plate.

With the sentence erased, the robot usually didn't finish anything. In the 20 counted episodes it ended like this:

| What ended on the plate | Task 7 (stove bowl wanted) | Task 9 (cabinet bowl wanted) |
|---|---|---|
| the stove bowl | 3 | 5 |
| the cabinet bowl | 0 | 1 |
| the cookie box | 2 | 1 |
| none of the checked objects | 5 | 3 |

The last row isn't "nothing". The ramekin wasn't one of the checked objects, and in the videos two of task 7's
five (starting states 10 and 13) end with the ramekin on the plate. That was seen in the last frames on 2026-11-13,
not checked by the simulator.

Across all 40 blank episodes, a bowl reached the plate 15 times. It was the stove bowl 12 times and the cabinet bowl 3
times.

## What we read from it

These readings are ours.
- **The words decide this pair.** With the sentence, 95% success. Without it, 20%. On these two tasks the model
  clearly uses the instruction to choose the bowl, unlike the picture-only shortcut that the published average
  suggests for LIBERO-Spatial as a whole (68.2% with no instruction, LIBERO-CF Table I).
- **Our guess was wrong in an interesting way.** We expected the robot to keep doing a familiar bowl move and get
  about half right. Instead it mostly stalled, or did something no task asks for. Three times out of 20 it put the
  cookie box on the plate, and in the earlier blank run we saw it open the cabinet's top drawer twice. Every
  LIBERO-Spatial task ends with "place it on the plate", and the robot still moved things toward the plate, just not
  the right thing.
- **When it did take a bowl, it preferred the one on the stove** (12 of 15). We don't know why yet. One guess is that
  the stove spot is closer to the arm's starting pose.
- **A blank instruction is something the model never saw in training.** Every training example came with its task's
  sentence (`prompt_from_task=True` in the `pi05_libero` config), so part of what we see may be the model reacting
  to an unfamiliar input, as well as to missing information. Experiment 1's other arm, another task's sentence, would
  separate the two.

## Limits

- 10 episodes per task and condition give wide intervals; the blank rate could be anywhere from 10% to 35%.
- The "lifted" check counts the cabinet bowl as lifted from the first step, because it already sits above the table,
  so we use that check only for the stove bowl and the cookie box.
- The first blank run didn't check the cookie box or the drawer. We saw cookie-box and drawer endings in its videos,
  but only the counted run's numbers are machine-checked.

## What it cost

A successful episode took 11.7 s on average and a full 220-step episode 24.3 s, at 0.19 s per model call. Building a
scene took about 4 s once cached. At that rate the full LIBERO-Spatial reproduction (500 episodes, mostly successes)
should take under 2 hours on this machine.
