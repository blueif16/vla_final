# 4. What "understanding the instruction" means, and how to test it

After this chapter you can define language grounding by what the robot does, describe the four prompt conditions in
our submitted plan, and say what each result would tell us. You can also explain why a test with a different task's
sentence needs more than a success rate, and why a model might ignore the words.
Needs: chapters 1 to 3. Reading time: 10 min. Web version: https://blueif16.github.io/vla_final/learn/04-the-grounding-question.html

Two tasks in LIBERO-Spatial start from the same table. One black bowl sits on the stove and an identical one sits on
top of the wooden cabinet. Task 7 says "pick up the black bowl on the stove and place it on the plate", and task 9 says
the same thing with "on the wooden cabinet" in place of "on the stove". Chapter 3 found this pair in LIBERO's task
files. The two files differ only in the sentence and in which of the two bowls starts where, so the picture can't say
which bowl to take. Only the sentence can.

On 2026-11-11 we ran `pi05_libero`, the checkpoint from chapter 2, on both tasks. Each task ran from ten of its
stored starting arrangements, once with its own sentence and once with an empty string where the sentence goes.
Everything else was the same, down to where each object stood. If the arm makes the same reach both times, grabs the
same bowl and puts it on the same plate, the sentence wasn't what drove the motion.

It didn't make the same reach. In starting arrangement 2 of task 9, the robot given its sentence reached up to the bowl
on the cabinet and carried it to the plate. Given an empty string, it took the bowl on the stove instead, and the
simulator scored the run a failure. (We show that run on the web page because it shows the change plainly; most blank
runs didn't end like it, as the table below shows.) Across all the runs, the robot did the right task 19 times in 20
with its sentence and 8 times in 40 with an empty string. The empty string ran from 20 starting arrangements per task:
the ten used with the sentence, and ten more in which the simulator also checked the cookie box. The motion changed
when the words went away, so on this pair the words are doing real work.

## A definition we can measure

We can't look inside the model and see "understanding". So we define it by behaviour. An instruction is grounded when
changing the words changes what the robot does, in the way the new words say. When the words change and the behaviour
doesn't, the model is running on the picture.

Our run passes the first half of that test and can't reach the second. Taking the words away changed what the robot
did. But an empty string doesn't ask for anything, so there was no "way the new words say" for the robot to follow.
In the 20 blank runs where the simulator also checked the cookie box, the runs ended like this:

| What reached the plate | Task 7 (stove bowl wanted) | Task 9 (cabinet bowl wanted) |
|---|---|---|
| the stove bowl | 3 (scored a success) | 5 (scored a failure) |
| the cabinet bowl | 0 | 1 (scored a success) |
| the cookie box | 2 | 1 |
| none of the checked objects | 5 | 3 |

The robot took the stove bowl in both tasks, and that same move counts as a success for task 7 and a failure for task 9.
"None of the checked objects" means neither bowl nor the cookie box reached the plate. The simulator didn't check the
small ramekin, though, and in two of those runs (task 7, starting arrangements 10 and 13) the arm put the ramekin on
the plate. We saw that in the videos; the simulator didn't check it.

In most blank runs no bowl reached the plate at all. Across all 40, a bowl got there 15 times, and 12 of those 15 times
it was the bowl on the stove. We don't know yet why the robot prefers that one; one guess of ours is that the stove
sits closer to where the arm starts. Every LIBERO-Spatial task ends with "place it on the plate", and even without a
sentence the robot kept moving things towards the plate, just not always the right thing.

There's a catch in reading these numbers. The model never saw an empty instruction in training, because every
training example came with its task's sentence (`prompt_from_task=True` in the `pi05_libero` config). So part of what
the table shows may be the model reacting to an input it has never seen, on top of the missing information. A sentence
for a different task, the last of the four conditions below, would separate the two.

## The four conditions in our submitted plan

| Condition | What we send | If success stays high | If success drops |
|---|---|---|---|
| Original | the task's own sentence | baseline (should match the published ~98%) | our setup has a problem; fix it before anything else |
| Paraphrase | the same request in different words | the model copes with wording it never trained on | it matches the exact training strings |
| Blank | an empty instruction | the picture alone was enough to choose the task | the model needed the words |
| Different task, same scene | a feasible instruction for another task in this scene | **warning sign**: it did the scene's usual task and ignored the new words | it may be listening (see below) |

On LIBERO-Spatial's first task, the one whose recorded run chapter 2 steps through, the four sentences would be:
- original: "pick up the black bowl between the plate and the ramekin and place it on the plate" (openpi's published
  score on LIBERO-Spatial is 98.8);
- paraphrase: "pick up the black bowl sitting between the ramekin and the plate and put it on the plate";
- blank: "";
- different task: "pick up the cookie box and place it on the plate", which the LIBERO-CF paper wrote for this same
  table (its CF-Spatial task 1).

The picture is the same in all four, and only the sentence changes. "Success" means LIBERO's own check for this table's
task: the bowl between the plate and the ramekin ends on the plate.

## A different task needs more than a success rate

The last row needs care. A newcomer often believes that when a different instruction makes the original task's success
rate drop, the model must have followed the new words. A drop says only that the robot stopped doing the original task.
It doesn't say what the robot did instead. It might have done the new task, or it might have frozen or flailed. Our
blank run already shows a drop with nothing to follow: success fell from 19 in 20 to 8 in 40, there were no new words
at all, and in most of those runs no bowl reached the plate. So for this condition we need to record which task, if
any, the robot actually completed.

The LIBERO-CF paper (chapter 5) wrote 50 instructions of this kind for LIBERO's tables and calls each one a
counterfactual instruction, a task the table allows but the model wasn't trained to do there. It uses three measures
for this, and we can reuse them. The grounding rate is how often the gripper touches the object the new instruction
names, whether or not the task gets finished. Faithful success counts episodes where the robot completed the new task,
and biased success counts those where it did the scene's original task instead. The paper also counts how often the
gripper touched the original task's object.

Here is how the four ways one episode can end would count, for "pick up the cookie box and place it on the plate" on
task 0's table:

| How the episode ends | Grounding | Faithful success | Biased success | LIBERO's own score for task 0 |
|---|---|---|---|---|
| the cookie box ends on the plate | yes | yes | no | failure |
| the gripper touches the cookie box, but nothing reaches the plate | yes | no | no | failure |
| the bowl between the plate and the ramekin ends on the plate (the table's usual task) | no | no | yes | success |
| the gripper never touches the cookie box, and nothing reaches the plate | no | no | no | failure |

Only the third ending counts as biased success, and it's also the only one LIBERO's own check scores as a success. So
when that score drops, the cause could be the first, the second or the fourth ending, and only the first is the robot
doing what it was told. We haven't run this condition yet.

## A paraphrase must point at the same bowl

The paraphrase row needs care too. In LIBERO-Spatial the sentence picks a bowl by its position, so a paraphrase must
still point at the same bowl ("the bowl sitting between the ramekin and the plate"), or we've changed the task by
accident.

It's easy to do. Shorten task 0's "between the plate and the ramekin" to "next to the ramekin", and the sentence names
the other bowl, because task 0's file starts the second bowl next to the ramekin. "Pick up the black bowl next to the
ramekin and place it on the plate" is also, word for word, the sentence of LIBERO-Spatial task 1, so the model has seen
it in training, on task 1's table. A paraphrase that names the other bowl isn't testing wording any more. It has turned
into the different-task condition, run without anyone meaning to.

## Why a model might ignore the words

Chapter 1 gave the reason. Imitation learning rewards whatever predicts the demonstrated action. In three of the four
LIBERO suites, the starting picture already predicts it for almost every task, so the words add almost nothing during
training. (Chapter 3 lists the two pairs of tasks that share a starting table.) In LIBERO-Goal they
are the only thing that tells the tasks apart, so there the model has to use them.

| Suite | Tasks | Starting tables |
|---|---|---|
| LIBERO-Goal | 10 | 1 |
| LIBERO-Spatial | 10 | 9 (tasks 7 and 9 share one) |
| LIBERO-Object | 10 | 10 |
| LIBERO-10 | 10 | 9 (the two "put both ... in the basket" tasks in LIVING_ROOM_SCENE2 share one) |

Our pair from the opening is one of those two exceptions, and it behaved the way this reasoning predicts. The picture
can't choose between its two tasks, so the model needed the sentence, and without it the robot mostly failed. That
says nothing yet about LIBERO-Spatial as a whole, where eight of the ten tasks start from a table of their own.

This gives a prediction we can check, and it is our reading, not yet a result. A blank or wrong instruction should
hurt little on Spatial, Object and LIBERO-10, and hurt a lot on Goal. If the model reads words only where the data
forced it to, then "does π0.5 understand language?" has no single answer. It depends on what the fine-tuning data
asked of it. Chapter 5 has the published blank-instruction numbers for our checkpoint, suite by suite.

## What this means for our project

The question we submitted, "how does a VLA actually understand the instruction?", becomes a set of numbers: success
under four conditions on four suites, plus which task was done under the wrong instruction. Our first run covered one
condition on one pair of tasks. Its other half, giving each task the other task's sentence, would show whether the
model follows the words or only reacts to losing them. Chapter 5 shows that other groups have already measured
several of these numbers for the same checkpoint, which changes what is worth our time.

## Check yourself

1. Define "grounded" in terms of what the robot does.
2. Under a different-task instruction, the original task's success falls from 98% to 40%. What else do you need to
   measure before saying the model followed the new words?
3. Why does our reading predict that a blank instruction hurts most on LIBERO-Goal?
4. In our run, the empty string sent the arm to the other bowl. Why is this pair a good place to see the words matter,
   and why doesn't it tell us how LIBERO-Spatial behaves as a whole? Say it in your own words.

<details><summary>Answers</summary>

1. Changing the words changes what the robot does, in the way the new words say.
2. Which task the robot did in the other 60%. Did it complete the new task, touch the new object, or do nothing
   useful? Grounding rate and faithful versus biased success answer this.
3. Goal is the only suite where all tasks share one starting picture. Without words the model can't tell them apart,
   so it can only guess.
4. Its two tasks start from the same table, so only the sentence can say which bowl to take, and the model can't
   succeed without reading it. In eight of Spatial's ten tasks the table alone identifies the task, so a blank
   instruction might change little there.

</details>

Pick one answer for each; the right one and why the others are wrong are folded below each question.

5. We send task 0's table the sentence "pick up the cookie box and place it on the plate", and task 0's success rate
   falls from 98% to 40%. What can we say about the other 60% of episodes?
   A. The robot followed the new words in them, since it stopped doing the old task.
   B. Nothing yet. We need to see what the robot did in them, for example with the grounding rate and faithful success.
   C. The model ignores language, because it still did the old task 40% of the time.

<details><summary>Answer to 5</summary>

B. The grounding rate says whether it touched the cookie box, and faithful success whether it put the box on the
plate. LIBERO's own check for task 0 can't tell either apart from a robot that froze. A is the wrong belief this
chapter names: stopping the old task is all a drop shows. C goes too far: the 40% counts against the model as biased
success, but behaviour changed in the other 60%, and whether that change followed the words is the open part.

</details>

6. Which of these would work as a paraphrase of task 0's sentence, "pick up the black bowl between the plate and the
   ramekin and place it on the plate"?
   A. "pick up the black bowl next to the ramekin and place it on the plate"
   B. "pick up a black bowl and place it on the plate"
   C. "put the black bowl that sits between the ramekin and the plate onto the plate"

<details><summary>Answer to 6</summary>

C. The words are different, and it still names the same bowl, so success still means the same thing. A names the
other bowl, which starts next to the ramekin on task 0's table, and it's the exact sentence of LIBERO-Spatial task 1.
B doesn't say which of the two bowls, so either would count as doing what it asks.

</details>

7. On our shared-table pair, an empty string cut success from 19 in 20 to 8 in 40. Why doesn't that yet show the
   model follows the words in the way they say?
   A. An empty string asks for nothing, so there was nothing for the robot to follow. Part of the drop may also be the
      model reacting to an input it never saw in training.
   B. Because 8 in 40 is too close to 19 in 20 to tell apart.
   C. Because LIBERO-Spatial is a suite where the picture decides the task.

<details><summary>Answer to 7</summary>

A. The drop shows the words matter on this pair. Whether the robot does what new words say needs a sentence that asks
for something else, such as the other task's sentence. B is wrong: our results give 76–99% and 10–35% as the likely
ranges for the two rates, far apart. C is wrong for this pair: both tasks start from the same table, so the picture
can't decide.

</details>

8. By our reading, on which suite should a blank instruction hurt the most?
   A. LIBERO-Spatial, because its sentences describe where things are.
   B. LIBERO-Goal, because all ten of its tasks start from the same table.
   C. LIBERO-10, because its tasks are the longest.

<details><summary>Answer to 8</summary>

B. With one picture for ten tasks, only the words tell the model what to do; chapter 5 shows the published number for
our checkpoint. A is wrong because in eight of Spatial's ten tasks the starting table already tells the tasks apart.
C is wrong because length makes tasks harder, but a blank instruction hurts where the picture can't tell the tasks
apart, and eight of LIBERO-10's ten tasks start from a table of their own.

</details>

## Sources

- Our experiment 1, run on 2026-11-11 with openpi's `pi05_libero` checkpoint and evaluation settings:
  `stage1/results/exp1-shared-table.md` (results, the endings table, the 95% ranges, our readings) and
  `stage1/runs/exp1-shared-table/episodes.jsonl` (one record per run). The web page's clip and frames were made from
  the local videos by `tools/ch4/make_assets.py`, which records the rule for each pick. The ramekin in the first
  "none" run was seen by us in its video on 2026-11-13; the simulator didn't check it.
- Our recorded run of LIBERO-Spatial task 0 from its first starting arrangement, 2026-11-11
  (`stage1/runs/recorded-call-spatial0/`).
- Fang et al. (2026), When Vision Overrides Language (LIBERO-CF), https://arxiv.org/abs/2602.17659 (CC BY 4.0, v3 read
  2026-11-13: grounding rate, faithful and biased success, 50 counterfactual tasks in suites of 15, 10, 10 and 15).
  Code, MIT licence: https://github.com/yuffish/VLA-CF; its `libero_cf_spatial/01-pick_up_the_cookie_box_and_place_it_on_the_plate.bddl`
  starts from task 0's arrangement (checked 2026-11-13).
- LIBERO's task files for LIBERO-Spatial (`libero/libero/bddl_files/libero_spatial/`, at the version openpi pins):
  the task 7 and 9 files differ only in the sentence and in which bowl starts where; task 0's file starts bowl 1
  between the plate and the ramekin and bowl 2 next to the ramekin. Starting tables per suite: chapter 3 and
  `library/papers.yaml` (libero-bddl). Checked 2026-11-11 and 2026-11-13.
- openpi: the `pi05_libero` config (`prompt_from_task=True`) and the published 98.8 on LIBERO-Spatial
  (`examples/libero/README.md`), checked 2026-11-11, https://github.com/Physical-Intelligence/openpi
- Our submitted plan, CS 6180 team sign-up sheet, November 2026 (quoted in chapter 6)
