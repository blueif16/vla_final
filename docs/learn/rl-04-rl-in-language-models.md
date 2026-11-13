# RL 4. Where the grade comes from: RL in language models

After this chapter you can say how a chat model is trained with RL, name who or what grades it in each of the common
methods, and work out which answers in a group get pushed up.
Needs: RL 1 to RL 3. Reading time: 10 min.

In March 2022 OpenAI published InstructGPT. People who compared its answers with those of GPT-3 preferred the
answers of a 1.3-billion-parameter InstructGPT model to those of the 175-billion-parameter GPT-3, even though the
smaller model had, in the paper's words, "100x fewer parameters". The smaller model didn't know more. It had been trained with RL on what people preferred. Eight
months later OpenAI released ChatGPT, trained the same way.

## A language model is already a policy

The five words from RL 1 fit a language model without much stretching. The agent is the model. An action is the next
token, a word or a piece of one. One episode is one whole answer. The environment is the prompt, and later the tools
the model can use (a terminal, a browser, a code repository). The reward is a score for the whole answer, and it
usually comes only at the end.

The step that experts take for granted is the policy. A language model, before any RL, already gives every possible
next token a chance of being picked. That is exactly what RL 1's rule needs: sample some answers, score them, and make
the tokens in the better-than-average answers a little more likely. The model gives tens of thousands of chances at
every token, which is why language models are trained with policy-gradient methods (RL 3) and not with score sheets.

## A model's education in four stages

1. **Pretraining.** The model reads a huge amount of text and learns to predict the next word. This is where its
   knowledge comes from.
2. **Supervised fine-tuning.** It studies worked examples written by people: a question and a good answer. This
   teaches it the format of an answer and basic manners.
3. **Preference RL.** A grader judges its answers for tone, helpfulness and safety, and RL pushes it towards the ones
   graded better. This teaches judgement.
4. **Verifiable and agentic RL.** It practises on tasks with an automatic grade: maths problems with known answers,
   code repositories with failing tests, and jobs in a browser or a terminal. This teaches skill.

Stages 1 and 2 are the copying step from RL 3, and stages 3 and 4 are the practice. Ten years ago RL, when it was used
at all, was a final polish. Today stage 4 is where much of a frontier model's reasoning and agent skill comes from
(chapter 5).

## Where the grade comes from

The methods for language models differ mostly in one thing: who or what gives the score.

**People's preferences (RLHF, reinforcement learning from human feedback).** InstructGPT did it in three steps. People
wrote example answers for supervised fine-tuning. Then people were shown two or more answers to the same prompt and
picked the better one, and a second network, the reward model, learned to predict which answer they would pick. Then
the chat model was trained with PPO (RL 3) to get high scores from the reward model. People only grade a sample once;
the reward model then grades millions of answers during training. Because the reward model is itself a network that
learned from examples, the chat model can find answers it scores well that people wouldn't like (RL 2's reward
hacking).

**An AI judge with written principles (RLAIF, Constitutional AI).** For judging harmlessness, Anthropic replaced the
human comparisons with an AI model that compares answers against a written list of principles, which they called a
constitution. In the paper's words, "the only human oversight is provided through a list of rules or principles". AI
feedback costs far less than people's time, so it scales to many more comparisons.

**No judge at all (DPO, direct preference optimisation).** DPO trains directly on pairs of answers where one was
preferred. It raises the chance of the preferred answer and lowers the chance of the rejected one, compared with the
model it started from. There's no separate reward model to train and no loop of sampling new answers; the paper's
title says the language model is "secretly a reward model". It's RL-flavoured but not RL in
RL 1's sense, because the model never tries anything during training; it only learns from answers already written.
DPO is cheap and simple, which is why many open models use it.

**A checker (RLVR, reinforcement learning with verifiable rewards).** For some tasks the grade can be computed. The
final number of a maths problem matches the answer key or it doesn't, and the code passes its tests or it doesn't. A
checker like this is much harder to fool than a learned reward model, though RL 2 showed that tests can be gamed too.
OpenAI's o1 (September 2024) was trained with RL to work through a problem in a chain of thought before answering, and
it got better both with more RL and with more time spent thinking. DeepSeek-R1 (January 2025) published a recipe
that others could copy. Its first version, R1-Zero, was trained with RL only, without the worked examples of stage 2,
and with rewards from simple rules for a correct answer and the right format. Habits such as going back over its
earlier steps and trying another approach appeared during training without anyone showing them.

**The group's own average (GRPO).** PPO needs a coach network (RL 3), and for a language model the coach is
typically, as the DeepSeekMath paper puts it, "another model of comparable size as the policy model". GRPO, from that
paper (2024), drops the coach. It samples a group of answers to the same question, scores them all, and uses the
group's average as the baseline, which is RL 1's rule again. DeepSeekMath sampled 64 answers per question; the
default in Hugging Face's TRL library is 8. Say 8 answers come back and 3 are right (score 1) and 5 are wrong (score 0). The average is 3/8 = 0.375. Each
right answer gets +0.625 and each wrong one −0.375. GRPO also divides by how spread out the scores are, which in this
group turns them into about +1.29 and −0.77. If all 8 answers are right, or all 8 are wrong, every answer gets 0 and
the model learns nothing from that question, which is RL 2's exploration problem showing up again. So the questions
that teach the most are the ones the model gets right some of the time.

**Many steps in a sandbox (agentic RL).** The model works through a whole task in a terminal, a browser or a code
repository, taking many actions, and is graded at the end on what happened: did the tests pass, was the right file
changed, was the answer found. Anthropic's Claude 3.7 Sonnet with extended thinking, together with a preview of
Claude Code, and OpenAI's Deep Research, both in February 2025, were early products trained this way.

| Method | Where the grade comes from | Famous use |
|---|---|---|
| RLHF | people compare answers; a reward model learns their taste and scores the model | InstructGPT, ChatGPT |
| RLAIF / Constitutional AI | an AI judge following written principles | Anthropic's Claude |
| DPO | no judge and no RL loop; push the preferred answer up and the rejected one down | many open models |
| RLVR | a checker: does the maths match, does the code pass its tests | o1, DeepSeek-R1 |
| GRPO | a group of answers to one question; each is compared with the group's average | DeepSeek; most open-source RL |
| agentic RL | many steps in a sandbox, graded at the end | coding agents, computer use, research agents |

## Key moments, 2017 to early 2025

| When | What happened | Why it mattered |
|---|---|---|
| 2017 | RL from human preferences (Christiano et al.); PPO | the two ingredients of RLHF |
| Mar 2022 | InstructGPT | a 1.3B model trained with RLHF preferred over the 175B GPT-3 |
| Nov 2022 | ChatGPT | RLHF goes mainstream |
| Dec 2022 | Constitutional AI | AI feedback replaces much human labelling |
| May 2023 | DPO | cheap preference tuning; the default for many open models |
| Sep 2024 | OpenAI o1 | RL on chains of thought; thinking longer becomes a way to get better answers |
| Nov 2024 | Tülu 3 names RLVR | verifiable rewards written up in the open |
| Dec 2024 | OpenAI reinforcement fine-tuning preview | RL sold to companies as a service (chapter 6) |
| Jan 2025 | DeepSeek-R1 | an open recipe; reasoning grows out of RL with rule-based rewards |
| Feb 2025 | Claude 3.7 Sonnet with extended thinking and Claude Code preview; OpenAI Deep Research | reasoning and agentic RL ship as products |

What came after is chapter 5.

## The wrong belief: people grade the answers

It's easy to picture RL for chat models as people reading answers and scoring them, all through training. Even in
RLHF, people grade only a sample, once, and the reward model does the grading during training. In RLVR nobody grades
anything. DeepSeek-R1-Zero's rewards came from rules that checked the final answer and the format.

## What this means for our project

LIBERO's goal check is a verifiable reward, the robot version of an RLVR checker: the bowl is on the plate or it
isn't. The group trick carries over too. Run the same task several times from the same start, and compare each try
with the group's average. Chapter 7 shows a LIBERO paper that did this.

## Check yourself

1. Where does the grade come from in RLHF, DPO, RLVR and GRPO?
2. A model answers one question four times, and the checker scores the answers 1, 1, 0 and 0. Before dividing by the
   spread, what does GRPO give each answer? What happens if all four score 1?
3. Why is a checker harder to fool than a reward model trained on people's preferences? Say it in your own words.

<details><summary>Answers</summary>

1. RLHF: a reward model that learned from people's comparisons. DPO: there is no grader during training, only pairs
   of answers people (or an AI) already ranked. RLVR: a checker, such as an answer key or a test suite. GRPO: any of
   these scores, compared with the average of a group of answers to the same question.
2. The average is 0.5, so the two right answers get +0.5 and the two wrong ones −0.5. If all four score 1, the
   average is 1 and every answer gets 0, so the model learns nothing from that question.
3. A reward model is a network that learned people's taste from a limited set of examples, so it has blind spots, and
   RL will find answers that score high in them. A checker tests the thing itself (is the answer right, do the tests
   pass), so there are far fewer ways to score high without doing the task. Fewer, not none: tests can be special-cased
   (RL 2).

</details>

## Sources

- Ouyang et al. (2022), "Training language models to follow instructions with human feedback" (InstructGPT),
  https://arxiv.org/abs/2203.02155
- Christiano et al. (2017), "Deep reinforcement learning from human preferences", https://arxiv.org/abs/1706.03741
- Bai et al. (2022), "Constitutional AI: Harmlessness from AI Feedback", https://arxiv.org/abs/2212.08073
- Rafailov et al. (2023), "Direct Preference Optimization", https://arxiv.org/abs/2305.18290
- Lambert et al. (2024), "Tülu 3", https://arxiv.org/abs/2411.15124
- OpenAI (2024), "Learning to reason with LLMs", https://openai.com/index/learning-to-reason-with-llms/
- DeepSeek-AI (2025), "DeepSeek-R1", https://arxiv.org/abs/2501.12948
- Shao et al. (2024), "DeepSeekMath" (GRPO), https://arxiv.org/abs/2402.03300
- Dates, quotes and the date we checked each one are in `library/rl.yaml`.
