# AGENTS.md

This is the CS 6180 final project of Jingyi Fu and Shiran Wang, about vision-language-action models (VLAs). As of
2026-11-11 the team has submitted a candidate question (does π0.5 read the instruction on LIBERO?), learned that much of
it is already published, and is choosing what to do instead. No code has been written yet. The project review is on
2026-11-18, the poster on 2026-12-16 and the write-up is due 2026-12-18.

## If someone asks you to teach them this

The chapters in `docs/learn/` are written to be taught in order. Their index is `docs/learn/README.md`.

1. Ask what they already know about robot learning, VLAs and LIBERO, and what they need it for. Skip or slow down from
   their answer.
2. Teach one chapter at a time. Start from the chapter's concrete case, ask them to predict what happens before you
   tell them, and give the answer plainly if they get stuck.
3. Before moving on, ask the chapter's "Check yourself" questions. Each chapter names a wrong belief newcomers often
   hold; listen for it.
4. Answer from the chapters and the sources they cite. If the chapters don't cover a question, say so, then look it up
   and give the source.
5. End each session by asking them to say in two sentences what they now understand and what is still fuzzy. Note the
   fuzzy part and start there next time.

## What is decided and what is open

`docs/learn/06-where-we-stand.md` is the only place that says what the team has decided. Anything not listed there as
decided is open, including the options in that chapter and any idea in the other chapters. Never present an open item
as the plan. When the team decides something together, move it to "Decided" with the date and who decided.

## Writing in this repo

New chapters follow the shape in `.claude/skills/teaching/SKILL.md`. Every fact carries its source and the date it
was checked, and our own readings are labelled as ours. Numbers are copied from their source, never rounded into new
ones.

## Facts that are easy to get wrong

- `pi05_libero` gets two camera images and the instruction, and no robot joint readings (`discrete_state_input=False`
  in openpi's `pi05_libero` config). Chapter 2 explains how we read this from the code.
- Only LIBERO-Goal has all ten tasks starting from the same scene. In the other suites the scene identifies the task.
- The blank-instruction numbers for `pi05_libero` are already published (LIBERO-CF, Table I). See chapter 5.
