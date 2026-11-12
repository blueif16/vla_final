# What we're studying

Shiran chose this direction on 2026-11-11, and [chapter 6](docs/learn/06-where-we-stand.md) is where we record what's
decided. The question, the experiments and the steps below are our first draft, and Jingyi hasn't reviewed them yet.

## The question

When π0.5 does a household task, what is it actually going by: the words we give it, what each of its cameras shows,
or the layout it remembers from training? And what does that mean for a robot working in a real home?

## Why it matters now

Robots you talk to are starting to be sold for homes. 1X takes orders for its NEO home robot at $20,000, or $499 a
month, with US deliveries starting in 2026. Its order page names laundry and getting the door as example chores and
says owners can "speak naturally to NEO". For tasks NEO can't do yet, a 1X expert can supervise it remotely. The
models behind robots like this are VLAs. In April 2026 Physical Intelligence, the company that makes π0.5, released
π0.7. Its paper says the model "can follow diverse language instructions in unseen environments" and can fold laundry
on a robot that never saw the task before.

Lab studies of the earlier open models keep finding that the words matter less than you'd think. With the instruction
erased, π0.5 still succeeds more than half the time on three of LIBERO's four suites (LIBERO-CF). Zhang and Bisk call
the failure "instruction blindness" and trace it to fine-tuning on a small amount of robot data. Jang et al. gave six
trained policies an empty instruction, and the robot started moving in every episode. So what these robots actually
go by is still an open question, just as they are being sold for homes. A robot that ignores your words and does the
job it knows best might turn on the stove when you asked it to move a bowl. Our experiments put that question in a
form anyone can watch.

## Why this question

π0.5 succeeds about 98% of the time on LIBERO's kitchen tasks (98.0% on LIBERO-Goal, in openpi's own evaluation).
That number doesn't say what the robot looked at to get there. In three of LIBERO's four suites, almost every task
starts from its own arrangement of objects, so the picture alone gives away which task it is
([chapter 3](docs/learn/03-libero.md)). A robot could score 98% without reading a word.

Other groups have measured part of this. With the instruction removed, the same checkpoint still succeeds 68.2% of the
time on LIBERO-Spatial. On LIBERO-Goal, where all ten tasks start from the same table, it falls to 10.2% (LIBERO-CF,
Table I). We'll repeat that test first, partly to check our own setup against a known number.

Then we widen it. The words are one thing the robot might go by, and the cameras and the remembered layout are two
more. Each experiment below changes one of them the way a real home would. Someone phrases the request their own way,
a camera gets bumped, or the plate sits somewhere new.

Each experiment should be one that anyone can follow. You guess what the robot will do, then watch the videos and see
the number. Some experiments will repeat published results, which is fine as long as the answer isn't obvious
beforehand.

## Three stages

| Stage | Where | Status |
|---|---|---|
| 1 | LIBERO's kitchen scenes, on our desktop GPU | doing now |
| 2 | laundry folding in simulation (the LeHome Challenge), on a rented GPU | next, if a trial run works |
| 3 | a real SO-101 arm folding a towel | parked |

## Stage 1: the LIBERO kitchen

The model is `pi05_libero`, which is π0.5 fine-tuned on LIBERO by Physical Intelligence. At each step it gets two
camera images and the instruction, and nothing else ([chapter 2](docs/learn/02-pi0-and-pi05.md)). It sends back 10
actions, and the robot runs the first 5 before asking again.

### First, watch it work

Before we change anything, we run the model as published and look at what it does. We record videos of each suite,
save the two images it receives and the actions it returns during one episode, and check our success rates against
openpi's 98.8 on LIBERO-Spatial and 98.0 on LIBERO-Goal. If ours are far off, something in our setup is wrong, and we
fix that before running any experiment.

### The experiments

Each experiment changes one thing. It gives a success rate next to the normal run, videos side by side, and a short
write-up that asks the reader to guess first.

| # | Guess first | What we change | What it stands for in a real home | Published result to compare |
|---|---|---|---|---|
| 1 | If we erase the instruction, will the robot still put the bowl on the plate? | the instruction: the original, a blank one, or another task's sentence for the same table, on LIBERO-Goal and LIBERO-Spatial | a robot that does its usual job whatever you say | LIBERO-CF Table I: 10.2 (Goal) and 68.2 (Spatial) with the instruction removed |
| 2 | Does it still work if you say it your own way? | a reworded instruction, the same request in Chinese, a typo | people don't talk like the training data | LIBERO-Plus reports that models barely react to rewording (from its abstract) |
| 3 | Which camera does it need? | black out the wrist camera, or the table camera | a camera that gets covered or breaks | none found |
| 4 | How far can the table camera move before the robot gets lost? | shift and turn the table camera in small steps | someone bumps the camera | LIBERO-Plus found camera angle hurts most (from its abstract) |
| 5 | If we move the plate, does the bowl go to the plate or to where the plate used to be? | the starting position of one object | no kitchen is set up like the training data | LIBERO-PRO: models above 90% fall to 0.0% when objects, positions or instructions change (from its abstract) |
| 6 | What if it thinks less, or looks again less often? | refinement steps: 5, 2 or 1 instead of 10; actions run per chunk: 1 or 10 instead of 5 | a cheaper, slower computer; reacting when something moves | none found |

In experiment 1 we'll also record which task the robot did when it didn't do the one asked. A 2026 paper (Jang et
al.) found that policies on LIBERO-Goal often finish a task nobody asked for when the instruction is empty. We'll
count which tasks π0.5 does, including how often it turns on the stove.

LIBERO-Spatial gives experiment 1 a sharper test. Two of its tasks, "the bowl on the stove" and "the bowl on the
wooden cabinet", start from the same table, with identical black bowls in both places ([chapter 3](docs/learn/03-libero.md)).
Our guess is that with the instruction erased, the robot keeps doing well on the other eight tasks and gets these two
right only about half the time, because the picture can't tell it which bowl to take.

### Steps

1. **Run it.** Serve `pi05_libero` on the desktop and connect openpi's LIBERO client. This is done when one episode
   plays and saves a video. The part we expect to need work is drawing the camera images inside WSL, where MuJoCo's
   GPU rendering may not work. The fallback renders on the CPU and is slower. (Our guess, not tested yet.)
2. **Reproduce.** Run the original instructions on LIBERO-Goal and LIBERO-Spatial, 500 episodes each. This is done
   when our success rates sit near 98.0 and 98.8 and we know how long one episode takes, which tells us what every
   later experiment costs.
3. **Look inside one episode.** Save the two images, the sentence and the 10-action chunks from one run. This is done
   when we can show what goes in and what comes out on our own run, the way chapter 1 draws it.
4. **Build one experiment runner.** One command runs a number of episodes under a named condition (an instruction, a
   blacked-out camera, a camera pose, a moved object, the refinement steps, the actions per chunk). It saves the
   success rate, a video, and on LIBERO-Goal which task got done. This is done when experiment 1 runs from it.
5. **Experiment 1, checked against LIBERO-CF.** This is done when our blank-instruction numbers sit next to their 10.2
   and 68.2, with a reason if they differ.
6. **Experiments 2 to 6.**
7. **Write each one up**, with the guess, the videos, the number and what it means in a real home. This is done when
   each experiment has its own page.

How many episodes each experiment needs is our own arithmetic. openpi's evaluation runs 50 episodes per task, so 500
per suite. With 500 episodes, a success rate near 50% is known to within about ±4.4 points (95% confidence). With 50
episodes on one task, it's about ±14. So a 10-point gap between two whole suites is real, and a 10-point gap on one
task may not be. We'll choose the count for each experiment once step 2 tells us what an episode costs.

## Stage 2: laundry folding (next)

Folding laundry is a real household chore, and in 2026 it became possible to study it in simulation with our model
family. The LeHome Challenge, held at the ICRA 2026 robotics conference, released a simulator in which two SO-101 arms
fold four kinds of garment: long-sleeve tops, T-shirts, long pants and shorts. The team that came first published its
policy. It's built on π0.5 with openpi, and it folds 79.63% of garments in the simulator.

The simulator runs on Isaac Sim, which needs an RTX-class GPU with at least 16 GB of memory, more than our desktop
has. So stage 2 starts with a trial on a rented 48 GB card, an L40S or RTX 6000 Ada, which costs about $0.74 to $1.09
an hour on RunPod (checked November 2026). We install the simulator and the winning policy and run their evaluation.
The trial passes if we see their result, 80% or more on garments the policy trained on, with all three cameras
rendering. That isn't certain, because a forum post reports cameras failing on rented machines with the same simulator
version. If the trial fails, we finish with stage 1 and write down what went wrong.

If it passes, we ask the same question on laundry.
- **Tell it the wrong garment.** According to the winner's blog, the policy's only instruction is a garment-type
  label that it works out at the start of each episode. What happens if we tell it "shorts" while it's holding a
  shirt? (We haven't read the code yet.)
- **A garment it has never seen**, in a new colour or pattern.
- **Bump one of its three cameras**, or black one out.
- **Start the garment in a messier pose**, if the simulator allows it. (Not checked.)

## Stage 3: a real arm (parked)

A low-cost SO-101 arm folding a real towel would be the most real version. Community towel-folding models built on
π0.5 and SmolVLA already exist. We've parked it because it needs the arms, our own recorded demonstrations, and a
rented GPU to fine-tune π0.5 (LoRA fine-tuning needs more than 22.5 GB). We'll come back to it after stage 2.

## What we need to know

| What | Why we need it | Where we learn it |
|---|---|---|
| What a VLA takes in and sends out, and what an action chunk is | to read any of the experiments | [chapter 1](docs/learn/01-what-a-vla-is.md) |
| What `pi05_libero` sees: two images and a sentence, no joint readings; 10 actions predicted, 5 run | to design experiments 3 and 6 | [chapter 2](docs/learn/02-pi0-and-pi05.md) |
| The four LIBERO suites, and why LIBERO-Goal is the one where the words matter | to choose suites for experiments 1 and 2 | [chapter 3](docs/learn/03-libero.md) |
| How to measure reading: success, grounding rate, faithful and biased success | experiment 1 | [chapter 4](docs/learn/04-the-grounding-question.md) |
| What other groups found, with their numbers | to compare ours | [chapter 5](docs/learn/05-what-others-found.md) |
| How to run openpi: the policy server, the LIBERO client, rendering in MuJoCo | steps 1 and 2 | to write |
| LIBERO's insides: starting states, how each task's goal is checked, camera settings | experiments 1, 4 and 5 | to write |
| How π0.5 refines its actions and when the robot asks again, in openpi's code | experiment 6 | chapter 1's figures, plus a page to write |
| How many episodes a comparison needs | every experiment | to write |
| Isaac Sim, LeRobot, the SO-101 arm and the winning laundry policy | stage 2 | to write later |

## Where we are now

- We wrote six chapters that take a newcomer from what a VLA is to the choice we faced. Chapter 1 is also a web
  page, with diagrams, talk clips and side notes.
- We checked our submitted plan against published work. The blank-instruction and other-task tests for our exact
  checkpoint are already published (LIBERO-CF), and rewording has been tested at benchmark scale (LIBERO-PRO,
  LIBERO-Plus). Many more 2026 papers ask a version of the question ([chapter 5](docs/learn/05-what-others-found.md),
  [`library/papers.yaml`](library/papers.yaml)). So we kept the question, widened it from the words to everything the
  robot goes by, and tied each test to something that happens in a real home.
- We compared six places to run experiments ([`library/environments.yaml`](library/environments.yaml)) and checked our
  compute. Our desktop GPU is enough for stage 1, and stage 2 needs a rented card.
- Stage 1 runs on our desktop. `pi05_libero` serves on the GPU, and LIBERO runs with openpi's exact versions
  ([`stage1/README.md`](stage1/README.md)). Step 1 is done.
- We have a first answer from experiment 1, on the two LIBERO-Spatial tasks that share a table
  ([`stage1/results/exp1-shared-table.md`](stage1/results/exp1-shared-table.md)). With its own sentence the robot
  took the right bowl 19 times out of 20. With the sentence erased it succeeded 8 times out of 40, and it sometimes put
  the cookie box on the plate instead. We had guessed about half, so our guess was wrong. An episode takes 12 to 24
  seconds, so the full reproduction in step 2 should take under 2 hours per suite.

## Sources

All checked 2026-11-11 unless noted. Numbers are copied from [`library/`](library/).
- openpi, LIBERO results for `pi05_libero` and the evaluation script, https://github.com/Physical-Intelligence/openpi
- Liu et al. (2023), LIBERO, https://arxiv.org/abs/2306.03310
- Fang et al. (2026), When Vision Overrides Language (LIBERO-CF), https://arxiv.org/abs/2602.17659
- Zhou et al. (2025), LIBERO-PRO, https://arxiv.org/abs/2510.03827
- Fei et al. (2025), LIBERO-Plus, https://arxiv.org/abs/2510.13626
- Jang et al. (2026), VLA Policies Do Not Know When Not to Act, https://arxiv.org/abs/2610.41609
- Zhang and Bisk (2026), Flatness Preserves Instruction Following in Vision-Language-Action Models,
  https://arxiv.org/abs/2606.23641
- Physical Intelligence (2026), π0.7: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities,
  https://arxiv.org/abs/2604.15483
- 1X, NEO order page, https://www.1x.tech/order
- LeHome Challenge 2026, https://github.com/lehome-official/lehome-challenge
- The winning LeHome policy: https://huggingface.co/IliaLarchenko/lehome_sim, its code
  https://github.com/IliaLarchenko/lehome_solution, report https://arxiv.org/abs/2606.27163 and blog
  https://ilialarchenko.com/projects/lehome2026
- Isaac Sim 5.1 requirements, https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/requirements.html
- RunPod pricing, https://www.runpod.io/pricing (checked November 2026)
