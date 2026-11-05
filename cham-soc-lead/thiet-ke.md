# Thiết kế ứng dụng chăm sóc lead (AppSheet)

Dựa trên "Mô tả yêu cầu phần mềm quản lý và chăm sóc lead phụ huynh" của trường, khảo sát ngày 02/11/2026, và phản hồi của trường về quy tắc follow-up (11/2026, quy tắc nhắc v2). Trường dùng Google Workspace có sẵn **AppSheet Core**, nên app làm bằng AppSheet, không tốn thêm phí.

## 1. Mục tiêu và người dùng

- **Sale** (6 người, phần lớn là giáo viên hoặc quản lý kiêm nhiệm): mở app trên điện thoại thấy ngay hôm nay cần gọi ai; ghi kết quả mỗi lần chăm sóc **dưới 30 giây**, chủ yếu bằng bấm nút.
- **Chủ / quản lý**: tự động thấy mỗi sale giữ bao nhiêu lead, lead nào bị bỏ quên, tỷ lệ chốt, lý do từ chối, nguồn nào mang về lead tốt.
- Dữ liệu vẫn là **Google Sheet**; chủ mở file gốc xem hay xuất báo cáo như bây giờ.

## 2. Dữ liệu nằm ở đâu

Các tab của app được thêm vào **cùng file Google Sheet mà bot Messenger đang ghi** (file có tab `Leads` và `Chủ đề`), để một file có đủ mọi thứ.

- Tab **`Leads` của bot giữ nguyên**: app chỉ **đọc**, không sửa, không thêm cột. Script của bot ghi lại cả cột A đến P của một hàng mỗi lần có sự kiện, và dừng ghi nếu có người chiếm cột bot cần dùng sau này (`docs/google-sheet-leads.md` của repo bot, mục 5).
- App có 9 tab riêng, đặt tên khác hẳn tab của bot để khỏi nhầm:

| Tab | Mỗi hàng là | Ai ghi |
|---|---|---|
| `Hồ sơ lead` | Một phụ huynh đang được chăm sóc | Sale (thêm lead), chủ (phân lead, tạm dừng) |
| `Chăm sóc` | Một lần liên hệ | Sale, qua form |
| `Sale` | Một người dùng app | Chủ |
| `Danh mục` | Một lựa chọn trong danh sách (cơ sở, nguồn, lý do…) | Chủ |
| `Cấu hình` | Một con số trong quy tắc nhắc | Chủ |
| `Ngày nghỉ` | Một ngày lễ (thứ 7, Chủ nhật tự nghỉ, không cần ghi) | Chủ |
| `Gửi thông tin` | Một lần chủ gửi ưu đãi học phí hoặc thông tin hoạt động cho phụ huynh | App, khi chủ bấm "Đã gửi" |
| `Thống kê` | Một tháng của một cơ sở (hoặc "Tất cả"): phễu và tỷ lệ chuyển đổi | Công thức trong Sheet, tự tính |
| `Tổng hợp lead` | Mọi lead đang có, lọc theo cơ sở, sale, tình trạng, mức khẩn, kèm quá trình tư vấn | Công thức trong Sheet, cho chủ xem trên máy tính |

**Lead từ Messenger** không tự sang app. Trong app có danh sách "Messenger chưa nhận" (phụ huynh đã để SĐT cho bot mà chưa có hồ sơ), **chỉ chủ thấy**. Chủ bấm **"Giao lead"**: app mở form thêm lead đã điền sẵn tên, tuổi bé, SĐT, quảng cáo và Customer ID lấy từ tab của bot; chủ chọn **Sale phụ trách** rồi lưu. Customer ID dùng để nối hai bên và tránh nhận trùng.

Lead từ nguồn khác (Zalo, gọi hotline, tự tìm hiểu, giới thiệu, đến trực tiếp, sự kiện, website) thì sale bấm **"Thêm lead"** và nhập tay, chọn đúng **Nguồn**. Các lead này nằm chung tab `Hồ sơ lead` với lead từ Messenger, nên được nhắc việc và được tính vào `Thống kê` như nhau.

**Nhập tay ở đâu cho đúng:**
- Cách nên dùng: nút **Thêm lead** trong app. App tự điền Mã lead, Ngày nhận, Sale phụ trách và chỉ cho chọn giá trị có trong danh sách.
- Gõ thẳng vào tab `Hồ sơ lead` trên máy tính cũng được, miễn là: thêm ở **hàng trống cuối bảng** (không chèn giữa, không thêm hay đổi thứ tự cột); **Mã lead** không trùng (vd `T` + ngày giờ: `T2611021530`); **Ngày nhận** dạng ngày giờ; **Sale phụ trách** là email có trong tab `Sale`; **Cơ sở**, **Nguồn** chọn đúng chữ trong tab `Danh mục`.
- **Không bao giờ gõ vào tab `Leads` của bot.** Tab đó chỉ dành cho lead Messenger do bot ghi; thêm tay vào đó thì báo cáo tuần đếm nhầm thành lead Messenger, và app hiểu nhầm là lead chưa nhận.
- Muốn có thêm nguồn (vd "TikTok", "Tờ rơi"): thêm một hàng loại "Nguồn" ở tab `Danh mục`, app tự có lựa chọn mới.

## 3. Các cột

Tên cột là tên tiêu đề trên Sheet. Kiểu là kiểu cần chọn trong AppSheet.

### `Hồ sơ lead`

| Cột | Kiểu AppSheet | Ghi chú |
|---|---|---|
| Mã lead | Text, **Key** | Giá trị đầu `UNIQUEID()`, ẩn |
| Ngày nhận | DateTime | Giá trị đầu `NOW()`, không cho sửa |
| Tên phụ huynh | Name | Bắt buộc |
| Tên bé | Name | |
| Tuổi bé | Text | Ghi như phụ huynh nói, vd "18 tháng", "3 tuổi" |
| SĐT | Phone | Bắt buộc. AppSheet tự có nút gọi và nhắn SMS |
| Cơ sở | Enum | Danh sách lấy từ `Danh mục` loại "Cơ sở" |
| Nguồn | Enum | `Danh mục` loại "Nguồn" |
| Chiến dịch | Text | Tên quảng cáo hoặc chiến dịch. Lead từ Messenger lấy từ cột Quảng cáo của bot |
| PH quan tâm | EnumList | `Danh mục` loại "Mối quan tâm": học phí, chương trình, giờ học, đưa đón… |
| Sale phụ trách | Ref → `Sale` | Giá trị đầu `USEREMAIL()`. Chỉ chủ đổi được (phân lead) |
| Customer ID | Text | ID Messenger, chỉ có ở lead từ bot. Ẩn với sale |
| Chất lượng lead | Enum | Tốt / Trung bình / Kém. Sale chọn sau lần tư vấn đầu |
| Lý do chất lượng | Enum | `Danh mục` loại "Lý do chất lượng". Chỉ hiện khi Trung bình hoặc Kém |
| Ghi chú | LongText | |
| Tạm dừng | Yes/No | Chỉ chủ đổi. Bật thì lead chuyển giai đoạn **Dừng**, ngừng nhắc. Giá trị đầu `FALSE`, không bắt buộc |
| Chủ nhắc lúc | DateTime | Nút **Nhắc sale** của chủ ghi giờ vào đây; app gửi email nhắc sale phụ trách (mục 6). Sale thấy dòng "Chủ đã nhắc lúc…" trong chi tiết lead |
| Ngày sinh bé | Date | Sale điền khi phụ huynh cho ngày cụ thể. Trống thì app ước tính từ Tuổi bé (mục 4) |
| Em nhỏ | Enum | Có em nhỏ / Sắp sinh em / Không. Trống là chưa hỏi. Sale điền khi app nhắc hỏi em nhỏ |
| Ngày sinh em | Date | Ngày sinh hoặc dự sinh của em. Chỉ hiện và bắt buộc khi Có em nhỏ / Sắp sinh em. Nút **Tạo lead cho em** chép sang Ngày sinh bé của lead em |

3 cột cuối (đợt 2) nằm ở cột R – T trên Sheet, sau các cột mà tab `Tổng hợp lead` đọc (A – Q).

### `Chăm sóc`

| Cột | Kiểu AppSheet | Ghi chú |
|---|---|---|
| Mã | Text, **Key** | `UNIQUEID()`, ẩn |
| Mã lead | Ref → `Hồ sơ lead` | **Is a part of: bật**, để thêm lần chăm sóc ngay trong trang lead |
| Thời gian | DateTime | `NOW()`, tự ghi, sale không nhập |
| Sale | Ref → `Sale` | `USEREMAIL()`, tự ghi, sale không nhập |
| Phương thức | Enum, nút bấm | Gọi điện / Zalo / Messenger (Facebook) / SMS / Gặp trực tiếp tại trường |
| Tình trạng | Enum, nút bấm | Chưa liên lạc được / Đang cân nhắc / Yêu cầu gọi lại sau / Đã hẹn tham quan / học thử / Hẹn nhưng không đến / Đã tham quan / học thử / Đã đặt cọc / Đã nhập học / Từ chối |
| Mức quan tâm | Enum, nút bấm | Rất quan tâm / Quan tâm bình thường / Hời hợt. Ẩn khi Từ chối, Chưa liên lạc được, Hẹn nhưng không đến |
| Phản hồi | Text | Ô gõ ngắn, vd "băn khoăn học phí, muốn hỏi thêm chồng" |
| Lý do từ chối | Enum | `Danh mục` loại "Lý do từ chối": Học phí / Chọn trường khác / Chưa có nhu cầu / Xa nhà / Sai độ tuổi / Sai số điện thoại / Khác. Chỉ hiện và bắt buộc khi Từ chối |
| Ngày hẹn gọi lại | Date | Chỉ hiện và bắt buộc khi Hẹn lại sau = "Chọn ngày". Giá trị đầu **để trống** |
| Ngày hẹn tham quan | Date | Chỉ hiện và bắt buộc khi "Đã hẹn tham quan / học thử" |
| Lần thứ | Number | **App formula** (mục 4), ẩn trong form |
| Hạn liên hệ tiếp | Date | **App formula** (mục 4), ẩn trong form |
| PH chủ động | Yes/No | "Phụ huynh chủ động liên hệ". Bật thì lần này là mốc, đếm L1/L2/L3 lại từ đầu. Giá trị đầu `FALSE` |
| Hẹn lại sau | Enum, nút bấm | 1 tuần / 2 tuần / 1 tháng / 3 tháng / Chọn ngày. Ẩn khi Từ chối, Đã nhập học, Đã đặt cọc, Hẹn nhưng không đến. Bắt buộc khi "Yêu cầu gọi lại sau" |
| Đã gửi thư mời | Yes/No | Chỉ hiện khi Đã đặt cọc. Bật thì lead "Đã chốt", thôi nhắc. Giá trị đầu `FALSE` |
| Ngày nhập học dự kiến | Date | Chỉ hiện khi Đã đặt cọc. Sale điền (thường có trong thư mời). Dùng cho nhắc sau nhập học (đợt 2) |

4 cột cuối nằm **sau** cột Hạn liên hệ tiếp (cột N – Q trên Sheet), để công thức tab `Thống kê` và `Tổng hợp lead` (dựa vào vị trí cột A – M) không phải sửa.

Form chỉ có **3 chỗ bắt buộc phải bấm**: Phương thức, Tình trạng, Mức quan tâm. Các ô khác hiện ra khi cần. Thứ tự trong form: Phương thức, PH chủ động, Tình trạng, Mức quan tâm, Phản hồi, Lý do từ chối, Hẹn lại sau, Ngày hẹn gọi lại, Ngày hẹn tham quan, Đã gửi thư mời, Ngày nhập học dự kiến.

### `Sale`

| Cột | Kiểu | Ghi chú |
|---|---|---|
| Email | Email, **Key** | Email Google dùng đăng nhập app |
| Tên | Name | |
| Cơ sở | Enum | |
| Vai trò | Enum | Sale / Chủ. "Chủ" thấy thêm các màn hình tổng hợp và được phân lead |
| Đang làm | Yes/No | Người nghỉ thì tắt, không xoá (để giữ lịch sử) |

### `Danh mục`, `Cấu hình`, `Ngày nghỉ`, `Gửi thông tin`

- `Danh mục`: cột **Loại** và **Giá trị**. Chủ thêm, bớt lựa chọn ngay trên Sheet, không cần sửa app.
- `Cấu hình`: cột **Khóa** (Text, Key), **Giá trị** (Number), **Ý nghĩa**. Đổi số ở đây là app nhắc theo số mới. Mặc định (số ngày, trừ khi ghi khác):

| Khóa | Mặc định | Dùng cho |
|---|---|---|
| L1, L2, L3 | 1, 3, 7 | Nhắc lần 1, 2, 3 khi phụ huynh không hẹn ngày |
| Chưa liên lạc tối đa | 3 (lần) | "Chưa liên lạc được" liên tiếp chừng này lần thì chuyển dài hạn |
| Sau tham quan | 1 | Hỏi cảm nhận sau buổi tham quan |
| Chốt sau tham quan | 3 | Nhắc chốt sau lần hỏi cảm nhận |
| Từ chối trường khác | 180 | Nhắc lại sau chừng này ngày, hoặc đầu năm học (mốc nào đến trước) |
| Từ chối trường khác tối thiểu | 30 | Nhưng không sớm hơn chừng này ngày sau khi từ chối |
| Đầu năm học tháng, Đầu năm học ngày | 7, 1 | Đầu năm học 01/07 |
| Từ chối chưa nhu cầu | 90 | |
| Từ chối khác | 90 | |
| Ưu đãi lần đầu | 60 | Nhóm băn khoăn học phí: gửi ưu đãi lần đầu sau chừng này ngày kể từ lần liên hệ cuối |
| Ưu đãi cách nhau | 60 | Hai lần gửi ưu đãi cách nhau ít nhất chừng này ngày (mọi lead) |
| Ưu đãi tối đa | 2 (lần) | Nhóm băn khoăn học phí |
| Ưu đãi lần 2 trong vòng | 180 | Nhóm băn khoăn học phí: quá chừng này ngày sau lần 1 mà chưa gửi lần 2 thì thôi |
| Thông tin dài hạn | 30 | Lead dài hạn: gửi thông tin hoạt động cách nhau chừng này ngày |
| Tuổi nhận học (tháng) | 15 (tháng) | Bé nhỏ hơn tuổi này thì chờ, nhắc khi bé sắp đủ tuổi |
| Nhắc trước tuổi nhận học | 30 | Nhắc trước ngày bé đủ tuổi nhận học chừng này ngày |
| Tuổi tối đa (tháng) | 72 (tháng) | Bé đủ tuổi này thì nhắc sale hỏi phụ huynh về em nhỏ |
| Sau nhập học | 90 | Chừng này ngày sau ngày bé vào học thì nhắc giới thiệu chương trình đại sứ |

  Giờ gửi email buổi sáng (8h) đặt trong AppSheet (Automation), không đặt được từ Sheet.
- `Ngày nghỉ`: cột **Ngày** (Date, Key), **Tên**. Chỉ ghi ngày lễ, nghỉ bù, nghỉ Tết của trường; thứ 7 và Chủ nhật app tự coi là ngày nghỉ. Sheet mẫu có sẵn các ngày lễ dương lịch 2027; Tết và Giỗ Tổ chủ điền theo thông báo của trường.
- `Gửi thông tin`: **Mã** (Key, `UNIQUEID()`), **Mã lead** (Ref → `Hồ sơ lead`), **Thời gian** (DateTime), **Loại** (Ưu đãi học phí / Thông tin hoạt động), **Người gửi** (Email), **Ghi chú**. App thêm một hàng khi chủ bấm **Đã gửi ưu đãi** hoặc **Đã gửi thông tin**. Không làm đổi lịch nhắc của sale; sale thấy các lần chủ đã gửi trong chi tiết lead.

### `Thống kê`

Tab này **chỉ có công thức** (ở hàng 2), tự sinh mỗi tháng × mỗi cơ sở một hàng, từ tháng có lead đầu tiên tới tháng hiện tại, tháng mới nhất trên cùng. Chủ mở Sheet xem được ngay; trong app là bảng chỉ đọc.

| Cột | Ý nghĩa |
|---|---|
| Tháng | `YYYY-MM` |
| Cơ sở | "Tất cả" hoặc tên cơ sở trong `Danh mục` |
| Mã | Tháng · Cơ sở, làm **Key** trong AppSheet |
| Lead mới | Số lead có **Ngày nhận** trong tháng |
| Đã tư vấn | Trong số đó, lead đã liên hệ được ít nhất một lần (có lần chăm sóc khác "Chưa liên lạc được") |
| Đã tham quan | Lead từng có tình trạng Đã tham quan, Đã đặt cọc hoặc Đã nhập học |
| Đã đặt cọc | Lead từng có tình trạng Đã đặt cọc hoặc Đã nhập học |
| Đã nhập học | Lead từng có tình trạng Đã nhập học |
| Tỷ lệ tư vấn / tham quan / đặt cọc / nhập học | Mỗi bước chia cho Lead mới |
| Lead mới tháng trước | Để so sánh |

**Tính theo tháng nhận lead**: lead về tháng 10 mà tháng 11 mới nhập học thì vẫn được tính vào tháng 10. Vì vậy số của tháng gần nhất còn tăng dần trong vài tuần sau, khi phụ huynh đi tham quan, đặt cọc. Cách tính này cho biết lead của tháng nào chuyển đổi tốt, và so được tháng với tháng.

Công thức nằm ở `mau/thong-ke-cong-thuc.md`. Hàm `thong_ke_thang` trong `quy_tac_nhac.py` tính đúng các con số này để đối chiếu.

### `Tổng hợp lead`

Tab cho chủ mở trên máy tính, **đặt đầu tiên** trong file. Hàng 1 có 4 ô chọn: **Cơ sở**, **Sale**, **Tình trạng**, **Mức khẩn** (mặc định "Tất cả"). Bên dưới là mọi lead khớp bộ lọc, lead mới nhận lên đầu, mỗi lead một hàng: mã, ngày nhận, phụ huynh, bé, cơ sở, nguồn, sale, tình trạng hiện tại, mức quan tâm, lần cuối, hạn liên hệ, mức khẩn, số lần chăm sóc, và **quá trình tư vấn** (mỗi lần một dòng: ngày · sale · phương thức · tình trạng · phản hồi). Bấm vào ô quá trình tư vấn để đọc hết.

Chỉ có công thức, không ai gõ vào tab này. Công thức và cách tính: `mau/tong-hop-lead-cong-thuc.md`.

## 4. Quy tắc nhắc

Mỗi lần sale lưu một lần chăm sóc, app tính **Hạn liên hệ tiếp** cho lần đó. Hạn của một lead là hạn của **lần chăm sóc mới nhất**. Lead chưa có lần chăm sóc nào thì hạn là **ngày nhận** (liên hệ ngay khi được giao).

**Ngày nghỉ.** Thứ 7, Chủ nhật và các ngày trong tab `Ngày nghỉ` không nhắc sale chủ động liên hệ (sale vẫn trả lời khi phụ huynh tự nhắn). Nhắc rơi vào ngày nghỉ thì **dời tới ngày làm việc kế tiếp**. Riêng nhắc **xác nhận lịch tham quan** là **ngày làm việc liền trước buổi tham quan** (tham quan thứ 2 thì xác nhận thứ 6), để không nhắc sau buổi tham quan; gọi xác nhận vào hoặc sau ngày đó thì chuyển sang nhắc hỏi cảm nhận. Số ngày trong quy tắc là ngày lịch, dời sau khi cộng.

Theo thứ tự ưu tiên (giá trị trong ngoặc là khoá ở `Cấu hình`). Ba dòng **0a – 0c** (đợt 2) tính ở mức **lead** (cột ảo của `Hồ sơ lead`), đứng trước mọi dòng khác, trừ Tạm dừng; các dòng 1 – 14 là hạn của từng lần chăm sóc.

| # | Tình huống | Hạn liên hệ tiếp | Giai đoạn |
|---|---|---|---|
| 0a | Bé đủ 6 tuổi (Tuổi tối đa) vào ngày cần nhắc (hoặc lead dài hạn, không còn hạn, tới ngày bé đủ 6 tuổi), hoặc lần cuối là Từ chối vì Sai độ tuổi. Không áp dụng khi đã chốt, hay từ chối vì Xa nhà / Sai số điện thoại | Ngày bé đủ 6 tuổi (hoặc ngày liên hệ cuối nếu muộn hơn; Sai độ tuổi: ngày từ chối): **hỏi phụ huynh có em nhỏ / sắp sinh em**. Sale điền ô Em nhỏ → không nhắc | Đang chăm sóc → Dừng khi đã điền Em nhỏ |
| 0b | Đã chốt (Đã nhập học, hoặc đặt cọc đã gửi thư mời) và có ngày vào học: Ngày nhập học dự kiến (muộn nhất, ghi lúc đặt cọc), không có thì ngày ghi Đã nhập học lần đầu | Ngày vào học + 90 ngày (Sau nhập học): **giới thiệu chương trình đại sứ phụ huynh**. Có lần chăm sóc vào hoặc sau ngày đó → không nhắc | Đã chốt |
| 0c | Bé chưa đủ 15 tháng (Tuổi nhận học) vào lần liên hệ cuối, lần đó là Đang cân nhắc không hẹn ngày, hoặc Từ chối vì Chưa có nhu cầu / Khác. Hoặc lead em nhỏ (Nguồn "Em nhỏ trong gia đình") chưa liên hệ | 30 ngày trước ngày bé đủ tuổi (Nhắc trước tuổi nhận học); liên hệ rồi mà vẫn chưa tới ngày đủ tuổi: đúng ngày đủ tuổi | Dài hạn |
| 1 | Đã nhập học | Không nhắc | Đã chốt |
| 2 | Từ chối vì Học phí | Không nhắc sale. Lead vào danh sách **Gửi ưu đãi** của chủ | Dài hạn |
| 3 | Từ chối vì Xa nhà, Sai độ tuổi, Sai số điện thoại | Không nhắc | Dừng |
| 4 | Từ chối vì Chọn trường khác | Sau 180 ngày hoặc đầu năm học (01/07), mốc nào đến trước, nhưng ít nhất 30 ngày | Dài hạn |
| 5 | Từ chối vì Chưa có nhu cầu / Khác | Sau 90 ngày | Dài hạn |
| 6 | Đã đặt cọc, chưa gửi thư mời | **Ngay trong ngày**: viết thư mời tuyển sinh | Đang chăm sóc |
| 6b | Đã đặt cọc, đã gửi thư mời | Không nhắc (thủ tục nhập học do văn phòng cơ sở lo) | Đã chốt |
| 7 | Hẹn nhưng không đến | Ngay trong ngày (hẹn lại) | Đang chăm sóc |
| 7b | Phụ huynh hẹn ngày (Hẹn lại sau) | Đúng ngày hẹn: +7, +14 ngày, +1, +3 tháng, hoặc ngày sale chọn | Đang chăm sóc |
| 8 | Đã hẹn tham quan / học thử | Ngày làm việc liền trước buổi tham quan (xác nhận lịch). Ghi nhận vào hoặc sau ngày đó (gọi xác nhận xong): sau buổi tham quan 1 ngày (Sau tham quan) | Đang chăm sóc |
| 10 | Chưa liên lạc được | Ngày làm việc kế tiếp. Lần thứ 3 liên tiếp (Chưa liên lạc tối đa): không nhắc | Đang chăm sóc / Dài hạn |
| 11 | Đã tham quan / học thử | Sau 1 ngày, hỏi cảm nhận (Sau tham quan) | Đang chăm sóc |
| 12 | Lần thứ > 3 | Không nhắc | Dài hạn |
| 13 | Lần thứ 2 ngay sau "Đã tham quan" (lần hỏi cảm nhận) | Sau 3 ngày, nhắc chốt (Chốt sau tham quan) | Đang chăm sóc |
| 14 | Còn lại (Đang cân nhắc, Yêu cầu gọi lại không hẹn ngày…) | L1 sau 1 ngày, L2 sau 3 ngày, L3 sau 7 ngày | Đang chăm sóc |

**Tuổi bé** (dòng 0a, 0c). Có Ngày sinh bé thì dùng. Không có thì ước tính từ chữ ở ô Tuổi bé, tại ngày nhận lead, lấy điểm giữa: "2 tuổi" là 30 tháng, "3-4 tuổi" 48, "dưới 2 tuổi" 18, "2 tuổi rưỡi" 30, "2 tuổi 8 tháng" 32, "1,5 tuổi" 18, "18 tháng" 18, "dưới 18 tháng" 15, số trần ≤ 7 là tuổi ("2t" 30), lớn hơn là tháng ("18th" 18); ngày sinh = ngày nhận − tháng × 30,44 ngày. "N tháng tuổi" là N tháng; "dưới N tháng" là N − 3, không dưới 0. Có năm sinh (số ≥ 1900 trong 3 số đầu): ngày/tháng/năm có "/" hoặc "-" ("02/12/2025") thì lấy đúng ngày; tháng/năm ("3/2023", "tháng 4 năm 2024") thì ngày 15 của tháng đó; có tuổi đứng trước năm ("8 tháng, sinh 2026", "2 tuổi 3 tháng, sinh 2024") thì dùng tuổi, chỉ đọc các số trước năm; chỉ có năm ("sinh năm 2022") thì giữa năm (01/07). Chữ không có số thì không đoán. Lệch vài tuần, trường đã đồng ý.

**Việc cần làm** (cột ảo của lead, hiện trên thẻ và trong email 8h): Hỏi phụ huynh có em nhỏ hoặc sắp sinh em / Giới thiệu chương trình đại sứ phụ huynh / Bé sắp đủ tuổi nhận học / Bé đủ tuổi nhận học / Liên hệ lần đầu / Viết thư mời tuyển sinh / Xác nhận lịch tham quan / Hỏi cảm nhận sau buổi tham quan / Hẹn lại lịch tham quan / Liên hệ lại sau khi từ chối / Gọi lại.

**Mốc và Lần thứ.** Mốc là lần chăm sóc có tình trạng Đã hẹn tham quan, Đã tham quan, Đã đặt cọc, Từ chối, hoặc lần có **PH chủ động** bật. Lần thứ đếm các lần chăm sóc kể từ mốc gần nhất, mốc tính là lần 1; lần **Chưa liên lạc được không được đếm**. Ví dụ: gọi không được, gọi không được, gọi được và phụ huynh cân nhắc → L1. Hết L3 vẫn chưa chốt → dài hạn. Phụ huynh tự liên hệ lại → sale bật PH chủ động khi ghi nhận → nhắc cũ bỏ, đếm lại từ L1. Sau một lần Từ chối, lần liên hệ lại tiếp theo là lần 2.

**Giai đoạn** của lead: Tạm dừng bật → Dừng; dòng 0a – 0c như bảng; chưa có lần chăm sóc nào → Đang chăm sóc; còn lại theo bảng trên (lần mới nhất có hạn → Đang chăm sóc, không hạn → Dài hạn).

**Mức khẩn** của lead: hạn trước hôm nay là **Quá hạn** (đỏ), hạn hôm nay là **Hôm nay** (cam), sau hôm nay là **Sắp tới**.

**Bỏ quên** (cho chủ): lead **Đang chăm sóc** mà **quá hạn**. Lead mới chưa liên hệ lần nào và quá hạn thì báo chủ trong email 8h.

**Danh sách chủ tự gửi** (app không nhắn phụ huynh; chủ gửi qua Zalo rồi bấm **Đã gửi**, chọn nhiều lead một lần được):

- **Gửi ưu đãi**: lead Đang chăm sóc hoặc Dài hạn, có SĐT, không ở tình trạng Đã đặt cọc.
  - **Nhóm băn khoăn học phí** (Từ chối vì Học phí, hoặc Lý do chất lượng "Học phí vượt khả năng", hoặc một ô Phản hồi có chữ "học phí"): lần 1 sau 60 ngày kể từ lần liên hệ cuối (Ưu đãi lần đầu); lần 2 cách lần 1 ít nhất 60 ngày (Ưu đãi cách nhau) và trong vòng 180 ngày (Ưu đãi lần 2 trong vòng); tối đa 2 lần (Ưu đãi tối đa). Hết lượt thì chỉ còn nhận thông tin hoạt động.
  - **Lead khác**: cách lần gửi ưu đãi trước ít nhất 60 ngày.
  - Chủ tự quyết ưu đãi tháng này có đáng gửi không; app không lưu nội dung hay giá trị ưu đãi.
- **Gửi thông tin** (sự kiện, hội thảo, video giới thiệu): lead Dài hạn, có SĐT, lần gửi thông tin trước cách ít nhất 30 ngày (Thông tin dài hạn). Lọc theo cơ sở.

`quy_tac_nhac.py` là bản Python của đúng các quy tắc này; `test_quy_tac_nhac.py` có một ca thử cho mỗi dòng quy tắc của trường. Sửa quy tắc thì sửa cả công thức AppSheet dưới đây lẫn file Python.

### Công thức AppSheet

Tên bảng có dấu cách vẫn dùng được trong công thức, vd `Chăm sóc[Mã]`. Mọi `LOOKUP` vào `Cấu hình` chỉ tra **chữ cố định** (`LOOKUP("L1", "Cấu hình", "Khóa", "Giá trị")`), không đặt tên cột vào trong `LOOKUP`. Dưới đây `CH("x")` là viết tắt của `LOOKUP("x", "Cấu hình", "Khóa", "Giá trị")`: khi dán vào AppSheet phải viết đầy đủ (bản dán sẵn ở `nang-cap-quy-tac-v2.md`).

AppSheet **không có `EDATE`**: cộng n tháng viết `MIN(LIST(EOMONTH(d, n - 1) + DAY(d), EOMONTH(d, n)))` (ngày không có như 31/02 thì lấy ngày cuối tháng, giống `cong_thang` trong Python). Cộng trừ ngày: `Date + số` ra Date; so sánh hai ngày bằng `TODAY() >= [Ngày] + n` (Date − Date ra Duration, không so trực tiếp với số được).

**`Chăm sóc`**, theo thứ tự (cột sau dùng cột trước):

| Cột | Loại | Kiểu | Công thức |
|---|---|---|---|
| Mốc gần nhất | ảo | Ref → `Chăm sóc` | `ANY(ORDERBY(SELECT(Chăm sóc[Mã], AND([Mã lead] = [_THISROW].[Mã lead], [Thời gian] < [_THISROW].[Thời gian], OR(IN([Tình trạng], LIST("Đã hẹn tham quan / học thử", "Đã tham quan / học thử", "Đã đặt cọc", "Từ chối")), [PH chủ động]))), [Thời gian], TRUE))` |
| Lần thứ | App formula | Number | `IF(OR(IN([Tình trạng], LIST("Đã hẹn tham quan / học thử", "Đã tham quan / học thử", "Đã đặt cọc", "Từ chối")), [PH chủ động]), 1, 1 + COUNT(SELECT(Chăm sóc[Mã], AND([Mã lead] = [_THISROW].[Mã lead], [Thời gian] < [_THISROW].[Thời gian], [Tình trạng] <> "Chưa liên lạc được", OR(ISBLANK([_THISROW].[Mốc gần nhất]), [Thời gian] >= [_THISROW].[Mốc gần nhất].[Thời gian])))))` |
| Liên lạc được trước | ảo | DateTime | `MAX(SELECT(Chăm sóc[Thời gian], AND([Mã lead] = [_THISROW].[Mã lead], [Thời gian] < [_THISROW].[Thời gian], [Tình trạng] <> "Chưa liên lạc được")))` |
| Chưa LL liên tiếp | ảo | Number | `IF([Tình trạng] <> "Chưa liên lạc được", 0, 1 + COUNT(SELECT(Chăm sóc[Mã], AND([Mã lead] = [_THISROW].[Mã lead], [Thời gian] < [_THISROW].[Thời gian], [Tình trạng] = "Chưa liên lạc được", OR(ISBLANK([_THISROW].[Liên lạc được trước]), [Thời gian] > [_THISROW].[Liên lạc được trước])))))` (đếm hàng **trước** rồi cộng 1 cho chính nó: lúc thêm mới qua form, hàng đang lưu chưa có trong bảng) |
| Ngày hẹn | ảo | Date | `IFS([Hẹn lại sau] = "1 tuần", DATE([Thời gian]) + 7, [Hẹn lại sau] = "2 tuần", DATE([Thời gian]) + 14, [Hẹn lại sau] = "1 tháng", MIN(LIST(EOMONTH(DATE([Thời gian]), 0) + DAY(DATE([Thời gian])), EOMONTH(DATE([Thời gian]), 1))), [Hẹn lại sau] = "3 tháng", MIN(LIST(EOMONTH(DATE([Thời gian]), 2) + DAY(DATE([Thời gian])), EOMONTH(DATE([Thời gian]), 3))), TRUE, [Ngày hẹn gọi lại])` |
| Đầu năm học tới | ảo | Date | xem dưới |
| Hạn thô | ảo | Date | xem dưới |
| Hạn liên hệ tiếp | App formula | Date | `IF(ISBLANK([Hạn thô]), "", WORKDAY([Hạn thô] - 1, 1, Ngày nghỉ[Ngày]))` |

`WORKDAY(ngày, n, danh sách ngày lễ)` bỏ qua thứ 7, Chủ nhật và ngày lễ. `WORKDAY(d - 1, 1, …)` ra chính `d` nếu `d` là ngày làm việc, không thì ngày làm việc kế tiếp. `WORKDAY(d, -1, …)` ra ngày làm việc liền trước `d` (dùng cho ngày xác nhận lịch tham quan).

**Đầu năm học tới** (ngày đầu năm học gần nhất sau ngày ghi nhận):

```
IF(
  EOMONTH(DATE([Thời gian]), CH("Đầu năm học tháng") - MONTH(DATE([Thời gian])) - 1) + CH("Đầu năm học ngày") > DATE([Thời gian]),
  EOMONTH(DATE([Thời gian]), CH("Đầu năm học tháng") - MONTH(DATE([Thời gian])) - 1) + CH("Đầu năm học ngày"),
  EOMONTH(DATE([Thời gian]), CH("Đầu năm học tháng") - MONTH(DATE([Thời gian])) + 11) + CH("Đầu năm học ngày")
)
```

**Hạn thô** (ngày nhắc trước khi dời qua ngày nghỉ; trống là không nhắc):

```
IFS(
  [Tình trạng] = "Đã nhập học", "",
  AND([Tình trạng] = "Từ chối", IN([Lý do từ chối], LIST("Học phí", "Xa nhà", "Sai độ tuổi", "Sai số điện thoại"))), "",
  AND([Tình trạng] = "Từ chối", [Lý do từ chối] = "Chọn trường khác"),
    MAX(LIST(
      MIN(LIST(DATE([Thời gian]) + CH("Từ chối trường khác"), [Đầu năm học tới])),
      DATE([Thời gian]) + CH("Từ chối trường khác tối thiểu"))),
  AND([Tình trạng] = "Từ chối", [Lý do từ chối] = "Chưa có nhu cầu"), DATE([Thời gian]) + CH("Từ chối chưa nhu cầu"),
  [Tình trạng] = "Từ chối", DATE([Thời gian]) + CH("Từ chối khác"),
  [Tình trạng] = "Đã đặt cọc", IF([Đã gửi thư mời], "", DATE([Thời gian])),
  [Tình trạng] = "Hẹn nhưng không đến", DATE([Thời gian]),
  ISNOTBLANK([Ngày hẹn]), [Ngày hẹn],
  AND([Tình trạng] = "Đã hẹn tham quan / học thử", ISNOTBLANK([Ngày hẹn tham quan])),
    IF(DATE([Thời gian]) < WORKDAY([Ngày hẹn tham quan], -1, Ngày nghỉ[Ngày]),
      WORKDAY([Ngày hẹn tham quan], -1, Ngày nghỉ[Ngày]),
      [Ngày hẹn tham quan] + CH("Sau tham quan")),
  [Tình trạng] = "Chưa liên lạc được",
    IF([Chưa LL liên tiếp] >= CH("Chưa liên lạc tối đa"), "", DATE([Thời gian]) + 1),
  [Tình trạng] = "Đã tham quan / học thử", DATE([Thời gian]) + CH("Sau tham quan"),
  [Lần thứ] > 3, "",
  AND([Lần thứ] = 2, [Mốc gần nhất].[Tình trạng] = "Đã tham quan / học thử"), DATE([Thời gian]) + CH("Chốt sau tham quan"),
  TRUE, DATE([Thời gian]) + SWITCH([Lần thứ], 1, CH("L1"), 2, CH("L2"), 3, CH("L3"), 1)
)
```

**`Hồ sơ lead`**, các cột ảo. `[Related Chăm sócs]` là danh sách lần chăm sóc AppSheet tự tạo khi `Chăm sóc` có cột Ref tới `Hồ sơ lead`; tên có thể hơi khác, xem trong mục **Columns**.

| Cột ảo | Kiểu | Công thức |
|---|---|---|
| Lần cuối | Ref → `Chăm sóc` | `ANY(ORDERBY([Related Chăm sócs], [Thời gian], TRUE))` |
| Tình trạng hiện tại | Text | `IF(ISBLANK([Lần cuối]), "Mới", [Lần cuối].[Tình trạng])` |
| Mức quan tâm hiện tại | Text | `[Lần cuối].[Mức quan tâm]` |
| Hạn liên hệ | Date | xem **Đợt 2** dưới |
| Giai đoạn | Text | xem **Đợt 2** dưới |
| Việc cần làm | Text | xem **Đợt 2** dưới |
| Mức khẩn | Text | `IFS(ISBLANK([Hạn liên hệ]), "", [Hạn liên hệ] < TODAY(), "Quá hạn", [Hạn liên hệ] = TODAY(), "Hôm nay", TRUE, "Sắp tới")` |
| Nhóm | Text | `IFS([Mức khẩn] = "Quá hạn", "1 · Quá hạn", [Mức khẩn] = "Hôm nay", "2 · Hôm nay", [Mức khẩn] = "Sắp tới", "3 · Sắp tới", TRUE, CONCATENATE("4 · ", [Giai đoạn]))` |
| Ngày không cập nhật | Decimal | `HOUR(NOW() - IF(ISBLANK([Lần cuối]), [Ngày nhận], [Lần cuối].[Thời gian])) / 24` |
| Đã kết thúc | Yes/No | `IN([Giai đoạn], LIST("Đã chốt", "Dừng"))` |
| Bỏ quên | Yes/No | `AND([Giai đoạn] = "Đang chăm sóc", [Mức khẩn] = "Quá hạn")` |
| Lead mới chưa liên hệ | Yes/No | `AND(ISBLANK([Lần cuối]), NOT([Tạm dừng]), [Mức khẩn] = "Quá hạn")` |
| Số ngày quá hạn | Number | `IF([Mức khẩn] = "Quá hạn", HOUR(TODAY() - [Hạn liên hệ]) / 24, 0)` |
| Lần cuối tóm tắt | Text | `IF(ISBLANK([Lần cuối]), "Chưa liên hệ lần nào", CONCATENATE(TEXT([Lần cuối].[Thời gian], "DD/MM"), " · ", [Lần cuối].[Tình trạng], IF(ISBLANK([Lần cuối].[Phản hồi]), "", CONCATENATE(" · ", [Lần cuối].[Phản hồi]))))` |
| Liên hệ cuối lúc | DateTime | `IF(ISBLANK([Lần cuối]), [Ngày nhận], [Lần cuối].[Thời gian])` |
| Băn khoăn học phí | Yes/No | `OR(AND([Lần cuối].[Tình trạng] = "Từ chối", [Lần cuối].[Lý do từ chối] = "Học phí"), [Lý do chất lượng] = "Học phí vượt khả năng", COUNT(SELECT(Chăm sóc[Mã], AND([Mã lead] = [_THISROW].[Mã lead], CONTAINS([Phản hồi], "học phí")))) > 0)` |
| Số lần gửi ưu đãi | Number | `COUNT(SELECT(Gửi thông tin[Mã], AND([Mã lead] = [_THISROW].[Mã lead], [Loại] = "Ưu đãi học phí")))` |
| Gửi ưu đãi cuối | DateTime | `MAX(SELECT(Gửi thông tin[Thời gian], AND([Mã lead] = [_THISROW].[Mã lead], [Loại] = "Ưu đãi học phí")))` |
| Gửi thông tin cuối | DateTime | `MAX(SELECT(Gửi thông tin[Thời gian], AND([Mã lead] = [_THISROW].[Mã lead], [Loại] = "Thông tin hoạt động")))` |
| Nên gửi ưu đãi | Yes/No | xem dưới |
| Nên gửi thông tin | Yes/No | `AND([Giai đoạn] = "Dài hạn", ISNOTBLANK([SĐT]), OR(ISBLANK([Gửi thông tin cuối]), TODAY() >= DATE([Gửi thông tin cuối]) + CH("Thông tin dài hạn")))` |

**Nên gửi ưu đãi**:

```
AND(
  IN([Giai đoạn], LIST("Đang chăm sóc", "Dài hạn")),
  ISNOTBLANK([SĐT]),
  [Tình trạng hiện tại] <> "Đã đặt cọc",
  IF([Băn khoăn học phí],
    IFS(
      [Số lần gửi ưu đãi] = 0, TODAY() >= DATE([Liên hệ cuối lúc]) + CH("Ưu đãi lần đầu"),
      [Số lần gửi ưu đãi] >= CH("Ưu đãi tối đa"), FALSE,
      TRUE, AND(
        TODAY() >= DATE([Gửi ưu đãi cuối]) + CH("Ưu đãi cách nhau"),
        TODAY() <= DATE([Gửi ưu đãi cuối]) + CH("Ưu đãi lần 2 trong vòng"))
    ),
    OR([Số lần gửi ưu đãi] = 0, TODAY() >= DATE([Gửi ưu đãi cuối]) + CH("Ưu đãi cách nhau"))
  )
)
```

**Đợt 2: tuổi bé, em nhỏ, sau nhập học** (cột ảo của `Hồ sơ lead`, ẩn trừ Ngày sinh dùng, Đủ tuổi nhận học, Việc cần làm; bản dán sẵn ở `nang-cap-quy-tac-dot-2.md`). `Hạn cơ bản` là Hạn liên hệ của đợt 1 bỏ phần Tạm dừng.

| Cột ảo | Kiểu | Công thức |
|---|---|---|
| Số tuổi | List (Item type Decimal) | `EXTRACTNUMBERS(SUBSTITUTE([Tuổi bé], ",", "."))` |
| Số 1 | Decimal | `IF(COUNT([Số tuổi]) >= 1, ABS(INDEX([Số tuổi], 1)), 0)` |
| Số 2 | Decimal | `IF(COUNT([Số tuổi]) >= 2, ABS(INDEX([Số tuổi], 2)), 0)` |
| Số 3 | Decimal | `IF(COUNT([Số tuổi]) >= 3, ABS(INDEX([Số tuổi], 3)), 0)` |
| Năm trong tuổi | Number | `IF(MAX(LIST([Số 1], [Số 2], [Số 3])) >= 1900, ROUND(MAX(LIST([Số 1], [Số 2], [Số 3]))), 0)` |
| Số đếm | Number | `IFS([Năm trong tuổi] = 0, COUNT([Số tuổi]), [Số 1] >= 1900, 0, [Số 2] >= 1900, 1, TRUE, 2)` |
| Đủ tuổi nhận học | Date | `IF(ISBLANK([Ngày sinh dùng]), "", MIN(LIST(EOMONTH([Ngày sinh dùng], CH("Tuổi nhận học (tháng)") - 1) + DAY([Ngày sinh dùng]), EOMONTH([Ngày sinh dùng], CH("Tuổi nhận học (tháng)")))))` |
| Hết tuổi | Date | `IF(ISBLANK([Ngày sinh dùng]), "", MIN(LIST(EOMONTH([Ngày sinh dùng], CH("Tuổi tối đa (tháng)") - 1) + DAY([Ngày sinh dùng]), EOMONTH([Ngày sinh dùng], CH("Tuổi tối đa (tháng)")))))` |
| Hạn cơ bản | Date | `IF(ISBLANK([Lần cuối]), WORKDAY(DATE([Ngày nhận]) - 1, 1, Ngày nghỉ[Ngày]), [Lần cuối].[Hạn liên hệ tiếp])` |
| Chốt rồi | Yes/No | `OR([Lần cuối].[Tình trạng] = "Đã nhập học", AND([Lần cuối].[Tình trạng] = "Đã đặt cọc", [Lần cuối].[Đã gửi thư mời]))` |
| Hạn chờ tuổi | Date | `IF(DATE([Liên hệ cuối lúc]) < [Đủ tuổi nhận học] - CH("Nhắc trước tuổi nhận học"), [Đủ tuổi nhận học] - CH("Nhắc trước tuổi nhận học"), [Đủ tuổi nhận học])` |
| Hạn đại sứ | Date | `IF(AND(ISNOTBLANK([Ngày vào học]), DATE([Liên hệ cuối lúc]) < [Ngày vào học] + CH("Sau nhập học")), [Ngày vào học] + CH("Sau nhập học"), "")` |

**Tháng tuổi lúc nhận** (Decimal):

```
IFS(
  [Số đếm] = 0, "",
  AND(OR(CONTAINS([Tuổi bé], "tuổi"), CONTAINS([Tuổi bé], "tuoi")), NOT(AND([Số đếm] = 1, OR(CONTAINS([Tuổi bé], "tháng"), CONTAINS([Tuổi bé], "thang"))))),
    IFS(
      AND([Số đếm] >= 2, OR(CONTAINS([Tuổi bé], "tháng"), CONTAINS([Tuổi bé], "thang"))), [Số 1] * 12 + [Số 2],
      OR(CONTAINS([Tuổi bé], "rưỡi"), CONTAINS([Tuổi bé], "ruoi")), [Số 1] * 12 + 6,
      [Số đếm] >= 2, ([Số 1] + [Số 2] + 1) * 6,
      OR(CONTAINS([Tuổi bé], "dưới"), CONTAINS([Tuổi bé], "duoi")), [Số 1] * 12 - 6,
      [Số 1] <> FLOOR([Số 1]), [Số 1] * 12,
      TRUE, [Số 1] * 12 + 6
    ),
  OR(CONTAINS([Tuổi bé], "tháng"), CONTAINS([Tuổi bé], "thang")), IF(OR(CONTAINS([Tuổi bé], "dưới"), CONTAINS([Tuổi bé], "duoi")), MAX(LIST(0.0, [Số 1] - 3)), [Số 1]),
  [Số 1] <= 7, [Số 1] * 12 + 6,
  TRUE, [Số 1]
)
```

**Ngày sinh dùng** (Date):

```
IFS(
  ISNOTBLANK([Ngày sinh bé]), [Ngày sinh bé],
  AND([Số 3] >= 1900, [Số 2] >= 1, [Số 2] <= 12, [Số 1] >= 1, [Số 1] <= 31, OR(CONTAINS([Tuổi bé], "/"), CONTAINS([Tuổi bé], "-"))),
    MIN(LIST(
      EOMONTH(DATE([Ngày nhận]), ([Năm trong tuổi] - YEAR([Ngày nhận])) * 12 - MONTH([Ngày nhận]) + ROUND([Số 2]) - 1) + ROUND([Số 1]),
      EOMONTH(DATE([Ngày nhận]), ([Năm trong tuổi] - YEAR([Ngày nhận])) * 12 - MONTH([Ngày nhận]) + ROUND([Số 2])))),
  AND([Số 2] >= 1900, [Số 1] >= 1, [Số 1] <= 12, OR(CONTAINS([Tuổi bé], "/"), CONTAINS([Tuổi bé], "-"), CONTAINS([Tuổi bé], CONCATENATE("tháng ", ROUND([Số 1]))), CONTAINS([Tuổi bé], CONCATENATE("thang ", ROUND([Số 1]))))),
    EOMONTH(DATE([Ngày nhận]), ([Năm trong tuổi] - YEAR([Ngày nhận])) * 12 - MONTH([Ngày nhận]) + ROUND([Số 1]) - 1) + 15,
  ISNOTBLANK([Tháng tuổi lúc nhận]), DATE([Ngày nhận]) - ROUND([Tháng tuổi lúc nhận] * 30.44),
  [Năm trong tuổi] > 0,
    EOMONTH(DATE([Ngày nhận]), ([Năm trong tuổi] - YEAR([Ngày nhận])) * 12 - MONTH([Ngày nhận]) + 6) + 1,
  TRUE, ""
)
```

**Mốc hỏi em** (Date):

```
IFS(
  [Chốt rồi], "",
  AND([Lần cuối].[Tình trạng] = "Từ chối", [Lần cuối].[Lý do từ chối] = "Sai độ tuổi"), DATE([Lần cuối].[Thời gian]),
  AND([Lần cuối].[Tình trạng] = "Từ chối", IN([Lần cuối].[Lý do từ chối], LIST("Xa nhà", "Sai số điện thoại"))), "",
  ISBLANK([Hết tuổi]), "",
  IF(ISBLANK([Hạn cơ bản]), TODAY() >= [Hết tuổi], [Hạn cơ bản] >= [Hết tuổi]),
    MAX(LIST([Hết tuổi], DATE([Liên hệ cuối lúc]))),
  TRUE, ""
)
```

**Chờ đủ tuổi** (Yes/No):

```
AND(
  ISNOTBLANK([Đủ tuổi nhận học]),
  NOT([Chốt rồi]),
  ISBLANK([Mốc hỏi em]),
  IF(ISBLANK([Lần cuối]),
    AND([Nguồn] = "Em nhỏ trong gia đình", DATE([Ngày nhận]) < [Đủ tuổi nhận học]),
    AND(
      DATE([Lần cuối].[Thời gian]) < [Đủ tuổi nhận học],
      OR(
        AND([Lần cuối].[Tình trạng] = "Đang cân nhắc", ISBLANK([Lần cuối].[Ngày hẹn])),
        AND([Lần cuối].[Tình trạng] = "Từ chối", IN([Lần cuối].[Lý do từ chối], LIST("Chưa có nhu cầu", "Khác")))
      )
    )
  )
)
```

**Ngày vào học** (Date):

```
IFS(
  NOT([Chốt rồi]), "",
  COUNT(SELECT(Chăm sóc[Mã], AND([Mã lead] = [_THISROW].[Mã lead], [Tình trạng] = "Đã đặt cọc", ISNOTBLANK([Ngày nhập học dự kiến])))) > 0,
    MAX(SELECT(Chăm sóc[Ngày nhập học dự kiến], AND([Mã lead] = [_THISROW].[Mã lead], [Tình trạng] = "Đã đặt cọc", ISNOTBLANK([Ngày nhập học dự kiến])))),
  COUNT(SELECT(Chăm sóc[Mã], AND([Mã lead] = [_THISROW].[Mã lead], [Tình trạng] = "Đã nhập học"))) > 0,
    DATE(MIN(SELECT(Chăm sóc[Thời gian], AND([Mã lead] = [_THISROW].[Mã lead], [Tình trạng] = "Đã nhập học")))),
  TRUE, ""
)
```

**Hạn liên hệ** (Date):

```
IFS(
  [Tạm dừng], "",
  ISNOTBLANK([Mốc hỏi em]), IF(ISBLANK([Em nhỏ]), WORKDAY([Mốc hỏi em] - 1, 1, Ngày nghỉ[Ngày]), ""),
  ISNOTBLANK([Hạn đại sứ]), WORKDAY([Hạn đại sứ] - 1, 1, Ngày nghỉ[Ngày]),
  [Chờ đủ tuổi], WORKDAY([Hạn chờ tuổi] - 1, 1, Ngày nghỉ[Ngày]),
  TRUE, [Hạn cơ bản]
)
```

**Giai đoạn** (Text):

```
IFS(
  [Tạm dừng], "Dừng",
  ISNOTBLANK([Mốc hỏi em]), IF(ISBLANK([Em nhỏ]), "Đang chăm sóc", "Dừng"),
  [Chốt rồi], "Đã chốt",
  [Chờ đủ tuổi], "Dài hạn",
  ISBLANK([Lần cuối]), "Đang chăm sóc",
  [Lần cuối].[Tình trạng] = "Đã đặt cọc", "Đang chăm sóc",
  [Lần cuối].[Tình trạng] = "Từ chối", IF(IN([Lần cuối].[Lý do từ chối], LIST("Xa nhà", "Sai độ tuổi", "Sai số điện thoại")), "Dừng", "Dài hạn"),
  ISNOTBLANK([Hạn cơ bản]), "Đang chăm sóc",
  TRUE, "Dài hạn"
)
```

**Việc cần làm** (Text):

```
IFS(
  ISBLANK([Hạn liên hệ]), "",
  ISNOTBLANK([Mốc hỏi em]), "Hỏi phụ huynh có em nhỏ hoặc sắp sinh em",
  ISNOTBLANK([Hạn đại sứ]), "Giới thiệu chương trình đại sứ phụ huynh",
  [Chờ đủ tuổi], IF([Hạn chờ tuổi] < [Đủ tuổi nhận học], "Bé sắp đủ tuổi nhận học", "Bé đủ tuổi nhận học"),
  ISBLANK([Lần cuối]), "Liên hệ lần đầu",
  [Lần cuối].[Tình trạng] = "Đã đặt cọc", "Viết thư mời tuyển sinh",
  AND([Lần cuối].[Tình trạng] = "Đã hẹn tham quan / học thử", ISNOTBLANK([Lần cuối].[Ngày hẹn tham quan]), [Hạn liên hệ] < [Lần cuối].[Ngày hẹn tham quan]), "Xác nhận lịch tham quan",
  IN([Lần cuối].[Tình trạng], LIST("Đã hẹn tham quan / học thử", "Đã tham quan / học thử")), "Hỏi cảm nhận sau buổi tham quan",
  [Lần cuối].[Tình trạng] = "Hẹn nhưng không đến", "Hẹn lại lịch tham quan",
  [Lần cuối].[Tình trạng] = "Từ chối", "Liên hệ lại sau khi từ chối",
  TRUE, "Gọi lại"
)
```

**`Sale`**, các cột ảo cho màn hình của chủ:

| Cột ảo | Công thức |
|---|---|
| Đang giữ | `COUNT(SELECT(Hồ sơ lead[Mã lead], AND([Sale phụ trách] = [_THISROW].[Email], [Giai đoạn] = "Đang chăm sóc")))` |
| Liên hệ hôm nay | `COUNT(SELECT(Chăm sóc[Mã], AND([Sale] = [_THISROW].[Email], DATE([Thời gian]) = TODAY())))` |
| Quá hạn | `COUNT(SELECT(Hồ sơ lead[Mã lead], AND([Sale phụ trách] = [_THISROW].[Email], [Mức khẩn] = "Quá hạn")))` |
| Tổng lead | `COUNT(SELECT(Hồ sơ lead[Mã lead], [Sale phụ trách] = [_THISROW].[Email]))` |
| Đã chốt | `COUNT(SELECT(Hồ sơ lead[Mã lead], AND([Sale phụ trách] = [_THISROW].[Email], [Giai đoạn] = "Đã chốt")))` |
| Tỷ lệ chốt | `IF([Tổng lead] = 0, 0, DECIMAL([Đã chốt]) / [Tổng lead])`, kiểu Percent. Phải có `DECIMAL`: AppSheet chia hai số nguyên thì làm tròn xuống (1/4 ra 0) |
| Số lần chăm sóc | `COUNT(SELECT(Chăm sóc[Mã], [Sale] = [_THISROW].[Email]))` |

**Ai là chủ** (dùng trong điều kiện hiện màn hình, quyền sửa):

```
LOOKUP(USEREMAIL(), "Sale", "Email", "Vai trò") = "Chủ"
```

## 5. Màn hình

### Sale

1. **Hôm nay cần liên hệ** (màn hình mở đầu): lead của tôi có Mức khẩn là Quá hạn hoặc Hôm nay, xếp theo Hạn liên hệ (cũ nhất trước). Quá hạn tô đỏ. Từ thứ 2 đến thứ 6; nhắc rơi vào thứ 7, Chủ nhật, ngày lễ đã được dời.
2. **Của tôi**: **chỉ lead mình phụ trách** (sale không thấy lead của người khác), có **ô tìm kiếm** (tên phụ huynh, tên bé, vài số cuối SĐT), nhóm theo Mức khẩn. Khi phụ huynh tự gọi hoặc nhắn tới, sale gõ tìm, mở ra là bấm **Ghi nhận lần chăm sóc**. Không thấy thì bấm **Thêm lead**: nếu SĐT đó đã có trong hệ thống (do sale khác phụ trách), app báo chủ để chủ quyết định giao cho ai (mục 6).
3. **Chi tiết lead**: thông tin phụ huynh và bé; nút **Gọi**, **SMS**, **Mở Zalo**; lịch sử các lần chăm sóc và các lần chủ đã gửi ưu đãi / thông tin; nút **Ghi nhận lần chăm sóc**; nút **Đã gửi thư mời** (chỉ hiện khi lần cuối là Đã đặt cọc mà chưa gửi thư mời); dòng **Việc cần làm**; ô **Gia đình có em nhỏ?** và nút **Tạo lead cho em** (mở form lead mới điền sẵn tên phụ huynh, SĐT, cơ sở, nguồn "Em nhỏ trong gia đình", ngày sinh em; hiện khi đã chọn Có em nhỏ / Sắp sinh em và chưa tạo lead em).
4. **Form ghi nhận**: các lựa chọn ở mục 3, nút bấm thay vì gõ chữ.
5. **Thêm lead** (lead tự tìm được: Zalo, hotline, đến trực tiếp…). Sale phụ trách tự điền là chính mình.

### Chủ (chỉ hiện với Vai trò = Chủ)

- **Báo cáo tháng**: hai nút chọn **Tháng** và **Cơ sở** (mặc định tháng hiện tại, Tất cả). Hiện phễu Lead mới → Đã tư vấn → Đã tham quan → Đặt cọc → Nhập học, mỗi bước kèm số, % so với lead mới, % so với bước trước, và số lead mới so với tháng trước. Bấm vào để xem danh sách lead của tháng đó. Chọn tháng cũ để nhìn lại.
- **Tất cả lead** (chỉ chủ): mọi lead của trường, có ô tìm kiếm, lọc **Cơ sở**, **Sale**. Bấm vào một lead là thấy chi tiết và **dòng thời gian các lần tư vấn** (mới nhất trên cùng: ngày, sale, phương thức, tình trạng, mức quan tâm, phản hồi), kèm nút Nhắc sale. Trên máy tính, tab `Tổng hợp lead` của Sheet cho cùng thông tin.
- **So sánh các tháng / các cơ sở**: bảng tab `Thống kê`, nhóm theo tháng, kèm biểu đồ lead mới theo tháng.
- **Theo sale**: mỗi sale đang giữ bao nhiêu lead, đã liên hệ hôm nay bao nhiêu, quá hạn bao nhiêu, tỷ lệ chốt, số lần chăm sóc.
- **Bỏ quên** và **Rất quan tâm chưa chốt**: danh sách chi tiết, **nhóm theo sale phụ trách** để chủ biết nhắc ai. Mỗi lead hiện tên phụ huynh, bé, cơ sở, sale phụ trách, số ngày quá hạn hoặc số ngày chưa cập nhật, và **lần cuối** (ngày · tình trạng · phản hồi). Nút **Nhắc sale** gửi email nhắc cho sale phụ trách và ghi lại thời điểm đã nhắc, để lần sau chủ biết mình đã nhắc chưa.
- **Gửi ưu đãi**: lead nên gửi ưu đãi học phí hôm nay (mục 4), nhóm băn khoăn học phí lên đầu, lọc theo cơ sở. Mỗi dòng: tên phụ huynh, bé, cơ sở, sale, số lần đã gửi, lần gửi cuối; nút **Zalo** và **Đã gửi ưu đãi**. Chọn nhiều dòng rồi bấm Đã gửi một lần được.
- **Gửi thông tin**: lead dài hạn nên gửi thông tin hoạt động (sự kiện, hội thảo, video), lọc theo cơ sở; nút **Zalo** và **Đã gửi thông tin**.
- **Biểu đồ**: lead theo nguồn, theo cơ sở; lý do từ chối; chất lượng lead theo nguồn.
- **Phân lead**: sửa Sale phụ trách ngay trong chi tiết lead.

Phân tích sâu hơn (chất lượng theo chiến dịch, hiệu quả từng nguồn từ lead đến nhập học, so sánh tuần) để cho báo cáo tuần của plugin `casa-ops`, vì biểu đồ AppSheet đơn giản.

## 6. Nhắc việc

- **Trong app**: màn hình mở đầu luôn là danh sách hôm nay, quá hạn tô đỏ.
- **Email 8h sáng, thứ 2 đến thứ 6** (AppSheet Automation): gửi mỗi sale số lead cần liên hệ hôm nay và quá hạn, kèm tên phụ huynh. Không ghi SĐT trong email.
- **Email 8h cho chủ, thứ 2 đến thứ 6**: lead mới chưa liên hệ đã quá hạn (kèm sale phụ trách), số lead bỏ quên, số lead trong danh sách Gửi ưu đãi và Gửi thông tin hôm nay.
- **Zalo**: chưa làm. Gửi tin Zalo tự động phải qua Zalo OA và dịch vụ tin nhắn trả phí của Zalo; để sau khi app chạy ổn.

- **Chủ nhắc sale**: chủ bấm **Nhắc sale** ở danh sách bỏ quên hoặc rất quan tâm chưa chốt → app gửi ngay email cho sale phụ trách: tên phụ huynh, bé, cơ sở, quá hạn bao lâu, lần cuối liên hệ, kèm link mở lead trong app. Không ghi SĐT trong email.

- **Lead trùng**: khi một lead mới được thêm (trừ lead em nhỏ tạo bằng nút **Tạo lead cho em**, cùng SĐT với anh/chị) mà SĐT đã có ở lead khác, app gửi email cho chủ (tên hai lead, hai sale phụ trách) để chủ gộp hoặc giao lại. Cần vì sale không thấy lead của nhau nên có thể thêm trùng.
- **Giao lead Messenger**: chủ thấy danh sách "Messenger chưa nhận" và giao cho sale. Sale được giao nhận email "Bạn được giao lead mới".

**Không nhắc trùng với bot.** Bot nhắc tư vấn viên trên Telegram khi có tin nhắn **mới** chưa ai trả lời và gửi bản tổng hợp lúc 9h (bot không đổi theo quy tắc v2, vẫn chạy cả thứ 7 vì thẻ của bot đến từ tin phụ huynh chủ động nhắn). App nhắc **gọi lại** những phụ huynh đã nhận vào hồ sơ. Quy ước: sau khi chủ giao lead Messenger trong app, người tư vấn reply `/xong` vào thẻ của phụ huynh đó trên Telegram, để bot ghi "Đã liên hệ" và thôi nhắc.

## 7. Quyền

- Chỉ email có trong tab `Sale` (và **Đang làm** bật) đăng nhập được.
- **Sale chỉ xem và sửa lead mình phụ trách** cùng các lần chăm sóc của lead đó. Làm bằng **security filter** của AppSheet: dữ liệu của người khác không được tải về điện thoại sale (không chỉ ẩn trên màn hình).
- **Chủ xem mọi lead**, phân lead (đổi Sale phụ trách), tạm dừng, giao lead Messenger, xem báo cáo. Sale không tải được tab `Leads` của bot và tab `Thống kê`.
- Khi chủ chuyển lead sang sale khác, lead (kèm lịch sử chăm sóc) biến mất khỏi app của sale cũ và hiện ở app của sale mới.
- Sửa lần chăm sóc: người ghi hoặc chủ.
- Tab `Leads` của bot: chỉ đọc trong app.
- Sheet chứa dữ liệu cá nhân của phụ huynh và trẻ: chỉ chia sẻ cho người cần dùng.

## 8. Báo cáo tuần

Khi app chạy, plugin `casa-ops` (skill `bao-cao-tuan`) đọc thêm tab `Hồ sơ lead` và `Chăm sóc` để báo cáo: lead và tỷ lệ chốt theo sale, lead bị bỏ quên, lead "Rất quan tâm" chưa chốt, lý do từ chối, chất lượng lead theo nguồn và chiến dịch, phễu Lead mới → Nhập học. Hai bên dùng chung các cột ở mục 3, nên đổi tên cột thì phải sửa cả hai.

## 9. Triển khai

1. Dựng app trên **Sheet mẫu** (dữ liệu giả), theo [huong-dan-appsheet.md](huong-dan-appsheet.md).
2. Thử với 1 – 2 sale trong một tuần, sửa theo phản hồi.
3. Thêm 9 tab của app vào file Sheet thật của bot (sao chép tab từ Sheet mẫu, xoá dữ liệu giả), đổi nguồn dữ liệu của app sang file thật, điền email thật vào tab `Sale`.
4. Mở cho cả 6 sale.
