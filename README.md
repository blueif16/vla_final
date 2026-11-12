# CS 6180 final project: vision-language-action models

We're Jingyi Fu and Shiran Wang, a team in CS 6180, and our final project is about vision-language-action models
(VLAs). This repo holds what we've learned so far and the question we're working on. Our code and results will go
here too as the project moves.

## What a VLA is

A VLA is the model behind a robot that looks through its cameras, reads an instruction such as "put the bowl on the
plate", and moves its arm to do it. It's built on a vision-language model, the kind trained on billions of web images
and captions, and then trained further on recordings of people steering robots through tasks. Several times a second
it takes the camera images and the sentence and returns the next few motions for the arm and gripper.

## The question we started from

π0.5, an open VLA from Physical Intelligence, succeeds about 98% of the time on LIBERO, a widely used set of simulated
robot tasks. We wanted to know how much of that comes from reading the instruction. In most LIBERO tasks the objects
on the table are arranged differently for each task, so the picture alone gives away which task it is. A robot could
score well without reading the words at all.

So our first plan was to change the instruction and watch whether the robot's behaviour changes with it. We'd reword
it, remove it, or ask for a different task in the same scene, and measure success over 50 trials per task on all four
LIBERO suites.

Other groups have since measured part of this. With the instruction removed, the same π0.5 checkpoint still succeeds
68.2% of the time on LIBERO-Spatial. On LIBERO-Goal, the one suite where all ten tasks start from the same scene, it
falls to 10.2% ([Fang et al., 2026](https://arxiv.org/abs/2602.17659)).

## What we're studying now

We kept the question and widened it. When π0.5 does a household task, what is it actually going by: the words, what
each camera shows, or the layout it remembers from training? Each experiment changes one of these the way a real home
would. We erase the instruction, reword it, black out a camera, bump it, or move the plate, and then count how often
the robot still succeeds and record videos of what it does. We start in LIBERO's kitchen scenes, and if a trial run
works we move on to a π0.5 model that folds laundry in simulation. [`topic.md`](topic.md) has the question, the
experiments and the steps, and [where we stand](docs/learn/06-where-we-stand.md) records what we've decided.

## Learn the background

The chapters are also a website, with diagrams you can play with, talk clips that start at the right moment and side
notes for every term: **[blueif16.github.io/vla_final](https://blueif16.github.io/vla_final/)** (chapters 1 and 2 so far).

[`docs/learn`](docs/learn/README.md) has six short chapters, about 50 minutes in all. They go from what a VLA is,
through π0.5 and the LIBERO benchmark, to what other groups have found and the choice in front of us. Each chapter
ends with questions to check yourself and lists its sources.

## Learning with an AI agent

You can open this repo in Claude Code, Codex or another coding agent and ask it to teach you. [`AGENTS.md`](AGENTS.md)
tells the agent how. It goes one chapter at a time, asks the check questions, and keeps what we've decided apart from
what's still open.

## What's in the repo

| Path | What it holds |
|---|---|
| `topic.md` | our research question, the three stages, the experiments and the steps |
| `docs/learn/` | the learning chapters as markdown and web pages, the glossary and our status ([chapter 6](docs/learn/06-where-we-stand.md)) |
| `docs/assets/` | the website's styles, scripts, shared glossary of terms and images |
| `library/` | every clip time, image licence and checked number we've found, so later chapters reuse them |
| `AGENTS.md` | instructions for an AI agent teaching from this repo (`CLAUDE.md` points to it) |
| `.claude/skills/teaching/`, `.claude/skills/teaching-web/` | how we write teaching chapters and turn them into web pages, so an agent can add more the same way |
