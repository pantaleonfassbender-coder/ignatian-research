# -*- coding: utf-8 -*-
"""Build assets/download/ignatiana-data.zip — the corpus as one archive.

The data-paper preparation (JOHD) and a courtesy to researchers: every
open data file of the apparatus in one download, with the licenses and a
manifest. Excluded: the two author essays (data/pilgrim_profile.json,
data/exercised_self.json — all rights reserved, outside the open
licenses), and data/modules.json (a build artifact duplicating the module
files). Everything else in data/ is either public-domain text with CC0
editorial layers or CC BY 4.0 editorial matter, as LICENSES.md states per
file. Run after every module ship, after bundle-modules.py:

    python tools/build-download.py
"""
import json, os, zipfile, datetime

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUTDIR = os.path.join(ROOT, "assets", "download")
os.makedirs(OUTDIR, exist_ok=True)
OUT = os.path.join(OUTDIR, "ignatiana-data.zip")

EXCLUDE = {"pilgrim_profile.json", "exercised_self.json", "modules.json"}

prog = json.load(open(os.path.join(ROOT, "data", "program.json"), encoding="utf-8"))
shipped = sorted(p["id"] for p in prog if p.get("status") == "shipped")
cff = open(os.path.join(ROOT, "CITATION.cff"), encoding="utf-8").read()
import re
version = re.search(r"^version: ([\d.]+)", cff, re.M).group(1)

manifest = f"""Ignatiana: A Research Apparatus for Ignatian Spirituality
Data download, version {version}, built {datetime.date.today().isoformat()}

Live site:  https://ignatian-research.netlify.app/
Repository: https://github.com/pantaleonfassbender-coder/ignatian-research
Archive:    https://doi.org/10.5281/zenodo.22682750 (concept DOI, all versions)

Contents: every open data file of the apparatus (data/*.json), the license
texts, and this manifest. The two interpretive author essays are NOT
included (all rights reserved). Licensing per file is stated in
LICENSES.md at the repository root; in brief: the historical texts are
public domain; this site's editions, working translations, paragraph
numbering and derived data are dedicated CC0 1.0 (see LICENSE-DATA);
editorial prose (introductions, blurbs, notes) is CC BY 4.0 (see
LICENSE-CONTENT). Cite the printed editions for any passage you quote;
cite the apparatus by its CITATION.cff.

Shipped program modules in this version ({len(shipped)}):
{", ".join(shipped)}
"""

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("MANIFEST.txt", manifest)
    for name in ("LICENSE", "LICENSE-DATA", "LICENSE-CONTENT", "LICENSES.md",
                 "SOURCES.md", "CITATION.cff"):
        z.write(os.path.join(ROOT, name), name)
    n = 0
    for fn in sorted(os.listdir(os.path.join(ROOT, "data"))):
        if not fn.endswith(".json") or fn in EXCLUDE:
            continue
        z.write(os.path.join(ROOT, "data", fn), f"data/{fn}")
        n += 1
print(f"wrote assets/download/ignatiana-data.zip: {n} data files, "
      f"{os.path.getsize(OUT)/1048576:.1f} MB, version {version}")
