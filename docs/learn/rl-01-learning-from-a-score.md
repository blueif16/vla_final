# RL 1. Learning from a score: what reinforcement learning is

After this chapter you can explain reinforcement learning with five words and one loop, work out from a handful of
scores which tries a learner should repeat more often, and say why a learner that is only given a score can end up
better than the people it learned from.
Needs: nothing. Reading time: 10 min.
Web version, with pictures, videos of DQN, AlphaGo and hide-and-seek, an explorable and a learner we trained (15–20 min):
https://blueif16.github.io/vla_final/learn/rl-01-learning-from-a-score.html

Picture a robot arm at a table with a black bowl and a plate on it. No one steers the arm through the task, and no
one shows it what a person would do. The simulator checks one thing when
each try ends: is the bowl on the plate? It answers 1 for yes and 0 for no. Suppose the arm already reaches for the
bowl now and then, and lands it on the plate in some of its tries but not most. Reinforcement learning (RL) is the rule
that makes the lucky tries a little more likely next time, and then again after the next batch of tries, until the
bowl ends up on the plate most of the time.

Nobody ever tells the arm which move was right. It only ever learns how well a whole try went.

The idea is older than computers. In 1898 the psychologist Edward Thorndike shut cats in small cages, now known as
puzzle boxes. A cat could get out and reach its reward, such as food, only by working a lever or a button, and at first
it hit on that by trying things at random. Over repeated trials it got out faster and faster. In 1911 Thorndike called
the rule behind this the law of effect: "Of several responses made to the same situation, those which are accompanied
or closely followed by satisfaction to the animal will, other things being equal, be more firmly connected with the
situation." Reinforcement learning gives the same rule to a computer.

## A second example: a pole on a cart

The second example is much smaller. It's called CartPole, and it comes from a 1983 paper by Andrew Barto, Richard
Sutton and Charles Anderson. A pole stands on a cart, fixed at the bottom by a hinge, and the cart runs along a short
track. At every step the learner moves the cart left or right. When the pole leans to the right, moving the cart right
brings it back under the pole, and moving it left lets the pole fall further.

The score is 1 point for every step the pole stays up. A try ends when the pole leans more than 12 degrees, when the
cart runs off the end of the track, or after 500 steps. So a try's score is how many steps it lasted, and 500 is the
most it can get. The simulation runs 50 steps a second, which makes 500 steps ten seconds of balancing.

We ran CartPole in Gymnasium, a free library of test problems for RL, with a learner that starts out moving left or
right at random, half the time each. Its first four tries scored 31, 66, 22 and 47, so all four were over in less than
a second and a half (the web version shows them). Nobody tells this learner which move was right either. All it gets
after each try is the score.

## Five words and a loop

The field describes every problem with the same five words: the agent is the learner, the environment is the world
it acts in, an action is what the agent does at one moment, the reward is the score the environment hands back, and
the policy is the agent's current habits ("in a situation like this, I tend to do that"). Here they are for both
examples.

| Word | The arm | CartPole |
|---|---|---|
| agent | the network that moves the arm | the program that picks left or right |
| environment | the simulated table, its objects and their physics | the cart, the pole, the track and their physics |
| action | one small move of the hand or the gripper | moving the cart left or right |
| reward | 1 if the bowl is on the plate when the try ends, otherwise 0 | 1 point for every step the pole stays up |
| policy | how likely it is to make each move, in each situation | how likely it is to move left, for each position of the cart and the pole |

The five words are the vocabulary of the field's textbook, *Reinforcement Learning: An Introduction*, by Richard Sutton
and Andrew Barto. In March 2025 the two of them received the 2024 ACM Turing Award "for developing the conceptual and
algorithmic foundations of reinforcement learning."

These words fit together as a loop. The agent looks at the situation. For the arm that's a camera picture, and for
CartPole it's four numbers: where the cart is, how fast it's going, how far the pole leans and how fast it's tipping.
The agent acts, the environment changes, and a reward comes back. In CartPole it comes at every step, and for the arm
only when a try ends. One try from start to finish is an episode. After a batch
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

Taking away the average matters more than it looks. In CartPole every try earns some points, so pushing up every
move by its raw score would push up whatever the learner happened to do, good or bad. With the average taken off,
only the tries that beat the usual result get pushed up.

If all four tries score 0, as they might when the bowl is almost out of reach, the average is 0, every try's score
minus the average is 0, and nothing changes. A learner that never succeeds has nothing to learn from. That's the first
problem in chapter 2. Four scores of 1 change nothing either, because when every try does equally well there's
nothing to tell them apart.

Can a rule this small learn anything real? We gave it to the CartPole learner. In each round it makes 16 tries and
works out their average score. Then every move in every try is made a little more or a little less likely, by that
try's score minus the average. In the first round the 16 tries lasted 22.9 steps on average. By round 300 the average
was 497.5, close to the most a try can score. We ran the whole thing twice more from different random starts, and
those runs ended at 500 and 456.7. Nobody told the learner to move the cart towards the side the pole leans. By round
300 it does: the further the pole leans or tips to one side, the more likely it is to move the cart that way. All it
ever saw was scores. The script is `tools/cartpole/train_and_film.py`, and every score is in
`docs/assets/data/rl01-cartpole.json`.

Rules from the same family work on much harder problems. In 2017 DeepMind put simulated bodies on courses of
"challenging terrains and obstacles" and gave them "a simple reward function based on forward progress". With a
policy-gradient method, the family this chapter's rule belongs to, they learned to "run, jump, crouch and turn"
(video: https://www.youtube.com/watch?v=hx_bgoTF7bs).

## Learning from a score versus learning from examples

Most machine learning is supervised. Every training example comes with the right answer, and the model is corrected
towards it. A learner that copies demonstrations, recordings of an expert doing the task, learns this way, and that's
called behaviour cloning. It's like studying with the answer key open.

RL is like doing practice problems where the teacher only tells you your grade. A grade says how well you did but not
what you should have written, so the feedback is weaker and the learner needs many more tries. In return, nothing
caps it at the level of its teacher. A learner that copies people can at best match them. A learner pushed towards a
higher score can find moves no person showed it. AlphaZero learned chess, shogi and Go only by playing against itself,
starting from random play, and it beat a world-champion program in each of the three (chapter 3).

Three famous results show it happening. The first is DeepMind's DQN, published in *Nature* in 2015. It learned Atari
games "receiving only the pixels and the game score as inputs", and reached "a level comparable to that of a
professional human games tester across a set of 49 games, using the same algorithm, network architecture and
hyperparameters". In Breakout, after about 600 games, it began digging a tunnel up one side of the wall and sending the
ball round the back (video: https://www.youtube.com/watch?v=TmPfTpjtdgg). In the AlphaGo film, Demis Hassabis says the
researchers "didn't know about that strategy".

The second is AlphaGo. It learned first from human games and then by playing against itself, and in March 2016 it beat
the Go champion Lee Sedol 4 games to 1 in Seoul. In game 2 it played a stone that, by DeepMind's account, "had a 1 in
10,000 chance of being played by a human": move 37, at P10 (the film's chapter on game 2:
https://www.youtube.com/watch?v=WXuK6gekU1Y&t=1700s).

The third is OpenAI's hide-and-seek, from 2019. Two teams played in a room with boxes, ramps and walls, and over
millions of rounds the hiders learned to build shelters out of boxes. Then the seekers learned to use ramps to get over
the walls, and the hiders learned to lock the ramps away before building. "We did not explicitly incentivize any of
these behaviors," says the narrator of OpenAI's video (https://www.youtube.com/watch?v=kopoLzvh5jY).

A common belief is that a reward works like a label, telling the model which move was right. It doesn't. In the bowl
example the score comes once, after up to a few hundred steps, and it never says which of those steps helped. Sorting
that out is one of the three things that make RL hard, and chapter 2 is about them.

## Check yourself

1. Name the agent, environment, action, reward and policy for a model that learns to play chess.
2. Four CartPole tries keep the pole up for 20, 40, 60 and 80 steps. Which tries get their moves pushed up, and how do
   the pushes compare?
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
2. The average is 50 steps, so the pushes are −30, −10, +10 and +30. The tries that lasted 60 and 80 steps get their
   moves pushed up, the 80-step try three times as hard as the 60-step one. The tries that lasted 20 and 40 steps get
   theirs pushed down.
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
- Thorndike (1898), *Animal Intelligence: An Experimental Study of the Associative Processes in Animals*; the law of
  effect is quoted from Thorndike (1911), *Animal Intelligence*, p. 244, https://archive.org/details/cu31924003032954.
  What the cats had to do: Britannica, "Thorndike puzzle box" (checked 2026-11-13).
- ACM (2025-03-05), the 2024 Turing Award, https://www.acm.org/media-center/2025/march/turing-award-2024.
- Heess et al. (2017), "Emergence of Locomotion Behaviours in Rich Environments", https://arxiv.org/abs/1707.02286.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518,
  https://www.nature.com/articles/nature14236. The 600 games and the tunnel: the description of Google DeepMind's
  "DQN Breakout" video.
- AlphaGo: https://deepmind.google/research/alphago/ (4–1, the 1 in 10,000 chance); the game 2 record from
  https://homepages.cwi.nl/~aeb/go/games/games/AlphaGo/LeeSedol/2.sgf.
- Baker et al. (2019), "Emergent Tool Use From Multi-Agent Autocurricula", https://arxiv.org/abs/1909.07528.
- Barto, Sutton and Anderson (1983), "Neuronlike adaptive elements that can solve difficult learning control problems",
  *IEEE Transactions on Systems, Man, and Cybernetics* SMC-13(5), 834–846, https://doi.org/10.1109/TSMC.1983.6313077
  (where CartPole comes from).
- Gymnasium, CartPole-v1, https://gymnasium.farama.org/environments/classic_control/cart_pole/ (two actions, 1 point
  per step including the last, ends past 12 degrees, at the track's end or after 500 steps; checked 2026-11-13). 50
  steps a second from `tau = 0.02` in `cartpole.py`, Gymnasium 1.0.0. MIT licence.
- Our CartPole run: `tools/cartpole/train_and_film.py` (step size 0.001, 16 tries a round, 300 rounds, seeds 0–2),
  scores in `docs/assets/data/rl01-cartpole.json`.
