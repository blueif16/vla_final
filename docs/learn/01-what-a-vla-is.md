# 1. What a vision-language-action model is

After this chapter you can say what goes into a VLA and what comes out, explain why people build one on top of a
vision-language model, and say what an action chunk is.
Needs: nothing. Reading time: 8 min.

A robot arm stands at a table with a black bowl, a plate and a small stove on it. Someone types "put the bowl on the
plate". From then on, several times a second, something has to decide how the arm and its gripper move next. A
vision-language-action model (VLA) is one neural network that makes that decision. It looks at the camera images,
reads the sentence, and returns the next few motions.

## What goes in and what comes out

Going in, there are usually one or two camera images (one camera looking at the table, one on the robot's wrist), the
instruction as text, and often the robot's own joint readings. Coming out are actions, which are just numbers that
tell the arm where to go. In the simulator we use (chapter 3), one action is seven numbers. Three move the hand along
x, y and z, three rotate it, and the last one opens or closes the gripper.

The robot runs the actions, the cameras take new pictures, and the model is asked again. This loop runs until the task
is done or time runs out. A network that maps what the robot sees to what it does is called a policy, so a VLA is a
policy that also reads language.

## Why start from a vision-language model

Robot data is expensive. Every training example is a person steering the robot through the task by hand
(teleoperation), so a single task might come with only 50 demonstrations. Vision-language models (VLMs) such as
PaliGemma have already been trained on billions of web images with text, so they know what a bowl looks like and what
"the one on the left" means. A VLA takes a VLM and keeps training it on robot demonstrations, so the robot can borrow
that knowledge instead of learning it from 50 examples.

Google's RT-2 (2023) made this idea widely known. OpenVLA (2024) was an open 7-billion-parameter version, and π0 (2024)
from Physical Intelligence is the family our project uses.

## Two ways to get actions out

The first way treats actions like words. Each action number is cut into 256 bins, and the model writes out bin numbers
the same way it would write text. RT-2 and OpenVLA work like this. It is simple, but writing long motions token by
token is slow and the bins are coarse.

The second way adds a smaller network next to the VLM, called an action expert. It starts from random noise and
refines it, in about ten steps, into a smooth sequence of real-valued actions. The refinement method is diffusion or
its close relative flow matching. π0 and π0.5 work like this.

## Action chunks

Both kinds of model usually predict several future actions at once, called an action chunk. π0 predicts 50 steps
ahead, and the LIBERO version of π0.5 predicts 10. The robot runs some of them (in the LIBERO evaluation script, the
first 5), then asks the model again with fresh images. Predicting ahead makes the motion smoother, and asking again
lets the robot correct itself.

## How a VLA learns

Training has three stages. The VLM is trained on web images and text. Then the whole VLA is trained on demonstrations
from many robots. Finally it is fine-tuned on the robot and tasks it will be tested on, such as the LIBERO benchmark.
In the robot stages the model learns by imitation (behaviour cloning). It sees a picture and an instruction, guesses
the action, and is corrected towards what the human operator actually did.

A common belief is that a model trained on instructions must be reading them. Imitation only learns what helps it copy
the demonstrations. If every scene in the training data comes with exactly one instruction, the picture alone already
tells the model what to do, and nothing in training rewards it for reading the words.

## What this means for our project

That last point is the root of our question. A VLA can score near 100% on a benchmark while ignoring the instruction,
as long as the benchmark never shows the same scene with two different instructions. Chapter 3 shows where LIBERO does
and doesn't do this, and chapter 4 turns it into tests.

## Check yourself

1. What goes into a VLA at each step, and what comes out?
2. A model predicts 10 actions per call and the robot runs 5 before calling again. How many calls does a 220-step
   episode take?
3. Why could a VLA trained on 40 instructions still ignore language? Explain it in your own words.

<details><summary>Answers</summary>

1. Camera images, the instruction text, and often the robot's joint readings go in. A chunk of future actions comes
   out, each one a small set of numbers for the arm and gripper.
2. 44 calls (220 ÷ 5).
3. It learns by copying demonstrations. If each scene in training appears with only one instruction, the image alone
   predicts the actions, so reading the words never lowers the training error, and nothing pushes the model to use
   them.

</details>

## Sources

- Brohan et al. (2023), RT-2, https://arxiv.org/abs/2307.15818
- Kim et al. (2024), OpenVLA, https://arxiv.org/abs/2406.09246
- Black et al. (2024), π0: A Vision-Language-Action Flow Model for General Robot Control, https://arxiv.org/abs/2410.24164
- openpi LIBERO evaluation script, `examples/libero/main.py` (`replan_steps = 5`), checked 2026-11-11,
  https://github.com/Physical-Intelligence/openpi
