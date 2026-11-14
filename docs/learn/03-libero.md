# 3. LIBERO, the benchmark

After this chapter you can name the four LIBERO suites and what changes between the tasks in each, describe how a
standard evaluation is run, and explain why a 98% score doesn't show that a model reads the instruction.
Needs: chapters 1 and 2. Reading time: 20 min.
Web version, with the pictures, diagrams and side notes this text describes: https://blueif16.github.io/vla_final/learn/03-libero.html

Picture one table in the LIBERO-Goal suite. On it are a bowl, a plate, a stove, a wine bottle, a wine rack, a cream
cheese box and a small cabinet with drawers. The same table, with the same objects in the same places, is used for ten
different tasks. Among them are "open the middle drawer of the cabinet", "put the bowl on the stove", "turn on the
stove" and "put the bowl on the plate".

One try at one of these tasks is called an episode. During an episode our model is called again and again, and each
time it gets two camera pictures and the task's sentence (chapter 2). When an episode starts, both pictures look the
same for all ten tasks, apart from objects shifted by a few centimetres. Only the sentence says which task to do.

> **Side note: what the model gets.** The web page shows the two pictures at the first step of a recording on this
> table: the table camera, which sees the table and the robot from the front, and the wrist camera, which looks down on
> the same table from the robot's hand (physical-intelligence/libero, episode 379, step 0). The model gets two fresh
> pictures and the sentence at every call, returns 10 actions, and the robot runs the first 5. When this chapter says
> "the first picture", it means the table camera's picture at the start of an episode.

The web page then plays three recordings made at that table, side by side: the first demonstration in the training
dataset of "put the bowl on the plate", of "turn on the stove" and of "put the wine bottle on top of the cabinet"
(physical-intelligence/libero, episodes 379, 388 and 385). For the first second the three tables look alike, give or
take a few centimetres, and then the three arms go three different ways. Each frame of the clip is one step of the
simulation, which runs 20 steps per simulated second. The clip plays 10 frames a second, half the simulation's speed,
and it skips the moments when the person held the mouse still, because those steps were cut from the dataset.

Each of these recordings is one episode. `pi05_libero`'s training data is made of episodes like them, and a test is an
episode too, with the model steering the arm instead of a person. Either way, the episode ends at a point the
simulator can check.

> **Side note: what an episode is.** On the web page, the first and last pictures of the "put the bowl on the plate"
> recording (step 0, and step 111 with the bowl on the plate), and two timelines. In a test the model drives: the
> episode starts from one of the task's stored starting tables and ends when the goal holds (a success) or when the
> step limit runs out (a failure). In a recording a person drives: the episode starts from a newly set-up table, and
> LIBERO's recording script stops once the goal has held for 10 steps and saves the recording. Each saved step pairs the
> two pictures with the action the person took at that moment. `pi05_libero` learned from 1,693 such episodes, all of
> them successes. A test scores the episodes the model drives itself, and a later figure follows one to its end. RL 1
> calls one scored try an episode too. (LIBERO's `scripts/collect_demonstration.py`, OpenVLA's
> `experiments/robot/libero/regenerate_libero_dataset.py`, openpi's `examples/libero/main.py`, read 2026-11-14.)

## What LIBERO is

LIBERO (Liu et al., 2023) is a benchmark of 130 tasks for a robot arm in simulation, such as putting a bowl on a
plate, opening a drawer or turning on a stove. Its authors grouped the tasks into suites, and VLA papers mostly report
four of them, each with ten tasks. **`pi05_libero` was trained on the 40 tasks of those four suites, and it is tested
on the same 40.** The other ninety tasks make up LIBERO-90, which it never trained on.

The web page draws the 130 tasks as one square each: four rows of ten for LIBERO-Spatial, LIBERO-Object, LIBERO-Goal
and LIBERO-10, the 40 tasks `pi05_libero` trained on and is tested on, and nine rows of ten for LIBERO-90, which isn't
in its training data. LIBERO-100 is LIBERO-10 and LIBERO-90 together (our count of LIBERO's task files, one `.bddl`
file per task in five folders, 2026-11-14; the split from the paper's Section 4.2).

Everything in LIBERO is simulated, and three layers of software share the work. At the bottom, the MuJoCo physics
engine works out how everything moves. robosuite is built on MuJoCo and adds the robot arm, the cameras and the step
that applies one action. LIBERO is built on robosuite and adds the scenes, the objects, the task files and the check
that a task is done. The model never touches any of this directly. It only receives the pictures and sends back
actions. On the web page a diagram stacks the three layers, with the model outside them: openpi's evaluation script
carries two pictures and the sentence up to it and its actions back down.

The simulated arm copies a real robot arm, the Franka Panda. Each task comes with 50 demonstrations, which a person
recorded by steering the simulated arm with a 3D mouse, a puck you push, lift and twist. The three in the clip are
among them.

> **Side note: the real arm and the 3D mouse.** LIBERO's arm is robosuite's model of the Panda, an arm designed by
> Franka Emika; the web page shows a photo of an arm from the same maker at a trade fair in 2017 ("Franka Emika2" by
> Ims, CC BY-SA 4.0, Wikimedia Commons). The paper says the demonstrations were steered with a 3Dconnexion SpaceMouse,
> and the page shows another 3D mouse from that maker ("3Dconnexion with hand…" by Jiří Sedláček, CC BY-SA 3.0,
> Wikimedia Commons). Pushing the cap moves the robot's hand, twisting it turns the hand, and holding a button closes
> the gripper. Those are the seven numbers of an action: three to move, three to turn, one for the gripper (robosuite's
> `devices/spacemouse.py`, read 2026-11-14).

`pi05_libero`'s training data doesn't hold all 50 recordings of every task. It holds 1,693 for its 40 tasks
(chapter 2). Before openpi trained on them, the OpenVLA team replayed every recording in the simulator to save its
pictures at 256 × 256 pixels instead of 128 × 128. They cut out the steps where the person held the mouse still, and
they kept only the replays that still ended in success. By our count of the dataset, that left between 29 and 50
recordings per task.

The four ten-task suites differ in what stays the same from one task to the next.

| Suite | What stays the same | What changes between tasks | Example instruction |
|---|---|---|---|
| LIBERO-Spatial | a plate, a ramekin, a cookie box, a stove and a cabinet, each in its place | where two identical black bowls stand, and which of them is meant | "pick up the black bowl between the plate and the ramekin and place it on the plate" |
| LIBERO-Object | the basket in its place, and the job: pick up one grocery item and put it in the basket | which item to pick, and the other items on the floor around it | "pick up the alphabet soup and place it in the basket" |
| LIBERO-Goal | the scene, the objects and their positions | the goal | "put the wine bottle on top of the cabinet" |
| LIBERO-10 (also called LIBERO-Long) | nothing; its ten tasks use nine scenes in kitchens, living rooms and a study | the scene and the goal; nine of the ten sentences ask for two things | "turn on the stove and put the moka pot on it" |

> **Side note: what the suites were built for.** LIBERO was made to study lifelong learning, a robot that keeps
> learning new tasks one after another and carries what it knows from one task to the next. The paper says each
> ten-task suite tests whether one kind of knowledge carries over: where things are, which objects, or what the goal
> is. VLA papers use the suites differently. OpenVLA's team trained one model per suite and openpi one on all four,
> and both report how often the model succeeds. (Liu et al. 2023, Figure 1 and Section 1; the OpenVLA and openpi READMEs, read
> 2026-11-14.)

The web page shows one task from each suite in the first picture the model gets, with the objects named in its
sentence marked: the two identical bowls, the ramekin and the plate for Spatial; the alphabet soup and the basket for
Object; the wine bottle and the cabinet for Goal; the stove and the moka pot for the LIBERO-10 kitchen task. These
pictures are mirror images, like the clip. The cabinets stand at the right of the table there, while LIBERO's paper
shows them at the left. Every picture in `pi05_libero`'s LIBERO training data was flipped this way, and so is every
picture it gets in a test.

> **Side note: why the pictures are mirrored.** robosuite hands back each camera picture upside down, because a setting
> in it (`IMAGE_CONVENTION = "opengl"` in `macros.py`) keeps the rows in the order the renderer writes them, bottom row
> first. Flipped top to bottom, the picture shows the camera's view, which is what LIBERO's paper prints. openpi turns
> each picture half a turn instead (`[::-1, ::-1]`, "rotate 180 degrees to match train preprocessing"), because the
> training pictures got the same half turn when OpenVLA's team converted the data (moojink/rlds_dataset_builder). Half a
> turn flips a picture top to bottom and left to right. The first flip undoes the upside-down picture, and the second
> is left over, so the model gets a mirror image. Writing shows it: on a milk carton seen by the wrist camera in a
> training picture (episode 851, step 70) the word Milk reads backwards, and one flip makes it read right, which never
> happens with a picture that is only turned. Words for sides go through the flip too. In a recording of "put the
> chocolate pudding to the right of the plate" (episode 1), the pudding ends up left of the plate in the model's
> picture. (Our reading of robosuite 1.4.1, OpenVLA's notes and openpi's `main.py`, 2026-11-14.)

LIBERO's paper prints its own pictures of the suites, the camera's way round (its Figures 8 to 11, CC BY 4.0): Spatial's
ten tasks at their start, and every other task at its end. The web page keeps them in a "go deeper" rail.

LIBERO-90 holds the other ninety tasks of LIBERO-100. The paper describes them as short tasks and LIBERO-10's as long
ones. By our count of the task files, LIBERO-90's tasks start from just 20 tables in kitchens, living rooms and
studies, with between 2 and 7 tasks starting from the same arrangement on each table. On those tables, as in
LIBERO-Goal, only the sentence says which task to do.

`pi05_libero` never trained on LIBERO-90. Using LIBERO-90, or data like it, to train a model that has to read the words
is one of the options listed in chapter 6, and nothing about it has been decided.

> **Side note: LIBERO-90's 20 tables.** Ten kitchens with 5, 7, 4, 6, 5, 2, 3, 2, 6 and 6 tasks each, six living rooms
> with 4, 5, 5, 5, 4 and 4, and four studies with 4, 4, 5 and 4. Within each scene the task files list the same
> objects, regions and `(:init)` block (our comparison, 2026-11-14).

## How a standard evaluation runs

This section follows one task from its file to its score. It's the task from our chapter 2 run, LIBERO-Spatial's
"pick up the black bowl between the plate and the ramekin and place it on the plate".

Each LIBERO task is written down in one text file, its task file. The file lists the objects on the table and gives
each one a small square of the table to start in. It also states the goal as a goal condition the simulator can check,
which for our task is that the bowl is on the plate.

The squares are small. Each one is 2 cm on a side, on a table 1.2 m wide, so the file leaves an object very little room
to move from one start to the next. The sentence the model gets doesn't come from inside the file. LIBERO's code makes
it from the file's name, by turning the underscores into spaces.

> Side note: PDDL or BDDL? LIBERO's paper draws its task files as `*.pddl` (its Figure 2, which shows another task),
> after PDDL, the language AI planning programs read. In LIBERO's code the files end in `.bddl`, for the Behavior
> Domain Definition Language from Stanford's BEHAVIOR benchmark, which borrows PDDL's ideas. LIBERO reads its files with
> BDDL's own parser (`envs/bddl_utils.py` imports the `bddl` package; checked 2026-11-14).

The web page shows the real task file of our task
(`libero/libero/bddl_files/libero_spatial/pick_up_the_black_bowl_between_the_plate_and_the_ramekin_and_place_it_on_the_plate.bddl`),
cut to its four parts, next to the first picture the model got and a map of the start squares drawn to scale. The four
parts, as the file writes them:

```
(:fixtures
  main_table - table
  wooden_cabinet_1 - wooden_cabinet
  flat_stove_1 - flat_stove
)
(:objects
  akita_black_bowl_1 akita_black_bowl_2 - akita_black_bowl
  cookies_1 - cookies
  glazed_rim_porcelain_ramekin_1 - glazed_rim_porcelain_ramekin
  plate_1 - plate
)
(:regions
  (plate_region (:target main_table)
    (:ranges ((0.05 0.19 0.07 0.21))))
  (between_plate_ramekin_region (:target main_table)
    (:ranges ((-0.06 0.19 -0.04 0.21))))
  (cabinet_region (:target main_table)
    (:ranges ((0.02 -0.28 0.04 -0.26)))
    (:yaw_rotation ((2.6613777765410678 2.7242096296128633))))
  … 13 more regions
)
(:init
  (On akita_black_bowl_1 main_table_between_plate_ramekin_region)
  (On akita_black_bowl_2 main_table_next_to_ramekin_region)
  (On plate_1 main_table_plate_region)
  (On cookies_1 main_table_box_region)
  (On glazed_rim_porcelain_ramekin_1 main_table_ramekin_region)
  (On wooden_cabinet_1 main_table_cabinet_region)
  (On flat_stove_1 main_table_stove_region)
)
(:goal
  (And (On akita_black_bowl_1 plate_1))
)
```

- **What's on the table.** Fixtures stay where they're put: the table, a cabinet with three drawers and a stove. The
  five objects can be moved: two identical black bowls, a cookie box, a ramekin (a small cup) and a plate.
- **Where each thing may start.** A region's four numbers are where it starts and ends along the table's two
  directions, in metres from the middle of the table (our reading of `envs/utils.py`, `rectangle2xyrange`: x from, y
  from, x to, y to). So each of these regions is a square 2 cm on a side. The cabinet's region also lets it turn, within
  a range 3.6 degrees wide (our conversion from radians). The file lists 16 regions and uses 7, and all ten Spatial
  files carry this same list.
- **Where each thing does start.** One line per thing, naming the region it starts in. The ten Spatial tasks differ
  here, in which regions the two bowls start in.
- **What counts as done.** Bowl 1 on the plate. All ten Spatial tasks have this same goal line.

The file's own `(:language …)` line, which reads "Pick the akita black bowl between the plate and the ramekin and place
it on the plate", isn't shown, because LIBERO never sends it to the model (`benchmark/__init__.py`,
`grab_language_from_filename`).

Each task also comes with 50 fixed starting arrangements, its starting states. LIBERO's authors made them once, inside
the task file's squares, and saved all 50 in one file per task that ships with LIBERO's code (a `.pruned_init` file in
`libero/libero/init_files/`). The program that made them isn't in LIBERO's repository, so we can't say exactly how they
were drawn.

The web page draws the path from the file to the first picture in five steps. (1) The task file gives each object its
2 cm square and states the goal. (2) LIBERO's authors saved 50 starting states, 92 numbers each. (3) At the start of an
episode, the script builds the table and loads one stored state. (4) It sends a do-nothing action 10 times while the
objects fall into place, and these steps aren't counted. (5) It takes the first picture, turns it 180 degrees and
shrinks it to 224 × 224 pixels, and sends it to the model with the wrist camera's picture and the sentence. Steps 1 and
2 were done once; steps 3 to 5 happen at the start of every episode.

Every episode starts the same way in openpi's evaluation script, the program Physical Intelligence published to run
LIBERO against the model. Our own runs use a copy of it. The script builds the table from the task file and then loads
one stored state, which puts the arm and the five loose objects where that state says.

Every loose object is stored at the same height, 0.97 m, whatever its shape, and a comment in openpi's script says the
simulator drops the objects. So the script sends a do-nothing action for 10 steps while they fall. Only then does it
take the first picture, turn it 180 degrees and shrink it to 224 × 224 pixels for the model. None of those 10 steps
counts toward the episode's length.

LIBERO's README says the starting states are fixed for benchmarking. If every run drew new arrangements, two models
could be tested on different tables. With stored ones, every model gets the same 50 for each task, apart from the
cabinet's and the stove's exact place. An evaluation runs one episode from each starting state, so a task gets 50 trials
and a suite gets 500. A trial is what openpi's script calls one of these episodes. Running all 50 turns a task's single
yes or no into a rate.

> Side note: what one stored state holds. A row of 92 numbers: the arm's seven joints and two fingers, where each of the
> five loose objects is and which way it faces, the cabinet's three drawers and the stove's knob, and 43 speeds, which
> are all zero. By our reading of the stored file, each loose object's centre moves over about 3 cm each way across the
> 50 (2.59 to 2.99 cm), a little more than its 2 cm square, and the objects always face the same way. The arm's joints
> differ by up to 0.1009 radians, about 6 degrees. The web page plots bowl 1's centre in all 50 states against its
> square (tools/ch3/stored_state_numbers.py).

The web page shows all 50 starting states of our task, each as the first picture the model gets from it. The bowl to
take always sits between the plate and the ramekin. From picture to picture the loose objects shift by up to about 3 cm.
The cabinet also stands at a slightly different angle, because LIBERO doesn't store the cabinet and the stove. It places
them again, inside their squares, at every reset (`envs/bddl_base_domain.py`, `_reset_internal`), a fact openpi's script
notes in a comment beside its random seed: the seed "seems to affect object positions even when using fixed initial
state". Our render of state 0 matches the first picture the model got in our chapter 2 run.

Once the first picture is taken, the episode moves in steps. In each step the simulator applies one action, the seven
numbers the model sent, for 1/20 of a simulated second. The model is called once every 5 steps, as in chapter 2, so our
run's 104 steps took 21 calls and 5.2 seconds of simulated time (our arithmetic). Between two calls the model sees
nothing new. The robot runs the 5 actions it was given, and the next pictures arrive with the next call. Simulated
seconds aren't clock seconds. In our own runs a successful LIBERO-Spatial episode took 11.7 seconds on the clock, on
average.

> Side note: what a step is. MuJoCo computes each step in 25 small updates of 0.002 s (robosuite 1.4.1,
> `control_freq=20`, `SIMULATION_TIMESTEP = 0.002`). The web page shows the wrist pictures of two calls in a row from our
> run, call 7 at step 35 and call 8 at step 40, a quarter of a second apart. Between them the hand moved down and the
> gripper closed on the bowl.

After every step, the simulator checks the goal condition. The episode ends as soon as the condition holds, or when a
step limit runs out. For our task the condition is `(On akita_black_bowl_1 plate_1)`, and LIBERO's code decides it
with three tests (our reading of `envs/predicates/base_predicates.py` and
`envs/object_states/base_object_states.py`, `check_ontop`). The bowl and the plate must touch, the plate's position
must not be higher than the bowl's, and seen from above the two positions must be less than 3 cm apart. An object's
position is the one point the simulator keeps for it, which for the bowl and the plate sits at their centre seen from
above. The goal holds only at a step where all three pass. The web page draws three cases side by side: the hand holding
the bowl above the plate, much as at step 100 of our run (the two don't touch yet, so not yet); a bowl dropped on the plate's edge
(it touches, but its centre is more than 3 cm off, so not yet); and the bowl resting in the middle with the hand still
holding it (done).

When a goal has several parts, such as "the top drawer is open" and "the bowl is in it", the simulator runs every
part's test, and the goal holds only at a step where all of them pass. No test asks whether the robot has let go of the
bowl, either. In our run, the model's last actions all still said to keep the gripper closed when the goal held after
step 104.

In openpi's evaluation script the step limits are 220, 280, 300 and 520 steps for Spatial, Object, Goal and LIBERO-10.
The comments beside them give the longest training demonstration in each suite as 193, 254, 270 and 505 steps, and we
counted the same four numbers in the training dataset. So each limit sits a little above the longest time a person took
on that suite. By our reading, a limit is there so that an episode that never reaches its goal still ends. Such an
episode runs to the limit, which for Spatial is 220 steps, or 11 simulated seconds.

> Side note: step limits. On one scale, the longest demonstration and the limit per suite: Spatial 193 and 220, Object
> 254 and 280, Goal 270 and 300, LIBERO-10 505 and 520. Our run's 104 steps were an ordinary length, since this task's 45
> demonstrations in the training data took 75 to 168 steps (our count from physical-intelligence/libero's
> `meta/episodes.jsonl`, 2026-11-14).

The web page puts our whole chapter 2 run on one ruler under four of its table-camera pictures (steps 0, 35, 70 and
100). The episode starts when the script loads stored state 0, and the objects then settle for 10 steps that aren't
counted. Step 0 is the first call to the model. From there the model is called every 5 steps, 21 times in all, and each
step is 1/20 of a simulated second. The goal condition first held after step 104, 5.2 simulated seconds in, so the
episode stopped there and counted as a success. Had it never held, the episode would have run to step 220, 11 simulated
seconds, and counted as a failure. openpi's script also stops an episode if the simulator raises an error, and counts it
as a failure.

The success rate is the share of episodes in which the goal held. Each task is a tenth of its suite's episodes, so a
task the model always failed would cost the suite's rate 10 points. A rate from few episodes is also rough. Near 50%,
one task's 50 episodes pin its rate down only to within about 14 points either way, and a suite's 500 narrow that to
about 4.4 (our arithmetic, at 95% confidence).

openpi's README reports 98.8% on LIBERO-Spatial for `pi05_libero`, but it doesn't say how many episodes or runs stand
behind that number. So we don't turn the percentage into a count of episodes. The script runs 500 per suite by default.

Not every group counts the same way, either. LIBERO's own paper tested its policies with 20 episodes per task, each
allowed up to 600 steps (its Appendix D), so before comparing two scores, check how each one was counted.

> Side note: same score on a rerun? The 50 starts are stored, so they're the same. The cabinet and stove are drawn with
> openpi's random seed of 7, so by our reading they're the same too. The model starts every call from random noise
> (chapter 2), and openpi's policy server draws it from a random key that restarts with the server
> (`jax.random.key(0)`) and moves on at every call (`src/openpi/policies/policy.py`). So by our reading, a rerun draws
> the same noise only on a freshly started server. We haven't tested a rerun.

The plan we submitted for the course asks how the score changes with the words. It would run every task under four
prompts: its own instruction, a paraphrase of it, a blank prompt, and the instruction of a different task on the same
table. Run in full, that comes to 4 prompts × 4 suites × 10 tasks × 50 trials = 8,000 episodes. The plan is a proposal
we submitted, not a decision. [Chapter 6](06-where-we-stand.md) keeps the list of what the team has decided, and which
experiments we run is still open.

> Side note: how 8,000 adds up. Picture four rows, one per prompt, each of four blocks, one per suite. A block is ten
> thin strips, one per task, of 50 episodes each, so 500. Four blocks make 2,000 for one prompt, and four prompts make
> 8,000.

## Why a high score doesn't prove the words were read

Start with what `pi05_libero` learned from. Chapter 2 said openpi fine-tuned it on 1,693 demonstrations of LIBERO's
40 tasks. Those are the same 40 tasks the benchmark tests it on. Each demonstration comes with its task's sentence,
word for word the sentence the test sends, and starts from that task's table.

So the tasks, the sentences and the tables in the test are all ones the model has practised, each task in 29 to 50
demonstrations. The only new thing is the exact starting position of each object and of the arm. LIBERO's 50 stored
starting states aren't the demonstrations' own starts. LIBERO's authors drew them separately, at random in the same
way as the demonstrations' starts, so a test start differs from a training start by the same few-centimetre shifts
that the 50 test starts show between each other (Bo Liu, LIBERO's first author, on LIBERO's GitHub, issue 2,
2023-06-18).

> Side note: why 1,693 and not 2,000. The first section told why fewer than LIBERO's 2,000 recordings reached openpi's
> dataset: the OpenVLA team replayed each one and kept only the replays that still reached the goal. Out of 500
> per suite, Spatial kept 432, Object 454, Goal 428 and LIBERO-10 379, and a single task kept between 29 and 50 (our
> count of the dataset's episode list, 2026-11-14; the reason is from OpenVLA's regeneration script and from Moo Jin
> Kim of the OpenVLA team on GitHub, 2024-10-17).

The web page shows one task both ways: the first picture of the dataset's first three demonstrations of LIBERO-Spatial's
"pick up the black bowl between the plate and the ramekin and place it on the plate" (episodes 1272, 1273 and 1275),
above the first picture from stored starting states 0, 1 and 2. All six show the same objects in the same places, with
the bowl to take between the plate and the ramekin, and they differ only by a few centimetres. Our own pixel
comparison of 42 of this task's 45 demonstrations with all 50 stored states agrees that no demonstration starts from a
stored state (2026-11-14).

Before you read on, guess: in which of the four suites could you name the task from its first picture alone, without
the sentence?

A task's starting table means the objects on the table and where each one starts, as the task file's `(:init)` block
lays them out (the task file in the previous section). In LIBERO-Spatial, LIBERO-Object and LIBERO-10, almost every task has a
starting table of its own, so its first picture is enough to name the task. In LIBERO-Goal no first picture can,
because all ten tasks share one table. A model can reach a high score by learning "this starting table means this
motion" and never looking at the sentence.

The web page shows this with the first picture of all 40 tasks, one row per suite, each rendered by us from starting
state 0 the way the model receives it. In the Spatial, Object and LIBERO-10 rows the pictures differ. In the Goal row
all ten show one table, apart from the few-centimetre shifts every start has.

We compared the starting tables in LIBERO's task files and found two exceptions. In LIBERO-Spatial, "pick up the black
bowl on the stove" and "pick up the black bowl on the wooden cabinet" start from the same table. One black bowl sits
on the stove and an identical one sits on the cabinet, so the picture can't say which one to take. The goal check
names one particular bowl, though, so carrying the other one to the plate counts as a failure. In LIBERO-10, "put both
the alphabet soup and the tomato sauce in the basket" and "put both the cream cheese box and the butter in the basket"
also start from the same table. For each of these pairs, only the sentence tells the two tasks apart.

It's the first picture that matters here, because the model keeps nothing from one call to the next. Each call gets
only the two pictures of that moment and the sentence. So in a pair, the first actions come from two pictures that
look the same for both tasks, and from the sentence. Once the arm has started toward one bowl, every later picture
shows it on its way to that bowl.

> Side note: the wrist camera sees the same. The model's second picture comes from a camera on its wrist. At the first
> step of the Spatial pair, that camera looks down on the same objects in the same places in both tasks. By our pixel
> check of our 2026-11-11 run, the two tasks' first wrist pictures differ about as much as the wrist pictures of two
> starts of one task do.

Why would training let a model skip the words? Training scores it on one thing. At each moment of a demonstration the
model proposes its next actions, and its error is how far they are from what the person did next. That is the
flow-matching error of chapter 2, and nothing in it asks whether the sentence was used. As chapter 1 put it, imitation
only learns what helps it copy.

In Spatial, Object and LIBERO-10, the starting table already says which task this is, so it already says what the
person did next. On the table with a bowl on the cookie box, the person always picked up that bowl. A model that went
by the picture alone would make the same small error as one that read the sentence, so training has no reason to
prefer the reader. In Goal the table is the same for all ten tasks, as the three demonstrations at the top of this
chapter show, so only the sentence says what the person did next. A model that ignored it would keep mixing up ten
different motions, and its error would stay larger.

By our reading, then, training asked for the words only in Goal and in the two pairs. That is a reading of how the
training works, not a measurement. Whether `pi05_libero` actually goes without the words elsewhere is what chapter 4
tests.

> Side note: LIBERO's authors saw this too. In their own experiments, LIBERO's authors gave a small policy, much smaller
> than a VLA, the task in two kinds of way while it learned LIBERO-10: the task's sentence, or a label such as "Task
> 5", each turned into numbers by a language model. The numbers a language model makes from a sentence are its
> language embedding, and "Task 5" is a task ID, which says nothing about what to do. The policy learned about equally
> well with either (no statistically significant difference). The authors' explanation is that the sentence's numbers
> only worked as a label for the task (Liu et al. 2023, Section 5.2 and Table 3, and finding 3 in Section 1).

The two shared pairs are the places outside Goal where training did reward reading. The demonstrations of "pick up the
black bowl on the stove" and of "pick up the black bowl on the wooden cabinet" start from the same table, but the
person took a different bowl in each. Only the sentence could tell the model which bowl the person took, so on those
two tasks a model that skipped the words would have kept a larger error. The same goes for the two basket tasks in
LIBERO-10. Counted in the training data, the Spatial pair has 79 of the suite's 432 demonstrations and the basket pair
82 of LIBERO-10's 379. In Goal all 428 start from the one shared table, and in Object none do (our count). This is our
reading too, and it makes the Spatial pair a good place to test the model, which chapter 4 does.

LIBERO-Goal works the other way. All ten of its tasks start from one table, so a model that ignored the sentence would
get the same first pictures in all ten. It would make the same kind of motion each time, apart from the random numbers
each call starts from. That one motion can finish one of the ten goals, maybe two, and it misses the rest. Averaged
over the ten tasks, that comes to about one success in ten. This is our own arithmetic, and chapter 5 shows a
published number that matches it.

> Side note: one motion, ten goal checks. Say the model always carries the bowl to the plate. Checked against Goal's
> ten tasks, that motion finishes "put the bowl on the plate" and none of the other nine, so one task in ten succeeds.
> Every other single motion does about as badly. The motion is our example.

`pi05_libero` succeeds in 98.0% of Goal episodes, far above one in ten. At the first step Goal's ten tasks differ only
in their sentence, apart from the few-centimetre shifts, which are drawn the same way for every task and so say nothing
about which one it is. The model must be using the sentence in Goal. What this chapter can't settle is whether it also
uses the sentence where the picture already names the task, in Spatial, Object and LIBERO-10, because a high score
there would come out the same either way.

| Suite | Starting tables for 10 tasks | Success (openpi README) | What the score can show (our reading) |
|---|---|---|---|
| LIBERO-Spatial | 9 | 98.8 | It can't show whether the model reads. Eight tasks have a table of their own, and the stove and cabinet pair is two tasks of the ten inside this average. |
| LIBERO-Object | 10 | 98.2 | It can't show whether the model reads. Every task has a table of its own. |
| LIBERO-Goal | 1 | 98.0 | It shows that the model uses the sentence here. No picture could pick the right task, and a model without the words would land near one in ten. |
| LIBERO-10 | 9 | 92.4 | It can't show whether the model reads. Eight tasks have a table of their own, and the two basket tasks are two of the ten inside this average. |

A newcomer often reads "98% on LIBERO-Spatial" as "the model understands spatial words like *between*". The first
pictures show why that doesn't follow. In eight of the ten Spatial tasks the starting table belongs to that task alone,
and in training the person always took the same bowl from it. So the picture points to the right bowl as clearly as
"between the plate and the ramekin" does, and a model could reach 98.8% with the words or without them. The stove and
cabinet pair is the one place in the suite where the words have to do the work. The opposite conclusion goes too far
as well. The score doesn't show that the model ignores *between* either, because a score this high would come out the
same both ways. Chapter 4 tests it.

Another group, LIBERO-PRO (Zhou et al. 2025, Section 2.3 and Figure 4), moved the object the robot has to pick up away
from where LIBERO starts it. For OpenVLA and π0, success collapsed once the shift passed 0.2, and π0.5 kept some
success up to about 0.4, in units the paper doesn't name. The authors write that even small shifts sent the arm toward
the object's usual spot instead of where it now stood, and they read that as memorised positions. Chapter 5 covers the
rest of that paper.

## What this means for our project

Goal's 98.0% already shows that `pi05_libero` uses the sentence when the picture can't name the task. Whether it also
uses the sentence when the picture can, in Spatial, Object and LIBERO-10, is still open, and those suites' scores
can't answer it. Inside those suites, the two shared pairs are the tasks that can answer it, because there the picture
can't decide. The plan we submitted with the course sign-up compares the four suites under different prompts, and this
chapter says what such a comparison can and can't show. That plan is a proposal, not a decision, and chapter 6 lists
what the team has decided. Chapter 4 turns the open question into tests.

## Check yourself

1. In which suite must a model read the instruction to succeed, and why?
2. How many episodes does one full evaluation of one suite under one prompt take?
3. A model scores 98% on LIBERO-Spatial. Explain why that doesn't show it understands "between the plate and the
   ramekin".
4. Every training demonstration comes with its sentence. Why can training still leave a model that never reads the
   sentence in LIBERO-Spatial?
5. Why does openpi's script send a do-nothing action for 10 steps before it takes the first picture, and why don't
   those steps count toward the 220-step limit?

<details><summary>Answers</summary>

1. LIBERO-Goal. All ten tasks start from the same scene, so only the sentence tells them apart.
2. 500 (10 tasks × 50 trials).
3. The "between the plate and the ramekin" task starts from its own arrangement of objects, so the picture alone
   identifies the task. The model can map arrangements to motions without using the words.
4. Training scores only the model's actions against what the person did next. In eight of the ten Spatial tasks the
   starting table already says which bowl the person took, so going by the picture alone gives the same small error as
   reading the sentence, and nothing pushes the model to read. Only in the stove and cabinet pair does the error
   depend on the sentence.
5. LIBERO stores every loose object at the same height, 0.97 m, and the script's comment says the simulator drops the
   objects, so the script waits for them to fall before the model sees anything. The model doesn't act during those
   steps, so they aren't part of its episode. In the code the loop runs for the step limit plus the 10 waiting steps
   (`while t

</details>

In questions 6 to 14, pick one answer before you open the answers. Each wrong option is a belief newcomers often
hold, and the answers say why each option is right or wrong. (On the web page, each option opens on its own.)

6. Which suite starts all ten of its tasks from the same table?
   - A. LIBERO-Spatial, since its ten tasks use the same objects.
   - B. LIBERO-Object, since every task puts something in the same basket.
   - C. LIBERO-Goal.

<details><summary>Answers to 6 to 14, with why each option is right or wrong</summary>

6. C is right.
   - A: No. The objects are the same, but the two black bowls start in different places in each task, so the tables
     differ (figure 3.11, top row).
   - B: No. The basket stays, but each task has its own set of groceries on the floor, in its own places.
   - C: Right. All ten tasks start from one arrangement of the bowl, plate, stove, wine bottle, cream cheese and
     cabinet, so only the sentence says which task it is.

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
- Liu et al. (2023), LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning,
  [arXiv 2306.03310](https://arxiv.org/abs/2306.03310), CC BY 4.0. Read again 2026-11-14: Figure 1's caption on what
  each suite tests (spatial relationships, objects, task goals); Section 4.2, LIBERO-100 split into 90 short-horizon
  and 10 long-horizon tasks; Section 4.3, demonstrations by teleoperation with a 3Dconnexion SpaceMouse. Figures 8 to
  11 reused under CC BY 4.0 in the "go deeper" rail.
- LIBERO's code at the commit openpi pins: `scripts/collect_demonstration.py` (a recording stops once the goal has held
  for 10 steps; SpaceMouse by default), `scripts/create_dataset.py`, `libero/libero/envs/bddl_base_domain.py` (a new
  arrangement is sampled from the task file's regions on reset), and the task files in `libero/libero/bddl_files/`,
  read 2026-11-14. [github.com/Lifelong-Robot-Learning/LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO)
- Our comparison of LIBERO's task files, 2026-11-14: 130 files in five folders; in LIBERO-Spatial only the two black
  bowls change place; nine of LIBERO-10's ten goals ask for two things; LIBERO-90's 90 tasks share 20 starting
  arrangements, 2 to 7 per scene.
- robosuite 1.4.1 (the version in openpi's LIBERO environment), read 2026-11-14: `macros.py` (`IMAGE_CONVENTION =
  "opengl"`), `environments/robot_env.py` (camera pictures), `environments/base.py` (one action per step),
  `models/robots/manipulators/panda_robot.py` (the Panda, "designed by Franka"), `devices/spacemouse.py` (the 3D
  mouse's controls). [github.com/ARISE-Initiative/robosuite](https://github.com/ARISE-Initiative/robosuite)
- OpenVLA (Kim et al. 2024): `experiments/robot/libero/regenerate_libero_dataset.py` (pictures re-recorded at 256 × 256,
  still steps removed, failed replays dropped, and the note that the RLDS conversion turns pictures 180 degrees) and
  `libero_utils.py`, and the README's LIBERO section, read 2026-11-14.
  [github.com/openvla/openvla](https://github.com/openvla/openvla)
- Moo Jin Kim, `rlds_dataset_builder` (MIT), the LIBERO builders that turn both pictures with `[::-1,::-1]`, linked from
  OpenVLA's README, read 2026-11-14. [github.com/moojink/rlds_dataset_builder](https://github.com/moojink/rlds_dataset_builder)
- physical-intelligence/libero, CC BY 4.0: `meta/episodes.jsonl` and `meta/info.json` (1,693 episodes, 10 fps, longest
  episodes 193, 254, 270 and 505 steps, 29 to 50 episodes per task, our count), and frames of episodes 379, 851 and 1,
  read through the Hugging Face datasets-server on 2026-11-14.
  [huggingface.co/datasets/physical-intelligence/libero](https://huggingface.co/datasets/physical-intelligence/libero)
- Photos from Wikimedia Commons: "Franka Emika2" by Ims (CeBIT 2017), CC BY-SA 4.0,
  [commons.wikimedia.org/wiki/File:Franka_Emika2.jpg](https://commons.wikimedia.org/wiki/File:Franka_Emika2.jpg);
  "3Dconnexion with hand at Institute of Geography of Masaryk University in Brno" by Jiří Sedláček, CC BY-SA 3.0,
  [commons.wikimedia.org/wiki/File:3Dconnexion_with_hand_at_Institute_of_Geography_of_Masaryk_University_in_Brno,_Brno-City_District.jpg](https://commons.wikimedia.org/wiki/File:3Dconnexion_with_hand_at_Institute_of_Geography_of_Masaryk_University_in_Brno,_Brno-City_District.jpg).
  Licences checked through the Commons API, 2026-11-14. Both cropped.
- Liu et al. (2023), LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning,
  https://arxiv.org/abs/2306.03310 (HTML v2), CC BY 4.0. Read 2026-11-14: Figure 2 (cropped for the side note "PDDL or
  BDDL?"), Appendix C.2 (the task file called a "PDDL-based Scene Description File"), Appendix D (their own policies
  evaluated over 20 test episodes per task, of at most 600 steps).
- LIBERO's code at the commit openpi pins (f78abd6, 2023-12-24), https://github.com/Lifelong-Robot-Learning/LIBERO, MIT
  licence. Read 2026-11-14: the task file `libero/libero/bddl_files/libero_spatial/pick_up_the_black_bowl_between_the_plate_and_the_ramekin_and_place_it_on_the_plate.bddl`
  and the other nine Spatial files (same regions, same goal); `benchmark/__init__.py` (the sentence comes from the file
  name; stored states loaded from `.pruned_init`); `envs/utils.py` (`rectangle2xyrange`, how a region's four numbers
  are read); `envs/bddl_base_domain.py` (`control_freq=20`, line 63; placement of fixtures and objects; `_reset_internal`,
  which places the cabinet and the stove again at every reset; `step`, which checks the goal after every step);
  `envs/problems/libero_tabletop_manipulation.py` (`_check_success` ANDs the goal's parts; the table's size and height);
  `envs/predicates/base_predicates.py` (`On`) and `envs/object_states/base_object_states.py` (`check_ontop`, the three
  tests); the bowl's and plate's model files; the cabinet's and stove's joints; `envs/env_wrapper.py`
  (`set_init_state`); the README's note that the starting states are fixed for benchmarking.
- LIBERO's stored starting states for Spatial task 0 (`init_files/libero_spatial/…pruned_init`), loaded with numpy and
  torch on 2026-11-14 by `tools/ch3/stored_state_numbers.py` (no simulator): 50 rows of 92 numbers, the objects' spread,
  the arm's spread.
- BDDL, the Behavior Domain Definition Language (Stanford Vision and Learning Lab, BEHAVIOR benchmark),
  https://github.com/StanfordVL/bddl; README of the installed package (bddl 1.0.1) read 2026-11-14.
- robosuite 1.4.1 (the version in openpi's LIBERO environment), https://github.com/ARISE-Initiative/robosuite.
  Read 2026-11-14: `robosuite/environments/base.py` (what `control_freq` means, how many physics updates a step runs)
  and `robosuite/macros.py` (`SIMULATION_TIMESTEP = 0.002`).
- openpi, https://github.com/Physical-Intelligence/openpi (local checkout 215abfb). Read 2026-11-14:
  `examples/libero/main.py` (step limits and the longest-demonstration comments, lines 60-67; seed 7 and the comment
  that the seed "seems to affect object positions even when using fixed initial state", lines 45, 50 and 195; the 10
  waiting steps outside the limit, line 104; an error ends an episode, lines 160-162);
  `src/openpi/policies/policy.py` (the random key starts at `jax.random.key(0)` and is split at every call, lines 65 and
  75); `examples/libero/README.md` (the 98.8 / 98.2 / 98.0 / 92.4 table, with no episode count).
- physical-intelligence/libero on Hugging Face, `meta/episodes.jsonl`, `meta/tasks.jsonl` and `meta/info.json`,
  https://huggingface.co/datasets/physical-intelligence/libero (CC BY 4.0), fetched 2026-11-14: our count of each suite's
  longest demonstration (193, 254, 270, 505) and of Spatial task 0's 45 demonstrations (75 to 168 steps).
- Our recorded run, `stage1/runs/recorded-call-spatial0/calls.json` (2026-11-11): 104 steps, 21 calls, the gripper
  commands at the end; our 60 episodes in `stage1/results/exp1-shared-table.md` (2026-11-11): 11.7 s per successful
  episode in our runs.
- The plan we submitted, quoted in chapter 6,
  https://github.com/blueif16/vla_final/blob/main/docs/learn/06-where-we-stand.md (the four prompts).
- physical-intelligence/libero (CC BY 4.0), `meta/episodes.jsonl`, `tasks.jsonl` and `info.json`, read 2026-11-14:
  1,693 demonstrations (Spatial 432, Object 454, Goal 428, LIBERO-10 379; 29 to 50 per task, our count); the 40 task
  sentences match the benchmark's word for word (our comparison).
  https://huggingface.co/datasets/physical-intelligence/libero
- OpenVLA, `experiments/robot/libero/regenerate_libero_dataset.py` and README, read 2026-11-14 (no-op commands removed,
  failed replays dropped); Moo Jin Kim, openvla issue 138, 2024-10-17. https://github.com/openvla/openvla
- Bo Liu, LIBERO issue 2, 2023-06-18, and Yifeng Zhu, LIBERO issue 40, 2024-10-20, on the stored starting states being
  drawn separately from the demonstrations' starts. https://github.com/Lifelong-Robot-Learning/LIBERO/issues/2
- Liu et al. (2023), LIBERO, Section 5.2 and Table 3 (language embeddings against a task-ID embedding on LIBERO-Long),
  read 2026-11-14. https://arxiv.org/abs/2306.03310
- openpi commit 215abfb: `src/openpi/policies/libero_policy.py`, `src/openpi/policies/policy.py`,
  `examples/libero/main.py` and `examples/libero/README.md`, read 2026-11-14.
- Zhou et al. (2025), LIBERO-PRO, Sections 2.3 and 5.1 and Figure 4 (CC BY 4.0), read 2026-11-14.
  https://arxiv.org/abs/2510.03827
- Our pixel checks of 2026-11-14 (demonstration starts against stored starts for Spatial task 0; the pair's first wrist
  pictures from our 2026-11-11 run).
