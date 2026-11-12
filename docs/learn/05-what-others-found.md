# 5. What other groups have already found

After this chapter you can say which parts of our submitted plan have already been measured, quote the published
blank-instruction numbers for our exact checkpoint, and name what still looks open.
Needs: chapters 1 to 4. Reading time: 10 min.

In February 2026 a group ran the official π0.5 LIBERO checkpoint with the instruction removed. On LIBERO-Spatial it
still succeeded 68.2% of the time, and on LIBERO-Goal it fell to 10.2%. That is the blank arm of our plan, on our
model, already published.

This chapter lists what we found in a search on 2026-11-11. The search was not exhaustive, so a paper we missed can
still change the picture.

## The numbers closest to our plan

The LIBERO-CF paper ("When Vision Overrides Language", Fang et al., CoRL 2026 spotlight) ran each official LIBERO
checkpoint three ways. V+L means images and instruction, vision-only means the instruction removed, and language-only
means the images removed. Success rates, from its Table I:

| Model | Inputs | Spatial | Object | Goal | Long | Average |
|---|---|---|---|---|---|---|
| π0.5 | V+L | 98.8 | 98.2 | 98.0 | 92.4 | 96.9 |
| π0.5 | vision-only | 68.2 | 56.6 | 10.2 | 71.6 | 51.7 |
| π0.5 | language-only | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| π0 | vision-only | 28.0 | 26.8 | 3.4 | 15.6 | 18.5 |
| OpenVLA-OFT | vision-only | 83.2 | 98.2 | 10.0 | 85.0 | 69.1 |

π0.5 with no instruction still does the right task two times in three on Spatial and LIBERO-10. On Goal it lands at
10.2%, close to the one-in-ten guess from chapter 3. That fits the prediction in chapter 4.

LIBERO-CF also built 50 counterfactual tasks, which give a different feasible instruction in an existing LIBERO scene,
often naming an object that was only background during training. That is the "different task, same scene" arm of our
plan. The paper finds that models often do the scene's familiar task instead of the one asked. It then proposes
Counterfactual Action Guidance (CAG), which runs the policy twice, once with the instruction and once without, and
pushes the action further in the direction the instruction moved it. CAG works like classifier-free guidance in image
generation. The training-free version raised π0.5's grounding rate by 9.7 points and task success by 3.6 points on
LIBERO-CF.

## The other papers

| Paper | What they did | What they found |
|---|---|---|
| LIBERO-PRO (Zhou et al., Oct 2025) | changed objects, starting positions, instructions and environments | models above 90% fall to 0.0% in the changed settings; outputs stayed the same with corrupted instructions or meaningless tokens |
| LIBERO-Plus (Fei et al., Oct 2025; CVPR 2026) | 10,030 task variants across seven kinds of change, including LLM-rewritten instructions | models are largely insensitive to changes in wording and tend to ignore the instruction; camera angle and the robot's starting pose hurt most |
| LangGap (Hou and Zhao, Feb 2026) | π0.5 on new tasks that share one fixed layout, plus targeted data augmentation | augmentation raised success from 0% to 90% when trained on one task, but only from 0% to 28% with many tasks, and capacity looked like the limit as the tasks grew more varied |
| Not All Features Are Created Equal (Grant, Zhao and Wang, ICLR 2026) | looked inside π0.5, OpenVLA-OFT and others with probes, sparse autoencoders and activation injection | language matters only when the picture doesn't settle the goal; inside the model, different prompts can be told apart with 99.3% accuracy while behaviour stays the same |
| Mechanistic Interpretability for Steering VLAs (Häon et al., CoRL 2025) | found directions inside π0 and OpenVLA's layers linked to behaviours such as speed and direction | pushing on those directions steers the robot at run time in LIBERO and on a real arm |

The LIBERO-PRO, LIBERO-Plus, LangGap and Grant et al. rows come from the abstracts and project pages. We haven't read
their full tables yet.

## What still looks open

This part is our reading, written to be argued with.
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
   LIBERO-10, and fell to 10.2% on Goal.
2. All ten Goal tasks start from the same picture, so without words the model can only guess among ten, which gives
   about one in ten.
3. CAG runs the policy with and without the instruction at test time and amplifies the difference the instruction
   makes. LangGap trains on extra data where tasks share a layout, so the model has to use the words.

</details>

## Sources

All checked 2026-11-11.
- Fang et al. (2026), When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLAs,
  https://arxiv.org/abs/2602.17659, code https://github.com/yuffish/VLA-CF
- Zhou et al. (2025), LIBERO-PRO, https://arxiv.org/abs/2510.03827
- Fei et al. (2025), LIBERO-Plus, https://arxiv.org/abs/2510.13626
- Hou and Zhao (2026), LangGap, https://arxiv.org/abs/2603.00592
- Grant, Zhao and Wang (2026), Not All Features Are Created Equal, https://arxiv.org/abs/2603.19233 and
  https://cwru-aism.github.io/vla-interp-page/
- Häon et al. (2025), Mechanistic Interpretability for Steering Vision-Language-Action Models,
  https://arxiv.org/abs/2509.00328
