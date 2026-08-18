# Licensing, file by file

This repository holds four kinds of material, and one licence for all of them
would be wrong: the code is the author's, the editorial texts are the author's,
the derived data is a compilation of facts, and two categories belong to other
people entirely.

| What | Files | Licence |
|---|---|---|
| **Source code** | `index.html`, `app.js`, `corpus.js`, `viz.js`, `dialogue.js`, `style.css`, `netlify/functions/*`, `netlify.toml`, `robots.txt` | [MIT](LICENSE) |
| **Editorial texts** | `data/introductions.json`, `data/glossary.json`, `data/lexicon.json`, `data/sections.json`, `README.md`, and the editorial prose inside `app.js` and `index.html` | [CC BY 4.0](LICENSE-CONTENT) |
| **Derived datasets** | `data/anchors.json`, `works.json`, `corpus.json`, `terms.json`, `keyness.json`, `network.json`, `persons.json`, `places.json`, `itinerary.json`, `discernment.json` | [CC0 1.0](LICENSE-DATA) — public domain dedication |
| **Public-domain source text** | `data/letters.json` | Public domain in its own right — see below |
| **Third-party libraries** | `vendor/` | Upstream licences — see below |

## The two categories that are not the author's to license

**`data/letters.json`** holds the twenty-four letters of 1524–1547 in the
translation of D. F. O'Leary, edited by Alban Goodier (B. Herder / Manresa
Press, 1914). That translation is in the public domain by age, which is why it
could be included at all. It is not covered by any licence granted here, because
it was never the author's to grant. Use it as you would any public-domain text.
Note that it is an optical scan whose errors are left visible rather than
silently emended — the reasoning is on the site's method page.

**`vendor/`** holds unmodified third-party builds:

- `pdf.min.mjs`, `pdf.worker.min.mjs` — pdf.js 4.6.82, Mozilla, Apache License 2.0
- `jspdf.umd.min.js` — jsPDF 2.5.2, MIT

They are vendored rather than loaded from a CDN so that opening the site
contacts no host but its own. Their licences travel with them and are unaffected
by anything declared here.

## What none of this licenses

**The five in-copyright translations.** The Spiritual Exercises (trans. Ganss,
IJS 1992), the Constitutions and Complementary Norms (ed. Padberg, IJS 1996),
A Pilgrim's Testament (trans. Divarkar, IJS 1995), the Spiritual Diary (ed. and
trans. Munitiz, Inigo Enterprises 1987) and the Directives (trans. Palmer, IJS
1996) remain the property of their publishers and translators.

**No part of their text is in this repository.** What is here describes them —
page correspondences, counts, registers — and describing a book grants no rights
in it. A reader who wants the text of those works must own it; the apparatus is
built on that assumption throughout.

If you hold rights in one of these editions and consider anything here to exceed
what derived data and scholarly citation permit, write to the address in the
site's legal notice and it will be dealt with promptly.
