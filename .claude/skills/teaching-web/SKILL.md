---
name: teaching-web
description: Turn a teaching chapter (markdown from the teaching skill) into a web page people learn from - Physical Intelligence's blog look (warm off-white, serif titles, mono labels, gold and green flow diagrams with dotted grids), every noun introduced in the sentence or with a hover side note from a shared glossary, a contents rail on the left, inline SVG diagrams chosen by the relationship they show, small explorables the reader drives, horizontal "go deeper" rails of YouTube clips that start and stop at the exact second, reusable figures and note cards, check-yourself answers that fold open, all published on GitHub Pages. Includes the reference library rule (every clip time, image licence and checked number is recorded once and reused), where clip times come from, which figures may be reused, and the screenshot and click-through checks. Use when asked to make a chapter, lesson, explainer or notes into a web page, github.io site or interactive page, to add visuals, diagrams, SVGs, flowcharts, videos or hover notes to teaching content, or to make learning material "look better" or "more web-accessible".
---

# Teaching web pages

**Why it exists** (user, 2026-11-11). Markdown chapters teach agents well but people need more. The user asked for a
github.io page that looks like Physical Intelligence's blog, illustrates every idea with SVG figures in Pi's diagram
style, embeds short YouTube pieces "anchored directly to the minutes", introduces every noun ("we don't want any
nouns to pass through without introduction", with hover side notes), has a menu on the left, and squeezes extra
material into horizontal scroll paths. First built for chapter 1 of `vla_final`; that page is the reference
implementation: `docs/learn/01-what-a-vla-is.html` in the `vla_final` repo (github.com/blueif16/vla_final).

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
   - a change over time or a process the reader should feel → an explorable they drive: a slider, a Step/Play button;
   - a real thing (a robot, a scene) → a photo or video frame in a dark media frame;
   - numbers → a chart made with the `dataviz` skill.
   No decorative pictures. Put the figure right after the paragraph that points at it and label parts on the figure
   itself (spatial contiguity). Every figure gets a mono caption that says what to notice.
4. **One colour, one meaning, on every page.** Gold = the model being discussed and the main data flow. Green = actions
   and the robot loop. Beige boxes = everything else; white cards = text inputs. Tan arrows = secondary flows. Dashed
   ghost boxes = something present but not used.
5. **Go deeper rails.** After a section, a horizontal rail of 2-4 cards: clips (with start and end), reusable figures
   (with licence credit), and text cards that link to our own project ("2 pictures + 1 sentence"). A rail holds what a
   curious reader wants and a hurried one can skip.
6. **Clips start at the second that matters.** Never guess a time. Take it from a timed source (below), set `end` to
   the next section's start, and say on the card what the listener will hear, in our own words.
7. **Check it** (below), publish to GitHub Pages, and add the page to the site index.

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
  `references/cdp-check.mjs`.
- Every number on the page matches `library/papers.yaml`.

## Publishing

GitHub Pages from the `main` branch, `/docs` folder, with `docs/.nojekyll`. Chapters live next to their markdown
(`docs/learn/NN-topic.html`); the index links web chapters, and the markdown on GitHub for chapters not built yet.

## Verdicts

None yet. After the user judges a page, add a dated line: what held, what failed and why.

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

The canonical copy of this skill and its `assets/` is `~/.claude/skills/teaching-web/`; a copy lives in the
`vla_final` repo under `.claude/skills/teaching-web/`. After editing one, copy it to the other.
