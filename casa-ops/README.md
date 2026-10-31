# casa-ops

Plugin riêng của **Casa dei Bambini**, hệ thống mầm non ở Hà Nội (Chùa Láng, Mỹ Đình, Kim Mã), nhận bé từ 15 tháng đến 6 tuổi.

## Thành phần

| Thành phần | Nội dung |
|---|---|
| [`references/boi-canh-casa.md`](references/boi-canh-casa.md) | Cơ sở, chương trình theo tuổi, học phí, USP, giọng văn với phụ huynh, quy ước Việt Nam, quy tắc dữ liệu cá nhân |
| [`references/du-lieu-lead.md`](references/du-lieu-lead.md) | Cấu trúc Sheet lead của bot (tab Leads, Chủ đề), cách chuẩn hóa, phân việc với bot, dữ liệu chăm sóc lead dự kiến |
| `skills/bao-cao-tuan` | Báo cáo lead hằng tuần (8h sáng thứ Hai) |
| `skills/chu-de-noi-dung` | Top chủ đề phụ huynh hỏi → gợi ý nội dung và quảng cáo |
| `skills/ra-soat-hoi-dap` | Rà soát chất lượng bộ hỏi đáp của bot hằng tháng: gộp trùng, đánh dấu mâu thuẫn, sửa giọng văn, tìm câu đáng thành thông tin chung |

`bao-cao-tuan` đã có script tính toán (`scripts/bao_cao_tuan.py`) và test bằng dữ liệu giả; còn chờ khảo sát để chốt kênh gửi và lịch chạy tự động. `chu-de-noi-dung` và `ra-soat-hoi-dap` vẫn ở dạng **khung**.

Bộ kiểm tra hành vi của skill nằm ở [`evals/`](evals/README.md).

## Cài đặt

```
/plugin install casa-ops --marketplace pichu124/casa-plugins
```

## Connector

Google Sheets và Google Drive, xem [CONNECTORS.md](CONNECTORS.md).

## Nguyên tắc

- Plugin chỉ đọc dữ liệu và soạn bản nháp. Không nhắn phụ huynh, không nhắc tư vấn viên vì bot Messenger đã làm phần này.
- Báo cáo không in SĐT đầy đủ, chỉ ghi tên kèm 4 số cuối.
- Không đưa dữ liệu thật của phụ huynh và trẻ vào repo.
