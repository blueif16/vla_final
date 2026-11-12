# 4. What "understanding the instruction" means, and how to test it

After this chapter you can define language grounding by what the robot does, describe the four prompt conditions in
our submitted plan, and say what each result would tell us.
Needs: chapters 1 to 3. Reading time: 8 min.

Take a LIBERO-Spatial scene and run the model twice from the same starting arrangement. The first time it gets the
real sentence, "pick up the black bowl between the plate and the ramekin and place it on the plate". The second time
it gets an empty string. If the arm makes the same reach, grabs the same bowl and puts it on the same plate both
times, the sentence wasn't what drove the motion.

## A definition we can measure

We can't look inside the model and see "understanding". So we define it by behaviour. An instruction is grounded when
changing the words changes what the robot does, in the way the new words say. When the words change and the behaviour
doesn't, the model is running on the picture.

## The four conditions in our submitted plan

| Condition | What we send | If success stays high | If success drops |
|---|---|---|---|
| Original | the task's own sentence | baseline (should match the published ~98%) | our setup has a problem; fix it before anything else |
| Paraphrase | the same request in different words | the model copes with wording it never trained on | it matches the exact training strings |
| Blank | an empty instruction | the picture alone was enough to choose the task | the model needed the words |
| Different task, same scene | a feasible instruction for another task in this scene | **warning sign**: it did the scene's usual task and ignored the new words | it may be listening (see below) |

The last row needs care. When we ask for a different task, a drop in the original task's success rate doesn't yet
mean the model followed the new words. It might have frozen or flailed. So for this condition we need to record which
task, if any, the robot actually completed. The LIBERO-CF paper (chapter 5) uses three measures for this, and we can
reuse them. The grounding rate is how often the gripper touches the object the new instruction names. Faithful success
counts episodes where the robot completed the new task, and biased success counts those where it did the scene's
original task instead.

The paraphrase row needs care too. In LIBERO-Spatial the sentence picks a bowl by its position, so a paraphrase must
still point at the same bowl ("the bowl sitting between the ramekin and the plate"), or we've changed the task by
accident.

## Why a model might ignore the words

Chapter 1 gave the reason. Imitation learning rewards whatever predicts the demonstrated action. In three of the four
LIBERO suites, the starting picture already predicts it for almost every task, so the words add almost nothing during
training. (Chapter 3 lists the two pairs of tasks that share a starting table.) In LIBERO-Goal they
are the only thing that tells the tasks apart, so there the model has to use them.

This gives a prediction we can check, and it is our reading, not yet a result. A blank or wrong instruction should
hurt little on Spatial, Object and LIBERO-10, and hurt a lot on Goal. If the model reads words only where the data
forced it to, then "does π0.5 understand language?" has no single answer. It depends on what the fine-tuning data
asked of it.

## What this means for our project

The question we submitted, "how does a VLA actually understand the instruction?", becomes a set of numbers: success
under four conditions on four suites, plus which task was done under the wrong instruction. Chapter 5 shows that other
groups have already measured several of these numbers for the same checkpoint, which changes what is worth our time.

## Check yourself

1. Define "grounded" in terms of what the robot does.
2. Under a different-task instruction, the original task's success falls from 98% to 40%. What else do you need to
   measure before saying the model followed the new words?
3. Why does our reading predict that a blank instruction hurts most on LIBERO-Goal?

<details><summary>Answers</summary>

1. Changing the words changes what the robot does, in the way the new words say.
2. Which task the robot did in the other 60%. Did it complete the new task, touch the new object, or do nothing
   useful? Grounding rate and faithful versus biased success answer this.
3. Goal is the only suite where all tasks share one starting picture. Without words the model can't tell them apart,
   so it can only guess.

</details>

## Sources

- Fang et al. (2026), When Vision Overrides Language (LIBERO-CF), https://arxiv.org/abs/2602.17659 (grounding rate,
  faithful and biased success)
- Our submitted plan, CS 6180 team sign-up sheet, November 2026 (quoted in chapter 6)
