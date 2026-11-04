#!/usr/bin/env python3
"""Progress table: filled/total per level x kind, and list of unfinished packs.
Usage: python3 -I status.py [--packs]"""
import json, glob, os, sys, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(BASE, "n2-n1-handoff")
tot = collections.Counter(); fil = collections.Counter(); pk = collections.Counter(); pkdone = collections.Counter()
unfinished = []
for lv in ("N2", "N1"):
    for p in sorted(glob.glob(f"{ROOT}/{lv}/*.json")):
        d = json.load(open(p, encoding="utf-8"))
        k = (lv, d["kind"])
        n = len(d["items"]); f = sum(1 for i in d["items"] if i["answer"] is not None)
        tot[k] += n; fil[k] += f; pk[k] += 1
        if f == n:
            pkdone[k] += 1
        elif f:
            unfinished.append(f"{lv}/{os.path.basename(p)} {f}/{n}")
print(f"{'level':5} {'kind':16} {'packs':>9} {'items':>12}")
for k in sorted(tot):
    print(f"{k[0]:5} {k[1]:16} {pkdone[k]:>4}/{pk[k]:<4} {fil[k]:>5}/{tot[k]:<6}")
print(f"TOTAL items {sum(fil.values())}/{sum(tot.values())}")
if "--packs" in sys.argv and unfinished:
    print("partial:", *unfinished, sep="\n  ")
