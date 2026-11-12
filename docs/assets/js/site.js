/* Learning-site behaviour: term side notes (with the term's Chinese name when the glossary has a zh field),
   horizontal rails, YouTube clips that start at a set second,
   contents with scroll-spy, hover groups in diagrams, and two small explorables (refine, chunks).
   Canonical copy: ~/.claude/skills/teaching-web/assets/site.js */
(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const fmt = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

  /* ---------- term side notes ---------- */
  const G = window.GLOSSARY || {};
  const pop = document.createElement("div");
  pop.className = "term-pop";
  pop.id = "term-pop";
  pop.setAttribute("role", "tooltip");
  pop.hidden = true;
  document.body.appendChild(pop);
  let openTerm = null, hideTimer = null;

  function place(btn) {
    const r = btn.getBoundingClientRect();
    const w = pop.offsetWidth, h = pop.offsetHeight;
    let left = r.left + window.scrollX + r.width / 2 - w / 2;
    left = Math.max(window.scrollX + 16, Math.min(left, window.scrollX + document.documentElement.clientWidth - w - 16));
    let top = r.bottom + window.scrollY + 8;
    if (r.bottom + h + 16 > window.innerHeight && r.top - h - 8 > 0) top = r.top + window.scrollY - h - 8;
    pop.style.left = left + "px";
    pop.style.top = top + "px";
  }
  function show(btn) {
    clearTimeout(hideTimer);
    const e = G[btn.dataset.term];
    if (!e) return;
    if (openTerm && openTerm !== btn) openTerm.setAttribute("aria-expanded", "false");
    const zh = e.zh ? ` <span class="zh" lang="zh-CN">${e.zh}</span>` : "";
    pop.innerHTML = `<div class="label">${e.t}${zh}</div><div>${e.d}</div>` +
      (e.more ? `<div class="more">${e.more}</div>` : "");
    pop.hidden = false;
    place(btn);
    btn.setAttribute("aria-expanded", "true");
    openTerm = btn;
  }
  function hide(now) {
    clearTimeout(hideTimer);
    const go = () => { pop.hidden = true; if (openTerm) openTerm.setAttribute("aria-expanded", "false"); openTerm = null; };
    now ? go() : (hideTimer = setTimeout(go, 160));
  }
  $$(".term").forEach((btn) => {
    const entry = G[btn.dataset.term];
    if (!entry) console.warn("No glossary entry for", btn.dataset.term);
    // the Chinese name sits right after the term; terms are wrapped on first use only, so it shows once per page
    if (entry && entry.zh && !(btn.nextElementSibling && btn.nextElementSibling.classList.contains("zh"))) {
      const z = document.createElement("span");
      z.className = "zh";
      z.lang = "zh-CN";
      z.textContent = "\u00a0" + entry.zh;
      // a button is an atomic inline, so a line may break between it and the next span; a nowrap wrapper keeps
      // the term and its Chinese name on one line
      const pair = document.createElement("span");
      pair.className = "term-zh";
      btn.before(pair);
      pair.append(btn, z);
    }
    btn.type = "button";
    btn.setAttribute("aria-describedby", "term-pop");
    btn.setAttribute("aria-expanded", "false");
    btn.addEventListener("mouseenter", () => show(btn));
    btn.addEventListener("mouseleave", () => hide());
    btn.addEventListener("focus", () => show(btn));
    btn.addEventListener("blur", () => hide());
    btn.addEventListener("click", (ev) => { ev.stopPropagation(); openTerm === btn && !pop.hidden ? hide(true) : show(btn); });
  });
  pop.addEventListener("mouseenter", () => clearTimeout(hideTimer));
  pop.addEventListener("mouseleave", () => hide());
  document.addEventListener("click", (ev) => { if (!pop.contains(ev.target)) hide(true); });
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") hide(true); });
  window.addEventListener("resize", () => openTerm && !pop.hidden && place(openTerm));

  /* ---------- horizontal rails ---------- */
  $$(".rail").forEach((rail) => {
    const track = $(".rail-track", rail), prev = $(".rail-prev", rail), next = $(".rail-next", rail);
    if (!track) return;
    const step = () => { const c = $(".card", track); return c ? c.getBoundingClientRect().width + 16 : 320; };
    const update = () => {
      if (prev) prev.disabled = track.scrollLeft < 4;
      if (next) next.disabled = track.scrollLeft + track.clientWidth > track.scrollWidth - 4;
    };
    prev && prev.addEventListener("click", () => track.scrollBy({ left: -step(), behavior: "smooth" }));
    next && next.addEventListener("click", () => track.scrollBy({ left: step(), behavior: "smooth" }));
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  });

  /* ---------- YouTube clips: thumbnail first, player starts at the set second ---------- */
  $$("[data-yt]").forEach((m) => {
    const id = m.dataset.yt, start = +m.dataset.start || 0, end = m.dataset.end ? +m.dataset.end : null;
    if (!$("img", m)) {
      const img = document.createElement("img");
      img.src = `https://i.ytimg.com/vi/${id}/hqdefault.jpg`;
      img.alt = ""; img.loading = "lazy";
      m.prepend(img);
    }
    const chip = document.createElement("span");
    chip.className = "yt-time";
    chip.textContent = end ? `${fmt(start)} → ${fmt(end)}` : `from ${fmt(start)}`;
    const b = document.createElement("button");
    b.className = "yt-play";
    b.setAttribute("aria-label", `Play clip from ${fmt(start)}`);
    b.innerHTML = '<span><svg viewBox="0 0 24 24"><path d="M6 4l15 8-15 8z"/></svg></span>';
    m.append(b, chip);
    b.addEventListener("click", () => {
      const f = document.createElement("iframe");
      const q = new URLSearchParams({ start: String(start), autoplay: "1", rel: "0", modestbranding: "1" });
      if (end) q.set("end", String(end));
      f.src = `https://www.youtube-nocookie.com/embed/${id}?${q}`;
      f.title = m.dataset.title || "YouTube clip";
      f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
      f.allowFullscreen = true;
      m.innerHTML = "";
      m.appendChild(f);
    });
  });

  /* ---------- contents: scroll-spy and reading progress ---------- */
  const heads = $$(".prose h2[id]");
  const tocLinks = $$(".toc a");
  const bar = $(".progress");
  function spy() {
    const y = window.scrollY + 140;
    let cur = heads[0];
    heads.forEach((h) => { if (h.offsetTop <= y) cur = h; });
    tocLinks.forEach((a) => a.classList.toggle("active", cur && a.getAttribute("href") === "#" + cur.id));
    if (bar) {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + "%";
    }
  }
  window.addEventListener("scroll", spy, { passive: true });
  spy();

  /* ---------- hover groups in diagrams: point at one part, the rest dims ---------- */
  $$(".dg[data-hover]").forEach((svg) => {
    const parts = $$("[data-g]", svg);
    const groups = $$("[data-g].grp", svg);
    const on = (g) => parts.forEach((p) => p.classList.toggle("dim", !p.dataset.g.split(" ").includes(g)));
    const off = () => parts.forEach((p) => p.classList.remove("dim"));
    groups.forEach((grp) => {
      grp.setAttribute("tabindex", "0");
      grp.addEventListener("mouseenter", () => on(grp.dataset.g));
      grp.addEventListener("focus", () => on(grp.dataset.g));
      grp.addEventListener("mouseleave", off);
      grp.addEventListener("blur", off);
      grp.addEventListener("click", () => on(grp.dataset.g));
    });
  });

  /* ---------- explorable: refining noise into an action chunk ---------- */
  $$("[data-widget=refine]").forEach((w) => {
    const svg = $("svg", w), slider = $("input", w), out = $(".readout", w), again = $(".btn", w);
    const n = 10, line = $(".path", svg), dotsG = $(".dots", svg);
    const target = JSON.parse(w.dataset.target); // [[x,y],...] n points
    let noise = [];
    const rnd = () => noise = target.map(() => [40 + Math.random() * 380, 40 + Math.random() * 200]);
    function draw() {
      const k = +slider.value, t = k / n;
      const pts = target.map((p, i) => [noise[i][0] * (1 - t) + p[0] * t, noise[i][1] * (1 - t) + p[1] * t]);
      line.setAttribute("points", pts.map((p) => p.join(",")).join(" "));
      line.style.opacity = 0.25 + 0.75 * t;
      dotsG.innerHTML = pts.map((p, i) => `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="${i === 0 ? 6 : 5}" />`).join("");
      out.textContent = `step ${k} of ${n}`;
    }
    slider.addEventListener("input", draw);
    again.addEventListener("click", () => { rnd(); slider.value = 0; draw(); });
    rnd(); draw();
  });

  /* ---------- explorable: action chunks on a timeline ---------- */
  $$("[data-widget=chunks]").forEach((w) => {
    const grid = $(".chunk-grid", w), out = $(".readout", w);
    const N = +w.dataset.steps || 40, H = +w.dataset.horizon || 10, R = +w.dataset.run || 5;
    grid.innerHTML = Array.from({ length: N }, () => '<div class="cell"></div>').join("");
    const cells = $$(".cell", grid);
    let t = 0, calls = 0, busy = false, playing = null;
    const report = () => out.textContent = `calls ${calls} · steps run ${t}`;
    function call() {
      if (busy || t >= N) return Promise.resolve(false);
      busy = true; calls++;
      cells.forEach((c) => c.classList.remove("pred", "drop"));
      cells[t].classList.add("call");
      for (let i = t; i < Math.min(t + H, N); i++) cells[i].classList.add("pred");
      report();
      return new Promise((res) => {
        let i = 0;
        const tick = () => {
          if (i < R && t < N) { cells[t].classList.remove("pred"); cells[t].classList.add("done"); t++; i++; report(); setTimeout(tick, 110); }
          else { for (let j = t; j < Math.min(t + H - R, N); j++) { cells[j].classList.remove("pred"); cells[j].classList.add("drop"); } busy = false; res(true); }
        };
        setTimeout(tick, 380);
      });
    }
    function reset() { clearInterval(playing); playing = null; t = 0; calls = 0; busy = false; cells.forEach((c) => c.className = "cell"); report(); }
    $(".do-step", w).addEventListener("click", () => call());
    $(".do-play", w).addEventListener("click", () => {
      if (playing) { clearInterval(playing); playing = null; return; }
      call(); playing = setInterval(() => { if (t >= N) { clearInterval(playing); playing = null; } else call(); }, 1100);
    });
    $(".do-reset", w).addEventListener("click", reset);
    report();
  });

  /* =====================================================================================================
     Components added with chapter 2 (2026-11-11): action-chunk heat map, scroll-driven stage, mode switch,
     code with linked annotations. Chapter 1 doesn't use them.
     ===================================================================================================== */
  const SVGNS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(SVGNS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };

  /* ---------- action-chunk heat map: blue (-1) through beige (0) to green (+1), number printed in each cell ---------- */
  const C0 = [238, 236, 228], CPOS = [87, 123, 55], CNEG = [63, 111, 168];
  const cellColour = (v) => {
    const t = Math.min(1, Math.abs(v)), c = v >= 0 ? CPOS : CNEG;
    return { fill: `rgb(${C0.map((a, i) => Math.round(a + (c[i] - a) * t)).join(",")})`, ink: t > 0.55 ? "#fff" : "#29271F" };
  };
  const fmt2 = (v) => (Math.abs(v) < 0.005 ? 0 : v).toFixed(2).replace("-", "−");
  function chunkMap(g, opts) {
    const o = Object.assign({ x: 0, y: 0, cw: 58, ch: 30, lw: 34, hh: 24, run: 5, bracket: true }, opts);
    g.innerHTML = "";
    o.cols.forEach((c, j) => {
      const t = el("text", { x: o.x + o.lw + j * o.cw + o.cw / 2, y: o.y + o.hh - 8, "text-anchor": "middle", class: "ck-head" }, g);
      t.textContent = c;
    });
    const rows = [];
    for (let i = 0; i < o.rows; i++) {
      const rg = el("g", { class: "ck-r" }, g);
      const lab = el("text", { x: o.x + o.lw - 8, y: o.y + o.hh + i * o.ch + o.ch / 2 + 4, "text-anchor": "end", class: "ck-row" }, rg);
      lab.textContent = i + 1;
      const cells = [];
      for (let j = 0; j < o.cols.length; j++) {
        const cx = o.x + o.lw + j * o.cw, cy = o.y + o.hh + i * o.ch;
        const r = el("rect", { x: cx, y: cy, width: o.cw, height: o.ch, rx: 4, class: "ck-cell" }, rg);
        const t = el("text", { x: cx + o.cw / 2, y: cy + o.ch / 2 + 4.5, "text-anchor": "middle", class: "ck-val" }, rg);
        cells.push({ r, t, tip: el("title", {}, r) });
      }
      rows.push({ g: rg, cells });
    }
    let br = null;
    if (o.bracket) {
      br = el("g", { class: "ck-br" }, g);
      const bx = o.x + o.lw + o.cols.length * o.cw + 8, y0 = o.y + o.hh, ym = y0 + o.run * o.ch, y1 = y0 + o.rows * o.ch;
      el("path", { d: `M${bx} ${y0 + 2}h8V${ym - 3}h-8`, class: "ck-run" }, br);
      el("path", { d: `M${bx} ${ym + 3}h8V${y1 - 2}h-8`, class: "ck-out" }, br);
      [["RUN", (y0 + ym) / 2 - 2, "ck-tag"], ["first " + o.run, (y0 + ym) / 2 + 13, "ck-tag2"],
       ["DROPPED", (ym + y1) / 2 - 2, "ck-tag"], ["asked again", (ym + y1) / 2 + 13, "ck-tag2"]].forEach(([s, y, c]) => {
        if (o.small && c === "ck-tag2") return;
        el("text", { x: bx + 16, y, class: c }, br).textContent = s;
      });
    }
    return {
      set(vals, { done = true, exact = null } = {}) {
        rows.forEach((row, i) => {
          row.g.classList.toggle("ck-drop", done && i >= o.run);
          row.cells.forEach((c, j) => {
            const v = vals[i][j], k = cellColour(v);
            c.r.setAttribute("fill", k.fill);
            c.t.style.fill = k.ink;
            c.t.textContent = fmt2(v);
            c.tip.textContent = `action ${i + 1}, ${o.cols[j]}: ${exact ? exact[i][j] : v.toFixed(4)}`;
          });
        });
        if (br) br.style.opacity = done ? 1 : 0;
      }
    };
  }
  const readJSON = (sel) => { const s = sel && document.querySelector(sel); return s ? JSON.parse(s.textContent) : null; };
  // one fixed noise sample (mulberry32 + Box-Muller), so the page draws the same noise on every visit
  function noiseLike(rows, cols, seed = 7) {
    let a = seed >>> 0;
    const rnd = () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    return Array.from({ length: rows }, () => Array.from({ length: cols }, () => Math.sqrt(-2 * Math.log(rnd() + 1e-9)) * Math.cos(2 * Math.PI * rnd())));
  }
  $$("[data-widget=chunk]").forEach((svg) => {
    const data = chunkOf(readJSON(svg.dataset.src), +svg.dataset.call || 0);
    if (!data) return;
    // on phones the cells get narrower and the bracket labels shorter, so all seven columns fit without panning
    const small = window.matchMedia("(max-width: 600px)").matches;
    const geo = small ? { cw: 46, lw: 26, small: true } : { cw: 58, lw: 34 };
    const rows = data.actions.length, cols = data.cols.length;
    svg.setAttribute("viewBox", `0 0 ${2 + geo.lw + cols * geo.cw + 16 + (small ? 66 : 110)} ${2 + 24 + rows * 30 + 4}`);
    svg.classList.toggle("ck-small", small);
    chunkMap(el("g", {}, svg), Object.assign({ x: 2, y: 2, ch: 30, cols: data.cols, rows, run: +svg.dataset.run || 5 }, geo))
      .set(data.actions, { exact: data.actions });
  });

  // a data block holds either one chunk {cols, actions} or a recorded run {cols, calls: [{step, run, actions}]}
  function chunkOf(d, i) {
    if (!d) return null;
    if (d.actions) return d;
    const c = d.calls[Math.max(0, Math.min(d.calls.length - 1, i))];
    return { cols: d.cols, actions: c.actions, run: c.run, step: c.step };
  }

  /* ---------- a recorded run, call by call: pictures in, chunk out, and the gripper over the whole run ---------- */
  $$("[data-widget=episode]").forEach((w) => {
    const data = readJSON(w.dataset.src);
    if (!data || !data.calls) return;
    const n = data.calls.length, R = data.calls[0].run;
    const imgs = $$("img[data-cam]", w), svg = $(".ep-chunk", w), strip = $(".ep-strip", w);
    const label = $(".ep-label", w), play = $(".ep-play", w);
    const small = window.matchMedia("(max-width: 600px)").matches;
    const geo = small ? { cw: 46, lw: 26, small: true } : { cw: 58, lw: 34 };
    const rows = data.calls[0].actions.length, cols = data.cols.length;
    svg.setAttribute("viewBox", `0 0 ${2 + geo.lw + cols * geo.cw + 16 + (small ? 66 : 110)} ${2 + 24 + rows * 30 + 4}`);
    svg.classList.toggle("ck-small", small);
    const map = chunkMap(el("g", {}, svg), Object.assign({ x: 2, y: 2, ch: 30, cols: data.cols, rows, run: R }, geo));
    const src = (i, cam) => data.img.replace("{NN}", String(i).padStart(2, "0")).replace("{cam}", cam);
    // the strip: one cell per step the robot ran, coloured by the gripper number of that step's action
    let hl = null;
    if (strip) {
      const steps = n * R, W = 600, cw = W / steps;
      strip.setAttribute("viewBox", `0 0 ${W} 58`);
      for (let c = 0; c < n; c++) for (let j = 0; j < R; j++) {
        const v = data.calls[c].actions[j][cols - 1], k = c * R + j;
        const r = el("rect", { x: (k * cw).toFixed(2), y: 14, width: (cw + 0.3).toFixed(2), height: 22, fill: cellColour(v).fill }, strip);
        el("title", {}, r).textContent = `step ${data.calls[c].step + j}: grip ${v}`;
      }
      for (let c = 1; c < n; c++) el("path", { d: `M${(c * R * cw).toFixed(2)} 14v22`, stroke: "#F5F4EF", "stroke-width": 1 }, strip);
      hl = el("rect", { y: 9, height: 32, width: (R * cw).toFixed(2), rx: 3, fill: "none", stroke: "#29271F", "stroke-width": 2 }, strip);
      el("text", { x: 0, y: 54, class: "ep-tick" }, strip).textContent = "step 0";
      el("text", { x: W, y: 54, "text-anchor": "end", class: "ep-tick" }, strip).textContent = `step ${steps - 1}`;
    }
    let cur = 0, timer = null;
    function show(i) {
      cur = (i + n) % n;
      const c = data.calls[cur];
      map.set(c.actions, { exact: c.actions });
      imgs.forEach((im) => { im.src = src(cur, im.dataset.cam); });
      if (label) label.textContent = `call ${cur + 1} of ${n} · starts at step ${c.step}`;
      if (hl) hl.setAttribute("x", (cur * R * (600 / (n * R))).toFixed(2));
    }
    const stop = () => { clearInterval(timer); timer = null; if (play) play.textContent = "Play the run"; };
    $(".ep-prev", w).addEventListener("click", () => { stop(); show(cur - 1); });
    $(".ep-next", w).addEventListener("click", () => { stop(); show(cur + 1); });
    if (play) play.addEventListener("click", () => {
      if (timer) return stop();
      for (let i = 0; i < n; i++) ["table", "wrist"].forEach((cam) => { const im = new Image(); im.src = src(i, cam); });
      if (cur === n - 1) show(0);
      play.textContent = "Pause";
      timer = setInterval(() => { if (cur >= n - 1) stop(); else show(cur + 1); }, 1400);
    });
    show(+w.dataset.call || 0);
  });

  /* ---------- scroll-driven stage: scenes switch as the steps beside (or below) it scroll past ---------- */
  $$("[data-widget=scrolly]").forEach((sc) => {
    const steps = $$(".step", sc), stage = $(".stage", sc);
    const scenes = $$("[data-steps]", stage), pills = $$(".minimap [data-k]", stage);
    const ctrl = $(".stage-ctrl", stage), slider = ctrl && $("input", ctrl), readout = ctrl && $(".readout", ctrl);
    const data = chunkOf(readJSON(sc.dataset.src), +sc.dataset.call || 0), holder = $(".chunk-holder", stage);
    const kOut = $$(".k-out", stage);
    let map = null, noise = null, k = -1, cur = 0, manual = false;
    if (data && holder) {
      map = chunkMap(holder, { x: +holder.dataset.x || 40, y: +holder.dataset.y || 70, cols: data.cols, rows: data.actions.length, run: 5, cw: 54, ch: 31 });
      noise = noiseLike(data.actions.length, data.cols.length);
      $$(".noise-cell", stage).forEach((c, i) => c.setAttribute("fill", cellColour(noise[i % noise.length][3]).fill));
    }
    function drawK(kk) {
      if (!map) return;
      k = kk;
      const t = k / 10;
      const done = cur === 8 && k === 10;
      map.set(data.actions.map((row, i) => row.map((v, j) => noise[i][j] * (1 - t) + v * t)), { done, exact: k === 10 ? data.actions : null });
      if (slider) slider.value = k;
      if (readout) readout.textContent = `step ${k} of 10`;
      kOut.forEach((e) => { e.textContent = done ? "THE ROBOT RUNS ROWS 1-5" : (k === 10 ? "STEP 10 OF 10 · DONE" : `REFINEMENT STEP ${k} OF 10`); });
    }
    function set(n) {
      if (n === cur) return;
      cur = n;
      stage.dataset.step = n;
      steps.forEach((s, i) => s.classList.toggle("is-on", i + 1 === n));
      scenes.forEach((g) => g.classList.toggle("on", g.dataset.steps.split(" ").includes(String(n))));
      const keys = (steps[n - 1].dataset.map || "").split(" ");
      pills.forEach((p) => p.classList.toggle("on", keys.includes(p.dataset.k)));
      if (ctrl) ctrl.hidden = !(n === 7 || n === 8);
      manual = false;
      drawK(n < 7 ? 0 : n === 8 ? 10 : Math.max(0, k));
      const label = $(".label", steps[n - 1]);
      stage.setAttribute("aria-label", `Figure 2.3, step ${n} of ${steps.length}: ${label ? label.textContent : ""}`);
    }
    function onScroll() {
      const vh = window.innerHeight;
      const narrow = window.matchMedia("(max-width: 900px)").matches;
      const sb = narrow ? stage.getBoundingClientRect().bottom : 0;
      const line = narrow ? sb + (vh - sb) * 0.4 : vh * 0.55;
      let n = 1;
      steps.forEach((s, i) => { if (s.getBoundingClientRect().top < line) n = i + 1; });
      set(n);
      if (n === 7 && !manual && map) {
        const r = steps[6].getBoundingClientRect();
        const kk = Math.round(10 * Math.max(0, Math.min(1, (line - r.top) / Math.max(1, r.height * 0.6))));
        if (kk !== k) drawK(kk);
      }
    }
    if (slider) slider.addEventListener("input", () => { manual = true; drawK(+slider.value); });
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    set(1);
    onScroll();
  });

  /* ---------- a figure with settings to switch between: buttons set data-mode, [data-show] parts follow ---------- */
  $$("[data-widget=modes]").forEach((w) => {
    const btns = $$(".seg button", w), parts = $$("[data-show]", w);
    const set = (m) => {
      w.dataset.mode = m;
      btns.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.mode === m)));
      parts.forEach((p) => { p.style.display = p.dataset.show.split(" ").includes(m) ? "" : "none"; });
    };
    btns.forEach((b) => b.addEventListener("click", () => set(b.dataset.mode)));
    set(w.dataset.mode || btns[0].dataset.mode);
  });

  /* ---------- code with linked annotations: point at a setting, the part it controls lights up ---------- */
  $$("[data-widget=annotate]").forEach((w) => {
    const keys = $$(".k[data-part]", w), rows = $$(".spec [data-part]", w), out = $(".annot-out", w);
    const idle = out ? out.innerHTML : "";
    let pinned = null;
    const on = (k) => {
      const ps = k.dataset.part.split(" ");
      w.classList.add("focus");
      keys.forEach((x) => x.classList.toggle("hot", x === k));
      rows.forEach((r) => r.classList.toggle("hot", r.dataset.part.split(" ").some((p) => ps.includes(p))));
      if (out) out.innerHTML = k.dataset.note;
    };
    const off = () => {
      if (pinned) return on(pinned);
      w.classList.remove("focus");
      keys.forEach((x) => x.classList.remove("hot"));
      rows.forEach((r) => r.classList.remove("hot"));
      if (out) out.innerHTML = idle;
    };
    keys.forEach((k) => {
      k.setAttribute("tabindex", "0");
      k.setAttribute("role", "button");
      k.addEventListener("mouseenter", () => on(k));
      k.addEventListener("mouseleave", off);
      k.addEventListener("focus", () => on(k));
      k.addEventListener("blur", off);
      k.addEventListener("click", () => { pinned = pinned === k ? null : k; if (pinned) on(k); else off(); });
      k.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); k.click(); } });
    });
  });
})();
