# -*- coding: utf-8 -*-
"""Cut the three Exercises text streams into the fifteen editorial sections.

The es/la offsets were established by reading the actual (garbled) headings
out of the extracted streams — see the build log; fuzzy anchor guessing
proved less reliable than measuring once. Margins of ~100 chars are left on
each cut so the editorial pass sees both sides of every boundary. Mullan
(CCEL, proofed text) is cut by its own clean headings.
"""
import io, json, os, re

RAW = "C:/Users/leofa/AppData/Local/Temp/exercitia-raw.json"
CCEL = "C:/Users/leofa/OneDrive/Desktop/Ignatius/Sources/mullan_ccel.txt"
OUTDIR = "C:/Users/leofa/AppData/Local/Temp/exx-raw"

# id, von, bis, es offset, la offset, CCEL heading regex
SECTIONS = [
    ("ann",    1,  20,      0,      0, r"^ANNOTATIONS"),
    ("tit",   21,  23,  16050,  16450, r"^SPIRITUAL EXERCISES$"),
    ("exam",  24,  44,  17600,  18050, r"^PARTICULAR AND DAILY EXAMEN"),
    ("exx",   45,  72,  27700,  29350, r"^FIRST EXERCISE"),
    ("add",   73,  90,  39500,  43200, r"^ADDITIONS"),
    ("king",  91, 100,  46650,  50600, r"^THE CALL OF THE TEMPORAL KING"),
    ("incnat",101, 117, 50900,  54450, r"^THE FIRST DAY AND FIRST CONTEMPLATION"),
    ("rep",  118, 134,  57500,  58050, r"^THE THIRD CONTEMPLATION"),
    ("states",135, 168, 63200,  66400, r"^PREAMBLE TO CONSIDER STATES"),
    ("elec", 169, 189,  78550,  80300, r"^PRELUDE FOR MAKING ELECTION"),
    ("w3",   190, 217,  85800,  89100, r"^THE FIRST CONTEMPLATION AT MIDNIGHT IS"),
    ("w4",   218, 237,  99100, 101350, r"^FOURTH WEEK"),
    ("modos",238, 260, 106750, 109950, r"^THREE METHODS OF PRAYER"),
    ("myst", 261, 312, 113650, 116050, r"^THE MYSTERIES OF THE LIFE OF CHRIST"),
    ("disc", 313, 336, 147100, 147500, r"^RULES$|^FOR PERCEIVING AND KNOWING"),
    ("rules",337, 370, 159750, 158900, r"^IN THE MINISTRY OF DISTRIBUTING ALMS"),
]
MARGIN = 100

def main():
    raw = json.loads(io.open(RAW, encoding="utf-8").read())
    os.makedirs(OUTDIR, exist_ok=True)
    for li, lang in ((3, "es"), (4, "la")):
        t = raw[lang]
        for k, sec in enumerate(SECTIONS):
            start = max(0, sec[li] - MARGIN)
            end = SECTIONS[k + 1][li] + MARGIN if k + 1 < len(SECTIONS) else len(t)
            io.open(f"{OUTDIR}/{sec[0]}.{lang}.txt", "w", encoding="utf-8").write(t[start:end])
    # Mullan: cut at clean CCEL headings
    en = io.open(CCEL, encoding="utf-8").read()
    lines = en.split("\n")
    pos, offs = 0, {}
    lineoff = []
    for ln in lines:
        lineoff.append(pos)
        pos += len(ln) + 1
    for sid, von, bis, _, _, pat in SECTIONS:
        rx = re.compile(pat)
        offs[sid] = None
        for i, ln in enumerate(lines):
            if rx.match(ln.strip()):
                offs[sid] = lineoff[i]
                break
        if offs[sid] is None:
            print(f"  !! CCEL heading missing for {sid}: {pat}")
    known = [(sid, offs[sid]) for sid, *_ in [(s[0],) for s in SECTIONS] if offs[sid] is not None]
    known = [(s[0], offs[s[0]]) for s in SECTIONS if offs[s[0]] is not None]
    for k, (sid, o) in enumerate(known):
        end = known[k + 1][1] if k + 1 < len(known) else len(en)
        io.open(f"{OUTDIR}/{sid}.en.txt", "w", encoding="utf-8").write(en[o:end])
    print("sections:", len(SECTIONS))
    for s in SECTIONS:
        sizes = []
        for lang in ("es", "la", "en"):
            f = f"{OUTDIR}/{s[0]}.{lang}.txt"
            sizes.append(os.path.getsize(f) if os.path.exists(f) else 0)
        print(f"  {s[0]:7s} [{s[1]:3d}-{s[2]:3d}] es={sizes[0]:6d} la={sizes[1]:6d} en={sizes[2]:6d}")

if __name__ == "__main__":
    main()
