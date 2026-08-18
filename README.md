# Ignatiana — a research apparatus for the writings of Ignatius of Loyola

Live: **<https://ignatian-research.netlify.app/>**

Six texts as one working corpus: the *Spiritual Exercises*, the *Constitutions* with their
*Complementary Norms*, the dictated memoir known as *A Pilgrim's Testament*, the *Spiritual Diary*, the
early *Directives on giving the Exercises*, and the letters of 1524–1547. The apparatus indexes them by
their canonical numbering, traces the vocabulary that migrates between them, and lets you put a question
to the corpus with the evidence attached.

It is a working instrument, not a publication. It was built for one reader's use and is opened here in
case it is useful to others; the limits are stated at length rather than buried.

---

## The rights position, first

This is the constraint everything else follows from. Ignatius died in 1556 and his writings are long out
of copyright. The **translations** that make them readable are not.

| Work | Translation | Rights | In this repository |
|---|---|---|---|
| *Letters and Instructions*, vol. I | D. F. O'Leary, 1914 | public domain | **full text included** (24 letters) |
| *The Spiritual Exercises* | George E. Ganss, 1992 | in copyright | derived data only |
| *Constitutions & Complementary Norms* | ed. John W. Padberg, 1996 | in copyright | derived data only |
| *A Pilgrim's Testament* | Parmananda R. Divarkar, 1995 | in copyright | derived data only |
| *The Spiritual Diary* | Joseph A. Munitiz, 1987 | in copyright | derived data only |
| *Directives on the Exercises* | Martin E. Palmer, 1996 | in copyright | derived data only |

For the five in-copyright translations this repository carries **no running text at all**: only
paragraph-level citation anchors, counts, co-occurrence edges, name registers, and editorial matter
written for this site. All rights in those translations rest with their publishers and translators —
principally the Institute of Jesuit Sources and Inigo Enterprises.

Full-text functions work against a copy **you** own. Your PDF is read in the browser by pdf.js, stored in
that browser's IndexedDB, and never uploaded. Only the passages local retrieval selects for a specific
question are sent onward.

If you hold rights in one of these editions and consider anything here to exceed what derived data and
scholarly citation permit, write to the address in the site's legal notice and it will be dealt with
promptly.

---

## What a researcher gets

**A canonical citation index.** 1,887 anchors tying paragraph numbers to the page on which they begin, so
that a concordance hit reads `SpEx [23]` or `Const [134]` rather than a page number nobody cites.
Coverage by work: Exercises 369 of 370, Constitutions 812 of 827, Pilgrim's Testament 101 of 101, Diary
486 of 490, and 119 across the six directory documents.

**A concordance across all six works at once**, with keyword in context, hit distribution per work, and a
canonical citation on every line — once you have opened your own copies.

**The 1914 letters in full**, searchable and quotable without any copy of your own, with recipient, place
and date for each.

**A discernment lexicon**: 27 terms of the vocabulary of consolation, desolation and election traced
across the corpus, with their distribution — which is where the differences between the works become
visible rather than merely assertable.

**Registers and networks**: persons, places, the memoir's itinerary, log-likelihood keyness per work, and
a co-occurrence graph of the correspondence.

**A citation-bound dialogue.** Questions are answered only from passages retrieved from your own copies,
with a canonical citation required on every substantive claim. It refuses to assert what the passages do
not carry. It is still a language model and can misread; every citation it gives can and should be
checked.

---

## What is in `data/`

About 500 kB of JSON, all of it derived or editorial.

| File | Contents |
|---|---|
| `works.json` | the six works: translator, rights, citation form, body range, sections, linguistic measures |
| `anchors.json` | 1,887 canonical paragraph anchors, each with PDF page and printed page |
| `letters.json` | the 24 public-domain letters in full, with recipient, place, date |
| `introductions.json`, `sections.json` | editorial orientation, textual history, key passages, internal divisions |
| `lexicon.json` | 27 discernment terms traced across the corpus |
| `glossary.json` | 39 institutional, practical and philological terms |
| `keyness.json`, `terms.json`, `network.json` | log-likelihood profiles, distributions, co-occurrence graph |
| `persons.json`, `places.json`, `itinerary.json` | registers and the memoir's route |
| `discernment.json`, `corpus.json` | term-family distributions and corpus totals |

`anchors.json` is the piece most likely to be useful on its own. Its shape is
`{ workId: [ { n: paragraph, p: pdfPage, s: printedPage }, … ] }` — a plain concordance between the
canonical numbering and the pagination of the reference editions, which is tedious to build and easy to
reuse.

---

## Opening your own copies

Drop one or more PDFs into *Open from your own copies*. Recognition is automatic but not blind: each file
is scored against all six editions on the evidence of its front matter — the title of the edition, the
translator or editor, phrases proper to that volume, and phrases belonging to a *different* volume, which
count against — corroborated by the page count of the reference edition. A work is opened only when one
candidate wins by a clear margin; otherwise the panel asks which work it is, with the file already read.

This matters because the six volumes quote each other. The Constitutions name the Exercises on their
first pages, and Ganss's name stands in the front matter of three editions because the 1996 Constitutions
print his translation — so a signature that counts shared phrases alone will file Padberg's Constitutions
and Munitiz's Diary under the Exercises. Each work can also be opened from a named file directly, which
overrides recognition, and removed again individually. Where a page count diverges from the reference
edition the panel says so, rather than letting a divergent printing be silently mis-cited.

Editions the anchors were built against: Ganss (IJS, 1992); Padberg (IJS, 1996); Divarkar (IJS, 1995);
Munitiz, *Íñigo: Discernment Log-Book* (Inigo Enterprises, 1987); Palmer (IJS, 1996); O'Leary, ed. Goodier
(B. Herder / Manresa Press, 1914). A different printing will still search; its pages will not line up.

---

## Limits

Set out in full on the site's *Method, sources and limits* page, and worth reading before citing anything.
In brief: the 1914 letters are an optical scan whose errors are left visible rather than silently emended;
name recognition is automatic and over-recognises liturgical capitalisation while under-recognising
Spanish and Basque names; the Complementary Norms are not separated out as an independent citation series;
type–token ratio is length-dependent and should not be compared across works of very different extent;
and the itinerary follows the memoir's own account, which is a narrative composed thirty years after the
events and shaped for a purpose.

---

## Running it

A static site with one Netlify Function. No build step, no dependencies — the folder deploys as it stands.

```
python -m http.server 8000     # then open http://localhost:8000
```

Everything except the dialogue works locally: retrieval, concordance, registers and charts all run in the
browser.

To deploy your own copy, point Netlify at a fork, or drag the folder onto <https://app.netlify.com/drop>.
`netlify.toml` must stay in the deployment root.

**The dialogue** calls `/.netlify/functions/dialogue`, which uses Netlify's **AI Gateway**: Netlify injects
`ANTHROPIC_API_KEY` and `ANTHROPIC_BASE_URL` into the function, so no key of your own is needed and usage
is billed in Netlify credits. It requires at least one production deploy and AI features enabled for the
team, and it is bypassed if you set either variable yourself — set your own `ANTHROPIC_API_KEY` if you
would rather use your own Anthropic account. The model defaults to `claude-sonnet-4-6`; set `DIALOG_MODEL`
to change it, with fallback to `claude-sonnet-4-5` and `claude-3-7-sonnet-latest`. Without any endpoint
configured the rest of the site is unaffected.

**No key is stored in this repository**, and none has ever been committed to it.

```
index.html            shell and navigation
app.js                router, data, all views
corpus.js             pdf.js reading, identification, index, KWIC, collocation, BM25
viz.js                charts and force-directed graph, no external library
dialogue.js           dialogue module and PDF export
data/*.json           derived data and editorial matter
vendor/               pdf.js 4.6.82, jsPDF 2.5.2 — vendored, so no CDN is contacted
netlify/functions/    the dialogue function
```

---

## Reuse

Four kinds of material, licensed separately, because one blanket licence would
misdescribe at least two of them. The mapping is in **[LICENSES.md](LICENSES.md)**;
in short:

- **Code** — [MIT](LICENSE).
- **Editorial texts** (introductions, glossary, discernment lexicon, section
  notes, this README) — [CC BY 4.0](LICENSE-CONTENT).
- **Derived datasets**, the anchor table above all — [CC0 1.0](LICENSE-DATA),
  a public-domain dedication. A concordance between canonical paragraph numbers
  and printed pagination is a compilation of facts: laborious to establish,
  discovered rather than invented. It is released free because a citation index
  that others cannot build on is of little use.
- **`data/letters.json`** is the 1914 O'Leary translation. It is in the public
  domain in its own right, and no licence here applies to it — it was never the
  author's to license.
- **`vendor/`** carries the upstream licences of pdf.js (Apache-2.0) and jsPDF
  (MIT).

None of this grants any right in the five in-copyright translations the
apparatus describes. No part of their text is in this repository.

## Citing the apparatus

> Pantaleon Fassbender, *Ignatiana: A Research Apparatus for the Writings of Ignatius of Loyola*,
> <https://ignatian-research.netlify.app/> (accessed …).

See `CITATION.cff` for a machine-readable form. When citing a passage found through the concordance,
cite the printed edition, not this site — the anchors exist precisely so that you can.

## Contributions and corrections

Corrections are welcome, and errors in the anchor table especially so: a wrong anchor produces a wrong
citation, which is the one failure mode this instrument must not have. Open an issue with the work, the
paragraph number and the page you find it on.

---

Operated by a private individual and unaffiliated with the Society of Jesus, the Institute of Jesuit
Sources or any publisher. Privacy notice and legal notice are on the site.
