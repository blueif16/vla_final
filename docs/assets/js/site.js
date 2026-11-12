/* Learning-site behaviour: term side notes, horizontal rails, YouTube clips that start at a set second,
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
    pop.innerHTML = `<div class="label">${e.t}</div><div>${e.d}</div>` +
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
    if (!G[btn.dataset.term]) console.warn("No glossary entry for", btn.dataset.term);
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
})();
