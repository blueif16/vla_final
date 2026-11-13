# RL 1. Learning from a score: what reinforcement learning is

After this chapter you can explain reinforcement learning with five words and one loop, work out from a handful of
scores which tries a learner should repeat more often, and say why a learner that is only given a score can end up
better than the people it learned from.
Needs: nothing. Chapter 1 of the VLA series helps with the robot example. Reading time: 8 min.
Web version, with predict-first questions, an explorable and talk clips (15–20 min):
https://blueif16.github.io/vla_final/learn/rl-01-learning-from-a-score.html

Go back to the robot arm from the first VLA chapter, standing at a table with a black bowl and a plate. This time no
one steers the arm through the task, and no one records what a person would do. The simulator checks one thing when
each try ends: is the bowl on the plate? It answers 1 for yes and 0 for no. Suppose the arm already reaches for the
bowl now and then, and lands it on the plate in some of its tries but not most. Reinforcement learning (RL) is the rule
that makes the lucky tries a little more likely next time, and then again after the next batch of tries, until the
bowl ends up on the plate most of the time.

Nobody ever tells the arm which move was right. It only ever learns how well a whole try went.

## Five words and a loop

The field describes every problem with the same five words.

| Word | What it means | In the bowl example |
|---|---|---|
| agent | the learner | the network that moves the arm |
| environment | the world the agent acts in | the simulated table, its objects and their physics |
| action | what the agent does at one moment | seven numbers that move the hand and the gripper (VLA chapter 1) |
| reward | the score the environment hands back | 1 if the bowl is on the plate when the try ends, otherwise 0 |
| policy | the agent's current habits: "in a situation like this, I tend to do that" | the VLA itself |

These words fit together as a loop. The agent looks at the situation, which for the arm is a camera picture. It acts,
the environment changes, and sometimes a reward comes back. One try from start to finish is an episode. After a batch
of episodes the policy is adjusted towards whatever scored higher, and the loop starts again. A game-playing agent
might go round this loop millions of times.

```
        ┌──────────── look (camera picture) ─────────────┐
        │                                                 │
     agent ──── act (move the arm) ────> environment ─────┤
   (policy)                                               │
        ^                                                 │
        └── adjust the habits <── reward (1 or 0) <───────┘
```

## How "do more of what scored well" works

A policy doesn't pick one fixed action. It gives every possible action a chance of being picked, and learning
changes those chances. Here is the smallest version, with numbers.

Say that at some point in the task the policy reaches to the left half the time and to the right half the time. The
arm makes four tries, and they score 1, 0, 0 and 1. The average is 0.5. For each try, take its score minus the
average: +0.5, −0.5, −0.5 and +0.5. Those differences say how hard to push. The two tries that did better than
average get the actions they took made a bit more likely, and the two that did worse get theirs made a bit less
likely. If both successful tries reached left, "reach left" might now come up 55 times in 100 instead of 50.

In one line:

> change in an action's chance ∝ (score of the try it was in − the average score)

People call the difference in the brackets the advantage, because it measures how much better than usual a try went.
Each change is kept small, so one lucky try can't rewrite the habits. Ronald Williams wrote down this rule in 1992,
and his algorithm, REINFORCE, still sits under most of the methods in this series.

Taking away the average matters more than it looks. In a game where every try earns some points, pushing up every
action by its raw score would make every habit stronger at once. With the average taken off, only the tries that beat
the usual result get pushed up.

## Learning from a score versus learning from examples

Most machine learning is supervised. Every training example comes with the right answer, and the model is corrected
towards it. A VLA learns this way when it copies demonstrations (behaviour cloning, VLA chapter 1). It's like studying
with the answer key open.

RL is like doing practice problems where the teacher only tells you your grade. A grade says how well you did but not
what you should have written, so the feedback is weaker and the learner needs many more tries. In return, nothing
caps it at the level of its teacher. A learner that copies people can at best match them. A learner pushed towards a
higher score can find moves no person showed it. AlphaZero learned chess, shogi and Go only by playing against itself,
starting from random play, and it beat a world-champion program in each of the three (chapter 3).

A common belief is that a reward works like a label, telling the model which move was right. It doesn't. In the bowl
example the score comes once, after up to a few hundred steps, and it never says which of those steps helped. Sorting
that out is one of the three things that make RL hard, and chapter 2 is about them.

## What this means for our project

`pi05_libero` learned only by imitation, from the 50 recorded demonstrations that come with each LIBERO task (VLA
chapter 3). But LIBERO already has the other half of an RL setup. The goal check that decides whether an episode
counts as a success is exactly the 1-or-0 score in this chapter's example, so RL on LIBERO wouldn't need anyone to
write a new grader. Chapter 7 shows groups that have done this, and whether we try it is open (VLA chapter 6 lists
what's decided).

## Check yourself

1. Name the agent, environment, action, reward and policy for a model that learns to play chess.
2. Four tries score 2, 4, 6 and 8 points. Which tries get their actions pushed up, and how do the pushes compare?
3. Why can a learner that is only given a score end up better than the people who made its training data, when a
   learner that copies them can't? Say it in your own words.
4. In the bowl example, what does the reward tell the arm? (a) Which of its moves was the right one at each step.
   (b) How well the whole try went, as one number at the end. (c) What a person would have done in the same spot.
5. Four tries score 3, 3, 3 and 3 points. What does the rule do to the actions in them? (a) It pushes them all up,
   since every try earned points. (b) It pushes up the first try most, because it came first. (c) Nothing.
6. A chat model is trained with RL, using the same five words. What is one action? (a) The next word it writes.
   (b) One whole answer. (c) The grade the answer gets.

<details><summary>Answers</summary>

1. The agent is the chess program. The environment is the board and the opponent. An action is one move. The reward
   is the result at the end (for example +1 for a win, 0 for a draw, −1 for a loss). The policy is the program's
   current habit of which move it tends to play in each position.
2. The average is 5, so the pushes are −3, −1, +1 and +3. The tries that scored 6 and 8 get their actions pushed up,
   the one that scored 8 three times as hard as the one that scored 6. The tries that scored 2 and 4 get pushed down.
3. Copying is corrected towards what the people did, so the best it can do is match them. RL is pushed towards a
   higher score, and any move that raises the score gets reinforced, whether or not a person ever made it.
4. (b). Not (a): that's the wrong belief this chapter names; the score never says which step helped. Not (c): that's
   what a demonstration gives, and no one shows this arm anything.
5. (c). Every try's score minus the average is 0, so nothing is pushed. (a) would be pushing by the raw score, and the
   order of tries in (b) doesn't matter to the rule.
6. (a). Each word, or piece of a word, is one action. A whole answer (b) is one try, an episode, and the grade (c) is
   the reward.

</details>

## Sources

- Sutton and Barto (2018), *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press. Free online:
  http://incompleteideas.net/book/the-book-2nd.html (chapter 1 for the five words; chapter 13 for policy gradients
  and the baseline).
- Williams (1992), "Simple statistical gradient-following algorithms for connectionist reinforcement learning",
  *Machine Learning* 8, 229–256, https://doi.org/10.1007/BF00992696 (REINFORCE, with a baseline subtracted from the
  reward).
- Silver et al. (2017), "Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm",
  https://arxiv.org/abs/1712.01815 (AlphaZero).
- LIBERO and its success check: VLA chapter 3 and its sources.
