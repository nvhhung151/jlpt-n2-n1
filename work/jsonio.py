"""Doc/ghi goi JSON dung dinh dang JSON.stringify(obj, null, 1) + "\\n" (UTF-8, LF)."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
PKG = os.path.join(ROOT, "n2-n1-handoff")
ORIG = os.path.join(BASE, "orig")


def _escape(s):
    # Giong JSON.stringify: chi escape " \\ va ky tu dieu khien < 0x20; khong escape ky tu khong phai ASCII.
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == '\\':
            out.append('\\\\')
        elif ch == '\b':
            out.append('\\b')
        elif ch == '\f':
            out.append('\\f')
        elif ch == '\n':
            out.append('\\n')
        elif ch == '\r':
            out.append('\\r')
        elif ch == '\t':
            out.append('\\t')
        elif o < 0x20 or 0xD800 <= o <= 0xDFFF:
            out.append('\\u%04x' % o)
        else:
            out.append(ch)
    out.append('"')
    return ''.join(out)


def _num(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return str(v)
    if v != v or v in (float('inf'), float('-inf')):
        return 'null'
    if v == int(v) and abs(v) < 1e21:
        return str(int(v))
    return repr(v)


def stringify(v, indent=1, level=0):
    pad = ' ' * (indent * (level + 1))
    end = ' ' * (indent * level)
    if v is None:
        return 'null'
    if isinstance(v, (bool, int, float)):
        return _num(v)
    if isinstance(v, str):
        return _escape(v)
    if isinstance(v, list):
        if not v:
            return '[]'
        return '[\n' + ',\n'.join(pad + stringify(x, indent, level + 1) for x in v) + '\n' + end + ']'
    if isinstance(v, dict):
        if not v:
            return '{}'
        return '{\n' + ',\n'.join(pad + _escape(k) + ': ' + stringify(x, indent, level + 1) for k, x in v.items()) + '\n' + end + '}'
    raise TypeError(type(v))


def dumps(obj):
    return stringify(obj) + '\n'


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save(path, obj):
    data = dumps(obj).encode('utf-8')
    tmp = path + '.tmp'
    with open(tmp, 'wb') as f:
        f.write(data)
    os.replace(tmp, path)


def packet_path(level, name, orig=False):
    name = name if name.endswith('.json') else name + '.json'
    return os.path.join(ORIG if orig else PKG, level, name)
