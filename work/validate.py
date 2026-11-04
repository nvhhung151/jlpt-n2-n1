"""Kiem goi da dien so voi work/orig va brief.

  python validate.py <file|thu muc> [...] [--json] [--errors] [--quiet]

In moi loi dang {file, id, code, detail, severity}. severity "error" la loi chan, "warning" la canh bao.
Mac dinh in ca loi va canh bao; --errors chi in loi chan; --quiet chi in tong ket; --json in mang JSON.
"""
import glob
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict

from jsonio import ORIG, PKG, dumps

LEVEL_MAX_LEN = {'N2': 50, 'N1': 60}
WORD_TYPES = {'danh từ', 'động từ nhóm I', 'động từ nhóm II', 'động từ nhóm III', 'tính từ い', 'tính từ な', 'phó từ',
              'trợ từ', 'liên từ', 'thán từ', 'cụm từ', 'số từ', 'đại từ'}
BANK_TYPES = ('FILL', 'ORDER_STAR', 'MEANING', 'ERROR')
ERROR_PROMPT = 'Câu nào dùng sai mẫu?'
KANJI_RE = re.compile(r'[㐀-䶿一-鿿豈-﫿々〆ヶ]')
KANA_ONLY_RE = re.compile(r'^[ぁ-ゟ゠-ヿー・]+$')
PAREN_RE = re.compile(r'\(([^()]*)\)')
AI_RE = [re.compile(r'claude|chatgpt|\bgpt\b|openai|\bgemini\b|\bllm\b|anthropic', re.I), re.compile(r'(?<![A-Za-z])AI(?![A-Za-z])')]
EN_WORD_RE = re.compile(r'\b(the|of|and|or|to|be|is|are|with|for|from|by|as|at|on|in|it|this|that|which|who|'
                        r'thing|person|people|make|do|get|have|go|come|take|give|very|not|no|yes)\b', re.I)
TEMPLATE_RE = [re.compile(r'^これは.*です。$'), re.compile(r'を使います。$'), re.compile(r'^それは.*です。$')]
MNEMONIC_KINDS = ('VOCAB_MNEMONIC', 'KANJI_MNEMONIC')


def strip_ws(s):
    return re.sub(r'\s+', '', s or '')


def is_str(v):
    return isinstance(v, str) and v.strip() != ''


class Ctx:
    """Du lieu dung chung: danh sach Kanji/tu N1 (kiem vuot cap), cac id mau phu."""

    def __init__(self):
        self.n1_kanji = set()
        self.n1_words = set()
        self.secondary_ids = defaultdict(set)
        for f in glob.glob(os.path.join(ORIG, 'N1', '*.json')):
            d = json.load(open(f, encoding='utf-8'))
            for it in d['items']:
                c = it['context']
                if d['kind'].startswith('KANJI_') and c.get('character'):
                    self.n1_kanji.add(c['character'])
                if d['kind'].startswith('VOCAB_') or d['kind'] == 'TOPIC_ASSIGN':
                    e = c.get('expression') or ''
                    if len(e) >= 2 and KANJI_RE.search(e):
                        self.n1_words.add(e)
        for lv in ('N2', 'N1'):
            for f in glob.glob(os.path.join(ORIG, lv, 'GRAMMAR_PARENT-*.json')):
                d = json.load(open(f, encoding='utf-8'))
                self.secondary_ids[lv].update(it['id'] for it in d['items'])
            for f in glob.glob(os.path.join(ORIG, lv, 'GRAMMAR_CORE-*.json')):
                d = json.load(open(f, encoding='utf-8'))
                if d['header'].get('grammar_role') == 'SECONDARY':
                    self.secondary_ids[lv].update(it['id'] for it in d['items'])


class Report:
    def __init__(self, path):
        self.file = os.path.relpath(path, PKG).replace(os.sep, '/')
        self.out = []

    def err(self, id_, code, detail):
        self.out.append({'file': self.file, 'id': id_, 'code': code, 'detail': detail, 'severity': 'error'})

    def warn(self, id_, code, detail):
        self.out.append({'file': self.file, 'id': id_, 'code': code, 'detail': detail, 'severity': 'warning'})


# ── cau tieng Nhat ─────────────────────────────────────────────────────────────────────────────────────────

def above_level(text, level, ctx):
    if level != 'N2' or not text:
        return []
    found = [k for k in sorted(set(KANJI_RE.findall(text))) if k in ctx.n1_kanji]
    words = [w for w in ctx.n1_words if w in text and not any(ch in ctx.n1_kanji for ch in w)]
    return found + sorted(words)[:3]


def check_ja_text(rep, id_, text, where, level, ctx):
    hits = above_level(text, level, ctx)
    if hits:
        rep.warn(id_, 'EXAMPLE_ABOVE_LEVEL', f'{where}: có Kanji/từ N1 {hits} trong 「{text}」')


def check_example(rep, id_, ex, where, level, ctx, existing):
    if not isinstance(ex, dict) or set(ex) != {'ja', 'ja_furigana', 'vi'}:
        rep.err(id_, 'EXAMPLE_SHAPE', f'{where}: phải là {{ja, ja_furigana, vi}}')
        return
    ja, fu, vi = ex['ja'], ex['ja_furigana'], ex['vi']
    if not (is_str(ja) and is_str(fu) and is_str(vi)):
        rep.err(id_, 'EXAMPLE_EMPTY', f'{where}: ja/ja_furigana/vi không được rỗng')
        return
    if PAREN_RE.sub('', fu) != ja:
        rep.err(id_, 'FURIGANA_MISMATCH', f'{where}: bỏ (...) ra 「{PAREN_RE.sub("", fu)}」 ≠ ja 「{ja}」')
    for reading in PAREN_RE.findall(fu):
        if not KANA_ONLY_RE.match(reading):
            rep.err(id_, 'FURIGANA_NOT_KANA', f'{where}: phần trong ngoặc 「{reading}」 không phải kana')
    if re.search(r'[()]', PAREN_RE.sub('', fu)):
        rep.err(id_, 'FURIGANA_PAREN', f'{where}: ngoặc không cân trong ja_furigana')
    if '（' in fu or '）' in fu:
        rep.warn(id_, 'FURIGANA_FULLWIDTH', f'{where}: ja_furigana có ngoặc toàn góc, cách đọc phải dùng ngoặc ASCII')
    # cum Kanji khong co cach doc ngay sau
    for m in re.finditer(r'[㐀-鿿々〆ヶ]+', fu):
        nxt = fu[m.end():m.end() + 1]
        if nxt != '(':
            rep.warn(id_, 'FURIGANA_MISSING', f'{where}: cụm 「{m.group()}」 thiếu cách đọc')
            break
    n = len(strip_ws(ja))
    if not (8 <= n <= LEVEL_MAX_LEN[level]):
        rep.err(id_, 'EXAMPLE_LENGTH', f'{where}: dài {n} ký tự (cho phép 8–{LEVEL_MAX_LEN[level]})')
    if strip_ws(ja) in existing:
        rep.err(id_, 'EXAMPLE_DUPLICATE', f'{where}: trùng câu đã có 「{ja}」')
    for t in TEMPLATE_RE:
        if t.search(ja):
            rep.warn(id_, 'TEMPLATE_SENTENCE', f'{where}: câu theo khuôn 「{ja}」')
    if re.search(r'[぀-ヿ一-鿿]', vi):
        rep.warn(id_, 'VI_HAS_JAPANESE', f'{where}: bản dịch còn chữ Nhật')
    check_ja_text(rep, id_, ja, where, level, ctx)


def check_examples(rep, it, ans, level, ctx, lo, hi, total_lo=None, total_hi=None):
    exs = ans.get('examples')
    id_ = it['id']
    if not isinstance(exs, list):
        rep.err(id_, 'EXAMPLES_SHAPE', 'examples phải là mảng')
        return
    have = it['context'].get('examples') or []
    existing = {strip_ws(e.get('ja')) for e in have if isinstance(e, dict)}
    if not (lo <= len(exs) <= hi):
        rep.err(id_, 'EXAMPLE_COUNT', f'cần {lo}–{hi} câu mới, có {len(exs)}')
    total = len(have) + len(exs)
    if total_lo is not None and not (total_lo <= total <= total_hi):
        rep.err(id_, 'EXAMPLE_COUNT', f'tổng câu (kể cả câu có sẵn {len(have)}) phải {total_lo}–{total_hi}, đang {total}')
    seen = set()
    for i, ex in enumerate(exs):
        check_example(rep, id_, ex, f'examples[{i}]', level, ctx, existing)
        if isinstance(ex, dict) and is_str(ex.get('ja')):
            k = strip_ws(ex['ja'])
            if k in seen:
                rep.err(id_, 'EXAMPLE_DUPLICATE', f'examples[{i}] trùng câu khác trong cùng mục')
            seen.add(k)


# ── nghia / chu ───────────────────────────────────────────────────────────────────────────────────────────

def check_meaning_format(rep, id_, value, field, strict=True):
    add = rep.err if strict else rep.warn
    if not is_str(value):
        rep.err(id_, 'MEANING_EMPTY', f'{field} rỗng')
        return
    parts = value.split('; ')
    if len(parts) > 3:
        add(id_, 'MEANING_FORMAT', f'{field}: quá 3 nghĩa')
    if any(not p.strip() or p != p.strip() for p in parts) or ';' in value.replace('; ', ''):
        add(id_, 'MEANING_FORMAT', f'{field}: phải ngăn nghĩa bằng "; "')
    if value.rstrip().endswith('.'):
        add(id_, 'MEANING_FORMAT', f'{field}: không có dấu chấm cuối')
    # Owner 04/11: meaning_vi / meanings_vi không được có ngoặc ( ) （ ） [ ] — lỗi chặn ở mọi loại gói.
    if re.search(r'[()（）\[\]［］]', value):
        rep.err(id_, 'MEANING_FORMAT', f'{field}: không được có ngoặc ( ) （ ） [ ]: 「{value}」')
    for p in parts:
        if p[:1] and p[:1] != p[:1].lower():
            rep.warn(id_, 'MEANING_CASE', f'{field}: 「{p}」 viết hoa đầu (chỉ được với tên riêng)')
    if EN_WORD_RE.search(value) or re.search(r'[fjwzFJWZ]', value):
        rep.warn(id_, 'MEANING_ENGLISH', f'{field}: có thể có chữ tiếng Anh: 「{value}」')


def check_mnemonic(rep, id_, value):
    if not is_str(value):
        rep.err(id_, 'MNEMONIC_EMPTY', 'mnemonic_vi rỗng')
        return
    sentences = [s for s in re.split(r'(?<=[.!?…])\s+', value.strip()) if s]
    if len(sentences) > 2:
        rep.warn(id_, 'MNEMONIC_LONG', f'mẹo nhớ {len(sentences)} câu (nên 1–2)')


# ── GRAMMAR_BANK ─────────────────────────────────────────────────────────────────────────────────────────

def check_question(rep, id_, q, where, level, ctx):
    if not isinstance(q, dict):
        rep.err(id_, 'BANK_SHAPE', f'{where}: phải là object')
        return None
    need = {'type', 'prompt_ja', 'options', 'answer_index', 'explanation_vi'}
    if set(q) != need:
        rep.err(id_, 'BANK_SHAPE', f'{where}: trường {sorted(q)} ≠ {sorted(need)}')
    t, prompt, opts, ai = q.get('type'), q.get('prompt_ja'), q.get('options'), q.get('answer_index')
    if t not in BANK_TYPES:
        rep.err(id_, 'BANK_TYPE', f'{where}: type {t!r} không hợp lệ')
    if not is_str(prompt):
        rep.err(id_, 'BANK_PROMPT', f'{where}: prompt_ja rỗng')
        prompt = ''
    if not isinstance(opts, list) or len(opts) != 4 or not all(is_str(o) for o in opts):
        rep.err(id_, 'BANK_OPTIONS', f'{where}: cần đúng 4 lựa chọn không rỗng')
        opts = [o for o in (opts or []) if isinstance(o, str)]
    elif len({strip_ws(o) for o in opts}) != 4:
        rep.err(id_, 'BANK_OPTIONS_DUP', f'{where}: có lựa chọn trùng nhau')
    if not isinstance(ai, int) or isinstance(ai, bool) or not 0 <= ai <= 3:
        rep.err(id_, 'BANK_ANSWER_INDEX', f'{where}: answer_index phải 0–3')
    if not is_str(q.get('explanation_vi')):
        rep.err(id_, 'BANK_EXPLANATION', f'{where}: explanation_vi rỗng')
    if t == 'FILL' and '（　　）' not in prompt:
        rep.err(id_, 'BANK_FILL_BLANK', f'{where}: FILL phải có 「（　　）」')
    if t == 'ORDER_STAR':
        stars, blanks = prompt.count('★'), prompt.count('＿＿')
        if stars != 1 or stars + blanks != 4:
            rep.err(id_, 'BANK_ORDER_STAR', f'{where}: cần đúng 4 ô và 1 ★ (đang {blanks} ＿＿ + {stars} ★)')
    if t == 'ERROR' and prompt != ERROR_PROMPT:
        rep.err(id_, 'BANK_ERROR_PROMPT', f'{where}: prompt_ja phải là 「{ERROR_PROMPT}」')
    if t == 'MEANING' and any(re.search(r'[぀-ヿ]', o) for o in opts):
        rep.warn(id_, 'BANK_MEANING_LANG', f'{where}: lựa chọn MEANING nên là câu tiếng Việt')
    jp = [prompt] if t != 'ERROR' else []
    if t in ('FILL', 'ORDER_STAR', 'ERROR'):
        jp += opts
    for s in jp:
        check_ja_text(rep, id_, s, where, level, ctx)
    return (t, strip_ws(prompt), tuple(strip_ws(o) for o in opts))


def check_bank(rep, it, ans, level, ctx):
    id_ = it['id']
    cb = ans.get('check_bank')
    keys = set()
    if not isinstance(cb, list) or len(cb) != 8:
        rep.err(id_, 'GRAMMAR_BANK_SHORT', f'check_bank cần đúng 8 câu, có {len(cb) if isinstance(cb, list) else 0}')
        cb = cb if isinstance(cb, list) else []
    counts = defaultdict(int)
    for i, q in enumerate(cb):
        k = check_question(rep, id_, q, f'check_bank[{i}]', level, ctx)
        if k:
            counts[k[0]] += 1
            if k in keys:
                rep.err(id_, 'BANK_DUPLICATE', f'check_bank[{i}] trùng câu khác')
            keys.add(k)
    if cb and any(counts[t] != 2 for t in BANK_TYPES):
        rep.err(id_, 'BANK_TYPE_COUNT', f'mỗi dạng đúng 2 câu, đang {dict(counts)}')
    oi = ans.get('order_items')
    if not isinstance(oi, list) or len(oi) != 2:
        rep.err(id_, 'ORDER_ITEMS', 'order_items cần đúng 2 bài')
        oi = oi if isinstance(oi, list) else []
    for i, o in enumerate(oi):
        if not isinstance(o, dict) or set(o) != {'pieces', 'answer_order', 'translation_vi'}:
            rep.err(id_, 'ORDER_ITEMS', f'order_items[{i}]: cần {{pieces, answer_order, translation_vi}}')
            continue
        p, a = o['pieces'], o['answer_order']
        if not isinstance(p, list) or not 3 <= len(p) <= 5 or not all(is_str(x) for x in p):
            rep.err(id_, 'ORDER_ITEMS', f'order_items[{i}]: cần 3–5 mảnh')
            continue
        if len({strip_ws(x) for x in p}) != len(p):
            rep.err(id_, 'ORDER_ITEMS', f'order_items[{i}]: có mảnh trùng nhau')
        if not isinstance(a, list) or sorted(a) != list(range(len(p))):
            rep.err(id_, 'ORDER_ITEMS', f'order_items[{i}]: answer_order phải là hoán vị 0..{len(p) - 1}')
        if a == list(range(len(p))):
            rep.warn(id_, 'ORDER_ITEMS_SORTED', f'order_items[{i}]: mảnh đang xếp sẵn đúng thứ tự')
        if not is_str(o['translation_vi']):
            rep.err(id_, 'ORDER_ITEMS', f'order_items[{i}]: translation_vi rỗng')
        for x in p:
            check_ja_text(rep, id_, x, f'order_items[{i}]', level, ctx)
    fi = ans.get('fill_items')
    if not isinstance(fi, list) or len(fi) != 2:
        rep.err(id_, 'FILL_ITEMS', 'fill_items cần đúng 2 bài')
        fi = fi if isinstance(fi, list) else []
    for i, o in enumerate(fi):
        if not isinstance(o, dict) or not {'sentence_ja', 'answer', 'translation_vi'} <= set(o) \
                or set(o) - {'sentence_ja', 'answer', 'translation_vi', 'accept'}:
            rep.err(id_, 'FILL_ITEMS', f'fill_items[{i}]: cần {{sentence_ja, answer, translation_vi[, accept]}}')
            continue
        if not is_str(o['sentence_ja']) or '＿＿' not in o['sentence_ja']:
            rep.err(id_, 'FILL_ITEMS', f'fill_items[{i}]: câu phải có 「＿＿」')
        if not is_str(o['answer']) or not is_str(o['translation_vi']):
            rep.err(id_, 'FILL_ITEMS', f'fill_items[{i}]: answer/translation_vi rỗng')
        if 'accept' in o and (not isinstance(o['accept'], list) or not all(is_str(x) for x in o['accept'])):
            rep.err(id_, 'FILL_ITEMS', f'fill_items[{i}]: accept phải là mảng chuỗi')
        check_ja_text(rep, id_, o.get('sentence_ja') or '', f'fill_items[{i}]', level, ctx)
    ep = ans.get('extra_practice')
    if not isinstance(ep, list) or len(ep) != 3:
        rep.err(id_, 'EXTRA_PRACTICE', 'extra_practice cần đúng 3 câu')
        ep = ep if isinstance(ep, list) else []
    for i, q in enumerate(ep):
        k = check_question(rep, id_, q, f'extra_practice[{i}]', level, ctx)
        if k and k in keys:
            rep.err(id_, 'EXTRA_DUPLICATE', f'extra_practice[{i}] trùng câu trong check_bank')
        if k:
            keys.add(k)


# ── tung goi ─────────────────────────────────────────────────────────────────────────────────────────────

def check_answer(rep, d, it, level, ctx):
    kind, id_, ans, c = d['kind'], it['id'], it['answer'], it['context']
    if not isinstance(ans, dict):
        rep.err(id_, 'ANSWER_SHAPE', 'answer phải là object hoặc null')
        return
    need = set(it['fields_needed'])
    allowed = set(need) | ({'confusable_ids'} if kind in MNEMONIC_KINDS else set()) \
        | ({'han_viet_alt'} if kind == 'KANJI_CORE' else set())
    missing, extra = need - set(ans), set(ans) - allowed
    if missing:
        rep.err(id_, 'FIELD_MISSING', f'thiếu {sorted(missing)}')
    if extra:
        rep.err(id_, 'FIELD_EXTRA', f'thừa {sorted(extra)}')
    if 'confusable_ids' in ans and ans['confusable_ids'] != []:
        rep.err(id_, 'CONFUSABLE_NOT_EMPTY', 'confusable_ids phải để []')

    if kind == 'VOCAB_TYPE':
        if ans.get('word_type_label') not in WORD_TYPES:
            rep.err(id_, 'WORD_TYPE', f'nhãn {ans.get("word_type_label")!r} không thuộc 13 nhãn')
    elif kind == 'VOCAB_MEANING':
        check_meaning_format(rep, id_, ans.get('meaning_vi'), 'meaning_vi')
    elif kind in MNEMONIC_KINDS:
        check_mnemonic(rep, id_, ans.get('mnemonic_vi'))
    elif kind == 'VOCAB_EXAMPLE':
        check_examples(rep, it, ans, level, ctx, 1, 3, 1, 3)
    elif kind == 'TOPIC_ASSIGN':
        pair = (ans.get('topic_key'), ans.get('topic_vi'))
        ok = {(t['topic_key'], t['topic_vi']) for t in d['header'].get('topics', [])} | {('khac', 'Từ thông dụng khác')}
        if pair not in ok:
            rep.err(id_, 'TOPIC_INVALID', f'cặp {pair} không có trong header.topics')
    elif kind == 'KANJI_CORE':
        if 'han_viet' in need:
            hv = ans.get('han_viet')
            if not is_str(hv) or hv != hv.upper():
                rep.err(id_, 'HAN_VIET_CASE', f'han_viet {hv!r} phải viết HOA, không rỗng')
        if 'han_viet_alt' in ans:
            alt = ans['han_viet_alt']
            if not isinstance(alt, list) or any(not is_str(x) or x != x.upper() for x in alt):
                rep.err(id_, 'HAN_VIET_CASE', 'han_viet_alt phải là mảng chuỗi viết HOA')
        if 'meanings_vi' in need:
            check_meaning_format(rep, id_, ans.get('meanings_vi'), 'meanings_vi', strict=False)
    elif kind == 'RADICAL_NAME':
        nv = ans.get('name_vi')
        if not is_str(nv) or nv != nv.lower():
            rep.err(id_, 'RADICAL_NAME', f'name_vi {nv!r} phải chữ thường, không rỗng')
    elif kind == 'GRAMMAR_UNIT':
        units = d['header'].get('units', [])
        if ans.get('unit_no') not in units:
            rep.err(id_, 'UNIT_INVALID', f'unit_no {ans.get("unit_no")!r} không có trong header.units')
        t = ans.get('unit_title_vi')
        if t is not None and not is_str(t):
            rep.err(id_, 'UNIT_TITLE', 'unit_title_vi phải là chuỗi ngắn hoặc null')
    elif kind == 'GRAMMAR_PARENT':
        pid = ans.get('parent_id')
        cand = {x['id'] for x in c.get('candidates', [])} | {x['id'] for x in d['header'].get('mains', [])}
        if pid not in cand:
            rep.err(id_, 'PARENT_INVALID', f'parent_id {pid!r} không có trong candidates/header.mains')
        if pid == id_:
            rep.err(id_, 'PARENT_SELF', 'parent_id trỏ vào chính nó')
        if pid in ctx.secondary_ids[level]:
            rep.err(id_, 'PARENT_IS_SECONDARY', f'parent_id {pid} là mẫu phụ')
    elif kind == 'GRAMMAR_CORE':
        secondary = d['header'].get('grammar_role') == 'SECONDARY'
        for f in ('meaning_vi', 'formation', 'usage_vi', 'nuance_vi', 'common_mistakes_vi'):
            if f in need and not is_str(ans.get(f)):
                rep.err(id_, 'GRAMMAR_FIELD_EMPTY', f'{f} rỗng')
        if 'formation' in need and is_str(ans.get('formation')) and re.search(r'[～~]', ans['formation']):
            rep.warn(id_, 'FORMATION_TILDE', 'formation nên dùng 〜 (U+301C)')
        if 'examples' in need:
            if secondary:
                check_examples(rep, it, ans, level, ctx, 1, 2, 1, 2)
            else:
                check_examples(rep, it, ans, level, ctx, 1, 3, 3, 3)
    elif kind == 'GRAMMAR_BANK':
        check_bank(rep, it, ans, level, ctx)

    for s in iter_strings(ans):
        if any(r.search(s) for r in AI_RE):
            rep.err(id_, 'AI_NAME', f'có tên AI/model: 「{s[:60]}」')
            break


def iter_strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, list):
        for x in v:
            yield from iter_strings(x)
    elif isinstance(v, dict):
        for x in v.values():
            yield from iter_strings(x)


def strip_answers(d):
    return {**d, 'items': [{k: v for k, v in it.items() if k != 'answer'} for it in d['items']]}


def validate_file(path, ctx):
    rep = Report(path)
    level = os.path.basename(os.path.dirname(path))
    raw = open(path, 'rb').read()
    try:
        d = json.loads(raw.decode('utf-8'))
    except Exception as e:  # noqa: BLE001
        rep.err(None, 'JSON_INVALID', str(e))
        return rep.out, None
    if dumps(d).encode('utf-8') != raw:
        rep.err(None, 'FORMAT', 'file không đúng định dạng JSON.stringify(obj, null, 1) + "\\n"')
    orig_path = os.path.join(ORIG, level, os.path.basename(path))
    if not os.path.exists(orig_path):
        rep.err(None, 'FILE_UNKNOWN', 'không có bản gốc tương ứng')
        return rep.out, d
    orig = json.load(open(orig_path, encoding='utf-8'))
    if strip_answers(d) != strip_answers(orig):
        rep.err(None, 'NON_ANSWER_CHANGED', 'có trường ngoài answer khác bản gốc')
    for it in d['items']:
        if it.get('answer') is not None:
            check_answer(rep, d, it, level, ctx)
    return rep.out, d


def repetition(docs, level, targets):
    """Canh bao lap khuon theo ca cap: nhieu muc cung mo dau meo nho / cau vi du."""
    out = []
    starts = defaultdict(list)
    ex_starts = defaultdict(list)
    for path, d in docs:
        rel = os.path.relpath(path, PKG).replace(os.sep, '/')
        for it in d['items']:
            a = it.get('answer')
            if not isinstance(a, dict):
                continue
            m = a.get('mnemonic_vi')
            if is_str(m):
                key = re.sub(r'\s+', ' ', m.strip())[:14].lower()
                starts[key].append((rel, it['id']))
            for ex in a.get('examples') or []:
                if isinstance(ex, dict) and is_str(ex.get('ja')):
                    ex_starts[strip_ws(ex['ja'])[:6]].append((rel, it['id']))
    for key, lst in starts.items():
        if len(lst) >= 4:
            for rel, id_ in lst:
                if rel in targets:
                    out.append({'file': rel, 'id': id_, 'code': 'REPEAT_MNEMONIC_START',
                                'detail': f'{len(lst)} mẹo nhớ {level} cùng mở đầu 「{key}…」', 'severity': 'warning'})
    for key, lst in ex_starts.items():
        if len(lst) >= 8:
            for rel, id_ in lst:
                if rel in targets:
                    out.append({'file': rel, 'id': id_, 'code': 'REPEAT_EXAMPLE_START',
                                'detail': f'{len(lst)} câu ví dụ {level} cùng mở đầu 「{key}…」', 'severity': 'warning'})
    return out


def collect(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += sorted(glob.glob(os.path.join(p, '**', '*.json'), recursive=True))
        else:
            files.append(p)
    return [os.path.abspath(f) for f in files if os.path.basename(os.path.dirname(f)) in ('N2', 'N1')]


def run(paths, ctx=None):
    ctx = ctx or Ctx()
    files = collect(paths)
    out = []
    for f in files:
        o, _ = validate_file(f, ctx)
        out += o
    for level in ('N2', 'N1'):
        targets = {os.path.relpath(f, PKG).replace(os.sep, '/') for f in files
                   if os.path.basename(os.path.dirname(f)) == level}
        if not targets:
            continue
        docs = []
        for f in sorted(glob.glob(os.path.join(PKG, level, '*.json'))):
            try:
                docs.append((f, json.load(open(f, encoding='utf-8'))))
            except Exception:  # noqa: BLE001
                pass
        out += repetition(docs, level, targets)
    return out


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = {a for a in sys.argv[1:] if a.startswith('--')}
    if not args:
        raise SystemExit(__doc__)
    res = run(args)
    errors = [r for r in res if r['severity'] == 'error']
    warns = [r for r in res if r['severity'] == 'warning']
    if '--json' in flags:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    elif '--quiet' not in flags:
        for r in (errors if '--errors' in flags else res):
            print(json.dumps(r, ensure_ascii=False))
    print(f'TONG: {len(errors)} loi chan, {len(warns)} canh bao', file=sys.stderr)
    sys.exit(1 if errors else 0)
