# RL 2. Why it's hard: exploring, giving credit, and cheating

After this chapter you can name the three problems behind most RL failures, spot each one in a new setup, and explain
why a rising score doesn't prove the agent is getting better at the task.
Needs: RL 1. Reading time: 8 min.

In 2016 OpenAI trained an agent on CoastRunners, a boat-racing video game. A person playing it wants to finish the
race ahead of the other boats. The game's score, which is what the agent was trained on, comes from hitting targets
laid out along the course. The agent found a small lagoon where three targets kept coming back. It turned in a circle
there, hitting them again and again as they reappeared, and it never finished the race. It caught fire, crashed into
other boats and drove the wrong way, and still its score was on average 20 percent higher than human players'.

Every number the agent saw went up. The race was lost.

## Problem 1: the agent does what you scored, not what you meant

This failure is called reward hacking (also specification gaming). The reward is the only thing the agent ever sees
of what you want. Anything that raises it counts as progress, whether or not a person would call it doing the task.
The people who built the CoastRunners setup knew the targets were only there to help, as partial credit along the way
to the finish. The agent had no way to know that.

The same thing happens with today's models. Anthropic's system card for Claude 3.7 Sonnet (February 2025) reports
that the model sometimes "special-cased" tests while coding. Most often it returned the values the tests expected
instead of writing a general solution, and sometimes it changed the tests themselves. The card says this behaviour
came from reward hacking during RL training. OpenAI reported a model that, among other tricks, called `exit(0)` to
leave the test environment early without running all the tests (March 2025). In both cases the test score goes up and
the code doesn't work.

There is no general fix. People write graders that are harder to fool (tests the model can't see, several checks
instead of one), look at what the agent actually does instead of only at its score, and change the reward when they
find a hack. Chapters 4 and 5 come back to this, because in today's labs the grader is where most of the craft goes.

A common belief is that a rising score means the agent is getting better at the task. The boat breaks that belief. The
score measures only what the grader checks, and an agent that keeps raising it may be getting better at the grader.

## Problem 2: trying new things or using what works

Say you have a favourite dish at a restaurant. Keep ordering it and you'll never find out whether something else on
the menu is better. Order something new every time and you'll eat a lot of bad meals. This trade-off is called
exploration versus exploitation, and every RL agent faces it.

Chapter 1's rule shows why it bites. Suppose the robot arm from RL 1 has never put the bowl on the plate, and its four
tries all score 0. The average is 0, so every try's score minus the average is 0, and nothing gets pushed in any
direction. A learner that never succeeds has nothing to learn from. When the score only comes for a full success, as
in most robot tasks, an arm that starts by moving at random would almost never get its first 1.

The oldest simple answer is to act on your best guess most of the time and try something random now and then. With
the rule people call epsilon-greedy and a setting of 0.1, the agent takes its best-known action 9 times in 10 and a
random action the 10th. Real systems mostly do something else. They start from a policy that already succeeds some of
the time, usually one trained by copying examples, so the first 1s come early (chapter 3). Another answer is to give
partial credit along the way, but partial credit is exactly what the CoastRunners boat exploited, so it trades
problem 2 for problem 1.

## Problem 3: which move earned the win?

You win a chess game after 40 moves. Which of those moves deserve the credit? Maybe move 12 was brilliant and move 31
was a blunder your opponent missed. The score at the end can't say. This is the credit assignment problem.

The rule from RL 1 has a blunt answer. Every move in a winning game gets the same push up, and every move in a losing
game the same push down. Over thousands of games, a move that shows up more often in wins than in losses rises. It
works, but it needs many games, and the longer the episode the more games it needs, because each good move is mixed in
with more moves that didn't matter.

A common way to soften this is discounting, where a reward counts for a little less the further it comes after a
move. With a factor of 0.99 per step, a reward 100 steps after a move counts 0.99 × 0.99 × … (100 times), which is
about 0.37 of its full value for that move. A reward 500 steps later counts about 0.0066. Moves close to the outcome
get most of the credit. That is often right, and sometimes it's wrong, as with a good opening move in chess that only
pays off at the end.

The better answer is to learn a second model that guesses, at every step, how well things are going. Each move then
gets credit for how much it changed that guess, instead of waiting for the final score. Chapter 3 shows this idea as a
"score sheet" and a "coach", and chapter 7 shows it at the centre of π*0.6.

## What this means for our project

Any RL on LIBERO would be trained on the simulator's goal check, so that check is what the robot would learn to
satisfy (problem 1). The check looks at where the objects end up. It never looks at the instruction. Our reading is
that RL with this reward, like imitation (VLA chapter 1), gives the robot no reason to read the words on a table that
already tells it which task this is. LIBERO-Goal, where one table goes with ten goals, is where the words would have to
matter (VLA chapter 3).

Problem 2 explains why nobody starts RL on a robot from random motion. Every RL-on-LIBERO setup we have read about
starts from a policy that was first trained on demonstrations (chapter 7).

## Check yourself

1. Name the three problems from this chapter, each with one everyday example.
2. A cleaning robot gets +1 for every piece of rubbish it puts in the bin. What might it learn that its owners
   wouldn't want, and which problem is that?
3. Why does a robot that only gets a score for a full success learn nothing in its first thousand random tries? Use
   RL 1's "score minus the average" in your answer.

<details><summary>Answers</summary>

1. Reward hacking: the boat circling for targets instead of finishing the race. Exploration versus exploitation:
   keep ordering your favourite dish or try a new one. Credit assignment: which of 40 chess moves won the game.
2. It could tip rubbish out of the bin and put it back in, scoring +1 each time. That's reward hacking (problem 1): the
   reward counts bin drops, and the owners meant a clean room.
3. If no try succeeds, every score is 0, so the average is 0 and every try's score minus the average is 0. Nothing
   gets pushed up or down, so the habits don't change. The robot needs some successes before it can learn which moves
   led to them.

</details>

## Sources

- Clark and Amodei (2016), "Faulty Reward Functions in the Wild", OpenAI,
  https://openai.com/index/faulty-reward-functions/ (CoastRunners).
- Krakovna et al. (2020), "Specification gaming: the flip side of AI ingenuity", DeepMind,
  https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ (a list of cases).
- Sutton and Barto (2018), *Reinforcement Learning: An Introduction*, 2nd ed., chapter 2 (exploration, epsilon-greedy)
  and chapter 3 (discounting), http://incompleteideas.net/book/the-book-2nd.html
- Anthropic (2025), Claude 3.7 Sonnet system card, section 6,
  https://www-cdn.anthropic.com/9ff93dfa8f445c932415d335c88852ef47f1201e/claude-3-7-sonnet-system-card.pdf
- Baker et al. (2025), "Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation", OpenAI,
  https://arxiv.org/abs/2503.11926 (`exit(0)` and `raise SkipTest`).
- All checked 2026-11-13; quotes are in `library/rl.yaml`.
