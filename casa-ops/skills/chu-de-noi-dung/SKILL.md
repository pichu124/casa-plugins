---
name: chu-de-noi-dung
description: Tổng hợp các chủ đề phụ huynh hỏi nhiều nhất trên Messenger (tab Chủ đề của Sheet lead) rồi gợi ý nội dung bài đăng và quảng cáo cho Casa dei Bambini. Dùng khi người dùng hỏi "phụ huynh hay hỏi gì", "tháng này nên đăng gì", "gợi ý nội dung quảng cáo", "chủ đề nào đang nóng".
argument-hint: "[khoảng thời gian, cơ sở hoặc quảng cáo cần xem]"
---

# /chu-de-noi-dung

> **Trạng thái: khung (đợt 1).** Cách tổng hợp đã thống nhất. Mẫu gợi ý nội dung, số bài mỗi kỳ và kênh đăng làm ở đợt 2.

Đọc trước: [bối cảnh Casa](../../references/boi-canh-casa.md) (mục 4 về USP và khó khăn, mục 5 về giọng văn), [dữ liệu lead](../../references/du-lieu-lead.md).

## Dữ liệu vào

- Tab `Chủ đề` của Sheet lead, đọc qua `~~spreadsheet`. Mặc định lấy 30 ngày gần nhất.
- Có thể lọc theo cơ sở, nhóm tuổi hoặc tên quảng cáo.

## Các bước

1. Tách cột `Chủ đề` (nhiều chủ đề nối bằng `, `) và đếm số lần cùng số phụ huynh khác nhau (theo Customer ID) cho mỗi chủ đề.
2. Xếp hạng top chủ đề, kèm xu hướng so với kỳ trước.
3. Cắt theo cơ sở, nhóm tuổi và quảng cáo: quảng cáo nào kéo về câu hỏi gì.
4. Đọc mẫu `Câu hỏi` của từng chủ đề top để hiểu phụ huynh thật sự băn khoăn điều gì. Trích tối đa vài câu, đã bỏ thông tin cá nhân.
5. Gợi ý nội dung: mỗi chủ đề top có 1 – 2 ý bài đăng và 1 ý quảng cáo. Mỗi ý gồm thông điệp chính, USP liên quan, gợi ý hình ảnh hay video, và lời kêu gọi theo giọng văn của Casa.

## Lưu ý

- Chủ đề `Học phí` thường đứng đầu. Nội dung nên nói về giá trị (Cambridge, giáo viên nước ngoài toàn thời gian, cam kết không tăng học phí) và mời để lại SĐT/Zalo. Không đăng bảng học phí.
- Không dùng các từ sale bị tránh (mục 5 bối cảnh). Không hứa điều trường chưa xác nhận.
- Có thể dùng thêm plugin `marketing` để soạn bài chi tiết, nhưng phải giữ bối cảnh và giọng văn của Casa.

## Việc còn lại ở đợt 2

- Mẫu đầu ra: lịch nội dung tuần hay tháng, số ý mỗi kỳ.
- Kênh đăng (Facebook, Zalo OA, TikTok…) và connector tương ứng, theo kết quả khảo sát.
- Nối với số liệu quảng cáo (chi phí, lead mỗi quảng cáo) nếu trường có connector Facebook Ads.
