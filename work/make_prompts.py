"""Sinh file huong dan cho tung goi (work/prompts/<CAP>/<GOI>.txt) va file tham chieu work/ref/.
Chi ghep huong dan, khong sinh noi dung goi."""
import glob
import json
import os
from collections import defaultdict

from jsonio import BASE, ORIG

TEMPLATE = open(os.path.join(BASE, 'AGENT-PROMPT.txt'), encoding='utf-8').read()

KIND_RULES = {
    'VOCAB_TYPE': """- VOCAB_TYPE: xét cách dùng thật của từ (xem context.examples, meaning_vi). Cụm nhiều từ/thành ngữ → "cụm từ". Từ chỉ dùng như phó từ → "phó từ". Tính từ đuôi い thật (高い) là "tính từ い"; きれい/有名/嫌い là "tính từ な".""",
    'VOCAB_MEANING': """- VOCAB_MEANING: nghĩa ngắn, tự nhiên như từ điển tốt; nghĩa chính đầu; theo topic_vi của mục; tối đa 3 nghĩa. TUYỆT ĐỐI KHÔNG dùng ngoặc ( ) （ ） [ ] trong meaning_vi (lỗi chặn): thay vì "gọi lại (người đang đi)" viết "gọi lại người đang đi".""",
    'TOPIC_ASSIGN': """- TOPIC_ASSIGN: chép ĐÚNG một cặp {topic_key, topic_vi} từ header.topics (gần nghĩa nhất với nghĩa chính của từ). Không hợp chủ đề nào: {"topic_key": "khac", "topic_vi": "Từ thông dụng khác"}.""",
    'KANJI_CORE': """- KANJI_CORE: chỉ trường trong fields_needed. han_viet: âm Hán Việt thông dụng nhất, viết HOA (vd ĐỘC). meanings_vi: nghĩa tiếng Việt, chữ thường, tối đa 3 nghĩa ngăn "; ", KHÔNG có ngoặc ( ) （ ） [ ]. Chữ có 2 âm Hán Việt thông dụng hoặc chưa chắc âm nào chính: han_viet một âm, âm còn lại vào "han_viet_alt": ["..."] (HOA) và ghi notes type "uncertain".""",
    'RADICAL_NAME': """- RADICAL_NAME: name_vi là tên bộ thủ tiếng Việt theo bảng 214 bộ (context.number là số thứ tự bộ, sample_kanji là chữ có bộ đó), chữ thường, vd "nhân", "thủy", "mộc", "khẩu". Chỉ tên, không kèm số hay giải thích.""",
    'GRAMMAR_UNIT': """- GRAMMAR_UNIT: unit_no phải thuộc header.units. Tham chiếu các mẫu CHÍNH đã nằm trong từng bài: D:\\project\\jlpt-n2-n1\\work\\ref\\{LEVEL}-units.json ({unit_no: [{pattern, meaning_vi}]}). Mẫu cùng chức năng với mẫu đã có trong bài nào thì vào bài đó; mẫu càng cơ bản càng vào bài nhỏ. unit_title_vi: để null (tên bài thống nhất sẽ đặt sau, tránh các gói đặt tên khác nhau cho cùng một bài).""",
    'GRAMMAR_PARENT': """- GRAMMAR_PARENT: mỗi mục là một MẪU PHỤ. parent_id = id một mẫu CHÍNH cùng chức năng/nghĩa (ưu tiên trong context.candidates; không hợp thì tìm trong header.mains). Không chọn id mẫu phụ, không chọn chính nó. Dựa vào pattern, meaning_vi, examples của mục để so chức năng. CHỈ chọn mẫu cùng chức năng THẬT SỰ (vd 〜もしない "chẳng thèm, thậm chí không" là nhấn mạnh phủ định → không gắn vào 〜ことなく "mà không"). Đọc hết header.mains, không chỉ candidates. Nếu không có mẫu chính nào thật sự cùng chức năng: chọn mẫu gần nhất và ghi notes {"id", "type": "uncertain", "issue": "...", "suggest": "..."}.""",
    'GRAMMAR_CORE': """- GRAMMAR_CORE: header.grammar_role = "SECONDARY" là mẫu phụ, không có hoặc khác là mẫu CHÍNH. Mỗi mục chỉ điền trường trong fields_needed của mục đó.
  - formation: dùng ký hiệu 〜 (U+301C), V-て, Vる, Vた, Vない, Vます, N, Aい, Aな; vd "N + にあたって", "Vる / N の + 際に".
  - meaning_vi: câu ngắn tiếng Việt (viết hoa đầu câu, có thể có dấu chấm). Nếu context.meaning_vi đã có thì giữ thống nhất ý đó.
  - usage_vi (1–2 câu: khi nào dùng), nuance_vi (1 câu: sắc thái, trang trọng, văn viết/nói, và khác mẫu gần nghĩa ở đâu), common_mistakes_vi (1–2 câu: người Việt hay nhầm gì, nhầm với mẫu gần nghĩa nào, vì sao sai).
  - examples (mẫu CHÍNH): tổng ĐÚNG 3 câu kể cả context.examples → viết 3 − (số câu có sẵn) câu mới. Mẫu PHỤ: tổng 1–2 câu kể cả câu có sẵn (viết 1–2 câu mới khi chưa có câu nào). Câu ví dụ phải dùng đúng mẫu ngữ pháp của mục, tự nhiên.""",
    'VOCAB_MNEMONIC': """- VOCAB_MNEMONIC: {"mnemonic_vi": "...", "confusable_ids": []}. Mẹo giúp nhớ ĐÚNG nghĩa chính của mục (theo meaning_vi/topic_vi): ghép âm Hán Việt của từng chữ Kanji ra nghĩa, hoặc liên tưởng âm đọc gần tiếng Việt, hoặc hình ảnh. Không chỉ nhắc lại nghĩa. Đa dạng cách mở đầu.""",
    'KANJI_MNEMONIC': """- KANJI_MNEMONIC: {"mnemonic_vi": "...", "confusable_ids": []}. Câu chuyện hình ảnh từ các bộ phận thật của chữ (bộ thủ + phần còn lại) dẫn tới nghĩa và gắn âm Hán Việt (context.han_viet). Bộ phận phải đúng với chữ. Đa dạng cách mở đầu.""",
    'VOCAB_EXAMPLE': """- VOCAB_EXAMPLE: viết 1–2 câu mới cho mỗi mục (tổng không quá 3 kể cả câu có sẵn). Câu phải dùng đúng từ của mục (expression, có thể chia thể) với đúng nghĩa meaning_vi/topic_vi. Mỗi câu một bối cảnh thật (gia đình, công việc, tin tức, trường học...), không lặp khuôn giữa các mục.""",
    'GRAMMAR_BANK': """- GRAMMAR_BANK: mỗi mục là một mẫu CHÍNH (id trùng id trong GRAMMAR_CORE). TRƯỚC KHI VIẾT, đọc answer đã điền của cùng id trong D:\\project\\jlpt-n2-n1\\n2-n1-handoff\\{LEVEL}\\GRAMMAR_CORE-*.json (tìm theo id; dùng python chỉ để đọc/tìm) để thống nhất nghĩa, cấu trúc, sắc thái.
  - check_bank: đúng 8 câu, mỗi dạng FILL, ORDER_STAR, MEANING, ERROR đúng 2 câu; mỗi câu {type, prompt_ja, options (4 chuỗi khác nhau), answer_index 0–3, explanation_vi}. Phân bố answer_index đa dạng.
    - FILL: prompt_ja có 「（　　）」; 4 phương án; chỉ 1 đúng.
    - ORDER_STAR: prompt_ja dạng 「…＿＿ ＿＿ ★ ＿＿…」 có đúng 4 ô (3 ＿＿ + 1 ★); options là 4 mảnh; answer_index là mảnh ở ô ★ khi xếp đúng. Tự xếp lại để chắc chỉ có 1 cách xếp đúng.
    - MEANING: prompt_ja là câu dùng mẫu; options là 4 câu nghĩa tiếng Việt; 1 đúng.
    - ERROR: prompt_ja = "Câu nào dùng sai mẫu?"; options là 4 câu tiếng Nhật, đúng 1 câu dùng mẫu SAI; answer_index chỉ câu sai đó.
    - explanation_vi: giải thích vì sao đúng/sai, kèm nghĩa câu.
  - Viết xong, kiểm lại TỪNG câu: thử thay từng phương án nhiễu vào câu; phương án nhiễu nào cũng đúng (kể cả mẫu gần nghĩa) thì phải đổi. Không 2 lựa chọn trùng.
  - order_items: 2 bài {pieces (3–5 mảnh), answer_order (hoán vị chỉ số mảnh theo thứ tự đúng), translation_vi}; chọn câu có trật tự duy nhất; mảnh không để sẵn đúng thứ tự.
  - fill_items: 2 bài {sentence_ja có 「＿＿」, answer, translation_vi}; có đáp án khác cũng đúng thì thêm "accept": [...].
  - extra_practice: 3 câu cùng định dạng check_bank (dạng tùy chọn), khác các câu trong check_bank.""",
}

LEVEL_RULE = {'N2': ' (N5 + N4 + N3 + N2; KHÔNG dùng từ/ngữ pháp/Kanji N1)', 'N1': ' (toàn bộ JLPT N5→N1)'}
LEN = {'N2': '8–50 ký tự', 'N1': '8–60 ký tự'}


def write_refs():
    os.makedirs(os.path.join(BASE, 'ref'), exist_ok=True)
    for lv in ('N2', 'N1'):
        units = defaultdict(list)
        for f in sorted(glob.glob(os.path.join(ORIG, lv, 'GRAMMAR_CORE-*.json'))):
            d = json.load(open(f, encoding='utf-8'))
            if d['header'].get('grammar_role') == 'SECONDARY':
                continue
            for it in d['items']:
                u = it['context'].get('unit_no')
                if u:
                    units[u].append({'pattern': it['context']['pattern'], 'meaning_vi': it['context'].get('meaning_vi')})
        with open(os.path.join(BASE, 'ref', f'{lv}-units.json'), 'w', encoding='utf-8') as fh:
            json.dump({str(k): units[k] for k in sorted(units)}, fh, ensure_ascii=False, indent=1)


def render(level, packet):
    kind = packet.rsplit('-', 1)[0]
    extra = ''
    if kind == 'GRAMMAR_UNIT':
        extra = f'- Tham chiếu bài: D:\\project\\jlpt-n2-n1\\work\\ref\\{level}-units.json\n'
    text = (TEMPLATE.replace('{KIND_RULES}', KIND_RULES[kind] + '\n').replace('{EXTRA_PATHS}', extra)
            .replace('{LEVEL_RULE}', LEVEL_RULE[level]).replace('{LEN}', LEN[level]))
    return text.replace('{LEVEL}', level).replace('{PACKET}', packet).replace('{KIND}', kind)


if __name__ == '__main__':
    write_refs()
    n = 0
    for lv in ('N2', 'N1'):
        os.makedirs(os.path.join(BASE, 'prompts', lv), exist_ok=True)
        os.makedirs(os.path.join(BASE, 'notes', lv), exist_ok=True)
        for f in sorted(glob.glob(os.path.join(ORIG, lv, '*.json'))):
            packet = os.path.basename(f)[:-5]
            with open(os.path.join(BASE, 'prompts', lv, packet + '.txt'), 'w', encoding='utf-8') as fh:
                fh.write(render(lv, packet))
            n += 1
    print('prompts', n)
