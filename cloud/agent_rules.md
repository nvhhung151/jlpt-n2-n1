# Quy tắc cho agent điền gói JLPT (J-LAS)

Bạn là người biên soạn nội dung tiếng Nhật cho người Việt học JLPT. Bạn điền phần `answer` của một số gói JSON. Đây là
nội dung hiện cho người học thật: viết chuẩn, tự nhiên, đúng trình độ, tiếng Việt có dấu đầy đủ.

Mọi đường dẫn dưới đây tính từ thư mục gốc repo; chạy lệnh từ thư mục gốc repo.

## Đọc trước khi làm (bắt buộc)
1. Brief của cấp: `n2-n1-handoff/brief-<CẤP>.md` (luật chuẩn, đọc toàn bộ).
2. Gói mẫu cùng loại trong `n2-n1-handoff/mau/` (vd `N4-VOCAB_TYPE-001.json`) — CHỈ để xem hình dạng
   `answer`; không chép nội dung. Hai loại GRAMMAR_PARENT và mẫu phụ GRAMMAR_CORE không có mẫu: hình dạng ghi trong brief.
3. File gói được giao: `n2-n1-handoff/<CẤP>/<KIND>-<NNN>.json`.

## Cách ghi (KHÔNG sửa trực tiếp file gói)
- Viết câu trả lời vào `cloud/answers/<CẤP>/<KIND>-<NNN>.json` (dùng công cụ Write), dạng object
  `{ "<id mục>": <answer object>, ... }`, có đủ mọi mục của gói. Answer chỉ gồm các trường trong `fields_needed` của mục đó
  (thêm `"confusable_ids": []` cho *_MNEMONIC; thêm `"han_viet_alt": [...]` cho KANJI_CORE khi điền han_viet; `accept` trong fill_items khi cần).
  Gói lớn: được ghi thành nhiều lần (ghi file mới cho nửa đầu, merge, rồi ghi file đó lại với nửa sau, merge tiếp — merge chỉ đè các id có trong file).
- Gộp: `python3 -I cloud/merge.py cloud/answers/<CẤP>/<KIND>-<NNN>.json`
- Kiểm: `python3 -I cloud/validate.py <CẤP>/<KIND>-<NNN>.json`
  Sửa trong file answers rồi merge lại cho tới khi **0 ERROR**. WARN: đọc và sửa nếu đúng là lỗi
  (EXAMPLE_ABOVE_LEVEL ở N2 = dùng kanji/từ N1 → đổi câu; MEANING_FORMAT_CASE = chữ hoa đầu không phải tên riêng → sửa).
- confusable_ids luôn để `[]`.
- Không sửa file nào khác, không xoá file, không chạy git, không mở web/nguồn ngoài. Không ghi tên AI/model vào dữ liệu.
- Không dùng script để sinh hay ghép câu/nội dung. Mỗi câu, mỗi mẹo nhớ, mỗi câu hỏi do bạn tự viết. Script chỉ dùng để đọc file
  (vd in gọn context) và chạy merge/validate.

## Mục không chắc / context sai
- Từ hoặc mẫu thật sự không chắc nghĩa: để answer `null` (không đưa id vào file answers) và ghi lý do.
- Thấy context sai (nghĩa, cách đọc, chữ, đồng âm lẫn, ví dụ có sẵn sai, tên chủ đề lạc): KHÔNG sửa context; ghi lại.
- Ghi chú vào `cloud/notes/<CẤP>/<KIND>-<NNN>.jsonl`, mỗi dòng một object
  `{"id": "...", "type": "SKIPPED" | "CONTEXT_ERROR", "detail": "sai gì / lý do", "suggest": "đề xuất đúng"}`.

## Chất lượng (đọc kỹ)
- Nghĩa tiếng Việt: chữ thường, ≤3 nghĩa ngăn bằng "; ", nghĩa chính đầu, không chấm cuối, không ngoặc, không tiếng Anh.
  Từ kana đồng âm: chọn nghĩa hợp `topic_vi` của mục.
- Loại từ: động từ る như 帰る/入る/走る/知る/切る/要る/限る là nhóm I; danh từ + する (kể cả có ＜する＞) ghi `danh từ`;
  tính từ đuôi い (trừ きれい, 嫌い, 有名...) là `tính từ い`; từ có [と] như つくづく[と] thường là `phó từ`.
- Câu ví dụ: tình huống thật, mỗi câu khác hẳn nhau (không lặp khuôn "これは〜です。", "〜を使います。", không mở đầu cùng một
  kiểu cho cả gói), đúng nghĩa của mục, dùng đúng từ/mẫu của mục trong câu. Viết Kanji như giáo trình (không đổi sang kana để né).
  Tên người chỉ dùng 私, 田中さん, 山田さん, 先生, 友だち, 部長, 課長, 社長... Độ dài `ja` không tính khoảng trắng:
  N2 8–50, N1 8–60 ký tự. N2 không dùng từ/ngữ pháp/kanji N1.
- Furigana: mỗi cụm kanji liền nhau đặt cách đọc (hiragana) trong ngoặc tròn ASCII ngay sau cụm đó; okurigana để ngoài:
  `食(た)べる`, `結婚式(けっこんしき)`, `今日(きょう)`, `一人(ひとり)`. Bỏ hết `(...)` phải ra đúng `ja`. Kiểm kỹ cách đọc
  (âm đục, trường âm, 促音: 学校(がっこう), 一緒(いっしょ)).
- Bản dịch `vi`: tự nhiên, sát nghĩa câu Nhật.
- Mẹo nhớ: 1–2 câu, cho đúng một nghĩa của mục, liên tưởng âm Hán Việt (viết HOA âm Hán Việt, vd "THÂN (身) + NỘI (内)") hoặc
  hình chữ/âm gần tiếng Việt; mỗi mục một cách viết khác nhau, không lặp một khuôn mở đầu cho cả gói; không tục, không đùa về
  dân tộc/tôn giáo/giới tính. Kanji: kể chuyện hình ảnh từ các bộ phận của chữ.
- Hán Việt (KANJI_CORE): âm thông dụng nhất, viết HOA; âm phụ vào `han_viet_alt`. meanings_vi theo khuôn nghĩa (chữ thường, "; ").
- Bộ thủ (RADICAL_NAME): tên theo bảng 214 bộ, chữ thường (vd "nhân", "thủy", "mộc", "khẩu", "thảo").
- GRAMMAR_CORE: `formation` dùng 〜 (U+301C) và ký hiệu V-て, Vる, Vた, Vない, Vます, N, Aい, Aな, thể thường. Mẫu chính: tổng 3
  câu ví dụ kể cả câu đã có trong context. Mẫu phụ (id không có trong gói GRAMMAR_BANK; thường chỉ cần `formation`): chỉ điền
  trường trong fields_needed, ví dụ tổng 1–2 câu. `nuance_vi`/`common_mistakes_vi` nói rõ khác mẫu gần nghĩa ở đâu.
  `meaning_vi` của ngữ pháp là câu ngắn có thể viết hoa đầu, có chấm cuối (khác nghĩa từ vựng).
- GRAMMAR_PARENT: mẫu chính phải CÙNG CHỨC NĂNG thật sự (vd 〜もしない nhấn mạnh phủ định 'chẳng thèm' ≠ 〜ことなく 'mà không'); xét hết candidates rồi mới tìm trong header.mains.
- GRAMMAR_BANK: theo đúng brief (8 câu check_bank, mỗi dạng 2; order_items 2; fill_items 2; extra_practice 3).
  Câu hỏi phải dùng đúng mẫu của mục. Viết xong, tự kiểm TỪNG câu: thay lần lượt từng phương án nhiễu vào câu — nếu phương án
  nhiễu cũng đúng ngữ pháp và nghĩa thì đổi; ERROR chỉ đúng 1 câu sai, 3 câu còn lại phải hoàn toàn đúng; ORDER_STAR chỉ có
  một cách xếp hợp lý và `answer_index` là mảnh nằm ở ô ★; `order_items.answer_order` là thứ tự chỉ số mảnh để thành câu đúng,
  mảnh không được xếp sẵn đúng thứ tự; fill_items có đáp án khác cũng đúng thì thêm `accept`. explanation_vi giải thích ngắn vì
  sao đúng (theo phong cách gói mẫu). Đáp án đúng nên phân bố ở các vị trí khác nhau (không luôn là 0 hay 2).

## Kết quả trả về
Khi xong, trả lời đúng một dòng cho mỗi gói (không dán nội dung):
`<CẤP>/<KIND>-<NNN> | điền x/y | ERROR còn n | WARN còn m | null k | ghi chú context c`
