# Báo cáo điền gói N2–N1 (lộ trình JLPT)

Ngày: 2026-11-07. Người làm: HungNVH, nội dung soạn với hỗ trợ AI, đã tự kiểm bằng script.

## Tóm tắt

- Đã điền **16,630/16,713** mục (461 gói). **83 mục để null**, mục nào cũng có lý do (bảng dưới).
- Chỉ điền trường `answer`; không đổi id, context, fields_needed, header, tên file. Kanji 突く JK-7A81 bỏ qua theo HUONG-DAN.
- Kiểm bằng script riêng (`cloud/validate.py`): 0 lỗi chặn. Đã kiểm: JSON, đủ/đúng trường, nhãn loại từ, khuôn nghĩa, furigana khớp `ja`, độ dài câu (N2 ≤50, N1 ≤60), số câu ví dụ, Hán Việt viết HOA, cặp chủ đề, unit_no, parent_id thuộc mains, bộ câu hỏi (8 câu đủ 4 dạng, 4 phương án khác nhau, ★, （　　）, order/fill/extra_practice), lặp khuôn, tên AI.
- **Chưa chạy** `build_level_source.mjs` (không có trong repo nhận được) → `EXAMPLE_ABOVE_LEVEL` và `*_SIMILAR` mới kiểm một phần (đối chiếu danh sách kanji/từ N1 trong gói). Còn 225 cảnh báo vượt cấp, hầu hết do chính chữ của từ/mẫu đang soạn (vd 妊娠, 派遣, 次第) — đã giữ nguyên chữ theo brief.
- `confusable_ids` để `[]` toàn bộ (không có compiled list để lấy id hợp lệ).
- GRAMMAR_UNIT N2: `unit_title_vi` để null (giữ tên bài có sẵn); N1 có thêm tên bài 15–18.

## Số mục theo loại

| Cấp | Loại | Đã điền / Tổng |
|---|---|---|
| N1 | GRAMMAR_BANK | 161/162 |
| N1 | GRAMMAR_CORE | 456/458 |
| N1 | GRAMMAR_PARENT | 243/292 |
| N1 | GRAMMAR_UNIT | 69/69 |
| N1 | KANJI_CORE | 95/95 |
| N1 | KANJI_MNEMONIC | 600/600 |
| N1 | RADICAL_NAME | 128/128 |
| N1 | TOPIC_ASSIGN | 608/608 |
| N1 | VOCAB_EXAMPLE | 1524/1528 |
| N1 | VOCAB_MEANING | 737/738 |
| N1 | VOCAB_MNEMONIC | 1999/2000 |
| N1 | VOCAB_TYPE | 1964/1964 |
| N2 | GRAMMAR_BANK | 210/210 |
| N2 | GRAMMAR_CORE | 776/778 |
| N2 | GRAMMAR_PARENT | 488/489 |
| N2 | GRAMMAR_UNIT | 91/91 |
| N2 | KANJI_CORE | 6/6 |
| N2 | KANJI_MNEMONIC | 309/309 |
| N2 | RADICAL_NAME | 105/105 |
| N2 | TOPIC_ASSIGN | 904/904 |
| N2 | VOCAB_EXAMPLE | 1317/1324 |
| N2 | VOCAB_MEANING | 167/170 |
| N2 | VOCAB_MNEMONIC | 1994/2000 |
| N2 | VOCAB_TYPE | 1679/1685 |

## Ghi chú về context (file `GHI-CHU-CONTEXT.jsonl` đi kèm)

Mỗi dòng: `{level, packet, id, type, detail, suggest}`. Không sửa context, chỉ ghi lại.

| Cấp | Sai context | Chưa chắc / để team quyết | Lý do null |
|---|---|---|---|
| N2 | 941 | 136 | 24 |
| N1 | 522 | 0 | 58 |

Loại lỗi hay gặp: cách đọc sai (vd 透き通る すきとうる→すきとおる, 行方 なめがた→ゆくえ), chữ sai (見在→現在, 観逆→観客), `meaning_vi` lẫn câu ví dụ hoặc lạc nghĩa, Hán Việt sai (縦 Sỉ→Tung, 梯 Đệ→Thê), mẫu ngữ pháp trùng nhau hoặc `pattern` ghi bằng tiếng Việt.

## Điểm cần team quyết / nên duyệt lại

- N2 KANJI_MNEMONIC 001-003: mẹo nhớ hơi gượng: 毒, 栄, 鼻, 芸, 底, 総, 営, 勇
- N2 KANJI_MNEMONIC 004-006: tách chữ còn lỏng: 巨, 再, 河, 汗, 略, 航, 照
- N2 KANJI_CORE / KANJI_MNEMONIC: 齧 âm Hán Việt KHIẾT hay NIẾT (team quyết)
- N2 KANJI_MNEMONIC-008: 畑 là kokuji, context ghi han_viet "Đèn" sai
- N1 VOCAB_TYPE-006: 来る (きたる) là liên thể từ, không có nhãn phù hợp → tạm gán 'phó từ'
- N2 VOCAB_EXAMPLE 004-006: có thể đã đổi chính từ đích sang kana để né cảnh báo vượt cấp (vd 独り言 → ひとり言); cần rà lại
- N1 VOCAB_TYPE: động từ ～ずる (報ずる, 重んずる, 禁ずる) gán 'động từ nhóm III'; とんだ, あっさりした, こってりした gán 'cụm từ'
- N2 VOCAB_EXAMPLE-005 JV-e4fc3b31d7: expression お襁褓 (chữ rất hiếm) — câu dùng お襁褓(むつ); có thể nên để おむつ
- N1 GRAMMAR_UNIT-002: tạo tên bài 15–18 mới ("Liên quan, lập trường"; "Mà không, bất chấp"; "Đánh đổi, bằng phương tiện"; "Bổ nghĩa, tình huống")
- N1 GRAMMAR_PARENT 002-004: 26 mẫu phụ để null vì không có mẫu chính cùng chức năng trong header.mains (vd ～とは限らない, ～を前提に, ～を機に, ～くらいなら) — team chọn: gán tạm mẫu gần nhất hay nâng lên mẫu chính
- N1 GRAMMAR_PARENT 005-008: thêm 23 mẫu phụ để null (ごとく/ごとき, ぶる, てみせる, たて, っぱなし, まぎれに, 後を絶たない...); một số gán tạm (〜はめになる→を余儀なくされる, 〜びる→N+めく, 〜にして→といえども)
- N2 GRAMMAR_BANK-009 JG-df00d02bd4 (ようがない): đã sửa phương án 道の教えようがない → 道を教えようがない (câu ERROR thứ 2); nên đọc lại

## Mục để null (83)

| Cấp | Gói | id | Mục | Lý do |
|---|---|---|---|---|
| N2 | GRAMMAR_CORE-013.json | JG-596bc19f9b | Nhân dịp..., nhờ... mà... | pattern chỉ ghi 'Nhân dịp..., nhờ... mà...' không có mẫu tiếng Nhật, meaning_vi rác ('Đã trình bày chi tiết ở khối 411.'), không có ví dụ nên không xác định đượ |
| N2 | GRAMMAR_CORE-020.json | JG-e9a6dc7f88 | N2 dễ nhầm | Không phải một mẫu ngữ pháp mà là mục tổng hợp các nhóm dễ nhầm (không có formation riêng) |
| N2 | GRAMMAR_PARENT-012.json | JG-e9a6dc7f88 | N2 dễ nhầm | Không phải một mẫu ngữ pháp mà là mục tổng hợp các nhóm dễ nhầm (không có formation riêng) |
| N2 | VOCAB_EXAMPLE-004.json | JV-79895c0650 | 問 | Mục '問' đọc 'とん' không rõ từ nào (có thể là 問屋 とんや/といや); không đủ ngữ cảnh để viết câu đúng |
| N2 | VOCAB_EXAMPLE-007.json | JV-61ea58486b | アビール＜する＞ | context sai chữ nên không viết ví dụ |
| N2 | VOCAB_EXAMPLE-008.json | JV-6ba4ad9996 | 重なる | expression, reading, meaning không khớp nhau |
| N2 | VOCAB_EXAMPLE-008.json | JV-b1d8f512d6 | 観逆 | expression sai chữ |
| N2 | VOCAB_EXAMPLE-008.json | JV-6739a904f9 | 鮮やかな | reading sai nên không viết ví dụ |
| N2 | VOCAB_EXAMPLE-010.json | JV-2cc0ba3e22 | ブラン | Expression 'ブラン' (ぶらん) không rõ nghĩa, nhiều khả năng là gõ sai của 'プラン' (kế hoạch) trong chủ đề Du lịch |
| N2 | VOCAB_EXAMPLE-012.json | JV-cb23ffd367 | 公 | Expression '公' đọc こう đứng riêng, không rõ nghĩa/từ mục tiêu (có thể là tiền tố/hậu tố hoặc おおやke) |
| N2 | VOCAB_MEANING-001.json | JV-79895c0650 | 問 | Mục '問' đọc 'とん' không rõ từ nào (có thể là 問屋 とんや/といや); không đủ ngữ cảnh để viết câu đúng |
| N2 | VOCAB_MEANING-002.json | JV-d6fc48fa28 | 優勝な | expression 優勝な: 優勝 là danh từ (vô địch), không đi với な; nghĩa trống, không rõ ý định |
| N2 | VOCAB_MEANING-002.json | JV-b1d8f512d6 | 観逆 | expression sai chữ |
| N2 | VOCAB_MNEMONIC-005.json | JV-2a946d290e | 見在 | 見在 (けんざい) không phải từ N2 thông dụng, có vẻ gõ nhầm; không có nghĩa trong context |
| N2 | VOCAB_MNEMONIC-005.json | JV-79895c0650 | 問 | Mục '問' đọc 'とん' không rõ từ nào (có thể là 問屋 とんや/といや); không đủ ngữ cảnh để viết câu đúng |
| N2 | VOCAB_MNEMONIC-007.json | JV-47237f6ee9 | 斜めくな | expression 斜めくな / ななめくな không phải từ có thật, không rõ nghĩa |
| N2 | VOCAB_MNEMONIC-009.json | JV-d6fc48fa28 | 優勝な | expression 優勝な: 優勝 là danh từ (vô địch), không đi với な; nghĩa trống, không rõ ý định |
| N2 | VOCAB_MNEMONIC-013.json | JV-b1d8f512d6 | 観逆 | expression sai chữ |
| N2 | VOCAB_MNEMONIC-016.json | JV-2cc0ba3e22 | ブラン | Expression 'ブラン' (ぶらん) không rõ nghĩa, nhiều khả năng là gõ sai của 'プラン' (kế hoạch) trong chủ đề Du lịch |
| N2 | VOCAB_TYPE-004.json | JV-c699b46d56 | 明くる | 明くる là liên thể từ (連体詞, chỉ đứng trước danh từ: 明くる日), không có nhãn tương ứng trong 13 nhãn; cần người duyệt chọn nhãn |
| N2 | VOCAB_TYPE-004.json | JV-79895c0650 | 問 | Mục '問' đọc 'とん' không rõ từ nào (có thể là 問屋 とんや/といや); không đủ ngữ cảnh để viết câu đúng |
| N2 | VOCAB_TYPE-006.json | JV-47237f6ee9 | 斜めくな | expression 斜めくな / ななめくな không phải từ có thật, không rõ nghĩa |
| N2 | VOCAB_TYPE-011.json | JV-b1d8f512d6 | 観逆 | expression sai chữ |
| N2 | VOCAB_TYPE-026.json | JV-c5a01ac00b | 超〜 | 超〜 là tiền tố (接頭語), không khớp nhãn nào trong 13 nhãn loại từ |
| N2 | VOCAB_TYPE-026.json | JV-a2f188660f | 諸〜 | 諸〜 là tiền tố (接頭語), không khớp nhãn nào trong 13 nhãn loại từ |
| N1 | GRAMMAR_BANK-007.json | JG-a5ec828b3e | たるに | Mẫu "たるに" không có nghĩa, ví dụ trong context; GRAMMAR_CORE cùng id cũng để null (không chắc mẫu gốc, có thể trích sai từ 〜たるもの / 〜たる + N) nên không thể soạn câ |
| N1 | GRAMMAR_CORE-002.json | JG-a5ec828b3e | たるに | Mẫu "たるに" không có nghĩa, ví dụ trong context; GRAMMAR_CORE cùng id cũng để null (không chắc mẫu gốc, có thể trích sai từ 〜たるもの / 〜たる + N) nên không thể soạn câ |
| N1 | GRAMMAR_CORE-013.json | JG-30359f632b | N1 dễ nhầm | Mục tổng hợp 'N1 dễ nhầm' không phải một mẫu ngữ pháp đơn (ví dụ gồm 〜限り và 〜なくして khác chức năng), không có formation duy nhất |
| N1 | GRAMMAR_PARENT-002.json | JG-32d8381bd4 | Không thể kết luận rõ... | 〜とも〜とも言えない/言わない (không kết luận được A hay B) không có mẫu chính cùng chức năng trong header.mains |
| N1 | GRAMMAR_PARENT-002.json | JG-6c0a2d09ed | Không đủ... | pattern 'Không đủ...' và ví dụ (説明が足りない) là động từ 足りる thông thường, không phải ngữ pháp; meaning_vi trộn lẫn với に足りない (không đáng để) |
| N1 | GRAMMAR_PARENT-002.json | JG-670324b1e4 | Không hẳn là... | 〜とは限らない (không hẳn là) không có mẫu chính cùng chức năng trong header.mains |
| N1 | GRAMMAR_PARENT-002.json | JG-4dee5e1610 | Không thể bỏ qua... | 〜ではすまない (không thể xong chỉ bằng N) không có mẫu chính cùng chức năng; ずにはすまない là 'buộc phải làm', どころの話ではない khác chức năng |
| N1 | GRAMMAR_PARENT-002.json | JG-5ee574f221 | Xét về ... cũng như về ... | 〜といい〜といい (xét về A cũng như B) không có mẫu chính cùng chức năng trong header.mains |
| N1 | GRAMMAR_PARENT-002.json | JG-d071ce5c18 | Hễ... là... | V-ては (mỗi lần... là...) khác với 〜つ〜つ (luân phiên đối xứng) và không có mẫu chính nào khác cùng chức năng; meaning_vi tự nêu 'khác kiểu luân phiên' |
| N1 | GRAMMAR_PARENT-002.json | JG-f8fddd1571 | Không phải là không... | 〜ないものでもない (không phải là không) không có mẫu chính cùng chức năng trong header.mains |
| N1 | GRAMMAR_PARENT-002.json | JG-b24740322d | Đến mức là... (khen/chê) | 〜ときている (đã thế lại còn... nên) khác chức năng với ときたら (nêu chủ đề để phàn nàn) nên không gán vào JG-02fd59fc58; tiêu đề 'Đến mức là...' cũng lệch nghĩa |
| N1 | GRAMMAR_PARENT-002.json | JG-a5c45b57b1 | Kể ra thì vô số | 〜たらきりがない (kể ra thì vô tận) không có mẫu chính cùng chức năng trong header.mains |
| N1 | GRAMMAR_PARENT-003.json | JG-86b3a73ff6 | Không thể so với... | 〜とは比べものにならない (không thể so sánh) không có mẫu chính cùng chức năng trong header.mains |
| N1 | GRAMMAR_PARENT-003.json | JG-406ac0e278 | Vô số... | 〜ばきりがない (nếu bắt đầu thì vô tận) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-003.json | JG-a020602f52 | 〜かいがある/ない | 〜かいがある/ない (đáng công/uổng công) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-003.json | JG-97ea375bd0 | 〜といい...といい | 〜といい〜といい (xét cả A lẫn B) không có mẫu chính cùng chức năng trong header.mains |
| N1 | GRAMMAR_PARENT-003.json | JG-14c35d37ef | Không thể... sao nhỉ | 〜ものだろうか (liệu có thể... không nhỉ) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-003.json | JG-9f8124f185 | Có vẻ như... | 〜とみえて (có vẻ như) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-003.json | JG-5996811f1a | Hễ thấy... thì... | 〜とみると (hễ thấy là) không có mẫu chính cùng chức năng; が早いか/そばから khác sắc thái |
| N1 | GRAMMAR_PARENT-004.json | JG-52c6352be3 | Lấy... làm điều kiện | 〜を前提にして (lấy làm tiền đề) không có mẫu chính cùng chức năng; を踏まえて (dựa trên kết quả đã có) và ものとする khác chức năng |
| N1 | GRAMMAR_PARENT-004.json | JG-5bb3adcae0 | Trên cơ sở... | 〜前提で (trên cơ sở) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-004.json | JG-fc11bcf121 | Với tiền đề... | 〜を前提として (với tiền đề) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-004.json | JG-d97397085a | 〜ごとく/ごとき/ごとし | 〜ごとく/ごとき/ごとし (như) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-004.json | JG-7e6f8bf5bc | 〜にもほどがある | 〜にもほどがある (quá mức chấp nhận được) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-004.json | JG-cc17447a2e | Dù có ... thì cũng vô ích | 〜たところで (dù có làm cũng vô ích) không có mẫu chính cùng chức năng; とて/といえども chỉ gần nghĩa |
| N1 | GRAMMAR_PARENT-004.json | JG-af21afb1f9 | Thà ... còn hơn đến mức ... | 〜くらいなら (thà... còn hơn) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-004.json | JG-dbc9a674cc | Chồng chất... | N に N を重ねて (chồng chất) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-004.json | JG-1a2cc85656 | Nhân dịp... | 〜を機に(して) (nhân dịp) không có mẫu chính cùng chức năng; 旁/がてら khác chức năng |
| N1 | GRAMMAR_PARENT-004.json | JG-3343f5c2ae | 〜ばかりだ/に/の | 〜ばかりだ/の/に (đến mức) khác với んばかり (như sắp làm); chưa có mẫu chính tương ứng |
| N1 | GRAMMAR_PARENT-005.json | JG-8202e3f75e | Như... / tựa như... | 〜ごとく (văn chương, như) không có mẫu chính cùng chức năng trong header.mains (không thấy ごとし/ごとく/ごとき) |
| N1 | GRAMMAR_PARENT-005.json | JG-b2a9bf8cc0 | Tương đương... | N並み (tương đương N) không có mẫu chính phù hợp trong candidates hay header.mains |
| N1 | GRAMMAR_PARENT-005.json | JG-41815ce73f | Chính... mới... | NこそNだが (nhấn mạnh rồi nhượng bộ) khác chức năng với N/Vば+こそ (JG-b33c37f6ec, chính vì...mới), không chắc nên không gán |
| N1 | GRAMMAR_PARENT-005.json | JG-30fb121e88 | Giống như... | 〜ごとき (văn chương, giống như) không có mẫu chính cùng chức năng trong header.mains |
| N1 | GRAMMAR_PARENT-006.json | JG-a88085f5a4 | 〜拍子に | 〜拍子に (đúng lúc một sự việc ngẫu nhiên xảy ra) không có mẫu chính cùng chức năng; が早いか/そばから khác sắc thái (kế tiếp liền/lặp lại) |
| N1 | GRAMMAR_PARENT-006.json | JG-f3cf2a3086 | Sẽ làm cho xem | 〜てみせる (sẽ làm cho xem) không có mẫu chính tương ứng trong candidates hay header.mains |
| N1 | GRAMMAR_PARENT-006.json | JG-63f857781b | Theo đúng... | 〜るがままに (đúng theo, mặc cho) không có mẫu chính tương ứng |
| N1 | GRAMMAR_PARENT-006.json | JG-6e7347f8a1 | 〜たて(の) | 〜たて(の) (vừa mới làm xong) không có mẫu chính tương ứng; そばから/が早いか khác chức năng |
| N1 | GRAMMAR_PARENT-006.json | JG-558f225c92 | 〜ての+名詞 | 〜ての+名詞 (連れての来日) không có mẫu chính tương ứng |
| N1 | GRAMMAR_PARENT-006.json | JG-1b53b4c1b6 | 〜ても〜きれない(否定的表現) | 〜ても〜きれない không có mẫu chính tương ứng (に堪えない/て止まない khác chức năng) |
| N1 | GRAMMAR_PARENT-006.json | JG-98d93a4460 | Để nguyên / ... suốt không dừng | 〜っぱなし (để nguyên, cứ mãi) không có mẫu chính tương ứng |
| N1 | GRAMMAR_PARENT-007.json | JG-9943860b58 | Làm bộ... | 〜ぶって (ra vẻ, giả bộ) không có mẫu chính cùng chức năng trong candidates hay header.mains |
| N1 | GRAMMAR_PARENT-007.json | JG-d01126affa | Làm như... | 〜ぶった (làm như) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-007.json | JG-270569e469 | Tỏ ra... | 〜ぶる (tỏ ra) không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-007.json | JG-6899499a74 | 〜をいいことに | 〜をいいことに (lợi dụng) không có mẫu chính tương ứng |
| N1 | GRAMMAR_PARENT-007.json | JG-bbc418a588 | Cứ xem như... | 〜たことにしてください không có mẫu chính tương ứng (mẫu ngữ pháp cấp thấp hơn N1) |
| N1 | GRAMMAR_PARENT-007.json | JG-85f1cfef4f | 〜にかこつけて | 〜にかこつけて (vin cớ) không có mẫu chính tương ứng |
| N1 | GRAMMAR_PARENT-008.json | JG-069b77dfee | 〜ぶる | 〜ぶる (cố tình ra vẻ) khác chức năng với N+めく (nhuốm vẻ tự nhiên); không có mẫu chính cùng chức năng |
| N1 | GRAMMAR_PARENT-008.json | JG-dbdce29ad7 | 〜べくして | 〜べくして (đúng như tất yếu) khác chức năng với 〜べく (mục đích); không có mẫu chính tương ứng |
| N1 | GRAMMAR_PARENT-008.json | JG-407692f4e5 | 〜まぎれに | 〜まぎれに (trong cơn... làm bừa) không có mẫu chính tương ứng |
| N1 | GRAMMAR_PARENT-008.json | JG-c75be10fc9 | 〜後を絶たない | 〜後を絶たない không có mẫu chính tương ứng |
| N1 | GRAMMAR_PARENT-008.json | JG-37aa545d9b | 「〜ん」を使った表現 | 〜んとする (=ようとする) khác chức năng với んが為に/んばかりに; không có mẫu chính tương ứng |
| N1 | GRAMMAR_PARENT-008.json | JG-30359f632b | N1 dễ nhầm | Mục tổng hợp 'N1 dễ nhầm' không phải một mẫu ngữ pháp đơn (ví dụ gồm 〜限り và 〜なくして khác chức năng), không có formation duy nhất |
| N1 | VOCAB_EXAMPLE-020.json | JV-bd8cbc1d60 | 限りな | expression 限りな bị cắt dở (không phải từ hoàn chỉnh), không xác định được ý định |
| N1 | VOCAB_EXAMPLE-033.json | JV-996dfa51c2 | 愛でたい | Biểu thức 愛でたい (đọc めでたい) nghĩa 'đáng mừng' không khớp: めでたい thường viết 目出度い/めでたい; 愛でたい là dạng 愛でる + たい (muốn thưởng ngoạn). |
| N1 | VOCAB_EXAMPLE-035.json | JV-50ccd9d6f4 | 米 | Mục 米: reading ghi '米' (không phải kana) và meaning_vi 'vo gạo／mài dao bếp' sai (trùng nghĩa của 包丁を研ぐ); không rõ đây là こめ hay べい. |
| N1 | VOCAB_EXAMPLE-038.json | JV-f56152e177 | 重役 | 重役 ghi cách đọc おもやく, nghĩa 'vai trò quan trọng'; từ thông dụng là 重役 じゅうやく (giám đốc, thành viên ban lãnh đạo), không chắc nghĩa/cách đọc đúng của mục nên để n |
| N1 | VOCAB_MEANING-002.json | JV-cbf817a740 | 丸々[化] ＜する＞ | biểu thức 丸々[化]＜する＞ (まるまる[か]) không rõ là từ nào, ghép 化 với 丸々 không có nghĩa chắc chắn; để null |
| N1 | VOCAB_MNEMONIC-007.json | JV-2da599cffb | さらう | さらう kana đồng âm nhiều nghĩa (浚う nạo vét, 攫う cuỗm đi, 復習う ôn lại); chủ đề 'Việc nhà' không xác định rõ nghĩa nên điền gộp nghĩa chính, độ chắc chưa cao |

## Số mục đã điền theo từng file

| Cấp | File | Đã điền / Tổng |
|---|---|---|
| N2 | GRAMMAR_BANK-001.json | 10/10 |
| N2 | GRAMMAR_BANK-002.json | 10/10 |
| N2 | GRAMMAR_BANK-003.json | 10/10 |
| N2 | GRAMMAR_BANK-004.json | 10/10 |
| N2 | GRAMMAR_BANK-005.json | 10/10 |
| N2 | GRAMMAR_BANK-006.json | 10/10 |
| N2 | GRAMMAR_BANK-007.json | 10/10 |
| N2 | GRAMMAR_BANK-008.json | 10/10 |
| N2 | GRAMMAR_BANK-009.json | 10/10 |
| N2 | GRAMMAR_BANK-010.json | 10/10 |
| N2 | GRAMMAR_BANK-011.json | 10/10 |
| N2 | GRAMMAR_BANK-012.json | 10/10 |
| N2 | GRAMMAR_BANK-013.json | 10/10 |
| N2 | GRAMMAR_BANK-014.json | 10/10 |
| N2 | GRAMMAR_BANK-015.json | 10/10 |
| N2 | GRAMMAR_BANK-016.json | 10/10 |
| N2 | GRAMMAR_BANK-017.json | 10/10 |
| N2 | GRAMMAR_BANK-018.json | 10/10 |
| N2 | GRAMMAR_BANK-019.json | 10/10 |
| N2 | GRAMMAR_BANK-020.json | 10/10 |
| N2 | GRAMMAR_BANK-021.json | 10/10 |
| N2 | GRAMMAR_CORE-001.json | 40/40 |
| N2 | GRAMMAR_CORE-002.json | 40/40 |
| N2 | GRAMMAR_CORE-003.json | 40/40 |
| N2 | GRAMMAR_CORE-004.json | 40/40 |
| N2 | GRAMMAR_CORE-005.json | 40/40 |
| N2 | GRAMMAR_CORE-006.json | 10/10 |
| N2 | GRAMMAR_CORE-007.json | 40/40 |
| N2 | GRAMMAR_CORE-008.json | 40/40 |
| N2 | GRAMMAR_CORE-009.json | 40/40 |
| N2 | GRAMMAR_CORE-010.json | 40/40 |
| N2 | GRAMMAR_CORE-011.json | 40/40 |
| N2 | GRAMMAR_CORE-012.json | 40/40 |
| N2 | GRAMMAR_CORE-013.json | 39/40 |
| N2 | GRAMMAR_CORE-014.json | 40/40 |
| N2 | GRAMMAR_CORE-015.json | 40/40 |
| N2 | GRAMMAR_CORE-016.json | 40/40 |
| N2 | GRAMMAR_CORE-017.json | 40/40 |
| N2 | GRAMMAR_CORE-018.json | 40/40 |
| N2 | GRAMMAR_CORE-019.json | 40/40 |
| N2 | GRAMMAR_CORE-020.json | 39/40 |
| N2 | GRAMMAR_CORE-021.json | 8/8 |
| N2 | GRAMMAR_PARENT-001.json | 40/40 |
| N2 | GRAMMAR_PARENT-002.json | 40/40 |
| N2 | GRAMMAR_PARENT-003.json | 40/40 |
| N2 | GRAMMAR_PARENT-004.json | 40/40 |
| N2 | GRAMMAR_PARENT-005.json | 40/40 |
| N2 | GRAMMAR_PARENT-006.json | 40/40 |
| N2 | GRAMMAR_PARENT-007.json | 40/40 |
| N2 | GRAMMAR_PARENT-008.json | 40/40 |
| N2 | GRAMMAR_PARENT-009.json | 40/40 |
| N2 | GRAMMAR_PARENT-010.json | 40/40 |
| N2 | GRAMMAR_PARENT-011.json | 40/40 |
| N2 | GRAMMAR_PARENT-012.json | 39/40 |
| N2 | GRAMMAR_PARENT-013.json | 9/9 |
| N2 | GRAMMAR_UNIT-001.json | 40/40 |
| N2 | GRAMMAR_UNIT-002.json | 40/40 |
| N2 | GRAMMAR_UNIT-003.json | 11/11 |
| N2 | KANJI_CORE-001.json | 6/6 |
| N2 | KANJI_MNEMONIC-001.json | 40/40 |
| N2 | KANJI_MNEMONIC-002.json | 40/40 |
| N2 | KANJI_MNEMONIC-003.json | 40/40 |
| N2 | KANJI_MNEMONIC-004.json | 40/40 |
| N2 | KANJI_MNEMONIC-005.json | 40/40 |
| N2 | KANJI_MNEMONIC-006.json | 40/40 |
| N2 | KANJI_MNEMONIC-007.json | 40/40 |
| N2 | KANJI_MNEMONIC-008.json | 29/29 |
| N2 | RADICAL_NAME-001.json | 40/40 |
| N2 | RADICAL_NAME-002.json | 40/40 |
| N2 | RADICAL_NAME-003.json | 25/25 |
| N2 | TOPIC_ASSIGN-001.json | 40/40 |
| N2 | TOPIC_ASSIGN-002.json | 40/40 |
| N2 | TOPIC_ASSIGN-003.json | 40/40 |
| N2 | TOPIC_ASSIGN-004.json | 40/40 |
| N2 | TOPIC_ASSIGN-005.json | 40/40 |
| N2 | TOPIC_ASSIGN-006.json | 40/40 |
| N2 | TOPIC_ASSIGN-007.json | 40/40 |
| N2 | TOPIC_ASSIGN-008.json | 40/40 |
| N2 | TOPIC_ASSIGN-009.json | 40/40 |
| N2 | TOPIC_ASSIGN-010.json | 40/40 |
| N2 | TOPIC_ASSIGN-011.json | 40/40 |
| N2 | TOPIC_ASSIGN-012.json | 40/40 |
| N2 | TOPIC_ASSIGN-013.json | 40/40 |
| N2 | TOPIC_ASSIGN-014.json | 40/40 |
| N2 | TOPIC_ASSIGN-015.json | 40/40 |
| N2 | TOPIC_ASSIGN-016.json | 40/40 |
| N2 | TOPIC_ASSIGN-017.json | 40/40 |
| N2 | TOPIC_ASSIGN-018.json | 40/40 |
| N2 | TOPIC_ASSIGN-019.json | 40/40 |
| N2 | TOPIC_ASSIGN-020.json | 40/40 |
| N2 | TOPIC_ASSIGN-021.json | 40/40 |
| N2 | TOPIC_ASSIGN-022.json | 40/40 |
| N2 | TOPIC_ASSIGN-023.json | 24/24 |
| N2 | VOCAB_EXAMPLE-001.json | 40/40 |
| N2 | VOCAB_EXAMPLE-002.json | 40/40 |
| N2 | VOCAB_EXAMPLE-003.json | 40/40 |
| N2 | VOCAB_EXAMPLE-004.json | 39/40 |
| N2 | VOCAB_EXAMPLE-005.json | 40/40 |
| N2 | VOCAB_EXAMPLE-006.json | 40/40 |
| N2 | VOCAB_EXAMPLE-007.json | 39/40 |
| N2 | VOCAB_EXAMPLE-008.json | 37/40 |
| N2 | VOCAB_EXAMPLE-009.json | 40/40 |
| N2 | VOCAB_EXAMPLE-010.json | 39/40 |
| N2 | VOCAB_EXAMPLE-011.json | 40/40 |
| N2 | VOCAB_EXAMPLE-012.json | 39/40 |
| N2 | VOCAB_EXAMPLE-013.json | 40/40 |
| N2 | VOCAB_EXAMPLE-014.json | 40/40 |
| N2 | VOCAB_EXAMPLE-015.json | 40/40 |
| N2 | VOCAB_EXAMPLE-016.json | 40/40 |
| N2 | VOCAB_EXAMPLE-017.json | 40/40 |
| N2 | VOCAB_EXAMPLE-018.json | 40/40 |
| N2 | VOCAB_EXAMPLE-019.json | 40/40 |
| N2 | VOCAB_EXAMPLE-020.json | 40/40 |
| N2 | VOCAB_EXAMPLE-021.json | 40/40 |
| N2 | VOCAB_EXAMPLE-022.json | 40/40 |
| N2 | VOCAB_EXAMPLE-023.json | 40/40 |
| N2 | VOCAB_EXAMPLE-024.json | 40/40 |
| N2 | VOCAB_EXAMPLE-025.json | 40/40 |
| N2 | VOCAB_EXAMPLE-026.json | 40/40 |
| N2 | VOCAB_EXAMPLE-027.json | 40/40 |
| N2 | VOCAB_EXAMPLE-028.json | 40/40 |
| N2 | VOCAB_EXAMPLE-029.json | 40/40 |
| N2 | VOCAB_EXAMPLE-030.json | 40/40 |
| N2 | VOCAB_EXAMPLE-031.json | 40/40 |
| N2 | VOCAB_EXAMPLE-032.json | 40/40 |
| N2 | VOCAB_EXAMPLE-033.json | 40/40 |
| N2 | VOCAB_EXAMPLE-034.json | 4/4 |
| N2 | VOCAB_MEANING-001.json | 39/40 |
| N2 | VOCAB_MEANING-002.json | 38/40 |
| N2 | VOCAB_MEANING-003.json | 40/40 |
| N2 | VOCAB_MEANING-004.json | 40/40 |
| N2 | VOCAB_MEANING-005.json | 10/10 |
| N2 | VOCAB_MNEMONIC-001.json | 40/40 |
| N2 | VOCAB_MNEMONIC-002.json | 40/40 |
| N2 | VOCAB_MNEMONIC-003.json | 40/40 |
| N2 | VOCAB_MNEMONIC-004.json | 40/40 |
| N2 | VOCAB_MNEMONIC-005.json | 38/40 |
| N2 | VOCAB_MNEMONIC-006.json | 40/40 |
| N2 | VOCAB_MNEMONIC-007.json | 39/40 |
| N2 | VOCAB_MNEMONIC-008.json | 40/40 |
| N2 | VOCAB_MNEMONIC-009.json | 39/40 |
| N2 | VOCAB_MNEMONIC-010.json | 40/40 |
| N2 | VOCAB_MNEMONIC-011.json | 40/40 |
| N2 | VOCAB_MNEMONIC-012.json | 40/40 |
| N2 | VOCAB_MNEMONIC-013.json | 39/40 |
| N2 | VOCAB_MNEMONIC-014.json | 40/40 |
| N2 | VOCAB_MNEMONIC-015.json | 40/40 |
| N2 | VOCAB_MNEMONIC-016.json | 39/40 |
| N2 | VOCAB_MNEMONIC-017.json | 40/40 |
| N2 | VOCAB_MNEMONIC-018.json | 40/40 |
| N2 | VOCAB_MNEMONIC-019.json | 40/40 |
| N2 | VOCAB_MNEMONIC-020.json | 40/40 |
| N2 | VOCAB_MNEMONIC-021.json | 40/40 |
| N2 | VOCAB_MNEMONIC-022.json | 40/40 |
| N2 | VOCAB_MNEMONIC-023.json | 40/40 |
| N2 | VOCAB_MNEMONIC-024.json | 40/40 |
| N2 | VOCAB_MNEMONIC-025.json | 40/40 |
| N2 | VOCAB_MNEMONIC-026.json | 40/40 |
| N2 | VOCAB_MNEMONIC-027.json | 40/40 |
| N2 | VOCAB_MNEMONIC-028.json | 40/40 |
| N2 | VOCAB_MNEMONIC-029.json | 40/40 |
| N2 | VOCAB_MNEMONIC-030.json | 40/40 |
| N2 | VOCAB_MNEMONIC-031.json | 40/40 |
| N2 | VOCAB_MNEMONIC-032.json | 40/40 |
| N2 | VOCAB_MNEMONIC-033.json | 40/40 |
| N2 | VOCAB_MNEMONIC-034.json | 40/40 |
| N2 | VOCAB_MNEMONIC-035.json | 40/40 |
| N2 | VOCAB_MNEMONIC-036.json | 40/40 |
| N2 | VOCAB_MNEMONIC-037.json | 40/40 |
| N2 | VOCAB_MNEMONIC-038.json | 40/40 |
| N2 | VOCAB_MNEMONIC-039.json | 40/40 |
| N2 | VOCAB_MNEMONIC-040.json | 40/40 |
| N2 | VOCAB_MNEMONIC-041.json | 40/40 |
| N2 | VOCAB_MNEMONIC-042.json | 40/40 |
| N2 | VOCAB_MNEMONIC-043.json | 40/40 |
| N2 | VOCAB_MNEMONIC-044.json | 40/40 |
| N2 | VOCAB_MNEMONIC-045.json | 40/40 |
| N2 | VOCAB_MNEMONIC-046.json | 40/40 |
| N2 | VOCAB_MNEMONIC-047.json | 40/40 |
| N2 | VOCAB_MNEMONIC-048.json | 40/40 |
| N2 | VOCAB_MNEMONIC-049.json | 40/40 |
| N2 | VOCAB_MNEMONIC-050.json | 40/40 |
| N2 | VOCAB_TYPE-001.json | 40/40 |
| N2 | VOCAB_TYPE-002.json | 40/40 |
| N2 | VOCAB_TYPE-003.json | 40/40 |
| N2 | VOCAB_TYPE-004.json | 38/40 |
| N2 | VOCAB_TYPE-005.json | 40/40 |
| N2 | VOCAB_TYPE-006.json | 39/40 |
| N2 | VOCAB_TYPE-007.json | 40/40 |
| N2 | VOCAB_TYPE-008.json | 40/40 |
| N2 | VOCAB_TYPE-009.json | 40/40 |
| N2 | VOCAB_TYPE-010.json | 40/40 |
| N2 | VOCAB_TYPE-011.json | 39/40 |
| N2 | VOCAB_TYPE-012.json | 40/40 |
| N2 | VOCAB_TYPE-013.json | 40/40 |
| N2 | VOCAB_TYPE-014.json | 40/40 |
| N2 | VOCAB_TYPE-015.json | 40/40 |
| N2 | VOCAB_TYPE-016.json | 40/40 |
| N2 | VOCAB_TYPE-017.json | 40/40 |
| N2 | VOCAB_TYPE-018.json | 40/40 |
| N2 | VOCAB_TYPE-019.json | 40/40 |
| N2 | VOCAB_TYPE-020.json | 40/40 |
| N2 | VOCAB_TYPE-021.json | 40/40 |
| N2 | VOCAB_TYPE-022.json | 40/40 |
| N2 | VOCAB_TYPE-023.json | 40/40 |
| N2 | VOCAB_TYPE-024.json | 40/40 |
| N2 | VOCAB_TYPE-025.json | 40/40 |
| N2 | VOCAB_TYPE-026.json | 38/40 |
| N2 | VOCAB_TYPE-027.json | 40/40 |
| N2 | VOCAB_TYPE-028.json | 40/40 |
| N2 | VOCAB_TYPE-029.json | 40/40 |
| N2 | VOCAB_TYPE-030.json | 40/40 |
| N2 | VOCAB_TYPE-031.json | 40/40 |
| N2 | VOCAB_TYPE-032.json | 40/40 |
| N2 | VOCAB_TYPE-033.json | 40/40 |
| N2 | VOCAB_TYPE-034.json | 40/40 |
| N2 | VOCAB_TYPE-035.json | 40/40 |
| N2 | VOCAB_TYPE-036.json | 40/40 |
| N2 | VOCAB_TYPE-037.json | 40/40 |
| N2 | VOCAB_TYPE-038.json | 40/40 |
| N2 | VOCAB_TYPE-039.json | 40/40 |
| N2 | VOCAB_TYPE-040.json | 40/40 |
| N2 | VOCAB_TYPE-041.json | 40/40 |
| N2 | VOCAB_TYPE-042.json | 40/40 |
| N2 | VOCAB_TYPE-043.json | 5/5 |
| N1 | GRAMMAR_BANK-001.json | 10/10 |
| N1 | GRAMMAR_BANK-002.json | 10/10 |
| N1 | GRAMMAR_BANK-003.json | 10/10 |
| N1 | GRAMMAR_BANK-004.json | 10/10 |
| N1 | GRAMMAR_BANK-005.json | 10/10 |
| N1 | GRAMMAR_BANK-006.json | 10/10 |
| N1 | GRAMMAR_BANK-007.json | 9/10 |
| N1 | GRAMMAR_BANK-008.json | 10/10 |
| N1 | GRAMMAR_BANK-009.json | 10/10 |
| N1 | GRAMMAR_BANK-010.json | 10/10 |
| N1 | GRAMMAR_BANK-011.json | 10/10 |
| N1 | GRAMMAR_BANK-012.json | 10/10 |
| N1 | GRAMMAR_BANK-013.json | 10/10 |
| N1 | GRAMMAR_BANK-014.json | 10/10 |
| N1 | GRAMMAR_BANK-015.json | 10/10 |
| N1 | GRAMMAR_BANK-016.json | 10/10 |
| N1 | GRAMMAR_BANK-017.json | 2/2 |
| N1 | GRAMMAR_CORE-001.json | 40/40 |
| N1 | GRAMMAR_CORE-002.json | 39/40 |
| N1 | GRAMMAR_CORE-003.json | 40/40 |
| N1 | GRAMMAR_CORE-004.json | 40/40 |
| N1 | GRAMMAR_CORE-005.json | 2/2 |
| N1 | GRAMMAR_CORE-006.json | 40/40 |
| N1 | GRAMMAR_CORE-007.json | 40/40 |
| N1 | GRAMMAR_CORE-008.json | 40/40 |
| N1 | GRAMMAR_CORE-009.json | 40/40 |
| N1 | GRAMMAR_CORE-010.json | 40/40 |
| N1 | GRAMMAR_CORE-011.json | 40/40 |
| N1 | GRAMMAR_CORE-012.json | 40/40 |
| N1 | GRAMMAR_CORE-013.json | 15/16 |
| N1 | GRAMMAR_PARENT-001.json | 40/40 |
| N1 | GRAMMAR_PARENT-002.json | 31/40 |
| N1 | GRAMMAR_PARENT-003.json | 33/40 |
| N1 | GRAMMAR_PARENT-004.json | 30/40 |
| N1 | GRAMMAR_PARENT-005.json | 36/40 |
| N1 | GRAMMAR_PARENT-006.json | 33/40 |
| N1 | GRAMMAR_PARENT-007.json | 34/40 |
| N1 | GRAMMAR_PARENT-008.json | 6/12 |
| N1 | GRAMMAR_UNIT-001.json | 40/40 |
| N1 | GRAMMAR_UNIT-002.json | 29/29 |
| N1 | KANJI_CORE-001.json | 40/40 |
| N1 | KANJI_CORE-002.json | 40/40 |
| N1 | KANJI_CORE-003.json | 15/15 |
| N1 | KANJI_MNEMONIC-001.json | 40/40 |
| N1 | KANJI_MNEMONIC-002.json | 40/40 |
| N1 | KANJI_MNEMONIC-003.json | 40/40 |
| N1 | KANJI_MNEMONIC-004.json | 40/40 |
| N1 | KANJI_MNEMONIC-005.json | 40/40 |
| N1 | KANJI_MNEMONIC-006.json | 40/40 |
| N1 | KANJI_MNEMONIC-007.json | 40/40 |
| N1 | KANJI_MNEMONIC-008.json | 40/40 |
| N1 | KANJI_MNEMONIC-009.json | 40/40 |
| N1 | KANJI_MNEMONIC-010.json | 40/40 |
| N1 | KANJI_MNEMONIC-011.json | 40/40 |
| N1 | KANJI_MNEMONIC-012.json | 40/40 |
| N1 | KANJI_MNEMONIC-013.json | 40/40 |
| N1 | KANJI_MNEMONIC-014.json | 40/40 |
| N1 | KANJI_MNEMONIC-015.json | 40/40 |
| N1 | RADICAL_NAME-001.json | 40/40 |
| N1 | RADICAL_NAME-002.json | 40/40 |
| N1 | RADICAL_NAME-003.json | 40/40 |
| N1 | RADICAL_NAME-004.json | 8/8 |
| N1 | TOPIC_ASSIGN-001.json | 40/40 |
| N1 | TOPIC_ASSIGN-002.json | 40/40 |
| N1 | TOPIC_ASSIGN-003.json | 40/40 |
| N1 | TOPIC_ASSIGN-004.json | 40/40 |
| N1 | TOPIC_ASSIGN-005.json | 40/40 |
| N1 | TOPIC_ASSIGN-006.json | 40/40 |
| N1 | TOPIC_ASSIGN-007.json | 40/40 |
| N1 | TOPIC_ASSIGN-008.json | 40/40 |
| N1 | TOPIC_ASSIGN-009.json | 40/40 |
| N1 | TOPIC_ASSIGN-010.json | 40/40 |
| N1 | TOPIC_ASSIGN-011.json | 40/40 |
| N1 | TOPIC_ASSIGN-012.json | 40/40 |
| N1 | TOPIC_ASSIGN-013.json | 40/40 |
| N1 | TOPIC_ASSIGN-014.json | 40/40 |
| N1 | TOPIC_ASSIGN-015.json | 40/40 |
| N1 | TOPIC_ASSIGN-016.json | 8/8 |
| N1 | VOCAB_EXAMPLE-001.json | 40/40 |
| N1 | VOCAB_EXAMPLE-002.json | 40/40 |
| N1 | VOCAB_EXAMPLE-003.json | 40/40 |
| N1 | VOCAB_EXAMPLE-004.json | 40/40 |
| N1 | VOCAB_EXAMPLE-005.json | 40/40 |
| N1 | VOCAB_EXAMPLE-006.json | 40/40 |
| N1 | VOCAB_EXAMPLE-007.json | 40/40 |
| N1 | VOCAB_EXAMPLE-008.json | 40/40 |
| N1 | VOCAB_EXAMPLE-009.json | 40/40 |
| N1 | VOCAB_EXAMPLE-010.json | 40/40 |
| N1 | VOCAB_EXAMPLE-011.json | 40/40 |
| N1 | VOCAB_EXAMPLE-012.json | 40/40 |
| N1 | VOCAB_EXAMPLE-013.json | 40/40 |
| N1 | VOCAB_EXAMPLE-014.json | 40/40 |
| N1 | VOCAB_EXAMPLE-015.json | 40/40 |
| N1 | VOCAB_EXAMPLE-016.json | 40/40 |
| N1 | VOCAB_EXAMPLE-017.json | 40/40 |
| N1 | VOCAB_EXAMPLE-018.json | 40/40 |
| N1 | VOCAB_EXAMPLE-019.json | 40/40 |
| N1 | VOCAB_EXAMPLE-020.json | 39/40 |
| N1 | VOCAB_EXAMPLE-021.json | 40/40 |
| N1 | VOCAB_EXAMPLE-022.json | 40/40 |
| N1 | VOCAB_EXAMPLE-023.json | 40/40 |
| N1 | VOCAB_EXAMPLE-024.json | 40/40 |
| N1 | VOCAB_EXAMPLE-025.json | 40/40 |
| N1 | VOCAB_EXAMPLE-026.json | 40/40 |
| N1 | VOCAB_EXAMPLE-027.json | 40/40 |
| N1 | VOCAB_EXAMPLE-028.json | 40/40 |
| N1 | VOCAB_EXAMPLE-029.json | 40/40 |
| N1 | VOCAB_EXAMPLE-030.json | 40/40 |
| N1 | VOCAB_EXAMPLE-031.json | 40/40 |
| N1 | VOCAB_EXAMPLE-032.json | 40/40 |
| N1 | VOCAB_EXAMPLE-033.json | 39/40 |
| N1 | VOCAB_EXAMPLE-034.json | 40/40 |
| N1 | VOCAB_EXAMPLE-035.json | 39/40 |
| N1 | VOCAB_EXAMPLE-036.json | 40/40 |
| N1 | VOCAB_EXAMPLE-037.json | 40/40 |
| N1 | VOCAB_EXAMPLE-038.json | 39/40 |
| N1 | VOCAB_EXAMPLE-039.json | 8/8 |
| N1 | VOCAB_MEANING-001.json | 40/40 |
| N1 | VOCAB_MEANING-002.json | 39/40 |
| N1 | VOCAB_MEANING-003.json | 40/40 |
| N1 | VOCAB_MEANING-004.json | 40/40 |
| N1 | VOCAB_MEANING-005.json | 40/40 |
| N1 | VOCAB_MEANING-006.json | 40/40 |
| N1 | VOCAB_MEANING-007.json | 40/40 |
| N1 | VOCAB_MEANING-008.json | 40/40 |
| N1 | VOCAB_MEANING-009.json | 40/40 |
| N1 | VOCAB_MEANING-010.json | 40/40 |
| N1 | VOCAB_MEANING-011.json | 40/40 |
| N1 | VOCAB_MEANING-012.json | 40/40 |
| N1 | VOCAB_MEANING-013.json | 40/40 |
| N1 | VOCAB_MEANING-014.json | 40/40 |
| N1 | VOCAB_MEANING-015.json | 40/40 |
| N1 | VOCAB_MEANING-016.json | 40/40 |
| N1 | VOCAB_MEANING-017.json | 40/40 |
| N1 | VOCAB_MEANING-018.json | 40/40 |
| N1 | VOCAB_MEANING-019.json | 18/18 |
| N1 | VOCAB_MNEMONIC-001.json | 40/40 |
| N1 | VOCAB_MNEMONIC-002.json | 40/40 |
| N1 | VOCAB_MNEMONIC-003.json | 40/40 |
| N1 | VOCAB_MNEMONIC-004.json | 40/40 |
| N1 | VOCAB_MNEMONIC-005.json | 40/40 |
| N1 | VOCAB_MNEMONIC-006.json | 40/40 |
| N1 | VOCAB_MNEMONIC-007.json | 39/40 |
| N1 | VOCAB_MNEMONIC-008.json | 40/40 |
| N1 | VOCAB_MNEMONIC-009.json | 40/40 |
| N1 | VOCAB_MNEMONIC-010.json | 40/40 |
| N1 | VOCAB_MNEMONIC-011.json | 40/40 |
| N1 | VOCAB_MNEMONIC-012.json | 40/40 |
| N1 | VOCAB_MNEMONIC-013.json | 40/40 |
| N1 | VOCAB_MNEMONIC-014.json | 40/40 |
| N1 | VOCAB_MNEMONIC-015.json | 40/40 |
| N1 | VOCAB_MNEMONIC-016.json | 40/40 |
| N1 | VOCAB_MNEMONIC-017.json | 40/40 |
| N1 | VOCAB_MNEMONIC-018.json | 40/40 |
| N1 | VOCAB_MNEMONIC-019.json | 40/40 |
| N1 | VOCAB_MNEMONIC-020.json | 40/40 |
| N1 | VOCAB_MNEMONIC-021.json | 40/40 |
| N1 | VOCAB_MNEMONIC-022.json | 40/40 |
| N1 | VOCAB_MNEMONIC-023.json | 40/40 |
| N1 | VOCAB_MNEMONIC-024.json | 40/40 |
| N1 | VOCAB_MNEMONIC-025.json | 40/40 |
| N1 | VOCAB_MNEMONIC-026.json | 40/40 |
| N1 | VOCAB_MNEMONIC-027.json | 40/40 |
| N1 | VOCAB_MNEMONIC-028.json | 40/40 |
| N1 | VOCAB_MNEMONIC-029.json | 40/40 |
| N1 | VOCAB_MNEMONIC-030.json | 40/40 |
| N1 | VOCAB_MNEMONIC-031.json | 40/40 |
| N1 | VOCAB_MNEMONIC-032.json | 40/40 |
| N1 | VOCAB_MNEMONIC-033.json | 40/40 |
| N1 | VOCAB_MNEMONIC-034.json | 40/40 |
| N1 | VOCAB_MNEMONIC-035.json | 40/40 |
| N1 | VOCAB_MNEMONIC-036.json | 40/40 |
| N1 | VOCAB_MNEMONIC-037.json | 40/40 |
| N1 | VOCAB_MNEMONIC-038.json | 40/40 |
| N1 | VOCAB_MNEMONIC-039.json | 40/40 |
| N1 | VOCAB_MNEMONIC-040.json | 40/40 |
| N1 | VOCAB_MNEMONIC-041.json | 40/40 |
| N1 | VOCAB_MNEMONIC-042.json | 40/40 |
| N1 | VOCAB_MNEMONIC-043.json | 40/40 |
| N1 | VOCAB_MNEMONIC-044.json | 40/40 |
| N1 | VOCAB_MNEMONIC-045.json | 40/40 |
| N1 | VOCAB_MNEMONIC-046.json | 40/40 |
| N1 | VOCAB_MNEMONIC-047.json | 40/40 |
| N1 | VOCAB_MNEMONIC-048.json | 40/40 |
| N1 | VOCAB_MNEMONIC-049.json | 40/40 |
| N1 | VOCAB_MNEMONIC-050.json | 40/40 |
| N1 | VOCAB_TYPE-001.json | 40/40 |
| N1 | VOCAB_TYPE-002.json | 40/40 |
| N1 | VOCAB_TYPE-003.json | 40/40 |
| N1 | VOCAB_TYPE-004.json | 40/40 |
| N1 | VOCAB_TYPE-005.json | 40/40 |
| N1 | VOCAB_TYPE-006.json | 40/40 |
| N1 | VOCAB_TYPE-007.json | 40/40 |
| N1 | VOCAB_TYPE-008.json | 40/40 |
| N1 | VOCAB_TYPE-009.json | 40/40 |
| N1 | VOCAB_TYPE-010.json | 40/40 |
| N1 | VOCAB_TYPE-011.json | 40/40 |
| N1 | VOCAB_TYPE-012.json | 40/40 |
| N1 | VOCAB_TYPE-013.json | 40/40 |
| N1 | VOCAB_TYPE-014.json | 40/40 |
| N1 | VOCAB_TYPE-015.json | 40/40 |
| N1 | VOCAB_TYPE-016.json | 40/40 |
| N1 | VOCAB_TYPE-017.json | 40/40 |
| N1 | VOCAB_TYPE-018.json | 40/40 |
| N1 | VOCAB_TYPE-019.json | 40/40 |
| N1 | VOCAB_TYPE-020.json | 40/40 |
| N1 | VOCAB_TYPE-021.json | 40/40 |
| N1 | VOCAB_TYPE-022.json | 40/40 |
| N1 | VOCAB_TYPE-023.json | 40/40 |
| N1 | VOCAB_TYPE-024.json | 40/40 |
| N1 | VOCAB_TYPE-025.json | 40/40 |
| N1 | VOCAB_TYPE-026.json | 40/40 |
| N1 | VOCAB_TYPE-027.json | 40/40 |
| N1 | VOCAB_TYPE-028.json | 40/40 |
| N1 | VOCAB_TYPE-029.json | 40/40 |
| N1 | VOCAB_TYPE-030.json | 40/40 |
| N1 | VOCAB_TYPE-031.json | 40/40 |
| N1 | VOCAB_TYPE-032.json | 40/40 |
| N1 | VOCAB_TYPE-033.json | 40/40 |
| N1 | VOCAB_TYPE-034.json | 40/40 |
| N1 | VOCAB_TYPE-035.json | 40/40 |
| N1 | VOCAB_TYPE-036.json | 40/40 |
| N1 | VOCAB_TYPE-037.json | 40/40 |
| N1 | VOCAB_TYPE-038.json | 40/40 |
| N1 | VOCAB_TYPE-039.json | 40/40 |
| N1 | VOCAB_TYPE-040.json | 40/40 |
| N1 | VOCAB_TYPE-041.json | 40/40 |
| N1 | VOCAB_TYPE-042.json | 40/40 |
| N1 | VOCAB_TYPE-043.json | 40/40 |
| N1 | VOCAB_TYPE-044.json | 40/40 |
| N1 | VOCAB_TYPE-045.json | 40/40 |
| N1 | VOCAB_TYPE-046.json | 40/40 |
| N1 | VOCAB_TYPE-047.json | 40/40 |
| N1 | VOCAB_TYPE-048.json | 40/40 |
| N1 | VOCAB_TYPE-049.json | 40/40 |
| N1 | VOCAB_TYPE-050.json | 4/4 |
