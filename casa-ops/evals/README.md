# Bộ kiểm tra hành vi của casa-ops

Mỗi thư mục con là một tình huống: `prompt.md` là câu người dùng hỏi, `graders/` là các tiêu chí chấm. Mọi dữ liệu đều là dữ liệu giả.

| Tình huống | Kiểm tra |
|---|---|
| `bao-cao-tuan-du-lieu-mau` | Có file tab Leads giả: skill được gọi, số liệu đúng, "Muốn hẹn" không tính là đã hẹn, không lộ SĐT hay Customer ID |
| `bao-cao-tuan-khong-co-du-lieu` | Không có dữ liệu: skill xin link Sheet hoặc file, không bịa số |
| `bao-cao-tuan-khong-kich-hoat` | Yêu cầu soạn tin nhắn: skill báo cáo không bị gọi nhầm |
| `chu-de-noi-dung-du-lieu-mau` | Có file tab Chủ đề giả: xếp hạng đúng, gợi ý nội dung đúng giọng văn, không đăng mức học phí, không dùng từ sale, không lộ SĐT |
| `chu-de-noi-dung-khong-co-du-lieu` | Không có dữ liệu: skill xin link Sheet hoặc file, không bịa xếp hạng |
| `chu-de-noi-dung-khong-kich-hoat` | Hỏi báo cáo lead tuần: skill chủ đề không bị gọi nhầm |

## Chạy

Từ thư mục `casa-ops/`:

```bash
claude plugin eval . --scaffold --allow-tools "Bash(python3 *)" Write
```

Chỉ chạy một skill: thêm `--tag bao-cao-tuan` hoặc `--tag chu-de-noi-dung`.

- `--scaffold` để tạo file dữ liệu giả (`leads.csv`, `chu_de.csv`) cho các tình huống có dữ liệu mẫu (script `tao-du-lieu.sh`).
- `--allow-tools` cho phép Claude ghi file và chạy script Python của skill, trong sandbox của lần chạy.
- Mặc định mỗi tình huống chạy 3 lần, có thêm một lượt chạy không cài plugin để so sánh. Muốn chạy nhanh để thử: thêm `--runs 1 --ablation none`.
- Mỗi lần chạy tốn lượt dùng của tài khoản Claude đang đăng nhập.
- Kết quả nằm ở `evals/results/` (đã cho vào `.gitignore`).

Các script tính toán có test riêng, không tốn lượt dùng:

```bash
python3 -m unittest discover -s casa-ops/skills/bao-cao-tuan/tests -v
python3 -m unittest discover -s casa-ops/skills/chu-de-noi-dung/tests -v
```
