# Hướng dẫn soạn gói nội dung JLPT N2 + N1 (J-LAS)

**Hạn nộp: hết ngày 04/11.** Làm cả N2 và N1, gửi lại một lần.

## Trong gói bàn giao có gì

| Thư mục / file | Nội dung |
|---|---|
| `N2/` | 225 gói JSON cấp N2 cần điền |
| `N1/` | 236 gói JSON cấp N1 cần điền |
| `brief-N2.md`, `brief-N1.md` | Luật soạn chi tiết từng cấp (đọc kỹ trước khi làm) |
| `mau/` | 11 gói mẫu đã hoàn thiện và duyệt (lấy từ N4), mỗi loại một gói, để xem đúng hình dạng `answer` |

## Điền gì

- **Chỉ điền phần `answer`** của từng mục: thay `"answer": null` bằng object có đúng các trường trong `fields_needed`.
- Không sửa `id`, `context`, `fields_needed`, `header`, `packet_id`, `kind`, `level`; không đổi tên, thêm hay xóa file.
- Ghi file bằng `JSON.stringify(obj, null, 1) + "\n"` (UTF-8). File phải là JSON hợp lệ.
- Mục không làm được: để `answer: null` và ghi lý do vào báo cáo.

## Thứ tự làm (mỗi cấp, làm N2 trước rồi N1)

1. **Loại ngắn**: `VOCAB_TYPE`, `VOCAB_MEANING`, `TOPIC_ASSIGN`, `KANJI_CORE`, `RADICAL_NAME`, `GRAMMAR_UNIT`.
2. **`GRAMMAR_PARENT`**: gắn mẫu phụ vào một mẫu chính cùng chức năng.
3. **`GRAMMAR_CORE`**: mẫu chính (đủ trường) và mẫu phụ (`header.grammar_role: "SECONDARY"`, chỉ nghĩa, cấu trúc, 1–2 ví dụ).
4. **Mẹo nhớ**: `VOCAB_MNEMONIC`, `KANJI_MNEMONIC`.
5. **Câu ví dụ**: `VOCAB_EXAMPLE`.
6. **`GRAMMAR_BANK`**: câu hỏi luyện tập (làm cuối, khi nghĩa và ví dụ của mẫu đã chắc).

## Tự kiểm

- Luôn kiểm JSON hợp lệ cho mỗi file đã sửa:
  `node -e "JSON.parse(require('fs').readFileSync('<file>','utf8'))"`.
- Nếu bạn làm trên máy có sẵn repo J-LAS đã cài bộ biên dịch: chép các gói đã điền vào
  `data/learning-path/authoring/N2/` (hoặc `N1/`) của repo, rồi chạy lệnh tự kiểm ghi trong `brief-N2.md` / `brief-N1.md`
  (mục "Tự kiểm") từ thư mục gốc repo, đọc `target/check-n2/errors.json` (hoặc `check-n1`) và sửa lỗi thuộc phần bạn soạn.
- Không có repo: chỉ cần kiểm JSON hợp lệ và tự rà theo luật trong brief; bên nhận sẽ chạy bộ kiểm đầy đủ.

## Bỏ qua

- **Kanji `突く` (id `JK-7A81`)**: dữ liệu nguồn bị lỗi (một mục Kanji ghi cả chữ kèm okurigana). Mục này đã được gỡ khỏi
  `N2/KANJI_CORE-001.json` và `N2/KANJI_MNEMONIC-008.json` trong gói bàn giao — **bỏ qua**, không thêm lại.
  (Động từ 突く trong các gói từ vựng là một từ bình thường, vẫn soạn như thường.)

## Nộp lại

- Gửi lại **một lần**, đúng cấu trúc thư mục này: `N2/` và `N1/` với các file đã điền (cùng tên file), kèm một file báo cáo ngắn
  `BAO-CAO.md`: số mục đã điền theo từng file, mục bỏ trống + lý do, sai sót thấy trong `context` (id, sai gì, đề xuất đúng).
- Không cần gửi lại `mau/` và các brief.
