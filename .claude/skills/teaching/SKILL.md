---
name: teaching
description: How we make material that teaches us a new field step by step, so a person, or their agent on their behalf, can learn it - a course project's background, a research area, a model, a tool. Backward design from who the learner is and what they must be able to do afterwards, a map of the ideas with the steps experts skip, chapters that each open on one concrete case and end with check questions, what is known, what is our reading and what is still open kept apart with dated sources, and a tutor file (AGENTS.md) so any agent can teach from the chapters one at a time. Markdown first; later the same chapter plan becomes explainer video scripts. Use when asked to teach, explain a topic so it sticks, onboard someone or their agent, write learning chapters, a primer, a study guide, background docs, a lesson or an explainer, and when someone says "teach me", "help me understand", "get my partner up to speed", "for her agent to absorb", 教我, 讲给我听, 入门 or 科普.
---

# Teaching: from zero to working knowledge

**Why it exists** (user, 2026-11-11). We keep stepping into fields we don't know yet, and we want one way to make the
material that teaches us. It starts as markdown chapters that a person can read and that their agent can absorb and
teach from, one step at a time. Later the same plan becomes videos. The first use was the CS 6180 VLA project
(the `vla_final` repo).

**Write every line the learner reads with `de-ai-writing` loaded** (user, 2026-11-11: "do load it in when you are
writing anything to me to teach me something"). Teaching text is published text for this rule, even when the only
reader is us.

## The loop

0. **Check the project's `library/` first** for sources, clips and checked numbers we already hold.
1. **The learner and the goal.** Write two or three sentences about who will learn this: what they already know, what
   they need it for and by when. Then write what they will be able to do at the end, as things a person does: explain
   X to a classmate, predict what happens when Y changes, choose between A and B. Every chapter serves one of these.
   (Backward design, Wilson.)
2. **The map.** List the five to nine ideas the goal needs and draw how they connect (a short text diagram is enough).
   Then find the expert blind spots: the steps you take in one jump that a newcomer has to take in three. Those steps
   get written out, because the writer's knowledge closes every gap in their own head (curse of knowledge, Pinker).
3. **The order.** Open with the question the learner cares about, as a puzzle or a stake ("the robot scores 98% -
   does it read the words at all?"). Then go concrete case → name it → general rule, never the other way round
   (Sanderson: examples before frameworks; concreteness fading, Fyfe et al.). Each chapter needs only the chapters
   before it.
4. **One chapter per idea**, in the shape below. Keep new terms to a handful per chapter, define each one in a clause
   the first time, and put it in the glossary. Cut anything that doesn't serve the chapter's outcome, however true it
   is (coherence and segmenting, Mayer; cognitive load, Sweller).
5. **Name the wrong model.** When a newcomer is likely to believe something false, say the belief and show the case
   that breaks it. A misconception left unnamed survives the chapter (Wilson).
6. **Check questions.** End each chapter with two or three questions that make the learner recall and apply the idea,
   with the answers folded away. Recall beats rereading for what stays (retrieval practice, Roediger and Karpicke). At
   least one question asks them to explain why, in their own words (self-explanation, Chi).
7. **Known, our reading, open.** Mark every claim as one of three things: a fact with its source and date, our own
   reading (say so), or still open. A decision the team hasn't made together is open, and an example the user gave is
   one option, written in their words (our rule: nothing is decided until we decide it together). Numbers are copied from the source, never rounded into
   something new.
8. **The tutor file.** If an agent will teach from the chapters, the repo gets an `AGENTS.md` from
   `templates/tutor.md`, plus `CLAUDE.md` containing `@AGENTS.md`. It tells the agent how to teach (below) and where
   the decided/open list lives.
9. **Hand it over.** The user reads and names any fix. After they judge, write what held or failed into Verdicts below.

## Chapter shape

```markdown
# N. <the idea, in plain words>

After this chapter you can <one to three outcomes from step 1>.
Needs: chapter <M>. Reading time: <n> min.

<One concrete case the learner can picture, before any definition.>

<The idea in plain steps. Every step says how the one before leads to it. One diagram if the picture is the
mechanism; none if it would only decorate.>

<The likely wrong belief, and the case that breaks it.>

## What this means for <our project>
<The link from this idea to the thing we are doing.>

## Check yourself
1. <recall question>
2. <apply question>
3. <why question>

<details><summary>Answers</summary> ... </details>

## Sources
<author, year, title, link; the date we checked anything that changes>
```

Name chapters `NN-short-topic.md` and put an index (`README.md`) in the folder with the order, one line per chapter
and the map from step 2. Keep a `glossary.md`.

## How the tutor agent teaches

This goes into `templates/tutor.md`, and it is the part a learner's agent follows. It comes from LearnLM's five
principles (active learning, managing load, adapting to the learner, curiosity, metacognition) and from Wilson.
- Ask what the learner already knows before the first chapter, and skip or slow down from that.
- One chapter at a time. Start from its concrete case, ask the learner to predict before telling, and give the answer
  plainly if they're stuck. Withholding answers isn't teaching.
- Before moving on, ask the chapter's check questions and listen for the wrong model the chapter names.
- Answer from the chapters and their sources. When the chapters don't cover something, say so and look it up rather
  than guessing.
- Never present an open item as decided. Point to the status list.
- End a session by asking the learner to say in two sentences what they now understand and what is still fuzzy.

## Web page

When a chapter should also be a web page (diagrams, clips at the right second, hover notes for every term, rails of
extra material), build it with the `teaching-web` skill. Its library rule applies to markdown chapters too: every clip
time, image licence and checked number goes into the project's `library/` once, and later chapters reuse it (user,
2026-11-11).

## Later: video

Each chapter can become one explainer: its concrete case is the opening, its check question the closing question,
and the script is written with `de-ai-writing` (`references/spoken.md`) and `captions`. Not built yet; write it here
when we make the first one.

## Verdicts

None yet. After each round the user judges, add a dated line: what was taught, what held, what failed and why.

## Sources

- Greg Wilson, *Teaching Tech Together* (2019), https://teachtogether.tech: learner personas, concept maps, expert
  blind spot, misconceptions, formative checks, backward design.
- Deans for Impact, *The Science of Learning* (2nd ed.):
  https://www.deansforimpact.org/files/assets/thescienceoflearning2nded.pdf (worked examples, retrieval, spacing).
- Grant Sanderson, 3Blue1Brown FAQ and the Summer of Math Exposition notes, https://www.3blue1brown.com/faq/
  (examples before general frameworks, open with the key exercise).
- Fyfe, McNeil, Son and Goldstone (2014), "Concreteness fading in mathematics and science instruction", *Educational
  Psychology Review*.
- Roediger and Karpicke (2006), "Test-enhanced learning", *Psychological Science*. Chi et al. (1994),
  "Eliciting self-explanations improves understanding", *Cognitive Science*.
- Richard Mayer, *Multimedia Learning* (coherence, segmenting, signalling); John Sweller, cognitive load theory.
- Steven Pinker, *The Sense of Style* (2014), chapter on the curse of knowledge.
- LearnLM Team, Google (2024), "LearnLM: Improving Gemini for Learning", https://arxiv.org/abs/2412.16429.

The canonical copy is `~/.claude/skills/teaching/` on Shiran's machine. A copy is kept in the `vla_final` repo
(`.claude/skills/teaching/`) so a partner's agent can use it. After editing one, copy it to the other.
