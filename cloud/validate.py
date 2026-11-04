#!/usr/bin/env python3
"""Validate filled packs against the brief.

Usage:
  python3 -I validate.py N1/VOCAB_TYPE-001.json [...]   # specific packs (relative to pack root)
  python3 -I validate.py N1                              # whole level
  python3 -I validate.py --all                           # N2 + N1, also cross-item template checks
Options: --json (machine output), --quiet (summary only)
Prints one line per problem: SEVERITY CODE file id detail
"""
import json, os, re, sys, glob, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(BASE, "n2-n1-handoff")
ORIG = os.path.join(BASE, "work", "orig")

TYPE_LABELS = {"danh từ", "động từ nhóm I", "động từ nhóm II", "động từ nhóm III", "tính từ い", "tính từ な",
               "phó từ", "trợ từ", "liên từ", "thán từ", "cụm từ", "số từ", "đại từ"}
LEN_MAX = {"N2": 50, "N1": 60}
KANJI_RE = re.compile(r"[㐀-䶿一-鿿豈-﫿々〆ヶ]")
PAREN_RE = re.compile(r"\(([^()]*)\)")
KANA_RE = re.compile(r"^[ぁ-ゟ゠-ヿー]+$")
AI_RE = re.compile(r"(Claude|ChatGPT|GPT|Gemini|Anthropic|OpenAI|(?<![A-Za-zÀ-ỹ])AI(?![A-Za-zÀ-ỹ]))")
BANK_TYPES = ["FILL", "ORDER_STAR", "MEANING", "ERROR"]
ERROR_PROMPT = "Câu nào dùng sai mẫu?"

problems = []


def P(sev, code, f, iid, detail=""):
    problems.append((sev, code, f, iid, detail))


_cache = {}


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def level_meta(lv):
    if lv in _cache:
        return _cache[lv]
    bank, parents, mains, sec_ids = set(), set(), set(), set()
    for p in glob.glob(f"{ORIG}/{lv}/GRAMMAR_BANK-*.json"):
        bank |= {i["id"] for i in load(p)["items"]}
    for p in glob.glob(f"{ORIG}/{lv}/GRAMMAR_PARENT-*.json"):
        d = load(p)
        parents |= {i["id"] for i in d["items"]}
        mains |= {m["id"] for m in d["header"]["mains"]}
    meta = {"bank": bank, "parents": parents, "mains": mains}
    _cache[lv] = meta
    return meta


def above_level_sets():
    if "above" in _cache:
        return _cache["above"]
    k2, k1, v1 = set(), set(), set()
    for lv, ks in (("N2", k2), ("N1", k1)):
        for p in glob.glob(f"{ORIG}/{lv}/KANJI_*.json"):
            for i in load(p)["items"]:
                ks.add(i["context"]["character"])
    for p in glob.glob(f"{ORIG}/N1/VOCAB_*.json") + glob.glob(f"{ORIG}/N1/TOPIC_ASSIGN-*.json"):
        for i in load(p)["items"]:
            e = re.sub(r"\[.*?\]|（.*?）|\(.*?\)", "", i["context"]["expression"]).strip()
            if len(e) >= 2 and KANJI_RE.search(e):
                v1.add(e)
    res = (k1 - k2, v1)
    _cache["above"] = res
    return res


def check_example(f, iid, lv, ex, where):
    if not isinstance(ex, dict) or set(ex.keys()) != {"ja", "ja_furigana", "vi"}:
        P("ERROR", "EXAMPLE_SHAPE", f, iid, f"{where}: cần đúng {{ja, ja_furigana, vi}}")
        return
    ja, fu, vi = ex["ja"], ex["ja_furigana"], ex["vi"]
    if not all(isinstance(x, str) and x.strip() for x in (ja, fu, vi)):
        P("ERROR", "EXAMPLE_EMPTY", f, iid, where)
        return
    if "(" in ja or ")" in ja:
        P("ERROR", "JA_HAS_PAREN", f, iid, f"{where}: {ja}")
    stripped = PAREN_RE.sub("", fu)
    if stripped != ja:
        P("ERROR", "FURIGANA_MISMATCH", f, iid, f"{where}: ja={ja} | bỏ ngoặc={stripped}")
    for m in PAREN_RE.finditer(fu):
        if not KANA_RE.match(m.group(1)):
            P("ERROR", "FURIGANA_NOT_KANA", f, iid, f"{where}: ({m.group(1)})")
    # every kanji run must be followed by a reading
    outside = fu
    pos = 0
    for m in re.finditer(r"[㐀-䶿一-鿿豈-﫿々〆ヶ]+", fu):
        # skip if inside parens
        before = fu[:m.start()]
        if before.count("(") > before.count(")"):
            continue
        nxt = fu[m.end():m.end() + 1]
        if nxt != "(":
            P("ERROR", "FURIGANA_MISSING", f, iid, f"{where}: '{m.group(0)}' thiếu cách đọc")
            break
    n = len(re.sub(r"\s", "", ja))
    if n < 8 or n > LEN_MAX[lv]:
        P("ERROR", "EXAMPLE_LENGTH", f, iid, f"{where}: {n} ký tự (cho phép 8–{LEN_MAX[lv]}): {ja}")
    if lv == "N2":
        k_above, v_above = above_level_sets()
        ks = sorted({c for c in ja if c in k_above})
        if ks:
            P("WARN", "EXAMPLE_ABOVE_LEVEL", f, iid, f"{where}: kanji N1 {''.join(ks)}: {ja}")
        vs = [v for v in v_above if v in ja]
        if vs:
            P("WARN", "EXAMPLE_ABOVE_LEVEL_VOCAB", f, iid, f"{where}: từ N1 {vs[:3]}: {ja}")


def check_meaning_short(f, iid, s, code="MEANING_FORMAT"):
    if not isinstance(s, str) or not s.strip():
        P("ERROR", code, f, iid, "rỗng")
        return
    if s != s.strip():
        P("ERROR", code, f, iid, "khoảng trắng thừa đầu/cuối")
    if s.endswith(".") or s.endswith("。"):
        P("ERROR", code, f, iid, f"dấu chấm cuối: {s}")
    if re.search(r"[()（）\[\]]", s):
        P("ERROR", code, f, iid, f"có ngoặc: {s}")
    parts = s.split("; ")
    if len(parts) > 3:
        P("ERROR", code, f, iid, f">3 nghĩa: {s}")
    if any(not p.strip() for p in parts) or ";" in s.replace("; ", ""):
        P("ERROR", code, f, iid, f"ngăn cách sai (phải là '; '): {s}")
    if s[:1] != s[:1].lower():
        P("WARN", code + "_CASE", f, iid, f"chữ hoa đầu (chỉ được với tên riêng): {s}")


def check_bank_q(f, iid, q, where):
    keys = {"type", "prompt_ja", "options", "answer_index", "explanation_vi"}
    if not isinstance(q, dict) or set(q.keys()) != keys:
        P("ERROR", "BANK_SHAPE", f, iid, f"{where}: cần đúng {sorted(keys)}")
        return None
    t = q["type"]
    if t not in BANK_TYPES:
        P("ERROR", "BANK_TYPE", f, iid, f"{where}: type {t}")
    o = q["options"]
    if not (isinstance(o, list) and len(o) == 4 and all(isinstance(x, str) and x.strip() for x in o)):
        P("ERROR", "BANK_OPTIONS", f, iid, f"{where}: cần 4 lựa chọn không rỗng")
    elif len(set(x.strip() for x in o)) != 4:
        P("ERROR", "BANK_OPTIONS_DUP", f, iid, f"{where}: lựa chọn trùng nhau {o}")
    if not (isinstance(q["answer_index"], int) and 0 <= q["answer_index"] <= 3):
        P("ERROR", "BANK_ANSWER_INDEX", f, iid, f"{where}: {q['answer_index']}")
    if not (isinstance(q["explanation_vi"], str) and q["explanation_vi"].strip()):
        P("ERROR", "BANK_EXPLANATION", f, iid, where)
    pj = q["prompt_ja"]
    if not (isinstance(pj, str) and pj.strip()):
        P("ERROR", "BANK_PROMPT", f, iid, where)
        return t
    if t == "FILL" and "（　　）" not in pj:
        P("ERROR", "BANK_FILL_BLANK", f, iid, f"{where}: thiếu （　　）: {pj}")
    if t == "ORDER_STAR":
        if pj.count("★") != 1 or pj.count("＿＿") != 3:
            P("ERROR", "BANK_ORDER_STAR", f, iid, f"{where}: cần 3 ô ＿＿ và 1 ★: {pj}")
    if t == "ERROR" and pj != ERROR_PROMPT:
        P("ERROR", "BANK_ERROR_PROMPT", f, iid, f"{where}: prompt_ja phải là '{ERROR_PROMPT}'")
    return t


def check_item(f, lv, kind, it, header):
    iid = it["id"]
    a = it["answer"]
    if a is None:
        return False
    need = it["fields_needed"]
    if not isinstance(a, dict):
        P("ERROR", "ANSWER_SHAPE", f, iid, "answer phải là object")
        return True
    allowed = set(need)
    if kind in ("VOCAB_MNEMONIC", "KANJI_MNEMONIC"):
        allowed.add("confusable_ids")
    if kind == "KANJI_CORE" and "han_viet" in need:
        allowed.add("han_viet_alt")
    missing = [k for k in need if k not in a]
    extra = [k for k in a if k not in allowed]
    if missing:
        P("ERROR", "FIELD_MISSING", f, iid, str(missing))
    if extra:
        P("ERROR", "FIELD_EXTRA", f, iid, str(extra))
    blob = json.dumps(a, ensure_ascii=False)
    if AI_RE.search(blob):
        P("ERROR", "AI_NAME", f, iid, AI_RE.search(blob).group(0))
    ctx = it["context"]

    if kind == "VOCAB_TYPE":
        if a.get("word_type_label") not in TYPE_LABELS:
            P("ERROR", "TYPE_LABEL", f, iid, str(a.get("word_type_label")))
    elif kind == "VOCAB_MEANING":
        check_meaning_short(f, iid, a.get("meaning_vi"))
    elif kind == "TOPIC_ASSIGN":
        pairs = {(t["topic_key"], t["topic_vi"]) for t in header["topics"]} | {("khac", "Từ thông dụng khác")}
        if (a.get("topic_key"), a.get("topic_vi")) not in pairs:
            P("ERROR", "TOPIC_PAIR", f, iid, f"{a.get('topic_key')}/{a.get('topic_vi')}")
    elif kind == "KANJI_CORE":
        if "han_viet" in need:
            hv = a.get("han_viet")
            if not (isinstance(hv, str) and hv.strip() and hv == hv.upper()):
                P("ERROR", "HAN_VIET_CASE", f, iid, str(hv))
            alt = a.get("han_viet_alt", [])
            if not (isinstance(alt, list) and all(isinstance(x, str) and x == x.upper() for x in alt)):
                P("ERROR", "HAN_VIET_ALT", f, iid, str(alt))
        if "meanings_vi" in need:
            check_meaning_short(f, iid, a.get("meanings_vi"), "KANJI_MEANING_FORMAT")
    elif kind == "RADICAL_NAME":
        n = a.get("name_vi")
        if not (isinstance(n, str) and n.strip()):
            P("ERROR", "RADICAL_EMPTY", f, iid)
        elif n != n.lower():
            P("WARN", "RADICAL_CASE", f, iid, n)
    elif kind == "GRAMMAR_UNIT":
        if a.get("unit_no") not in header["units"]:
            P("ERROR", "UNIT_NO", f, iid, str(a.get("unit_no")))
        t = a.get("unit_title_vi")
        if t is not None and not (isinstance(t, str) and t.strip()):
            P("ERROR", "UNIT_TITLE", f, iid, str(t))
    elif kind == "GRAMMAR_PARENT":
        meta = level_meta(lv)
        pid = a.get("parent_id")
        cands = {c["id"] for c in ctx.get("candidates", [])} | {m["id"] for m in header["mains"]}
        if pid not in cands:
            P("ERROR", "PARENT_NOT_CANDIDATE", f, iid, str(pid))
        if pid not in meta["mains"]:
            P("ERROR", "PARENT_NOT_MAIN", f, iid, str(pid))
        if pid == iid:
            P("ERROR", "PARENT_SELF", f, iid)
    elif kind in ("VOCAB_MNEMONIC", "KANJI_MNEMONIC"):
        m = a.get("mnemonic_vi")
        if not (isinstance(m, str) and m.strip()):
            P("ERROR", "MNEMONIC_EMPTY", f, iid)
        else:
            sents = [s for s in re.split(r"(?<=[.!?…])\s+", m.strip()) if s.strip()]
            if len(sents) > 2:
                P("WARN", "MNEMONIC_LONG", f, iid, f"{len(sents)} câu")
            if len(m) > 260:
                P("WARN", "MNEMONIC_LONG", f, iid, f"{len(m)} ký tự")
        c = a.get("confusable_ids", [])
        if c != []:
            P("WARN", "CONFUSABLE_NOT_EMPTY", f, iid, "để [] (không có compiled list để kiểm id)")
    elif kind == "VOCAB_EXAMPLE":
        exs = a.get("examples")
        ctx_ex = ctx.get("examples", [])
        if not isinstance(exs, list) or not exs:
            P("ERROR", "EXAMPLE_COUNT", f, iid, "cần ≥1 câu mới")
        else:
            if len(exs) + len(ctx_ex) > 3:
                P("ERROR", "EXAMPLE_COUNT", f, iid, f"tổng {len(exs)+len(ctx_ex)} > 3")
            seen = {e["ja"] for e in ctx_ex}
            for k, e in enumerate(exs):
                check_example(f, iid, lv, e, f"ex{k+1}")
                if isinstance(e, dict) and e.get("ja") in seen:
                    P("ERROR", "EXAMPLE_DUP", f, iid, e.get("ja"))
                if isinstance(e, dict):
                    seen.add(e.get("ja"))
    elif kind == "GRAMMAR_CORE":
        meta = level_meta(lv)
        role = "MAIN" if iid in meta["bank"] else "SECONDARY"
        for k in ("meaning_vi", "formation", "usage_vi", "nuance_vi", "common_mistakes_vi"):
            if k in need and not (isinstance(a.get(k), str) and a.get(k).strip()):
                P("ERROR", "GRAMMAR_FIELD_EMPTY", f, iid, k)
        if "formation" in need and isinstance(a.get("formation"), str) and "~" in a["formation"]:
            P("ERROR", "FORMATION_TILDE", f, iid, "dùng 〜 (U+301C), không dùng ~")
        if "examples" in need:
            exs = a.get("examples")
            ctx_ex = ctx.get("examples", [])
            if not isinstance(exs, list) or not exs:
                P("ERROR", "EXAMPLE_COUNT", f, iid, "thiếu examples")
            else:
                tot = len(exs) + len(ctx_ex)
                if role == "MAIN" and tot != 3:
                    P("ERROR", "EXAMPLE_COUNT", f, iid, f"mẫu chính cần tổng 3 câu, đang {tot}")
                if role == "SECONDARY" and not (1 <= tot <= 2):
                    P("ERROR", "EXAMPLE_COUNT", f, iid, f"mẫu phụ cần tổng 1–2 câu, đang {tot}")
                seen = {e["ja"] for e in ctx_ex}
                for k, e in enumerate(exs):
                    check_example(f, iid, lv, e, f"ex{k+1}")
                    if isinstance(e, dict) and e.get("ja") in seen:
                        P("ERROR", "EXAMPLE_DUP", f, iid, e.get("ja"))
                    if isinstance(e, dict):
                        seen.add(e.get("ja"))
    elif kind == "GRAMMAR_BANK":
        cb = a.get("check_bank")
        if not isinstance(cb, list) or len(cb) != 8:
            P("ERROR", "GRAMMAR_BANK_SHORT", f, iid, f"check_bank cần đúng 8 câu, đang {len(cb) if isinstance(cb, list) else cb}")
            cb = cb if isinstance(cb, list) else []
        types = collections.Counter(check_bank_q(f, iid, q, f"check_bank[{k}]") for k, q in enumerate(cb))
        for t in BANK_TYPES:
            if types.get(t, 0) != 2:
                P("ERROR", "GRAMMAR_BANK_TYPES", f, iid, f"{t}: {types.get(t, 0)} (cần 2)")
        sigs = {(q.get("prompt_ja"), tuple(q.get("options", []))) for q in cb if isinstance(q, dict)}
        ep = a.get("extra_practice")
        if not isinstance(ep, list) or len(ep) != 3:
            P("ERROR", "EXTRA_PRACTICE_COUNT", f, iid, f"cần 3, đang {len(ep) if isinstance(ep, list) else ep}")
            ep = ep if isinstance(ep, list) else []
        for k, q in enumerate(ep):
            check_bank_q(f, iid, q, f"extra_practice[{k}]")
            if isinstance(q, dict) and (q.get("prompt_ja"), tuple(q.get("options", []))) in sigs:
                P("ERROR", "EXTRA_PRACTICE_DUP", f, iid, f"extra_practice[{k}] trùng check_bank")
        oi = a.get("order_items")
        if not isinstance(oi, list) or len(oi) != 2:
            P("ERROR", "ORDER_ITEMS_COUNT", f, iid, "cần 2 bài")
            oi = oi if isinstance(oi, list) else []
        for k, o in enumerate(oi):
            if not isinstance(o, dict) or set(o.keys()) != {"pieces", "answer_order", "translation_vi"}:
                P("ERROR", "ORDER_ITEM_SHAPE", f, iid, f"order_items[{k}]: cần {{pieces, answer_order, translation_vi}}")
                continue
            pcs, ao = o["pieces"], o["answer_order"]
            if not (isinstance(pcs, list) and 3 <= len(pcs) <= 5 and all(isinstance(x, str) and x for x in pcs)):
                P("ERROR", "ORDER_ITEM_PIECES", f, iid, f"order_items[{k}]: 3–5 mảnh")
            elif sorted(ao) != list(range(len(pcs))):
                P("ERROR", "ORDER_ITEM_ORDER", f, iid, f"order_items[{k}]: answer_order không phải hoán vị")
            elif ao == list(range(len(pcs))):
                P("WARN", "ORDER_ITEM_UNSHUFFLED", f, iid, f"order_items[{k}]: mảnh đang xếp sẵn đúng thứ tự")
            if not (isinstance(o["translation_vi"], str) and o["translation_vi"].strip()):
                P("ERROR", "ORDER_ITEM_TRANSLATION", f, iid, f"order_items[{k}]")
        fi = a.get("fill_items")
        if not isinstance(fi, list) or len(fi) != 2:
            P("ERROR", "FILL_ITEMS_COUNT", f, iid, "cần 2 bài")
            fi = fi if isinstance(fi, list) else []
        for k, o in enumerate(fi):
            if not isinstance(o, dict) or not {"sentence_ja", "answer", "translation_vi"} <= set(o.keys()) \
                    or set(o.keys()) - {"sentence_ja", "answer", "translation_vi", "accept"}:
                P("ERROR", "FILL_ITEM_SHAPE", f, iid, f"fill_items[{k}]")
                continue
            if "＿＿" not in o["sentence_ja"]:
                P("ERROR", "FILL_ITEM_BLANK", f, iid, f"fill_items[{k}]: thiếu ＿＿")
            if not (isinstance(o["answer"], str) and o["answer"].strip()):
                P("ERROR", "FILL_ITEM_ANSWER", f, iid, f"fill_items[{k}]")
            if "accept" in o and not (isinstance(o["accept"], list) and all(isinstance(x, str) and x for x in o["accept"])):
                P("ERROR", "FILL_ITEM_ACCEPT", f, iid, f"fill_items[{k}]")
    return True


def check_pack(path):
    rel = os.path.relpath(path, ROOT)
    lv = rel.split(os.sep)[0]
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        d = json.loads(raw)
    except Exception as e:  # noqa
        P("ERROR", "JSON_INVALID", rel, "-", str(e))
        return None
    if json.dumps(d, ensure_ascii=False, indent=1) + "\n" != raw:
        P("ERROR", "FILE_FORMAT", rel, "-", "phải ghi bằng JSON.stringify(obj,null,1)+\\n")
    o = load(os.path.join(ORIG, rel))
    for k in ("header", "kind", "level", "packet_id"):
        if d.get(k) != o.get(k):
            P("ERROR", "FIELD_CHANGED", rel, "-", k)
    if set(d.keys()) != set(o.keys()):
        P("ERROR", "FIELD_CHANGED", rel, "-", "top-level keys")
    if len(d["items"]) != len(o["items"]):
        P("ERROR", "ITEM_COUNT_CHANGED", rel, "-")
        return d
    filled = 0
    for it, oi in zip(d["items"], o["items"]):
        for k in ("id", "context", "fields_needed"):
            if it.get(k) != oi.get(k):
                P("ERROR", "FIELD_CHANGED", rel, oi["id"], k)
        if set(it.keys()) != set(oi.keys()):
            P("ERROR", "FIELD_CHANGED", rel, oi["id"], "item keys")
        if check_item(rel, lv, d["kind"], it, d["header"]):
            filled += 1
    return d


def cross_checks(packs):
    """Template / repetition checks across many packs."""
    mn = collections.defaultdict(list)
    ex_start = collections.defaultdict(list)
    for rel, d in packs:
        for it in d["items"]:
            a = it["answer"]
            if not isinstance(a, dict):
                continue
            if isinstance(a.get("mnemonic_vi"), str):
                key = (d["level"], d["kind"], " ".join(a["mnemonic_vi"].split()[:4]).lower())
                mn[key].append((rel, it["id"]))
            for e in a.get("examples", []) or []:
                if isinstance(e, dict) and isinstance(e.get("ja"), str):
                    ja = e["ja"]
                    if ja.startswith("これは") or ja.endswith("を使います。"):
                        P("WARN", "EXAMPLE_TEMPLATE", rel, it["id"], ja)
                    ex_start[(d["level"], ja[:6])].append((rel, it["id"]))
    for key, lst in mn.items():
        if len(lst) >= 8:
            P("WARN", "MNEMONIC_TEMPLATE", lst[0][0], lst[0][1], f"{len(lst)} mẹo nhớ mở đầu '{key[2]}' ({key[1]})")
    for key, lst in ex_start.items():
        if len(lst) >= 8:
            P("WARN", "EXAMPLE_START_REPEAT", lst[0][0], lst[0][1], f"{len(lst)} câu mở đầu '{key[1]}'")


def main(argv):
    as_json = "--json" in argv
    quiet = "--quiet" in argv
    args = [a for a in argv if not a.startswith("--")]
    targets = []
    if "--all" in argv:
        args = ["N2", "N1"]
    for a in args:
        p = a if os.path.isabs(a) else os.path.join(ROOT, a)
        if os.path.isdir(p):
            targets += sorted(glob.glob(os.path.join(p, "*.json")))
        else:
            targets.append(p)
    packs = []
    for t in targets:
        d = check_pack(t)
        if d is not None:
            packs.append((os.path.relpath(t, ROOT), d))
    if len(packs) > 1:
        cross_checks(packs)
    errs = [p for p in problems if p[0] == "ERROR"]
    warns = [p for p in problems if p[0] == "WARN"]
    if as_json:
        print(json.dumps([dict(zip(("severity", "code", "file", "id", "detail"), p)) for p in problems], ensure_ascii=False, indent=1))
    elif not quiet:
        for p in problems:
            print(" | ".join(str(x) for x in p))
    print(f"SUMMARY packs={len(packs)} errors={len(errs)} warnings={len(warns)}", file=sys.stderr if as_json else sys.stdout)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
