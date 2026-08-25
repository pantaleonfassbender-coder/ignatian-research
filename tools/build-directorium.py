# -*- coding: utf-8 -*-
"""Carves the official Directory of 1599 out of the 1919 Madrid volume.

Source: Monumenta Ignatiana, series secunda: Exercitia spiritualia S. Ignatii
de Loyola et eorum directoria, Madrid 1919 (public domain in the United
States as a pre-1930 publication), which reproduces the Florence 1599
printing (Apud Philippum Iunctam) of the Directorium in its original
orthography. Text layer: the Internet Archive's OCR of the Princeton copy
(monumentaignatia01igna).

This script does the deterministic part only: it locates the 1599 text,
splits it into its forty chapters, and writes the RAW OCR of each chapter to
a working file. It deliberately does not attempt to clean the Latin: the OCR
interleaves the printing's marginal captions with the body line by line and
garbles the sixteenth-century typography (u/v, long s), and mechanical rules
would corrupt as much as they heal. The reading text and the translation are
produced from this raw material in a documented editorial pass; see
data/directorium.json and the method note it carries.

Run:  python tools/build-directorium.py <path-to-mi1919_djvu.txt> [--out FILE]
"""

import io
import json
import os
import re
import sys

# ------------------------------------------------------------------ locate

START_MARK = r"DIRECTORIUM\s+EXERCITIORUM\s+SPIRITUALIUM\s+S\.\s*P\.\s*IGNATII\s+DE\s+LOYOLA\s+F"
END_MARK = r"INDEX\s+RERUM\s+PERSONARUM"

# Chapter headings end in 'Cap. <numeral>'. Two printed forms occur: title and
# 'Cap. N.' on one line, or the title on its own line with a bare 'Cap. N.'
# after it. The OCR mangles both words ('Gap.', 'Cab.', "1 'II" for VII,
# 'XXL' for XXI), so the numeral is never trusted: chapters are numbered by
# their order, and the repair table anchors what neither pattern can see.
NUM = r"[IVXLM1lIiJj/'°L ]{1,10}"
HEAD = re.compile(r"(?m)^([^\n]{4,90}?[CG]a[pb]\s*\.?\s*" + NUM + r"[\.\s]{0,3})\s*$")
HEAD_BARE = re.compile(r"(?m)^\s*([CG]a[pb]\s*[.,]?\s*" + NUM + r"\s*\.?)\s*$")

# Headings the OCR damaged beyond the pattern: unique raw substrings located
# by hand in the working text, in reading order, each marking where the named
# chapter begins. Verified against the numerals of the neighbouring chapters.
REPAIRS = [
    # (chapter number, unique raw anchor at/near the heading)
    (32, "De  oralione  [>ost  faclam"),      # De oratione post factam electionem. Cap. XXXII
    (40, "Qnac  commoidaiida  suiil"),        # Quae commendanda sunt ei qui absoluit Exercitia. Cap. XL
]

# The Florence printing closes with the rector's attestation and the
# imprimatur, which belong to it; the 1919 volume's own appendices
# (bibliography of editions) follow and do not.
TRIM_AFTER = "APPENDICES"



def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    src = sys.argv[1]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None

    t = io.open(src, encoding="utf-8", errors="replace").read()
    m = re.search(START_MARK, t)
    if not m:
        print("Startmarke nicht gefunden.")
        sys.exit(1)
    seg = t[m.start():]
    e = re.search(END_MARK, seg[10000:])
    body = seg[:e.start() + 10000] if e else seg
    cut = body.find(TRIM_AFTER, 10000)
    if cut > 0:
        body = body[:cut]

    cuts = [(h.start(), h.group(1).strip()) for h in HEAD.finditer(body)]
    taken = {c[0] for c in cuts}
    for h in HEAD_BARE.finditer(body):
        # bare 'Cap. N.': the heading proper is the preceding non-empty line;
        # the cut sits at that line so the title stays with its chapter
        line_start = body.rfind("\n", 0, h.start())
        prev_end = line_start
        while prev_end > 0 and body[prev_end - 1] == "\n":
            prev_end -= 1
        prev_start = body.rfind("\n", 0, prev_end) + 1
        title = body[prev_start:prev_end].strip()
        pos = prev_start if 4 <= len(title) <= 90 else h.start()
        if not any(abs(pos - c) < 60 for c in taken):
            cuts.append((pos, (title + "  " + h.group(1).strip()) if pos != h.start() else h.group(1).strip()))
            taken.add(pos)
    for num, anchor in REPAIRS:
        i = body.find(anchor)
        if i < 0:
            print(f"REPAIR-Anker fehlt: Kap. {num}: {anchor[:50]!r}")
            sys.exit(1)
        cuts.append((i, f"[repariert: Cap. {num}]"))
    cuts.sort()

    chapters = []
    # Everything before the first heading is the 1599 front matter: title page
    # and Acquaviva's preface. Kept as chapter 0.
    chapters.append({"n": 0, "kopf_roh": "(Titelblatt und Praefatio)",
                     "roh": body[:cuts[0][0]].strip() if cuts else body})
    for i, (pos, kopf) in enumerate(cuts):
        end = cuts[i + 1][0] if i + 1 < len(cuts) else len(body)
        chapters.append({"n": i + 1, "kopf_roh": kopf, "roh": body[pos:end].strip()})

    out = out or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "..", "..", "directorium-raw.json")
    io.open(out, "w", encoding="utf-8").write(
        json.dumps({"quelle": "Monumenta Ignatiana II, Madrid 1919 (IA: monumentaignatia01igna)",
                    "kapitel": chapters}, ensure_ascii=False))
    print(f"{len(chapters) - 1} Kapitel + Vorspann -> {out}")
    for c in chapters:
        print(f"  {c['n']:3d}  {len(c['roh']):6d} Z.  {c['kopf_roh'][:70]}")


if __name__ == "__main__":
    main()
