# 3. LIBERO, the benchmark

After this chapter you can name the four LIBERO suites and what changes between the tasks in each, describe how a
standard evaluation is run, and explain why a 98% score doesn't show that a model reads the instruction.
Needs: chapters 1 and 2. Reading time: 10 min.
Web version, with the first picture of all 40 tasks, all 50 starting states of one task and a recorded episode: https://blueif16.github.io/vla_final/learn/03-libero.html

Picture one table in the LIBERO-Goal suite. On it are a bowl, a plate, a stove, a wine bottle, a cream cheese box and
a small cabinet with drawers. The same table, with the same objects in the same places, is used for ten different
tasks. Among them are "open the middle drawer of the cabinet", "put the bowl on the stove", "turn on the stove" and
"put the bowl on the plate". When the episode starts, the picture is the same for all ten. Only the sentence says
which one to do.

The web page opens with three recordings from that table, played side by side: the first demonstration in the
training dataset of "put the bowl on the plate", of "turn on the stove" and of "put the wine bottle on top of the
cabinet" (physical-intelligence/libero, episodes 379, 388 and 385). For the first second the three tables look alike,
give or take a few centimetres, and then the three arms go three different ways.

## What LIBERO is

LIBERO (Liu et al., 2023) is a set of 130 robot manipulation tasks in simulation. It runs on robosuite, which runs on
the MuJoCo physics engine, and the robot is a simulated Franka Panda arm. Each task comes with 50 demonstrations
recorded by a person steering the robot with a 3D mouse (a 3Dconnexion SpaceMouse, the paper says). Research on VLAs
mostly reports four suites of ten tasks each.

| Suite | What stays the same | What changes between tasks | Example instruction |
|---|---|---|---|
| LIBERO-Spatial | the objects (two identical black bowls, a plate, a ramekin and others) | where they are placed, and which bowl is meant | "pick up the black bowl between the plate and the ramekin and place it on the plate" |
| LIBERO-Object | the basket and the task type | which grocery item to pick, and the items on the floor | "pick up the alphabet soup and place it in the basket" |
| LIBERO-Goal | the scene, the objects and their positions | the goal | "put the wine bottle on top of the cabinet" |
| LIBERO-10 (also called LIBERO-Long) | nothing in particular | scene and goal; each task has two steps | "put both the alphabet soup and the tomato sauce in the basket" |

The paper's own pictures of the suites (its Figures 8 to 11, CC BY 4.0) show Spatial's ten starting tables and every
other task at its end, as its appendix C.1 says. LIBERO-10 is ten tasks of the paper's LIBERO-100, and that figure
doesn't mark which ones.

There is also LIBERO-90, the other ninety tasks of LIBERO-100. They are shorter and share kitchen, living-room and
study scenes. Several of them use the same scene, which makes LIBERO-90 a possible source of training data where the
words matter (chapter 6).

## How a standard evaluation runs

Each task is written down in one text file, its task file (in LIBERO's code these end in `.bddl`; the paper's drawing
calls them PDDL files). The file names the objects, gives each one a small region of the table to start in, and states
the goal as a goal condition the simulator can check, such as "the bowl is on the plate". The paper's Figure 2 draws
one such file, whose goal is two conditions at once: the top drawer is open, and the bowl is in it.

Each task has 50 fixed starting arrangements, its starting states, stored with the benchmark. LIBERO's README says
they were fixed for benchmarking, so every model is tested from the same ones. An evaluation runs one episode from
each, so a task gets 50 trials and a suite gets 500.

The 50 are one arrangement with small differences. We rendered all 50 for LIBERO-Spatial's "pick up the black bowl
between the plate and the ramekin and place it on the plate", each as the first picture the model receives (openpi's
10 settling steps, then the picture turned 180 degrees and shrunk to 224 pixels). The objects shift by a few
centimetres and the cabinet turns a little, but the bowl to take always sits between the plate and the ramekin. By our
reading of that task file, each object may start anywhere in a square 2 cm on a side, and the cabinet's turn varies
over 3.6 degrees. Our render of starting state 0 matches the first picture the model received in our chapter 2 run.

The simulator checks the goal condition after every step, and the episode ends as soon as it holds or when a step
limit runs out. In openpi's script the limits are 220, 280, 300 and 520 steps for Spatial, Object, Goal and LIBERO-10.
The script's comments give the longest training demonstration in each suite as 193, 254, 270 and 505 steps, so each
limit sits a little above it. In our chapter 2 run the goal condition, `(On akita_black_bowl_1 plate_1)`, held at step
104, so the episode stopped there and counted as a success. Had it never held, the episode would have stopped at step
220 as a failure. The success rate is the share of episodes that met the goal.

One run of the four-prompt plan we submitted (chapter 6) therefore comes to 4 prompts × 4 suites × 10 tasks × 50
trials = 8,000 episodes.

## Why a high score doesn't prove the words were read

In LIBERO-Spatial, LIBERO-Object and LIBERO-10, almost every task starts from its own arrangement of objects, so the
picture at the first step is usually enough to tell which task this is. A model can reach a high score by learning
"this arrangement means this motion" and never looking at the sentence.

The web page shows this with the first picture of all 40 tasks, one row per suite, each rendered by us from starting
state 0 the way the model receives it. In the Spatial, Object and LIBERO-10 rows the pictures differ. In the Goal row
all ten show one table, apart from the few-centimetre shifts every start has.

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
pictures differ. In eight of the ten Spatial tasks the starting table belongs to that task alone, so the picture points
to the right bowl as clearly as "between the plate and the ramekin" does. The stove and cabinet pair is the one place
in the suite where the words have to do the work.

LIBERO's own paper found something that fits. When its authors trained their own, much smaller policies on these
suites, giving the task's sentence as a language embedding did no better than giving a bare task number (Liu et al.,
2023, Section 1, finding 3). By our reading, a policy only needs to know which task it's on, and a number tells it
that as well as a sentence.

## What this means for our project

The plan we submitted (chapter 6) compares suites. LIBERO-Goal is the one suite where the benchmark forces the model
to read, and the other three let it get away without reading, apart from the two shared pairs. The interesting results
sit in the gap between them.

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

In questions 4 to 8, pick one answer before you open the answers. Each wrong option is a belief newcomers often
hold, and the answers say why each option is right or wrong. (On the web page, each option opens on its own.)

4. `pi05_libero` succeeds in 98.8% of LIBERO-Spatial episodes. What does that show about the word *between*?
   - A. The model understands it, because the Spatial sentences pick the bowl by where it is.
   - B. Nothing either way, because the picture already says which bowl to take in almost every Spatial task.
   - C. It ignores the words, since the picture is enough.
5. Which suite starts all ten of its tasks from the same table?
   - A. LIBERO-Spatial, since its ten tasks use the same objects.
   - B. LIBERO-Object, since every task puts something in the same basket.
   - C. LIBERO-Goal.
6. A LIBERO-Spatial episode has run for 150 steps, and the bowl still isn't on the plate. When does the episode end?
   - A. When the bowl reaches the plate, or at step 220 if it never does.
   - B. When the model decides the task is done and stops sending actions.
   - C. At step 104, the length of our run.
7. What are the 50 trials of one task?
   - A. 50 different tables, each with its own objects.
   - B. 50 new random arrangements, drawn fresh for every evaluation.
   - C. The same arrangement 50 times, with the objects shifted by a few centimetres each time, stored with the
     benchmark.
8. Why do the two shared pairs matter for our question?
   - A. Outside LIBERO-Goal, they are the only tasks whose first picture can't say which task it is, so the words
     have to.
   - B. They show a mistake in the benchmark that makes those tasks impossible.
   - C. They make LIBERO-Spatial as hard to guess as LIBERO-Goal.

<details><summary>Answers to 4 to 8, with why each option is right or wrong</summary>

4. B is right.
   - A: No, and this is the wrong belief the chapter names. Eight of the ten Spatial tasks start from a table no
     other task uses, so the picture picks the bowl as well as the sentence does. The score can't tell which of the
     two the model went by.
   - B: Right. A model can score high by learning each starting table's motion. Only the stove and cabinet pair needs
     the words, and a score over all ten tasks hides how the model did on those two.
   - C: No, that goes too far the other way. The score shows only that the model doesn't need the words for most of
     these tasks, not that it never uses them. Chapter 4 tests that.
5. C is right.
   - A: No. The objects are the same, but the two black bowls start in different places in each task, so the tables
     differ.
   - B: No. The basket stays, but each task has its own set of groceries on the floor, in its own places.
   - C: Right. All ten tasks start from one arrangement of the bowl, plate, stove, wine bottle, cream cheese and
     cabinet, so only the sentence says which task it is.
6. A is right.
   - A: Right. The simulator checks the goal condition after every step. If it holds, the episode ends as a success,
     and if it still doesn't hold at the 220-step limit, the episode ends as a failure.
   - B: No. The model has no way to stop an episode. Its actions only move the hand and open or close the gripper,
     and the simulator decides when the episode is over by checking the goal condition.
   - C: No. 104 is when the goal happened to hold in our run. A Spatial episode that hasn't reached its goal keeps
     going until step 220.
7. C is right.
   - A: No. All 50 use the same objects in the same arrangement, and only small shifts differ.
   - B: No. The 50 starting states are stored with the benchmark, so every model and every run starts from the same
     50.
   - C: Right. One episode runs from each stored state, so a task gets 50 trials and a suite gets 500.
8. A is right.
   - A: Right. In suites where the picture usually gives the task away, these four tasks can only be told apart by
     reading. Chapter 4 runs our model on the Spatial pair.
   - B: No. Every task in a pair can be done. The sentence says which bowl, or which two groceries, to take, so a
     model that reads it can succeed.
   - C: No. One pair among ten tasks still leaves eight Spatial tasks with a table of their own. In Goal, all ten
     share one.

</details>

## Sources

- Liu et al. (2023), LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning, NeurIPS Datasets and
  Benchmarks, https://arxiv.org/abs/2306.03310 and https://libero-project.github.io. Licence CC BY 4.0. Read
  2026-11-13: the SpaceMouse demonstrations (Section 4.3), a task as a starting-state distribution plus a goal
  predicate (Section 2), "The simulation terminates when all predicates are verified true" (Section 4.1), finding 3
  (Section 1), and which figures show starting or goal states (Appendix C.1).
- LIBERO's code at the commit openpi pins (f78abd6), checked 2026-11-13: the README's note that the starting states
  are fixed for benchmarking, `libero/libero/benchmark/__init__.py` (stored states in `.pruned_init` files),
  `libero/libero/envs/bddl_base_domain.py` (the goal is checked after every step) and the task files in
  `libero/libero/bddl_files/`, https://github.com/Lifelong-Robot-Learning/LIBERO
- openpi `examples/libero/main.py` (step limits and the longest-demonstration comments beside them, 50 trials per task,
  seed 7, 10 settling steps), checked 2026-11-11 and 2026-11-13, https://github.com/Physical-Intelligence/openpi
- Our comparison of the task files' starting layouts, 2026-11-11 (Goal 10 tasks from 1 layout, Spatial 10 from 9,
  Object 10 from 10, LIBERO-10 10 from 9).
- Our renders of LIBERO's stored starting states, 2026-11-13, made by `tools/ch3/render_first_frames.py` without
  running any model; the opening clip, `tools/ch3/make_goal_demos_clip.py`, from physical-intelligence/libero
  (CC BY 4.0), https://huggingface.co/datasets/physical-intelligence/libero
- Zhou et al. (2025), LIBERO-PRO, https://arxiv.org/abs/2510.03827 (the argument that LIBERO rewards memorising
  layouts)
