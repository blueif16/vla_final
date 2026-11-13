# Learning path

Six short chapters take you from "what is a VLA?" to the decision our team has to make. Read them in order; each one
builds on the ones before. Every chapter ends with check questions and lists its sources.

A second series, on reinforcement learning, is [further down](#reinforcement-learning-from-talking-machines-to-thinking-doing-machines).

| # | Chapter | What you'll be able to do | Time |
|---|---|---|---|
| 1 | [What a VLA is](01-what-a-vla-is.md) ([web](https://blueif16.github.io/vla_final/learn/01-what-a-vla-is.html)) | say what goes into a vision-language-action model and what comes out | 8 min |
| 2 | [π0, π0.5 and the checkpoint we run](02-pi0-and-pi05.md) ([web](https://blueif16.github.io/vla_final/learn/02-pi0-and-pi05.html)) | say exactly what `pi05_libero` sees at each step | 8 min |
| 3 | [LIBERO, the benchmark](03-libero.md) ([web](https://blueif16.github.io/vla_final/learn/03-libero.html)) | explain why a 98% score doesn't prove the robot reads | 10 min |
| 4 | [What "understanding the instruction" means](04-the-grounding-question.md) ([web](https://blueif16.github.io/vla_final/learn/04-the-grounding-question.html)) | describe the four prompt tests and what each result means | 10 min |
| 5 | [What other groups have already found](05-what-others-found.md) ([web](https://blueif16.github.io/vla_final/learn/05-what-others-found.html)) | say which parts of our plan are already published | 10 min |
| 6 | [Where we stand](06-where-we-stand.md) | name what's decided, what's open and the options we're weighing | 6 min |

Terms are collected in the [glossary](glossary.md).

## How the ideas connect

```
robot policy ──> VLA = vision-language model + action output        (ch. 1)
                   │
                   └─> π0.5: PaliGemma + action expert, flow matching
                         └─> pi05_libero sees 2 images + 1 sentence   (ch. 2)
                               │
LIBERO: 4 suites ──────────────┤  only LIBERO-Goal shares one scene   (ch. 3)
                               │  across all its tasks
                               v
grounding question: does changing the words change the behaviour?    (ch. 4)
                               │
published answers (LIBERO-CF, LIBERO-PRO, LIBERO-Plus, LangGap, ...)  (ch. 5)
                               │
                               v
what's left for us to do, and the choice in front of us              (ch. 6)
```

## Reinforcement learning: from talking machines to thinking, doing machines

Pretraining gave language models what they know. Reinforcement learning (RL) is the training that turned them into
models that work through a problem, use tools and finish a job, and it is how robots like π*0.6 get better with
practice. These seven chapters explain it from the ground up, for someone who uses AI tools and has seen a little
machine learning but no RL. There is almost no math. Where a formula helps, it comes with small numbers you can work
out by hand. By the end you can explain RL to a friend, predict how an RL setup will go wrong, place a lab's
announcement in the picture, and judge whether a task is worth training with RL at all.

The series stands on its own. Its examples come back to robots and to our project now and then, and chapter 7 joins
the two series.

| # | Chapter | What you'll be able to do | Time |
|---|---|---|---|
| RL 1 | [Learning from a score](rl-01-learning-from-a-score.md) | explain RL with five words and one loop, and say which tries a learner should repeat | 10 min |
| RL 2 | [Why it's hard: exploring, giving credit, and cheating](rl-02-why-its-hard.md) | predict the three ways an RL setup goes wrong | 8 min |
| RL 3 | [The classic methods, and the games that made them famous](rl-03-classic-methods.md) | tell a score sheet from a habit, a coach and an imagination, and name where each was used | 10 min |
| RL 4 | [Where the grade comes from: RL in language models](rl-04-rl-in-language-models.md) | say how a chat model is trained with RL and who or what grades it in each method | 10 min |
| RL 5 | [The frontier: whole jobs, fuzzy tasks and real users](rl-05-the-frontier.md) | place a lab's new RL strategy and say which problem it attacks | 11 min |
| RL 6 | [RL in companies: build, rent or sell](rl-06-rl-in-companies.md) | judge whether a company's task is worth RL, and which role fits | 9 min |
| RL 7 | [Robots that practise](rl-07-robots-that-practice.md) | explain how π*0.6 improves from its own tries, and what RL on LIBERO would need | 9 min |

Terms are in the same [glossary](glossary.md), marked RL 1 to RL 7.

### How the ideas connect

```
trial and error with a score: agent, environment, action, reward, policy   (RL 1)
   │
   ├─> why it's hard: exploring, credit assignment, reward hacking        (RL 2)
   │
   ├─> classic methods: score sheets, habits, a coach, imagination,       (RL 3)
   │   copying first; the games that made them famous
   │
   └─> language models: where the grade comes from                       (RL 4)
       (people, an AI judge, a checker, the group's average)
          │
          └─> the frontier: whole jobs in sandboxes, fuzzy tasks          (RL 5)
              graded by rubrics, models that learn from their users
                 │
                 ├─> companies: decision engines, use / rent / sell       (RL 6)
                 │
                 └─> robots that practice: π*0.6, RL on LIBERO,           (RL 7)
                     and the one rule: RL only improves what you can score
```
