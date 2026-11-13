# RL 7. Robots that practise

After this chapter you can explain why a robot trained only by copying can't recover from its own mistakes, walk
through how π*0.6 improves from its own tries, and say what RL on LIBERO needs and what it has shown so far.
Needs: RL 1 to RL 4, and VLA chapters 1 and 2. Reading time: 9 min.

In November 2025 Physical Intelligence published π*0.6, a version of their robot model trained with RL on its own
experience. They ran it making espresso drinks for 13 hours straight, folding laundry it had never seen in a home it
had never been in for over two hours without interruption, and assembling cardboard boxes that a factory then used
for real packaging. On some of the hardest tasks, their RL method more than doubled the throughput, the number of
tasks the robot finished successfully per hour, and roughly halved how often it failed.

Before this practice, the robot had been trained on demonstrations for each task, like π0.5. The doubling came from
practising on top of them.

## Why copying isn't enough

A policy trained only on demonstrations (behaviour cloning, VLA chapter 1) has two limits. The π*0.6 paper puts them
in one sentence: such policies "are known to suffer from compounding errors and, at best, can only be as performant as
the demonstration data".

Compounding errors work like this. The demonstrations show an expert doing the task well. The robot copies them
closely but not perfectly, so now and then its gripper ends up a little off from anywhere the expert's ever was. The
demonstrations never showed that situation, so the policy is less sure what to do, and its next action is a little
worse, which takes it further from anything it has seen. Small slips grow into failures. No number of perfect
demonstrations fixes this, because the expert never makes the robot's mistakes, so the data never shows how to
recover from them.

Practice does show it. The robot's own tries are full of its own mistakes, and some of those tries recover anyway.

## Recap, step by step

Physical Intelligence's method is called Recap, short for RL with Experience and Corrections via Advantage-conditioned
Policies.

1. **Pre-train with RL already in it.** π*0.6 is pre-trained on data from many robots and tasks, much as π0.5 was,
   but with the advantage label of step 5 built in from the start.
2. **Fine-tune on demonstrations** for the task at hand.
3. **Deploy and collect.** The robot attempts the task on its own, and every try is labelled a success or a failure.
   When it makes a big mistake, an expert can take over by remote control and correct it. This is the "coaching".
4. **Train a value function.** This is RL 3's coach. It looks at a moment of a try and predicts how many steps are
   left until success, or that the try is heading for failure. Because it judges every moment, it answers RL 2's
   credit assignment question: an action that made success look closer than expected gets the credit.
5. **Label and retrain.** Every action in the data gets a label, "Advantage: positive" if it did clearly better than
   the value function expected and "Advantage: negative" otherwise. The label is added to the model's input as text,
   and the expert's corrections are always labelled positive. The model is trained to produce each action given its
   label.
6. **Ask for the good version.** When the robot runs, its input always says "Advantage: positive", so it acts like the
   better-than-usual moments in its own experience and its coaches' corrections.
7. **Repeat** steps 3 to 6 with the improved robot.

Step 5 is easiest to see with made-up numbers. Count the value as minus the number of steps left. At some moment the value
function says 40 steps to go, so the value is −40. One step later it says 35 steps to go, −35. Each step costs 1, so
the action's advantage is −1 + (−35) − (−40) = +4: the robot got five steps closer to success while one step passed.
If instead it still said 40 steps to go after the move, the advantage would be −1 + (−40) − (−40) = −1. The first action
gets "Advantage: positive", the second "negative" (Recap also sets a threshold for each task, so only actions that are
clearly better count as positive).

Recap learns from data that has already been collected, which is called offline RL, instead of RL 1's loop of sampling
and pushing. The paper reports that its labelling approach worked much better than a policy-gradient approach they
compared it with.

## RL on LIBERO

Several groups have run RL on the benchmark our project uses. All of them used LIBERO's own goal check as the reward:
1 for success, 0 otherwise.

- **πRL** (October 2025, built on the RLinf framework) took π0 and π0.5, fine-tuned each on only a few demonstrations,
  and then trained them with online RL. For π0.5 that was 40 demonstrations across all four suites, one per task. On
  LIBERO, π0.5 went from 77.1% to 98.3% and π0 from 57.6% to 97.6%. These were the authors' own few-shot fine-tunes,
  not the released `pi05_libero`.
- **SimpleVLA-RL** (September 2025) used GRPO (RL 4) on OpenVLA-OFT, another VLA. Starting from one demonstration per
  task, the LIBERO average went from 48.9% to 96.9%.

Both start from a copied policy that already succeeds sometimes, which is RL 2's answer to exploration. We haven't yet
checked whether any of them tested the instruction the way VLA chapter 4 does.

## Doing RL yourself

There are two levels.

**Level 1 changes the harness around a model, not its weights.** You run the agent, score the result, let it rewrite
its own prompts, notes or tools, and keep only the changes that raise the score. It's RL 1's loop with the harness in
place of the policy. It works with models you can only reach through an API, and for one person it usually pays off
best.

**Level 2 changes the weights.** The common tools are Hugging Face's TRL, ByteDance's verl, OpenPipe's ART, Prime
Intellect's verifiers library, and hosted services such as Tinker (chapter 6). For robots, RLinf is the framework
behind πRL. Good first projects all come with a grader that costs nothing:

- text-to-SQL, scored by running the query and comparing the result;
- search agents, scored against questions with known answers;
- game agents for Wordle or Sokoban, scored by winning;
- robot control in MuJoCo, where the physics engine checks whether the task was done.

A robot set up in MuJoCo faces exactly this choice: improve the harness around a fixed VLA, or fine-tune the VLA's
weights with RL.

## The wrong belief: more demonstrations would be enough

It's tempting to think a robot that fails just needs more demonstrations. Compounding errors say otherwise. Each new
demonstration shows the expert doing it right again, and never the robot's own slips. π*0.6 already had its
demonstrations, and practice doubled its throughput on some of the hardest tasks.

## What this means for our project

Three links, and all are our reading. First, π*0.6's RL step works through words. The robot is told "Advantage:
positive" as text and it behaves differently. That works because training showed the same kinds of situations with
both labels, which is the condition VLA chapter 1 says a policy needs before words change what it does. Second, our
stage 2 is laundry folding, the task where Physical Intelligence used RL to make their robot reliable. Third, πRL shows
that RL on π0.5 in LIBERO runs and has been published. Whether any RL belongs in our project is open (VLA chapter 6).

## Looking back over the series

RL is trial and error with a grade (RL 1). Its three problems are exploring, giving credit and cheating (RL 2), and
its classic methods are different answers to them (RL 3). In language models the methods differ mostly in where the
grade comes from (RL 4). The frontier is moving to whole jobs in sandboxes, fuzzy tasks graded with rubrics, and models
that learn from their users (RL 5). Companies use, rent or sell it (RL 6), and robots are starting to practise. Through
all of it, RL only improves what you can score, so whoever writes the best grader wins.

## Check yourself

1. Put Recap's steps in order, starting from pre-training.
2. The value function says 40 steps to go. After action A it says 35; after action B it says 40. Using this chapter's
   formula, what is each action's advantage, and which one gets "Advantage: positive"?
3. Why can't a robot trained only on expert demonstrations recover from its own mistakes? Say it in your own words.

<details><summary>Answers</summary>

1. Pre-train with advantage labels built in; fine-tune on demonstrations for the task; deploy and collect labelled
   tries with expert corrections; train the value function; label every action positive or negative and retrain; run
   with "Advantage: positive"; repeat from deployment.
2. A: −1 + (−35) − (−40) = +4. B: −1 + (−40) − (−40) = −1. A gets "Advantage: positive".
3. Its demonstrations only show the expert doing the task well. Once the robot drifts a little, it's somewhere the
   expert never was, so the data has nothing to tell it how to get back, and each slip makes the next one more likely.

</details>

## Sources

- Physical Intelligence (2025), "π*0.6: a VLA That Learns From Experience", https://arxiv.org/abs/2511.14759 (v2,
  2025-11-19; abstract, Sections II, V-B, V-C) and blog https://www.pi.website/blog/pistar06 (2025-11-17).
- Chen et al. (2025), "πRL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models",
  https://arxiv.org/abs/2510.25889 (v1 abstract for the LIBERO numbers).
- Li et al. (2025), "SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning", https://arxiv.org/abs/2509.09674
- RLinf, https://github.com/RLinf/RLinf; TRL, https://github.com/huggingface/trl; verl,
  https://github.com/volcengine/verl; ART, https://github.com/OpenPipe/ART; verifiers,
  https://github.com/PrimeIntellect-ai/verifiers
- All checked 2026-11-13; quotes are in `library/rl.yaml`.
