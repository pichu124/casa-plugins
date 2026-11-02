# Ứng dụng chăm sóc lead

App trên điện thoại cho 6 sale ghi kết quả chăm sóc phụ huynh và được nhắc gọi lại; chủ xem tổng hợp. Làm bằng **AppSheet** (có sẵn trong Google Workspace của trường, gói AppSheet Core), dữ liệu nằm trên Google Sheet.

| File | Nội dung |
|---|---|
| [thiet-ke.md](thiet-ke.md) | Dữ liệu (các tab, cột), quy tắc nhắc, công thức AppSheet, màn hình, quyền |
| [huong-dan-appsheet.md](huong-dan-appsheet.md) | Dựng app từng bước, kèm danh sách kiểm tra với dữ liệu mẫu |
| `quy_tac_nhac.py` | Quy tắc nhắc viết bằng Python (bản đối chiếu cho công thức AppSheet) và script tạo dữ liệu mẫu |
| `test_quy_tac_nhac.py` | Test quy tắc nhắc và dữ liệu mẫu |
| `mau/` | Dữ liệu mẫu (giả) cho từng tab, ngày gốc 02/11/2026 |

Sheet mẫu trên Google Drive (dữ liệu giả, cùng nội dung với `mau/`): "Casa – Chăm sóc lead (mẫu, dữ liệu giả)".

Chạy test: `python3 -m unittest discover -s cham-soc-lead -v`. Tạo lại dữ liệu mẫu theo ngày khác: `python3 cham-soc-lead/quy_tac_nhac.py --tao-mau <thư mục> --hom-nay YYYY-MM-DD`.

Không đưa dữ liệu thật của phụ huynh và trẻ vào thư mục này.
