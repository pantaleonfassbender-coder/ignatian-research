# -*- coding: utf-8 -*-
"""Extract the Spanish Autograph and the Vulgata of the Spiritual Exercises
from Monumenta Ignatiana, ser. II (Madrid 1919), working on the PDF itself.

The 1919 edition prints four texts in parallel: verso pages carry
AUTOGRAPHUM | VULGATA VERSIO, recto pages VERSIO PRIMA | VERSIO P. ROOTHAAN.
Stage 1 needs the verso pages only. The Abbyy djvu stream interleaves the
columns unpredictably, so the columns are cut geometrically instead: for
each verso page the gutter is located as the widest horizontal whitespace
gap in the body region, and each column is cropped and extracted separately.
Running heads are cropped away by y-position; the apparatus at the foot of
each column is reduced afterwards by pattern (sigla lines), the remainder
being for the editorial pass.

Output: two page-jointed raw streams (es, la) for editorial segmentation
into the canonical [1]-[370] units.
"""
import io, json, re
import pdfplumber

PDF = "C:/Users/leofa/OneDrive/Desktop/Ignatius/Sources/monumentaignatia01igna_1919.pdf"
OUT = "C:/Users/leofa/AppData/Local/Temp/exercitia-raw.json"

VERSO = re.compile(r"AUTOGRA|VULGATA|V[UÜ]LGAT|AUTOGRAPH")
RECTO = re.compile(r"VERSIO\s+PR|ROOTH|ROOTII|ROOT1")

HEAD_Y = 88          # running head ends above this line
MIN_WORDS = 40       # pages with less are plates/blanks

def gutter_of(words, width):
    """Widest horizontal gap between word boxes in the middle band."""
    xs = sorted((w["x0"], w["x1"]) for w in words)
    best, bx = 0, width / 2
    cur = None
    for x0, x1 in xs:
        if cur is None or x0 <= cur:
            cur = max(cur or 0, x1)
            continue
        gap = x0 - cur
        mid = (x0 + cur) / 2
        if gap > best and width * 0.35 < mid < width * 0.65:
            best, bx = gap, mid
        cur = max(cur, x1)
    return bx

def lines_of(words):
    """Cluster words into lines by top coordinate, then order by x."""
    out = []
    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if out and abs(w["top"] - out[-1][0][ -1]) <= 3.5:
            out[-1][0].append(w["top"]); out[-1][1].append(w)
        else:
            out.append(([w["top"]], [w]))
    return "\n".join(" ".join(x["text"] for x in sorted(ws, key=lambda w: w["x0"]))
                     for _, ws in out)

def main():
    pdf = pdfplumber.open(PDF)
    pages_out, skipped = [], []
    # The parallel text runs printed 222-562; printed = pdf - 5 throughout,
    # and verso pages are the even printed numbers. Iterating by parity also
    # catches the pages whose running head the OCR mangled beyond recognition.
    for printed in range(222, 563, 2):
        i = printed + 5
        p = pdf.pages[i]
        words = [w for w in p.extract_words() if w["top"] > HEAD_Y]
        if len(words) < MIN_WORDS:
            skipped.append(printed)
            continue
        gut = gutter_of(words, p.width)
        # assign by word start: words never begin inside the gutter gap, so a
        # word starting left of it belongs to the left column even when its
        # tail (a line-end syllable like 'en-') reaches across the midline
        left = lines_of([w for w in words if w["x0"] < gut])
        right = lines_of([w for w in words if w["x0"] >= gut])
        pages_out.append({"pdf": i, "gedruckt": printed, "es": left, "la": right})
    pdf.close()

    def post(s):
        out = []
        for ln in s.split("\n"):
            x = ln.strip()
            if not x:
                continue
            # apparatus sigla lines: 'a praecipitado Ant.', '■ non declaret.'
            if re.match(r"^[a-z*■\u25a0]\s+\S", x) and len(x) < 80 and not re.match(r"^[ay]\s", x):
                continue
            # editorial references: 'V. supra, Proleg., p. 106.'
            if re.match(r"^[VC]f?\.\s+(supra|infra)", x):
                continue
            # stray page numbers
            if re.fullmatch(r"\d{1,3}", x):
                continue
            out.append(x)
        return "\n".join(out)

    es = "".join(f"\n@@S{p['gedruckt']}@@\n" + post(p["es"]) for p in pages_out)
    la = "".join(f"\n@@S{p['gedruckt']}@@\n" + post(p["la"]) for p in pages_out)

    result = {
        "quelle": "Monumenta Ignatiana ser. II (Madrid 1919), verso pages, geometric column split",
        "seiten": [p["gedruckt"] for p in pages_out],
        "uebersprungen": skipped,
        "es": es, "la": la,
    }
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(result, ensure_ascii=False))
    print("verso pages:", len(pages_out), "skipped:", skipped)
    print("printed range:", pages_out[0]["gedruckt"], "-", pages_out[-1]["gedruckt"])
    print("es chars:", len(es), "la chars:", len(la))
    print("written:", OUT)

if __name__ == "__main__":
    main()
