---
name: teaching-interactives
description: How to design the interactive parts and the footage on a teaching web page so they teach one thing and nothing else - start from the one sentence the figure teaches, decide whether it should be interactive at all (a still, a few labelled frames, a short video, or an explorable), make the default state already show the point, put the one control on the object itself, answer within 0.1 s, give it a task and a predict-first question, cut every panel, column, legend and button that isn't in the sentence, open still and let motion start on scroll or tap, and make our own footage (simulator runs filmed by a script in the repo) instead of talk clips. Holds the evidence (interactivity, guided discovery, animation vs static, prediction, seductive details, how many readers click, PhET and explorable-explanation practice), the audit checklist, the audit of RL 1 and the verdicts. Use when building, auditing or redesigning an explorable, widget, slider, stepper, simulation, interactive diagram, quiz-like figure, animation or video on a teaching page, when a component "shows too much stuff", is "hard to interact with" or "not straightforward", and whenever someone asks what an interaction is for, wants "image videos" or real footage instead of talking clips, or asks to make a figure interactive.
---

# Interactive parts that teach

**Why it exists** (user, 2026-11-13, after the RL 1 page). Our interactive components "are just showing too much
stuff. They're not just hard to manage and hard to interact with, but not straightforward." The user asked for this
separate skill and for it to start from their question: "what exactly are we teaching? How exactly are we setting
these interactions so that it benefits teaching?" In the same verdict: "We need more image videos" instead of YouTube
talk clips ("These are harder to understand"), and the painted drawings held ("I like your drawing").

It works with `teaching` (what a chapter teaches) and `teaching-web` (how a page is built and published). Words on
the figure are written with `de-ai-writing` loaded.

The rules below are our reading of the evidence, first applied to RL 1 on 2026-11-13. They stay open until the user
judges the result; their verdicts go at the end.

## The loop, for every interactive figure or video

1. **Write the one sentence the figure teaches**, as a relation between things the reader can see: "each try pushes
   what it did up or down by its score minus the average". List the quantities in it. If you can't write the
   sentence, the figure isn't ready. Everything on screen must be one of those quantities or a label for one.
2. **Decide whether it should be interactive at all.** Interaction earns its place only when the reader changing an
   input of the sentence and seeing the output change is the lesson (Moreno and Mayer 2007). Otherwise:
   - a process in steps → a few labelled still frames side by side, not an animation (Tversky et al. 2002; Mayer et
     al. 2005; Hegarty et al. 2003);
   - a real thing that moves → a short video of it (video-based animation d = 0.76, Höffler and Leutner 2007);
   - a few settings to compare → small multiples side by side, not tabs (nothing important behind a click);
   - many rounds of something → a chart of real data, not a "run 10 rounds" button.
3. **The default state already shows the point**, with labels on the figure and a caption that says what to notice.
   A reader who never touches it still learns the sentence. Nothing the chapter needs sits behind a click, a hover
   or a tab (Conlen, Kale and Heer 2019; Tse 2016; Aisch 2017; Victor 2011; Patel).
4. **One kind of control, on the object.** The reader drags or taps the thing in the sentence (the score, the point),
   not a slider or button off to the side (PhET interviews; Patel: "It's usually better design to use direct
   manipulation to control the inputs"). Label it in one to three words ("Tap a score"). Don't add Play, Step,
   Reset or pace controls for their own sake: learner control has an average effect near zero (Karich et al. 2014,
   g = 0.05), and system-paced animation beat learner-paced (Berney and Bétrancourt 2016).
5. **Answer at once.** The output changes within 0.1 s of the input (Nielsen), in the same figure, next to the
   control. Controls look clickable (Moran 2017: weak signifiers cost 22% more time).
6. **Give it a task and a guess.** Before the figure or right after it, one question the reader answers by using
   it ("all four tries score 0: what happens?"), with a predict box (Brod 2021; Hegarty et al. 2003; Kim et al. 2017),
   and the answer in the prose after it, so the narrative never depends on the interaction. Unguided exploration
   hurts (Alfieri et al. 2011, d = −0.38); guidance, prompts and asking for an explanation help (d = 0.30 overall).
7. **Cut.** Remove every panel, column, legend entry, mode and button that isn't in the sentence (seductive details:
   Rey 2012; PhET's "Radio Waves": experts were impressed, "Students on the other hand were overwhelmed"). Lean
   schematic. One idea per figure; build complexity across figures, and put any free-play sandbox at the end (Case;
   Patel).
8. **Open still.** Nothing moves until the reader scrolls to it or taps it, and nothing loops forever beside the text
   (PhET: "start up with very little or no animation"; Tse: trigger motion on scroll; blinking cues in pictures hurt,
   −0.56 for retention in Schneider et al. 2018, read through the TUM Clearinghouse summary).
9. **Check it at 390 px.** Type on the figure never drops below about 11 px and tap targets stay large. When the
   figure is an SVG that scales, give it a compact layout for narrow screens (a narrower viewBox, bigger type, fewer
   words) instead of letting it shrink.

## Footage ("image videos")

- **Film the thing itself, and prefer our own footage.** A simulator run filmed by a script in the repo gives a clip
  whose licence is ours and whose numbers are checked: every frame is a real state, the script and the data file
  are published, and the page links both. RL 1's CartPole clips are made by `tools/cartpole/train_and_film.py` in
  `vla_final`.
- Other people's footage only with a licence that allows it (CC BY, MIT repos), credited in the caption, or as a
  YouTube embed of a demo. Never re-host a company's video.
- **Keep a clip to one event**: one try, one result, under about 15 s. An overlay is fine when it is part of the
  lesson (RL 1's score counter shows the reward adding up, one point a step). Say in the caption if it's slowed down.
- **How it plays is open** (2026-11-13). Two versions are on RL 1 for the user to compare: figure 1.2 plays muted when
  half of it is on screen, twice, then stops (`video[data-play=view]`); figure 1.5 opens still on its first frame
  with a Play button and plays once (`video[data-play=tap]`). Both pause and replay on tap, and both act like "tap"
  under reduced motion. Record the user's choice in Verdicts.
- Encode H.264 MP4, `yuv420p`, `+faststart`, CRF 28, sides divisible by 8 (else the encoder stretches the frame), with
  a poster JPG of the first frame (a mid-clip poster shows a score before anything has happened).

## Audit checklist

For each component, write a row: the sentence it teaches; the quantities on screen; how many controls and of how many
kinds; what the default state shows with no interaction; what is hidden behind a click, hover or tab; whether the
prose says the point without it; the smallest text and tap target at 390 px; verdict (keep, cut, redesign).

## Audit: RL 1 (2026-11-13)

- **Figure 1.4, the tries explorable** (before). Sentence: each try pushes what it did up or down by its score minus
  the average. On screen: two scenario tabs, two probability bars, a history line chart, a five-column table, four
  buttons (Apply the push, Run 4 new tries, Run 10 rounds, Start over) and a status line. The default state showed
  the batch but not the push; the push needed a click. Tabs, rounds, the history chart and three buttons were outside
  the sentence. **After:** four tries in one row; the only control is each try's score dot (tap or Enter flips it
  0/1); a dashed average line, an arrow from it to each score (score minus average), the push under each, and the
  chance of reaching left with a dotted mark at the old 50%. It opens on the chapter's example and already reads
  50% → 55%. Repeated rounds moved to figure 1.5, a chart of a real run. The "almost out of reach" setting became a
  predict box ("all four tries score 0: what happens?") answered in the prose. Code: `docs/assets/js/rl.js`.
- **Figure 1.3, the loop** (hover groups): every label shows by default and the hover only picks a part out, so it
  stays.
- **Predict boxes**: stay; one more was added as figure 1.4's task.
- **Talk clips in the rail** (two Sergey Levine talks): cut; they were about robots, and the user asked RL 1 to stay
  on RL itself. In their place, real footage in the text (figures 1.2 and 1.5) and a card for our script.
- VLA chapters 1 and 2 are not audited yet (user, 2026-11-13: "let's just focus on RL1 and try to make it right").

## Evidence (read 2026-11-13 by a research pass; access as marked)

- Moreno and Mayer (2007), "Interactive multimodal learning environments", *Educational Psychology Review* 19 [full]:
  interactivity doesn't cause learning by itself. Learners who designed the plants: transfer d = 1.49 and 1.34.
  Ordering the steps of a causal chain was "not sufficient"; adding a prompt to reflect gave d = 0.71. "navigation
  alone ... would not be sufficient to make a learning environment interactive."
- Learner control: Karich, Burns and Maki (2014), *RER* 84(3), 18 studies, g = 0.05 [secondary: TUM Clearinghouse];
  Rey et al. (2019), segmenting, *Educ Psychol Rev* 31 [full]: retention d = 0.32, transfer d = 0.36, learner-paced
  segments helped only transfer (d = 0.45); Berney and Bétrancourt (2016), *Computers & Education* 101, 61 studies,
  g = 0.226 for animation over static, and system-paced animations beat learner-paced ones [abstract and EARLI paper].
- Guidance: Alfieri et al. (2011), *JEP* 103(1) [full]: unassisted discovery vs explicit instruction d = −0.38;
  enhanced discovery d = 0.30; guided discovery 0.50, elicited explanation 0.36, generation −0.15. de Jong and van
  Joolingen (1998), *RER* 68(2) [full]: learners "tend to vary too many variables"; assignments help; adding
  variables gradually was mixed (no gain in a simple domain). Kirschner, Sweller and Clark (2006) [full].
- Animation vs static: Tversky, Morrison and Bétrancourt (2002) [full] ("Animations are often too complex or too fast
  to be accurately perceived"; several diagrams "allow comparison and reinspection"); Höffler and Leutner (2007)
  [abstract]: d = 0.37 overall, video-based 0.76, procedural-motor 1.06; Mayer, Hegarty, Mayer and Campbell (2005)
  [excerpt]: static frames beat narrated animation on 4 of 8 comparisons; Hegarty, Kriz and Cate (2003) [abstract];
  Wong et al. (2012) [abstract]: the transient-information effect grows with longer sections; Kalyuga (2008)
  [abstract]: novices did better with static diagrams.
- Prediction: Brod (2021), *PBR* 28 [full]; Kim, Reinecke and Hullman (2017), CHI [abstract and excerpt]; Sinha and
  Kapur (2021) [abstract]: problem solving before instruction g = 0.36.
- Seductive details: Rey (2012), *ERR* 7(3) [abstract; numbers from the author's slides]: retention d = 0.30, transfer
  0.48, much smaller without time limits (0.10 and 0.06), but seductive pictures still hurt transfer (d = 0.56,
  Rey 2014). Sundararajan and Adesope (2020): g = 0.33 against [secondary].
- Who clicks: Conlen, Kale and Heer (2019), EuroVis [full], over 50,000 sessions: "if details were only revealed after
  a click, readers may never see it"; in one article "the median number of interactions with the algorithm details
  button and with the slider was zero". Tse (2016), Malofiej slides [full, no measurements]: "If you make the reader
  click or do anything other than scroll, something spectacular has to happen." Aisch (2017) [full]: the 85% figure
  counted clicks on one button; "15% of readers isn't nobody", but don't hide what's important. Hohman et al.
  (2020), Distill: "There is limited empirical evaluation of the effectiveness of interactive articles."
- Practice: Victor, "Explorable Explanations" (2011): the explanation "works as a static explanation"; "Most
  interactive widgets dump the user in a sandbox." Amit Patel (Red Blob Games, 2018-2020): "I've tried to make the
  initial state show something without interaction"; "I try to make one diagram for each concept." Nicky Case: give a
  concrete experience first, sandbox at the end. PhET interviews, Adams et al. (2008), *JILR* 19(3) and 19(4) [full]:
  "the simulation must function intuitively"; students hesitate with more than about three groups of three
  controls; "Students only read text that is attached to a control"; but PhET also lets students change "all
  relevant parameters" behind an advanced button. Podolefsky, Moore and Perkins (2013), implicit scaffolding.
  Ciechanowski's articles open on a model with one line saying what to do and what to notice (no written method).
- Usability: Nielsen, response-time limits ("0.1 second is about the limit for having the user feel that the system
  is reacting instantaneously"); Moran (2017), NN/g, flat UI signifiers.
- Not reviewed: 3Blue1Brown; Podolefsky, Perkins and Adams (2010) wouldn't download; the originals of Mayer and
  Chandler (2001), Karich (2014) and Höffler and Leutner (2007, full text).

## Verdicts

After the user judges a page built with this skill, add a dated line: what held, what failed and why.

The canonical copy is `~/.claude/skills/teaching-interactives/`; a copy lives in the `vla_final` repo under
`.claude/skills/teaching-interactives/`. After editing one, copy it to the other.
