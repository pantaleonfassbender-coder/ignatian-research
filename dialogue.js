/* dialogue.js — citation-bound questioning of the corpus. */
import * as C from "./corpus.js";
import { corpus } from "./corpus.js";
import { D, esc, nf, short, lockedBox, citeChip, wc, workOf, debounce } from "./app.js";

const session = [];

export function renderDialogue(view, args) {
  const pre = new URLSearchParams((location.hash.split("?")[1] || "")).get("q") || "";
  view.innerHTML = "";
  const wrap = document.createElement("div");
  wrap.innerHTML = `
  <div class="viewhead">
    <span class="tag">Citation-bound dialogue</span>
    <h1>Put a question to the corpus</h1>
    <p class="lede">Your question is first answered locally: a BM25 retrieval searches the works available on
    this device and selects the passages that bear on it. Only those passages are sent onward, and the model
    is instructed to answer from them alone and to attach a canonical citation to every claim it makes.</p>
  </div>
  <div class="chatwrap">
    <div>
      <div id="chatlog"></div>
      <div class="composer">
        <textarea id="q" rows="3" placeholder="e.g. What does Ignatius mean when he tells a director to ask about consolation and desolation?">${esc(pre)}</textarea>
        <button class="primary" id="send">Ask</button>
      </div>
      <p class="fine" style="margin-top:.5rem">Ctrl/⌘ + Enter sends. Answers are reconstructions from the
      retrieved passages; check the citations before quoting.</p>
    </div>
    <aside>
      <div class="card">
        <span class="tag">Scope</span>
        <div id="scope" style="margin-top:.5rem"></div>
        <hr style="margin:.9rem 0">
        <label class="fld">Passages per question
          <select id="topk"><option>6</option><option selected>8</option><option>12</option><option>16</option></select></label>
        <label class="fld" style="margin-top:.6rem">Register
          <select id="mode">
            <option value="scholarly" selected>scholarly — cautious, source-critical</option>
            <option value="synoptic">synoptic — compare the works against each other</option>
            <option value="philological">philological — attend to the wording and its translation</option>
          </select></label>
        <div id="modstate" style="margin-top:.8rem"></div>
      </div>
      <div class="card" style="margin-top:1rem">
        <span class="tag">Export</span>
        <p class="fine" style="margin:.5rem 0 .7rem">The session as a citable PDF, with the passages used and
        a full bibliographical apparatus.</p>
        <button id="pdfBtn" style="width:100%">Save session as PDF</button>
        <button id="clearBtn" class="ghost" style="width:100%;margin-top:.5rem">Clear session</button>
      </div>
      <div class="card" style="margin-top:1rem">
        <span class="tag">Suggestions</span><div id="sug" style="margin-top:.5rem"></div>
      </div>
    </aside>
  </div>`;
  view.append(wrap);

  const log = wrap.querySelector("#chatlog");
  const qf = wrap.querySelector("#q");
  const scope = wrap.querySelector("#scope");
  const chosen = new Set(C.openIds());

  function drawScope() {
    scope.innerHTML = "";
    for (const w of D.works) {
      const open = C.isOpen(w.id);
      const b = document.createElement("button");
      b.className = "chip" + (open && chosen.has(w.id) ? " on" : "");
      b.textContent = w.kurz;
      b.disabled = !open;
      if (!open) b.title = "not open on this device";
      b.onclick = () => {
        chosen.has(w.id) ? chosen.delete(w.id) : chosen.add(w.id);
        drawScope(); updateState();
      };
      scope.append(b);
    }
  }
  function updateState() {
    const box = wrap.querySelector("#modstate");
    const locked = D.works.filter(w => !C.isOpen(w.id));
    const n = corpus._chunks.filter(c => chosen.has(c.work)).length;
    box.innerHTML = `<p class="fine">${nf(n)} passages in scope across ${chosen.size} work${chosen.size === 1 ? "" : "s"}.</p>`;
    if (locked.length) {
      box.append(lockedBox(`${locked.length} work${locked.length === 1 ? " is" : "s are"} still locked and cannot be searched: ${locked.map(w => w.kurz).join(", ")}.`));
    }
  }
  drawScope(); updateState();

  const SUG = [
    "How do the Exercises and the Constitutions each define indifference?",
    "What does Ignatius tell a director to do when a retreatant is in desolation?",
    "Where does the requirement of an account of conscience come from?",
    "How is the greater glory of God used as a decision criterion?",
    "What role do tears play, and where are they recorded?",
    "How does Ignatius write to someone who is being tempted?",
  ];
  wrap.querySelector("#sug").innerHTML = SUG.map(s =>
    `<button class="chip" style="text-align:left;white-space:normal" data-s="${esc(s)}">${esc(s)}</button>`).join("");
  wrap.querySelectorAll("[data-s]").forEach(b => b.onclick = () => { qf.value = b.dataset.s; qf.focus(); });

  function draw() {
    log.innerHTML = "";
    if (!session.length) {
      log.innerHTML = `<div class="card"><p class="fine" style="margin:0">No question yet. Nothing of your
        own copies is ever uploaded — only the passages the local retrieval selects for the question you ask.</p></div>`;
      return;
    }
    for (const m of session) {
      const d = document.createElement("div");
      d.className = "msg " + (m.rolle === "user" ? "user" : "bot");
      d.innerHTML = `<div class="who">${m.rolle === "user" ? "Question" : "Corpus"} ·
        ${new Date(m.zeit).toLocaleTimeString("en-GB")}</div>
        <div class="body">${m.rolle === "user" ? esc(m.text) : renderAnswer(m.text)}</div>
        ${m.quellen && m.quellen.length ? `<div class="sources"><strong>Passages used</strong>
          <ol style="margin:.4rem 0 0;padding-left:1.2rem">${m.quellen.map(q => `<li>
            ${citeChip(q.cite, q.work)} <span style="color:${wc(q.work)}">■</span>
            ${esc(short(workOf(q.work).titel, 46))}${q.score ? ` <span class="fine">· ${q.score}</span>` : ""}</li>`).join("")}</ol></div>` : ""}`;
      log.append(d);
    }
    log.lastElementChild.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
  draw();

  async function ask() {
    const q = qf.value.trim();
    if (q.length < 5) return;
    if (!chosen.size) { updateState(); return; }
    session.push({ rolle: "user", text: q, zeit: Date.now() });
    qf.value = ""; draw();

    const busy = document.createElement("div");
    busy.className = "msg bot";
    busy.innerHTML = `<div class="who">Corpus</div><div class="body thinking">Retrieving passages …</div>`;
    log.append(busy);

    const k = +wrap.querySelector("#topk").value;
    const mode = wrap.querySelector("#mode").value;
    const hits = C.retrieve(q, k, [...chosen]);
    if (!hits.length) {
      busy.remove();
      session.push({ rolle: "bot", quellen: [], zeit: Date.now(),
        text: "Nothing in the works currently in scope bears on that question. Try other wording, widen the scope, or open a work that is still locked." });
      draw(); return;
    }
    const passagen = hits.map(h => ({
      work: h.work, werk_titel: workOf(h.work).titel, uebersetzer: workOf(h.work).uebersetzer,
      cite: h.cite, zitat: h.cite ? h.cite.label : `${workOf(h.work).kurz}, p. ${h.page}`,
      seite: h.cite ? h.cite.seite : null, text: h.text, score: h.score, page: h.page,
    }));
    busy.querySelector(".body").textContent = `${passagen.length} passages found — composing the answer …`;

    try {
      const r = await fetch("/.netlify/functions/dialogue", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ frage: q, modus: mode, passagen,
          verlauf: session.slice(-6).map(m => ({ rolle: m.rolle, text: m.text.slice(0, 1400) })) }),
      });
      const data = await r.json().catch(() => ({}));
      busy.remove();
      if (!r.ok || data.error) {
        session.push({ rolle: "bot", quellen: passagen, zeit: Date.now(),
          text: "**The answering service is unavailable.** " + (data.error || `HTTP ${r.status}`) +
            "\n\nThe passages the local retrieval found are listed below and remain usable — retrieval runs entirely in your browser." });
      } else {
        session.push({ rolle: "bot", text: data.antwort || "(empty answer)", quellen: passagen, zeit: Date.now() });
      }
    } catch (e) {
      busy.remove();
      session.push({ rolle: "bot", quellen: passagen, zeit: Date.now(),
        text: "**Network error.** " + (e.message || e) + "\n\nThe retrieved passages are listed below." });
    }
    draw();
  }

  wrap.querySelector("#send").onclick = ask;
  qf.addEventListener("keydown", e => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) { e.preventDefault(); ask(); }
  });
  wrap.querySelector("#clearBtn").onclick = () => { session.length = 0; draw(); };
  wrap.querySelector("#pdfBtn").onclick = exportPdf;
}

/* ------------------------------------------------------------- render */
function renderAnswer(md) {
  return esc(md)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/\[((?:SpEx|Const|Autobiog\.|Diary|Dir\.|Letters)[^\]]{0,28})\]/g,
      (m, c) => `<span class="cite">${c}</span>`)
    .split(/\n{2,}/).map(p => `<p>${p.replace(/\n/g, "<br>")}</p>`).join("");
}

/* ------------------------------------------------------------- export */
async function exportPdf() {
  if (!session.length) { alert("The session contains no questions yet."); return; }
  if (!window.jspdf) {
    await new Promise((res, rej) => {
      const s = document.createElement("script");
      s.src = "vendor/jspdf.umd.min.js"; s.onload = res; s.onerror = rej;
      document.head.append(s);
    });
  }
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: "mm", format: "a4" });
  const M = 20, W = 210 - 2 * M;
  let y = M;
  const now = new Date();
  const line = (t, { size = 10, style = "normal", color = [30, 30, 30], gap = 1.6, indent = 0 } = {}) => {
    doc.setFont("times", style); doc.setFontSize(size); doc.setTextColor(...color);
    for (const p of doc.splitTextToSize(t, W - indent)) {
      if (y > 275) { footer(); doc.addPage(); y = M; }
      doc.text(p, M + indent, y); y += size * 0.42 + gap;
    }
  };
  const rule = () => { if (y > 272) { footer(); doc.addPage(); y = M; } doc.setDrawColor(200); doc.line(M, y, M + W, y); y += 5; };
  const footer = () => {
    doc.setFont("times", "normal"); doc.setFontSize(7.5); doc.setTextColor(140);
    doc.text("Ignatiana · dialogue transcript", M, 288);
    doc.text(String(doc.getNumberOfPages()), M + W, 288, { align: "right" });
  };

  const nq = session.filter(m => m.rolle === "user").length;
  line("Dialogue transcript", { size: 17, style: "bold", gap: 2.4 });
  line("The writings of Ignatius of Loyola", { size: 11.5, style: "bold", color: [110, 88, 20], gap: 1.2 });
  line(`Session of ${now.toLocaleDateString("en-GB")}, ${now.toLocaleTimeString("en-GB")} · ${nq} question${nq === 1 ? "" : "s"}`,
    { size: 8.5, color: [110, 110, 110], gap: 3 });
  rule();

  const used = new Map();
  for (const m of session) {
    if (m.rolle === "user") {
      y += 2;
      line("Question", { size: 8, style: "bold", color: [140, 110, 30], gap: .8 });
      line(m.text, { size: 11, style: "bold", color: [25, 25, 25], gap: 2.4 });
    } else {
      line("Answer", { size: 8, style: "bold", color: [110, 110, 110], gap: .8 });
      for (const par of m.text.replace(/\*\*/g, "").replace(/\*/g, "").split(/\n{2,}/))
        line(par, { size: 10, gap: 1.9 });
      if (m.quellen && m.quellen.length) {
        y += 1;
        line("Passages used", { size: 8, style: "bold", color: [110, 110, 110], gap: .9 });
        m.quellen.forEach((q, i) => {
          const w = workOf(q.work);
          line(`${i + 1}. ${q.zitat}${q.seite ? `, p. ${q.seite}` : ""} — ${w.titel}`,
            { size: 8.5, color: [90, 90, 90], gap: .7, indent: 4 });
          used.set(q.work, w);
        });
      }
      y += 3; rule();
    }
  }

  if (used.size) {
    if (y > 232) { footer(); doc.addPage(); y = M; }
    y += 2;
    line("Editions cited", { size: 12, style: "bold", gap: 2.2 });
    for (const w of used.values()) {
      line(`${w.titel}. Translated by ${w.uebersetzer}. ${w.verlag}, ${w.jahr}. Cited as ${w.zitierweise}.${w.rechte === "public-domain" ? " Public domain." : ""}`,
        { size: 8.6, color: [70, 70, 70], gap: 1.5 });
    }
  }
  y += 4;
  line("Note: the answers above were composed by a language model from the passages listed, which were selected by a local retrieval over the reader's own copies. They do not replace the texts and must be verified against them before citation. Rights in the modern translations rest with their publishers and translators.",
    { size: 7.6, color: [140, 140, 140], gap: 1 });
  footer();
  doc.save(`Ignatiana-dialogue_${now.toISOString().slice(0, 10)}.pdf`);
}
