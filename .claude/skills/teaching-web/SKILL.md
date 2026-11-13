---
name: teaching-web
description: Turn a teaching chapter (markdown from the teaching skill) into a web page people learn from - Physical Intelligence's blog look (warm off-white, serif titles, mono labels, gold and green flow diagrams with dotted grids), every noun introduced in the sentence or with a hover side note from a shared glossary, a contents rail on the left, inline SVG diagrams chosen by the relationship they show, small explorables the reader drives, horizontal "go deeper" rails of YouTube clips that start and stop at the exact second, reusable figures and note cards, check-yourself answers that fold open, multiple-choice checks with feedback for every option, emphasis on an evidence-based budget (point labels for parallel parts, key sentences, margin notes that show relationships), all published on GitHub Pages. Includes the reference library rule (every clip time, image licence and checked number is recorded once and reused), where clip times come from, which figures may be reused, and the screenshot and click-through checks. Use when asked to make a chapter, lesson, explainer or notes into a web page, github.io site or interactive page, to add visuals, diagrams, SVGs, flowcharts, videos, hover notes, sidenotes or margin notes, highlights or emphasis, or quizzes to teaching content, or to make learning material "look better" or "more web-accessible".
---

# Teaching web pages

**Why it exists** (user, 2026-11-11). Markdown chapters teach agents well but people need more. The user asked for a
github.io page that looks like Physical Intelligence's blog, illustrates every idea with SVG figures in Pi's diagram
style, embeds short YouTube pieces "anchored directly to the minutes", introduces every noun ("we don't want any
nouns to pass through without introduction", with hover side notes), has a menu on the left, and squeezes extra
material into horizontal scroll paths. First built for chapter 1 of `vla_final`; that page is the reference
implementation: `docs/learn/01-what-a-vla-is.html` in the `vla_final` repo (github.com/blueif16/vla_final). Chapter 2
(`docs/learn/02-pi0-and-pi05.html`) is the reference for the explorables added with it and for the emphasis
components.

The words on the page are written with `de-ai-writing` loaded, and the chapter's structure comes from `teaching`.

## The loop

1. **Start from the chapter and the library.** Read the markdown chapter and the project's `library/` (clips,
   images, papers). Use what is there before searching. Anything new you find goes into the library the moment it's
   useful, with its source and date (user, 2026-11-11: "we are recording its references so we don't need to
   re-download it again… just be a part of our pipelines").
2. **List the nouns.** Every term a newcomer might not know is either explained in its own sentence or wrapped as
   `<button class="term" data-term="key">`, on its first use only, with an entry in the shared `glossary.js`. Name the
   parts before showing the process (Mayer's pre-training principle). The page logs a console warning for a term with
   no glossary entry.
3. **One figure per idea, chosen by the relationship** (Clark and Lyons's functions of graphics):
   - parts of a system and how data moves → a flow diagram (boxes and arrows) in Pi's style;
   - a contrast → two panels side by side with the same layout (small multiples, Tufte);
   - a change the reader should feel → an explorable they drive, designed with the `teaching-interactives` skill
     (one sentence, the default state already shows it, one control on the object, nothing behind a click);
   - a real thing moving → a short clip of our own footage (`teaching-interactives`, "Footage");
   - a real thing (a robot, a scene) → a photo or video frame in a dark media frame;
   - numbers → a chart made with the `dataviz` skill.
   No decorative pictures. Put the figure right after the paragraph that points at it and label parts on the figure
   itself (spatial contiguity). Every figure gets a mono caption that says what to notice.
4. **One colour, one meaning, on every page.** Gold = the model being discussed and the main data flow. Green = actions
   and the robot loop. Beige boxes = everything else; white cards = text inputs. Tan arrows = secondary flows. Dashed
   ghost boxes = something present but not used.
5. **Mark the structure and the few things to keep**, from the budget in "Emphasis" below: point labels for a set
   that a figure splits, a key mark on the sentences that come back in later chapters, a margin note for a
   relationship that spans paragraphs, and multiple-choice checks next to the open ones.
6. **Go deeper rails.** After a section, a horizontal rail of 2-4 cards: clips (with start and end), reusable figures
   (with licence credit), and text cards that link to our own project ("2 pictures + 1 sentence"). A rail holds what a
   curious reader wants and a hurried one can skip.
7. **Clips start at the second that matters.** Never guess a time. Take it from a timed source (below), set `end` to
   the next section's start, and say on the card what the listener will hear, in our own words.
8. **Check it** (below), publish to GitHub Pages, and add the page to the site index.

## Style tokens (measured from pi.website/blog/api-beta, 2026-11-11)

- Colours: page `#F5F4EF`, ink `#29271F`, secondary `#625C4B` / `#746D58`, tan `#AAA184`, border and dots `#D7CFB6`,
  box `#EEECE4`, gold `#FBD45B` with edge `#C9A533`, green `#9BBC6C` with dark `#577B37`, media frame near-black.
- Type: Pi uses a classic serif for titles, a humanist sans for body and a mono for labels and captions. Our open
  equivalents: Newsreader, Source Sans 3, IBM Plex Mono (Google Fonts). Body 18 px / 1.68; H1 serif 64 px; subtitle
  serif grey; nav and meta in 14 px mono with underlines.
- Diagrams: a 16 px dot grid (`r=1`, `#D7CFB6`, opacity .65) on `#F5F4EF`; boxes `rx=12`, 1.5 px border; labels 15-17 px
  bold uppercase mono, sublabels 12-13 px mono `#625C4B`; main arrows 8-9 px gold with a triangle marker and a white
  dashed overlay (`10 34`) animated by dash offset; loop arrows green with a dark-green dash; containers dashed
  `6 6`, `rx=20`, label knocked out of the line by a background-coloured rect; line icons in `#746D58` 2.5-3 px with a
  gold joint; motion off under `prefers-reduced-motion`. Draw our own icons in this manner; never copy Pi's artwork.

## Emphasis: structure, key sentences, margin notes, multiple choice

**Why** (user, 2026-11-12, on chapter 2): "Just a bit more emphasis so that we can stay focused longer and keep our
attention, because if we see the whole passage, it's all the text, and it's easy for us to lose our focus." The user
asked for the parallel parts ("the first changes and second changes") to stand out, for the decoration to be "clean,
really clean, and follow our color schema", for more multiple-choice questions, and offered side structures "maybe on
the right" as one option. The design below was built from that and from the evidence; the user hasn't judged it yet.

**What the evidence says** (each read on 2026-11-12; "abstract" means only the abstract was opened):
- Readers remember what is marked, and unmarked text gains nothing: "Virtually all types of signals produce better
  memory for information they cue in a text, whereas memory for unsignaled information often is unaffected" (Lorch
  1989, abstract). So mark only what the reader must keep.
- Too much marking cancels it. Underlining only the target sentences helped cued recall; underlining the targets plus
  half of the other sentences was no better than no underlining (Lorch, Lorch and Klusewitz 1995, abstract).
- Signalling is supported in 24 of 28 tests, median effect size 0.41 (Mayer and Fiorella 2014, abstract). It helps
  most with complex material, for low prior knowledge, and "when signaling methods are used sparingly rather than
  excessively" (Fiorella 2015, citing Stull and Mayer 2007, which we haven't opened).
- Meta-analysis of 103 studies: retention g+ = 0.53, transfer g+ = 0.33, and lower cognitive load (Schneider, Beege,
  Nebel and Rey 2018, abstract). In its moderator table, read through a secondary summary (TUM Clearinghouse, 2018),
  text-structure signals such as headings or bold words give 0.71 (retention) and 0.35 (transfer), and blinking cues in
  pictures give −0.56 and −0.47. So: static cues only, never animated.
- Signals that tie text to a picture: r = .17 overall; .19 for low and medium prior knowledge, −.08 for high (Richter,
  Scheiter and Eitel 2016; the split is from Richter's dissertation version). Our readers are newcomers.
- Web scanning (Nielsen Norman Group): on a wall of text with no cues, readers fall back to the F-pattern (Pernice
  2017); reading the headings and skipping between them ("layer-cake") is the most effective way to scan (Pernice
  2019); readers see the first two words of a line far more than the third, so headings and list items start with the
  words that carry the point (Nielsen 2006); readers skip list items that all start with the same words ("bypassing",
  Pernice 2017); bold and highlight "selectively and sparingly", under 30% of the text (Wang and Chan 2023, guidance,
  not a measurement).
- Margin notes: Tufte CSS floats each note into the right margin from inline markup and hides it behind a tap toggle
  under 760 px (its toggle input is display:none, so the phone toggle may not take keyboard focus; our reading).
  Distill puts a plain `<aside>` in a gutter column and, under 768 px, into the flow at full width, open. Gwern
  ("Sidenotes in Web Design") wants notes on the right, shown by default ("any user effort defeats the point"), few and
  short so a CSS-only layout doesn't overlap, and read by screen readers next to the text they belong to. Words placed
  next to what they refer to help: g = 0.63 over 58 comparisons (Schroeder and Cenkci 2018, abstract; about words and
  pictures, so applying it to margin notes is our reading).
- Multiple choice: feedback after a multiple-choice test raised later cued recall from .31 (no feedback) to .45
  (immediate) and .56 (delayed), and cut wrong answers carried over from the lures from .24 to .15 and .14 (Butler and
  Roediger 2008, forced report, full text). Plausible ("competitive") wrong options made readers recall related facts
  better; cued recall didn't (Little, Bjork, Bjork and Angello 2012, full text). Three options are enough, every
  distractor should be plausible and built from learners' typical errors, none absurd (Haladyna, Downing and Rodriguez
  2002, guidelines read through a secondary page). Feedback that answers the specific choice beats right/wrong alone,
  comes after the attempt and stays short (Shute 2008, full text).

**Budget and rules** (our reading of the evidence, first used on chapter 2, 2026-11-12; open until the user judges):
- **One cue per job.** Headings and point labels show structure; a key mark holds a sentence to keep; a margin note
  shows a relationship; colours keep their figure meanings (gold = the model and its data flow, green = actions, rust
  = gradients); everything else is neutral (ink, tan, beige). No animation on any mark.
- **Key sentences (`strong.key`)**: at most one per h2 section, and only for a fact that later chapters build on or
  the chapter's main claim. Keep the whole page under about 5% of its prose words (chapter 2: 4 sentences, 76 of 1,603
  prose words, 4.7%). Never bold for tone.
- **Point labels (`h3.pt-k`)**: only for a real set of two to four items that a figure or several paragraphs split
  apart. The label gives the number and the count first ("1 of 2 changes"), then the item's topic in its own words.
- **Points to keep (`ol.points`)**: where a paragraph runs several take-aways together. Whole sentences, each starting
  with different words, no bold lead-ins.
- **Margin notes (`aside.side`)**: at most one per h2 section, for a relationship that spans paragraphs or a figure: a
  route, a proportion to scale, a few cases compared, a preview of a set. About 40 words or fewer plus an optional
  mini-diagram in the figure colours, written as plain sentences; a short label on a chip is fine, a row of
  fragments isn't. The note must be shorter than the prose block that hosts it, or end beside narrow prose; the check
  script reports collisions with wide figures.
- **Multiple choice (`li.mcq`)**: three options, one right; the wrong ones are beliefs a newcomer really holds (the
  chapter's named wrong belief first); each option's feedback says in one to three sentences why it's right or wrong,
  using only what the chapter or its sources say. Put them after the open recall questions, numbered on from them,
  and vary which letter is right. Add the same questions to the markdown chapter with the answers in `<details>`.

## Components (in `assets/`, copied into a project's `docs/assets/`)

`site.css` and `site.js` hold everything; `glossary.js` is per project. Markup patterns, all in the reference page:
- `.site-head`, `.doc-head` (h1, `.subtitle`, `.meta`, `.outcomes`, `details.contents` for phones), `nav.toc` (fixed
  left contents with scroll-spy, shown from 1400 px), `.progress` bar.
- `.prose` blocks between full-width `.fig` figures; wide SVGs sit in `.pan` so phones pan instead of shrinking them.
- `button.term[data-term]` → shared popover; works on hover, focus and tap; Esc closes.
- Chinese next to core terms (user, 2026-11-11): a glossary entry's `zh` field is shown in small grey type right after
  the term's first use (term and Chinese kept on one line by a `.term-zh` wrapper) and in the popover's label. Concepts
  get `zh`, names (models, companies, datasets, robots) don't. Use the word Chinese technical writing uses today,
  never a made-up one, and record the choice and its alternatives in the project's `library/terms-zh.yaml`. The
  `.zh` font stack is system CJK fonts only, so no web font is downloaded.
- Real frames: `.frame.film` (style `--cols:N`) is a grid of photos with HTML row labels (`.film-row`, e.g. one per
  camera) and column labels (`.film-col`, e.g. the time); put it in `.pan` so phones pan. `.shots` > `.shot` pairs a
  picture with the sentence it comes with. `.fig.narrow` keeps a tall photo at text width.
- `.rail` > `.rail-head` (`.label`, `.rail-title`, prev/next) + `.rail-track` of `article.card`; clip cards use
  `<div class="media" data-yt="ID" data-start="s" data-end="s" data-title="…">` (thumbnail first, then a
  youtube-nocookie iframe that starts at `start`, stops at `end`); figure cards use `.media.pic`; `.card.text` for notes.
- Explorables: `[data-widget=refine]` (noise → path slider, `data-target` points) and `[data-widget=chunks]`
  (`data-steps`, `data-horizon`, `data-run`). Hover groups in an SVG: `svg.dg[data-hover]` with `.grp[data-g]`.
- `.note` for a named wrong belief, `ol.quiz` with `details` answers, `.chapter-nav`, `.sources`.
- Added with chapter 2 (2026-11-11), reference page `docs/learn/02-pi0-and-pi05.html`: `.callcard` with
  `[data-widget=episode]` (a recorded run, call by call, from a JSON block), `[data-widget=chunk]` (an action-chunk heat
  map), `.scrolly` with `[data-widget=scrolly]` (a sticky figure that changes as steps scroll past), `[data-widget=modes]`
  (buttons that switch a figure between settings), `[data-widget=annotate]` (code whose settings light up the parts
  they control), `.timeline`, `.sharebar`, `.ruler`, `.clip-aside` (one clip inside the text) and `.frame.paper`.
- Added for emphasis (2026-11-12), same reference page:
  - `<strong class="key">` around a sentence to keep: semibold with a low tan band, so it never looks like a link or
    a term (both underlined) or a hovered term (gold).
  - `<h3 class="pt-k"><span class="pt-n">1</span>of 2 changes · the training data</h3>` before each item of a set
    that a figure splits; the badge is ink, so it carries no figure colour.
  - `ol.points`: numbered things to keep, with the same badges.
  - Margin notes: wrap the prose block in `<div class="has-side">` and put `<aside class="side" aria-label="Side note:
    …">` right after the prose, inside the wrapper. From 1240 px the note sits in the right margin, level with the top
    of the wrapper; below that it stays in the flow, open, after its prose, so the reading order is right on phones,
    with screen readers and without CSS. Inside a note: `.label`, short `p`, `.route` with `.chip` (`.in` white text
    input, `.hot` gold model, `.act` light-green action expert, `.out` green actions) and `.down` arrows (an inline
    12×22 SVG, `.g` for green; the route runs across between 640 and 1239 px), `.tokbar` + `.tokbar-key` (tokens to
    scale in figure 2.3's colours), `.side-tbl` (a few cases compared, rows with small inline SVGs) and `ol.side-pts`
    (badges that match `.pt-k`).
  - `li.mcq` in an `ol.quiz` (start a second list with `style="counter-reset: q 5"` to number on): a stem `p`, then
    `ol.mcq-opts` of `<li><details class="mcq-opt" name="mcq-N"><summary>option</summary><p>feedback</p></details></li>`,
    with `right` on the right option's `details`. One shared `name` per question makes opening one close the others.
    It works by click, tap, Enter and Space with no JavaScript; `site.js` only adds a line about the first pick. Marks
    stay neutral: a filled ink ✓ and solid border for right, an outlined ✕ and dashed border for wrong.
  - `.label code`, `.pt-k code` and `.nocase` keep names out of uppercase (a label would turn π0 into Π0 and
    pi05_base into PI05_BASE).

## Watercolour theme (text first)

**Why** (user, 2026-11-13, for the RL series): "use the watercolor style to do something that emphasizes text", with
each page about 15 to 20 minutes of reading, "sort of a new lesson and a new way of interacting". First built for RL 1,
`docs/learn/rl-01-learning-from-a-score.html` in `vla_final`; not yet judged by the user.
- `assets/watercolor.css` layers on `site.css` (`<body class="wc">`); every site.css component still works. It is
  generated by `assets/build_watercolor_css.py`, which inlines the painted textures as SVG data URIs (paper grain, a
  wash behind the title, a brush stroke under each h2, a painted band for `strong.key`, a pool behind small cards), so
  there are no image files. Edit the script, not the CSS.
- Colour meanings for the RL series: ochre = the learner (agent, policy), sap green = actions and the world, burnt
  sienna = the score (rewards and the push they give). Decoration is neutral umber so it never borrows a meaning.
  Nothing animates.
- Figures are inline SVG with two page-level filters in a hidden `<svg class="wc-defs">`: `#wc-wash` (ragged edge,
  granulation, darker rim) for fills (`.w-learner`, `.w-world`, `.w-score`, `.w-paper`, `.w-umber`, `.w-ink`) and
  `#wc-line` for brush lines (`.br-*`). Give `#wc-line` `filterUnits="userSpaceOnUse"` with a region that covers the
  whole figure: with the default bounding-box units a perfectly straight horizontal or vertical line has a zero-height
  box and draws nothing (found on RL 1, figure 1.4). Labels stay crisp, never filtered.
- Text-first components: `.predict` (a question, a textarea that saves nothing, and a `details` to compare; the reader
  commits to a guess before the page explains, the teaching skill's "ask them to predict"; leave out the `details`
  when the next paragraph gives the answer), `.formula` (one rule written out, `b.p` and `b.s` mark its parts in the
  meaning colours), `.tries` (RL 1's explorable, redesigned 2026-11-13 with `teaching-interactives`: an empty
  `svg.tries-plot` that `docs/assets/js/rl.js` draws, a `.tries-out` bar and a `.tries-say` line; its rule is exactly
  the chapter's, and the chapter's example must move "reach left" from 50% to 55%), `table.words` (a term in the first
  column, one column per example), `.frame.clip` with `video[data-play=view|tap]` (our own footage; see
  `teaching-interactives`) and `.runfig[data-widget=run]` (a line chart written into the page by a script between
  `<!-- run-chart:start -->` and `<!-- run-chart:end -->`, with its data in a JSON script tag for the pointer readout).
- On phones, anything decorative that overhangs the column (the title wash) must stay inside the viewport; the check
  script's overflow line catches it.

## Finding clip times

- YouTube refuses caption downloads from our machine without sign-in (yt-dlp: "confirm you're not a bot"), and the
  yt-rag transcript tool returned nothing for these talks. Don't spend time there.
- RoboBoom briefs (roboboom.com/briefs/…, sitemap at roboboom.com/sitemap.xml) split robotics talks into sections,
  each linked to YouTube with `&t=<seconds>`. Fetch a brief with curl and parse the `watch?v=ID&amp;t=Ns` links with
  the `<h3>` that follows. This gave us eleven timed talks for chapter 1.
- A video's own chapter list (in its description, visible through an Exa fetch or search) is the next best source.
- Write every timed section into `library/clips.yaml`, including the ones you don't use yet.

## Images and licences

- Check the licence on the arXiv abstract page first. CC BY 4.0: download the figure from `arxiv.org/html/<id>`, credit
  it in the caption. arXiv's default licence: don't copy figures; link, or draw our own.
- Convert to JPG at most 1600 px wide (`ffmpeg -vf "scale='min(1600,iw)':-2" -q:v 3`). Record every file in
  `library/images.yaml`, with figures we could reuse later.
- Company blogs (Pi, DeepMind) are style or link references only.

## Checks before publishing

- Serve `docs/` locally (`python3 -m http.server`) and screenshot in headless Chrome at 1440 and 390 px wide; look at
  every figure and rail. Headless Chrome screenshots of our own pages are fine; don't use it to get around a site's bot
  protection (the classifier refused that, 2026-11-11).
- Drive the page through the DevTools protocol (Node's built-in `WebSocket`, `--remote-debugging-port`): every
  `data-term` has a glossary entry, every Chinese label sits on its term's line, a popover opens, a clip's iframe has the right `start` and `end`, each widget
  responds, rails scroll, and the page has no horizontal overflow. The script used for chapter 1 is in
  `references/cdp-check.mjs`. For pages with the emphasis components, `references/cdp-check-emphasis.mjs <url>
  <width>` also opens every multiple-choice option by click and by keyboard, checks that each margin note stays in
  the viewport and clear of wide figures, counts the key-sentence budget and reports console errors; run it at 1440,
  about 1100 and 390. Load the page once with scripts disabled (`Emulation.setScriptExecutionDisabled`) and check
  that the quiz still opens and the notes sit in the flow.
- Every number on the page matches `library/papers.yaml`.

## Publishing

GitHub Pages from the `main` branch, `/docs` folder, with `docs/.nojekyll`. Chapters live next to their markdown
(`docs/learn/NN-topic.html`); the index links web chapters, and the markdown on GitHub for chapters not built yet.

## Verdicts

After the user judges a page, add a dated line: what held, what failed and why.
- 2026-11-13, RL 1 (watercolour theme, painted SVG figures, predict-first boxes, the `.tries` explorable). Held: "I
  like your drawing, and every time, I want us to incorporate more image visuals." Failed: (1) we keep reaching for
  YouTube talk clips instead of finding images and short videos to put on the page ("These are harder to understand
  … We need more image videos"); (2) the interactive components on every page "are just showing too much stuff. They're
  not just hard to manage and hard to interact with, but not straightforward." The user asked for a separate skill for
  designing them, starting from "what exactly are we teaching? How exactly are we setting these interactions so that
  it benefits teaching?" Not fixed yet; next session.

## Sources

- Physical Intelligence, "Frontier Models for Every Robot" (pi.website/blog/api-beta, 2026), its workflow SVG measured
  for colours, strokes and type.
- Ruth Colvin Clark and Chopeta Lyons, *Graphics for Learning* (2004; 2nd ed. 2011): communicative functions of
  graphics (decorative, representational, mnemonic, organizational, relational, transformational, interpretive).
- Richard Mayer, *Multimedia Learning*: spatial contiguity, signalling, coherence, segmenting, pre-training.
- Larkin and Simon (1987), "Why a diagram is (sometimes) worth ten thousand words", *Cognitive Science*: diagrams group
  what is used together by location, which cuts search.
- Hohman, Conlen, Heer and Chau (2020), "Communicating with Interactive Articles", Distill: connecting people and data,
  making systems playful, prompting self-reflection, personalising reading, reducing cognitive load.
- Bret Victor, "Up and Down the Ladder of Abstraction" (2011) and "Explorable Explanations" (2011).
- Edward Tufte, *Envisioning Information* (small multiples, layering and separation).
- Emphasis and margin notes (read 2026-11-12): Lorch (1989), "Text-signaling devices and their effects on reading and
  memory processes", *Educational Psychology Review* 1(3) (abstract); Lorch, Lorch and Klusewitz (1995), "Effects of
  typographical cues on reading and recall of text", *Contemporary Educational Psychology* 20(1) (abstract); Mayer
  and Fiorella (2014), *Cambridge Handbook of Multimedia Learning*, 2nd ed., ch. 12 (abstract), and Fiorella (2015),
  UCSB dissertation (escholarship.org/uc/item/55v7s9t1); Schneider, Beege, Nebel and Rey (2018), "A meta-analysis of
  how signaling affects learning with media", *Educational Research Review* 23 (abstract), with the moderator table
  from TUM Clearinghouse Kurzreview 22 (2018); Richter, Scheiter and Eitel (2016), "Signaling text-picture relations in
  multimedia learning", *Educational Research Review* 17 (abstract, and Richter's 2016 Tübingen dissertation);
  Nielsen (2006) "F-Shaped Pattern For Reading Web Content", Pernice (2017) "F-Shaped Pattern of Reading on the Web:
  Misunderstood, But Still Relevant", Pernice (2019) "Text Scanning Patterns: Eyetracking Evidence", Wang and Chan
  (2023) "Formatting Long-Form Content" (all nngroup.com); Tufte CSS (edwardtufte.github.io/tufte-css); Distill's
  guide (distill.pub/guide) and template layout CSS (github.com/distillpub/template); Gwern, "Sidenotes in Web
  Design" (gwern.net/sidenote); Schroeder and Cenkci (2018), "Spatial contiguity and spatial split-attention
  effects in multimedia learning environments", *Educational Psychology Review* 30 (abstract).
- Multiple choice (read 2026-11-12): Butler and Roediger (2008), "Feedback enhances the positive effects and reduces
  the negative effects of multiple-choice testing", *Memory & Cognition* 36(3); Little, Bjork, Bjork and Angello
  (2012), "Multiple-choice tests exonerated, at least of some charges", *Psychological Science* 23(11); Haladyna,
  Downing and Rodriguez (2002), "A review of multiple-choice item-writing guidelines", *Applied Measurement in
  Education* 15(3) (abstract; guideline wording from a secondary page); Shute (2008), "Focus on formative feedback",
  *Review of Educational Research* 78(1).

The canonical copy of this skill and its `assets/` is `~/.claude/skills/teaching-web/`; a copy lives in the
`vla_final` repo under `.claude/skills/teaching-web/`. After editing one, copy it to the other.
