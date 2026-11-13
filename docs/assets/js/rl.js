/* Explorables and footage for the reinforcement-learning series. Stands alone; site.js handles the shared page parts.

   [data-widget=tries] (RL 1, redesigned 2026-11-13 with the teaching-interactives skill). It teaches one sentence:
   each try pushes what it did up or down by its score minus the average. Four tries of the arm, each reaching left or
   right, each scoring 0 or 1. The reader taps a score dot to flip it; the average line, the arrows (score minus
   average) and the chance of reaching left next time update at once. The rule is REINFORCE with the batch average
   as the baseline (Williams 1992), applied once from a 50/50 start:
       theta = lr * sum_i (score_i - average) * (1[try i reached left] - 0.5),   chance of left = 1 / (1 + exp(-theta))
   With lr = 0.2 the chapter's example (left 1, right 0, right 0, left 1) gives 55%, the number the text uses.

   video[data-play]: real footage. "view" plays muted when at least half of it is on screen, pauses when it leaves,
   stops after two loops, and a tap pauses or replays it. "tap" opens still on its poster with a Play button and plays
   once. Under prefers-reduced-motion every clip behaves like "tap".

   [data-widget=run]: a line chart already drawn in the HTML; this only adds a readout under the pointer. */
(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const NS = "http://www.w3.org/2000/svg";
  const sig = (t) => 1 / (1 + Math.exp(-t));
  const pct = (p) => `${Math.round(p * 100)}%`;
  const num = (x) => (Math.round(x * 100) / 100).toString();
  const signed = (x) => (x > 0 ? "+" : x < 0 ? "−" : "") + num(Math.abs(x));
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- four tries and the push each one gives ---------- */
  $$("[data-widget=tries]").forEach((w) => {
    const lr = +w.dataset.lr || 0.2;
    const tries = [["left", 1], ["right", 0], ["right", 0], ["left", 1]].map(([a, r]) => ({ a, r }));
    const svg = $("svg.tries-plot", w), fill = $(".tries-out .bar i", w), val = $(".tries-out b", w), say = $(".tries-say", w);
    const Y1 = 64, Y0 = 174, y = (s) => Y0 - (Y0 - Y1) * s;
    const el = (tag, attrs, text) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (text != null) e.textContent = text; return e; };
    let X, R, avgLine, avgT, avgV, arrows, advs, effs, dots, compact = null;

    // Two layouts of the same figure: wide (viewBox 470) and, under 440 px, compact (viewBox 380, bigger type and
    // dots, no "more likely" words; the arrows and the sentence below carry them), so text never drops below ~11 px.
    function build() {
      const c = svg.getBoundingClientRect().width < 440;
      if (c === compact) return;
      compact = c;
      X = c ? [80, 152, 224, 296] : [92, 182, 272, 362]; R = c ? 19 : 17;
      const ax = c ? 324 : 406;
      svg.setAttribute("viewBox", c ? "0 0 384 222" : "0 0 470 236");
      svg.classList.toggle("compact", c);
      svg.replaceChildren();
      const defs = el("defs", {});
      const mk = el("marker", { id: "tries-head", viewBox: "0 0 10 10", refX: "6", refY: "5", markerWidth: "5", markerHeight: "5", orient: "auto-start-reverse" });
      mk.appendChild(el("path", { d: "M0 0 L10 5 L0 10 z", fill: "#9A4824" }));
      defs.appendChild(mk); svg.appendChild(defs);
      const lx = c ? 28 : 30;
      svg.appendChild(el("text", { class: "tick", x: lx, y: Y1 + 4, "text-anchor": "middle" }, "1"));
      svg.appendChild(el("text", { class: "tick", x: lx, y: Y0 + 4, "text-anchor": "middle" }, "0"));
      svg.appendChild(el("text", { class: "tick", x: lx, y: (Y1 + Y0) / 2 + 4, "text-anchor": "middle" }, "score"));
      svg.appendChild(el("text", { class: "tick", x: lx, y: 38, "text-anchor": "middle" }, c ? "" : "reached"));
      svg.appendChild(el("text", { class: "tick", x: lx, y: 214, "text-anchor": "middle" }, "push"));
      tries.forEach((t, i) => {
        svg.appendChild(el("text", { class: "hd", x: X[i], y: 16, "text-anchor": "middle" }, `try ${i + 1}`));
        svg.appendChild(el("text", { class: "act", x: X[i], y: 38, "text-anchor": "middle" }, t.a));
        svg.appendChild(el("line", { class: "track", x1: X[i], x2: X[i], y1: Y1, y2: Y0 }));
      });
      avgLine = el("line", { class: "avg", x1: X[0] - 40, x2: ax - 6 }); svg.appendChild(avgLine);
      avgT = el("text", { class: "avg-t", x: ax }); svg.appendChild(avgT);
      avgV = el("text", { class: "avg-t", x: ax }); svg.appendChild(avgV);
      arrows = tries.map(() => { const a = el("line", { class: "arrow", "marker-end": "url(#tries-head)" }); svg.appendChild(a); return a; });
      advs = tries.map((t, i) => { const e = el("text", { class: "adv", x: X[i], y: 214, "text-anchor": "middle" }); svg.appendChild(e); return e; });
      effs = tries.map((t, i) => { const e = el("text", { class: "eff", x: X[i], y: 230, "text-anchor": "middle" }); svg.appendChild(e); return e; });
      dots = tries.map((t, i) => {
        const g = el("g", { class: "dot", tabindex: "0", role: "button" });
        const ring = el("circle", { class: "ring", cx: X[i], r: R + 6 });
        const cc = el("circle", { cx: X[i], r: R });
        const n = el("text", { x: X[i] });
        g.append(ring, cc, n); svg.appendChild(g);
        const flip = () => { t.r = 1 - t.r; draw(); };
        g.addEventListener("click", flip);
        g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); flip(); } });
        return { g, ring, c: cc, n };
      });
    }

    function draw() {
      const avg = tries.reduce((s, t) => s + t.r, 0) / tries.length, ya = y(avg);
      avgLine.setAttribute("y1", ya); avgLine.setAttribute("y2", ya);
      avgT.setAttribute("y", ya - 5); avgT.textContent = "average";
      avgV.setAttribute("y", ya + 13); avgV.textContent = num(avg);
      let theta = 0;
      tries.forEach((t, i) => {
        const adv = t.r - avg, yd = y(t.r), d = dots[i];
        theta += lr * adv * ((t.a === "left" ? 1 : 0) - 0.5);
        d.g.setAttribute("class", `dot s${t.r}`);
        d.g.setAttribute("aria-label", `Try ${i + 1} reached ${t.a} and scored ${t.r}. Press to change its score to ${1 - t.r}.`);
        [d.ring, d.c].forEach((c) => c.setAttribute("cy", yd));
        d.n.setAttribute("y", yd + 5); d.n.textContent = t.r;
        const a = arrows[i];
        if (adv === 0) a.setAttribute("visibility", "hidden");
        else {
          const tip = yd + (adv > 0 ? R + 4 : -(R + 4));
          a.setAttribute("visibility", "visible");
          a.setAttribute("x1", X[i]); a.setAttribute("x2", X[i]); a.setAttribute("y1", ya); a.setAttribute("y2", tip);
        }
        const cls = adv > 0 ? "up" : adv < 0 ? "down" : "zero";
        advs[i].setAttribute("class", `adv ${cls}`); advs[i].textContent = adv === 0 ? "0" : signed(adv);
        effs[i].textContent = compact ? "" : adv > 0 ? "more likely" : adv < 0 ? "less likely" : "no change";
      });
      const p = sig(theta);
      fill.style.width = `${(p * 100).toFixed(1)}%`;
      val.textContent = `50% → ${pct(p)}`;
      const winners = tries.map((t, i) => (t.r > avg ? i + 1 : 0)).filter(Boolean);
      if (tries.every((t) => t.r === tries[0].r)) {
        say.textContent = `All four tries scored ${tries[0].r}, so the average is ${tries[0].r} and every score minus the average is 0. Nothing is pushed, and reaching left stays at 50%.`;
      } else {
        const list = winners.length === 1 ? `Try ${winners[0]} beat` : `Tries ${winners.slice(0, -1).join(", ")} and ${winners[winners.length - 1]} beat`;
        const dir = p > 0.5 + 1e-9 ? `up to ${pct(p)}` : p < 0.5 - 1e-9 ? `down to ${pct(p)}` : "nowhere: the pushes cancel out, and it stays at 50%";
        const what = winners.length === 1 ? "What that try did becomes more likely" : "What those tries did becomes more likely";
        say.textContent = `${list} the average of ${num(avg)}. ${what} and what the others did less likely, so reaching left goes ${dir}.`;
      }
    }
    build(); draw();
    let rt; window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { const was = compact; build(); if (was !== compact) draw(); }, 120); });
  });

  /* ---------- real footage ---------- */
  $$("video[data-play]").forEach((v) => {
    const mode = reduce ? "tap" : v.dataset.play;
    const frame = v.closest(".frame");
    v.muted = true; v.playsInline = true; v.loop = false; v.removeAttribute("autoplay");
    let loops = 0;
    const btn = document.createElement("button");
    btn.type = "button"; btn.className = "play"; btn.textContent = "Play";
    btn.setAttribute("aria-label", "Play the video");
    frame.appendChild(btn);
    const showBtn = (label) => { btn.hidden = false; btn.textContent = label; btn.setAttribute("aria-label", `${label} the video`); };
    const start = () => { btn.hidden = true; v.play().catch(() => showBtn("Play")); };
    btn.addEventListener("click", () => { loops = 0; v.currentTime = 0; start(); });
    v.addEventListener("click", () => { if (v.paused) start(); else { v.pause(); showBtn("Play"); } });
    if (mode === "view") {
      btn.hidden = true;
      v.addEventListener("ended", () => { if (++loops < 2) { v.currentTime = 0; v.play(); } else showBtn("Again"); });
      new IntersectionObserver((es) => es.forEach((e) => {
        if (e.isIntersecting && loops < 2 && btn.hidden) v.play().catch(() => showBtn("Play"));
        else if (!e.isIntersecting && !v.paused) v.pause();
      }), { threshold: 0.5 }).observe(v);
    } else {
      v.addEventListener("ended", () => showBtn("Again"));
    }
  });

  /* ---------- a readout under the pointer on a line chart drawn in the HTML ---------- */
  $$("[data-widget=run]").forEach((fig) => {
    const svg = $("svg", fig), data = JSON.parse($("script[type='application/json']", fig).textContent);
    const { x0, x1, y0, y1, max } = data.frame, ys = data.main, n = ys.length;
    const line = document.createElementNS(NS, "line"), dot = document.createElementNS(NS, "circle"), txt = document.createElementNS(NS, "text");
    line.setAttribute("class", "hover-line"); dot.setAttribute("class", "hover-dot"); dot.setAttribute("r", 4.5);
    txt.setAttribute("class", "lab-main");
    [line, dot, txt].forEach((e) => { e.setAttribute("visibility", "hidden"); svg.appendChild(e); });
    const toSvg = (ev) => { const p = svg.createSVGPoint(); p.x = ev.clientX; p.y = ev.clientY; return p.matrixTransform(svg.getScreenCTM().inverse()); };
    svg.addEventListener("pointermove", (ev) => {
      const p = toSvg(ev); if (p.x < x0 || p.x > x1) return;
      const i = Math.max(0, Math.min(n - 1, Math.round((p.x - x0) / (x1 - x0) * (n - 1))));
      const cx = x0 + (i / (n - 1)) * (x1 - x0), cy = y0 - (ys[i] / max) * (y0 - y1);
      line.setAttribute("x1", cx); line.setAttribute("x2", cx); line.setAttribute("y1", y1); line.setAttribute("y2", y0);
      dot.setAttribute("cx", cx); dot.setAttribute("cy", cy);
      txt.setAttribute("x", Math.min(cx + 8, x1 - 150)); txt.setAttribute("y", Math.max(cy - 10, y1 + 12));
      txt.textContent = `round ${i + 1}: average ${ys[i]}`;
      [line, dot, txt].forEach((e) => e.setAttribute("visibility", "visible"));
    });
    svg.addEventListener("pointerleave", () => [line, dot, txt].forEach((e) => e.setAttribute("visibility", "hidden")));
  });
})();
