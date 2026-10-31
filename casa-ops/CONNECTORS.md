# Connector

| Nhóm | Ký hiệu trong skill | Dùng để | Công cụ |
|---|---|---|---|
| Bảng tính | `~~spreadsheet` | Đọc tab **Leads** và **Chủ đề** do bot Messenger ghi | Google Sheets |
| Lưu trữ tài liệu | `~~cloud storage` | Tìm file Sheet lead, tài liệu giới thiệu trường, ảnh cơ sở vật chất | Google Drive |

`google sheets` để URL trống: Claude dùng connector Google Sheets mà người dùng đã kết nối trong claude.ai (Cài đặt → Connectors).

Chưa có connector nào thì skill vẫn chạy được với file người dùng tải lên (xuất Sheet ra `.xlsx` hoặc `.csv`).

Connector bổ sung (Zalo OA, Facebook Ads, LittleLives…) sẽ quyết ở đợt 2, theo công cụ trường đang dùng.
