# Dữ liệu lead

Plugin chỉ **đọc** dữ liệu. Ghi vào Sheet là việc của bot Messenger và (sau này) ứng dụng chăm sóc lead. Skill không sửa, xoá hay thêm hàng, trừ khi người dùng yêu cầu rõ.

## 1. Sheet lead của bot Messenger (đang chạy)

Bot ghi vào một Google Sheet của trường (vd "Casa – Lead Messenger"). Cấu trúc gốc nằm ở `docs/google-sheet-leads.md` trong repo `casa_preschool-messenger-bot`. Repo bot thay đổi cấu trúc thì cập nhật file này theo.

Mọi giờ là giờ Việt Nam, dạng `YYYY-MM-DD HH:MM:SS`.

### Tab `Leads`: mỗi phụ huynh (Customer ID) một hàng, cập nhật theo sự kiện mới nhất

| Cột | Ý nghĩa, cách dùng |
|---|---|
| Thời gian | Lúc có sự kiện mới nhất |
| Sự kiện | Sự kiện mới nhất: `SĐT mới`, `Đổi SĐT`, `Muốn hẹn tham quan/học thử`, `Chốt lịch hẹn`, `Xoá lịch hẹn`, `Đã liên hệ`, `Không quan tâm`, `Cập nhật thông tin` (hàng cũ có thể còn chữ `Hẹn tham quan/học thử`) |
| Tên Facebook | Tên phụ huynh. Không rõ thì là `khách chưa rõ tên` |
| Customer ID | PSID Messenger, dùng làm khóa. Không in ra báo cáo |
| SĐT | SĐT/Zalo. Báo cáo chỉ in 4 số cuối |
| Tên bé, Tuổi bé | Chữ tự do do AI trích từ lời phụ huynh (vd `2 tuổi`, `18 tháng`, `dưới 2 tuổi`) |
| Cơ sở/hệ | Chữ tự do: cơ sở hoặc hệ phụ huynh quan tâm |
| Khu vực | Khu vực, địa chỉ phụ huynh nói |
| Dự kiến nhập học | Chữ tự do |
| Hẹn tham quan/học thử | Lịch hẹn: AI hiểu (chưa chốt) hoặc tư vấn viên đã chốt |
| Quảng cáo | Tên quảng cáo phụ huynh bấm vào. **Có chữ = lead từ quảng cáo** |
| Giai đoạn | Xem bảng dưới |
| Tin cuối của phụ huynh | Không trích nguyên văn vào báo cáo nếu có thông tin cá nhân |
| Lần đầu liên hệ | Lúc có lead đầu tiên, không đổi. **Dùng cột này để xác định lead mới trong kỳ** |
| Cập nhật lúc | Lần cập nhật gần nhất |

Giá trị cột **Giai đoạn**:

| Giai đoạn | Nghĩa |
|---|---|
| `Mới` | Mới nhắn, chưa có gì |
| `Đã biết tuổi/cơ sở` | Đã biết tuổi bé hoặc cơ sở |
| `Đã có SĐT` | Đã để lại SĐT/Zalo |
| `Muốn hẹn tham quan/học thử` | AI hiểu phụ huynh muốn hẹn, **chưa chốt** |
| `Đã hẹn tham quan/học thử` | Tư vấn viên đã chốt lịch bằng `/hen` |
| `… · Đã liên hệ` | Hậu tố: tư vấn viên đã gõ `/xong`, vd `Đã có SĐT · Đã liên hệ` |
| `Không quan tâm` | Phụ huynh nói rõ không còn nhu cầu |

Khi đếm theo giai đoạn, bỏ hậu tố ` · Đã liên hệ` để ra giai đoạn chính, rồi đếm riêng số lead đã liên hệ.

### Tab `Chủ đề`: mỗi tin phụ huynh có chủ đề là một dòng (chỉ thêm, không sửa)

| Cột | Ý nghĩa |
|---|---|
| Thời gian | Lúc bot ghi |
| Customer ID | Nối với tab Leads khi cần |
| Quảng cáo | Tên quảng cáo (nếu có) |
| Cơ sở/hệ, Tuổi bé | Hồ sơ sau tin đó |
| Chủ đề | Một hay nhiều chủ đề, nối bằng `, ` |
| Chuyển tư vấn viên | `Có` / `Không`. **`Có` = câu bot không tự trả lời được** |
| Câu hỏi | Tin phụ huynh, SĐT đã thay bằng `[SĐT]`, tối đa 300 ký tự |

Danh sách chủ đề cố định (`app/topics.py` của bot): Học phí, Ưu đãi, Chương trình/phương pháp, Tiếng Anh/GV nước ngoài, Giáo viên/tỷ lệ cô trò, Cơ sở vật chất, Ăn uống/thực đơn, An toàn/sức khoẻ/camera, Giờ học/đón trả/trông muộn, Xe đưa đón, Độ tuổi/nhập học/hồ sơ, Học thử/tham quan, Thích nghi/tâm lý bé, So sánh trường khác, Khác.

### Chuẩn hóa khi tổng hợp

- **Cơ sở**: đưa về `Chùa Láng` / `Mỹ Đình` / `Kim Mã` / `Chưa rõ`. "Hongkong", "HK", "Huỳnh Thúc Kháng" là Chùa Láng. "FLC", "Phạm Hùng" là Mỹ Đình. "Vạn Phúc", "Ngọc Hà", "song ngữ" là Kim Mã. Chỉ ghi "quốc tế" mà không rõ cơ sở thì xếp vào `Quốc tế – chưa rõ cơ sở`. Nhắc nhiều cơ sở cùng lúc thì là `Chưa rõ`.
- **Nhóm tuổi**: `15 tháng – <2 tuổi`, `2 – <3 tuổi`, `3 – <5 tuổi`, `5 – 6 tuổi`, `Ngoài độ tuổi`, `Chưa rõ`. Nhóm này bám theo mốc 3 tuổi (bắt đầu học Cambridge) và mốc 5 tuổi (mức học phí khác).
  - Đổi chữ phụ huynh viết ra khoảng tuổi có thể (theo tháng), rồi lấy **điểm giữa**. Ví dụ "2 tuổi" là 24 – 36 tháng, điểm giữa 30 tháng; "1 tuổi" có điểm giữa 18 tháng nên vào nhóm 15 tháng – <2 tuổi; "dưới 2 tuổi" coi là 12 – 24 tháng.
  - Hiểu được: "18 tháng", "2t", "hai tuổi", "1 tuổi rưỡi", "2 tuổi 8 tháng", "3-4 tuổi", "dưới 2 tuổi", "sinh năm 2022", "sinh tháng 3/2023". Có năm sinh thì tính đến ngày chạy báo cáo.
  - Điểm giữa dưới 15 tháng hoặc từ 84 tháng (7 tuổi) trở lên là `Ngoài độ tuổi`. "6 tuổi" vẫn thuộc nhóm 5 – 6 tuổi, vì trường nhận bé tới 6 tuổi.
- Chữ không chắc chắn thì xếp `Chưa rõ`, không đoán.

## 2. Phân việc với bot (không làm trùng)

Bot đã tự nhắc tư vấn viên trên Telegram: thẻ lead chưa trả lời và bản tổng hợp lúc 9h hằng ngày. Plugin **không** gửi nhắc việc, không nhắn Telegram, không nhắn phụ huynh. Plugin chỉ làm báo cáo và phân tích cho chủ/quản lý, cùng bản nháp để người duyệt.

## 3. Hệ thống chăm sóc lead (đang lên kế hoạch)

Trường đang mô tả yêu cầu cho một ứng dụng giúp sale ghi kết quả chăm sóc và giúp chủ xem tổng hợp. Dữ liệu gốc vẫn nằm trên Google Sheet. Khi ứng dụng chạy, Sheet sẽ có thêm các dữ liệu sau và skill báo cáo mở rộng theo. Tên cột thật chốt khi ứng dụng xong.

**Thông tin lead (thêm so với bot):** Nguồn khách hàng (Facebook, Zalo, giới thiệu, đến trực tiếp, sự kiện), Chiến dịch / nội dung quảng cáo, Sale phụ trách, Ngày nhận lead, Ghi chú điều phụ huynh quan tâm.

**Nhật ký chăm sóc (mỗi lần liên hệ một bản ghi):**
- Phương thức: Gọi điện / Zalo / Messenger / SMS / Gặp trực tiếp.
- Tình trạng: Chưa liên lạc được / Đang cân nhắc / Yêu cầu gọi lại sau / Đã hẹn tham quan, học thử / Đã tham quan, học thử / Đã đặt cọc / Đã nhập học / Từ chối.
- Mức độ quan tâm: Rất quan tâm / Quan tâm bình thường / Hời hợt.
- Lý do từ chối: Học phí / Xa nhà / Chọn trường khác / Chưa có nhu cầu / Khác.
- Phản hồi của phụ huynh, ngày hẹn liên hệ lại. Thời gian và tên sale được ghi tự động.

**Chất lượng lead** (sale đánh giá sau lần tư vấn đầu): Tốt / Trung bình / Kém. Lead trung bình hoặc kém có thêm lý do: Sai độ tuổi / Ở quá xa / Sai hoặc thiếu SĐT / Chỉ để lại thông tin xem thử / Học phí vượt khả năng / Trùng lead / Khác.

**Quy tắc nhắc** (ứng dụng làm, plugin không làm): nhắc đúng ngày hẹn; không hẹn thì nhắc L1 sau 1 ngày, L2 sau 3 ngày, L3 sau 7 ngày, sau L3 chuyển `Tạm dừng`.

**Phễu chủ cần xem:** Lead mới → Đã tư vấn → Đã tham quan → Đặt cọc → Nhập học.

Khi có dữ liệu này, báo cáo tuần thêm: số lead và tỷ lệ chốt theo sale, lead bị bỏ quên (quá hạn nhắc hoặc quá 3 ngày chưa cập nhật), lead "Rất quan tâm" chưa chốt, lý do từ chối phổ biến, chất lượng lead theo nguồn và chiến dịch.
