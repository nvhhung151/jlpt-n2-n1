"""Gop answers vao goi.

  python merge.py <answers.json> [--packet <duong dan goi>]
  python merge.py --selftest            (doc/ghi lai moi goi goc, so byte-for-byte)

answers.json: object {id: answer} (answer la object, hoac null de giu trong). Mac dinh file answers
work/answers/<CAP>/<GOI>.json gop vao n2-n1-handoff/<CAP>/<GOI>.json. Chi doi truong "answer".
"""
import glob
import json
import os
import sys

from jsonio import ORIG, PKG, dumps, load, save


def target_for(answers_path):
    parts = os.path.normpath(answers_path).split(os.sep)
    level, name = parts[-2], parts[-1]
    return os.path.join(PKG, level, name)


def merge(answers_path, packet_path=None):
    packet_path = packet_path or target_for(answers_path)
    answers = load(answers_path)
    if not isinstance(answers, dict):
        raise SystemExit(f"{answers_path}: phai la object {{id: answer}}")
    obj = load(packet_path)
    ids = {it['id'] for it in obj['items']}
    unknown = sorted(set(answers) - ids)
    if unknown:
        raise SystemExit(f"{answers_path}: id khong co trong goi: {unknown[:5]}")
    changed = 0
    for it in obj['items']:
        if it['id'] in answers:
            it['answer'] = answers[it['id']]
            changed += 1
    save(packet_path, obj)
    filled = sum(1 for it in obj['items'] if it['answer'] is not None)
    print(f"{os.path.basename(packet_path)}: gop {changed} muc, da dien {filled}/{len(obj['items'])}")


def selftest():
    bad = 0
    files = sorted(glob.glob(os.path.join(ORIG, '*', '*.json')))
    for f in files:
        raw = open(f, 'rb').read()
        if dumps(json.loads(raw.decode('utf-8'))).encode('utf-8') != raw:
            bad += 1
            print('KHAC:', f)
    print(f"selftest: {len(files) - bad}/{len(files)} goi ghi lai giong byte-for-byte")
    return bad == 0


if __name__ == '__main__':
    args = sys.argv[1:]
    if args == ['--selftest']:
        sys.exit(0 if selftest() else 1)
    if not args:
        raise SystemExit(__doc__)
    packet = None
    if '--packet' in args:
        i = args.index('--packet')
        packet = args[i + 1]
        args = args[:i] + args[i + 2:]
    merge(args[0], packet)
