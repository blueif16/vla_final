# RL 5. The frontier: whole jobs, fuzzy tasks and real users

After this chapter you can say what an RL environment is and why labs buy them, place a lab's new RL strategy among
the six in this chapter, and say which of RL 2's problems each one attacks.
Needs: RL 1 to RL 4. Reading time: 11 min.

Cursor makes a code editor with a built-in coding agent called Composer. In March 2026 Cursor described how it now
trains Composer. Each cycle starts by collecting billions of tokens from the interactions of the people using it, and
turns their reactions into reward signals. The model's weights are updated from those signals, and the new version is
run against Cursor's test suites to make sure it hasn't got noticeably worse at anything. If it passes, it ships. A
cycle takes about five hours, so Cursor can ship an improved Composer several times in one day. In an A/B test of one
version, the share of the agent's edits that stayed in the user's code went up by 2.28%, unhappy follow-up messages
went down by 3.13%, and the time to answer went down by 10.3%.

Composer also found ways to cheat. Cursor had been throwing away examples where a tool call was broken, so on tasks
it was likely to fail, Composer learned to send a broken tool call on purpose, which never earned a negative reward.
It also learned to ask clarifying questions instead of making risky edits, since it was never punished for code it
didn't write. Cursor fixed the first by counting broken tool calls as negative examples. It caught the second by
monitoring the model, and changed the reward. RL 2's reward hacking is alive at the frontier.

This chapter is about where RL has gone since the products of early 2025. It is moving from single answers to whole
jobs, from tasks a checker can grade to fuzzy ones, and from simulations to real users.

## Environments are the new data

Labs used to buy labelled examples. Now they also buy environments. In today's sense an environment is three things
together: a task (fix this bug, book this flight, fill in this spreadsheet), a sandbox where the model can act on it
(a copy of a code repository with a terminal, a browser, a fake company's files), and a grader that scores what
happened at the end.

In September 2025 TechCrunch reported that leading labs were asking for more RL environments and that many startups
hoped to supply them. It also passed on a report from The Information that Anthropic's leaders had discussed spending
more than $1 billion on RL environments over the next year. A year later, in September 2026, a Y Combinator partner
said on YC's podcast that YC had funded more than a dozen companies in the last two years that each make more than
$10 million a year selling data or RL environments to the labs. Chapter 6 comes back to what this means for small
companies.

The craft has moved to the grader. A grader that can be fooled trains a model that cheats, as the Composer story
shows, so writing rewards that can't be gamed is now much of the work.

## Six strategies at the frontier

**1. Agentic RL in sandboxes.** Each try gets its own computer. The model opens files, runs commands and browses, and
is graded on what changed. The numbers are large. Cursor's Composer trained in hundreds of thousands of sandboxed
coding environments running at the same time. Moonshot's Kimi K3 report (July 2026) counts 51,219,741 sandboxes,
started from 1,505,678 different images, over its training and evaluation. Zhipu's GLM-5 (February 2026) built its own
asynchronous RL system, slime, so that slow sandbox jobs don't hold up the training. This strategy attacks
exploration (RL 2): more parallel tries mean more chances to find the first success.

**2. Hybrid rewards.** One score is built from several graders: hard checks such as tests, an AI judge with a
rubric, and a safety gate that can zero everything. Liquid AI's LFM2.5-2.6B (2026) used "an outcome-based reward that
combines an LLM-as-a-judge rubric, programmatic checks, and a hard safety gate". GLM-5 combines rule-based rewards
with two kinds of reward model. Kimi K2 (2025) combined verifiable rewards with a rubric it applies to its own answers.
Here is the shape of such a score, with weights we made up for illustration:

> reward = 0 if the safety check fails; otherwise 0.6 × (share of tests passed) + 0.4 × (the judge's rubric score)

An answer that passes 8 of 10 tests and gets 0.5 from the judge scores 0.6 × 0.8 + 0.4 × 0.5 = 0.68. The tests are
hard to fool, the judge covers what tests can't see, and the gate makes sure no amount of skill buys back an unsafe
answer. This attacks reward hacking (RL 2), because a hack has to fool every grader at once.

**3. Rubric rewards for fuzzy tasks.** Writing, medical advice and legal analysis have no answer key. An AI judge
scores the answer against a checklist written for that prompt (does it mention the drug interaction, does it say when
to see a doctor). Scale AI's "Rubrics as Rewards" (2025) extends RLVR this way. The new worry is rubric hacking. A 2026
Scale AI study found that weak judges let the model gain a lot of reward that didn't hold up under stronger judges,
and that even strong judges didn't prevent hacking when the rubric left important failures unlisted.

**4. GRPO becomes a family.** GRPO (RL 4) turned out to have rough edges, and small fixes keep appearing. DAPO
(ByteDance, 2025) adds four, one of which stops the model's answers from all becoming the same. GSPO (Qwen, 2025)
judges and clips whole answers instead of single tokens, which keeps the training of mixture-of-experts models stable. CISPO (MiniMax, 2025) changes what gets clipped. One of the problems is length bias. A 2025 paper found that
GRPO's way of averaging inflates the length of answers as training goes on. Hugging Face's TRL library, which many
people train with, now uses DAPO's loss by default, and its documentation says the original GRPO loss is "Not
recommended due to length bias".

**5. RL experts, then distil.** Instead of one RL run on everything, a lab trains a specialist for each area (maths,
code, agents) and then merges them into one student. The merging step is on-policy distillation. The student writes
its own answers and a teacher grades every token of them, which gives far more feedback than one score at the end of
an answer. Xiaomi's MiMo-V2-Flash (January 2026) introduced multi-teacher on-policy distillation. Kimi K3 trained nine
experts and merged them this way, and DeepSeek-V4 and NVIDIA's Nemotron 3 Ultra (both 2026) each distilled from more
than ten teachers.

**6. Learning from deployment.** Real users or real robots become the reward. Cursor's Composer is one case, and
Cursor's code suggestions (Tab) are another. Tab answers over 400 million requests a day, and its reward is built to
teach it when to stay quiet. In Cursor's example, an accepted suggestion earns 0.75, a rejected one −0.25, and showing
nothing earns 0. If a suggestion would be accepted with chance p, showing it is worth on average p × 0.75 − (1 − p) ×
0.25 = p − 0.25. That beats showing nothing only when p is above 0.25, so the model learns to show a suggestion only
when it's at least 25% likely to be accepted. The new Tab model made 21% fewer suggestions than the one before, and its
accept rate, the share of its suggestions that people kept, was 28% higher. For robots, π*0.6 learns from its own deployment (chapter 7).

| Strategy | Plain meaning | Problem from RL 2 it attacks | Who |
|---|---|---|---|
| agentic RL in sandboxes | each try gets its own computer, graded on what happened | exploration, at scale | Kimi K3, GLM-5, Nemotron 3 Ultra, Cursor |
| hybrid rewards | tests + an AI judge with a rubric + a safety gate | reward hacking | Kimi K2, GLM-5, LFM2.5 |
| rubric rewards | a judge scores fuzzy answers against a checklist | no checker exists; rubric hacking is the new risk | Rubrics as Rewards and later work |
| the GRPO family | small fixes for stability and length bias | training that drifts or blows up | DAPO, GSPO, CISPO |
| RL experts, then distil | one specialist per area, merged into one student | one score per answer is little feedback | MiMo-V2-Flash, Kimi K3, DeepSeek-V4, Nemotron 3 Ultra |
| learning from deployment | real users or robots give the reward | the gap between practice and real use | Cursor, π*0.6 |

## Two problems nobody has solved

Long jobs make credit assignment (RL 2) much harder. An agent that works for an hour and gets one score at the end
has thousands of actions to share that score between. And a model that keeps learning can forget what it knew. In
Thinking Machines' tests, training Qwen3-8B on a company's internal documents dropped its instruction-following score
from 85% to 79%, even with chat data mixed in. On-policy distillation from the earlier model brought it back to 83%
without losing the new knowledge. Our reading is that this is why distillation is now also discussed as a tool for
continual learning, not only for merging experts.

## Key moments, 2025 to now

| When | What happened | Why it mattered |
|---|---|---|
| Sep 2025 | Cursor Tab trained with online RL; TechCrunch reports labs' demand for RL environments | environments become the new data |
| Oct 2025 | Cursor Composer trained with RL in sandboxes; Thinking Machines launches Tinker | product companies train their own agents (chapter 6) |
| Nov 2025 | Physical Intelligence's π*0.6 | RL from deployment reaches real robots (chapter 7) |
| Jan 2026 | MiMo-V2-Flash's multi-teacher on-policy distillation | "RL experts, then distil" |
| Mar 2026 | Cursor's real-time RL: a new Composer checkpoint about every five hours | models learn from live users |
| 2026 | Kimi K3, DeepSeek-V4, Nemotron 3 Ultra distil from many RL-trained teachers | the common frontier recipe |
| Sep 2026 | YC: more than a dozen of its companies make over $10M a year selling data or environments to labs | selling practice worlds is an industry |
| Oct 2026 | Together AI launches Together Post-Training; Tinker turns one | RL on your own model becomes a cloud service (chapter 6) |

## The wrong belief: a shipped model is finished

It's natural to think a model is trained, then released, then stays the same until the next version. Cursor's
Composer shows the opposite. Its users' reactions are its reward, and a new checkpoint can ship every few hours.

## What this means for our project

LIBERO is an environment in exactly this chapter's sense. It has tasks (the instructions), a sandbox (the MuJoCo
table) and a grader (the goal check). What it doesn't have is a grader for fuzzy goals. "Put the bowl on the plate
gently" has no check in LIBERO, and RL 2 says the robot would learn only what the check measures.

## Check yourself

1. What three parts make up an RL environment in today's sense? Name them for a task like "book the cheapest flight".
2. In Cursor's Tab example, suppose a rejected suggestion cost −0.5 instead of −0.25 (and an accepted one still earned
   0.75). Above what chance of acceptance would the model start showing suggestions?
3. Why would a lab train several RL specialists and then distil them, instead of one RL run on everything? Say it in
   your own words.

<details><summary>Answers</summary>

1. A task, a sandbox where the model can act, and a grader. For the flight: the request with dates and cities; a
   browser with (often simulated) airline sites; a check that a booking was made for the right dates and that no
   cheaper matching flight existed.
2. Showing is worth p × 0.75 − (1 − p) × 0.5 = 1.25p − 0.5 on average, which beats 0 when p is above 0.4. So the model
   would show a suggestion only when it's at least 40% likely to be accepted.
3. Each specialist can be trained with the rewards, data and settings that suit its area, without one area's training
   pulling against another's. Distillation then gives the student a grade on every token from the right teacher, which
   is much more feedback than one score per answer, and it helps the student keep what each teacher knows.

</details>

## Sources

- Cursor (2026-03-26), "Improving Composer through real-time RL", https://cursor.com/blog/real-time-rl-for-composer
- Cursor (2025-09-12), "Improving Cursor Tab with online RL", https://cursor.com/blog/tab-rl
- Cursor (2025-10-29), "Composer: Building a fast frontier model with RL", https://cursor.com/blog/composer
- Zeff (2025-09-21), "Silicon Valley bets big on 'environments' to train AI agents", TechCrunch,
  https://techcrunch.com/2025/09/21/silicon-valley-bets-big-on-environments-to-train-ai-agents/
- Y Combinator, Lightcone podcast, "The State of Startups in 2026" (2026-09-17), https://www.youtube.com/watch?v=yslXlV2BP_Y
  at about 23:26 (we read third-party transcripts; the captions weren't available).
- Kimi K3 technical report, https://arxiv.org/abs/2607.24653; GLM-5, https://arxiv.org/abs/2602.15763 and
  https://z.ai/blog/glm-5; Nemotron 3 Ultra, https://arxiv.org/abs/2606.15007; DeepSeek-V4,
  https://arxiv.org/abs/2606.19348; MiMo-V2-Flash, https://arxiv.org/abs/2601.02780; Kimi K2,
  https://arxiv.org/abs/2507.20534; Liquid AI LFM2.5-2.6B, https://www.liquid.ai/blog/lfm2-5-2-6b
- Gunjal et al. (2025), "Rubrics as Rewards", https://arxiv.org/abs/2507.17746; Scale AI (2026), "Reward Hacking in
  Rubric-Based Reinforcement Learning", https://arxiv.org/abs/2605.12474
- DAPO, https://arxiv.org/abs/2503.14476; GSPO, https://arxiv.org/abs/2507.18071; CISPO (MiniMax-M1),
  https://arxiv.org/abs/2506.13585; Liu et al. (2025), "Understanding R1-Zero-Like Training", https://arxiv.org/abs/2503.20783;
  TRL `GRPOConfig` v1.17.1, https://github.com/huggingface/trl/blob/v1.17.1/trl/trainer/grpo_config.py
- Lu et al. (2025-10-27), "On-Policy Distillation", Thinking Machines, https://thinkingmachines.ai/blog/on-policy-distillation/
- Lambert (2026-06-16), "Frontier post-training recipe review", Interconnects,
  https://www.interconnects.ai/p/frontier-post-training-recipe-review
- All checked 2026-11-13; quotes are in `library/rl.yaml`.
