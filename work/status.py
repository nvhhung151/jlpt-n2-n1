"""Bang tien do theo cap x loai goi: so muc da dien / tong, so loi chan, so canh bao.

  python status.py [N2|N1] [--files]     (--files: them bang theo tung file)
"""
import glob
import json
import os
import sys
from collections import OrderedDict, defaultdict

import validate as V
from jsonio import PKG

ORDER = ['VOCAB_TYPE', 'VOCAB_MEANING', 'TOPIC_ASSIGN', 'KANJI_CORE', 'RADICAL_NAME', 'GRAMMAR_UNIT', 'GRAMMAR_PARENT',
         'GRAMMAR_CORE', 'VOCAB_MNEMONIC', 'KANJI_MNEMONIC', 'VOCAB_EXAMPLE', 'GRAMMAR_BANK']


def main():
    levels = [a for a in sys.argv[1:] if a in ('N2', 'N1')] or ['N2', 'N1']
    per_file = '--files' in sys.argv
    ctx = V.Ctx()
    res = V.run([os.path.join(PKG, lv) for lv in levels], ctx)
    errs, warns = defaultdict(int), defaultdict(int)
    for r in res:
        (errs if r['severity'] == 'error' else warns)[r['file']] += 1
    for lv in levels:
        table = OrderedDict((k, [0, 0, 0, 0, 0, 0]) for k in ORDER)  # files, files_done, filled, total, err, warn
        rows = []
        for f in sorted(glob.glob(os.path.join(PKG, lv, '*.json'))):
            rel = f'{lv}/{os.path.basename(f)}'
            try:
                d = json.load(open(f, encoding='utf-8'))
            except Exception:  # noqa: BLE001
                rows.append((rel, '-', '-', 'JSON lỗi', ''))
                continue
            filled = sum(1 for it in d['items'] if it['answer'] is not None)
            total = len(d['items'])
            t = table.setdefault(d['kind'], [0, 0, 0, 0, 0, 0])
            t[0] += 1
            t[1] += filled == total
            t[2] += filled
            t[3] += total
            t[4] += errs[rel]
            t[5] += warns[rel]
            rows.append((rel, filled, total, errs[rel], warns[rel]))
        print(f'\n== {lv}')
        print(f'{"loại gói":16} {"file xong":>10} {"mục đã điền":>14} {"lỗi":>6} {"cảnh báo":>9}')
        tot = [0, 0, 0, 0, 0, 0]
        for k, t in table.items():
            if not t[0]:
                continue
            tot = [a + b for a, b in zip(tot, t)]
            print(f'{k:16} {t[1]:>4}/{t[0]:<5} {t[2]:>6}/{t[3]:<7} {t[4]:>6} {t[5]:>9}')
        print(f'{"TỔNG":16} {tot[1]:>4}/{tot[0]:<5} {tot[2]:>6}/{tot[3]:<7} {tot[4]:>6} {tot[5]:>9}')
        if per_file:
            for r in rows:
                print('  ', r[0], f'{r[1]}/{r[2]}', 'lỗi', r[3], 'cảnh báo', r[4])


if __name__ == '__main__':
    main()
