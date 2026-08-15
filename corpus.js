/* corpus.js — local full-text layer for the Ignatian corpus.

   The public-domain Letters (O'Leary 1914) ship with this site and are always
   available. The five in-copyright translations are opened from the user's own
   PDFs: pdf.js reads them in the browser, the text is kept in IndexedDB, and
   nothing is uploaded. Canonical citation anchors are shipped as derived data
   and apply directly, because the page indices refer to the same editions. */

const DB = "ignatiana", STORE = "text";

export const corpus = {
  works: {},        // id -> {pages:[], meta:{}}
  meta: null,       // works.json
  anchors: null,    // anchors.json
  letters: null,    // letters.json (public domain, always present)
  _idx: {},         // id -> Map token -> [pageIdx]
  _chunks: [],      // retrieval units across everything available
  _bm25: null,
};

/* ---------------------------------------------------------- IndexedDB */
function idb() {
  return new Promise((res, rej) => {
    const r = indexedDB.open(DB, 1);
    r.onupgradeneeded = () => r.result.createObjectStore(STORE);
    r.onsuccess = () => res(r.result);
    r.onerror = () => rej(r.error);
  });
}
const tx = (mode, fn) => idb().then(db => new Promise((res, rej) => {
  const st = db.transaction(STORE, mode).objectStore(STORE);
  const rq = fn(st);
  rq.onsuccess = () => res(rq.result); rq.onerror = () => rej(rq.error);
}));
const dbGet = k => tx("readonly", s => s.get(k)).catch(() => null);
const dbPut = (k, v) => tx("readwrite", s => s.put(v, k));
const dbDel = k => tx("readwrite", s => s.delete(k));
const dbKeys = () => tx("readonly", s => s.getAllKeys()).catch(() => []);

/* ---------------------------------------------------------- normalise */
const LIG = [[/ﬀ/g, "ff"], [/ﬁ/g, "fi"], [/ﬂ/g, "fl"], [/ﬃ/g, "ffi"], [/ﬄ/g, "ffl"],
  [/ﬅ/g, "ft"], [/ﬆ/g, "st"], [/­/g, ""], [/[‘’‚]/g, "'"], [/[“”„]/g, '"'], [/ /g, " "]];
export function normalize(s) {
  for (const [re, r] of LIG) s = s.replace(re, r);
  return s;
}
/* The Munitiz typesetting encodes tt and ft through substitute glyphs. */
function diaryFix(s) {
  return s.replace(/([a-z]);(?=[a-z])/g, "$1tt").replace(/([a-z]):(?=[a-z])/g, "$1ft");
}

const STOP = new Set(("the a an and or but of to in on at by for with from as is are was were be " +
  "been being it its this that these those he she they we you i his her their our your my me him " +
  "them us not no nor so such then than there here which who whom whose what when where while if " +
  "unless because shall should will would may might can could must let do does did done have has " +
  "had having more most much many other another same own also very just only even still yet upon " +
  "into unto out up down over under again further once all any both each few one two three thing " +
  "things way ways make made take taken give given go going come came say said see seen know " +
  "known think thought well good great little long new old ought thereof therein hereby").split(" "));

export function tokens(s) {
  return (s.toLowerCase().match(/[a-zà-ÿ][a-zà-ÿ0-9'\-]{1,}/g) || []);
}

/* ------------------------------------------------------- identification */
/* Every volume in this corpus speaks of the others. The Constitutions cite the
   Exercises on their first pages; Ganss's name stands in the front matter of
   three of the six editions, because the 1996 Constitutions print his
   translation; Palmer's directories are a book *about* the Exercises. Counting
   one or two shared phrases therefore cannot separate them, and where two works
   scored alike the earliest key won by accident of object order — which is how
   Padberg's Constitutions and Munitiz's Diary were read into the Exercises' slot
   and stayed locked.

   Identification is accordingly weighted. The title of an edition counts for
   more than a name, a name for more than an incidental keyword, phrases that
   belong to a different volume count against, and the page count of the
   reference edition corroborates or contradicts the whole. A work is installed
   only when one candidate wins by a clear margin; otherwise the caller receives
   the ranking and puts the choice to the reader. */
const CUES = {
  spex: {
    titel: [/spiritual\s+exercises\s+of\s+(?:saint|st\b\.?)\s+ignatius/i, /translation\s+and\s+commentary/i],
    namen: [/ganss/i],
    marken: [/principle\s+and\s+foundation/i, /rules?\s+for\s+the\s+discernment/i,
      /contemplation\s+to\s+attain\s+love/i, /two\s+standards/i],
    gegen: [/complementary\s+norms/i, /log-?\s?book/i, /pilgrim'?s\s+testament/i,
      /manuscript\s+director/i, /official\s+directory/i, /letters\s+and\s+instructions/i],
  },
  const: {
    titel: [/constitutions\s+of\s+the\s+society\s+of\s+jesus/i, /complementary\s+norms/i],
    namen: [/padberg/i],
    marken: [/general\s+examen/i, /formula\s+of\s+the\s+institute/i, /declarations/i, /general\s+congregation/i],
    gegen: [/log-?\s?book/i, /pilgrim'?s\s+testament/i, /manuscript\s+director/i, /letters\s+and\s+instructions/i],
  },
  auto: {
    titel: [/pilgrim'?s\s+testament/i, /memoirs?\s+of\s+(?:saint|st\b\.?)\s+ignatius/i],
    namen: [/divarkar/i, /c[aâ]mara/i],
    marken: [/the\s+pilgrim\b/i, /reminiscences/i, /acta\s+patris/i],
    gegen: [/complementary\s+norms/i, /log-?\s?book/i, /manuscript\s+director/i, /letters\s+and\s+instructions/i],
  },
  diary: {
    titel: [/discernment\s+log-?\s?book/i, /spiritual\s+diary/i],
    namen: [/munitiz/i],
    marken: [/deliberation\s+on\s+poverty/i, /i[nñ]igo\b/i, /loquela/i],
    gegen: [/complementary\s+norms/i, /pilgrim'?s\s+testament/i, /manuscript\s+director/i,
      /letters\s+and\s+instructions/i],
  },
  dir: {
    titel: [/on\s+giving\s+the\s+spiritual\s+exercises/i, /manuscript\s+director(?:ies|y)/i,
      /official\s+directory/i, /directives\s+concerning/i],
    namen: [/palmer/i],
    marken: [/directory\s+of\s+1599/i, /polanco/i, /early\s+jesuit/i],
    gegen: [/complementary\s+norms/i, /log-?\s?book/i, /pilgrim'?s\s+testament/i, /letters\s+and\s+instructions/i],
  },
  letters: {
    titel: [/letters\s+and\s+instructions/i],
    namen: [/o'?leary/i, /goodier/i],
    marken: [/manresa\s+press/i, /herder/i, /volume\s+i\b/i],
    gegen: [/complementary\s+norms/i, /log-?\s?book/i, /pilgrim'?s\s+testament/i, /manuscript\s+director/i],
  },
};

const GEWICHT = { titel: 4, namen: 2, marken: 1, gegen: -4 };
const MARKEN_MAX = 3;      // incidental keywords cannot carry an identification
const GEGEN_MAX = 2;       // nor can a citation of another volume sink it entirely
const MIN_SCORE = 6;       // a title plus one corroboration
const MIN_ABSTAND = 4;     // and a clear lead over the runner-up

/** The page count of the reference edition, as corroborating evidence. A
    divergent printing is only mildly discounted; a count that is nowhere near
    the edition tells decisively against the identification. */
function seitenIndiz(n, erwartet) {
  if (!erwartet || !n) return 0;
  const d = Math.abs(n - erwartet) / erwartet;
  if (d <= 0.02) return 4;
  if (d <= 0.10) return 2;
  if (d <= 0.35) return 0;
  return -3;
}

/** Rank all six works against a PDF's front matter and extent.
    Returns {id, sicher, score, ranked}; id is null when nothing wins clearly. */
export function identify(pages) {
  const probe = pages.slice(0, 18).join(" ").replace(/\s+/g, " ");
  const ranked = Object.entries(CUES).map(([id, c]) => {
    const hits = rxs => (rxs || []).filter(r => r.test(probe)).length;
    const titel = hits(c.titel), namen = hits(c.namen);
    const marken = Math.min(MARKEN_MAX, hits(c.marken));
    const gegen = Math.min(GEGEN_MAX, hits(c.gegen));
    const seiten = seitenIndiz(pages.length, (workMeta(id) || {}).pdf_seiten);
    return {
      id, titel, namen, marken, gegen, seiten,
      score: titel * GEWICHT.titel + namen * GEWICHT.namen + marken * GEWICHT.marken +
             gegen * GEWICHT.gegen + seiten,
    };
  }).sort((a, b) => b.score - a.score);
  const [best, next] = ranked;
  const sicher = best.score >= MIN_SCORE && best.score - (next ? next.score : 0) >= MIN_ABSTAND;
  return { id: sicher ? best.id : null, sicher, score: best.score, ranked };
}

/* ------------------------------------------------------------- pdf.js */
export async function readPdf(file, onProgress) {
  const pdfjs = await import("./vendor/pdf.min.mjs");
  pdfjs.GlobalWorkerOptions.workerSrc = "./vendor/pdf.worker.min.mjs";
  const doc = await pdfjs.getDocument({ data: await file.arrayBuffer() }).promise;
  const n = doc.numPages, pages = new Array(n);
  for (let i = 1; i <= n; i++) {
    const tc = await (await doc.getPage(i)).getTextContent();
    let last = null, out = "";
    for (const it of tc.items) {
      if (last !== null && Math.abs(it.transform[5] - last) > 2) out += "\n";
      out += it.str;
      if (it.hasEOL) out += "\n";
      last = it.transform[5];
    }
    pages[i - 1] = normalize(out)
      .replace(/([A-Za-z])-\n([a-z])/g, "$1$2")
      .replace(/[ \t]+/g, " ");
    if (onProgress && (i % 8 === 0 || i === n)) onProgress(i, n);
    if (i % 40 === 0) await new Promise(r => setTimeout(r, 0));
  }
  return pages;
}

/* ------------------------------------------------------------ install */
export async function install(id, pages, filename) {
  if (id === "diary") pages = pages.map(diaryFix);
  const meta = {
    id, n: pages.length, quelle: filename, geladen: new Date().toISOString(),
    seitenOk: pages.length === (workMeta(id) || {}).pdf_seiten,
  };
  corpus.works[id] = { pages, meta };
  await dbPut(id, { pages, meta });
  reindex();
  return meta;
}
/** Drop a single work, so that a PDF filed under the wrong title can be
    replaced without clearing everything else. */
export async function forget(id) {
  await dbDel(id);
  delete corpus.works[id];
  reindex();
}
export async function forgetAll() {
  for (const k of await dbKeys()) await dbDel(k);
  corpus.works = {};
  reindex();
}
export async function restore(meta, anchors, letters) {
  corpus.meta = meta; corpus.anchors = anchors; corpus.letters = letters;
  for (const k of await dbKeys()) {
    const rec = await dbGet(k);
    if (rec && rec.pages) corpus.works[k] = rec;
  }
  reindex();
}

export const workMeta = id => (corpus.meta || []).find(w => w.id === id);
export const isOpen = id => id === "letters" || !!corpus.works[id];
export const openIds = () => (corpus.meta || []).filter(w => isOpen(w.id)).map(w => w.id);

/* --------------------------------------------------------- page access */
/** True when a PDF page belongs to Ignatius's text rather than to the
    translator's introduction, endnotes or index. */
export function inBody(id, p) {
  if (id === "letters") return true;
  const w = workMeta(id);
  if (!w || w.body_von == null) return true;
  return p >= w.body_von && p <= w.body_bis;
}

export function pagesOf(id) {
  if (corpus.works[id]) return corpus.works[id].pages;
  if (id === "letters" && corpus.letters) {
    // the public-domain letters are held as discrete letters, not pages
    return corpus.letters.map(l => l.text);
  }
  return null;
}

/* ------------------------------------------------- canonical citation */
export function citeFor(id, page) {
  if (id === "letters") {
    const l = corpus.letters[page];
    return l ? { label: `Letters, no. ${l.roman}`, n: l.n, seite: l.seite_von } : null;
  }
  const rows = (corpus.anchors || {})[id];
  if (!rows || !rows.length) return null;
  let best = null;
  for (const r of rows) {
    if (r.p <= page && (!best || r.n > best.n || r.p > best.p)) {
      if (!best || r.p > best.p || (r.p === best.p && r.n > best.n)) best = r;
    }
  }
  if (!best) return null;
  const w = workMeta(id);
  // Scholarly convention cites all these works by bracketed paragraph number,
  // whatever typographic device the individual edition happens to print.
  const num = best.dok ? `Doc. ${best.dok} [${best.n}]` : `[${best.n}]`;
  return { label: `${w.zk || w.kurz}${best.dok ? "," : ""} ${num}`, n: best.n, dok: best.dok,
           seite: best.s ?? null, exact: best.p === page };
}

/* ------------------------------------------------------------- index */
export function reindex() {
  corpus._idx = {};
  corpus._chunks = [];
  for (const w of corpus.meta || []) {
    const pages = pagesOf(w.id);
    if (!pages) continue;
    const inv = new Map();
    pages.forEach((txt, p) => {
      if (!inBody(w.id, p)) return;
      for (const t of new Set(tokens(txt))) {
        if (t.length < 3) continue;
        let a = inv.get(t); if (!a) inv.set(t, (a = []));
        a.push(p);
      }
      const clean = txt.replace(/\s+/g, " ").trim();
      if (clean.length < 90) return;
      const sents = clean.split(/(?<=[.!?:])\s+/);
      let cur = "";
      for (const s of sents) {
        if ((cur + " " + s).length > 950 && cur.length > 220) {
          corpus._chunks.push({ work: w.id, page: p, text: cur.trim() });
          cur = s;
        } else cur += " " + s;
      }
      if (cur.trim().length > 140) corpus._chunks.push({ work: w.id, page: p, text: cur.trim() });
    });
    corpus._idx[w.id] = inv;
  }
  buildBm25();
}

function buildBm25() {
  const df = new Map(); let total = 0;
  const docs = corpus._chunks.map(c => {
    const tf = new Map();
    const tk = tokens(c.text).filter(t => t.length > 2 && !STOP.has(t));
    for (const t of tk) tf.set(t, (tf.get(t) || 0) + 1);
    for (const t of tf.keys()) df.set(t, (df.get(t) || 0) + 1);
    total += tk.length;
    return { tf, len: tk.length };
  });
  corpus._bm25 = { df, docs, avg: total / Math.max(1, docs.length), N: docs.length };
}

/* ------------------------------------------------------------ search */
function pagesWith(id, terms) {
  const inv = corpus._idx[id];
  if (!inv) return [];
  let cand = null;
  for (const t of terms) {
    const s = new Set(inv.get(t) || []);
    cand = cand === null ? s : new Set([...cand].filter(x => s.has(x)));
    if (!cand.size) break;
  }
  return [...(cand || [])].sort((a, b) => a - b);
}

const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/** Keyword-in-context across every open work. */
export function kwic(q, { win = 54, limit = 500, works = null } = {}) {
  const terms = tokens(q).filter(t => t.length > 2);
  if (!terms.length) return [];
  const rx = new RegExp("(" + q.trim().split(/\s+/).map(esc).join("\\s+") + ")", "gi");
  const out = [];
  for (const w of corpus.meta || []) {
    if (works && !works.includes(w.id)) continue;
    const pages = pagesOf(w.id);
    if (!pages) continue;
    for (const p of pagesWith(w.id, terms)) {
      const txt = pages[p].replace(/\s+/g, " ");
      rx.lastIndex = 0;
      let m;
      while ((m = rx.exec(txt))) {
        out.push({
          l: txt.slice(Math.max(0, m.index - win), m.index),
          k: m[0],
          r: txt.slice(m.index + m[0].length, m.index + m[0].length + win),
          work: w.id, page: p, cite: citeFor(w.id, p),
        });
        if (out.length >= limit) return out;
      }
    }
  }
  return out;
}

/** Hits per work, for distribution displays. */
export function hitCounts(q) {
  const terms = tokens(q).filter(t => t.length > 2);
  const res = {};
  for (const w of corpus.meta || []) {
    const pages = pagesOf(w.id);
    if (!pages) { res[w.id] = null; continue; }
    const rx = new RegExp(q.trim().split(/\s+/).map(esc).join("\\s+"), "gi");
    let n = 0;
    for (const p of pagesWith(w.id, terms)) {
      n += (pages[p].replace(/\s+/g, " ").match(rx) || []).length;
    }
    res[w.id] = n;
  }
  return res;
}

export function collocates(q, span = 5, top = 28) {
  const key = q.toLowerCase().trim();
  const terms = tokens(q).filter(t => t.length > 2);
  const cnt = new Map();
  for (const w of corpus.meta || []) {
    const pages = pagesOf(w.id);
    if (!pages) continue;
    for (const p of pagesWith(w.id, terms)) {
      const tk = tokens(pages[p]);
      for (let i = 0; i < tk.length; i++) {
        if (!tk[i].startsWith(key.split(" ")[0])) continue;
        for (let j = Math.max(0, i - span); j <= Math.min(tk.length - 1, i + span); j++) {
          if (j === i) continue;
          const x = tk[j];
          if (x.length < 4 || STOP.has(x) || x === key) continue;
          cnt.set(x, (cnt.get(x) || 0) + 1);
        }
      }
    }
  }
  return [...cnt.entries()].sort((a, b) => b[1] - a[1]).slice(0, top);
}

/** BM25 retrieval over everything currently available. */
export function retrieve(query, k = 8, works = null) {
  if (!corpus._bm25 || !corpus._chunks.length) return [];
  const { df, docs, avg, N } = corpus._bm25;
  const q = tokens(query).filter(t => t.length > 2 && !STOP.has(t));
  if (!q.length) return [];
  const k1 = 1.4, b = 0.72, scored = [];
  for (let i = 0; i < docs.length; i++) {
    if (works && !works.includes(corpus._chunks[i].work)) continue;
    const d = docs[i]; let s = 0;
    for (const t of q) {
      const f = d.tf.get(t); if (!f) continue;
      const n = df.get(t) || 0;
      s += Math.log(1 + (N - n + 0.5) / (n + 0.5)) *
           (f * (k1 + 1)) / (f + k1 * (1 - b + b * d.len / avg));
    }
    if (s > 0) scored.push([i, s]);
  }
  scored.sort((a, c) => c[1] - a[1]);
  const perWork = new Map(), out = [];
  for (const [i, s] of scored) {
    const c = corpus._chunks[i];
    const used = perWork.get(c.work) || 0;
    if (used >= 4) continue;
    perWork.set(c.work, used + 1);
    out.push({ ...c, score: +s.toFixed(2), cite: citeFor(c.work, c.page) });
    if (out.length >= k) break;
  }
  return out;
}
