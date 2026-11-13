# 5. What other groups have already found

After this chapter you can say which parts of our submitted plan have already been measured, quote the published
blank-instruction numbers for our exact checkpoint, and name what still looks open. You can also say in one sentence
each how CAG and LangGap's augmentation try to fix the problem.
Needs: chapters 1 to 4. Reading time: 10 min. Web version: https://blueif16.github.io/vla_final/learn/05-what-others-found.html

In February 2026 a group at the University of North Carolina ran the official π0.5 LIBERO checkpoint with the
instruction removed. On LIBERO-Spatial it still succeeded 68.2% of the time, and on LIBERO-Goal it fell to 10.2%. That
is the blank arm of our plan, on our model, already published.

The web page puts the two results next to the first camera picture of three tasks from each suite (frames from the
physical-intelligence/libero dataset, CC BY 4.0). Each of those Spatial tasks starts from its own arrangement, and the
three Goal pictures show one table.

This chapter lists what we found in a search on 2026-11-11, rechecked on 2026-11-13. The search was not exhaustive,
so a paper we missed can still change the picture.

## The numbers closest to our plan

The LIBERO-CF paper ("When Vision Overrides Language", Fang et al., CoRL 2026 spotlight) ran each official LIBERO
checkpoint three ways. V+L means images and instruction, vision-only means the instruction removed, and language-only
means the images removed. Success rates, from its Table I:

| Model | Inputs | Spatial | Object | Goal | Long | Average |
|---|---|---|---|---|---|---|
| π0.5 | V+L | 98.8 | 98.2 | 98.0 | 92.4 | 96.9 |
| π0.5 | vision-only | 68.2 | 56.6 | 10.2 | 71.6 | 51.7 |
| π0.5 | language-only | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| π0 | V+L | 96.8 | 98.8 | 95.8 | 85.2 | 94.2 |
| π0 | vision-only | 28.0 | 26.8 | 3.4 | 15.6 | 18.5 |
| π0 | language-only | 0.0 | 0.0 | 2.2 | 0.0 | 0.6 |
| OpenVLA-OFT | V+L | 97.6 | 98.4 | 97.9 | 94.5 | 97.1 |
| OpenVLA-OFT | vision-only | 83.2 | 98.2 | 10.0 | 85.0 | 69.1 |
| OpenVLA-OFT | language-only | 0.0 | 0.0 | 3.4 | 0.0 | 0.9 |

The language-only rows are in the paper's first two versions (19 February and 15 July 2026). The third version
(4 November 2026) calls the table Table 1 and leaves them out; its other rows are the same. π0.5's V+L row matches
openpi's own LIBERO README exactly, which is why we read it as the checkpoint we run.

π0.5 with no instruction still does the right task two times in three on Spatial and LIBERO-10. On Goal it lands at
10.2%, close to the one-in-ten guess from chapter 3. That fits the prediction in chapter 4.

The other two models dip on Goal as well. OpenVLA-OFT falls to 10.0% there and π0 to 3.4%. Away from Goal they
differ a lot. Without the words OpenVLA-OFT keeps 69.1% on average and π0 keeps 18.5%.

A common wrong belief: "π0.5 keeps 68.2% on Spatial with no instruction, so it ignores the words there." With the
instruction it scores 98.8% on the same suite, so the words are what carry it from 68.2% up to 98.8%. And on the one
Spatial pair whose two tasks start from the same table, our own run (experiment 1, 2026-11-11) went from 19 of 20 with
the sentence to 8 of 40 without it. With 10 episodes per task and setting the intervals are wide (10–35% without the
sentence). The table settles most Spatial episodes by itself, and the words decide the rest.

## A different task in the same scene

LIBERO-CF also built 50 counterfactual tasks, which give a different feasible instruction in an existing LIBERO scene,
often naming an object that was only background during training. That is the "different task, same scene" arm of our
plan. The paper finds that models often do the scene's familiar task instead of the one asked.

Its Figure 2 shows this in pictures. In two scenes from its Spatial part, π0.5's grasps over 50 trials cluster on the
black bowl when it gets the task it trained on. Asked for the cookie box, they spread between the box and the bowl, and
with no instruction they centre on the bowl. When the bowl is taken off the table, the cookie-box request succeeds (the
caption doesn't say which model that second panel shows).

The paper counts two outcomes for each new task. Faithful means the robot did the task it was asked for, and biased
means it did the scene's original training task instead. Averaged over the benchmark's four parts (its Table 3),
π0.5 finished the task it was asked for in 13.2% of episodes and the old task in 60.9%. Its grounding rate, how often
the gripper touched the object the instruction named, was 30.8%.

## CAG, a fix at run time

The paper then proposes Counterfactual Action Guidance (CAG), which runs the policy twice, once with the instruction
and once without, and pushes the action further in the direction the instruction moved it. In its equation 2 the
action sent is the action without words plus a weight times the difference between the two actions. A weight of 1
gives the ordinary action back, and the paper uses 1.5 for π0 and π0.5, so the action goes half as far again past
where the words took it. The rule is applied to every number of the predicted action chunk.

CAG works like classifier-free guidance in image generation (Ho and Salimans 2022), where a model makes one estimate
with the text prompt and one without and the picture is pushed further toward the prompt. In CAG's training-free
version the run without words is π0.5 itself with the instruction removed. The other version trains a separate
vision-action model that never sees instructions and uses it for that run.

The training-free version raised π0.5's grounding rate by 9.7 points and task success by 3.6 points on LIBERO-CF. In
Table 3's terms, success on the task asked for went from 13.2% to 16.8%, and the old task fell from 60.9% to 43.5%.
Even with CAG, the robot finished the scene's old task more often than the new one. The version with a separately
trained model does better, 21.7% against 36.2%, and there too the old task comes out ahead.

The web page draws the two runs and the push as our own figure, and its "go deeper" cards show three of the paper's
figures (CC BY 4.0). Figure 4 tries several weights: for π0.5, touching the named object rises from 39.3% at a weight
of 1 to 58.4% at 3, while finishing the task peaks at 31.6% at 1.5 and falls to 16.4% at 3. Its numbers at 1 and 1.5
match the paper's CF-Spatial results with a separately trained model (our reading; the caption doesn't name the
setting). The paper also tried CAG on a real Franka arm, where it raised grounding by 9.4 points and success by 17.2
on average.

## The other papers

| Paper | What they did | What they found |
|---|---|---|
| LIBERO-PRO (Zhou et al., Oct 2025) | changed objects, starting positions, instructions and environments | models above 90% fall to 0.0% in the changed settings; outputs stayed the same with corrupted instructions or meaningless tokens |
| LIBERO-Plus (Fei et al., Oct 2025; CVPR 2026) | 10,030 task variants across seven kinds of change, including LLM-rewritten instructions | models are largely insensitive to changes in wording and tend to ignore the instruction; camera angle and the robot's starting pose hurt most |
| LangGap (Hou and Zhao, Feb 2026) | π0.5 on new tasks that share one fixed layout, plus targeted data augmentation | augmentation raised success from 0% to 90% when trained on one task, but only from 0% to 28% with many tasks, and capacity looked like the limit as the tasks grew more varied |
| Not All Features Are Created Equal (Grant, Zhao and Wang, NeurIPS 2026 and an ICLR 2026 workshop) | looked inside π0.5, OpenVLA-OFT and others with probes, sparse autoencoders and activation injection | language matters only when the picture doesn't settle the goal; inside the model, different prompts can be told apart with 99.3% accuracy while behaviour stays the same; with an empty prompt their π0.5 kept 31.6% on LIBERO-Object and 5.8% on Goal, against 91.0% and 92.6% with the prompt |
| Mechanistic Interpretability for Steering VLAs (Häon et al., CoRL 2025) | found directions inside π0 and OpenVLA's layers linked to behaviours such as speed and direction | pushing on those directions steers the robot at run time in LIBERO and on a real arm |

The LIBERO-PRO, LIBERO-Plus, LangGap and Grant et al. rows come from the abstracts and project pages, plus the first
two sections of LIBERO-PRO's paper. We haven't read their full tables yet.

LIBERO-PRO's Figure 3 (CC BY 4.0, on the web page) shows the meaningless-token case. Told to pick up the salad
dressing and place it in the basket, the policy does. Given a meaningless string such as "fdsgfdsgsd" or "xxx"
instead, it still picks up the salad dressing and puts it in the basket. The paper evaluates OpenVLA, π0 and π0.5 and
doesn't say which one the figure shows.

## What still looks open

This part is our reading, written to be argued with. The web page maps each paper onto the arms of our plan. The
original-sentence, blank and different-task arms have measurements on `pi05_libero`. The paraphrase arm has them on
other models, or on setups we haven't checked. For when reading stops during fine-tuning, we found nothing.
- The blank and different-task arms of our plan have been measured for `pi05_libero`. The paraphrase arm has been run
  at benchmark scale by LIBERO-PRO and LIBERO-Plus. Running the plan as submitted would mostly reproduce known results.
- We found no study that tracks *when* during fine-tuning the model stops reading. The base π0.5 was trained to follow
  language; somewhere between `pi05_base` and `pi05_libero`, reading stopped mattering outside LIBERO-Goal.
- LangGap and Grant et al. both point at the training data, where one instruction per scene lets the picture stand in
  for the words. How much scene-sharing the data needs before the model reads is measured only in part.
- CAG fixes the problem at run time. Whether a cheap fine-tuning change does as well on the same tests is open.

## Check yourself

1. Which arm of our submitted plan has already been published for our exact checkpoint, and what did it show?
2. Why does π0.5's 10.2% on LIBERO-Goal with no instruction fit the explanation from chapter 4?
3. In one sentence each, how do LIBERO-CF's CAG and LangGap's augmentation try to fix the problem?

<details><summary>Answers</summary>

1. The blank-instruction arm (LIBERO-CF, Table I). π0.5 kept 68.2% on Spatial, 56.6% on Object and 71.6% on
   LIBERO-10, and fell to 10.2% on Goal. The different-task arm was published for it too, in LIBERO-CF's 50 new tasks.
2. All ten Goal tasks start from the same picture, so without words the model can only guess among ten, which gives
   about one in ten.
3. CAG runs the policy with and without the instruction at test time and amplifies the difference the instruction
   makes. LangGap trains on extra data where tasks share a layout, so the model has to use the words.

</details>

Multiple choice. Pick an answer before you open it.

4. π0.5 scores 68.2% on LIBERO-Spatial with no instruction. What does that tell you?
   A. It ignores the words on Spatial, since it does the task without them.
   B. The starting table settles most Spatial episodes, and the words still decide the rest.
   C. It understands spatial words such as "between" well enough to work out the task.
5. Why does π0.5 land at 10.2% on LIBERO-Goal with no instruction?
   A. All ten Goal tasks start from the same table, so without words it can't tell which one is wanted.
   B. Goal's tasks are harder to carry out, so it fails them more often.
   C. Without an instruction the robot doesn't move at all.
6. CAG runs π0.5 once with the instruction and once without. With the weight LIBERO-CF uses for π0.5, which action
   does it send?
   A. The average of the two actions.
   B. The action without words, because the picture alone is the more reliable guide.
   C. The action with words, pushed half as far again in the direction the words moved it.
7. On LIBERO-CF, training-free CAG raised π0.5's success on the task it was asked for from 13.2% to 16.8%. What did the
   robot finish most often, even with CAG?
   A. The task it was asked for.
   B. The scene's old training task.
   C. Nothing, because running the policy twice made it freeze.
8. LangGap's extra data took π0.5 from 0% to 90% when it trained on one new task, and from 0% to 28% when it trained
   on many. What did the authors read from this?
   A. Targeted data helps, but as the tasks grow more varied the model's capacity looks like the limit.
   B. Extra data solves the problem, since one task reached 90%.
   C. The model can't learn new tasks in a layout it already knows.
9. Which arm of our plan did our search find no study for?
   A. The blank instruction.
   B. The paraphrase.
   C. When during fine-tuning the model stops reading the words.

<details><summary>Answers to 4 to 9</summary>

4. B. With the words it scores 98.8%, so the words carry it from 68.2% up to 98.8%, and on the Spatial pair that
   shares a table our run fell from 19 of 20 to 8 of 40 without them (A is the wrong belief above). With no
   instruction there are no spatial words to understand, so C can't be it.
5. A. With one picture for ten tasks, a policy that ignores the words can at best pick one of them. With the
   instruction it scores 98.0% on Goal, so the tasks aren't harder (B), and without words it still finishes 10.2%, so
   it moves (C).
6. C. The weight is 1.5, so the action sent is the one without words plus 1.5 times the difference the words made. An
   average would be a weight of 0.5 (A), and the action without words a weight of 0 (B).
7. B. With CAG it finished the old task in 43.5% of episodes and the asked-for one in 16.8%. CAG moved both numbers the
   right way, and the old task still came out ahead.
8. A. That is the authors' reading in the abstract: the data partly closes the gap, and with more varied tasks even
   the trained ones did poorly. The 90% is for a single task (B), and it shows the model can learn one new task (C).
9. C, as far as our search on 2026-11-11 went. LIBERO-CF measured the blank arm on our exact checkpoint, and LIBERO-PRO
   and LIBERO-Plus tested reworded instructions at benchmark scale. None of the studies we found follows the words'
   effect across the training steps from `pi05_base` to `pi05_libero`. That is our reading.

</details>

## Sources

All checked 2026-11-11; rechecked and extended 2026-11-13.
- Fang et al. (2026), When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLAs,
  https://arxiv.org/abs/2602.17659 (CC BY 4.0; v1 19 Feb 2026, v2 15 Jul 2026, v3 4 Nov 2026; Table I of v1 and v2,
  Table 1 and Table 3 of v3, equation 2 and the weight 1.5 in section 6.2, Figures 2 to 5), project page
  https://vla-cf.github.io/, code https://github.com/yuffish/VLA-CF
- Zhou et al. (2025), LIBERO-PRO, https://arxiv.org/abs/2510.03827 (CC BY 4.0; abstract, sections 1 and 2 and Figure 3
  of v2)
- Fei et al. (2025), LIBERO-Plus, https://arxiv.org/abs/2510.13626 and https://sylvestf.github.io/LIBERO-plus/
- Hou and Zhao (2026), LangGap, https://arxiv.org/abs/2603.00592
- Grant, Zhao and Wang (2026), Not All Features Are Created Equal, https://arxiv.org/abs/2603.19233 and
  https://cwru-aism.github.io/vla-interp-page/ (the 99.3% is from the page as archived on 2026-03-20,
  https://web.archive.org/web/20260320025957/https://cwru-aism.github.io/vla-interp-page/; the page read on 2026-11-13
  says more than 99% and gives the empty-prompt numbers)
- Häon et al. (2025), Mechanistic Interpretability for Steering Vision-Language-Action Models,
  https://arxiv.org/abs/2509.00328 (CC BY 4.0)
- Ho and Salimans (2022), Classifier-Free Diffusion Guidance, https://arxiv.org/abs/2207.12598
- Our experiment 1, 2026-11-11: `stage1/results/exp1-shared-table.md`
- physical-intelligence/libero (CC BY 4.0), frame 0 of episodes 379, 388, 392, 1262, 1264 and 1283,
  https://huggingface.co/datasets/physical-intelligence/libero
