---
name: chu-de-noi-dung
description: Tổng hợp các chủ đề phụ huynh hỏi nhiều nhất trên Messenger (tab Chủ đề của Sheet bot) rồi gợi ý bài đăng và quảng cáo cho Casa dei Bambini, theo đúng USP và giọng văn của trường. Dùng khi người dùng hỏi "phụ huynh hay hỏi gì", "dạo này phụ huynh quan tâm gì", "tháng này nên đăng gì", "gợi ý nội dung / quảng cáo", "quảng cáo nào kéo câu hỏi gì", "chủ đề nào đang tăng".
argument-hint: "[khoảng thời gian, cơ sở, nhóm tuổi hoặc quảng cáo cần xem]"
---

# /chu-de-noi-dung

Đọc trước: [bối cảnh Casa](../../references/boi-canh-casa.md) (mục 4 về USP và khó khăn, mục 5 về giọng văn), [dữ liệu lead](../../references/du-lieu-lead.md) (tab Chủ đề), [connector](../../CONNECTORS.md).

Phần đếm và xếp hạng do script `scripts/chu_de.py` làm, để lần nào chạy cũng ra cùng kết quả. Claude chỉ đọc kết quả, rút ra nhận xét và soạn gợi ý nội dung.

## Bước 1. Xác định phạm vi

- Mặc định: **30 ngày gần nhất**, tính đến hết hôm qua (giờ Việt Nam). Kỳ so sánh là 30 ngày liền trước đó.
- Người dùng nêu tháng hay khoảng ngày thì dùng `--tu` và `--den` (tính cả hai ngày). "Tháng 10" là `--tu 2026-10-01 --den 2026-10-31`.
- Lọc khi được yêu cầu: `--co-so "Mỹ Đình"`, `--nhom-tuoi "3 – <5 tuổi"`, `--quang-cao "Cambridge"` (tên chứa chữ này).

## Bước 2. Lấy dữ liệu tab Chủ đề

Theo thứ tự ưu tiên:

1. **Connector `~~spreadsheet`** (Google Sheets): đọc toàn bộ tab `Chủ đề`, cả hàng tiêu đề, ghi ra file CSV UTF-8 trong thư mục tạm.
2. **File người dùng tải lên**: `.csv` hoặc `.xlsx` (script tự tìm tab `Chủ đề`).
3. Không có cả hai: hỏi link Sheet hoặc file. **Không tự bịa xếp hạng hay số liệu.** Có thể kể danh sách chủ đề bot đang theo dõi, nhưng không gán số.

Cần lấy cả kỳ trước để so sánh, nên đọc mọi dòng, đừng lọc trước.

## Bước 3. Chạy script

```bash
python3 scripts/chu_de.py <file> --now "<giờ Việt Nam hiện tại, YYYY-MM-DD HH:MM>" [--tu ...] [--den ...] [--co-so ...] [--format json]
```

Script trả về:
- xếp hạng chủ đề theo **số phụ huynh khác nhau** (một phụ huynh hỏi nhiều lần chỉ tính một), kèm lượt hỏi, % phụ huynh, so với kỳ trước;
- số lượt **phải chuyển tư vấn viên** của từng chủ đề;
- top chủ đề theo cơ sở, theo nhóm tuổi, theo quảng cáo;
- câu hỏi mẫu mới nhất của từng chủ đề, đã thay SĐT và email bằng `[SĐT]`, `[email]`.

"Khác" luôn xếp cuối và không dùng để gợi ý nội dung.

## Bước 4. Rút nhận xét

Viết 3 – 5 nhận xét ngắn, mỗi nhận xét dựa trên một con số của script. Nên để ý:

- **Chủ đề tăng mạnh** so với kỳ trước, và chủ đề kỳ trước có mà kỳ này không còn ai hỏi.
- **Chủ đề hay phải chuyển tư vấn viên**: nội dung hiện có (bài đăng, câu trả lời của bot) chưa trả lời đủ, nên làm nội dung giải thích.
- **Quảng cáo kéo câu hỏi gì**: quảng cáo nói về Cambridge mà phụ huynh lại hỏi học phí là tín hiệu nên đổi thông điệp hoặc trả lời trước điều phụ huynh lo trong chính quảng cáo.
- **Khác biệt theo cơ sở và độ tuổi**: nhóm dưới 3 tuổi thường lo thích nghi, giờ đón; nhóm 3 – 6 tuổi quan tâm chương trình, tiếng Anh.
- Số liệu ít (vài phụ huynh) thì nói rõ là tín hiệu sớm, chưa đủ kết luận.

## Bước 5. Gợi ý nội dung

Với **3 – 5 chủ đề đứng đầu** (trừ "Khác"), mỗi chủ đề:

- **Phụ huynh thật sự lo gì**: một câu, dựa trên câu hỏi mẫu.
- **1 – 2 ý bài đăng**: định dạng (bài viết, ảnh nhiều tấm, video ngắn, livestream hỏi đáp), thông điệp chính, điểm mạnh của Casa liên quan, gợi ý hình ảnh, lời mời cuối bài.
- **1 ý quảng cáo**: nhắm cơ sở và độ tuổi nào (theo số liệu bước 3), câu mở đầu, nội dung chính, lời mời.
- Viết thử câu mở đầu hoặc đoạn ngắn **theo đúng giọng văn của Casa** (bối cảnh mục 5): xưng "em" hoặc "Casa", gọi "Ba/Mẹ", nhẹ nhàng, không dùng từ sale.

### Gợi ý theo chủ đề

| Chủ đề | Hướng nội dung | Điểm của Casa có thể dùng | Lưu ý |
|---|---|---|---|
| Học phí | Giải thích Ba/Mẹ nhận được gì với mức đầu tư | Cambridge Early Years có bản quyền; giáo viên nước ngoài toàn thời gian (hệ quốc tế); cam kết không tăng học phí đến khi bé ra trường; thu theo quý, 6 tháng hoặc 12 tháng | **Không đăng bảng học phí hay con số cụ thể.** Mời để lại SĐT/Zalo để tư vấn theo độ tuổi |
| Ưu đãi | Mời tham quan, tư vấn | – | Không nêu % giảm khi chưa có thông tin đợt hiện hành. Tránh "nhanh tay", "số lượng có hạn" |
| Chương trình/phương pháp | Một ngày của bé; Cambridge kết hợp Montessori | Đủ 3 môn Cambridge, 6 lĩnh vực cho bé 3 – 6 tuổi; giáo cụ Montessori; lộ trình 15 tháng – 6 tuổi | Bé dưới 3 tuổi chưa học Cambridge: nói theo cách "chuẩn bị nền tảng" |
| Tiếng Anh/GV nước ngoài | Bé dùng tiếng Anh tự nhiên trong ngày | Hệ quốc tế: 1 giáo viên nước ngoài/lớp toàn thời gian | Hệ song ngữ (Kim Mã) là giáo viên nước ngoài luân phiên, khoảng 2 – 2,5 giờ/lớp/ngày: **không viết "toàn thời gian" cho Kim Mã** |
| Giáo viên/tỷ lệ cô trò | Giới thiệu đội ngũ | Giáo viên gắn bó lâu năm, có chuyên môn | Tỷ lệ cô trò cụ thể: [CẦN TRƯỜNG XÁC NHẬN] |
| Cơ sở vật chất | Ảnh, video thật của lớp học và không gian | Chùa Láng, Mỹ Đình nằm trong tòa nhà, đưa đón thuận tiện | Dùng ảnh thật của đúng cơ sở. Không phóng đại về cơ sở Kim Mã |
| Ăn uống/thực đơn | Bữa ăn ở trường; hoạt động Nấu ăn | Ngoại khóa Nấu ăn | Thực đơn cụ thể: [CẦN TRƯỜNG XÁC NHẬN] |
| An toàn/sức khoẻ/camera | Trường giữ an toàn cho bé thế nào | CAIP (kỹ năng phòng tránh tai nạn); hai cơ sở trong tòa nhà | Camera cho phụ huynh xem: [CẦN TRƯỜNG XÁC NHẬN] |
| Giờ học/đón trả/trông muộn | Giờ học, đón trả, gói trông sớm/muộn | Gói trông sớm, trông muộn theo tháng | Đón sau 17h30 có phí riêng |
| Xe đưa đón | – | – | Có xe hay không: [CẦN TRƯỜNG XÁC NHẬN] |
| Độ tuổi/nhập học/hồ sơ | Lộ trình theo tuổi, thủ tục nhập học | Nhận bé từ 15 tháng (đã đi vững) đến 6 tuổi | – |
| Học thử/tham quan | Mời tham quan, kể một buổi tham quan | – | Lời mời nhẹ nhàng: "nếu Ba/Mẹ thuận tiện" |
| Thích nghi/tâm lý bé | Những ngày đầu đi học; cô đồng hành cùng bé | Dưới 3 tuổi ưu tiên chăm sóc và thích nghi; tôn trọng nhịp riêng của từng bé | Không hứa "bé hết khóc sau X ngày" |
| So sánh trường khác | Casa khác ở điểm nào | 3 USP: Cambridge đầy đủ, giáo viên nước ngoài, nền tảng 10 năm Montessori | **Không chê, không nêu tên trường khác** |

Thêm: Casa Talk Show, Casa Tranh Tài, sinh hoạt House và các ngoại khóa (Khoa học, Robotic, Gym…) là chất liệu tốt cho video ngắn, ghép được với nhiều chủ đề.

## Ranh giới

- Không đưa **điểm yếu nội bộ** (bối cảnh mục 4: học phí bị cho là cao, cơ sở Kim Mã cũ, dân số khu vực già) vào câu chữ gửi phụ huynh. Có thể nhắc trong phần nhận xét nội bộ.
- Không trích câu hỏi mẫu ra nội dung công khai khi chưa bỏ hết tên bé, địa chỉ và chi tiết riêng. Script chỉ lọc được SĐT và email.
- Không in Customer ID. Chỉ soạn bản nháp: không tự đăng bài, không chạy quảng cáo.
- Muốn soạn bài hoàn chỉnh thì có thể dùng thêm plugin `marketing`, nhưng phải giữ bối cảnh và giọng văn của Casa.

## Kiểm tra

- Test của script, chạy bằng dữ liệu giả `tests/chu_de_mau.csv`: `python3 -m unittest discover -s casa-ops/skills/chu-de-noi-dung/tests -v`.
- Bộ kiểm tra hành vi của skill nằm ở `casa-ops/evals/` (xem README ở đó).

## Việc còn lại (chờ khảo sát)

- Kênh đăng (Facebook, Zalo OA, TikTok…), số bài mỗi tuần và mẫu lịch nội dung.
- Nối với số liệu quảng cáo (chi phí, lượt hiển thị, chi phí mỗi lead) nếu trường có connector Facebook Ads.
- Ai duyệt nội dung trước khi đăng.
