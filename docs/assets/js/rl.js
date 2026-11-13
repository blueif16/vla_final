/* Explorables for the reinforcement-learning series. Needs site.js loaded first only for the shared page parts;
   this file stands alone. First used on RL 1 (2026-11-13).

   [data-widget=tries]: the arm at one decision point can reach left or right. It runs four tries; each scores 1 if
   the bowl ends on the plate, else 0. "Apply the push" changes the arm's habit with RL 1's rule, which is REINFORCE
   with the batch average as the baseline (Williams 1992):
       theta += lr * sum_i (score_i - average) * (1[try i reached left] - chance of left)
       chance of left = 1 / (1 + exp(-theta))
   With lr = 0.2 the chapter's example batch (left 1, right 0, right 0, left 1) moves "reach left" from 50% to 55%,
   which is the number the text uses. The success chances per mode are made up for teaching, and the page says so. */
(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const sig = (t) => 1 / (1 + Math.exp(-t));
  const pct = (p) => `${Math.round(p * 100)}%`;
  const sgn = (x) => (x > 0 ? "+" : x < 0 ? "−" : "") + Math.abs(x).toFixed(2).replace(/\.?0+$/, "") || "0";

  $$("[data-widget=tries]").forEach((w) => {
    const lr = +w.dataset.lr || 0.2;
    const MODES = {
      easy: { left: 0.7, right: 0.15 },   // the bowl is within reach on the left
      hard: { left: 0.03, right: 0.0 },   // the bowl is almost out of reach: nearly every try scores 0
    };
    const EXAMPLE = [{ a: "left", r: 1 }, { a: "right", r: 0 }, { a: "right", r: 0 }, { a: "left", r: 1 }];
    let mode = "easy", theta = 0, batch = EXAMPLE.slice(), pushed = false, hist = [0.5], busy = null;

    const tbody = $("tbody", w), sum = $(".tries-sum", w), say = $(".tries-say", w);
    const barL = $("[data-bar=left] i", w), barR = $("[data-bar=right] i", w);
    const valL = $("[data-val=left]", w), valR = $("[data-val=right]", w);
    const hist$ = $(".hist", w);
    const btn = (k) => $(`[data-act=${k}]`, w);

    function drawPolicy() {
      const p = sig(theta);
      barL.style.width = pct(p); barR.style.width = pct(1 - p);
      valL.textContent = pct(p); valR.textContent = pct(1 - p);
      // sparkline of "reach left" over rounds, 0-100%, with the 50% line
      const W = 300, H = 70, n = Math.max(hist.length, 2), x = (i) => 30 + (i / Math.max(n - 1, 1)) * (W - 40);
      const y = (v) => 8 + (1 - v) * (H - 22);
      const pts = hist.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(" ");
      hist$.innerHTML =
        `<line x1="30" x2="${W - 10}" y1="${y(0.5)}" y2="${y(0.5)}" stroke="#DCCFB2" stroke-dasharray="4 4"/>` +
        `<text x="0" y="${y(1) + 4}">100%</text><text x="6" y="${y(0.5) + 4}">50%</text><text x="12" y="${y(0) + 4}">0%</text>` +
        `<polyline points="${pts}" fill="none" stroke="#B8862A" stroke-width="2.5" stroke-linejoin="round"/>` +
        `<circle cx="${x(hist.length - 1)}" cy="${y(hist[hist.length - 1])}" r="3.5" fill="#B8862A"/>` +
        `<text x="${W - 10}" y="${H - 1}" text-anchor="end">rounds: ${hist.length - 1}</text>`;
    }

    function drawBatch() {
      const avg = batch.reduce((s, t) => s + t.r, 0) / batch.length;
      tbody.innerHTML = batch.map((t, i) => {
        const adv = t.r - avg;
        const cls = adv > 0 ? "up" : adv < 0 ? "down" : "zero";
        const word = adv > 0 ? "more likely" : adv < 0 ? "less likely" : "no change";
        return `<tr><td>${i + 1}</td><td>reach ${t.a}</td><td><span class="sc s${t.r}">${t.r}</span></td>` +
          `<td class="${cls}">${sgn(adv) || "0"}</td><td class="${cls}">${word}</td></tr>`;
      }).join("");
      sum.textContent = `Average score of these four tries: ${avg.toFixed(2).replace(/\.?0+$/, "") || "0"}`;
      btn("update").disabled = pushed;
    }

    function run() {
      const p = sig(theta), m = MODES[mode];
      batch = Array.from({ length: 4 }, () => {
        const a = Math.random() < p ? "left" : "right";
        return { a, r: Math.random() < m[a] ? 1 : 0 };
      });
      pushed = false;
      drawBatch();
      const allSame = batch.every((t) => t.r === batch[0].r);
      say.textContent = allSame
        ? `All four tries scored ${batch[0].r}. Every score minus the average is 0, so the push will change nothing.`
        : "Tries that beat the average will push their reach up; the others push theirs down.";
    }

    function update() {
      if (pushed) return;
      const p = sig(theta), avg = batch.reduce((s, t) => s + t.r, 0) / batch.length;
      const before = p;
      theta += lr * batch.reduce((s, t) => s + (t.r - avg) * ((t.a === "left" ? 1 : 0) - p), 0);
      pushed = true;
      hist.push(sig(theta));
      drawPolicy(); drawBatch();
      const after = sig(theta);
      say.textContent = Math.round(after * 100) === Math.round(before * 100)
        ? `"Reach left" stays at ${pct(after)}. Nothing in this batch beat the average, so nothing was pushed.`
        : `"Reach left" went from ${pct(before)} to ${pct(after)}.`;
    }

    function rounds(n) {
      if (busy) { clearInterval(busy); busy = null; btn("auto").textContent = "Run 10 rounds"; return; }
      let k = 0;
      btn("auto").textContent = "Stop";
      const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      const step = () => { run(); update(); if (++k >= n) { clearInterval(busy); busy = null; btn("auto").textContent = "Run 10 rounds"; } };
      if (reduce) { for (let i = 0; i < n; i++) { run(); update(); } btn("auto").textContent = "Run 10 rounds"; return; }
      busy = setInterval(step, 420);
    }

    function reset() {
      if (busy) { clearInterval(busy); busy = null; btn("auto").textContent = "Run 10 rounds"; }
      theta = 0; hist = [0.5]; batch = EXAMPLE.slice(); pushed = false;
      drawPolicy(); drawBatch();
      say.textContent = "These are the four tries from the text. Apply the push to see the habit change.";
    }

    btn("run").addEventListener("click", run);
    btn("update").addEventListener("click", update);
    btn("auto").addEventListener("click", () => rounds(10));
    btn("reset").addEventListener("click", reset);
    $$("[data-mode]", w).forEach((b) => b.addEventListener("click", () => {
      mode = b.dataset.mode;
      $$("[data-mode]", w).forEach((o) => o.setAttribute("aria-pressed", String(o === b)));
      reset();
      if (mode === "hard") say.textContent = "Now the bowl is almost out of reach. Run some rounds and watch how often anything changes.";
    }));
    reset();
  });
})();
