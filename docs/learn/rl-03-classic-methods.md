# RL 3. The classic methods, and the games that made them famous

After this chapter you can tell the main families of RL methods apart by what each one learns, work out a small score
sheet by hand, and say why RL won at games long before it was useful anywhere else.
Needs: RL 1 and RL 2. Reading time: 10 min.

In March 2016, DeepMind's AlphaGo beat Lee Sedol, one of the best Go players in the world, by four games to one. Its
37th move in the second game was one that, by AlphaGo's own estimate, a human player would make with a chance of 1 in
10,000, and it won that game. AlphaGo was built from several of the ideas in this chapter at once. It first copied moves from games
between strong human players. Then it improved by playing against itself. It learned to judge how good a board
position was, and before each move it looked ahead through possible continuations of the game.

Each of those pieces is a family of RL methods. This chapter takes them one at a time.

## A score sheet: value-based methods

The first family learns a table of how good each move is in each situation, then simply picks the move with the
highest number. Such a number is called a value, and the table is a score sheet.

Here is a score sheet worked out by hand. A robot stands in a corridor of four squares, A B C D, and gets a reward of 1
when it steps into D. Each step it can move left or right. The rule for filling in the sheet is due to Richard Bellman
in the 1950s:

> value of a move = the reward it earns now + 0.9 × the value of the best move from where you land

The 0.9 is RL 2's discount. Start next to the goal and work backwards.

| Square | Value of "move right" | How |
|---|---|---|
| C | 1 | stepping into D earns 1 |
| B | 0.9 | earns 0 now, then lands on C, worth 1, times 0.9 |
| A | 0.81 | earns 0 now, then lands on B, worth 0.9, times 0.9 |

The reward at the end has flowed back, one square at a time, to the start. This is how a score sheet answers RL 2's
credit assignment question: each move gets credit through the value of where it leads.

In a real problem nobody can fill in the sheet by working backwards, because the agent doesn't know where each move
leads until it tries. Q-learning (Chris Watkins, 1989) fills it in from experience. Each time the agent makes a move,
it nudges that move's number towards "what I just earned + 0.9 × my current guess for where I landed". DeepMind's DQN
(2013, then in *Nature* in 2015) replaced the table with a neural network, so the "situation" could be the raw pixels
of an Atari game screen. In the 2015 paper, one network design with the same settings learned 49 Atari games from the
screen and the score alone, reaching a level comparable to a professional human games tester across them.

## Habits directly: policy gradient

The second family skips the score sheet and adjusts the habits themselves. This is RL 1's rule: run some tries, then
make the actions from better-than-average tries more likely. Think of a basketball player who keeps the shooting
motion from the free throws that went in. Ronald Williams's REINFORCE (1992) is the basic version.

Learning habits directly works when there are too many possible actions to list in a table. A robot arm's seven
numbers can take any value, and a language model chooses each next word from tens of thousands, so their policies are
learned this way. YouTube used REINFORCE to choose which videos to recommend.

## A player and a coach: actor-critic and PPO

The third family combines the first two. A player (the actor) holds the habits, and a coach (the critic) learns a score
sheet of situations. After every move, the coach says whether the game is now going better or worse than it expected
before the move. That difference is RL 1's advantage, now worked out step by step instead of once per episode, so the
player learns from each move without waiting for the final score.

PPO (Schulman et al., 2017) is the actor-critic method most people used for years. It adds a leash. However good a
batch of tries looked, one update may change an action's chance by at most about 20 percent (with the setting the PPO
paper used, the new chance divided by the old one stays between 0.8 and 1.2). One lucky batch can't drag the habits far, which keeps training stable. OpenAI
Five, the team of agents that beat the Dota 2 world champions in 2019, was trained with PPO, and so was the first
generation of chat models (chapter 4).

## Imagining ahead: model-based RL

The fourth family learns how the world responds to actions, which is called a model of the environment, and then plans
by imagining moves before making one. AlphaGo and its successor AlphaZero were given the rules of the game, so they
could look ahead exactly. MuZero (2019) wasn't told the rules. It learned its own model of what mattered for winning,
and still planned with it. It played Go, chess, shogi and Atari games.

Planning saves real tries, which matters most where tries are slow or costly. The catch is that a wrong model makes
for confident plans that fail.

## Copy first, then practise

The fifth family isn't a separate algorithm. It's an order of work: learn by copying experts first, then improve by
practice, the way a learner driver takes lessons before driving alone. AlphaGo copied human games before it played
itself. Every chat model learns from text and worked examples before RL (chapter 4). Robots do the same. π0.5 learned
from demonstrations, and π*0.6 adds practice on top (chapter 7).

Copying first answers RL 2's exploration problem. A policy that already succeeds sometimes gets non-zero scores from
its first batch of tries.

## One choice at a time: bandits

The last family is the simplest. There is one decision, the reward comes right away, and nothing that happens next
depends on it. A news site picks which of three headlines to show, and the reader clicks or doesn't. The name comes
from slot machines ("one-armed bandits"): you face a row of them and have to find the best one while losing as little
as possible on the others. This is RL 2's exploration problem in its purest form, without any credit assignment. It
runs a lot of ad choice, and A/B tests that move traffic towards the winning version while the test is still running.

## The six families side by side

| Family | What it learns | Famous use |
|---|---|---|
| value-based (Q-learning, DQN) | a score sheet of how good each move is in each situation | DQN on Atari |
| policy gradient (REINFORCE) | the habits themselves; do more of what worked | YouTube recommendations; the base of RL for language models |
| actor-critic (PPO) | habits plus a coach who says "better or worse than expected?" | OpenAI Five; the first RLHF chat models |
| model-based (MuZero) | how the world responds, then plans ahead in imagination | AlphaZero, MuZero |
| copy first, then RL | starts from imitation, then practises | AlphaGo; every modern chat model; robots |
| bandits | which single choice pays best | ads; A/B tests |

## Where the ideas came from

Around 1900, psychologists studying animals noticed that a behaviour followed by a reward gets repeated. Edward
Thorndike called it the law of effect. In the 1950s Richard Bellman gave the maths for "how good is this situation",
which is the score sheet above. The core algorithms came between 1988 and 1998. Richard Sutton published
temporal-difference learning (learning a value from the next guess instead of the final result), Chris Watkins
published Q-learning, and Gerald Tesauro's TD-Gammon taught itself backgammon by playing against itself. With some
hand-designed features of the board as input, it reached what Tesauro called "a strong master level that is extremely
close to the world's best human players". Sutton and Andrew Barto's textbook came out in 1998.

From 2013 to 2019 deep networks made RL famous: DQN on Atari, AlphaGo and AlphaZero, OpenAI Five in Dota 2 and
AlphaStar in StarCraft II. After that came a lull, and RL got a reputation for being amazing at games and hard to use
anywhere else. Games give an agent endless, free, exact practice and a clear score. Most real tasks give none of that,
and all three problems from RL 2 get worse. RL found its next big use in language models (chapter 4). In March 2025
Barto and Sutton were named the winners of the 2024 Turing Award, computing's best-known prize, "for developing the
conceptual and algorithmic foundations of reinforcement learning".

## The wrong belief: RL learns from nothing

AlphaZero did learn Go from nothing but the rules, so it's easy to think that this is what RL does. Most of RL's
successes started from copying. AlphaGo learned from human games first, chat models learn from text first, and robots
learn from demonstrations first. AlphaZero could skip that step because a board game is a perfect simulator. Tries are
free, the rules are exact and the score can't be argued with. A robot or a chat model has none of these.

## What this means for our project

`pi05_libero` sits at the end of the copy step: it was trained only on demonstrations. The value-based idea and the
coach are what π*0.6 adds to get from copying to practice (chapter 7).

## Check yourself

1. Which family fits each case best, and why? (a) A shop chooses which of three coupons to email each customer.
   (b) An agent learns Atari games from the screen. (c) A robot arm learns to pour, with continuous motions.
2. In the corridor example, redo the score sheet with a discount of 0.5 instead of 0.9. What is the value of "move
   right" at A?
3. Why did RL beat world champions at games years before it was useful in most other places? Use RL 2's three
   problems in your answer.

<details><summary>Answers</summary>

1. (a) A bandit: one choice, an instant reward (a purchase or not), nothing afterwards depends on it. (b) Value-based,
   as DQN did: a few buttons to choose from, so a score sheet over them works. (c) Policy gradient or actor-critic:
   the motions are continuous, so there's no list of moves to keep a score sheet over. Copying demonstrations first
   would help it get early successes.
2. C is 1, B is 0.5 and A is 0.25.
3. A game gives free, fast and exact tries, so the agent can explore for millions of games (problem 2). Its score is
   clear and hard to argue with, which leaves less room for reward hacking (problem 1), and with that many games even
   blunt credit assignment works (problem 3). Real tasks give few, slow or costly tries and a score someone has to
   write.

</details>

## Sources

- Silver et al. (2016), "Mastering the game of Go with deep neural networks and tree search", *Nature* 529.
- Watkins (1989), PhD thesis, Cambridge; Watkins and Dayan (1992), "Q-learning", *Machine Learning* 8.
- Mnih et al. (2013), "Playing Atari with Deep Reinforcement Learning", https://arxiv.org/abs/1312.5602; Mnih et al.
  (2015), "Human-level control through deep reinforcement learning", *Nature* 518.
- Williams (1992), REINFORCE (see RL 1).
- Schulman et al. (2017), "Proximal Policy Optimization Algorithms", https://arxiv.org/abs/1707.06347
- Schrittwieser et al. (2020), "Mastering Atari, Go, chess and shogi by planning with a learned model", *Nature* 588
  (MuZero; arXiv 2019, https://arxiv.org/abs/1911.08265).
- Sutton (1988), "Learning to predict by the methods of temporal differences", *Machine Learning* 3.
- Tesauro (1994), "TD-Gammon, a self-teaching backgammon program, achieves master-level play", *Neural Computation*
  6(2); Tesauro (1995), "Temporal difference learning and TD-Gammon", *Communications of the ACM* 38(3).
- Silver et al. (2017), AlphaZero, https://arxiv.org/abs/1712.01815
- OpenAI (2019-04-15), "OpenAI Five defeats Dota 2 world champions",
  https://openai.com/index/openai-five-defeats-dota-2-world-champions/; Berner et al. (2019), "Dota 2 with Large Scale
  Deep Reinforcement Learning", https://arxiv.org/abs/1912.06680 (trained with PPO).
- ACM (2025-03-05), "Barto and Sutton receive the 2024 ACM A.M. Turing Award",
  https://www.acm.org/media-center/2025/march/turing-award-2024
- Thorndike (1911), *Animal Intelligence* (the law of effect); Bellman (1957), *Dynamic Programming*.
- Sutton and Barto (1998; 2nd ed. 2018), *Reinforcement Learning: An Introduction*.
- Everything with a date or number above is in `library/rl.yaml` with its source and the date we checked it.
