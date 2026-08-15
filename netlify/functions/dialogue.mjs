/* Netlify Function — citation-bound answering over the Ignatian corpus.
   Uses Netlify's AI Gateway: ANTHROPIC_API_KEY and ANTHROPIC_BASE_URL are
   injected automatically. Nothing is stored or logged. */

const MODEL = process.env.DIALOG_MODEL || "claude-sonnet-4-6";
const FALLBACK = ["claude-sonnet-4-5", "claude-3-7-sonnet-latest"];

const BASE = `You are a research instrument for the writings of Ignatius of Loyola (1491–1556), working over six texts: the Spiritual Exercises, the Constitutions of the Society of Jesus with their Complementary Norms, the dictated memoir known as A Pilgrim's Testament, the Spiritual Diary, the early Directives on giving the Exercises, and the letters of 1524–1547.

Binding rules:
1. Answer ONLY from the passages supplied. What is not in them, you do not assert — not even where you believe you know it. If the passages are thin, say so and name what is missing.
2. Attach a canonical citation to every substantive claim, in the exact form given with each passage: [SpEx {23}], [Const [134]], [Autobiog. [30]], [Diary {17}], [Dir., Doc. 1 [5]], [Letters, no. V]. Never invent a number.
3. Quote at most a short phrase — roughly a dozen words — and only inside quotation marks with a citation. Otherwise paraphrase. The translations are under copyright and must not be reproduced at length.
4. Distinguish what a text says from what it presupposes and from what later texts make of it. Where the works differ, set the difference out rather than harmonising it.
5. Remember the genres: the Exercises are instructions to a director, the Diary is private shorthand, the Constitutions are law, the letters are occasional and addressed to a particular person in a particular situation. A sentence does not mean the same thing in each.
6. Scholarly English. Two to five paragraphs. No devotional register, no exhortation, no invented biography.
7. Where it is useful, close with the passage a reader should go to next.`;

const MODES = {
  scholarly: "\n\nRegister: cautious and source-critical. Mark the limits of what the passages establish.",
  synoptic: "\n\nRegister: synoptic. Organise the answer around how the works differ from one another, and say which genre each difference belongs to.",
  philological: "\n\nRegister: philological. Attend to the wording, to the fact that you are reading a modern English translation, and to what the underlying Spanish or Latin term is likely to have been where that matters for the argument.",
};

export default async (req) => {
  if (req.method !== "POST") return json({ error: "POST only." }, 405);
  let body;
  try { body = await req.json(); } catch { return json({ error: "Malformed JSON." }, 400); }

  const frage = String(body.frage || "").slice(0, 4000).trim();
  const modus = MODES[body.modus] ? body.modus : "scholarly";
  const passagen = Array.isArray(body.passagen) ? body.passagen.slice(0, 20) : [];
  const verlauf = Array.isArray(body.verlauf) ? body.verlauf.slice(-6) : [];

  if (frage.length < 5) return json({ error: "Send a formulated question." }, 400);
  if (!passagen.length) return json({ error: "No passages supplied." }, 400);

  const key = process.env.ANTHROPIC_API_KEY;
  const base = (process.env.ANTHROPIC_BASE_URL || "https://api.anthropic.com").replace(/\/$/, "");
  if (!key) {
    return json({
      error: "No access to the Anthropic endpoint is configured. In Netlify, enable AI Gateway under " +
             "Project configuration → AI Gateway, or set ANTHROPIC_API_KEY as an environment variable. " +
             "Local retrieval works regardless."
    }, 503);
  }

  const context = passagen.map((p, i) => {
    const head = `[${i + 1}] ${p.zitat}${p.seite ? `, p. ${p.seite}` : ""} — ${p.werk_titel || ""}` +
      `${p.uebersetzer ? ` (trans. ${p.uebersetzer})` : ""}`;
    return `${head}\n${String(p.text || "").slice(0, 2600)}`;
  }).join("\n\n---\n\n");

  const messages = [];
  for (const m of verlauf.slice(0, -1)) {
    if (!m || !m.text) continue;
    messages.push({ role: m.rolle === "user" ? "user" : "assistant", content: String(m.text).slice(0, 1600) });
  }
  messages.push({ role: "user", content: `PASSAGES\n\n${context}\n\n---\n\nQUESTION\n${frage}` });

  const payload = {
    model: MODEL, max_tokens: 1800, temperature: 0.2,
    system: BASE + MODES[modus], messages,
  };

  let last = "";
  for (const model of [MODEL, ...FALLBACK]) {
    payload.model = model;
    try {
      const r = await fetch(`${base}/v1/messages`, {
        method: "POST",
        headers: { "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01" },
        body: JSON.stringify(payload),
      });
      if (r.ok) {
        const d = await r.json();
        const antwort = (d.content || []).filter(c => c.type === "text").map(c => c.text).join("\n").trim();
        return json({ antwort: antwort || "(empty answer)", modell: model, passagen: passagen.length, verbrauch: d.usage || null });
      }
      last = `${r.status} ${(await r.text()).slice(0, 300)}`;
      if (r.status !== 404 && r.status !== 400) break;
    } catch (e) {
      last = String(e && e.message ? e.message : e);
      break;
    }
  }
  return json({ error: "The answering endpoint reports: " + last }, 502);
};

function json(o, status = 200) {
  return new Response(JSON.stringify(o), {
    status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

export const config = { path: "/.netlify/functions/dialogue" };
