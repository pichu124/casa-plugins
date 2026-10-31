---
name: ra-soat-hoi-dap
description: Rà soát chất lượng bộ hỏi đáp của bot Messenger Casa mỗi tháng một lần. Tìm các cặp trùng hoặc gần trùng để gộp, các cặp mâu thuẫn (vd học phí cũ và mới), câu trả lời lệch giọng văn chuẩn, và những câu phụ huynh hỏi lặp lại mà bot chưa học vì xếp là "chuyện riêng". Kết quả là danh sách đề xuất để trường duyệt. Dùng khi người dùng hỏi "rà soát hỏi đáp", "dọn bộ Q&A của bot", "có câu nào trùng hay mâu thuẫn không", hoặc khi đến kỳ rà soát hằng tháng.
argument-hint: "[tháng cần rà soát, mặc định là tháng trước]"
---

# /ra-soat-hoi-dap

> **Trạng thái: khung (đợt 1).** Mục tiêu và các bước đã thống nhất. Định dạng đề xuất và quy trình duyệt làm ở đợt 2. **Ưu tiên thấp nhất trong 3 skill**: hiện có khoảng 110 cặp hỏi đáp, rất ít cặp do bot tự học. Skill này làm sau cùng trong đợt 2, hoặc làm sớm hơn khi số cặp tự học tăng nhiều.

Đọc trước: [bối cảnh Casa](../../references/boi-canh-casa.md) (mục 5 về giọng văn), [dữ liệu lead](../../references/du-lieu-lead.md).

## Vì sao cần rà soát

Bot đã **tự học** cặp hỏi đáp mới. Khi tư vấn viên trả lời thẻ "CẦN TRỢ GIÚP" trên Telegram và đó là thông tin chung của trường, bot thêm cặp vào `data/qa_database.json` (có `source: "admin"` và `learned_at`). Khi bot học nhầm, tư vấn viên dùng lệnh `/quen`. Skill này **không** soạn câu hỏi mới, vì việc đó bot đã làm.

Bot chỉ thêm cặp mới vào cuối danh sách. Nó không gộp các cặp trùng và không phát hiện mâu thuẫn. Mỗi tin nhắn bot lại gửi toàn bộ danh sách hỏi đáp cho AI, nên càng nhiều cặp thừa thì bot càng chậm và tốn token, còn cặp mâu thuẫn làm bot trả lời sai.

## Dữ liệu vào

- **Bộ hỏi đáp hiện hành.** Nguồn chính là `data/qa_database.json` trên nhánh `main` của repo `casa_preschool-messenger-bot`, khóa `qa_pairs`. Mỗi cặp có `questions`, `answer`, `keywords`, `category`, `images`, `source`, `learned_at`, `tg_message_id`. Không đọc được repo thì dùng tab `Q&A` của Sheet "Bộ Q&A tư vấn – Casa dei Bambini" (Sheet tự đồng bộ mỗi giờ, đọc qua `~~spreadsheet`), hoặc endpoint `/qa-learned` của bot cho các cặp tự học.
- **Câu phụ huynh hỏi.** Tab `Chủ đề` của Sheet lead, các dòng có `Chuyển tư vấn viên` = `Có`, trong tháng rà soát.
- **Chuẩn so sánh.** `docs/quy-chuan-ngon-ngu.md` và `docs/quyet-dinh-noi-dung.md` của repo bot.

## Các bước

1. **Gộp trùng.** Tìm các cặp có câu hỏi trùng hoặc gần trùng ý. Đề xuất giữ một cặp, gộp các cách hỏi (`questions`, `keywords`) vào cặp đó, và chỉ ra cặp nào bỏ. Ưu tiên giữ cặp trường soạn sẵn, tức cặp không có `source: "admin"`, trừ khi cặp tự học có thông tin mới hơn.
2. **Đánh dấu mâu thuẫn.** Tìm các cặp trả lời khác nhau về cùng một thông tin: học phí, giờ đón, ưu đãi, độ tuổi, quy định thu… Đối chiếu với `quyet-dinh-noi-dung.md` và bối cảnh Casa, ghi rõ hai bên nói gì và `learned_at` của từng cặp. **Không tự chọn bên đúng**: để trường quyết.
3. **Sửa giọng văn.** Với câu trả lời lệch `quy-chuan-ngon-ngu.md` (xưng hô, câu cụt, từ ngữ quá "sale", quá dài, hỏi dồn nhiều thông tin), đề xuất câu viết lại. Giữ nguyên nội dung, chỉ sửa cách nói.
4. **Câu "chuyện riêng" lặp lại.** Khi tư vấn viên trả lời một câu mà bot xếp là chuyện riêng, bot báo 🔒 và không học câu đó. Gom các câu đã chuyển tư vấn viên trong tháng theo ý, rồi đối chiếu với bộ hỏi đáp. Ý nào được nhiều phụ huynh hỏi lại mà vẫn chưa có trong bộ hỏi đáp là ứng viên thông tin chung. Đề xuất cặp hỏi đáp và đánh dấu **[CẦN TRƯỜNG XÁC NHẬN]** cho câu trả lời. Không đưa tên bé hay chi tiết riêng của một gia đình vào cặp đề xuất.
5. **Xuất đề xuất.** Chia thành 4 nhóm theo 4 bước trên, kèm số cặp trước và sau khi rà soát. Trong mỗi nhóm, mục nào ảnh hưởng nhiều phụ huynh hơn thì xếp trước.

## Sau khi trường duyệt

- Đưa các thay đổi đã duyệt vào `data/qa_database.json` qua **PR nháp** ở repo bot. Chạy test của repo bot (repo có test kiểm tra kiến thức) trước khi mở PR.
- **Không push thẳng lên `main` của repo bot**: push lên `main` là deploy. Bot cũng tự đẩy các cặp tự học lên `main`, nên phải lấy bản mới nhất ngay trước khi sửa để không ghi đè cặp vừa học.
- Sau khi PR được gộp, người vận hành gọi `POST /reload-qa` để bot nạp bộ hỏi đáp mới.

## Ranh giới

- Chỉ đề xuất. Không tự xoá hay sửa cặp hỏi đáp khi trường chưa duyệt.
- Không nhắn phụ huynh, không nhắc tư vấn viên, không thay thế lệnh `/quen`.

## Việc còn lại ở đợt 2

- Định dạng đề xuất để trường duyệt: Google Doc, Sheet hay comment trên PR.
- Cách chạy hằng tháng: tác vụ hẹn giờ trong Cowork hoặc Claude Code.
- Bước 4 hiện phải đoán gián tiếp từ tab `Chủ đề`, vì Sheet không ghi riêng câu nào bị báo 🔒. Cần hỏi bên bot có ghi được các câu này ở đâu không (vd thêm một cột trong tab `Chủ đề`).
