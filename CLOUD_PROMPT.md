# Prompt cho phiên Claude Code chạy tiếp (dán nguyên khối dưới)

```text
Repo này chứa gói nội dung lộ trình JLPT N2 + N1 của J-LAS cần điền phần "answer". Mọi lệnh chạy từ thư mục gốc repo. Đọc TIEN-DO.md trước.

Phạm vi phiên này (người khác làm phần còn lại, KHÔNG đụng vào):
- N1: TẤT CẢ gói còn mục chưa điền (n2-n1-handoff/N1/).
- N2: CHỈ 5 loại GRAMMAR_CORE, VOCAB_MNEMONIC, KANJI_MNEMONIC, VOCAB_EXAMPLE, GRAMMAR_BANK (tất cả gói, kể cả 001).
- KHÔNG sửa gói N2 thuộc VOCAB_TYPE, VOCAB_MEANING, TOPIC_ASSIGN, KANJI_CORE, RADICAL_NAME, GRAMMAR_UNIT, GRAMMAR_PARENT, và KHÔNG sửa thư mục work/ (công cụ của phần N2 ngắn).

Cách làm:
1. Đọc cloud/agent_rules.md, n2-n1-handoff/HUONG-DAN.md, brief-N2.md, brief-N1.md. Công cụ: cloud/merge.py, cloud/validate.py, cloud/status.py (chạy bằng python3 -I). Không sửa 3 script này và work/orig/.
2. Xem tiến độ: python3 -I cloud/status.py
3. Giao việc cho subagent, chạy 8 subagent song song. Mỗi subagent nhận 2–3 gói cùng loại (GRAMMAR_BANK: 1 gói), với prompt:
   "Đọc và làm đúng theo cloud/agent_rules.md. Cấp: <CẤP>. Gói được giao: <danh sách>. Làm lần lượt từng gói, mỗi gói merge + validate tới 0 ERROR. Trả về mỗi gói đúng một dòng kết quả như quy định."
   Model subagent: sonnet cho mọi loại, TRỪ GRAMMAR_CORE và GRAMMAR_BANK dùng model mạnh nhất hiện có.
4. Thứ tự: N1 trước theo owner: VOCAB_TYPE, VOCAB_MEANING, TOPIC_ASSIGN, KANJI_CORE, RADICAL_NAME, GRAMMAR_UNIT → GRAMMAR_PARENT → GRAMMAR_CORE → VOCAB_MNEMONIC, KANJI_MNEMONIC → VOCAB_EXAMPLE → GRAMMAR_BANK. Sau đó N2 (5 loại): GRAMMAR_CORE → VOCAB_MNEMONIC, KANJI_MNEMONIC → VOCAB_EXAMPLE → GRAMMAR_BANK.
   GRAMMAR_BANK của một cấp chỉ chạy khi GRAMMAR_CORE cấp đó xong (đọc lại GRAMMAR_CORE đã điền của cùng mẫu để thống nhất nghĩa).
5. Phiên chính KHÔNG tự điền nội dung, KHÔNG đọc nội dung gói vào context; chỉ giao việc, đọc dòng kết quả, chạy status/validate.
6. Cứ khoảng 20 gói xong: python3 -I cloud/validate.py --all --quiet, rồi git pull --no-rebase && git add -A && git commit -m "Điền gói: <tóm tắt>" && git push. Subagent nào báo còn ERROR hoặc gói còn mục chưa điền mà không có ghi chú lý do → giao lại.
7. Xong hết: validate --all (0 ERROR), status, cập nhật bảng trong TIEN-DO.md, commit + push, báo bảng status và tổng số ghi chú trong cloud/notes/.
Không chạy git ngoài pull/add/commit/push trên nhánh hiện tại. Không mở web/nguồn ngoài.
```
