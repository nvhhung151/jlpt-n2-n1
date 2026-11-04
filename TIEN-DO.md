# Tiến độ điền gói JLPT N2 + N1 (J-LAS)

Hạn gốc: 04/11. Nộp cho owner luồng Learning: thư mục `N2/`, `N1/` đã điền (giữ tên file) + `BAO-CAO.md`.
Luật soạn: `n2-n1-handoff/HUONG-DAN.md`, `brief-N2.md`, `brief-N1.md`. Chỉ điền `answer`.

## Chia việc

| Phần | Ai làm | Công cụ | Trạng thái (cập nhật 04/11 11:12) |
|---|---|---|---|
| N2 – 7 loại ngắn: VOCAB_TYPE, VOCAB_MEANING, TOPIC_ASSIGN, KANJI_CORE, RADICAL_NAME, GRAMMAR_UNIT, GRAMMAR_PARENT | Hùng (Claude Code trên máy) | `work/` | **xong** 3.440/3.450 mục (10 null có lý do), 0 lỗi |
| N1 – gói 001 của 12 loại | xong | `cloud/` | 450 mục, 0 lỗi |
| N1 – toàn bộ phần còn lại (224 gói) | **cần người chạy tiếp** | `cloud/` | chưa làm |
| N2 – 5 loại nặng: GRAMMAR_CORE, VOCAB_MNEMONIC, KANJI_MNEMONIC, VOCAB_EXAMPLE, GRAMMAR_BANK (134 gói) | **cần người chạy tiếp** | `cloud/` | chưa làm |

Hai bộ công cụ `work/` và `cloud/` sửa các file gói KHÁC nhau, không đè nhau. Đừng sửa gói thuộc phần của người khác.

Tổng: 3.890/16.713 mục. Còn lại 12.823 mục, đều thuộc phần `cloud/` bên dưới.

## Chạy tiếp phần còn lại (Claude Code, trên web hoặc trên máy)

1. Mở Claude Code trên repo này (claude.ai/code → chọn repo, hoặc clone về rồi chạy `claude` ở thư mục gốc).
2. Dán prompt trong `CLOUD_PROMPT.md`.
3. Xem tiến độ: `python3 -I cloud/status.py`. Kiểm lỗi: `python3 -I cloud/validate.py --all --quiet`.
4. Phiên đó tự commit + push sau mỗi khoảng 20 gói.

Trước khi push từ máy khác: `git pull --no-rebase` rồi mới `git push`.

## Ghi chú sai sót trong context
`work/notes/` (phần N2 ngắn) và `cloud/notes/<CẤP>/` (phần còn lại): mỗi dòng `{id, type, detail, suggest}`. Gom vào `BAO-CAO.md` khi nộp.
