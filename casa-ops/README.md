# casa-ops

Plugin riêng của **Casa dei Bambini**, hệ thống mầm non ở Hà Nội (Chùa Láng, Mỹ Đình, Kim Mã), nhận bé từ 15 tháng đến 6 tuổi.

## Thành phần

| Thành phần | Nội dung |
|---|---|
| [`references/boi-canh-casa.md`](references/boi-canh-casa.md) | Cơ sở, chương trình theo tuổi, học phí, USP, giọng văn với phụ huynh, quy ước Việt Nam, quy tắc dữ liệu cá nhân |
| [`references/du-lieu-lead.md`](references/du-lieu-lead.md) | Cấu trúc Sheet lead của bot (tab Leads, Chủ đề), cách chuẩn hóa, phân việc với bot, dữ liệu chăm sóc lead dự kiến |
| `skills/bao-cao-tuan` | Báo cáo lead hằng tuần (8h sáng thứ Hai) |
| `skills/chu-de-noi-dung` | Top chủ đề phụ huynh hỏi → gợi ý nội dung và quảng cáo |
| `skills/ra-soat-hoi-dap` | Câu bot phải chuyển tư vấn viên → soạn cặp hỏi đáp mới để trường duyệt |

Cả 3 skill đang ở dạng **khung** (đợt 1) và sẽ hoàn thiện ở đợt 2.

## Connector

Google Sheets và Google Drive, xem [CONNECTORS.md](CONNECTORS.md).

## Nguyên tắc

- Plugin chỉ đọc dữ liệu và soạn bản nháp. Không nhắn phụ huynh, không nhắc tư vấn viên vì bot Messenger đã làm phần này.
- Báo cáo không in SĐT đầy đủ, chỉ ghi tên kèm 4 số cuối.
- Không đưa dữ liệu thật của phụ huynh và trẻ vào repo.
