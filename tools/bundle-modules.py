# -*- coding: utf-8 -*-
"""Bundle the shipped program modules' data files into data/modules.json.

The boot loads this one file instead of one request per module; app.js
falls back to the individual files if the bundle is missing or does not
cover every shipped module, and tools/check-ignatiana.py fails CI when the
bundle is stale. Run this after every module ship:

    python tools/bundle-modules.py
"""
import json, os

ROOT = os.path.join(os.path.dirname(__file__), "..")
prog = json.load(open(os.path.join(ROOT, "data", "program.json"), encoding="utf-8"))
shipped = [p for p in prog if p.get("status") == "shipped" and p.get("datei")]

bundle = {}
for p in shipped:
    f = os.path.join(ROOT, "data", f"{p['datei']}.json")
    bundle[p["datei"]] = json.load(open(f, encoding="utf-8"))

out = os.path.join(ROOT, "data", "modules.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(bundle, fh, ensure_ascii=False, separators=(",", ":"))
size = os.path.getsize(out)
print(f"wrote data/modules.json: {len(bundle)} modules, {size/1024:.0f} KB")
