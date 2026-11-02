# Thiết kế ứng dụng chăm sóc lead (AppSheet)

Dựa trên "Mô tả yêu cầu phần mềm quản lý và chăm sóc lead phụ huynh" của trường và khảo sát ngày 02/11/2026. Trường dùng Google Workspace có sẵn **AppSheet Core**, nên app làm bằng AppSheet, không tốn thêm phí.

## 1. Mục tiêu và người dùng

- **Sale** (6 người, phần lớn là giáo viên hoặc quản lý kiêm nhiệm): mở app trên điện thoại thấy ngay hôm nay cần gọi ai; ghi kết quả mỗi lần chăm sóc **dưới 30 giây**, chủ yếu bằng bấm nút.
- **Chủ / quản lý**: tự động thấy mỗi sale giữ bao nhiêu lead, lead nào bị bỏ quên, tỷ lệ chốt, lý do từ chối, nguồn nào mang về lead tốt.
- Dữ liệu vẫn là **Google Sheet**; chủ mở file gốc xem hay xuất báo cáo như bây giờ.

## 2. Dữ liệu nằm ở đâu

Các tab của app được thêm vào **cùng file Google Sheet mà bot Messenger đang ghi** (file có tab `Leads` và `Chủ đề`), để một file có đủ mọi thứ.

- Tab **`Leads` của bot giữ nguyên**: app chỉ **đọc**, không sửa, không thêm cột. Script của bot ghi lại cả cột A đến P của một hàng mỗi lần có sự kiện, và dừng ghi nếu có người chiếm cột bot cần dùng sau này (`docs/google-sheet-leads.md` của repo bot, mục 5).
- App có 5 tab riêng, đặt tên khác hẳn tab của bot để khỏi nhầm:

| Tab | Mỗi hàng là | Ai ghi |
|---|---|---|
| `Hồ sơ lead` | Một phụ huynh đang được chăm sóc | Sale (thêm lead), chủ (phân lead, tạm dừng) |
| `Chăm sóc` | Một lần liên hệ | Sale, qua form |
| `Sale` | Một người dùng app | Chủ |
| `Danh mục` | Một lựa chọn trong danh sách (cơ sở, nguồn, lý do…) | Chủ |
| `Cấu hình` | Một con số trong quy tắc nhắc | Chủ |

**Lead từ Messenger** không tự sang app. Trong app có danh sách "Messenger chưa nhận" (phụ huynh đã để SĐT cho bot mà chưa có hồ sơ). Sale hoặc chủ bấm **"Nhận lead này"**, app tạo hàng mới trong `Hồ sơ lead` với tên, tuổi bé, SĐT, quảng cáo và Customer ID lấy từ tab của bot. Customer ID dùng để nối hai bên và tránh nhận trùng.

Lead từ nguồn khác (Zalo, giới thiệu, đến trực tiếp, sự kiện, website) thì sale bấm **"Thêm lead"** và nhập tay.

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
| Tạm dừng | Yes/No | Chỉ chủ đổi. Bật thì ngừng nhắc |

### `Chăm sóc`

| Cột | Kiểu AppSheet | Ghi chú |
|---|---|---|
| Mã | Text, **Key** | `UNIQUEID()`, ẩn |
| Mã lead | Ref → `Hồ sơ lead` | **Is a part of: bật**, để thêm lần chăm sóc ngay trong trang lead |
| Thời gian | DateTime | `NOW()`, tự ghi, sale không nhập |
| Sale | Ref → `Sale` | `USEREMAIL()`, tự ghi, sale không nhập |
| Phương thức | Enum, nút bấm | Gọi điện / Zalo / Messenger (Facebook) / SMS / Gặp trực tiếp tại trường |
| Tình trạng | Enum, nút bấm | Chưa liên lạc được / Đang cân nhắc / Yêu cầu gọi lại sau / Đã hẹn tham quan / học thử / Đã tham quan / học thử / Đã đặt cọc / Đã nhập học / Từ chối |
| Mức quan tâm | Enum, nút bấm | Rất quan tâm / Quan tâm bình thường / Hời hợt. Ẩn khi Từ chối hoặc Chưa liên lạc được |
| Phản hồi | Text | Ô gõ ngắn, vd "băn khoăn học phí, muốn hỏi thêm chồng" |
| Lý do từ chối | Enum | `Danh mục` loại "Lý do từ chối". Chỉ hiện và bắt buộc khi Từ chối |
| Ngày hẹn gọi lại | Date | Tùy chọn. Bắt buộc khi "Yêu cầu gọi lại sau" |
| Ngày hẹn tham quan | Date | Chỉ hiện và bắt buộc khi "Đã hẹn tham quan / học thử" |
| Lần thứ | Number | **App formula** (mục 4), ẩn trong form |
| Hạn liên hệ tiếp | Date | **App formula** (mục 4), ẩn trong form |

Form chỉ có **3 chỗ bắt buộc phải bấm**: Phương thức, Tình trạng, Mức quan tâm. Các ô khác hiện ra khi cần.

### `Sale`

| Cột | Kiểu | Ghi chú |
|---|---|---|
| Email | Email, **Key** | Email Google dùng đăng nhập app |
| Tên | Name | |
| Cơ sở | Enum | |
| Vai trò | Enum | Sale / Chủ. "Chủ" thấy thêm các màn hình tổng hợp và được phân lead |
| Đang làm | Yes/No | Người nghỉ thì tắt, không xoá (để giữ lịch sử) |

### `Danh mục` và `Cấu hình`

- `Danh mục`: cột **Loại** và **Giá trị**. Chủ thêm, bớt lựa chọn ngay trên Sheet, không cần sửa app.
- `Cấu hình`: cột **Khóa**, **Giá trị**, **Ý nghĩa**. Mặc định: L1 = 1, L2 = 3, L3 = 7 (ngày), Bỏ quên = 3 (ngày), Hạn đặt cọc = 7 (ngày). Đổi số ở đây là app nhắc theo số mới (file yêu cầu ghi "số ngày có thể chỉnh sửa").

## 4. Quy tắc nhắc

Mỗi lần sale lưu một lần chăm sóc, app tính **Hạn liên hệ tiếp** cho lần đó. Hạn của một lead là hạn của **lần chăm sóc mới nhất**. Lead chưa có lần chăm sóc nào thì hạn là **ngày nhận** (phải liên hệ ngay trong ngày).

Theo thứ tự ưu tiên:

1. **Từ chối** hoặc **Đã nhập học**: ngừng nhắc.
2. Sale có điền **Ngày hẹn gọi lại**: nhắc đúng ngày đó.
3. **Đã hẹn tham quan / học thử**: nhắc **xác nhận lịch trước 1 ngày**. Sau khi đã gọi xác nhận (ghi một lần chăm sóc nữa), nhắc **hỏi cảm nhận sau buổi tham quan 1 ngày**.
4. **Đã đặt cọc**: nhắc hoàn tất thủ tục nhập học sau 7 ngày (`Cấu hình` › Hạn đặt cọc).
5. Đã nhắc quá 3 lần mà chưa tiến triển: ngừng nhắc, **đề xuất chủ chuyển "Tạm dừng"**.
6. **Chưa liên lạc được**: nhắc gọi lại sau 1 ngày.
7. Còn lại (đang cân nhắc, đã tham quan…): **L1** sau 1 ngày, **L2** sau 3 ngày, **L3** sau 7 ngày.

**Lần thứ** đếm số lần chăm sóc kể từ lần **tiến triển** gần nhất (Đã hẹn tham quan, Đã tham quan, Đã đặt cọc). Lần tiến triển tính là lần 1. Ví dụ: gọi lần đầu → L1; gọi lại vẫn cân nhắc → L2; lần nữa → L3; lần nữa vẫn chưa chốt → đề xuất tạm dừng. Nếu giữa chừng phụ huynh đi tham quan thì đếm lại từ đầu.

**Mức khẩn** của lead: hạn trước hôm nay là **Quá hạn** (đỏ), hạn hôm nay là **Hôm nay** (cam), sau hôm nay là **Sắp tới**.

**Bỏ quên** (cho chủ): lead chưa kết thúc, không tạm dừng, và quá hạn hoặc quá 3 ngày không có cập nhật (`Cấu hình` › Bỏ quên).

`quy_tac_nhac.py` là bản Python của đúng các quy tắc này, có test. Sửa quy tắc thì sửa cả công thức AppSheet dưới đây lẫn file Python.

### Công thức AppSheet

Tên bảng có dấu cách vẫn dùng được trong công thức, vd `Chăm sóc[Mã]`. Nếu AppSheet báo lỗi tên, xem tên bảng đúng như hiện trong mục **Data**.

**`Chăm sóc` › Mốc gần nhất** (cột ảo, kiểu Ref → `Chăm sóc`):

```
ANY(ORDERBY(
  SELECT(Chăm sóc[Mã], AND(
    [Mã lead] = [_THISROW].[Mã lead],
    [Thời gian] < [_THISROW].[Thời gian],
    IN([Tình trạng], LIST("Đã hẹn tham quan / học thử", "Đã tham quan / học thử", "Đã đặt cọc"))
  )),
  [Thời gian], TRUE))
```

**`Chăm sóc` › Lần thứ** (App formula):

```
IF(
  IN([Tình trạng], LIST("Đã hẹn tham quan / học thử", "Đã tham quan / học thử", "Đã đặt cọc")),
  1,
  1 + COUNT(SELECT(Chăm sóc[Mã], AND(
    [Mã lead] = [_THISROW].[Mã lead],
    [Thời gian] < [_THISROW].[Thời gian],
    OR(ISBLANK([_THISROW].[Mốc gần nhất]), [Thời gian] >= [_THISROW].[Mốc gần nhất].[Thời gian])
  )))
)
```

**`Chăm sóc` › Hạn liên hệ tiếp** (App formula):

```
IFS(
  IN([Tình trạng], LIST("Từ chối", "Đã nhập học")), "",
  ISNOTBLANK([Ngày hẹn gọi lại]), [Ngày hẹn gọi lại],
  [Tình trạng] = "Đã hẹn tham quan / học thử",
    IF(DATE([Thời gian]) < [Ngày hẹn tham quan] - 1, [Ngày hẹn tham quan] - 1, [Ngày hẹn tham quan] + 1),
  [Tình trạng] = "Đã đặt cọc",
    DATE([Thời gian]) + LOOKUP("Hạn đặt cọc", "Cấu hình", "Khóa", "Giá trị"),
  [Lần thứ] > 3, "",
  [Tình trạng] = "Chưa liên lạc được", DATE([Thời gian]) + 1,
  TRUE, DATE([Thời gian]) + LOOKUP(CONCATENATE("L", [Lần thứ]), "Cấu hình", "Khóa", "Giá trị")
)
```

**`Hồ sơ lead`**, các cột ảo. `[Related Chăm sócs]` là danh sách lần chăm sóc AppSheet tự tạo khi `Chăm sóc` có cột Ref tới `Hồ sơ lead`; tên có thể hơi khác, xem trong mục **Columns**.

| Cột ảo | Kiểu | Công thức |
|---|---|---|
| Lần cuối | Ref → `Chăm sóc` | `ANY(ORDERBY([Related Chăm sócs], [Thời gian], TRUE))` |
| Tình trạng hiện tại | Text | `IF(ISBLANK([Lần cuối]), "Mới", [Lần cuối].[Tình trạng])` |
| Mức quan tâm hiện tại | Text | `[Lần cuối].[Mức quan tâm]` |
| Hạn liên hệ | Date | `IFS([Tạm dừng], "", ISBLANK([Lần cuối]), DATE([Ngày nhận]), TRUE, [Lần cuối].[Hạn liên hệ tiếp])` |
| Mức khẩn | Text | `IFS(ISBLANK([Hạn liên hệ]), "", [Hạn liên hệ] < TODAY(), "Quá hạn", [Hạn liên hệ] = TODAY(), "Hôm nay", TRUE, "Sắp tới")` |
| Ngày không cập nhật | Decimal | `HOUR(NOW() - IF(ISBLANK([Lần cuối]), [Ngày nhận], [Lần cuối].[Thời gian])) / 24` |
| Đã kết thúc | Yes/No | `IN([Tình trạng hiện tại], LIST("Từ chối", "Đã nhập học"))` |
| Bỏ quên | Yes/No | `AND(NOT([Tạm dừng]), NOT([Đã kết thúc]), OR([Mức khẩn] = "Quá hạn", [Ngày không cập nhật] > LOOKUP("Bỏ quên", "Cấu hình", "Khóa", "Giá trị")))` |
| Đề xuất tạm dừng | Yes/No | `AND(NOT([Tạm dừng]), NOT([Đã kết thúc]), ISNOTBLANK([Lần cuối]), ISBLANK([Hạn liên hệ]))` |

**`Sale`**, các cột ảo cho màn hình của chủ:

| Cột ảo | Công thức |
|---|---|
| Đang giữ | `COUNT(SELECT(Hồ sơ lead[Mã lead], AND([Sale phụ trách] = [_THISROW].[Email], NOT([Tạm dừng]), NOT([Đã kết thúc]))))` |
| Liên hệ hôm nay | `COUNT(SELECT(Chăm sóc[Mã], AND([Sale] = [_THISROW].[Email], DATE([Thời gian]) = TODAY())))` |
| Quá hạn | `COUNT(SELECT(Hồ sơ lead[Mã lead], AND([Sale phụ trách] = [_THISROW].[Email], [Mức khẩn] = "Quá hạn")))` |
| Tổng lead | `COUNT(SELECT(Hồ sơ lead[Mã lead], [Sale phụ trách] = [_THISROW].[Email]))` |
| Đã nhập học | `COUNT(SELECT(Hồ sơ lead[Mã lead], AND([Sale phụ trách] = [_THISROW].[Email], [Tình trạng hiện tại] = "Đã nhập học")))` |
| Tỷ lệ chốt | `IF([Tổng lead] = 0, 0, [Đã nhập học] / [Tổng lead])`, kiểu Percent |
| Số lần chăm sóc | `COUNT(SELECT(Chăm sóc[Mã], [Sale] = [_THISROW].[Email]))` |

**Ai là chủ** (dùng trong điều kiện hiện màn hình, quyền sửa):

```
LOOKUP(USEREMAIL(), "Sale", "Email", "Vai trò") = "Chủ"
```

## 5. Màn hình

### Sale

1. **Hôm nay cần liên hệ** (màn hình mở đầu): lead của tôi có Mức khẩn là Quá hạn hoặc Hôm nay, xếp theo Hạn liên hệ (cũ nhất trước). Quá hạn tô đỏ.
2. **Lead**: hai thẻ **Của tôi** và **Tất cả**, ô tìm theo tên bé, tên phụ huynh, SĐT. Mọi sale đều xem được mọi lead để tư vấn khi phụ huynh tự nhắn tới. Nhắc việc chỉ dành cho sale phụ trách.
3. **Chi tiết lead**: thông tin phụ huynh và bé; nút **Gọi**, **SMS**, **Mở Zalo**; lịch sử các lần chăm sóc; nút **Ghi nhận lần chăm sóc**.
4. **Form ghi nhận**: các lựa chọn ở mục 3, nút bấm thay vì gõ chữ.
5. **Thêm lead** và **Messenger chưa nhận** (nút "Nhận lead này").

### Chủ (chỉ hiện với Vai trò = Chủ)

- **Theo sale**: mỗi sale đang giữ bao nhiêu lead, đã liên hệ hôm nay bao nhiêu, quá hạn bao nhiêu, tỷ lệ chốt, số lần chăm sóc.
- **Bỏ quên**, **Rất quan tâm chưa chốt**, **Đề xuất tạm dừng**.
- **Phễu**: đếm lead theo Tình trạng hiện tại (Mới → … → Đã nhập học).
- **Biểu đồ**: lead theo nguồn, theo cơ sở; lý do từ chối; chất lượng lead theo nguồn.
- **Phân lead**: sửa Sale phụ trách ngay trong chi tiết lead.

Phân tích sâu hơn (chất lượng theo chiến dịch, hiệu quả từng nguồn từ lead đến nhập học, so sánh tuần) để cho báo cáo tuần của plugin `casa-ops`, vì biểu đồ AppSheet đơn giản.

## 6. Nhắc việc

- **Trong app**: màn hình mở đầu luôn là danh sách hôm nay, quá hạn tô đỏ.
- **Email 7h30 sáng** mỗi ngày (AppSheet Automation): gửi mỗi sale số lead cần liên hệ hôm nay và quá hạn, kèm tên phụ huynh. Không ghi SĐT trong email.
- **Zalo**: chưa làm. Gửi tin Zalo tự động phải qua Zalo OA và dịch vụ tin nhắn trả phí của Zalo; để sau khi app chạy ổn.

**Không nhắc trùng với bot.** Bot nhắc tư vấn viên trên Telegram khi có tin nhắn **mới** chưa ai trả lời và gửi bản tổng hợp lúc 9h. App nhắc **gọi lại** những phụ huynh đã nhận vào hồ sơ. Quy ước: sale bấm "Nhận lead này" trong app thì reply `/xong` vào thẻ của phụ huynh đó trên Telegram, để bot ghi "Đã liên hệ" và thôi nhắc.

## 7. Quyền

- Chỉ email có trong tab `Sale` (và **Đang làm** bật) đăng nhập được.
- Mọi người xem được mọi lead. Sửa lần chăm sóc: người ghi hoặc chủ. Đổi Sale phụ trách và Tạm dừng: chỉ chủ.
- Tab `Leads` của bot: chỉ đọc trong app.
- Sheet chứa dữ liệu cá nhân của phụ huynh và trẻ: chỉ chia sẻ cho người cần dùng.

## 8. Báo cáo tuần

Khi app chạy, plugin `casa-ops` (skill `bao-cao-tuan`) đọc thêm tab `Hồ sơ lead` và `Chăm sóc` để báo cáo: lead và tỷ lệ chốt theo sale, lead bị bỏ quên, lead "Rất quan tâm" chưa chốt, lý do từ chối, chất lượng lead theo nguồn và chiến dịch, phễu Lead mới → Nhập học. Hai bên dùng chung các cột ở mục 3, nên đổi tên cột thì phải sửa cả hai.

## 9. Triển khai

1. Dựng app trên **Sheet mẫu** (dữ liệu giả), theo [huong-dan-appsheet.md](huong-dan-appsheet.md).
2. Thử với 1 – 2 sale trong một tuần, sửa theo phản hồi.
3. Thêm 5 tab của app vào file Sheet thật của bot (sao chép tab từ Sheet mẫu, xoá dữ liệu giả), đổi nguồn dữ liệu của app sang file thật, điền email thật vào tab `Sale`.
4. Mở cho cả 6 sale.
