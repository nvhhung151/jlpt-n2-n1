#!/usr/bin/env python3
"""Merge answers into a pack file.

Usage: python3 -I merge.py cloud/answers/N1/VOCAB_TYPE-001.json [more answer files...]

Answer file format: {"<item id>": <answer object or null>, ...}
Only the "answer" field of matching items is changed. Items not listed keep their current answer.
Pack is written as JSON.stringify(obj, null, 1) + "\n" (UTF-8).
"""
import json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK_ROOT = os.path.join(BASE, "n2-n1-handoff")


def merge(ans_path):
    lv = os.path.basename(os.path.dirname(ans_path))
    name = os.path.basename(ans_path)
    pack_path = os.path.join(PACK_ROOT, lv, name)
    with open(ans_path, encoding="utf-8") as f:
        answers = json.load(f)
    if not isinstance(answers, dict):
        raise SystemExit(f"{ans_path}: answers file must be an object id -> answer")
    with open(pack_path, encoding="utf-8") as f:
        pack = json.load(f)
    ids = {it["id"] for it in pack["items"]}
    unknown = [k for k in answers if k not in ids]
    n = 0
    for it in pack["items"]:
        if it["id"] in answers:
            it["answer"] = answers[it["id"]]
            n += 1
    tmp = pack_path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(pack, ensure_ascii=False, indent=1) + "\n")
    os.replace(tmp, pack_path)
    filled = sum(1 for it in pack["items"] if it["answer"] is not None)
    print(f"{lv}/{name}: merged {n}, filled {filled}/{len(pack['items'])}" + (f", UNKNOWN ids {unknown}" if unknown else ""))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        merge(p)
