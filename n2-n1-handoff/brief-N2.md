# Brief: soạn gói nội dung lộ trình JLPT N2 (J-LAS)

> Bản N2, dựa trên brief N3, giữ toàn bộ các bài học rút ra từ N5, N4, N3 (các mục cuối).

Bạn là người biên soạn nội dung tiếng Nhật cho người Việt học JLPT N2 trên web J-LAS. Bạn điền phần `answer` của các
gói JSON được giao. Đây là nội dung sẽ hiện cho người học thật — viết chuẩn, tự nhiên, đúng trình độ.

## Phạm vi và cấm

- Thư mục làm việc: thư mục gốc repo J-LAS (xem HUONG-DAN.md). Gói nằm ở thư mục `N2/` của gói bàn giao (trong repo: `data/learning-path/authoring/N2/`).
- **Chỉ sửa các file gói được giao cho bạn.** Không sửa file nào khác (nhất là không đụng `data/learning-path/authoring/N3/`
  đang có người khác soạn), không chạy git (commit/stash/checkout/add), không xóa file.
- Trong mỗi gói: với từng mục, thay `"answer": null` bằng object chứa đúng các trường trong `fields_needed` (theo luật dưới).
  Giữ nguyên `id`, `context`, `fields_needed`, `header`, `packet_id`, `kind`, `level`. File phải là JSON hợp lệ.
- **Không mở** bất kỳ nguồn dữ liệu ngoài, website hay sách nào để chép, và không mở các thư mục trong `target/` (trừ thư
  mục kiểm `target/check-n2/` và thư mục mẫu `mau/`). Nội dung phải do bạn tự viết.
- Không ghi tên AI/model nào vào dữ liệu.
- Mục nào thật sự không làm được (vd từ lạ không chắc nghĩa): để `answer: null` và ghi lý do trong báo cáo cuối.

## Mẫu câu trả lời

`mau/` có một gói mẫu cho mỗi loại (lấy từ N4, 5 mục đầu, `answer` là giá trị cuối cùng đã duyệt).
Xem để biết **đúng hình dạng** `answer` của từng loại. Không chép nội dung mẫu vào gói N2.
Hai loại chỉ có ở cấp có mẫu chính/phụ nên không có mẫu N4 — hình dạng:
- `GRAMMAR_PARENT`: `{ "parent_id": "JG-xxxxxxxxxx" }`.
- `GRAMMAR_CORE` mẫu phụ (`header.grammar_role: "SECONDARY"`): chỉ các trường trong `fields_needed` trong số
  `{ "meaning_vi": "...", "formation": "...", "examples": [ { "ja", "ja_furigana", "vi" } ] }` (1–2 câu, tính cả câu đã có).

## Luật chung

- **Nghĩa tiếng Việt** (`meaning_vi`): chữ thường (trừ tên riêng), tối đa 3 nghĩa ngăn bởi `"; "`, nghĩa chính đứng đầu,
  không dấu chấm cuối, không ngoặc tiếng Anh. Vd `"tôi; mình"`.
- **Loại từ** (`word_type_label`): đúng một trong: `danh từ`, `động từ nhóm I`, `động từ nhóm II`, `động từ nhóm III`,
  `tính từ い`, `tính từ な`, `phó từ`, `trợ từ`, `liên từ`, `thán từ`, `cụm từ`, `số từ`, `đại từ`.
  (Chú ý động từ る: 帰る, 入る, 走る, 知る, 切る... là nhóm I; する/来る và danh từ + する là nhóm III; きれい, 有名 là tính từ な.)
- **Câu ví dụ** (`examples`: mảng `{ "ja", "ja_furigana", "vi" }`):
  - Chỉ dùng từ vựng và ngữ pháp trình độ N5 + N4 + N3 + N2. Không dùng từ/ngữ pháp N1.
  - Độ dài `ja` (không tính khoảng trắng): 8–50 ký tự.
  - `ja_furigana`: viết đúng câu `ja`, mỗi cụm Kanji theo sau là cách đọc trong ngoặc tròn ASCII, vd
    `"学校(がっこう)へ行(い)きます。"`. **Xóa hết phần `(...)` phải ra đúng y hệt `ja`** (kể cả dấu câu, khoảng trắng).
  - Câu tự nhiên, ngữ cảnh đời thường/công việc/xã hội hợp trình độ N2; không tên riêng lạ (dùng 私, 田中さん, 山田さん,
    先生, 友だち, 部長, 会社...). `vi` dịch tự nhiên.
- **Mẹo nhớ** (`mnemonic_vi`): 1–2 câu tiếng Việt, giúp nhớ thật sự: liên tưởng âm Hán Việt (từ có Kanji) hoặc âm gần
  tiếng Việt, hoặc hình ảnh; không tục, không phản cảm, không đùa về dân tộc/tôn giáo.

## Luật theo loại gói (`kind`)

- `VOCAB_TYPE`: `{ "word_type_label": "..." }`.
- `VOCAB_MEANING`: `{ "meaning_vi": "..." }`.
- `VOCAB_EXAMPLE`: `{ "examples": [ ... ] }` — 1 câu chính bắt buộc, thêm tối đa 2 câu nếu muốn (tổng không quá 3 kể cả câu đã có trong `context.examples`). Không lặp câu đã có.
- `VOCAB_MNEMONIC`: `{ "mnemonic_vi": "...", "confusable_ids": [] }` — `confusable_ids` tùy chọn: id các từ N2 (hoặc N3/N4/N5 trong `data/learning-path/compiled/N3.json`, `N4.json`, `N5.json`) rất dễ nhầm (cùng cách đọc khác nghĩa, mặt chữ giống), lấy id từ `data/learning-path/compiled/N2.json` (mảng `vocabulary`). Không chắc thì để `[]`.
- `KANJI_MNEMONIC`: `{ "mnemonic_vi": "...", "confusable_ids": [] }` — câu chuyện hình ảnh từ các bộ phận của chữ (vd 休: người 亻 tựa cây 木 → nghỉ). `confusable_ids`: id Kanji dạng `JK-XXXX` dễ nhầm hình (vd 待/持) có trong `compiled/N2.json` (mảng `kanji`) hoặc cấp thấp hơn, hoặc `[]`.
- `RADICAL_NAME`: `{ "name_vi": "..." }` — tên bộ thủ tiếng Việt theo bảng 214 bộ (vd số 9 亻/人 "nhân", 85 氵/水 "thủy", 75 "mộc"). `context.number` là số thứ tự bộ, `sample_kanji` là một chữ có bộ đó.
- `TOPIC_ASSIGN`: `{ "topic_key": "...", "topic_vi": "..." }` — chọn chủ đề gần nghĩa nhất trong `header.topics` (chép đúng cặp key/vi). Không hợp chủ đề nào: `"khac"` / `"Từ thông dụng khác"`.
- `KANJI_CORE`: `{ "han_viet": "...", "han_viet_alt": [], "meanings_vi": "..." }` — chỉ các trường trong `fields_needed` (xem luật Hán Việt ở mục cuối).
- `GRAMMAR_UNIT`: `{ "unit_no": <số>, "unit_title_vi": "..." }` — xếp mẫu vào một bài trong `header.units` (bài 1 = cơ bản nhất). Mẫu càng cơ bản càng vào bài nhỏ; mẫu cùng chức năng với mẫu đã có trong bài nào thì vào bài đó. `unit_title_vi` ngắn hoặc `null`.
- `GRAMMAR_CORE` (mẫu chính): chỉ điền các trường trong `fields_needed`:
  `meaning_vi` (câu ngắn tiếng Việt), `formation` (ký hiệu: `〜` U+301C, `V-て`, `Vる`, `Vた`, `Vない`, `N`, `Aい`, `Aな`; vd `"N + にあたって"`),
  `usage_vi` (khi nào dùng, 1–2 câu), `nuance_vi` (sắc thái/độ trang trọng, văn viết hay văn nói, 1 câu), `common_mistakes_vi` (lỗi người Việt hay mắc, nhầm với mẫu gần nghĩa, 1–2 câu),
  `examples` (đủ 3 câu tổng cộng kể cả câu đã có, theo luật câu ví dụ).
- `GRAMMAR_BANK`: điền các trường trong `fields_needed`, tất cả dùng từ vựng N5 + N4 + N3 + N2:
  - `check_bank`: **đúng 8 câu**, mỗi dạng 2 câu: `FILL`, `ORDER_STAR`, `MEANING`, `ERROR`. Mỗi câu
    `{ "type", "prompt_ja", "options": [4 chuỗi], "answer_index": 0-3, "explanation_vi" }`.
    - `FILL`: câu có chỗ trống `（　　）`, 4 lựa chọn, chỉ 1 đúng.
    - `ORDER_STAR`: `prompt_ja` là câu với 4 ô `＿＿ ＿＿ ★ ＿＿` (★ ở đúng 1 vị trí); `options` là 4 mảnh; `answer_index` là mảnh nằm ở ô ★ khi xếp đúng.
    - `MEANING`: `prompt_ja` là câu dùng mẫu; `options` là 4 câu nghĩa tiếng Việt; 1 đúng.
    - `ERROR`: `options` là 4 câu tiếng Nhật; đúng 1 câu dùng mẫu SAI; `answer_index` chỉ câu sai đó; `prompt_ja` = "Câu nào dùng sai mẫu?".
    - Đáp án nhiễu phải sai rõ ràng, **không được cũng đúng**; không có 2 lựa chọn trùng nhau.
  - `order_items`: 2 bài xếp câu `{ "pieces": [3–5 mảnh], "answer_order": [chỉ số mảnh theo thứ tự đúng], "translation_vi" }`.
  - `fill_items`: 2 bài điền `{ "sentence_ja": "... ＿＿ ...", "answer": "...", "translation_vi" }`.
  - `extra_practice`: 3 câu cùng định dạng `check_bank` (dạng tùy chọn), khác các câu trong `check_bank`.

## Tự kiểm (bắt buộc trước khi báo xong)

1. Mỗi file gói bạn sửa phải parse được: `node -e "JSON.parse(require('fs').readFileSync('<file>','utf8'))"`.
2. Chạy bộ kiểm vào thư mục kiểm riêng:
   ```
   node tools/learning-path-source/compile/build_level_source.mjs --level N2 --out target/check-n2/N2.json --report-dir target/check-n2 --errors-json target/check-n2/errors.json
   ```
   Rồi lọc lỗi theo id các mục trong gói của bạn (đọc `errors.json`, mảng `{code,id,detail,warning}`). Sửa các lỗi
   thuộc phần bạn soạn: `EXAMPLE_ABOVE_LEVEL`, `EXAMPLE_LENGTH`, `FURIGANA_MISMATCH`, `MEANING_FORMAT`, `GRAMMAR_BANK_SHORT`,
   `DISTRACTOR_ALSO_CORRECT`, và mã lỗi kết thúc bằng `_SIMILAR` (câu hoặc nghĩa quá giống một nguồn ngoài → viết lại theo
   cách của bạn). Bỏ qua lỗi thuộc trường người khác soạn (vd bạn soạn loại từ thì bỏ qua MNEMONIC_MISSING).
   Nếu lệnh lỗi vì một file gói khác đang được người khác ghi dở (JSON parse error), đợi một chút rồi chạy lại.
3. Báo cáo cuối (ngắn): số mục đã điền theo từng file, mục bỏ trống + lý do, số lỗi còn lại thuộc phần bạn, các sai sót
   thấy trong `context` (id, sai gì, đề xuất đúng).

## Thêm cho N2 (bài học từ N5, N4 — bắt buộc)

- **Viết chữ như giáo trình**: từ thường viết Kanji thì viết Kanji (行きました, 来ない, 練習, 注文); KHÔNG đổi sang kana/số Ả Rập
  để né bộ kiểm. Bộ kiểm cấp đã đọc câu đúng cách: chỉ báo **chặn** khi có Kanji/từ có Kanji trên cấp
  (`EXAMPLE_ABOVE_LEVEL`) → khi đó mới đổi từ hoặc viết kana. `EXAMPLE_KANA_ABOVE_LEVEL` chỉ là cảnh báo. Tên giáo trình
  (山田さん, 田中さん...) được phép.
- **Nghĩa theo chủ đề**: một từ kana có nhiều nghĩa đồng âm → viết theo nghĩa hợp `topic_vi` của mục. Thấy nghĩa/cách đọc/chữ
  sẵn có trong context sai (đồng âm lẫn, lỗi chính tả, nghĩa lạc) thì **không sửa vào gói** (không phải trường của bạn) mà
  ghi vào báo cáo: id, sai gì, đề xuất đúng — lượt duyệt 2 sẽ sửa.
- **Mẹo nhớ** viết theo đúng một nghĩa của mục, không "hợp cả hai nghĩa".
- **KANJI_CORE** (`han_viet`, `han_viet_alt`, `meanings_vi`): `han_viet` là âm Hán Việt **thông dụng nhất**, viết HOA (読 ĐỘC,
  校 HIỆU, 生 SINH...); âm phụ vào `han_viet_alt` (mảng, HOA).
- **Bài điền (`fill_items`)**: khi có đáp án khác cũng đúng (ぐらい/くらい, けど/が, だから/ですから...) thêm
  `"accept": ["..."]` vào bài đó.
- **ORDER_STAR**: tự xếp lại câu để chắc mảnh ở ô ★ chỉ có một khả năng; `order_items` có trạng từ thời gian đảo được thì
  chọn câu mà trật tự là duy nhất.
- Ghi file gói bằng `JSON.stringify(obj, null, 1) + "\n"`, chỉ đổi `answer`.

## Thêm cho N2 (bài học từ N4, N3 — bắt buộc)

- **Không viết theo khuôn**: không lặp một mẫu câu cho nhiều từ (vd "これは〜です。", "〜を使います。"); mỗi ví dụ là một tình
  huống thật, tự nhiên, đúng nghĩa của mục. Không sinh câu/bài bằng script ghép chữ — mỗi câu tự viết.
- Từ ngoài hàng học (`queue: "EXTRA"`, trạng thái HOLD) **không có gói** — đừng tạo thêm. N2 có 2.000 từ trong hàng học;
  mọi Kanji N2 đều trong hàng học.
- Ngữ pháp N2 có **mẫu chính** (MAIN, soạn đủ) và **mẫu phụ** (SECONDARY, `header.grammar_role: "SECONDARY"`: chỉ
  `meaning_vi`, `formation`, 1–2 ví dụ khi chưa có; không viết usage/nuance/lỗi thường gặp, không câu hỏi). `GRAMMAR_PARENT`:
  chọn `parent_id` là id một mẫu chính **cùng chức năng** (ưu tiên trong `context.candidates`; không có thì tìm trong
  `header.mains`). Không chọn id của một mẫu phụ.
- Mẫu N2 nhiều cặp gần nghĩa (〜にあたって/〜に際して, 〜をめぐって/〜について...): `nuance_vi` và `common_mistakes_vi` nên nói rõ
  khác nhau ở đâu; đáp án nhiễu dùng mẫu gần nghĩa phải **thật sự sai** trong câu đó, nếu không thì đổi câu.
