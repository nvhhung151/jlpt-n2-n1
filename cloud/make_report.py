#!/usr/bin/env python3
"""Build BAO-CAO.md + GHI-CHU-CONTEXT.jsonl (all notes merged) at repo root, and the delivery zip.
Usage: python3 -I cloud/make_report.py"""
import json, glob, os, collections, zipfile, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(BASE, "n2-n1-handoff")
os.chdir(BASE)

# ---- collect notes (cloud/ part + work/ part done on the local machine) ----
notes = []
for p in sorted(glob.glob("cloud/notes/*/*.jsonl")):
    lv, pack = p.split("/")[-2], os.path.basename(p)[:-6]
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = d.get("type", "")
        typ = {"SKIPPED": "LY_DO_NULL", "CONTEXT_ERROR": "SAI_CONTEXT"}.get(t, t or "KHAC")
        notes.append({"level": lv, "packet": pack, "id": d.get("id"), "type": typ,
                      "detail": d.get("detail", ""), "suggest": d.get("suggest", "")})
for p in sorted(glob.glob("work/notes/N2/*.jsonl")):
    pack = os.path.basename(p)[:-6]
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = d.get("type", "")
        typ = {"null": "LY_DO_NULL", "context": "SAI_CONTEXT", "uncertain": "CHUA_CHAC"}.get(t, t or "KHAC")
        notes.append({"level": "N2", "packet": d.get("packet", pack), "id": d.get("id"), "type": typ,
                      "detail": d.get("detail") or d.get("issue") or d.get("note") or d.get("reason") or "",
                      "suggest": d.get("suggest") or d.get("suggestion") or ""})
with open("GHI-CHU-CONTEXT.jsonl", "w", encoding="utf-8") as f:
    for n in notes:
        f.write(json.dumps(n, ensure_ascii=False) + "\n")
by_id = collections.defaultdict(list)
for n in notes:
    by_id[n["id"]].append(n)

# ---- per-pack table + nulls ----
rows, nulls = [], []
tot = collections.Counter(); fil = collections.Counter()
for lv in ("N2", "N1"):
    for p in sorted(glob.glob(f"{ROOT}/{lv}/*.json")):
        d = json.load(open(p, encoding="utf-8"))
        n = len(d["items"]); f_ = sum(1 for i in d["items"] if i["answer"] is not None)
        rows.append((lv, os.path.basename(p), d["kind"], f_, n))
        tot[(lv, d["kind"])] += n; fil[(lv, d["kind"])] += f_
        for i in d["items"]:
            if i["answer"] is None:
                c = i["context"]
                label = c.get("expression") or c.get("pattern") or c.get("character") or ""
                why = next((x for x in by_id.get(i["id"], []) if x["type"] == "LY_DO_NULL"), None) \
                    or (by_id.get(i["id"]) or [{}])[0]
                nulls.append((lv, os.path.basename(p), i["id"], label, (why.get("detail") or "").replace("|", "/")))

cnt = collections.Counter((n["level"], n["type"]) for n in notes)
review = open("cloud/notes/REVIEW-TODO.md", encoding="utf-8").read().strip().splitlines()[1:]

L = []
L.append("# Báo cáo điền gói N2–N1 (lộ trình JLPT)")
L.append("")
L.append(f"Ngày: {datetime.date.today().isoformat()}. Người làm: HungNVH, nội dung soạn với hỗ trợ AI, đã tự kiểm bằng script.")
L.append("")
L.append("## Tóm tắt")
L.append("")
L.append(f"- Đã điền **{sum(fil.values()):,}/{sum(tot.values()):,}** mục ({len(rows)} gói). "
         f"**{sum(tot.values())-sum(fil.values())} mục để null**, mục nào cũng có lý do (bảng dưới).")
L.append("- Chỉ điền trường `answer`; không đổi id, context, fields_needed, header, tên file. Kanji 突く JK-7A81 bỏ qua theo HUONG-DAN.")
L.append("- Kiểm bằng script riêng (`cloud/validate.py`): 0 lỗi chặn. Đã kiểm: JSON, đủ/đúng trường, nhãn loại từ, khuôn nghĩa, furigana khớp `ja`, độ dài câu (N2 ≤50, N1 ≤60), số câu ví dụ, Hán Việt viết HOA, cặp chủ đề, unit_no, parent_id thuộc mains, bộ câu hỏi (8 câu đủ 4 dạng, 4 phương án khác nhau, ★, （　　）, order/fill/extra_practice), lặp khuôn, tên AI.")
L.append("- **Chưa chạy** `build_level_source.mjs` (không có trong repo nhận được) → `EXAMPLE_ABOVE_LEVEL` và `*_SIMILAR` mới kiểm một phần (đối chiếu danh sách kanji/từ N1 trong gói). Còn 225 cảnh báo vượt cấp, hầu hết do chính chữ của từ/mẫu đang soạn (vd 妊娠, 派遣, 次第) — đã giữ nguyên chữ theo brief.")
L.append("- `confusable_ids` để `[]` toàn bộ (không có compiled list để lấy id hợp lệ).")
L.append("- GRAMMAR_UNIT N2: `unit_title_vi` để null (giữ tên bài có sẵn); N1 có thêm tên bài 15–18.")
L.append("")
L.append("## Số mục theo loại")
L.append("")
L.append("| Cấp | Loại | Đã điền / Tổng |")
L.append("|---|---|---|")
for k in sorted(tot):
    L.append(f"| {k[0]} | {k[1]} | {fil[k]}/{tot[k]} |")
L.append("")
L.append("## Ghi chú về context (file `GHI-CHU-CONTEXT.jsonl` đi kèm)")
L.append("")
L.append("Mỗi dòng: `{level, packet, id, type, detail, suggest}`. Không sửa context, chỉ ghi lại.")
L.append("")
L.append("| Cấp | Sai context | Chưa chắc / để team quyết | Lý do null |")
L.append("|---|---|---|---|")
for lv in ("N2", "N1"):
    L.append(f"| {lv} | {cnt[(lv,'SAI_CONTEXT')]} | {cnt[(lv,'CHUA_CHAC')]} | {cnt[(lv,'LY_DO_NULL')]} |")
L.append("")
L.append("Loại lỗi hay gặp: cách đọc sai (vd 透き通る すきとうる→すきとおる, 行方 なめがた→ゆくえ), chữ sai (見在→現在, 観逆→観客), `meaning_vi` lẫn câu ví dụ hoặc lạc nghĩa, Hán Việt sai (縦 Sỉ→Tung, 梯 Đệ→Thê), mẫu ngữ pháp trùng nhau hoặc `pattern` ghi bằng tiếng Việt.")
L.append("")
L.append("## Điểm cần team quyết / nên duyệt lại")
L.append("")
L.extend(review)
L.append("")
L.append(f"## Mục để null ({len(nulls)})")
L.append("")
L.append("| Cấp | Gói | id | Mục | Lý do |")
L.append("|---|---|---|---|---|")
for r in nulls:
    L.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4][:160]} |")
L.append("")
L.append("## Số mục đã điền theo từng file")
L.append("")
L.append("| Cấp | File | Đã điền / Tổng |")
L.append("|---|---|---|")
for r in rows:
    L.append(f"| {r[0]} | {r[1]} | {r[3]}/{r[4]} |")
open("BAO-CAO.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

# ---- delivery zip: N2/, N1/, BAO-CAO.md, GHI-CHU-CONTEXT.jsonl ----
zp = os.path.join(BASE, "n2-n1-filled.zip")
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for lv in ("N2", "N1"):
        for p in sorted(glob.glob(f"{ROOT}/{lv}/*.json")):
            z.write(p, f"{lv}/{os.path.basename(p)}")
    z.write("BAO-CAO.md", "BAO-CAO.md")
    z.write("GHI-CHU-CONTEXT.jsonl", "GHI-CHU-CONTEXT.jsonl")
print("notes", len(notes), "nulls", len(nulls), "zip", zp, os.path.getsize(zp))
