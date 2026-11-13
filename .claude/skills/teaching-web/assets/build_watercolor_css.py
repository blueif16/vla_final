"""Builds docs/assets/css/watercolor.css. The painted textures are small SVGs inlined as data URIs, so the theme needs
no image files. Run from a project root that has docs/assets/css/: python3 ~/.claude/skills/teaching-web/assets/build_watercolor_css.py"""
from urllib.parse import quote

def uri(svg):
    svg = " ".join(svg.split())
    return 'url("data:image/svg+xml,' + quote(svg, safe=" =:/'.,-()") + '")'

# Paper grain: fine fractal noise, warm, very faint. Tiles seamlessly.
GRAIN = """<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'>
<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/>
<feColorMatrix values='0 0 0 0 0.42  0 0 0 0 0.35  0 0 0 0 0.24  0.16 0 0 0 -0.035'/></filter>
<rect width='260' height='260' filter='url(#n)'/></svg>"""

# A painted band for a sentence to keep: one stroke of diluted raw umber with ragged ends and a slightly darker edge.
# preserveAspectRatio none, so each line of a wrapped sentence gets its own stroke (box-decoration-break: clone).
def band(color, alpha, seed):
    return f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 40' preserveAspectRatio='none'>
<filter id='f' x='-4%' y='-40%' width='108%' height='180%'>
<feTurbulence type='fractalNoise' baseFrequency='0.035 0.22' numOctaves='3' seed='{seed}' result='n'/>
<feDisplacementMap in='SourceGraphic' in2='n' scale='10' xChannelSelector='R' yChannelSelector='G' result='d'/>
<feGaussianBlur in='d' stdDeviation='0.5' result='b'/>
<feMorphology in='b' operator='erode' radius='1.4' result='e'/>
<feComposite in='b' in2='e' operator='out' result='rim'/>
<feMerge><feMergeNode in='b'/><feMergeNode in='rim'/></feMerge></filter>
<path d='M7 15 C 90 10, 230 13, 393 11 L 395 32 C 250 35, 120 31, 5 34 Z' fill='{color}' fill-opacity='{alpha}' filter='url(#f)'/></svg>"""

# A short brush stroke under each section heading (neutral, so it never borrows a figure colour).
STROKE = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 24' preserveAspectRatio='none'>
<filter id='f' x='-5%' y='-60%' width='110%' height='220%'>
<feTurbulence type='fractalNoise' baseFrequency='0.04 0.3' numOctaves='3' seed='11' result='n'/>
<feDisplacementMap in='SourceGraphic' in2='n' scale='8' xChannelSelector='R' yChannelSelector='G'/></filter>
<path d='M4 13 C 70 8, 190 9, 296 10 L 290 16 C 190 18, 80 17, 6 18 Z' fill='#9C8661' fill-opacity='0.55' filter='url(#f)'/></svg>"""

# A soft wash behind the chapter title: two loose blooms of diluted umber and grey. Neutral on purpose.
HERO = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 360' preserveAspectRatio='none'>
<filter id='f' x='-20%' y='-30%' width='140%' height='160%'>
<feTurbulence type='fractalNoise' baseFrequency='0.012' numOctaves='4' seed='4' result='n'/>
<feDisplacementMap in='SourceGraphic' in2='n' scale='60' xChannelSelector='R' yChannelSelector='G' result='d'/>
<feGaussianBlur in='d' stdDeviation='6' result='b'/>
<feMorphology in='b' operator='erode' radius='5' result='e'/>
<feComposite in='b' in2='e' operator='out' result='rim'/>
<feMerge><feMergeNode in='b'/><feMergeNode in='rim'/></feMerge></filter>
<ellipse cx='300' cy='170' rx='290' ry='120' fill='#D9C7A4' fill-opacity='0.30' filter='url(#f)'/>
<ellipse cx='640' cy='210' rx='230' ry='105' fill='#B9BDB8' fill-opacity='0.22' filter='url(#f)'/></svg>"""

# A wash for small cards (predict, formula): a pale ragged-edged pool.
POOL = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 200' preserveAspectRatio='none'>
<filter id='f' x='-5%' y='-10%' width='110%' height='120%'>
<feTurbulence type='fractalNoise' baseFrequency='0.02 0.05' numOctaves='3' seed='9' result='n'/>
<feDisplacementMap in='SourceGraphic' in2='n' scale='16' xChannelSelector='R' yChannelSelector='G' result='d'/>
<feGaussianBlur in='d' stdDeviation='1.5' result='b'/>
<feMorphology in='b' operator='erode' radius='3' result='e'/>
<feComposite in='b' in2='e' operator='out' result='rim'/>
<feMerge><feMergeNode in='b'/><feMergeNode in='rim'/></feMerge></filter>
<rect x='10' y='10' width='580' height='180' rx='18' fill='#E6D9BE' fill-opacity='0.5' filter='url(#f)'/></svg>"""

css = f"""/* Watercolour theme for the reinforcement-learning series (first used on RL 1, 2026-11-13; not yet judged by the user).
   Layered on site.css: <body class="wc">. Every component of site.css still works; this file only repaints it and
   adds a few text-first components (.predict, .formula, .tries). The painted textures are inline SVG data URIs
   built by a script, so the theme needs no image files.
   Colour meanings in the RL series (one colour, one meaning, on every page):
     ochre  = the learner: the agent and its policy
     sap    = actions and the world they act on (the environment)
     sienna = the score: rewards, and the push they give
   Everything decorative (title wash, heading strokes, key-sentence bands) is neutral umber, so it never borrows a
   meaning colour. Nothing animates. */

.wc {{
  --bg: #FAF6EC;            /* cold-pressed paper */
  --card: #FFFDF7;
  --box: #F1EAD9;
  --line: #DCCFB2;
  --tan: #B49C74;
  --ink: #2B2620;
  --ink-2: #5E5444;
  --ink-3: #7A6E5A;
  --gold: #E8B547;          /* ochre: the learner */
  --gold-soft: #F6E2B0;
  --gold-edge: #B8862A;
  --green: #8DB35A;         /* sap green: actions and the world */
  --green-soft: #E3EDD2;
  --green-dark: #5E8A35;
  --sienna: #C9693F;        /* burnt sienna: the score */
  --sienna-soft: #F2D6C6;
  --sienna-dark: #9A4824;
  --umber: #9C8661;         /* neutral marks */
  --col: 700px;
}}
body.wc {{ background-color: var(--bg); background-image: {uri(GRAIN)}; font-size: 19px; line-height: 1.72; }}

/* the title sits on a loose wash; type is the hero */
.wc .doc-head {{ position: relative; }}
.wc .doc-head::before {{ content: ""; position: absolute; z-index: -1; left: 50%; width: min(100vw, 1020px); transform: translateX(-50%); top: -40px; height: 330px;
  background: {uri(HERO)} center / 100% 100% no-repeat; pointer-events: none; }}
.wc .doc-head h1 {{ font-size: clamp(42px, 7.4vw, 68px); }}
.wc .subtitle {{ color: var(--ink-2); font-style: italic; }}
.wc .outcomes {{ background: rgba(255, 253, 247, .72); border-color: var(--line); border-radius: 6px 14px 8px 16px; }}

/* headings: serif, with a short brush stroke underneath */
.wc .prose h2 {{ font: 400 33px/1.22 var(--serif); margin: 72px 0 22px; padding-bottom: 14px;
  background: {uri(STROKE)} left bottom / 132px 14px no-repeat; }}
.wc .prose h3 {{ font: 600 19px/1.4 var(--sans); }}

/* a sentence to keep: one painted band per line, semibold. Budget unchanged: one per section at most. */
.wc .key {{ font-weight: 600; background: {uri(band('#B79465', 0.42, 7))} 0 0 / 100% 100% no-repeat;
  padding: 0 .12em; -webkit-box-decoration-break: clone; box-decoration-break: clone; }}

/* terms keep their dotted underline; the hover wash is ochre-free so it doesn't read as "the learner" */
.wc .term {{ border-bottom-color: var(--umber); }}
.wc .term:hover, .wc .term[aria-expanded="true"] {{ background: rgba(201, 180, 143, .38); }}
.wc .term-pop {{ border-radius: 6px 14px 8px 14px; box-shadow: 0 14px 34px rgba(43, 38, 32, .15); }}

/* paper slips instead of boxes */
.wc .note {{ background: rgba(241, 234, 217, .78); border-left: 3px solid var(--umber); border-radius: 0 14px 10px 0; }}
.wc .quiz > li, .wc .card, .wc .chapter-nav a, .wc .contents {{ background: rgba(255, 253, 247, .8); border-radius: 6px 14px 8px 14px; }}
.wc .card.text {{ background: rgba(255, 253, 247, .92); }}
.wc .toc a.active {{ border-left-color: var(--umber); }}
.wc .progress {{ background: var(--umber); }}
.wc :focus-visible {{ outline-color: var(--umber); }}
.wc .side {{ border-left-color: var(--umber); }}

/* ---------- predict first (.predict): the reader commits to a guess before the page explains ----------
   No JavaScript and nothing stored: the box is only there so the guess gets written down. */
.predict {{ margin: 30px 0 30px; padding: 18px 22px 16px; background: {uri(POOL)} center / 100% 100% no-repeat; }}
.predict .label {{ color: var(--ink-2); margin-bottom: 4px; }}
.predict > p {{ margin: 0 0 10px; font: 400 21px/1.45 var(--serif); }}
.predict textarea {{ width: 100%; min-height: 3.2em; resize: vertical; font: 16px/1.5 var(--sans); color: var(--ink);
  background: rgba(255, 253, 247, .85); border: 1px dashed var(--umber); border-radius: 6px 10px 8px 10px; padding: 8px 12px; }}
.predict textarea:focus {{ outline: 2px solid var(--umber); outline-offset: 1px; border-style: solid; }}
.predict details {{ margin-top: 10px; }}
.predict summary {{ cursor: pointer; font: 13px var(--mono); color: var(--ink-2); }}
.predict details[open] summary {{ margin-bottom: 6px; }}
.predict details p {{ margin: 0 0 8px; font-size: 17.5px; }}

/* ---------- a rule written out (.formula) ---------- */
.formula {{ margin: 26px 0 26px; padding: 22px 24px; text-align: center; background: {uri(POOL)} center / 100% 100% no-repeat; }}
.formula .eq {{ font: 400 clamp(19px, 3vw, 24px)/1.5 var(--serif); }}
.formula .eq b {{ font-weight: 400; padding: 0 .2em; border-radius: 4px; }}
.formula .eq .s {{ background: var(--sienna-soft); }}
.formula .eq .p {{ background: var(--gold-soft); }}
.formula .label {{ margin-top: 8px; }}

/* ---------- RL 1's explorable: four tries, their scores and the push each one gives (.tries) ---------- */
.tries {{ background: rgba(255, 253, 247, .86); border: 1px solid var(--line); border-radius: 8px 16px 10px 18px; padding: 18px 18px 14px; }}
.tries .seg button[aria-pressed="true"] {{ background: var(--box); }}
.tries-body {{ display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: 22px; align-items: start; margin-top: 6px; }}
.chance {{ display: grid; grid-template-columns: 92px 1fr 46px; gap: 10px; align-items: center; margin: 8px 0; font: 13px var(--mono); }}
.chance .bar {{ height: 18px; border-radius: 9px; background: var(--box); overflow: hidden; border: 1px solid var(--line); }}
.chance .bar i {{ display: block; height: 100%; background: var(--gold); border-right: 2px solid var(--gold-edge); transition: width .45s ease; }}
.chance b {{ font-weight: 600; text-align: right; }}
.tries .hist {{ width: 100%; height: auto; display: block; margin-top: 10px; }}
.tries .hist text {{ font: 10.5px var(--mono); fill: var(--ink-3); }}
.tries-tbl {{ width: 100%; border-collapse: collapse; font: 13.5px/1.4 var(--mono); }}
.tries-tbl th {{ text-align: left; font-weight: 600; font-size: 11.5px; letter-spacing: .04em; text-transform: uppercase; color: var(--ink-3); padding: 0 6px 6px 0; }}
.tries-tbl td {{ padding: 7px 6px 7px 0; border-top: 1px solid var(--line); }}
.tries-tbl .sc {{ display: inline-block; min-width: 1.6em; text-align: center; border-radius: 5px; padding: 0 4px; }}
.tries-tbl .sc.s1 {{ background: var(--sienna); color: #fff; }}
.tries-tbl .sc.s0 {{ background: var(--box); color: var(--ink-2); }}
.tries-tbl .up {{ color: var(--sienna-dark); font-weight: 600; }}
.tries-tbl .down {{ color: var(--ink-2); }}
.tries-tbl .zero {{ color: var(--ink-3); }}
.tries-sum {{ margin: 10px 0 0; font: 13px/1.5 var(--mono); color: var(--ink-2); }}
.tries-say {{ margin: 12px 0 0; min-height: 1.6em; font-size: 16.5px; line-height: 1.55; }}
.tries .ctrl {{ margin-top: 14px; }}
@media (max-width: 760px) {{ .tries-body {{ grid-template-columns: 1fr; }} }}
@media (prefers-reduced-motion: reduce) {{ .chance .bar i {{ transition: none; }} }}

/* ---------- painted figures ----------
   Shapes take filter="url(#wc-wash)" (ragged edge, granulation, darker rim) or url(#wc-line) (a wobbly brush line).
   The filters are defined once per page in a hidden <svg class="wc-defs">. Labels stay crisp. */
.wc .dg text {{ font-family: var(--mono); fill: var(--ink); }}
.wc .dg .lbl {{ font: 400 21px var(--serif); }}
.wc .dg .lbl-i {{ font: italic 400 17px var(--serif); fill: var(--ink-2); }}
.wc .dg .sub {{ font-size: 12.5px; fill: var(--ink-2); }}
.wc .dg .w-learner {{ fill: var(--gold); fill-opacity: .62; }}
.wc .dg .w-world {{ fill: var(--green); fill-opacity: .5; }}
.wc .dg .w-score {{ fill: var(--sienna); fill-opacity: .9; }}
.wc .dg .w-paper {{ fill: #FFFDF7; fill-opacity: .9; }}
.wc .dg .w-umber {{ fill: #CDB58E; fill-opacity: .55; }}
.wc .dg .w-ink {{ fill: #3A332A; fill-opacity: .85; }}
.wc .dg .br-learner {{ stroke: var(--gold-edge); stroke-width: 6; fill: none; stroke-linecap: round; }}
.wc .dg .br-world {{ stroke: var(--green-dark); stroke-width: 6; fill: none; stroke-linecap: round; }}
.wc .dg .br-score {{ stroke: var(--sienna-dark); stroke-width: 5; fill: none; stroke-linecap: round; }}
.wc .dg .br-ink {{ stroke: #3A332A; stroke-width: 2.4; fill: none; stroke-linecap: round; stroke-linejoin: round; }}
.wc-defs {{ position: absolute; width: 0; height: 0; overflow: hidden; }}
"""
open("docs/assets/css/watercolor.css", "w").write(css)
print(len(css))
