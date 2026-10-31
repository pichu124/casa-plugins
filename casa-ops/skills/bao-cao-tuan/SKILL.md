---
name: bao-cao-tuan
description: Lập báo cáo lead hằng tuần cho Casa dei Bambini từ Google Sheet của bot Messenger. Báo cáo gồm lead mới, số lead theo giai đoạn, theo cơ sở và độ tuổi, tỷ lệ có SĐT → hẹn, lead từ quảng cáo, so sánh với tuần trước, và lead có SĐT quá 48 giờ chưa liên hệ. Dùng khi người dùng hỏi "báo cáo tuần", "tuần rồi có bao nhiêu lead", "tình hình tuyển sinh tuần này", hoặc khi tác vụ hẹn 8h sáng thứ Hai chạy.
argument-hint: "[tuần cần báo cáo, mặc định là tuần trước]"
---

# /bao-cao-tuan

> **Trạng thái: khung (đợt 1).** Các chỉ số và cách tính dưới đây đã thống nhất. Mẫu báo cáo chi tiết, cách chạy tự động lúc 8h thứ Hai và phần dữ liệu chăm sóc lead làm ở đợt 2.

Đọc trước: [bối cảnh Casa](../../references/boi-canh-casa.md), [dữ liệu lead](../../references/du-lieu-lead.md), [connector](../../CONNECTORS.md).

## Dữ liệu vào

- Tab `Leads` của Sheet lead, đọc qua `~~spreadsheet`. Chưa kết nối thì nhờ người dùng tải file `.xlsx`/`.csv`.
- Kỳ báo cáo mặc định: **tuần trước**, từ 00:00 thứ Hai đến 23:59 Chủ nhật, giờ Việt Nam. Kỳ so sánh là tuần liền trước đó.

## Chỉ số

| # | Chỉ số | Cách tính |
|---|---|---|
| 1 | Lead mới | Số hàng có `Lần đầu liên hệ` trong kỳ |
| 2 | Theo giai đoạn | Lead mới trong kỳ, đếm theo giai đoạn chính (bỏ hậu tố ` · Đã liên hệ`). Thêm một cột "đã liên hệ" |
| 3 | Theo cơ sở | Chuẩn hóa `Cơ sở/hệ` về Chùa Láng / Mỹ Đình / Kim Mã / Chưa rõ |
| 4 | Theo độ tuổi | Chuẩn hóa `Tuổi bé` về các nhóm tuổi trong file dữ liệu lead |
| 5 | Tỷ lệ có SĐT → hẹn | Trong số lead mới có SĐT: tỷ lệ ở `Đã hẹn tham quan/học thử` (đã chốt). Ghi riêng số `Muốn hẹn` chưa chốt |
| 6 | Lead từ quảng cáo | Lead mới có cột `Quảng cáo`, chia theo tên quảng cáo, kèm tỷ lệ có SĐT của từng quảng cáo |
| 7 | So với tuần trước | Chỉ số 1, 5, 6 của tuần trước, chênh lệch tuyệt đối và % |
| 8 | Có SĐT quá 48 giờ chưa liên hệ | Mọi lead (không giới hạn kỳ) có SĐT, giai đoạn không có hậu tố ` · Đã liên hệ`, không phải `Không quan tâm`, chưa chốt hẹn, và đã quá 48 giờ tính đến lúc chạy báo cáo. Mốc tính là lúc có SĐT; Sheet không có cột riêng nên dùng `Cập nhật lúc` khi `Sự kiện` là `SĐT mới`, nếu không thì dùng `Lần đầu liên hệ` |

Chỉ số 8 để chủ nắm tình hình trong báo cáo tuần. Báo cáo không nhắc từng tư vấn viên vì bot đã nhắc trên Telegram.

## Đầu ra (bản nháp, chốt ở đợt 2)

1. Ba dòng tóm tắt: lead mới, tỷ lệ SĐT → hẹn, chênh lệch so với tuần trước.
2. Các bảng theo giai đoạn, cơ sở, độ tuổi, quảng cáo.
3. Danh sách lead có SĐT quá 48 giờ chưa liên hệ: **tên kèm 4 số cuối SĐT**, cơ sở, tuổi bé, số giờ đã chờ. Không in SĐT đầy đủ và Customer ID.
4. Ghi chú về dữ liệu: số hàng không rõ cơ sở hay tuổi, hàng bị lỗi định dạng.

## Việc còn lại ở đợt 2

- Chốt mẫu trình bày: tin nhắn ngắn, Google Doc hay file đính kèm, và gửi đi kênh nào.
- Cách chạy lúc 8h sáng thứ Hai: tác vụ hẹn giờ trong Cowork hoặc Claude Code.
- Khi có Nhật ký chăm sóc (mục 3 file dữ liệu lead), thêm: lead theo sale, tỷ lệ chốt theo sale, lead bị bỏ quên, lead "Rất quan tâm" chưa chốt, lý do từ chối, chất lượng lead theo nguồn và chiến dịch, phễu Lead mới → Nhập học.
