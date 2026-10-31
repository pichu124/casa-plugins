---
name: ra-soat-hoi-dap
description: Gom các câu phụ huynh hỏi mà bot Messenger của Casa phải chuyển tư vấn viên, nhóm theo ý, rồi soạn cặp hỏi đáp mới để trường duyệt trước khi thêm vào bot. Dùng khi người dùng hỏi "bot chưa trả lời được câu nào", "rà soát hỏi đáp", "bổ sung câu trả lời cho bot", "câu nào phải chuyển tư vấn viên nhiều".
argument-hint: "[khoảng thời gian, mặc định 2 tuần gần nhất]"
---

# /ra-soat-hoi-dap

> **Trạng thái: khung (đợt 1).** Luồng làm việc đã thống nhất. Định dạng bàn giao cho bot và quy trình duyệt làm ở đợt 2.

Đọc trước: [bối cảnh Casa](../../references/boi-canh-casa.md) (mục 5 về giọng văn), [dữ liệu lead](../../references/du-lieu-lead.md).

## Dữ liệu vào

- Tab `Chủ đề`, các dòng có `Chuyển tư vấn viên` = `Có`, đọc qua `~~spreadsheet`.
- Bộ hỏi đáp hiện có của bot: `data/qa_database.json` trong repo `casa_preschool-messenger-bot` (người dùng gửi file hoặc cấp quyền đọc repo). Thêm `docs/quyet-dinh-noi-dung.md` cho các quyết định nội dung trường đã chốt.

## Các bước

1. Lấy các câu đã chuyển tư vấn viên trong kỳ. Bỏ thông tin cá nhân còn sót.
2. Gom các câu cùng ý thành nhóm, đếm số lần và số phụ huynh.
3. Đối chiếu với bộ hỏi đáp hiện có và chia mỗi nhóm thành một trong ba loại:
   - **Chưa có**: cần cặp hỏi đáp mới.
   - **Đã có nhưng bot vẫn chuyển**: ghi lại để xem cách diễn đạt hay từ khóa, không soạn trùng.
   - **Không nên để bot trả lời**: cần người xử lý, ví dụ khiếu nại, sức khỏe riêng của bé, xin bảng học phí chi tiết, thương lượng ưu đãi.
4. Với nhóm "Chưa có": soạn câu hỏi mẫu, vài cách hỏi khác và câu trả lời theo giọng văn của Casa. Câu trả lời chỉ dùng thông tin có trong bối cảnh và tài liệu của bot. Thông tin nào còn thiếu thì đánh dấu **[CẦN TRƯỜNG XÁC NHẬN]**, không tự bịa.
5. Xuất danh sách để trường duyệt, xếp theo số lần phụ huynh hỏi.

## Ranh giới

- Chỉ soạn bản nháp. Không sửa `qa_database.json`, không đổi bot, không nhắn phụ huynh.
- Không làm trùng phần nhắc tư vấn viên của bot.

## Việc còn lại ở đợt 2

- Định dạng bàn giao khớp với schema `qa_database.json` (hoặc Sheet hỏi đáp `docs/google-sheet-qa.md` của bot) để người vận hành dán vào dễ dàng.
- Quy trình duyệt: ai duyệt, duyệt ở đâu (Google Doc, Sheet hay comment).
