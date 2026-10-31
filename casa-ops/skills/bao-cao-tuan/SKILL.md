---
name: bao-cao-tuan
description: Lập báo cáo lead hằng tuần cho Casa dei Bambini từ tab Leads của Google Sheet bot Messenger. Báo cáo gồm lead mới, số lead theo giai đoạn, theo cơ sở và độ tuổi, tỷ lệ có SĐT → đã hẹn, lead từ quảng cáo, so sánh với tuần trước, và lead có SĐT quá 48 giờ chưa liên hệ. Dùng khi người dùng hỏi "báo cáo tuần", "tuần rồi có bao nhiêu lead / bao nhiêu phụ huynh mới", "tình hình tuyển sinh tuần này", "lead nào chưa ai gọi", hoặc khi tác vụ hẹn giờ 8h sáng thứ Hai chạy.
argument-hint: "[tuần cần báo cáo, mặc định là tuần trước]"
---

# /bao-cao-tuan

Đọc trước: [bối cảnh Casa](../../references/boi-canh-casa.md), [dữ liệu lead](../../references/du-lieu-lead.md), [connector](../../CONNECTORS.md).

Mọi con số đều do script `scripts/bao_cao_tuan.py` tính, để lần nào chạy cũng ra cùng kết quả. Claude không tự đếm bằng mắt khi chạy được script.

## Bước 1. Xác định kỳ báo cáo

- Mặc định là **tuần trước**: từ 00:00 thứ Hai đến 23:59:59 Chủ nhật, giờ Việt Nam. Chạy lúc 8h sáng thứ Hai thì kỳ báo cáo là tuần vừa kết thúc.
- Người dùng nêu tuần khác ("tuần 19/10", "tuần này") thì lấy một ngày trong tuần đó làm `--tuan`. "Tuần này" chưa hết tuần thì nói rõ số liệu mới tính đến lúc chạy.
- Kỳ so sánh luôn là tuần liền trước kỳ báo cáo.

## Bước 2. Lấy dữ liệu tab Leads

Theo thứ tự ưu tiên:

1. **Connector `~~spreadsheet`** (Google Sheets): đọc toàn bộ tab `Leads`, cả hàng tiêu đề. Ghi ra file CSV UTF-8 trong thư mục làm việc tạm, giữ nguyên tiêu đề cột. Chưa biết Sheet nào thì hỏi người dùng link, hoặc tìm bằng `~~cloud storage` file tên kiểu "Casa – Lead Messenger".
2. **File người dùng tải lên**: `.csv` hoặc `.xlsx` xuất từ tab Leads, dùng thẳng.
3. Không có cả hai: hỏi người dùng link Sheet hoặc file. **Không tự bịa số liệu.**

Cần lấy **mọi hàng**, không chỉ hàng của tuần báo cáo: phần so sánh dùng tuần trước, còn danh sách chờ quá 48 giờ dùng mọi lead.

File CSV tạm chứa dữ liệu thật: để trong thư mục tạm, không đưa vào repo hay gửi đi nơi khác.

## Bước 3. Chạy script

```bash
python3 scripts/bao_cao_tuan.py <file> --now "<giờ Việt Nam hiện tại, YYYY-MM-DD HH:MM>" [--tuan YYYY-MM-DD] [--format json]
```

- `--now` phải là giờ Việt Nam (UTC+7). Môi trường chạy thường để giờ UTC, nên luôn truyền `--now` cho chắc.
- Mặc định script in báo cáo Markdown. Dùng `--format json` khi cần số liệu để làm tiếp (vẽ biểu đồ, so sánh nhiều tuần).
- Script chỉ dùng thư viện chuẩn Python. File `.xlsx` cần thêm `openpyxl`; không có thì xuất CSV.

Không chạy được Python thì tính tay theo đúng các quy tắc ở bước 4, và ghi ở đầu báo cáo là số liệu tính tay.

## Bước 4. Quy tắc tính (script đã làm theo đúng các quy tắc này)

| # | Chỉ số | Cách tính |
|---|---|---|
| 1 | Lead mới | Hàng có `Lần đầu liên hệ` trong kỳ. Hàng không đọc được ngày thì bỏ qua và ghi chú. Trùng `Customer ID` thì chỉ tính hàng đầu |
| 2 | Theo giai đoạn | Lead mới, đếm theo giai đoạn chính sau khi bỏ hậu tố ` · Đã liên hệ`. Đếm riêng số lead có hậu tố đó. Chữ cũ `Hẹn tham quan/học thử` tính là `Muốn hẹn` |
| 3 | Theo cơ sở | Chuẩn hóa `Cơ sở/hệ` theo file dữ liệu lead. Nhắc nhiều cơ sở cùng lúc thì là `Chưa rõ` |
| 4 | Theo độ tuổi | Chuẩn hóa `Tuổi bé` theo file dữ liệu lead (lấy điểm giữa của khoảng tuổi có thể) |
| 5 | Có SĐT → đã hẹn | Trong lead mới có SĐT (từ 9 chữ số): tỷ lệ ở giai đoạn `Đã hẹn tham quan/học thử`, kể cả khi có hậu tố. **`Muốn hẹn` chưa chốt không tính là đã hẹn**, đếm riêng |
| 6 | Lead từ quảng cáo | Lead mới có chữ ở cột `Quảng cáo`. Chia theo tên quảng cáo, kèm số có SĐT, tỷ lệ có SĐT, số đã hẹn |
| 7 | So với tuần trước | Chỉ số 1, 5, 6. Chênh lệch tuyệt đối và %; tỷ lệ thì chênh theo điểm % |
| 8 | Có SĐT quá 48 giờ chưa liên hệ | Mọi lead (không chỉ kỳ báo cáo): có SĐT, không có hậu tố ` · Đã liên hệ`, không ở `Đã hẹn` hay `Không quan tâm`, và đã quá 48 giờ tính đến `--now`. Mốc tính: `Cập nhật lúc` khi `Sự kiện` là `SĐT mới` hoặc `Đổi SĐT`; còn lại dùng `Lần đầu liên hệ` (nên có thể tính dư giờ chờ) |

## Bước 5. Trình bày

- Giữ nguyên các con số script in ra. Có thể thêm 2 – 3 câu nhận xét ngắn ở cuối (vd quảng cáo nào có tỷ lệ để lại SĐT thấp, cơ sở nào tăng hay giảm), nhưng không thêm con số mới mà script không tính.
- **Không in SĐT đầy đủ, không in Customer ID.** Danh sách phụ huynh chỉ ghi tên kèm 4 số cuối, vd `Hoa Thử (…0402)`.
- Báo cáo dành cho chủ và quản lý, viết ngắn gọn. Không cần giọng văn "Ba/Mẹ".
- Danh sách chờ quá 48 giờ là để chủ nắm tình hình. **Không** nhắn tư vấn viên hay phụ huynh: bot đã nhắc tư vấn viên trên Telegram.
- Ghi chú về dữ liệu (hàng lỗi ngày, trùng ID, chưa rõ cơ sở hay tuổi) giữ ở cuối, để trường biết chỗ cần sửa trên Sheet.

## Kiểm tra

- Test của script, chạy bằng dữ liệu giả `tests/leads_mau.csv`: `python3 -m unittest discover -s casa-ops/skills/bao-cao-tuan/tests -v`.
- Bộ kiểm tra hành vi của skill nằm ở `casa-ops/evals/` (xem README ở đó).

## Việc còn lại (chờ khảo sát)

- Báo cáo gửi cho ai và qua kênh nào (tin nhắn, Google Doc, email), có tách theo cơ sở không.
- Cách chạy lúc 8h sáng thứ Hai: tác vụ hẹn giờ trong Cowork hoặc Claude Code, nằm trong tài khoản của ai.
- Khi có Nhật ký chăm sóc (mục 3 file dữ liệu lead), thêm: lead theo sale, tỷ lệ chốt theo sale, lead bị bỏ quên, lead "Rất quan tâm" chưa chốt, lý do từ chối, chất lượng lead theo nguồn và chiến dịch, phễu Lead mới → Nhập học.
