# Ignatiana — a research apparatus for the writings of Ignatius of Loyola

A static site with one Netlify Function. No build step, no dependencies: the folder deploys as it stands.

## 1. Deploying with Netlify Drop

1. Drag the **whole folder** (or the supplied ZIP) onto <https://app.netlify.com/drop>.
2. Netlify assigns an address of the form `https://<name>.netlify.app`; rename it under
   *Site configuration → Change site name*.
3. `netlify.toml` points Netlify at the function directory and must stay in the deployment root.

## 2. Enabling the dialogue

The dialogue module calls `/.netlify/functions/dialogue`, which uses Netlify's **AI Gateway**. Netlify injects
`ANTHROPIC_API_KEY` and `ANTHROPIC_BASE_URL` into every compute context, so no key of your own is required;
usage is billed in Netlify credits.

Requirements:

- at least one production deployment (with Netlify Drop the first deploy is production);
- AI features not disabled for the team (*Project configuration → AI Gateway*);
- **no** `ANTHROPIC_API_KEY` or `ANTHROPIC_BASE_URL` of your own — setting either bypasses the gateway.
  If you would rather use your own Anthropic key, set exactly that variable and the function will use it.

The model defaults to `claude-sonnet-4-6`; set `DIALOG_MODEL` to change it. On failure the function falls back
to `claude-sonnet-4-5` and then `claude-3-7-sonnet-latest`. Without any endpoint configured everything else
still works: retrieval runs in the browser and the passages it finds are displayed regardless.

## 3. The rights model, and what it means in practice

| Work | Translation | Rights | On this site |
|---|---|---|---|
| Letters and Instructions, vol. I | D. F. O'Leary, 1914 | public domain | **full text included** |
| The Spiritual Exercises | George E. Ganss, 1992 | in copyright | derived data only |
| Constitutions & Complementary Norms | ed. John W. Padberg, 1996 | in copyright | derived data only |
| A Pilgrim's Testament | Parmananda R. Divarkar, 1995 | in copyright | derived data only |
| The Spiritual Diary | Joseph A. Munitiz, 1987 | in copyright | derived data only |
| Directives on the Exercises | Martin E. Palmer, 1996 | in copyright | derived data only |

For the five in-copyright translations the deployment carries page-level citation anchors, counts, network
edges, name registers and editorial matter written for this site — no running text at all. A reader who owns
the books opens them through *Open from your own copies*: the PDF is read in the browser with pdf.js, stored in
that browser's IndexedDB, and never uploaded. Only the passages the local retrieval selects for a specific
question are sent to the function.

Recognition is automatic but not blind. Each PDF is scored against all six editions on the evidence of its
front matter — the title of the edition, the translator or editor, phrases proper to that volume, and phrases
belonging to a *different* volume, which count against — corroborated by the page count of the reference
edition. A work is opened only when one candidate wins by a clear margin; otherwise the status panel asks
which work the file is, with the file already read. This matters because the six volumes quote each other:
the Constitutions name the Exercises on their first pages, and Ganss's name stands in the front matter of
three editions because the 1996 Constitutions print his translation, so a signature counting shared phrases
alone will file Padberg's Constitutions and Munitiz's Diary under the Exercises. Each work can also be opened
from a named file directly, which overrides recognition, and removed again individually. Where the page count
diverges from the reference edition the status panel says so, so that a divergent printing is flagged rather
than silently mis-cited.

## 4. Folder contents

```
index.html            shell and navigation
app.js                router, data, all views
corpus.js             pdf.js reading, identification, index, KWIC, collocation, BM25
viz.js                charts and force-directed graph, no external library
dialogue.js           dialogue module and PDF export
style.css             styling
data/*.json           derived data and editorial matter (~500 kB)
vendor/               pdf.js 4.6.82, jsPDF 2.5.2
netlify/functions/    the dialogue function
netlify.toml          function directory and headers
```

| Data file | Contents |
|---|---|
| `works.json` | the six works: translator, rights, citation form, body range, sections, linguistic measures |
| `anchors.json` | 1,888 canonical paragraph anchors mapped to PDF page and printed page |
| `letters.json` | the 24 public-domain letters in full, with recipient, place, date |
| `introductions.json`, `sections.json` | editorial orientation, textual history, key passages, internal divisions |
| `lexicon.json` | 27 discernment terms traced across the corpus |
| `glossary.json` | 39 institutional, practical and philological terms |
| `keyness.json`, `terms.json`, `network.json` | log-likelihood profiles, distributions, co-occurrence graph |
| `persons.json`, `places.json`, `itinerary.json` | registers and the memoir's route |
| `discernment.json`, `corpus.json` | term-family distributions and corpus totals |

## 5. Citation

Hits are reported at the nearest preceding canonical anchor: `SpEx [23]`, `Const [134]`, `Autobiog. [30]`,
`Diary [17]`, `Dir., Doc. 1 [5]`, `Letters, no. V`. Anchor coverage is 369/370, 812/827, 101/101, 486/490 and
119 across the six directory documents. The method page in the site states the limits of this resolution.

## 6. If the site should not be public

Netlify offers password protection under *Site configuration → Access control* on paid plans. Nothing in the
deployment requires it — no in-copyright text is shipped — but a working apparatus in progress is often better
kept to a defined group.
