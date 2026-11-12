# 2. π0, π0.5 and the checkpoint we run

After this chapter you can name the parts of π0.5, say what Physical Intelligence has released and which checkpoint
we use, and say exactly what that checkpoint receives at every step.
Needs: chapter 1. Reading time: 8 min.
Web version, with a real run you can step through, diagrams and side notes: https://blueif16.github.io/vla_final/learn/02-pi0-and-pi05.html

Here is one call to our model during our own LIBERO run (2026-11-11). The simulator sends two 224×224 pictures, one
from a camera facing the table and one from the wrist, and the sentence "pick up the black bowl between the plate and
the ramekin and place it on the plate". The model sends back 10 future actions of 7 numbers each. The robot runs the
first 5, the simulator takes new pictures, and the next call goes out. That's all the model ever gets: two pictures
and one sentence. Our run took 21 calls, and the simulator counted the task done at step 104. The web version of this
chapter shows every call of that run.

## The parts

π0.5 has two networks that share one attention pass.
- The VLM is PaliGemma, which pairs a SigLIP image encoder with the Gemma 2B language model. It reads the images and
  the instruction. SigLIP cuts each 224×224 picture into 16×16 patches of 14 pixels and turns each patch into a token,
  so a picture is 256 tokens. Gemma's tokenizer turns our sentence into 20 tokens (a start marker, 18 pieces for the
  17 words, since "ramekin" is cut in two, and a line break). In one call the model reads 532 tokens, and 20 of them
  are the sentence. A third camera slot is filled with a black picture and masked out, and so are the 180 unused text
  slots. These counts are from openpi's code and from running the tokenizer on 2026-11-11.
- The action expert is a smaller transformer (about 300M parameters; openpi's code comments 311M), with the same 18
  layers as Gemma. It can attend to everything the VLM computed, layer by layer, and it turns random noise into an
  action chunk with flow matching, over ten refinement steps in openpi. The VLM runs once per call and keeps what each
  layer computed; the action expert runs once per refinement step.

The instruction reaches the actions only through that attention. If the action expert learns to rely on the image
part of the VLM's output, the words can be read by the VLM and still change nothing downstream.

## From π0 to π0.5

π0 (October 2024) introduced this design. π0.5 (April 2025) kept it and changed the training. It was co-trained on
data from many kinds of robots plus web data such as captioning and question answering, and it learned to say the
next sub-step in words ("pick up pillow", in the paper's example) before acting. The goal was a robot that can clean a kitchen or bedroom
in a home it has never seen.

The π0.5 in openpi was also trained with knowledge insulation. During robot training, the action expert's gradients
are stopped from flowing back into the VLM, and the VLM learns from the same actions written as FAST tokens and from
web data instead, so robot training doesn't wear away what the VLM learned from the web. openpi supports only the
flow-matching action head for π0.5.

That insulation was used in pre-training, not in openpi's fine-tuning. Karl Pertsch of Physical Intelligence wrote on
GitHub (openpi issue #649, 2025-09-11) that openpi fine-tunes with the action expert's flow-matching loss only, and the
gradients go through both the action expert and the VLM. So `pi05_libero`'s 30,000 LIBERO steps trained every weight,
VLM included, without insulation. Whether that wore away any of its language following is open.

Physical Intelligence has since published π*0.6 (November 2025), which adds learning from the robot's own experience
with reinforcement learning. Its weights are not part of openpi, and we don't need it for this project.

## What openpi gives us

openpi is Physical Intelligence's open-source code (JAX, with a PyTorch port added in September 2025) and its model
checkpoints. π0.5 was added in September 2025. The two checkpoints that matter to us are these.

| Checkpoint | What it is |
|---|---|
| `pi05_base` | The general π0.5, the starting point for fine-tuning |
| `pi05_libero` | `pi05_base` fine-tuned on LIBERO; this is the model in our plan |

The README lists the GPU memory needed. Inference needs more than 8 GB, LoRA fine-tuning more than 22.5 GB, and full
fine-tuning more than 70 GB. LoRA training works only in the JAX version, since the PyTorch port doesn't support it.

## How `pi05_libero` was made

The `pi05_libero` training config in openpi starts from `pi05_base` and trains for 30,000 steps at batch size 256 on
the `physical-intelligence/libero` dataset. That dataset holds 1,693 demonstrations covering the 40 tasks of four LIBERO
suites (Spatial, Object, Goal and LIBERO-10), so one model handles all four. The instruction for each demonstration
is the task's sentence.

Two settings in that config matter for our tests. `action_horizon=10` gives the 10-action chunk. And
`discrete_state_input=False` means the robot's state is not given to the model at all. In LIBERO the state is eight
numbers: where the hand is (3), how it's turned (3) and how far apart the two gripper fingers are (2). openpi's
evaluation script still sends them with every call, and the model's input code drops them. In openpi's code, π0 adds
the state as an extra input, while π0.5 only adds it as text inside the prompt, and this config turns that off. This
is our reading of the code (`src/openpi/models/pi0.py`, `src/openpi/transforms.py`, `src/openpi/models/tokenizer.py`,
`examples/libero/main.py`), checked on 2026-11-11.

So at the first step of an episode the model knows only two things, the pictures and the sentence. If it ignores the
sentence, the pictures decide everything.

## The scores everyone quotes

openpi's LIBERO README reports these success rates for `pi05_libero` after 30k steps.

| Spatial | Object | Goal | LIBERO-10 | Average |
|---|---|---|---|---|
| 98.8 | 98.2 | 98.0 | 92.4 | 96.85 |

Some independent re-trainings from `pi05_base` report lower numbers (the BehaPi baseline gives 91.8, 94.6, 90.8 and
86.2, a 90.85 average), so our first job is to reproduce these numbers on our own setup before testing anything
new.

## Check yourself

1. What does `pi05_libero` receive at each call, and what does it send back?
2. If we want to fine-tune π0.5 with LoRA, which checkpoint do we start from, and how much GPU memory do we need?
3. Why does `discrete_state_input=False` make the blank-instruction test cleaner?
4. Of the 532 tokens the model reads in one call, how many come from the sentence, and by what route can they change
   the actions?
5. `pi05_base` was pre-trained with knowledge insulation. What happened to its VLM during the fine-tune that made
   `pi05_libero`, and why might that matter for our question?

<details><summary>Answers</summary>

1. Two images (table camera and wrist camera) and the instruction sentence. It returns 10 actions of 7 numbers.
2. `pi05_base`, in the JAX version of openpi, on a GPU with more than 22.5 GB.
3. With no robot state and no instruction, the images are the model's only input, so whatever it does comes from
   the pictures alone.
4. 20. They can change the actions only through attention, because the action expert reads what Gemma computed in
   each layer and never sees the sentence itself.
5. openpi has no insulation for fine-tuning, so the action expert's gradients flowed into the VLM for all 30,000 steps.
   The knowledge-insulation work found that this weakens language following, so the fine-tune could have worn away
   some of the reading `pi05_base` could do. That's a possibility to test, not a finding.

</details>

In questions 6 to 11, pick one answer before you open the answers. Each wrong option is a belief newcomers often
hold, and the answers say why each option is right or wrong. (On the web page, each option opens on its own.)

6. In our run, the call that started at step 30 had already planned to close the gripper, in its tenth action. Yet
   the gripper closed at step 37, during the next call. Why didn't the first call's plan close it?
   - A. The robot carried out all ten actions, and the gripper took a few steps to respond.
   - B. The robot runs only the first five actions of a chunk. The tenth action was thrown away, and the next call
     planned the close again from new pictures.
   - C. openpi blended the two calls' plans where they overlap, and the blend put the close later.
7. The action expert produces the actions. How does the instruction reach it?
   - A. In every layer the expert reads what Gemma computed, and the words are in there, mixed with 512 picture
     tokens.
   - B. The expert reads the sentence's 20 tokens as part of its own input.
   - C. Gemma first writes the next small step in words, and the expert acts on that.
8. Gemma reads the sentence in every call. What does that tell us on its own?
   - A. The sentence changes what the robot does, since the model reads it.
   - B. The robot ignores the sentence and goes by the pictures.
   - C. Nothing yet about whether the sentence changes the actions. That has to be tested.
9. π0.5 kept π0's design. Which two things did it change?
   - A. A new network design, and the robot's state as an extra input.
   - B. What it was trained on, and saying the next small step in words before it acts.
   - C. What it was trained on, and knowledge insulation in every fine-tune.
10. How was the VLM trained during the 30,000-step fine-tune that made `pi05_libero`?
    - A. With knowledge insulation, like `pi05_base`, so the action expert's gradients stopped before the VLM.
    - B. The action expert's gradients flowed into the VLM, and every weight trained.
    - C. The VLM was frozen, and only the action expert learned.
11. openpi's evaluation script sends eight numbers about the robot's hand and fingers with every call. What does
    `pi05_libero` do with them?
    - A. The action expert takes them as an extra input, next to its action tokens.
    - B. They're written into the prompt as text, next to the instruction.
    - C. Its input code drops them, so it has to judge where the arm is from the two pictures.

<details><summary>Answers to 6 to 11, with why each option is right or wrong</summary>

6. B is right.
   - A: No. The robot never carries out all ten. It runs the first five and then asks the model again, so the
     tenth action never ran.
   - B: Right. Each call's last five actions are dropped. The next call started at step 35 and put the close in its
     third action, which is step 37.
   - C: No. Nothing is blended. The robot runs the first five actions of the newest chunk, and the other five are
     thrown away.
7. A is right.
   - A: Right. Attention is the only route. Gemma reads the 20 word tokens together with the picture tokens, and the
     expert reads Gemma's layers, so the words reach the actions only as part of that mix.
   - B: No. The expert's own input is 10 action tokens, which start out as random numbers. It never takes in the
     sentence itself.
   - C: No. That's π0.5 in the paper. openpi supports only the flow-matching action head for π0.5, so `pi05_libero`
     goes from the instruction straight to actions. That last part is our reading of openpi's README.
8. C is right.
   - A: No, and this is the wrong belief the chapter warns about. The reading happens in Gemma, and the actions come
     from the action expert. If the pictures were enough during training, the expert could learn to give the words
     little weight.
   - B: No, that goes too far the other way. Nothing in this chapter shows the robot ignoring the words. It shows
     only that it could, and chapter 4 turns that into tests.
   - C: Right. Reading and using are separate questions. Gemma reads the sentence every time, and whether the
     sentence changes the robot's moves has to be measured. Chapter 4 sets up the tests, and chapter 5 shows what
     other groups found.
9. B is right.
   - A: No. π0.5 kept the design, PaliGemma plus an action expert. And our checkpoint, `pi05_libero`, gets no robot
     state at all.
   - B: Right. The paper says 97.6% of the first-phase training examples didn't come from the mobile robots π0.5
     was built for. And given "clean the bedroom", it first writes a step such as "pick up pillow".
   - C: No. The training data is right, but insulation was used only in pre-training. openpi's fine-tune doesn't
     have it, which is how `pi05_libero` was made.
10. B is right.
    - A: No. Insulation was used to pre-train `pi05_base`. openpi doesn't implement it for fine-tuning, as Karl
      Pertsch of Physical Intelligence confirmed on GitHub.
    - B: Right. openpi's fine-tune has one loss, the action expert's flow matching, and its gradients go through the
      expert and the VLM alike. The knowledge-insulation work found this weakens language following, so whether it
      did here is still open.
    - C: No. The `pi05_libero` config trains every weight, the VLM included. Nothing was frozen.
11. C is right.
    - A: No. That's how π0 takes the robot's state in openpi's code. π0.5 has no state input in the action expert.
    - B: No, though that is the one way π0.5 can take the state. The config sets `discrete_state_input=False`,
      which turns it off, so the prompt holds only the instruction.
    - C: Right. With the only way in turned off, the eight numbers arrive and are thrown away. At every call the
      model has the two pictures and the sentence, and nothing more.

</details>

## Sources

- Physical Intelligence (2025), π0.5: a Vision-Language-Action Model with Open-World Generalization,
  https://arxiv.org/abs/2504.16054
- Driess et al. (2025), Knowledge Insulating Vision-Language-Action Models, https://arxiv.org/abs/2505.23705
- Physical Intelligence (2025), π*0.6: a VLA That Learns From Experience, https://arxiv.org/abs/2511.14759
- Beyer et al. (2024), PaliGemma: A versatile 3B VLM for transfer, https://arxiv.org/abs/2407.07726 (224-pixel images
  give 256 image tokens)
- Karl Pertsch's answers in openpi issue #649 (2025-09-11 and 2025-09-12),
  https://github.com/Physical-Intelligence/openpi/issues/649
- Our run of openpi's `pi05_libero` checkpoint, 2026-11-11: `stage1/runs/recorded-call-spatial0/calls.json`
- openpi README, LIBERO README and `src/openpi/training/config.py` (`pi05_libero`), checked 2026-11-11,
  https://github.com/Physical-Intelligence/openpi
- Dataset card, https://huggingface.co/datasets/physical-intelligence/libero, checked 2026-11-11
- An independent re-training: BehaPi checkpoints, https://huggingface.co/xuewei-huang/BehaPi-ckpts (model card read
  2026-11-11)
