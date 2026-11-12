# Learning path

Six short chapters take you from "what is a VLA?" to the decision our team has to make. Read them in order; each one
builds on the ones before. Every chapter ends with check questions and lists its sources.

| # | Chapter | What you'll be able to do | Time |
|---|---|---|---|
| 1 | [What a VLA is](01-what-a-vla-is.md) | say what goes into a vision-language-action model and what comes out | 8 min |
| 2 | [π0, π0.5 and the checkpoint we run](02-pi0-and-pi05.md) | say exactly what `pi05_libero` sees at each step | 8 min |
| 3 | [LIBERO, the benchmark](03-libero.md) | explain why a 98% score doesn't prove the robot reads | 8 min |
| 4 | [What "understanding the instruction" means](04-the-grounding-question.md) | describe the four prompt tests and what each result means | 8 min |
| 5 | [What other groups have already found](05-what-others-found.md) | say which parts of our plan are already published | 10 min |
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
