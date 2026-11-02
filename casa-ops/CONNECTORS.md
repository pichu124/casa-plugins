# Connector

Chọn theo công cụ trường đang dùng (khảo sát 02/11/2026): Google Sheets làm CRM, Google Drive, Gmail, Zalo để trao đổi nội bộ.

| Nhóm | Ký hiệu trong skill | Dùng để | Công cụ |
|---|---|---|---|
| Bảng tính | `~~spreadsheet` | Đọc tab **Leads** và **Chủ đề** do bot Messenger ghi | Google Sheets |
| Lưu trữ tài liệu | `~~cloud storage` | Tìm file Sheet lead, tài liệu giới thiệu trường, ảnh cơ sở vật chất | Google Drive |
| Email | `~~email` | Tạo **bản nháp** email báo cáo tuần để người dùng xem rồi tự bấm gửi | Gmail |

`google sheets` và `gmail` để URL trống: Claude dùng connector mà người dùng đã kết nối trong claude.ai (Cài đặt → Connectors).

Chưa có connector nào thì skill vẫn chạy được với file người dùng tải lên (xuất Sheet ra `.xlsx` hoặc `.csv`), và báo cáo hiện ngay trong khung chat.

## Không có connector

- **Zalo** (nhóm chat nội bộ) và **Zalo OA**: chưa có connector. Báo cáo tuần có bản tóm tắt chữ thường (`--format ngan`) để người dùng dán vào nhóm Zalo. Nội dung cho Zalo OA được soạn sẵn để người dùng đăng tay.
- **MISA** (kế toán): không kết nối. Plugin không đụng tới số liệu kế toán.
- **Facebook Ads**: trường chưa xác định ngân sách quảng cáo, nên chưa thêm. Gợi ý quảng cáo dừng ở mức ý tưởng.
