# 3. LIBERO, the benchmark

After this chapter you can name the four LIBERO suites and what changes between the tasks in each, describe how a
standard evaluation is run, and explain why a 98% score doesn't show that a model reads the instruction.
Needs: chapters 1 and 2. Reading time: 8 min.

Picture one table in the LIBERO-Goal suite. On it are a bowl, a plate, a stove, a wine bottle, a cream cheese box and
a small cabinet with drawers. The same table, with the same objects in the same places, is used for ten different
tasks. Among them are "open the middle drawer of the cabinet", "put the bowl on the stove", "turn on the stove" and
"put the bowl on the plate". When the episode starts, the picture is the same for all ten. Only the sentence says
which one to do.

## What LIBERO is

LIBERO (Liu et al., 2023) is a set of 130 robot manipulation tasks in simulation. It runs on robosuite, which runs on
the MuJoCo physics engine, and the robot is a simulated Franka Panda arm. Each task comes with 50 demonstrations
recorded by a person steering the robot. Research on VLAs mostly reports four suites of ten tasks each.

| Suite | What stays the same | What changes between tasks | Example instruction |
|---|---|---|---|
| LIBERO-Spatial | the objects (two identical black bowls, a plate, a ramekin and others) | where they are placed, and which bowl is meant | "pick up the black bowl between the plate and the ramekin and place it on the plate" |
| LIBERO-Object | the basket and the task type | which grocery item to pick, and the items on the floor | "pick up the alphabet soup and place it in the basket" |
| LIBERO-Goal | the scene, the objects and their positions | the goal | "put the wine bottle on top of the cabinet" |
| LIBERO-10 (also called LIBERO-Long) | nothing in particular | scene and goal; each task has two steps | "put both the alphabet soup and the tomato sauce in the basket" |

There is also LIBERO-90, ninety shorter tasks that share kitchen, living-room and study scenes. Several of its tasks
use the same scene, which makes it a possible source of training data where the words matter (chapter 6).

## How a standard evaluation runs

Each task has 50 fixed starting arrangements stored with the benchmark. An evaluation runs one episode from each, so
a task gets 50 trials and a suite gets 500. The simulator checks a goal condition (the bowl is on the plate, the drawer
is open) and the episode ends when it holds or when a step limit runs out. In openpi's script the limits are 220, 280,
300 and 520 steps for Spatial, Object, Goal and LIBERO-10, set just above the longest human demonstration in each. The
success rate is the share of episodes that met the goal.

One run of our four-prompt plan therefore comes to 4 prompts × 4 suites × 10 tasks × 50 trials = 8,000 episodes.

## Why a high score doesn't prove the words were read

In LIBERO-Spatial, LIBERO-Object and LIBERO-10, almost every task starts from its own arrangement of objects, so the
picture at the first step is usually enough to tell which task this is. A model can reach a high score by learning
"this arrangement means this motion" and never looking at the sentence.

We checked each task's starting layout in LIBERO's task files, and found two exceptions. In LIBERO-Spatial, "pick up
the black bowl on the stove" and "pick up the black bowl on the wooden cabinet" start from the same table. One black
bowl sits on the stove and an identical one sits on the cabinet, so the picture can't say which one to take. In
LIBERO-10, "put both the alphabet soup and the tomato sauce in the basket" and "put both the cream cheese box and the
butter in the basket" also start from the same table. For each of these pairs, only the sentence tells the two tasks
apart.

LIBERO-Goal is the exception. All ten tasks share one picture, so a model that ignores the sentence has to guess. If
it picked one of the ten tasks at random, it would succeed about one time in ten. This is our own arithmetic; chapter
5 shows a published number that matches it.

A newcomer often reads "98% on LIBERO-Spatial" as "the model understands spatial words like *between*". The
arrangement test above shows why that doesn't follow. The model only has to tell ten arrangements apart, and the
pictures differ.

## What this means for our project

Our plan compares suites. LIBERO-Goal is the one place where the benchmark forces the model to read, and the other
three suites let it get away without reading. The interesting results sit in the gap between them.

## Check yourself

1. In which suite must a model read the instruction to succeed, and why?
2. How many episodes does one full evaluation of one suite under one prompt take?
3. A model scores 98% on LIBERO-Spatial. Explain why that doesn't show it understands "between the plate and the
   ramekin".

<details><summary>Answers</summary>

1. LIBERO-Goal. All ten tasks start from the same scene, so only the sentence tells them apart.
2. 500 (10 tasks × 50 trials).
3. The "between the plate and the ramekin" task starts from its own arrangement of objects, so the picture alone
   identifies the task. The model can map arrangements to motions without using the words.

</details>

## Sources

- Liu et al. (2023), LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning, NeurIPS Datasets and
  Benchmarks, https://arxiv.org/abs/2306.03310 and https://libero-project.github.io
- openpi `examples/libero/main.py` (step limits, 50 trials per task, seed 7), checked 2026-11-11,
  https://github.com/Physical-Intelligence/openpi
- Zhou et al. (2025), LIBERO-PRO, https://arxiv.org/abs/2510.03827 (the argument that LIBERO rewards memorising
  layouts)
