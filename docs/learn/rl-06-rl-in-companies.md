# RL 6. RL in companies: build, rent or sell

After this chapter you can decide with three questions whether a task is worth training with RL, say which of three
roles fits a small company, and explain why a large company's own traffic is an advantage others can't copy.
Needs: RL 1 to RL 5. Reading time: 9 min.

After a doctor sees a patient, someone has to turn the visit into billing codes from ICD-10, the standard list of
diagnosis codes. A wrong code costs money and can break billing rules. Ambience Healthcare makes an AI scribe
that writes up doctors' visits, and in 2025 it trained a model to pick these codes. First it built a test set in
which each visit was labelled by a consensus of four or more expert clinicians. Then it trained OpenAI's o3-mini on
the task with OpenAI's reinforcement fine-tuning (RFT), a hosted service that grades every attempt automatically
against the right codes. On the test set, 18 experienced, board-certified physicians scored 0.45, the model before
training 0.39 and the model after training 0.57. Ambience reported this as a 27% relative improvement over the
physicians, cutting coding errors by about a quarter.

Ambience didn't build any RL machinery. It had a grader and a task that comes up with every patient visit, and it
rented the rest.

## Three questions before you train with RL

Our rule of thumb for the whole series comes down to three questions.

1. **Can the outcome be graded automatically?** Ambience could compare codes with the experts' labels. Without a
   grader, RL has nothing to push towards (RL 1), and a weak grader gets hacked (RL 2).
2. **Does the task repeat at high volume?** RL needs many tries, and the training only pays for itself if the
   trained model then does the task many times.
3. **Do cost, speed or privacy matter?** A smaller model trained for one task can be cheaper and faster than a
   frontier model, and it can run where the data has to stay.

If any answer is no, a frontier model with a good harness around it usually wins.

## Small and mid-size companies: use, rent or sell

For most small companies, RL is something they buy inside a model, rent as a service, or sell to those who train. Few
build it from scratch.

| Role | What it looks like | Examples |
|---|---|---|
| use | build on models that labs already trained with RL; improve your own harness with a score-and-revise loop, without touching weights (RL 7, level 1) | most startups today |
| rent | train a narrow model on hosted RL when you have a grader and volume | Ambience (above); Harvey (legal) and Thomson Reuters (CoCounsel, legal) with OpenAI's RFT |
| sell | build environments and graders for a domain you know, and sell them to labs or other companies | HUD; more than a dozen YC companies (RL 5) |

**Renting.** OpenAI announced RFT as a research preview in December 2024. Harvey, which makes AI for law firms,
reported a 20% higher F1 score after RFT (0.563 before, 0.6765 after). Services come and go, though. OpenAI's RFT page
now says it is winding down its fine-tuning platform: it's closed to new users, and existing customers can start
training jobs until 6 January 2027. Thinking Machines launched Tinker, an API for fine-tuning open models, in October
2025, and a year later it had added over 20 models to the 14 it launched with. Together AI launched Together
Post-Training in October 2026, for training a model "from environment rewards via RL and supervision data via SFT".

**Selling.** HUD, a YC company, says over 2,500 environments have been created on its platform (its own figure, 2026).
Prime Intellect runs an open Environments Hub (launched August 2025) where anyone can publish one.

## The reality check

RL is expensive and can backfire. In September 2025 TensorZero compared OpenAI's RFT with ordinary supervised
fine-tuning (SFT) on the same data. RFT cost 100 to 700 times more; on a data-extraction task, $65.07 against $0.09.
It improved an agentic coding task where SFT failed, but on a customer-service task SFT did better and RFT made the
model worse. The comparison has limits: RFT ran on o4-mini and SFT on GPT-4.1 mini, and the training sets were tiny.
Still, it breaks a belief that's easy to hold, that RL makes a model better at whatever you point it at. RL improves
the score. When the score doesn't capture the job, as is easy with something as open-ended as customer service, it
can make the job worse.

## Large companies: their traffic is the reward

Large companies have what RL is hungry for: millions of repeated decisions, each with an outcome they can measure.

Lyft's driver matching is a worked case. The simple rule sends the nearest free driver to each rider. But every match
also decides where drivers will be later, and a driver sent away from a busy area can't take the next rider there.
Lyft's new matching uses what its paper calls "a novel online reinforcement learning approach that estimates the
future earnings of drivers in real time", and it uses those estimates to find better matches. Each estimate is a
value, RL 3's score sheet.

With made-up numbers, it works like this. One rider needs a pickup. Driver A is 2 minutes away, waiting downtown, where
the value table expects her to earn $25 over the next hour. Driver B is 4 minutes away at the edge of town, where it
expects $10. Both would end the trip in the same place. The nearest-driver rule sends A. A value-aware match sends B,
because taking B off his spot gives up $10 of expected earnings and taking A off hers gives up $25, and A stays free
for the next rider downtown. The real system also weighs pickup time and much else.

Lyft tested this in 2021 with "switchback" experiments, which switch whole markets between the old and new system in
turns, and rolled it out globally that year. Its paper says the change let drivers serve millions of additional
riders each year and brought more than $30 million a year in incremental revenue.

| Where in the company | The decision RL makes | Example |
|---|---|---|
| feeds and recommendations | what to show next | YouTube's REINFORCE recommender (a 0.85% gain in viewing time in one test) |
| marketplace and dispatch | which driver gets which rider | Lyft (above) |
| hardware design | where to place blocks on a chip | Google's chip placement (published in *Nature* in 2021; its claims were disputed, and *Nature* added an addendum in 2024) |
| engineering | coding agents trained in sandboxes of real code | Cursor (RL 5) |
| legal | agents tuned on graded legal work | Thomson Reuters, Harvey |
| robots | grasping, folding, assembly from real practice | π*0.6 (RL 7) |

You'll often see DeepMind's data-centre cooling, with "up to 40 percent" less energy used for cooling (2016), listed as
an RL success. DeepMind's own posts describe neural networks that predict and recommend, and never use the word
reinforcement, so we leave it out.

The advantage compounds. More users produce more reward signal, which makes a better product, which brings more users.
Cursor's Tab model answers over 400 million requests a day (RL 5), and a smaller rival can't buy that signal.

## The wrong belief: RL makes a model better at whatever you train it on

TensorZero's customer-service result breaks it. RL makes a model better at the score, and the score is only as good
as the grader. Before renting RL, check that the grader measures the job.

## What this means for our project

In this chapter's terms, groups that ran RL on LIBERO (RL 7) are in the build role, with open tools. Our project so
far is in the use role: we run π0.5 as released. The three questions fit LIBERO well, as our reading. Its goal check
grades automatically, the simulator can run as many episodes as GPU time allows, and the cost is that GPU time.

## Check yourself

1. What are the three questions? Answer them for a company that wants RL to write marketing emails, graded by how
   many people click.
2. In the Lyft example, suppose Driver B's spot were worth $30 an hour instead of $10. Which driver would a
   value-aware match send, and why?
3. Why is a large company's own traffic an advantage that a smaller rival can't simply copy? Say it in your own words.

<details><summary>Answers</summary>

1. Can it be graded automatically, does it repeat at high volume, and do cost, speed or privacy matter? For the
   emails: clicks can be counted, but they come slowly, are noisy and can be gamed by clickbait (RL 2), so the grader
   is weak. Volume may be high. Cost may matter. With a weak grader, a frontier model with a good harness is the safer
   start.
2. Driver A. Taking A off her spot now gives up $25 and taking B off his gives up $30, so sending A costs the system
   less, and A is also closer.
3. Every user action is a graded try: kept or not, clicked or not, finished or not. A company with millions of users
   collects far more reward signal every day than a rival could pay to create, and each better model brings more
   users and so more signal.

</details>

## Sources

- Ambience Healthcare (2025-05-27), "Ambience Healthcare's AI platform surpasses clinician performance by 27% in
  medical coding",
  https://www.ambiencehealthcare.com/blog/ambience-healthcare-s-ai-platform-surpasses-clinician-performance-by-27-in-medical-coding-powered-by-new-openai-breakthrough;
  raw scores from OpenAI's RFT use-case guide, https://developers.openai.com/api/docs/guides/rft-use-cases (also
  Harvey, Thomson Reuters, and the wind-down notice).
- TensorZero (2025-09-25), "Is OpenAI's Reinforcement Fine-Tuning (RFT) Worth It?",
  https://www.tensorzero.com/blog/is-openai-reinforcement-fine-tuning-rft-worth-it/
- Thinking Machines (2025-10-01), "Announcing Tinker", https://thinkingmachines.ai/blog/announcing-tinker/; "One Year
  of Tinker" (2026-10-15), https://thinkingmachines.ai/news/one-year-of-tinker/
- Together AI (2026-10-19), "Together Post-Training", https://www.together.ai/blog/together-post-training
- HUD (2026), Series A announcement, https://www.hud.ai/blog/announcing-16m-series-a; Prime Intellect (2025-08-27),
  Environments Hub, https://www.primeintellect.ai/blog/environments
- Azagirre et al. (2024), "A Better Match for Drivers and Riders: Reinforcement Learning at Lyft", *INFORMS Journal on
  Applied Analytics* 54(1), https://arxiv.org/abs/2310.13810
- Chen et al. (2019), "Top-K Off-Policy Correction for a REINFORCE Recommender System", WSDM,
  https://arxiv.org/abs/1812.02353
- Mirhoseini et al. (2021), "A graph placement methodology for fast chip design", *Nature* 594,
  https://www.nature.com/articles/s41586-021-03544-w; Google DeepMind (2024-09-26), "How AlphaChip transformed computer
  chip design".
- DeepMind (2016-07-20), "DeepMind AI reduces Google data centre cooling bill by 40%",
  https://deepmind.google/discover/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/
- All checked 2026-11-13; quotes are in `library/rl.yaml`.
