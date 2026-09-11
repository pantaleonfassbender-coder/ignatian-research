# Licensing, file by file

This repository holds four kinds of material, and one licence for all of them
would be wrong: the code is the author's, the editorial texts are the author's,
the derived data is a compilation of facts, and two categories belong to other
people entirely.

| What | Files | Licence |
|---|---|---|
| **Source code** | `index.html`, `app.js`, `corpus.js`, `viz.js`, `dialogue.js`, `style.css`, `netlify/functions/*`, `netlify.toml`, `robots.txt` | [MIT](LICENSE) |
| **Editorial texts** | `data/introductions.json`, `data/introduction.json` (the introductory essay, with its manuscript in `docs/Fassbender-2026-Ignatiana-Introduction.docx`), `data/glossary.json`, `data/lexicon.json`, `data/sections.json`, `README.md`, and the editorial prose inside `app.js` and `index.html` | [CC BY 4.0](LICENSE-CONTENT) |
| **Derived datasets** | `data/anchors.json`, `works.json`, `corpus.json`, `terms.json`, `keyness.json`, `network.json`, `persons.json`, `places.json`, `itinerary.json`, `discernment.json` | [CC0 1.0](LICENSE-DATA) — public domain dedication |
| **Public-domain source text** | `data/letters.json` | Public domain in its own right — see below |
| **Bilingual edition of the 1599 Directory** | `data/directorium.json` | Latin: public domain (US, pre-1930 publication); English working translation: [CC0 1.0](LICENSE-DATA) — see below |
| **Trilingual edition of the Exercises** | `data/exercitia.json` | Spanish, Latin and English texts: public domain (US, pre-1930 publications); editorial segmentation and numbering: [CC0 1.0](LICENSE-DATA) |
| **Longridge 1919 texts** | `data/longridge_exx.json`, `data/longridge_dir.json` | Longridge's translation, commentary and notes: public domain (US, pre-1930 publication); editorial block assignment to the [1]–[370] grid: [CC0 1.0](LICENSE-DATA) — see below |
| **Bilingual edition of Favre's Memoriale** | `data/memoriale.json` | Latin: public domain (US, 1873 publication); English working translation and editorial paragraph numbering: [CC0 1.0](LICENSE-DATA) — see below |
| **Xavier letters (Coleridge 1872)** | `data/xavier.json` | Public domain (US, 1872 publication); selection and paragraph numbering: [CC0 1.0](LICENSE-DATA) — see below |
| **Nadal, In Examen annotationes** | `data/nadal.json` | Latin: public domain (Monumenta Ignatiana, 1919); English working translation: [CC0 1.0](LICENSE-DATA) |
| **Cautio Criminalis selections** | `data/spee.json` | Latin: public domain (1631 printing; transcription adds nothing licensable); English working translation: [CC0 1.0](LICENSE-DATA) |
| **Trutznachtigall selections** | `data/trutz.json`, `assets/spee/*` | German and facsimile pages: public domain (1649/1654 printing); transcription and English working translation: [CC0 1.0](LICENSE-DATA) |
| **Imago primi saeculi module** | `data/imago.json`, `assets/imago/*` | Engravings, Latin and Poirters's Dutch: public domain (two 1640 printings; faithful reproduction of a public-domain 2-D work adds nothing licensable); transcription, working translations and descriptions: [CC0 1.0](LICENSE-DATA) |
| **Bilingual edition of the Monita secreta** | `data/monita.json` | Latin and English: public domain (US, 1857 publication); editorial repair and alignment: [CC0 1.0](LICENSE-DATA) — see below |
| **Bilingual edition of the brief of 1773** | `data/dominus.json` | Latin: public domain (brief of 1773, edition of 1852); English working translation: [CC0 1.0](LICENSE-DATA) — see below |
| **The author's essay** | `data/pilgrim_profile.json`, `docs/Fassbender-2026-The-Pilgrims-Profile.docx` | © 2026 Dr. Pantaleon Fassbender, **all rights reserved** — deliberately excluded from the open licences above |
| **Third-party libraries** | `vendor/` | Upstream licences — see below |

## The two categories that are not the author's to license

**`data/letters.json`** holds the twenty-four letters of 1524–1547 in the
translation of D. F. O'Leary, edited by Alban Goodier (B. Herder / Manresa
Press, 1914). That translation is in the public domain by age, which is why it
could be included at all. It is not covered by any licence granted here, because
it was never the author's to grant. Use it as you would any public-domain text.
Note that it is an optical scan whose errors are left visible rather than
silently emended — the reasoning is on the site's method page.

**`data/directorium.json`** holds the Official Directory of 1599 twice over.
The Latin follows the printing in *Monumenta Ignatiana*, series secunda (Madrid,
1919, pp. 1138–1178), a pre-1930 publication in the United States public domain;
a faithful transcription of a public-domain text adds nothing licensable. The
English beside it is an unofficial machine-generated working translation made
for this repository directly from that Latin, consulting no copyrighted
translation; whatever rights it could attract are dedicated to the public domain
under CC0 1.0. It carries no ecclesiastical or scholarly authority — anyone
citing the Directory should cite the Latin.

**`data/exercitia.json`** holds the book of the Exercises three times over:
the Spanish Autograph and the Latin Vulgata of 1548 as printed in the Madrid
1919 *Monumenta Ignatiana* (a pre-1930 publication, US public domain), and
Elder Mullan's English translation (New York, 1914, US public domain). Faithful
transcription of public-domain texts adds nothing licensable; the editorial
segmentation into the canonical [1]–[370] paragraphs is dedicated to the public
domain under CC0 1.0.

**`data/pascal.json`** holds Letters V, VII and X of Pascal's *Lettres
provinciales* (1656–1657) complete, in the Rev. Thomas M'Crie's English
translation of 1856 (New York: Robert Carter & Brothers), via the Project
Gutenberg transcription #73959 — an 1856 publication in the United States
public domain; M'Crie's footnote markers are removed and his notes are not
reproduced. The editorial paragraph numbering is dedicated to the public
domain under CC0 1.0. The French original (public domain) is named as source
but not yet carried.

**`data/xavier.json`** holds four letters of St. Francis Xavier complete, in
the English of H. J. Coleridge SJ, *The Life and Letters of St. Francis
Xavier*, 2 vols. (London: Burns and Oates, 1872) — an 1872 publication in the
United States public domain; a faithful transcription adds nothing licensable.
Coleridge quotes the letters inside a running biography; the cutting of each
letter at its printed opening and dateline, the rejoining of the Kagoshima
letter's two installments, and the paragraph numbering are dedicated to the
public domain under CC0 1.0. Coleridge translated freely from the Latin of
older editions; anyone citing Xavier critically should cite the *Monumenta
Xaveriana*.

**`data/monita.json`** holds the *Monita secreta* — the anti-Jesuit forgery of
1614, carried by this apparatus as the debate it forced, not as truth — in the
bilingual printing of W. C. Brownlee, *Secret Instructions of the Jesuits* (New
York: American and Foreign Christian Union, 1857), Latin and English on facing
pages. An 1857 publication is in the United States public domain; a faithful
transcription adds nothing licensable. The OCR was repaired article by article
against the page images (a handful of articles lost at page breaks were
re-transcribed from the images by hand); that repair, and the pairing of the
Latin chapter/article grid with the English one, are dedicated to the public
domain under CC0 1.0.

**`data/dominus.json`** holds the brief *Dominus ac Redemptor* (21 July 1773)
complete, in the Latin of Augustin Theiner's edition, *Clementis XIV. Pont.
Max. Epistolae et Brevia* (Paris, 1852), doc. CCCXVII — a papal act of 1773 in
an 1852 printing, public domain twice over; a faithful transcription adds
nothing licensable. The English beside it is an unofficial machine-generated
working translation made for this repository directly from that Latin,
consulting no other translation; whatever rights it could attract are dedicated
to the public domain under CC0 1.0. It carries no ecclesiastical or scholarly
authority — cite the Latin, in Theiner's paragraph numbering as carried here.

**`data/memoriale.json`** holds the Memoriale of Blessed Peter Faber, with the
appendix of letters and counsels, as printed in the editio princeps, ed. Marcel
Bouix SJ (Paris: Gauthier-Villars, 1873) — an 1873 publication in the United
States public domain; a faithful transcription adds nothing licensable. Favre's
autograph is lost; the 1873 print gives the Latin version transmitted within
the Society of Jesus. The English beside it is an unofficial machine-generated
working translation made for this repository directly from that Latin, and the
paragraph numbering is this repository's own (the canonical MF numbering
belongs to the 1914 critical edition, which prints a different text); both are
dedicated to the public domain under CC0 1.0. The translation carries no
ecclesiastical or scholarly authority — cite the Latin.

**`data/longridge_exx.json`** and **`data/longridge_dir.json`** hold, in OCR
reconstruction, W. H. Longridge's *The Spiritual Exercises of Saint Ignatius of
Loyola. Translated from the Spanish with a Commentary and a Translation of the
Directorium in Exercitia* (London: Robert Scott, 1919): his commentary on the
Exercises with the seventeen Additional Notes, and his English translation of
the Official Directory of 1599. As a pre-1930 publication the book is in the
United States public domain; a faithful transcription adds nothing licensable.
The editorial work done here — segmentation of the commentary into blocks, their
assignment to ranges of the canonical [1]–[370] grid (which the 1919 book does
not carry), and the paragraph alignment of the Directory translation against the
Latin — is dedicated to the public domain under CC0 1.0.

**`vendor/`** holds unmodified third-party builds:

- `pdf.min.mjs`, `pdf.worker.min.mjs` — pdf.js 4.6.82, Mozilla, Apache License 2.0
- `jspdf.umd.min.js` — jsPDF 2.5.2, MIT

They are vendored rather than loaded from a CDN so that opening the site
contacts no host but its own. Their licences travel with them and are unaffected
by anything declared here.

## What none of this licenses

**The four in-copyright translations.** The Spiritual Exercises (trans. Ganss,
IJS 1992), the Constitutions and Complementary Norms (ed. Padberg, IJS 1996),
A Pilgrim's Testament (trans. Divarkar, IJS 1995) and the Spiritual Diary (ed.
and trans. Munitiz, Inigo Enterprises 1987) remain the property of their
publishers and translators. The same holds for Martin E. Palmer's *On Giving
the Spiritual Exercises* (IJS, 1996): no part of it is in this repository, and
the Directory translation here was made without consulting it.

**No part of their text is in this repository.** What is here describes them —
page correspondences, counts, registers — and describing a book grants no rights
in it. A reader who wants the text of those works must own it; the apparatus is
built on that assumption throughout.

If you hold rights in one of these editions and consider anything here to exceed
what derived data and scholarly citation permit, write to the address in the
site's legal notice and it will be dealt with promptly.
