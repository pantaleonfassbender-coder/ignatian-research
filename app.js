/* app.js — router, data, views */
import * as C from "./corpus.js";
import { corpus } from "./corpus.js";
import * as V from "./viz.js";
import { renderDialogue } from "./dialogue.js";

export const D = {};
const view = document.getElementById("view");

export const esc = s => String(s ?? "").replace(/[&<>"']/g, m =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
export const nf = n => new Intl.NumberFormat("en-GB").format(n);
export const short = (s, n) => (s || "").length > n ? s.slice(0, n - 1).trimEnd() + "…" : (s || "");
const el = h => { const t = document.createElement("template"); t.innerHTML = h.trim(); return t.content.firstElementChild; };

export const WORKCOLOR = {
  spex: "#c9a227", const: "#9db8a4", auto: "#c07a5a",
  diary: "#a89bc4", dir: "#7fa9c9", letters: "#c9968f",
};
export const wc = id => WORKCOLOR[id] || "#8a7d6a";
export const workOf = id => (D.works || []).find(w => w.id === id) || {};

/* --------------------------------------------------------------- boot */
async function boot() {
  const names = ["works", "corpus", "anchors", "letters", "terms", "keyness", "network",
    "discernment", "persons", "places", "itinerary", "introductions", "sections",
    "lexicon", "glossary"];
  const res = await Promise.all(names.map(n => fetch(`data/${n}.json`).then(r => r.json())));
  names.forEach((n, i) => D[n] = res[i]);
  D.introOf = {}; D.introductions.forEach(x => D.introOf[x.id] = x);
  try { await C.restore(D.works, D.anchors, D.letters); }
  catch (e) { console.warn("restore failed", e); }
  refreshUnlockBadge();
  window.addEventListener("hashchange", route);
  route();
}

const ROUTES = {
  overview: viewOverview, works: viewWorks, letters: viewLetters,
  concordance: viewConcordance, lexicon: viewLexicon, atlas: viewAtlas,
  register: viewRegister, language: viewLanguage, glossary: viewGlossary,
  method: viewMethod, dialogue: a => renderDialogue(view, a),
  privacy: viewPrivacy, imprint: viewImprint,
};
function route() {
  const h = (location.hash || "#/overview").slice(2).split("/");
  const name = h[0] || "overview";
  document.querySelectorAll("#nav a").forEach(a => a.classList.toggle("active", a.dataset.v === name));
  view.innerHTML = ""; window.scrollTo(0, 0);
  (ROUTES[name] || viewOverview)(h.slice(1));
}

/* ------------------------------------------------------------- pieces */
export function citeChip(cite, work) {
  if (!cite) return "";
  return `<a class="cite" href="#/works/${work}" title="${esc(workOf(work).titel || "")}">${esc(cite.label)}${cite.seite ? `, p. ${cite.seite}` : ""}</a>`;
}
function rightsBadge(w) {
  if (w.rechte === "public-domain") return `<span class="rights pd">public domain</span>`;
  return C.isOpen(w.id)
    ? `<span class="rights open">open on this device</span>`
    : `<span class="rights cr">in copyright · locked</span>`;
}
export function lockedBox(text) {
  const b = el(`<div class="locked"><strong>Full text not shipped</strong>
    <p style="margin:.3rem 0 .9rem;font-size:.9rem">${esc(text)}</p>
    <button class="primary">Open from your own copy</button></div>`);
  b.querySelector("button").onclick = openUnlock;
  return b;
}
export const debounce = (fn, ms) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; };

/* ============================================================ OVERVIEW */
function viewOverview() {
  const k = D.corpus;
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">Research apparatus</span>
      <h1>The writings of Ignatius of Loyola</h1>
      <p class="lede">Six texts, one working corpus: a retreat manual, a body of law, a dictated memoir,
      a private journal of discernment, a set of instructions for directors, and twenty-four letters.
      This apparatus indexes them by their canonical numbering, traces the vocabulary that migrates
      between them, and lets you put questions to the corpus with the evidence attached.</p>
    </div>

    <div class="grid g4" style="margin-bottom:1.6rem">
      <div class="kpi"><b>6</b><span>works</span></div>
      <div class="kpi"><b>${nf(k.pdf_seiten)}</b><span>pages</span></div>
      <div class="kpi"><b>${nf(k.anker)}</b><span>canonical anchors</span></div>
      <div class="kpi"><b>${nf(k.tokens)}</b><span>analysed tokens</span></div>
      <div class="kpi"><b>${nf(k.lemmata)}</b><span>lemmas</span></div>
      <div class="kpi"><b>${k.briefe}</b><span>letters in full</span></div>
    </div>

    <div class="grid g2" style="margin-bottom:2rem">
      <div class="card">
        <span class="tag">What is here without anything further</span>
        <h3>The Letters, in full</h3>
        <p style="font-size:.92rem;color:var(--fg2)">O'Leary's 1914 translation is in the public domain, so all
        twenty-four letters of 1524–1547 are included complete: readable, searchable, quotable, and part of
        every cross-corpus function on this site.</p>
        <p><a class="btn" href="#/letters">Read the letters →</a></p>
      </div>
      <div class="card" id="unlockCard">
        <span class="tag">What needs your own copy</span>
        <h3>The five modern translations</h3>
        <p style="font-size:.92rem;color:var(--fg2)">Ganss, Padberg, Divarkar, Munitiz and Palmer are under
        copyright. Their structure, statistics and citation anchors are here; their running text is not.
        Open them from a PDF you own and the concordance, canonical citation of hits and the evidence mode
        of the dialogue extend across the whole corpus.</p>
        <div id="unlockCardState"></div>
        <button class="primary" id="startUnlock">Open from your own copies</button>
      </div>
    </div>

    <h2>The corpus</h2>
    <div class="grid g3" id="worklist" style="margin-bottom:2.4rem"></div>

    <div class="grid g2">
      <div class="chartbox">
        <span class="tag">Where the vocabulary of discernment sits</span>
        <canvas id="discchart" style="margin-top:.6rem"></canvas>
        <div class="legend" id="disclegend"></div>
        <p class="fine">Each bar is one term family, split by the work it occurs in. Tears belong almost
        entirely to the Diary; discreet charity almost entirely to the Constitutions.</p>
      </div>
      <div class="chartbox">
        <span class="tag">Most frequent content lemmas across the corpus</span>
        <canvas id="topterms" style="margin-top:.6rem"></canvas>
      </div>
    </div>
  </div>`));

  const wl = view.querySelector("#worklist");
  for (const w of D.works) {
    const intro = D.introOf[w.id] || {};
    const card = el(`<div class="workcard" style="border-top:3px solid ${wc(w.id)}">
      <div style="display:flex;justify-content:space-between;gap:.6rem;align-items:flex-start">
        <h3>${esc(w.titel)}</h3></div>
      <div>${rightsBadge(w)}</div>
      <p class="fine" style="margin:0">${esc(w.uebersetzer)} · ${w.jahr} · ${esc(w.entstehung)}</p>
      <p style="font-size:.9rem;color:var(--fg2);margin:.2rem 0 0">${esc(w.beschreibung)}</p>
      <p class="fine" style="margin:.3rem 0 0">${nf(w.tokens)} tokens · ${w.anker ? nf(w.anker) + " anchors · " : ""}cited as <span class="mono">${esc(w.zitierweise)}</span>${intro.genre ? " · " + esc(intro.genre) : ""}</p>
    </div>`);
    card.onclick = () => location.hash = `#/works/${w.id}`;
    wl.append(card);
  }
  view.querySelector("#startUnlock").onclick = openUnlock;
  refreshUnlockCard();

  requestAnimationFrame(() => {
    const rows = D.discernment.slice(0, 14).map(d => ({
      label: d.begriff, v: d.f, disp: nf(d.f),
      parts: d.dist.map((v, i) => ({ v, color: wc(D.corpus.ids[i]) })),
    }));
    stackedBars(view.querySelector("#discchart"), rows, 210);
    view.querySelector("#disclegend").innerHTML = D.corpus.ids.map(id =>
      `<span><i style="background:${wc(id)}"></i>${esc(workOf(id).kurz)}</span>`).join("");
    V.bars(view.querySelector("#topterms"),
      D.corpus.top_lemmata.slice(0, 22).map(([w, f]) => ({ label: w, v: f, disp: nf(f) })),
      { padL: 150 });
  });
}

/** Stacked horizontal bars (work-by-work split). */
function stackedBars(cv, rows, padL) {
  const w = cv.clientWidth || 600, rowH = 24, h = rows.length * rowH + 8;
  const r = window.devicePixelRatio || 1;
  cv.width = w * r; cv.height = h * r; cv.style.width = w + "px"; cv.style.height = h + "px";
  const c = cv.getContext("2d"); c.setTransform(r, 0, 0, r, 0, 0);
  c.font = "12px -apple-system,Segoe UI,Roboto,sans-serif"; c.textBaseline = "middle";
  const max = Math.max(1, ...rows.map(x => x.v));
  rows.forEach((row, i) => {
    const y = i * rowH + rowH / 2 + 4;
    c.fillStyle = "#bcae99"; c.textAlign = "right";
    let lab = row.label;
    while (c.measureText(lab).width > padL - 12 && lab.length > 4) lab = lab.slice(0, -1);
    c.fillText(lab === row.label ? lab : lab + "…", padL - 8, y);
    let x = padL;
    const scale = (w - padL - 54) / max;
    for (const p of row.parts) {
      if (!p.v) continue;
      c.fillStyle = p.color; c.globalAlpha = .9;
      c.fillRect(x, y - 7, Math.max(1, p.v * scale), 14);
      x += p.v * scale;
    }
    c.globalAlpha = 1; c.fillStyle = "#8a7d6a"; c.textAlign = "left";
    c.fillText(row.disp, x + 7, y);
  });
}

/* =============================================================== WORKS */
function viewWorks(args) {
  if (args && args[0]) return workDetail(args[0]);
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">Six works</span>
      <h1>The corpus, work by work</h1>
      <p class="lede">Each entry gives an orientation, a note on the textual history and the translation used,
      practical advice on navigating the numbering, the passages that carry the most weight, and the internal
      divisions of the text.</p>
    </div><div class="grid g2" id="wl"></div></div>`));
  const wl = view.querySelector("#wl");
  for (const w of D.works) {
    const intro = D.introOf[w.id] || {};
    const card = el(`<div class="workcard" style="border-left:3px solid ${wc(w.id)}">
      <h3>${esc(w.titel)}</h3>
      <div>${rightsBadge(w)} <span class="chip">${esc(intro.genre || "")}</span>
        <span class="chip">difficulty ${"●".repeat(intro.difficulty || 0)}${"○".repeat(5 - (intro.difficulty || 0))}</span></div>
      <p class="fine" style="margin:0">trans. ${esc(w.uebersetzer)}, ${w.jahr} · ${esc(w.verlag)}</p>
      <p style="font-size:.9rem;color:var(--fg2);margin:.3rem 0 0">${esc(short(intro.orientation || w.beschreibung, 230))}</p>
    </div>`);
    card.onclick = () => location.hash = `#/works/${w.id}`;
    wl.append(card);
  }
}

function workDetail(id) {
  const w = workOf(id), intro = D.introOf[id] || {};
  if (!w.id) { location.hash = "#/works"; return; }
  const secs = D.sections.filter(s => s.id === id);
  const idx = D.works.findIndex(x => x.id === id);
  const prev = D.works[(idx - 1 + D.works.length) % D.works.length];
  const next = D.works[(idx + 1) % D.works.length];
  view.append(el(`<div>
    <p class="fine"><a href="#/works">← All works</a> ·
      <a href="#/works/${prev.id}">${esc(prev.kurz)}</a> · <a href="#/works/${next.id}">${esc(next.kurz)}</a></p>
    <div class="viewhead">
      <span class="tag" style="color:${wc(id)}">${esc(intro.genre || "")} · written ${esc(w.entstehung)}</span>
      <h1>${esc(w.titel)}</h1>
      <p class="fine">Translated by ${esc(w.uebersetzer)} · ${esc(w.verlag)}, ${w.jahr} ·
        cited as <span class="mono">${esc(w.zitierweise)}</span> · ${rightsBadge(w)}</p>
    </div>

    <div class="panel"><span class="tag">Orientation</span>
      <p class="readable">${esc(intro.orientation || "")}</p></div>

    <div class="grid g2">
      <div class="panel"><span class="tag">Textual history</span>
        <p class="readable" style="font-size:.98rem">${esc(intro.textual_history || "")}</p></div>
      <div class="panel"><span class="tag">How to read it</span>
        <p class="readable" style="font-size:.98rem">${esc(intro.how_to_read || "")}</p></div>
    </div>

    <div class="panel"><span class="tag">Passages that carry weight</span>
      <div class="grid g2" style="margin-top:.7rem">
        ${(intro.key_passages || []).map(p => `<div class="card">
          <span class="cite">${esc(p.cite)}</span>
          <h4 style="margin:.4rem 0 .3rem;font-size:1rem">${esc(p.label)}</h4>
          <p style="font-size:.87rem;color:var(--fg2);margin:0">${esc(p.why)}</p></div>`).join("")}
      </div></div>

    ${secs.length ? `<div class="panel"><span class="tag">Internal divisions</span>
      <div id="secs" style="margin-top:.7rem"></div></div>` : ""}

    <div class="grid g2">
      <div class="panel"><span class="tag">Profile</span>
        <table style="font-size:.85rem">
          <tr><td>Extent</td><td class="num">${nf(w.tokens)} tokens · ${w.pdf_seiten} pp.</td></tr>
          <tr><td>Sentences</td><td class="num">${nf(w.saetze)}</td></tr>
          <tr><td>Mean sentence length</td><td class="num">${w.satzlaenge} words</td></tr>
          <tr><td>Mean word length</td><td class="num">${w.wortlaenge} characters</td></tr>
          <tr><td>Noun rate</td><td class="num">${w.nominalquote} %</td></tr>
          <tr><td>Type–token ratio</td><td class="num">${w.ttr}</td></tr>
          <tr><td>Readability (LIX)</td><td class="num">${w.lix}</td></tr>
          <tr><td>Canonical anchors</td><td class="num">${w.anker ? `${nf(w.anker)} of ${nf(w.maxn)}` : "—"}</td></tr>
        </table></div>
      <div class="panel"><span class="tag">Characteristic lemmas (log-likelihood against the rest of the corpus)</span>
        <canvas id="keychart" style="margin-top:.6rem"></canvas></div>
    </div>

    <div class="panel"><span class="tag">Full text</span><div id="ftbox"></div></div>
  </div>`));

  if (secs.length) {
    const box = view.querySelector("#secs");
    for (const s of secs) {
      box.append(el(`<div style="border-left:2px solid ${wc(id)};padding-left:.9rem;margin-bottom:1rem">
        <div style="display:flex;gap:.6rem;align-items:baseline;flex-wrap:wrap">
          <strong style="font-family:var(--serif);font-size:1.03rem">${esc(s.name)}</strong>
          <span class="cite">${esc(w.zk)} [${s.von}–${s.bis}]</span></div>
        <p style="font-size:.9rem;color:var(--fg2);margin:.3rem 0 .2rem">${esc(s.summary)}</p>
        <p class="fine"><strong style="color:var(--acc2)">Watch for:</strong> ${esc(s.watch_for)}</p></div>`));
    }
  }

  requestAnimationFrame(() => {
    V.bars(view.querySelector("#keychart"),
      (D.keyness[id] || []).slice(0, 18).map(k => ({ label: k.w, v: k.ll, disp: `${k.f}× · LL ${k.ll}`, color: wc(id) })),
      { padL: 150 });
  });

  const ft = view.querySelector("#ftbox");
  if (id === "letters") {
    ft.append(el(`<p>The letters are public domain and included in full.
      <a class="btn" href="#/letters">Open the reader →</a></p>`));
  } else if (!C.isOpen(id)) {
    ft.append(lockedBox(`${w.titel} is under copyright in this translation. Open your own PDF to search it, read hits in context and cite them by ${w.zitierweise}.`));
  } else {
    ft.append(el(`<div><div class="toolbar" style="margin-bottom:.7rem">
      <input class="grow" id="fq" type="search" placeholder="Search within this work …"></div>
      <div id="fres"><p class="fine">Type at least three characters.</p></div></div>`));
    const fq = ft.querySelector("#fq"), fres = ft.querySelector("#fres");
    fq.oninput = debounce(() => {
      const q = fq.value.trim();
      if (q.length < 3) { fres.innerHTML = `<p class="fine">Type at least three characters.</p>`; return; }
      const rows = C.kwic(q, { works: [id], limit: 150 });
      fres.innerHTML = rows.length ? kwicTable(rows) : `<p class="fine">No occurrence in this work.</p>`;
    }, 220);
  }
}

/* ============================================================= LETTERS */
function viewLetters(args) {
  if (args && args[0]) return letterDetail(+args[0]);
  const L = D.letters;
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">Public domain · full text</span>
      <h1>Letters and Instructions, 1524–1547</h1>
      <p class="lede">Twenty-four letters in D. F. O'Leary's 1914 translation, from the convalescent's first
      surviving note to Inés Pascual through the long instruction to the community at Coimbra. Read them here
      in full; they are also part of every search and every dialogue on this site.</p>
    </div>
    <div class="grid g2" style="margin-bottom:1.6rem">
      <div class="chartbox"><span class="tag">Correspondence over time</span>
        <canvas id="tl" style="height:150px;margin-top:.5rem"></canvas>
        <p class="fine">Twelve of the twenty-four letters fall in the six years after the Society's approval.</p></div>
      <div class="chartbox"><span class="tag">Recipients by extent</span>
        <div style="max-height:220px;overflow:auto"><canvas id="rb"></canvas></div></div>
    </div>
    <div class="toolbar"><input class="grow" id="lq" type="search" placeholder="Search recipient, place or text …"></div>
    <div id="ll" class="grid g2"></div></div>`));

  const ll = view.querySelector("#ll");
  const draw = () => {
    const q = view.querySelector("#lq").value.toLowerCase().trim();
    ll.innerHTML = "";
    const rows = L.filter(l => !q ||
      (l.empfaenger + " " + l.ort + " " + l.datum + " " + l.text).toLowerCase().includes(q));
    for (const l of rows) {
      const card = el(`<div class="workcard" style="border-left:3px solid ${wc("letters")}">
        <div class="letterhead">
          <span class="cite">no. ${esc(l.roman)}</span>
          <strong style="font-family:var(--serif);font-size:1.05rem">To ${esc(l.empfaenger)}</strong></div>
        <p class="fine" style="margin:0">${esc([l.ort, l.datum].filter(Boolean).join(", ") || "place and date uncertain")}
          · pp. ${l.seite_von}–${l.seite_bis} · ${nf(l.tokens)} words</p>
        <p style="font-size:.9rem;color:var(--fg2);margin:.3rem 0 0">${esc(short(bodyOf(l), 210))}</p>
      </div>`);
      card.onclick = () => location.hash = `#/letters/${l.n}`;
      ll.append(card);
    }
    if (!rows.length) ll.append(el(`<p class="fine">Nothing matches.</p>`));
  };
  view.querySelector("#lq").oninput = debounce(draw, 180);
  draw();

  requestAnimationFrame(() => {
    const years = {};
    L.forEach(l => { if (l.jahr) years[l.jahr] = (years[l.jahr] || 0) + 1; });
    V.timeline(view.querySelector("#tl"),
      Object.entries(years).map(([y, v]) => [+y, v]), { h: 150, from: 1524, to: 1548 });
    V.bars(view.querySelector("#rb"),
      L.slice().sort((a, b) => b.tokens - a.tokens).map(l =>
        ({ label: `${l.roman} · ${short(l.empfaenger, 22)}`, v: l.tokens, disp: nf(l.tokens), color: wc("letters") })),
      { padL: 175, rowH: 20 });
  });
}

/** Strip the heading lines from a letter body for previews. */
function bodyOf(l) {
  const lines = l.text.split("\n");
  let i = 0;
  while (i < lines.length && i < 6 &&
    (!lines[i].trim() || /^(TO|To)\b|^\s*(JHUS|JHS|IHS)\s*$|^[A-Z][A-Za-z'. ]+,\s/.test(lines[i].trim()))) i++;
  return lines.slice(i).join(" ").replace(/\s+/g, " ").trim();
}

function letterDetail(n) {
  const l = D.letters.find(x => x.n === n);
  if (!l) { location.hash = "#/letters"; return; }
  const i = D.letters.indexOf(l);
  const prev = D.letters[(i - 1 + D.letters.length) % D.letters.length];
  const next = D.letters[(i + 1) % D.letters.length];
  view.append(el(`<div>
    <p class="fine"><a href="#/letters">← All letters</a> ·
      <a href="#/letters/${prev.n}">no. ${esc(prev.roman)}</a> · <a href="#/letters/${next.n}">no. ${esc(next.roman)}</a></p>
    <div class="viewhead">
      <span class="tag">Letter no. ${esc(l.roman)} · ${esc([l.ort, l.datum].filter(Boolean).join(", "))}</span>
      <h1>To ${esc(l.empfaenger)}</h1>
      <p class="fine">Letters and Instructions, vol. I, pp. ${l.seite_von}–${l.seite_bis} ·
        trans. D. F. O'Leary, 1914 · public domain · ${nf(l.tokens)} words</p>
    </div>
    <div class="panel"><div class="lettertext">${esc(l.text)}</div></div>
    <p class="fine">Text as scanned from the 1914 edition; occasional artefacts of the optical character
    recognition remain and are left uncorrected rather than silently emended.</p>
  </div>`));
}

/* ========================================================= CONCORDANCE */
function viewConcordance() {
  const pre = new URLSearchParams((location.hash.split("?")[1] || "")).get("q") || "";
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">Cross-corpus concordance</span>
      <h1>Concordance</h1>
      <p class="lede">Keyword in context across every work currently available, each hit resolved to its
      canonical citation. The Letters are always searchable; the other five join the search as you open them.</p>
    </div>
    <div class="toolbar">
      <input class="grow" id="q" type="search" placeholder="Search word or phrase …" value="${esc(pre)}">
      <button class="primary" id="go">Search</button>
    </div>
    <div class="toolbar" id="wfilter" style="margin-top:-.5rem"></div>
    <div id="out"></div>
    <div class="card" style="margin-top:1.4rem"><span class="tag">Starting points</span>
      <p style="margin:.5rem 0 0">${["consolation", "desolation", "discern", "election", "indifferent",
        "obedience", "poverty", "tears", "glory of God", "charity", "conscience", "greater"]
        .map(t => `<button class="chip" data-t="${t}">${t}</button>`).join("")}</p></div>
  </div>`));

  const wf = view.querySelector("#wfilter");
  const sel = new Set(C.openIds());
  for (const w of D.works) {
    const on = C.isOpen(w.id);
    const b = el(`<button class="chip ${on && sel.has(w.id) ? "on" : ""}" data-w="${w.id}"
      ${on ? "" : "disabled title='not open on this device'"}>${esc(w.kurz)}</button>`);
    b.onclick = () => {
      if (!on) return;
      sel.has(w.id) ? sel.delete(w.id) : sel.add(w.id);
      b.classList.toggle("on"); run();
    };
    wf.append(b);
  }

  const out = view.querySelector("#out");
  function run() {
    const q = view.querySelector("#q").value.trim();
    out.innerHTML = "";
    if (q.length < 3) { out.append(el(`<p class="fine">Type at least three characters.</p>`)); return; }
    const works = [...sel];
    if (!works.length) { out.append(el(`<p class="fine">Select at least one work.</p>`)); return; }
    const rows = C.kwic(q, { works, limit: 600 });
    const counts = C.hitCounts(q);
    const coll = C.collocates(q, 5, 22);
    out.append(el(`<div class="grid g2" style="margin-bottom:1.1rem">
      <div class="card"><span class="tag">Distribution</span>
        <table style="font-size:.85rem;margin-top:.5rem">${D.works.map(w => `<tr>
          <td><span style="color:${wc(w.id)}">■</span> ${esc(w.kurz)}</td>
          <td class="num">${counts[w.id] === null ? '<span class="fine">locked</span>' : nf(counts[w.id])}</td>
          <td style="width:52%"><div style="height:8px;border-radius:4px;background:var(--panel2)">
            <div style="height:8px;border-radius:4px;background:${wc(w.id)};width:${
              counts[w.id] ? Math.round(100 * counts[w.id] / Math.max(1, ...Object.values(counts).filter(Boolean))) : 0}%"></div>
          </div></td></tr>`).join("")}</table></div>
      <div class="card"><span class="tag">Collocates (± 5 words)</span>
        <p style="margin:.5rem 0 0">${coll.map(([x, f]) =>
          `<button class="chip" data-t="${esc(x)}">${esc(x)} <span style="color:var(--fg3)">${f}</span></button>`).join("") || '<span class="fine">none</span>'}</p></div>
    </div>`));
    out.append(el(`<div class="scroll">${kwicTable(rows)}</div>`));
    out.append(el(`<p class="fine" style="margin-top:.7rem">${nf(rows.length)} lines shown${rows.length >= 600 ? " (capped)" : ""}.</p>`));
    if (D.works.some(w => !C.isOpen(w.id)))
      out.append(lockedBox("Works still locked are excluded from these counts. Opening them extends the concordance across the whole corpus."));
    out.querySelectorAll("[data-t]").forEach(b => b.onclick = () => {
      view.querySelector("#q").value = b.dataset.t; run();
    });
  }
  view.querySelector("#go").onclick = run;
  view.querySelector("#q").addEventListener("keydown", e => { if (e.key === "Enter") run(); });
  view.querySelectorAll("[data-t]").forEach(b => b.onclick = () => {
    view.querySelector("#q").value = b.dataset.t; run();
  });
  if (pre) run();
}

function kwicTable(rows) {
  return `<table class="kwic"><tbody>${rows.map(r => `<tr>
    <td class="l">…${esc(r.l)}</td><td class="k">${esc(r.k)}</td><td class="r">${esc(r.r)}…</td>
    <td class="ref">${citeChip(r.cite, r.work)}</td></tr>`).join("")}</tbody></table>`;
}

/* ============================================================= LEXICON */
function viewLexicon() {
  const fields = [...new Set(D.lexicon.map(x => x.field))].sort();
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">Discernment lexicon</span>
      <h1>How the vocabulary travels</h1>
      <p class="lede">Ignatius uses a small, hard-worked vocabulary, and it does different work in different
      genres: what the retreat manual introduces as an interior datum the journal records as an event, the
      directives turn into a question a director must ask, the Constitutions convert into a legal criterion,
      and the letters apply as administrative judgement. Each entry follows one term along that path.</p>
    </div>
    <div class="toolbar">
      <input class="grow" id="lq" type="search" placeholder="Search term or definition …">
      <span>${fields.map(f => `<button class="chip" data-f="${esc(f)}">${esc(f)}</button>`).join("")}</span>
    </div>
    <div id="lx"></div></div>`));
  let field = null;
  const box = view.querySelector("#lx");
  function draw() {
    const q = view.querySelector("#lq").value.toLowerCase().trim();
    box.innerHTML = "";
    const rows = D.lexicon.filter(x => (!field || x.field === field) &&
      (!q || (x.term + " " + x.definition + " " + (x.latin || "")).toLowerCase().includes(q)));
    for (const x of rows) {
      const dcount = (D.discernment.find(d => d.begriff.toLowerCase().includes(x.term.toLowerCase())) || {}).dist;
      box.append(el(`<div class="panel">
        <span class="tag">${esc(x.field)}</span>
        <h2 style="margin:.25rem 0 .1rem">${esc(x.term)}${x.latin ? ` <span class="fine" style="font-style:italic">${esc(x.latin)}</span>` : ""}</h2>
        <p class="readable">${esc(x.definition)}</p>
        <p class="trajectory">${esc(x.trajectory)}</p>
        <div class="grid g2" style="margin-top:.8rem">
          <div><span class="tag">Loci</span>
            <div style="margin-top:.45rem">${(x.loci || []).map(l =>
              `<span class="locus"><span class="cite">${esc(l.cite)}</span> ${esc(l.note)}</span>`).join("")}</div></div>
          <div><span class="tag">Related</span>
            <p style="margin:.45rem 0 .6rem">${(x.related || []).map(r =>
              `<button class="chip" data-jump="${esc(r)}">${esc(r)}</button>`).join("")}</p>
            <a class="btn" href="#/concordance?q=${encodeURIComponent(x.term.split(" ")[0])}">Concordance →</a>
          </div>
        </div></div>`));
    }
    if (!rows.length) box.append(el(`<p class="fine">Nothing matches.</p>`));
    box.querySelectorAll("[data-jump]").forEach(b => b.onclick = () => {
      view.querySelector("#lq").value = b.dataset.jump; field = null;
      view.querySelectorAll("[data-f]").forEach(x => x.classList.remove("on"));
      draw();
    });
  }
  view.querySelector("#lq").oninput = debounce(draw, 180);
  view.querySelectorAll("[data-f]").forEach(b => b.onclick = () => {
    field = field === b.dataset.f ? null : b.dataset.f;
    view.querySelectorAll("[data-f]").forEach(x => x.classList.toggle("on", x.dataset.f === field));
    draw();
  });
  draw();
}

/* =============================================================== ATLAS */
function viewAtlas() {
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">Concept atlas</span>
      <h1>What stands next to what</h1>
      <p class="lede">Two terms are joined when they occur in the same sentence more often than chance
      allows. Colour marks the work in which a term has its centre of gravity, so the seams between the
      retreat manual, the journal and the law become visible as regions of the graph.</p>
    </div>
    <div class="chartbox">
      <div class="toolbar" style="margin-bottom:.6rem">
        <label class="fld">Density<select id="dens" style="width:auto">
          <option value="60">sparse (60 terms)</option>
          <option value="100" selected>medium (100 terms)</option>
          <option value="160">dense (160 terms)</option>
          <option value="999">everything</option></select></label>
        <button id="reheat" class="ghost">re-arrange</button>
      </div>
      <canvas id="net" style="width:100%;height:560px"></canvas>
      <div class="legend" id="leg"></div>
    </div>
    <div class="grid g2" style="margin-top:1.1rem">
      <div class="panel" id="sel"><span class="tag">Selection</span>
        <p class="fine">Click a node for its neighbours and its distribution across the corpus.</p></div>
      <div class="panel"><span class="tag">Terms that bridge the genres</span>
        <p class="fine">Terms whose neighbours are spread across the largest number of works — the vocabulary
        that holds the corpus together rather than belonging to one genre.</p>
        <div id="bridges"></div></div>
    </div></div>`));

  view.querySelector("#leg").innerHTML = D.corpus.ids.map(id =>
    `<span><i style="background:${wc(id)}"></i>${esc(workOf(id).kurz)}</span>`).join("");

  const nb = new Map();
  for (const e of D.network.edges) {
    if (!nb.has(e.s)) nb.set(e.s, new Set()); if (!nb.has(e.t)) nb.set(e.t, new Set());
    nb.get(e.s).add(e.t); nb.get(e.t).add(e.s);
  }
  const wOf = new Map(D.network.nodes.map(n => [n.id, n.werk]));
  const bridges = [...nb.entries()].map(([id, s]) => ({
    id, span: new Set([...s].map(x => wOf.get(x))).size, deg: s.size,
  })).filter(b => b.deg >= 4).sort((a, b) => b.span - a.span || b.deg - a.deg).slice(0, 16);
  view.querySelector("#bridges").innerHTML = bridges.map(b =>
    `<button class="chip" data-n="${esc(b.id)}">${esc(b.id)} <span style="color:var(--fg3)">${b.span} works</span></button>`).join("");

  let net = null;
  function build() {
    const lim = +view.querySelector("#dens").value;
    const keep = new Set(D.network.nodes.slice().sort((a, b) => b.f - a.f).slice(0, lim).map(n => n.id));
    const data = {
      nodes: D.network.nodes.filter(n => keep.has(n.id)).map(n => ({ ...n, teil: n.werk })),
      edges: D.network.edges.filter(e => keep.has(e.s) && keep.has(e.t)),
    };
    if (net) net.stop();
    net = V.network(view.querySelector("#net"), data, { h: 560, onSelect: showNode, palette: WORKCOLOR });
  }
  view.querySelector("#dens").onchange = build;
  view.querySelector("#reheat").onclick = () => net && net.reheat();
  build();
  view.querySelectorAll("[data-n]").forEach(b => b.onclick = () => { net.select(b.dataset.n); showNode(b.dataset.n); });

  function showNode(id) {
    const box = view.querySelector("#sel");
    if (!id) { box.innerHTML = `<span class="tag">Selection</span><p class="fine">Click a node.</p>`; return; }
    const nbs = D.network.edges.filter(e => e.s === id || e.t === id)
      .map(e => ({ w: e.s === id ? e.t : e.s, f: e.f })).sort((a, b) => b.f - a.f).slice(0, 18);
    const prof = D.terms[id];
    box.innerHTML = `<span class="tag">Term</span><h3 style="margin:.2rem 0 .1rem">${esc(id)}</h3>
      <p class="fine">${prof ? nf(prof.f) + " occurrences · in " + prof.werke + " of 6 works" : ""}</p>
      ${prof ? `<table style="font-size:.82rem;margin:.4rem 0 .8rem">${D.corpus.ids.map((w, i) => `<tr>
        <td><span style="color:${wc(w)}">■</span> ${esc(workOf(w).kurz)}</td>
        <td class="num">${prof.dist[i]}</td></tr>`).join("")}</table>` : ""}
      <span class="tag">Strongest neighbours</span>
      <p style="margin:.4rem 0 .6rem">${nbs.map(n =>
        `<button class="chip" data-n2="${esc(n.w)}">${esc(n.w)}</button>`).join("")}</p>
      <a class="btn" href="#/concordance?q=${encodeURIComponent(id)}">Concordance →</a>`;
    box.querySelectorAll("[data-n2]").forEach(b => b.onclick = () => { net.select(b.dataset.n2); showNode(b.dataset.n2); });
  }
}

/* ============================================================ REGISTER */
function viewRegister() {
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">Registers</span>
      <h1>Persons, places, itinerary</h1>
      <p class="lede">Who and where the corpus names, and the route the memoir traces. Names are recognised
      automatically and normalised, so the register is a finding aid rather than a critical index.</p>
    </div>
    <div class="grid g2" style="margin-bottom:1.4rem">
      <div class="chartbox"><span class="tag">Persons named</span><canvas id="pb"></canvas></div>
      <div class="chartbox"><span class="tag">Places named</span><canvas id="qb"></canvas></div>
    </div>
    <div class="panel"><span class="tag">The pilgrim's route, as the memoir tells it</span>
      <div class="timeline" style="margin-top:1rem" id="itin"></div></div>
    <div class="panel"><span class="tag">Correspondence</span>
      <p class="fine">Recipients of the twenty-four surviving letters of 1524–1547, in order of date.</p>
      <div class="scroll" style="margin-top:.6rem"><table id="ct"></table></div></div>
    <div class="panel"><span class="tag">Full register</span>
      <div class="toolbar" style="margin:.6rem 0">
        <input class="grow" id="rq" type="search" placeholder="Search name …">
        <button class="chip on" data-k="persons">persons</button>
        <button class="chip" data-k="places">places</button>
      </div>
      <div class="scroll"><table id="rt"></table></div></div>
  </div>`));

  requestAnimationFrame(() => {
    V.bars(view.querySelector("#pb"), D.persons.slice(0, 18).map(p =>
      ({ label: p.name, v: p.f, disp: nf(p.f) })), { padL: 155 });
    V.bars(view.querySelector("#qb"), D.places.slice(0, 18).map(p =>
      ({ label: p.name, v: p.f, disp: nf(p.f), color: "#9db8a4" })), { padL: 155 });
  });

  view.querySelector("#itin").innerHTML = D.itinerary.map(([jahr, ort, was, a, b]) =>
    `<div class="tlitem"><div class="tlyear">${jahr}</div>
      <strong style="font-family:var(--serif);font-size:1.05rem">${esc(ort)}</strong>
      <div style="color:var(--fg2);font-size:.9rem">${esc(was)}</div>
      <div class="fine"><span class="cite">Autobiog. [${a}–${b}]</span></div></div>`).join("");

  view.querySelector("#ct").innerHTML =
    `<thead><tr><th>No.</th><th>Recipient</th><th>Place</th><th>Date</th><th class="num">Words</th></tr></thead>
     <tbody>${D.letters.slice().sort((a, b) => (a.jahr || 0) - (b.jahr || 0)).map(l => `<tr>
       <td><a href="#/letters/${l.n}">${esc(l.roman)}</a></td>
       <td>${esc(l.empfaenger)}</td><td>${esc(l.ort || "—")}</td><td>${esc(l.datum || "—")}</td>
       <td class="num">${nf(l.tokens)}</td></tr>`).join("")}</tbody>`;

  let kind = "persons";
  const rt = view.querySelector("#rt");
  function drawR() {
    const q = view.querySelector("#rq").value.toLowerCase().trim();
    const rows = D[kind].filter(r => !q || r.name.toLowerCase().includes(q));
    rt.innerHTML = `<thead><tr><th>Name</th><th class="num">Mentions</th>
      ${D.corpus.ids.map(i => `<th class="num">${esc(workOf(i).kurz)}</th>`).join("")}</tr></thead>
      <tbody>${rows.slice(0, 220).map(r => `<tr><td>${esc(r.name)}</td><td class="num">${r.f}</td>
        ${r.dist.map((v, i) => `<td class="num" style="color:${v ? wc(D.corpus.ids[i]) : "var(--fg3)"}">${v || "·"}</td>`).join("")}
      </tr>`).join("")}</tbody>`;
  }
  view.querySelector("#rq").oninput = debounce(drawR, 180);
  view.querySelectorAll("[data-k]").forEach(b => b.onclick = () => {
    kind = b.dataset.k;
    view.querySelectorAll("[data-k]").forEach(x => x.classList.toggle("on", x.dataset.k === kind));
    drawR();
  });
  drawR();
}

/* ============================================================ LANGUAGE */
function viewLanguage() {
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">Quantitative profile</span>
      <h1>Six genres, six registers</h1>
      <p class="lede">The corpus spans a terse instructional manual, a shorthand private journal, a memoir
      dictated aloud, a body of Latinate law and a set of letters written to be read out. Those differences
      show up in measurable form, and the measures are worth reading against the genres rather than as a
      ranking.</p>
    </div>
    <div class="grid g2">
      <div class="chartbox"><span class="tag">Works in a feature space</span>
        <div class="toolbar" style="margin:.6rem 0">
          <label class="fld">x<select id="xa">
            <option value="satzlaenge">mean sentence length</option><option value="lix">readability (LIX)</option>
            <option value="nominalquote">noun rate</option><option value="ttr">type–token ratio</option>
            <option value="wortlaenge">mean word length</option></select></label>
          <label class="fld">y<select id="ya">
            <option value="nominalquote">noun rate</option><option value="lix">readability (LIX)</option>
            <option value="satzlaenge">mean sentence length</option><option value="ttr">type–token ratio</option>
            <option value="wortlaenge">mean word length</option></select></label>
        </div>
        <canvas id="sc" style="height:340px"></canvas>
        <p class="fine" id="scinfo">Point size is extent; colour is the work.</p></div>
      <div class="chartbox"><span class="tag">Measure by measure</span>
        <div class="toolbar" style="margin:.6rem 0"><select id="metric" style="width:auto">
          <option value="lix">readability (LIX) — lower is more accessible</option>
          <option value="satzlaenge">mean sentence length</option>
          <option value="nominalquote">noun rate (%)</option>
          <option value="ttr">type–token ratio</option>
          <option value="hapax">hapax legomena</option>
          <option value="tokens">extent in tokens</option></select></div>
        <canvas id="mb"></canvas>
        <p class="fine" style="margin-top:.8rem">Type–token ratio falls with length by construction; the
        Constitutions are five times the size of any other work here, so their low value is an artefact
        of extent rather than evidence of a poorer vocabulary.</p></div>
    </div>
    <div class="panel" style="margin-top:1.2rem"><span class="tag">Table</span>
      <div class="scroll" style="margin-top:.6rem"><table id="tbl"></table></div></div>
    <div class="panel"><span class="tag">Keyness</span>
      <div class="toolbar" style="margin:.6rem 0"><select id="kk" style="width:auto">
        ${D.works.map(w => `<option value="${w.id}">${esc(w.titel)}</option>`).join("")}</select></div>
      <canvas id="kc"></canvas>
      <p class="fine">Log-likelihood of each lemma in the work against the rest of the corpus.
      Values above 15.13 correspond to p &lt; 0.0001 at one degree of freedom.</p></div>
  </div>`));

  const LBL = { satzlaenge: "mean sentence length (words)", lix: "readability (LIX)",
    nominalquote: "noun rate (%)", ttr: "type–token ratio", wortlaenge: "mean word length",
    hapax: "hapax legomena", tokens: "extent (tokens)" };
  const scv = view.querySelector("#sc");
  function drawScatter() {
    const xk = view.querySelector("#xa").value, yk = view.querySelector("#ya").value;
    const pts = D.works.map(w => ({ x: w[xk], y: w[yk], r: 5 + Math.sqrt(w.tokens) / 42, color: wc(w.id), w }));
    const hits = V.scatter(scv, pts, { h: 340, xLabel: LBL[xk], yLabel: LBL[yk],
      xDec: xk === "ttr" ? 3 : 1, yDec: yk === "ttr" ? 3 : 1 });
    scv.onmousemove = ev => {
      const r = scv.getBoundingClientRect();
      const h = hits.find(h => (h.x - (ev.clientX - r.left)) ** 2 + (h.y - (ev.clientY - r.top)) ** 2 < h.r ** 2);
      scv.style.cursor = h ? "pointer" : "default";
      view.querySelector("#scinfo").textContent = h
        ? `${h.d.w.titel} — ${LBL[xk]}: ${h.d.x}, ${LBL[yk]}: ${h.d.y}`
        : "Point size is extent; colour is the work.";
    };
    scv.onclick = ev => {
      const r = scv.getBoundingClientRect();
      const h = hits.find(h => (h.x - (ev.clientX - r.left)) ** 2 + (h.y - (ev.clientY - r.top)) ** 2 < h.r ** 2);
      if (h) location.hash = `#/works/${h.d.w.id}`;
    };
  }
  const drawMetric = () => {
    const m = view.querySelector("#metric").value;
    V.bars(view.querySelector("#mb"), D.works.slice().sort((a, b) => b[m] - a[m]).map(w =>
      ({ label: w.kurz, v: w[m], disp: m === "ttr" ? w[m].toFixed(3) : nf(w[m]), color: wc(w.id) })),
      { padL: 110, rowH: 26 });
  };
  const drawKey = () => {
    const id = view.querySelector("#kk").value;
    V.bars(view.querySelector("#kc"), (D.keyness[id] || []).slice(0, 24).map(k =>
      ({ label: k.w, v: k.ll, disp: `${k.f}× · LL ${k.ll}`, color: wc(id) })), { padL: 165 });
  };
  const COLS = [["kurz", "Work"], ["tokens", "Tokens"], ["saetze", "Sentences"], ["satzlaenge", "Ø sent."],
    ["wortlaenge", "Ø word"], ["nominalquote", "Noun %"], ["ttr", "TTR"], ["hapax", "Hapax"], ["lix", "LIX"]];
  let sk = "tokens", sd = -1;
  function drawTable() {
    const rows = D.works.slice().sort((a, b) =>
      (typeof a[sk] === "string" ? a[sk].localeCompare(b[sk]) : a[sk] - b[sk]) * sd);
    view.querySelector("#tbl").innerHTML =
      `<thead><tr>${COLS.map(([k, l]) => `<th data-k="${k}" class="${k === "kurz" ? "" : "num"}">${l}${sk === k ? (sd > 0 ? " ▲" : " ▼") : ""}</th>`).join("")}</tr></thead>
       <tbody>${rows.map(w => `<tr>
         <td><a href="#/works/${w.id}" style="color:${wc(w.id)}">${esc(w.kurz)}</a>
           <span class="fine"> ${esc(short(w.titel, 34))}</span></td>
         <td class="num">${nf(w.tokens)}</td><td class="num">${nf(w.saetze)}</td>
         <td class="num">${w.satzlaenge}</td><td class="num">${w.wortlaenge}</td>
         <td class="num">${w.nominalquote}</td><td class="num">${w.ttr}</td>
         <td class="num">${nf(w.hapax)}</td><td class="num">${w.lix}</td></tr>`).join("")}</tbody>`;
    view.querySelectorAll("#tbl th").forEach(th => th.onclick = () => {
      if (sk === th.dataset.k) sd = -sd; else { sk = th.dataset.k; sd = th.dataset.k === "kurz" ? 1 : -1; }
      drawTable();
    });
  }
  view.querySelector("#xa").onchange = drawScatter;
  view.querySelector("#ya").onchange = drawScatter;
  view.querySelector("#metric").onchange = drawMetric;
  view.querySelector("#kk").onchange = drawKey;
  drawTable();
  requestAnimationFrame(() => { drawScatter(); drawMetric(); drawKey(); });
}

/* ============================================================ GLOSSARY */
function viewGlossary() {
  const fields = [...new Set(D.glossary.map(g => g.field))].sort();
  view.append(el(`<div>
    <div class="viewhead">
      <span class="tag">Technical vocabulary</span>
      <h1>Glossary</h1>
      <p class="lede">Institutional, practical and philological terms a reader of this corpus runs into —
      distinct from the discernment lexicon, which traces the terms that do the argumentative work.</p>
    </div>
    <div class="toolbar"><input class="grow" id="gq" type="search" placeholder="Search …">
      <span>${fields.map(f => `<button class="chip" data-f="${esc(f)}">${esc(f)}</button>`).join("")}</span></div>
    <div class="grid g2" id="gl"></div></div>`));
  let field = null;
  const box = view.querySelector("#gl");
  function draw() {
    const q = view.querySelector("#gq").value.toLowerCase().trim();
    box.innerHTML = "";
    D.glossary.filter(g => (!field || g.field === field) &&
      (!q || (g.term + g.definition).toLowerCase().includes(q)))
      .sort((a, b) => a.term.localeCompare(b.term))
      .forEach(g => box.append(el(`<div class="card">
        <span class="tag">${esc(g.field)}</span>
        <h3 style="margin:.25rem 0 .4rem">${esc(g.term)}</h3>
        <p style="font-size:.91rem;color:var(--fg2)">${esc(g.definition)}</p>
        <p style="margin:.4rem 0 0">${(g.loci || []).map(l => `<span class="cite">${esc(l)}</span>`).join(" ")}</p>
      </div>`)));
  }
  view.querySelector("#gq").oninput = draw;
  view.querySelectorAll("[data-f]").forEach(b => b.onclick = () => {
    field = field === b.dataset.f ? null : b.dataset.f;
    view.querySelectorAll("[data-f]").forEach(x => x.classList.toggle("on", x.dataset.f === field));
    draw();
  });
  draw();
}

/* ============================================================== METHOD */
function viewMethod() {
  const k = D.corpus;
  view.append(el(`<div>
    <div class="viewhead"><span class="tag">Transparency</span>
      <h1>Method, sources and limits</h1>
      <p class="lede">What was computed, from what, with which tools, and where the results do not carry.</p></div>

    <div class="panel"><h2>Rights, and what follows from them</h2>
      <p class="readable">Ignatius died in 1556 and his writings are long out of copyright. The English
      translations that make them readable are not. Of the six editions used here, one — O'Leary's 1914
      <em>Letters and Instructions</em> — has fallen into the public domain and is therefore included complete.
      The other five are living scholarly translations under copyright, and this site ships none of their
      running text: only page-level citation anchors, aggregate counts, co-occurrence edges, name registers,
      and editorial matter written for this site. Their full-text functions run against a copy the reader
      supplies, which is read in the browser and stored on the reader's own device.</p>
    </div>

    <div class="panel"><h2>Extraction and segmentation</h2>
      <p class="readable">Text was taken from the PDF text layer. Ligatures were normalised, end-of-line
      hyphenation resolved, running heads and folios stripped before counting, and publisher apparatus —
      introductions, endnotes, indexes — excluded from the body used for statistics, so that the measures
      describe Ignatius's text rather than his modern editors'.</p>
      <p class="readable">Two editions needed specific handling. The Constitutions volume is typeset so that
      ordinary extraction breaks words apart at kerning boundaries — some twenty thousand stray fragments;
      re-extraction in raw mode reduces this to a residue of legitimate abbreviations. The Munitiz Diary
      encodes the digraphs <span class="mono">tt</span> and <span class="mono">ft</span> through substitute
      glyphs, which are restored before analysis.</p>
    </div>

    <div class="panel"><h2>Canonical anchors</h2>
      <p class="readable">Scholarship on this corpus cites paragraph numbers, not pages, because the numbering
      is stable across editions and translations while pagination is not. ${nf(k.anker)} anchors were recovered
      by locating each canonical number at the start of its line — in the Exercises and the Diary in braces, in
      the Constitutions, the memoir and the directives in brackets — which distinguishes a paragraph marker from
      a cross-reference or a footnote sign in running text.</p>
      <table style="font-size:.86rem;max-width:520px">
        ${D.works.filter(w => w.maxn).map(w => `<tr><td>${esc(w.titel)}</td>
          <td class="num">${nf(w.anker)} of ${nf(w.maxn)}</td>
          <td class="num">${Math.round(100 * w.anker / w.maxn)} %</td></tr>`).join("")}
      </table>
      <p class="fine" style="margin-top:.7rem">A search hit is reported at the nearest preceding anchor on
      its page. That is the honest resolution: it locates the passage at paragraph granularity without
      pretending to a precision the page-level index does not have.</p>
    </div>

    <div class="panel"><h2>Measures</h2>
      <ul style="color:var(--fg2);font-size:.93rem">
        <li>Lemmatisation, part-of-speech tagging and named-entity recognition with spaCy
          (<span class="mono">en_core_web_sm</span>). Content words only: nouns, proper nouns, adjectives, verbs.</li>
        <li><strong>Keyness</strong>: log-likelihood of a lemma in one work against the remaining five, for
          positively deviating lemmas occurring at least four times.</li>
        <li><strong>Co-occurrence</strong>: two terms in the same sentence, weighted by pointwise mutual
          information; edges shown from five shared sentences upward.</li>
        <li><strong>Retrieval</strong> in the dialogue: Okapi BM25 (k₁ = 1.4, b = 0.72) over passages of about
          950 characters, at most four passages per work so that no single text dominates an answer.</li>
        <li><strong>LIX</strong>: mean sentence length plus the share of words over six characters.</li>
      </ul>
    </div>

    <div class="panel"><h2>Known limits</h2>
      <ul style="color:var(--fg2);font-size:.93rem">
        <li>The 1914 Letters are an optical scan. Its errors — a stray glyph, a broken word, a mangled date —
          are left visible rather than silently emended, because a silent emendation in a research tool is worse
          than a visible flaw.</li>
        <li>Name recognition is automatic. It over-recognises liturgical and formulaic capitalisation and
          under-recognises Spanish and Basque names; the register is a finding aid, not a critical index.</li>
        <li>The Complementary Norms are printed alongside the Constitutions in the 1996 volume and are not
          separated out as an independent citation series here.</li>
        <li>Type–token ratio is length-dependent and should not be compared across works of very different
          extent without correction.</li>
        <li>The itinerary follows the memoir's own account, which is a narrative composed thirty years after
          the events and shaped for a purpose; it is not a reconstruction from archival sources.</li>
      </ul>
    </div>
  </div>`));
}

/* ============================================================ PRIVACY */
function viewPrivacy() {
  view.append(el(`<div>
    <div class="viewhead"><span class="tag">Privacy</span>
      <h1>Privacy notice</h1>
      <p class="lede">What this site does with data, stated at the level of detail at which it is
      actually true. Every claim below describes code you can read in this page's source.</p></div>

    <div class="panel"><h2>Who is responsible</h2>
      <p class="readable">This site is operated by a private individual from the United States; the
      details are in the <a href="#/imprint">legal notice</a>. It is a personal research project,
      not operated on behalf of any institution, employer, publisher or religious order, and no data
      from it is passed to one.</p>
      <p class="readable">Because the site is reachable from the European Economic Area, this notice is
      written to satisfy the General Data Protection Regulation as well as United States law. Where the
      GDPR applies to a reader, the operator is the controller within the meaning of Article 4(7).</p>
    </div>

    <div class="panel"><h2>What this site is, technically</h2>
      <p class="readable">A set of static files with one server function. There are no user accounts, no
      login, no contact form and no newsletter. The site sets <strong>no cookies whatsoever</strong> and
      uses no analytics, tag manager, advertising, A/B-testing or session-recording service. It loads
      <strong>nothing from third-party servers</strong>: the two libraries it uses — pdf.js for reading
      PDFs and jsPDF for exporting them — are served from this site itself, as are all fonts and data
      files. Opening any page of this site therefore contacts exactly one host: the one in your address
      bar.</p>
    </div>

    <div class="panel"><h2>Server logs</h2>
      <p class="readable">The site is hosted by Netlify. Like any web server, Netlify's infrastructure
      records the requests it serves — typically IP address, timestamp, the URL requested, HTTP status,
      the amount of data transferred, and the browser's user-agent and referrer strings. This is technically
      unavoidable in delivering a website and is the only server-side collection that takes place. It is
      used to operate and secure the service, not to build profiles, and the operator of this site does not
      analyse it. Where the GDPR applies, the legal basis is Article 6(1)(f): the legitimate interest in
      delivering a functioning, secure website. Retention follows Netlify's own periods.</p>
      <p class="readable">The site is operated and hosted in the United States. For readers in the European
      Economic Area this means their request data are processed outside the EEA, by the operator and by
      Netlify Inc. as hosting provider.</p>
    </div>

    <div class="panel"><h2>Text stored on your own device</h2>
      <p class="readable">Five of the six translations are in copyright and are not shipped with this site.
      Their full-text functions work only on a copy you open yourself. When you do, the following happens
      entirely inside your browser: pdf.js reads the file's text layer, the site identifies which of the six
      works it is, and it stores the extracted text — together with the file name and the time you opened it
      — in your browser's own <strong>IndexedDB</strong> database, named <span class="mono">ignatiana</span>.</p>
      <p class="readable">Three things follow, and they are worth being exact about. The PDF itself is never
      uploaded, and neither is the extracted text: it is written to your device, not to any server. But this
      storage is <strong>persistent</strong> — it survives closing the tab, closing the browser and restarting
      the computer, and it will still be there on your next visit. And it is stored unencrypted, like all
      browser storage, so on a shared or public machine another person with access to that browser profile
      could read it.</p>
      <p class="readable">You can delete it at any time. Open the button in the top right: the status table
      offers <em>Remove</em> for a single work, and <em>Clear all stored text</em> empties the database
      entirely. Clearing site data for this domain in your browser settings has the same effect. Nothing on
      the server is affected, because nothing was ever there.</p>
    </div>

    <div class="panel"><h2>The dialogue module — what actually leaves your device</h2>
      <p class="readable">Everything else on this site runs locally. The dialogue is the one function that
      sends data outward, and it does so only when you submit a question. What is sent is precisely this:</p>
      <ul style="color:var(--fg2);font-size:.93rem">
        <li>your question, truncated at 4,000 characters;</li>
        <li>at most twenty passages retrieved for that question, each truncated at 2,600 characters,
          together with their citation labels and edition details;</li>
        <li>at most the last six turns of the current dialogue, each truncated at 1,600 characters, so that
          follow-up questions make sense.</li>
      </ul>
      <p class="readable">The whole book is never transmitted, and no work is transmitted merely because you
      have opened it — only the passages the retrieval step selects for the question in front of you. Where
      those passages come from a copy you opened yourself, text from your own file does leave your device at
      that moment. That is inherent to asking a question about it, and it is worth knowing before you ask.</p>
      <p class="readable">The request goes to Anthropic's language model through Netlify's AI Gateway, which
      means two recipients: Netlify Inc. and Anthropic PBC, both in the United States. The answer is returned
      to your browser and is not written to any storage by this site — the server function keeps no log, no
      database and no copy, and its responses carry
      <span class="mono">cache-control: no-store</span>. Where the GDPR applies, the legal basis is
      Article 6(1)(b) and (f): performing the function you asked for. If you would rather send nothing at all,
      use the concordance, lexicon and citation tools instead — they never leave your browser.</p>
      <p class="readable">Do not paste personal information, confidential material or anything concerning
      identifiable third parties into the question field. Nothing in this site's design requires it, and the
      operator has no way to retrieve or delete it once sent.</p>
    </div>

    <div class="panel"><h2>What this site does not do</h2>
      <ul style="color:var(--fg2);font-size:.93rem">
        <li>No cookies, no local or session storage, no fingerprinting, no pixels, no beacons.</li>
        <li>No analytics of any kind, first-party or third-party.</li>
        <li>No profiles, no automated decision-making, no advertising.</li>
        <li>No sale of personal information, and no sharing of it for cross-context behavioural advertising.</li>
        <li>No third-party requests at all — nothing is loaded from any other host.</li>
      </ul>
    </div>

    <div class="panel"><h2>Rights of readers in the European Economic Area</h2>
      <p class="readable">Where the GDPR applies, you have the right of access (Art. 15), rectification
      (Art. 16), erasure (Art. 17), restriction of processing (Art. 18), data portability (Art. 20), and the
      right to object to processing based on legitimate interests (Art. 21). Requests go to the address in the
      <a href="#/imprint">legal notice</a>. You also have the right to lodge a complaint with a supervisory
      authority under Article 77.</p>
      <p class="readable">In practice the answer to most such requests is short, because there is little to
      answer with: apart from the server logs described above, this site holds nothing about you. The text
      from your own copy is under your control, on your own device, and is deleted with one button.</p>
      <p class="readable">No representative in the Union has been designated under Article 27. The operator
      relies on the exemption in Article 27(2)(a): the processing here is occasional, involves no large-scale
      processing of special categories of data, and is unlikely to result in a risk to the rights and freedoms
      of natural persons. If that assessment ever ceases to hold, a representative will be designated and named
      here.</p>
    </div>

    <div class="panel"><h2>Notice for California residents</h2>
      <p class="readable">This section is provided under the California Online Privacy Protection Act
      (CalOPPA, Cal. Bus. &amp; Prof. Code §§ 22575–22579).</p>
      <p class="readable"><strong>Categories of personally identifiable information collected.</strong>
      Internet or other network activity information, in the form of the server request logs described above
      (including IP address, browser type and pages requested). No name, postal address, email address,
      telephone number, social security number or physical characteristics are collected, because the site
      has no field in which to enter them. Text you submit in the dialogue is transmitted to the model
      provider to produce an answer and is not retained by this site.</p>
      <p class="readable"><strong>Third parties with whom information is shared.</strong> The hosting
      provider (Netlify Inc.) and, for dialogue requests only, the model provider (Anthropic PBC). No
      information is sold, rented or shared for marketing purposes.</p>
      <p class="readable"><strong>Review and change of information.</strong> The site maintains no user
      accounts or stored profiles, so there is no record to review or amend. Text held on your own device can
      be deleted at any time with <em>Remove</em> or <em>Clear all stored text</em>.</p>
      <p class="readable"><strong>Do Not Track.</strong> This site does not track its visitors over time or
      across third-party websites, and it therefore does not change its behaviour in response to a Do Not
      Track signal — there is no tracking to switch off. No third parties collect personally identifiable
      information about visitors' online activities on this site, because no third-party content is loaded
      at all.</p>
      <p class="readable"><strong>Changes to this notice.</strong> Material changes will be posted on this
      page with a revised effective date below. The site has no mailing list through which to notify you
      individually.</p>
    </div>

    <div class="panel"><h2>Children</h2>
      <p class="readable">This is a scholarly research instrument addressed to adult readers. It is not
      directed to children, and it knowingly collects no information from them.</p>
    </div>

    <div class="panel"><h2>Changes</h2>
      <p class="readable">Effective 15 August 2026. Where this notice and the site's behaviour ever diverge,
      the notice is wrong and will be corrected — the description is meant to follow the code, not the other
      way round.</p>
    </div>
  </div>`));
}

/* ============================================================ IMPRINT */
function viewImprint() {
  view.append(el(`<div>
    <div class="viewhead"><span class="tag">Legal notice</span>
      <h1>Legal notice</h1>
      <p class="lede">Who operates this site, and how to reach them.</p></div>

    <div class="panel"><h2>Operator</h2>
      <p class="readable">
        Dr. Pantaleon Fassbender<br>
        16751 NE 5th Street<br>
        Williston, FL 32696<br>
        United States
      </p>
      <p class="readable">Email: <a href="mailto:pantaleonfassbender@gmail.com">pantaleonfassbender@gmail.com</a></p>
      <p class="readable">This site is a personal research project, operated and hosted in the United States
      by a private individual, and not on behalf of any institution, employer, publisher or religious order.
      There is no company behind it, and it carries no advertising and no sponsorship.</p>
      <p class="readable">Responsible for the content of this site: Dr. Pantaleon Fassbender, at the address
      above. How data are handled is set out separately in the <a href="#/privacy">privacy notice</a>.</p>
    </div>

    <div class="panel"><h2>Rights in the texts</h2>
      <p class="readable">The writings of Ignatius of Loyola are long out of copyright. The modern
      translations are not, and this site ships the running text of one public-domain edition only; for the
      rest it holds derived data and editorial matter written for this site. The full account is in
      <a href="#/method">Method, sources and limits</a>. All rights in the modern translations rest with
      their publishers and translators. If you hold rights in one of these editions and consider anything
      here to exceed what derived data and scholarly citation permit, write to the address above and it will
      be dealt with promptly.</p>
    </div>

    <div class="panel"><h2>Liability for links</h2>
      <p class="readable">This site links to a small number of external resources. Their content is the
      responsibility of their respective operators. They were checked when the link was set; continuous
      monitoring without concrete evidence of a problem is not practicable, and any link will be removed
      promptly if such evidence appears.</p>
    </div>

    <div class="panel"><h2>No warranty</h2>
      <p class="readable">This is a research instrument offered free of charge and without warranty of any
      kind. Its measures, registers and generated answers can be wrong; the limits are set out at length under
      <a href="#/method">Method, sources and limits</a>, and they are part of the tool rather than a
      disclaimer appended to it. Verify anything you intend to publish against the printed editions.</p>
    </div>
  </div>`));
}

/* ========================================================== UNLOCKING */
const modal = document.getElementById("unlockModal");
function openUnlock() { modal.hidden = false; drawUnlockTable(); }
function closeUnlock() { modal.hidden = true; }
document.getElementById("unlockBtn").onclick = openUnlock;
document.getElementById("closeUnlock").onclick = closeUnlock;
modal.addEventListener("click", e => { if (e.target === modal) closeUnlock(); });

const input = document.getElementById("pdfInput");
const drop = document.getElementById("drop");
drop.addEventListener("dragover", e => { e.preventDefault(); drop.classList.add("over"); });
drop.addEventListener("dragleave", () => drop.classList.remove("over"));
drop.addEventListener("drop", e => {
  e.preventDefault(); drop.classList.remove("over");
  handleFiles([...e.dataTransfer.files]);
});
input.onchange = () => handleFiles([...input.files]);

/* PDFs whose title page did not identify one work beyond doubt. They are kept
   in memory with their text already read, so that answering the question costs
   nothing further. */
let offen = [];

function seitenHinweis(id, n) {
  const w = workOf(id);
  return n === w.pdf_seiten ? "pagination matches the reference edition"
    : `the reference edition has ${nf(w.pdf_seiten)} pages and this file has ${nf(n)}, so canonical citations may be offset`;
}

/** Install already-read pages under a work, refusing to displace a different
    file without saying so. */
async function oeffnen(id, pages, filename, meldungen) {
  const vorher = corpus.works[id];
  const meta = await C.install(id, pages, filename);
  const w = workOf(id);
  if (vorher && vorher.meta.quelle !== filename)
    meldungen.push(`<span style="color:var(--warn)">${esc(w.titel)} was already open from ${esc(vorher.meta.quelle)}; ${esc(filename)} has replaced it.</span>`);
  meldungen.push(`<span style="color:var(--ok)">${esc(w.titel)} — ${nf(pages.length)} pages read, ${esc(seitenHinweis(id, meta.n))}.</span>`);
}

/**
 * @param files    PDFs to read.
 * @param zielId   Work the reader has named explicitly; skips identification.
 */
async function handleFiles(files, zielId = null) {
  const st = document.getElementById("unlockState");
  const prog = document.getElementById("unlockProgress");
  const fill = document.getElementById("barFill");
  const ptxt = document.getElementById("progressText");
  const done = [];
  for (const file of files) {
    if (file.type && file.type !== "application/pdf") continue;
    st.className = "statebox"; st.textContent = "";
    prog.hidden = false; fill.style.width = "0%";
    ptxt.textContent = `Opening ${file.name} …`;
    try {
      const pages = await C.readPdf(file, (i, n) => {
        fill.style.width = (i / n * 100).toFixed(1) + "%";
        ptxt.textContent = `${file.name} — page ${i} of ${n}`;
      });
      const urteil = C.identify(pages);
      if (zielId) {
        // The reader's own assignment stands, but a title page that says
        // otherwise is worth reporting.
        if (urteil.id && urteil.id !== zielId)
          done.push(`<span style="color:var(--warn)">${esc(file.name)} reads like ${esc(workOf(urteil.id).titel)}, but it has been opened as ${esc(workOf(zielId).titel)} as you asked.</span>`);
        await oeffnen(zielId, pages, file.name, done);
      } else if (urteil.id) {
        await oeffnen(urteil.id, pages, file.name, done);
      } else {
        // Nothing won clearly. Rather than file the book under whichever title
        // happened to score first, ask.
        offen.push({ name: file.name, pages, ranked: urteil.ranked });
        done.push(`<span style="color:var(--warn)">${esc(file.name)}: the title page does not identify one of the six works beyond doubt. Choose below — the file has been read already.</span>`);
      }
    } catch (e) {
      done.push(`<span style="color:var(--warn)">${esc(file.name)}: ${esc(e.message || String(e))}</span>`);
    }
  }
  prog.hidden = true;
  st.className = "statebox";
  st.innerHTML = done.join("<br>") || "Nothing to read.";
  drawChoices(st);
  refreshUnlockBadge(); refreshUnlockCard(); drawUnlockTable(); route();
}

/** One row per unidentified PDF: the ranking this site arrived at, and the last
    word left to the reader. */
function drawChoices(st) {
  offen.forEach(f => {
    const beste = (f.ranked.find(r => r.score > 0) || {}).id;
    const box = el(`<div class="choose">
      <span class="fine">${esc(f.name)} — ${nf(f.pages.length)} pages. Open as:</span>
      <select>${D.works.filter(w => w.rechte !== "public-domain").map(w =>
        `<option value="${w.id}"${beste === w.id ? " selected" : ""}>${esc(w.titel)} (${nf(w.pdf_seiten)} pp.)</option>`).join("")}</select>
      <button class="primary">Open</button>
      <button class="ghost">Discard</button>
    </div>`);
    const sel = box.querySelector("select");
    const [ok, weg] = box.querySelectorAll("button");
    ok.onclick = async () => {
      const done = [];
      await oeffnen(sel.value, f.pages, f.name, done);
      offen = offen.filter(x => x !== f);
      st.innerHTML = done.join("<br>");
      drawChoices(st);
      refreshUnlockBadge(); refreshUnlockCard(); drawUnlockTable(); route();
    };
    weg.onclick = () => { offen = offen.filter(x => x !== f); box.remove(); };
    st.append(box);
  });
}

document.getElementById("forgetBtn").onclick = async () => {
  await C.forgetAll();
  offen = [];
  document.getElementById("unlockState").className = "statebox";
  document.getElementById("unlockState").textContent = "All locally stored text removed.";
  refreshUnlockBadge(); refreshUnlockCard(); drawUnlockTable(); route();
};

function drawUnlockTable() {
  const t = document.getElementById("unlockTable");
  if (!t || !D.works) return;
  t.innerHTML = D.works.map(w => {
    const open = C.isOpen(w.id);
    const rec = corpus.works[w.id];
    const quelle = rec
      ? `${nf(rec.meta.n)} pp. · ${esc(rec.meta.quelle)}${rec.meta.seitenOk ? ""
          : `<div class="fine" style="color:var(--warn)">expects ${nf(w.pdf_seiten)} pp. — check that this is the right volume</div>`}`
      : w.rechte === "public-domain" ? "shipped with this site" : `expects ${nf(w.pdf_seiten)} pp.`;
    return `<tr><td style="color:${wc(w.id)}">■</td>
      <td>${esc(w.titel)}<div class="fine">${esc(w.uebersetzer)}, ${w.jahr}</div></td>
      <td>${w.rechte === "public-domain" ? '<span class="rights pd">included</span>'
        : open ? '<span class="rights open">open</span>' : '<span class="rights cr">locked</span>'}</td>
      <td class="fine">${quelle}</td>
      <td class="rowact">${w.rechte === "public-domain" ? "" :
        `<label class="mini">${rec ? "Replace" : "Choose file"}
           <input type="file" accept="application/pdf" data-open="${w.id}" hidden></label>
         ${rec ? `<button class="mini" data-forget="${w.id}">Remove</button>` : ""}`}</td></tr>`;
  }).join("");
  t.querySelectorAll("[data-open]").forEach(inp => inp.onchange = () => {
    const file = inp.files[0];
    inp.value = "";                    // so that the same file can be chosen twice
    if (file) handleFiles([file], inp.dataset.open);
  });
  t.querySelectorAll("[data-forget]").forEach(b => b.onclick = async () => {
    await C.forget(b.dataset.forget);
    refreshUnlockBadge(); refreshUnlockCard(); drawUnlockTable(); route();
  });
}
function refreshUnlockBadge() {
  const n = C.openIds().length;
  const b = document.getElementById("unlockBtn");
  b.classList.toggle("on", n > 1);
  document.getElementById("unlockLabel").textContent = `${n} of 6 open`;
}
function refreshUnlockCard() {
  const box = document.getElementById("unlockCardState");
  if (!box) return;
  const open = D.works.filter(w => w.rechte === "copyright" && C.isOpen(w.id));
  // A stored file whose extent is nowhere near the reference edition is usually
  // a volume filed under the wrong title, which leaves the right work locked.
  const fraglich = open.filter(w => {
    const rec = corpus.works[w.id];
    return rec && w.pdf_seiten && Math.abs(rec.meta.n - w.pdf_seiten) / w.pdf_seiten > 0.35;
  });
  box.innerHTML = (open.length
    ? `<p class="fine" style="color:var(--ok)">✓ open: ${open.map(w => esc(w.kurz)).join(", ")}
       — ${nf(corpus._chunks.length)} passages indexed.</p>`
    : `<p class="fine">None of the five opened yet.</p>`) +
    (fraglich.length
      ? `<p class="fine" style="color:var(--warn)">${fraglich.map(w =>
          `${esc(w.kurz)} holds ${nf(corpus.works[w.id].meta.n)} pages against the ${nf(w.pdf_seiten)} of the reference edition (${esc(corpus.works[w.id].meta.quelle)})`).join("; ")}
         — probably the wrong volume; remove it and open the works by name.</p>`
      : "");
}

boot();
