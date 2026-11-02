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

- `bao-cao-tuan` dùng được: báo cáo đầy đủ trong chat, bản tóm tắt để dán nhóm Zalo, bản nháp Gmail. Chạy tự động 8h sáng thứ Hai bằng tác vụ hẹn giờ (xem dưới).
- `chu-de-noi-dung` dùng được: xếp hạng chủ đề và gợi ý nội dung cho Facebook, Zalo OA, Website.
- `ra-soat-hoi-dap` vẫn ở dạng **khung** (ưu tiên thấp nhất).
- Hàm dùng chung (chuẩn hóa cơ sở, tuổi bé, ẩn SĐT) nằm ở `scripts/casa_chung.py`.

Bộ kiểm tra hành vi của skill nằm ở [`evals/`](evals/README.md).

## Cài đặt

```
/plugin install casa-ops --marketplace pichu124/casa-plugins
```

## Connector

Google Sheets, Google Drive và Gmail, xem [CONNECTORS.md](CONNECTORS.md). Zalo, Zalo OA và MISA chưa có connector.

## Chạy báo cáo tuần tự động (8h sáng thứ Hai)

Làm một lần, trong app Claude (Cowork):

1. Kết nối **Google Sheets** và **Gmail** ở Cài đặt → Connectors.
2. Tạo một **tác vụ hẹn giờ** (scheduled task) mới, lặp lại **mỗi thứ Hai lúc 8:00** giờ Việt Nam.
3. Dán nội dung sau, thay link Sheet và email người nhận:

   ```
   Lập báo cáo lead tuần trước của Casa từ Sheet lead: <link Google Sheet>.
   Đưa bản tóm tắt ngắn để dán Zalo, và tạo bản nháp Gmail gửi <email người nhận>.
   ```
4. Sáng thứ Hai: mở Gmail, xem bản nháp, bấm gửi. Copy bản tóm tắt ngắn dán vào nhóm Zalo.

Báo cáo chỉ tạo bản nháp email, không tự gửi. Tên mục "tác vụ hẹn giờ" trong app có thể khác một chút tùy phiên bản.

## Nguyên tắc

- Plugin chỉ đọc dữ liệu và soạn bản nháp. Không nhắn phụ huynh, không nhắc tư vấn viên vì bot Messenger đã làm phần này.
- Báo cáo không in SĐT đầy đủ, chỉ ghi tên kèm 4 số cuối.
- Không đưa dữ liệu thật của phụ huynh và trẻ vào repo.
