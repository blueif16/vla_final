# 6. Where we stand

This chapter is the team's status and changes as we decide things. It is the only place that says what is decided.
Anything not listed under "Decided" is open, including every option below.
Needs: chapters 1 to 5. Last updated: 2026-11-11.

## Decided

| What | When | Who |
|---|---|---|
| Team: Jingyi Fu and Shiran Wang | sign-up, November 2026 | both |
| The project is about VLAs | sign-up, November 2026; Shiran restated it on 2026-11-11 | both |

## Open

- **The research question.** Shiran (2026-11-11): "The research topic can be changed. Whatever the research topic is,
  it should focus on VLA-related knowledge." The submitted plan below is our current candidate.
- **The model and benchmark.** The submitted plan names `pi05_libero` and LIBERO. This holds for every option below,
  and it is still open until we agree on the question.

## The plan we submitted

From the CS 6180 sign-up sheet, in our words at the time.

> **How does a VLA actually understand the instruction? Testing language grounding in π0.5**
>
> We will run Physical Intelligence's open π0.5-LIBERO checkpoint in the LIBERO MuJoCo simulator. On every task in
> the four LIBERO suites, we will measure success rate over 50 trials under four prompts: the original instruction, a
> paraphrase, a blank prompt, and an instruction for a different task in the same scene. Success means a clear answer
> to whether the model's behavior depends on the words. For example, if a wrong instruction still produces the scene's
> usual task on LIBERO-Spatial and LIBERO-Object, the model is reading the scene rather than the language. If time
> allows, we will LoRA-fine-tune on the cluster with paraphrase augmentation and check whether grounding improves.

Chapter 5 shows that the blank and different-task arms have since been published for this checkpoint, and the
paraphrase arm at benchmark scale. That doesn't rule the plan out, but it changes what would be new.

## Options to weigh

None of these is chosen. Each row says what we'd measure, the nearest published work we found, and what it would
cost. The notes are our reading.

| Option | What we'd measure | Nearest published work | Cost | Note |
|---|---|---|---|---|
| A. The plan as submitted | four prompts × four suites, 8,000 episodes | LIBERO-CF, LIBERO-PRO, LIBERO-Plus | evaluation only | mostly a reproduction; useful as a check on our setup |
| B. When does reading stop? | LoRA fine-tune from `pi05_base` on LIBERO, save checkpoints along the way, and run the original, blank and different-task tests at each | none found on 2026-11-11 | LoRA training in JAX on a GPU with more than 22.5 GB, plus evaluation per checkpoint | the curve of "reading" against training steps would be new as far as we know |
| C. Data that forces reading | fine-tune with and without extra data where several tasks share a scene (LIBERO-90, or new instructions in existing scenes) and compare grounding | LangGap | like B, plus data preparation | close to LangGap, so we'd need a clear difference in design |
| D. Paraphrase augmentation (the submitted stretch goal) | fine-tune with paraphrased instructions and rerun the blank and different-task tests | LIBERO-Plus (tests paraphrases, doesn't train on them), LangGap | small, if added to B or C | paraphrases change the wording but keep one meaning per scene, so we'd predict the picture shortcut survives; that prediction is cheap to test |
| E. Look inside | probe or block the path from the instruction to the action expert and see where it stops mattering | Grant et al. 2026, Häon et al. 2025 | GPU for recording activations, little training | needs comfort with openpi's JAX model code |

We haven't researched VLA topics outside language grounding yet. If we want to look wider, the same search can be run
for other directions.

## A first step that helps every option

This is a proposal, not a decision. Each step is needed whichever option we pick, and together they give us a working
setup, one reproduced number and a clear choice for what's next.
1. Serve `pi05_libero` on the cluster and run the openpi LIBERO client.
2. Run the original instruction on one suite (500 episodes). Compare with the published 98.8 (Spatial) or 98.0 (Goal),
   and time one episode so we can price the rest.
3. Run the blank instruction on LIBERO-Goal and LIBERO-Spatial and compare with LIBERO-CF's 10.2 and 68.2.
4. Read LIBERO-CF and LangGap in full, then choose an option together.

## How to update this chapter

When we decide something, move it to "Decided" with the date and who decided, and change "Last updated". Keep the
submitted plan as it was written.
