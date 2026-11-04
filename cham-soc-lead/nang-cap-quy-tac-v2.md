# Nâng cấp app lên quy tắc nhắc v2

Dành cho app **đã dựng** theo `huong-dan-appsheet.md` (bản quy tắc 1/3/7 cũ). Quy tắc mới theo phản hồi của trường (11/2026) nằm ở `thiet-ke.md` mục 4; `quy_tac_nhac.py` là bản chuẩn có test. Đợt 1 gồm: chưa liên lạc được, hẹn ngày nhanh, PH chủ động, hẹn mà không đến, tham quan, đặt cọc và thư mời, từ chối theo lý do, dời qua thứ 7 / Chủ nhật / ngày lễ, danh sách chủ tự gửi ưu đãi và thông tin, email 8h.

Mọi công thức dưới đây đã viết đầy đủ để dán thẳng. Ô công thức nào cũng **gõ `=` trước** rồi dán (hoặc dán vào Expression Assistant). Làm đúng thứ tự: cột sau dùng cột trước.

Ước tính: 2 – 3 giờ. Sale đang dùng thử sẽ thấy thay đổi ngay khi bấm SAVE, nên làm ngoài giờ sale dùng.

## Bước 1. Sheet

Sheet mẫu gốc **"Casa – Chăm sóc lead (mẫu, dữ liệu giả)"** đã có sẵn dữ liệu v2. Trên bản sao của bạn:

1. Tab **`Chăm sóc`**: chọn toàn bộ (bấm ô góc trên trái), xoá. Sang Sheet mẫu gốc, tab `Chăm sóc`, chọn `A1:Q15`, Copy, quay lại bản sao, bấm `A1`, Paste. Tab giờ có 17 cột, thêm **PH chủ động, Hẹn lại sau, Đã gửi thư mời, Ngày nhập học dự kiến** ở cột N – Q.
2. Tab **`Cấu hình`** và **`Danh mục`**: làm y hệt (xoá hết, chép `A1:C18` và `A1:B37` từ Sheet mẫu gốc).
3. Hai tab mới: chuột phải tab **`Ngày nghỉ`** của Sheet mẫu gốc → **Sao chép vào** → chọn bản sao của bạn. Làm y hệt với tab **`Gửi thông tin`**. Đổi tên hai tab vừa chép, bỏ chữ "Bản sao của".
4. Dữ liệu mẫu dùng email `sale1@example.com`: chạy lại **Tìm và thay thế** như bước 0 của `huong-dan-appsheet.md` (đổi thành email của bạn, tất cả các trang tính, khớp toàn bộ nội dung ô).
5. Tab `Ngày nghỉ`: thêm các ngày nghỉ Tết, Giỗ Tổ, nghỉ bù của trường (cột A là ngày, cột B là tên). Thứ 7 và Chủ nhật không cần ghi.

Tab `Hồ sơ lead`, `Sale`, `Leads`, `Thống kê`, `Tổng hợp lead` giữ nguyên.

## Bước 2. Bảng mới và cột mới

**Data → +** (Add new data) → chọn bản sao → tick **Ngày nghỉ** (Read-Only) và **Gửi thông tin** (Updates, Adds) → Add.

- `Ngày nghỉ`: `Ngày` Type **Date**, tick **Key**; `Tên` Label. Bỏ Key ở `_RowNumber`.
- `Gửi thông tin`: `Mã` Key, Initial value `UNIQUEID()`, bỏ Show; `Mã lead` Type **Ref** → `Hồ sơ lead` (không tick Is a part of); `Thời gian` DateTime, Initial value `NOW()`; `Loại` **Enum**: `Ưu đãi học phí`, `Thông tin hoạt động`; `Người gửi` **Email**, Initial value `USEREMAIL()`; `Ghi chú` Text. Bỏ Key ở `_RowNumber`.

**Data → Chăm sóc** → nút ↻ (**Regenerate structure**) để AppSheet thấy 4 cột mới. Sau khi regenerate, kiểm tra lại: `Mã` vẫn là Key, `Mã lead` vẫn là Ref → Hồ sơ lead có Is a part of, `Tình trạng` vẫn là Label, Initial value của `Ngày hẹn gọi lại`, `Ngày hẹn tham quan` vẫn trống. Rồi chỉnh:

| Cột | Chỉnh |
|---|---|
| Tình trạng | Values thêm `Hẹn nhưng không đến` (đặt sau "Đã hẹn tham quan / học thử") |
| Mức quan tâm | Show? và Required?: `NOT(IN([Tình trạng], LIST("Từ chối", "Chưa liên lạc được", "Hẹn nhưng không đến")))` |
| PH chủ động | Type **Yes/No**; Initial value `FALSE`; Display name `Phụ huynh chủ động liên hệ` |
| Hẹn lại sau | Type **Enum**, Values `1 tuần`, `2 tuần`, `1 tháng`, `3 tháng`, `Chọn ngày`; Input mode **Buttons**; Show? `NOT(IN([Tình trạng], LIST("Từ chối", "Đã nhập học", "Đã đặt cọc", "Hẹn nhưng không đến")))`; Required? `[Tình trạng] = "Yêu cầu gọi lại sau"` |
| Ngày hẹn gọi lại | Show? và Required?: `[Hẹn lại sau] = "Chọn ngày"` |
| Đã gửi thư mời | Type **Yes/No**; Initial value `FALSE`; Show? `[Tình trạng] = "Đã đặt cọc"` |
| Ngày nhập học dự kiến | Type **Date**; Initial value trống; Show? `[Tình trạng] = "Đã đặt cọc"` |

## Bước 3. Công thức của `Chăm sóc`

Sửa cột có sẵn, thêm cột ảo mới (nút **+** → Add virtual column), đúng thứ tự:

**1. Mốc gần nhất** (ảo (sửa cột có sẵn), kiểu Ref → `Chăm sóc`)

```
ANY(ORDERBY(SELECT(Chăm sóc[Mã], AND([Mã lead] = [_THISROW].[Mã lead], [Thời gian] < [_THISROW].[Thời gian], OR(IN([Tình trạng], LIST("Đã hẹn tham quan / học thử", "Đã tham quan / học thử", "Đã đặt cọc", "Từ chối")), [PH chủ động]))), [Thời gian], TRUE))
```

**2. Lần thứ** (App formula (sửa cột có sẵn), kiểu Number)

```
IF(OR(IN([Tình trạng], LIST("Đã hẹn tham quan / học thử", "Đã tham quan / học thử", "Đã đặt cọc", "Từ chối")), [PH chủ động]), 1, 1 + COUNT(SELECT(Chăm sóc[Mã], AND([Mã lead] = [_THISROW].[Mã lead], [Thời gian] < [_THISROW].[Thời gian], [Tình trạng] <> "Chưa liên lạc được", OR(ISBLANK([_THISROW].[Mốc gần nhất]), [Thời gian] >= [_THISROW].[Mốc gần nhất].[Thời gian])))))
```

**3. Liên lạc được trước** (ảo, kiểu DateTime)

```
MAX(SELECT(Chăm sóc[Thời gian], AND([Mã lead] = [_THISROW].[Mã lead], [Thời gian] < [_THISROW].[Thời gian], [Tình trạng] <> "Chưa liên lạc được")))
```

**4. Chưa LL liên tiếp** (ảo, kiểu Number)

```
IF([Tình trạng] <> "Chưa liên lạc được", 0, 1 + COUNT(SELECT(Chăm sóc[Mã], AND([Mã lead] = [_THISROW].[Mã lead], [Thời gian] < [_THISROW].[Thời gian], [Tình trạng] = "Chưa liên lạc được", OR(ISBLANK([_THISROW].[Liên lạc được trước]), [Thời gian] > [_THISROW].[Liên lạc được trước])))))
```

(đếm hàng **trước** rồi cộng 1 cho chính nó: lúc thêm mới qua form, hàng đang lưu chưa có trong bảng)

**5. Ngày hẹn** (ảo, kiểu Date)

```
IFS([Hẹn lại sau] = "1 tuần", DATE([Thời gian]) + 7, [Hẹn lại sau] = "2 tuần", DATE([Thời gian]) + 14, [Hẹn lại sau] = "1 tháng", MIN(LIST(EOMONTH(DATE([Thời gian]), 0) + DAY(DATE([Thời gian])), EOMONTH(DATE([Thời gian]), 1))), [Hẹn lại sau] = "3 tháng", MIN(LIST(EOMONTH(DATE([Thời gian]), 2) + DAY(DATE([Thời gian])), EOMONTH(DATE([Thời gian]), 3))), TRUE, [Ngày hẹn gọi lại])
```

**6. Đầu năm học tới** (ảo, kiểu Date)

Công thức: xem dưới

**7. Hạn thô** (ảo, kiểu Date)

Công thức: xem dưới

**8. Hạn liên hệ tiếp** (App formula (sửa cột có sẵn), kiểu Date)

```
IF(ISBLANK([Hạn thô]), "", WORKDAY([Hạn thô] - 1, 1, Ngày nghỉ[Ngày]))
```


`WORKDAY(ngày, n, danh sách ngày lễ)` bỏ qua thứ 7, Chủ nhật và ngày lễ. `WORKDAY(d - 1, 1, …)` ra chính `d` nếu `d` là ngày làm việc, không thì ngày làm việc kế tiếp. `WORKDAY(d, -1, …)` ra ngày làm việc liền trước `d` (dùng cho ngày xác nhận lịch tham quan).

**Đầu năm học tới** (ngày đầu năm học gần nhất sau ngày ghi nhận):

```
IF(
  EOMONTH(DATE([Thời gian]), LOOKUP("Đầu năm học tháng", "Cấu hình", "Khóa", "Giá trị") - MONTH(DATE([Thời gian])) - 1) + LOOKUP("Đầu năm học ngày", "Cấu hình", "Khóa", "Giá trị") > DATE([Thời gian]),
  EOMONTH(DATE([Thời gian]), LOOKUP("Đầu năm học tháng", "Cấu hình", "Khóa", "Giá trị") - MONTH(DATE([Thời gian])) - 1) + LOOKUP("Đầu năm học ngày", "Cấu hình", "Khóa", "Giá trị"),
  EOMONTH(DATE([Thời gian]), LOOKUP("Đầu năm học tháng", "Cấu hình", "Khóa", "Giá trị") - MONTH(DATE([Thời gian])) + 11) + LOOKUP("Đầu năm học ngày", "Cấu hình", "Khóa", "Giá trị")
)
```

**Hạn thô** (ngày nhắc trước khi dời qua ngày nghỉ; trống là không nhắc):

```
IFS(
  [Tình trạng] = "Đã nhập học", "",
  AND([Tình trạng] = "Từ chối", IN([Lý do từ chối], LIST("Học phí", "Xa nhà", "Sai độ tuổi", "Sai số điện thoại"))), "",
  AND([Tình trạng] = "Từ chối", [Lý do từ chối] = "Chọn trường khác"),
    MAX(LIST(
      MIN(LIST(DATE([Thời gian]) + LOOKUP("Từ chối trường khác", "Cấu hình", "Khóa", "Giá trị"), [Đầu năm học tới])),
      DATE([Thời gian]) + LOOKUP("Từ chối trường khác tối thiểu", "Cấu hình", "Khóa", "Giá trị"))),
  AND([Tình trạng] = "Từ chối", [Lý do từ chối] = "Chưa có nhu cầu"), DATE([Thời gian]) + LOOKUP("Từ chối chưa nhu cầu", "Cấu hình", "Khóa", "Giá trị"),
  [Tình trạng] = "Từ chối", DATE([Thời gian]) + LOOKUP("Từ chối khác", "Cấu hình", "Khóa", "Giá trị"),
  [Tình trạng] = "Đã đặt cọc", IF([Đã gửi thư mời], "", DATE([Thời gian])),
  [Tình trạng] = "Hẹn nhưng không đến", DATE([Thời gian]),
  ISNOTBLANK([Ngày hẹn]), [Ngày hẹn],
  AND([Tình trạng] = "Đã hẹn tham quan / học thử", ISNOTBLANK([Ngày hẹn tham quan])),
    IF(DATE([Thời gian]) < WORKDAY([Ngày hẹn tham quan], -1, Ngày nghỉ[Ngày]),
      WORKDAY([Ngày hẹn tham quan], -1, Ngày nghỉ[Ngày]),
      [Ngày hẹn tham quan] + LOOKUP("Sau tham quan", "Cấu hình", "Khóa", "Giá trị")),
  [Tình trạng] = "Chưa liên lạc được",
    IF([Chưa LL liên tiếp] >= LOOKUP("Chưa liên lạc tối đa", "Cấu hình", "Khóa", "Giá trị"), "", DATE([Thời gian]) + 1),
  [Tình trạng] = "Đã tham quan / học thử", DATE([Thời gian]) + LOOKUP("Sau tham quan", "Cấu hình", "Khóa", "Giá trị"),
  [Lần thứ] > 3, "",
  AND([Lần thứ] = 2, [Mốc gần nhất].[Tình trạng] = "Đã tham quan / học thử"), DATE([Thời gian]) + LOOKUP("Chốt sau tham quan", "Cấu hình", "Khóa", "Giá trị"),
  TRUE, DATE([Thời gian]) + SWITCH([Lần thứ], 1, LOOKUP("L1", "Cấu hình", "Khóa", "Giá trị"), 2, LOOKUP("L2", "Cấu hình", "Khóa", "Giá trị"), 3, LOOKUP("L3", "Cấu hình", "Khóa", "Giá trị"), 1)
)
```

## Bước 4. Cột ảo của `Hồ sơ lead`

Sửa các cột đã có, thêm các cột mới, theo thứ tự trong bảng. Cột **Đề xuất tạm dừng** sẽ xoá ở bước 6, sau khi bỏ slice, view và quy tắc tô màu đang dùng nó.

**1. Lần cuối** (cột ảo, kiểu Ref → `Chăm sóc`)

```
ANY(ORDERBY([Related Chăm sócs], [Thời gian], TRUE))
```

**2. Tình trạng hiện tại** (cột ảo, kiểu Text)

```
IF(ISBLANK([Lần cuối]), "Mới", [Lần cuối].[Tình trạng])
```

**3. Mức quan tâm hiện tại** (cột ảo, kiểu Text)

```
[Lần cuối].[Mức quan tâm]
```

**4. Hạn liên hệ** (cột ảo, kiểu Date)

```
IFS([Tạm dừng], "", ISBLANK([Lần cuối]), WORKDAY(DATE([Ngày nhận]) - 1, 1, Ngày nghỉ[Ngày]), TRUE, [Lần cuối].[Hạn liên hệ tiếp])
```

**5. Giai đoạn** (cột ảo, kiểu Text)

```
IFS([Tạm dừng], "Dừng", ISBLANK([Lần cuối]), "Đang chăm sóc", OR([Lần cuối].[Tình trạng] = "Đã nhập học", AND([Lần cuối].[Tình trạng] = "Đã đặt cọc", [Lần cuối].[Đã gửi thư mời])), "Đã chốt", [Lần cuối].[Tình trạng] = "Từ chối", IF(IN([Lần cuối].[Lý do từ chối], LIST("Xa nhà", "Sai độ tuổi", "Sai số điện thoại")), "Dừng", "Dài hạn"), ISNOTBLANK([Hạn liên hệ]), "Đang chăm sóc", TRUE, "Dài hạn")
```

**6. Mức khẩn** (cột ảo, kiểu Text)

```
IFS(ISBLANK([Hạn liên hệ]), "", [Hạn liên hệ] < TODAY(), "Quá hạn", [Hạn liên hệ] = TODAY(), "Hôm nay", TRUE, "Sắp tới")
```

**7. Nhóm** (cột ảo, kiểu Text)

```
IFS([Mức khẩn] = "Quá hạn", "1 · Quá hạn", [Mức khẩn] = "Hôm nay", "2 · Hôm nay", [Mức khẩn] = "Sắp tới", "3 · Sắp tới", TRUE, CONCATENATE("4 · ", [Giai đoạn]))
```

**8. Ngày không cập nhật** (cột ảo, kiểu Decimal)

```
HOUR(NOW() - IF(ISBLANK([Lần cuối]), [Ngày nhận], [Lần cuối].[Thời gian])) / 24
```

**9. Đã kết thúc** (cột ảo, kiểu Yes/No)

```
IN([Giai đoạn], LIST("Đã chốt", "Dừng"))
```

**10. Bỏ quên** (cột ảo, kiểu Yes/No)

```
AND([Giai đoạn] = "Đang chăm sóc", [Mức khẩn] = "Quá hạn")
```

**11. Lead mới chưa liên hệ** (cột ảo, kiểu Yes/No)

```
AND(ISBLANK([Lần cuối]), NOT([Tạm dừng]), [Mức khẩn] = "Quá hạn")
```

**12. Số ngày quá hạn** (cột ảo, kiểu Number)

```
IF([Mức khẩn] = "Quá hạn", HOUR(TODAY() - [Hạn liên hệ]) / 24, 0)
```

**13. Lần cuối tóm tắt** (cột ảo, kiểu Text)

```
IF(ISBLANK([Lần cuối]), "Chưa liên hệ lần nào", CONCATENATE(TEXT([Lần cuối].[Thời gian], "DD/MM"), " · ", [Lần cuối].[Tình trạng], IF(ISBLANK([Lần cuối].[Phản hồi]), "", CONCATENATE(" · ", [Lần cuối].[Phản hồi]))))
```

**14. Liên hệ cuối lúc** (cột ảo, kiểu DateTime)

```
IF(ISBLANK([Lần cuối]), [Ngày nhận], [Lần cuối].[Thời gian])
```

**15. Băn khoăn học phí** (cột ảo, kiểu Yes/No)

```
OR(AND([Lần cuối].[Tình trạng] = "Từ chối", [Lần cuối].[Lý do từ chối] = "Học phí"), [Lý do chất lượng] = "Học phí vượt khả năng", COUNT(SELECT(Chăm sóc[Mã], AND([Mã lead] = [_THISROW].[Mã lead], CONTAINS([Phản hồi], "học phí")))) > 0)
```

**16. Số lần gửi ưu đãi** (cột ảo, kiểu Number)

```
COUNT(SELECT(Gửi thông tin[Mã], AND([Mã lead] = [_THISROW].[Mã lead], [Loại] = "Ưu đãi học phí")))
```

**17. Gửi ưu đãi cuối** (cột ảo, kiểu DateTime)

```
MAX(SELECT(Gửi thông tin[Thời gian], AND([Mã lead] = [_THISROW].[Mã lead], [Loại] = "Ưu đãi học phí")))
```

**18. Gửi thông tin cuối** (cột ảo, kiểu DateTime)

```
MAX(SELECT(Gửi thông tin[Thời gian], AND([Mã lead] = [_THISROW].[Mã lead], [Loại] = "Thông tin hoạt động")))
```

**19. Nên gửi ưu đãi** (cột ảo, kiểu Yes/No)

Công thức: xem dưới

**20. Nên gửi thông tin** (cột ảo, kiểu Yes/No)

```
AND([Giai đoạn] = "Dài hạn", ISNOTBLANK([SĐT]), OR(ISBLANK([Gửi thông tin cuối]), TODAY() >= DATE([Gửi thông tin cuối]) + LOOKUP("Thông tin dài hạn", "Cấu hình", "Khóa", "Giá trị")))
```


**Nên gửi ưu đãi**:

```
AND(
  IN([Giai đoạn], LIST("Đang chăm sóc", "Dài hạn")),
  ISNOTBLANK([SĐT]),
  [Tình trạng hiện tại] <> "Đã đặt cọc",
  IF([Băn khoăn học phí],
    IFS(
      [Số lần gửi ưu đãi] = 0, TODAY() >= DATE([Liên hệ cuối lúc]) + LOOKUP("Ưu đãi lần đầu", "Cấu hình", "Khóa", "Giá trị"),
      [Số lần gửi ưu đãi] >= LOOKUP("Ưu đãi tối đa", "Cấu hình", "Khóa", "Giá trị"), FALSE,
      TRUE, AND(
        TODAY() >= DATE([Gửi ưu đãi cuối]) + LOOKUP("Ưu đãi cách nhau", "Cấu hình", "Khóa", "Giá trị"),
        TODAY() <= DATE([Gửi ưu đãi cuối]) + LOOKUP("Ưu đãi lần 2 trong vòng", "Cấu hình", "Khóa", "Giá trị"))
    ),
    OR([Số lần gửi ưu đãi] = 0, TODAY() >= DATE([Gửi ưu đãi cuối]) + LOOKUP("Ưu đãi cách nhau", "Cấu hình", "Khóa", "Giá trị"))
  )
)
```

## Bước 5. Cột ảo của `Sale`

- **Đang giữ**: `COUNT(SELECT(Hồ sơ lead[Mã lead], AND([Sale phụ trách] = [_THISROW].[Email], [Giai đoạn] = "Đang chăm sóc")))`
- **Đã nhập học**: đổi tên thành `Đã chốt`, công thức `COUNT(SELECT(Hồ sơ lead[Mã lead], AND([Sale phụ trách] = [_THISROW].[Email], [Giai đoạn] = "Đã chốt")))`
- **Tỷ lệ chốt**: `IF([Tổng lead] = 0, 0, DECIMAL([Đã chốt]) / [Tổng lead])`

## Bước 6. Slice, màn hình, tô màu

1. **Format rules**: quy tắc **Đề xuất tạm dừng** đổi tên thành `Dài hạn`, điều kiện `[Giai đoạn] = "Dài hạn"` (giữ màu xanh dương).
2. **Views**: xoá view **Đề xuất tạm dừng**. **Data**: xoá slice **Đề xuất tạm dừng**, rồi xoá cột ảo **Đề xuất tạm dừng** của `Hồ sơ lead`.
3. Hai slice mới trên bảng `Hồ sơ lead`:
   - `Gửi ưu đãi`: `[Nên gửi ưu đãi]`
   - `Gửi thông tin`: `[Nên gửi thông tin]`
4. Hai view mới ở **MENU NAVIGATION**, kiểu **table**, Show if là công thức "chỉ chủ" (`LOOKUP(USEREMAIL(), "Sale", "Email", "Vai trò") = "Chủ"`), Behavior → Row Selected = **Mở hồ sơ**:
   - `Gửi ưu đãi` (slice Gửi ưu đãi): Sort by `Băn khoăn học phí` **Descending**; Column order: Tên phụ huynh, Cơ sở, Sale phụ trách, Băn khoăn học phí, Số lần gửi ưu đãi, Gửi ưu đãi cuối, Lần cuối tóm tắt.
   - `Gửi thông tin` (slice Gửi thông tin): Group by `Cơ sở`; Column order: Tên phụ huynh, Cơ sở, Sale phụ trách, Gửi thông tin cuối, Lần cuối tóm tắt.
5. **`Chăm sóc_Form`**, Column order: Phương thức, PH chủ động, Tình trạng, Mức quan tâm, Phản hồi, Lý do từ chối, Hẹn lại sau, Ngày hẹn gọi lại, Ngày hẹn tham quan, Đã gửi thư mời, Ngày nhập học dự kiến.
6. **`Hồ sơ lead_Detail`**: thêm **Giai đoạn** ngay sau Mức khẩn; thêm **Related Gửi thông tins** ở cuối (sau Related Chăm sócs).
7. Thẻ deck của sale: nếu muốn, đổi **Secondary header** của màn Hôm nay thành `Tình trạng hiện tại` để sale thấy ngay lead nào là "Đã đặt cọc" (cần viết thư mời).

## Bước 7. Nút bấm

1. **Đánh dấu thư mời** (bảng **Chăm sóc**): Do this **Data: set the values of some columns in this row**; Set `Đã gửi thư mời` = `TRUE`; Position **Hide**.
2. **Đã gửi thư mời** (bảng **Hồ sơ lead**): Do this **Data: execute an action on a set of rows**; Referenced table **Chăm sóc**; Referenced rows `LIST([Lần cuối])`; Referenced action **Đánh dấu thư mời**; Position **Prominent**; icon phong bì. Only if: `AND([Tình trạng hiện tại] = "Đã đặt cọc", NOT([Lần cuối].[Đã gửi thư mời]))`.
3. **Đã gửi ưu đãi** (bảng **Hồ sơ lead**): Do this **Data: add a new row to another table using values from this row**; Table **Gửi thông tin**; Set: `Mã lead` = `[Mã lead]`, `Loại` = `"Ưu đãi học phí"` (các cột khác tự điền); Position **Prominent**. Only if: công thức "chỉ chủ". Behavior: Needs confirmation `Đánh dấu đã gửi ưu đãi cho phụ huynh này?`
4. **Đã gửi thông tin**: như nút 3, `Loại` = `"Thông tin hoạt động"`, confirmation `Đánh dấu đã gửi thông tin hoạt động?`
5. View **Gửi ưu đãi**: Actions **Manual**, giữ **Mở Zalo**, **Đã gửi ưu đãi**. View **Gửi thông tin**: **Mở Zalo**, **Đã gửi thông tin**. Màn table cho chọn nhiều dòng (biểu tượng ☑ ở góc trên) rồi bấm nút một lần.

## Bước 8. Bảo mật và email

1. **Security filters**: bảng `Gửi thông tin`: `OR(LOOKUP(USEREMAIL(), "Sale", "Email", "Vai trò") = "Chủ", [Mã lead].[Sale phụ trách] = USEREMAIL())`. Bảng `Ngày nghỉ`: để trống.
2. Bot **Nhắc việc 7h30**: đổi tên `Nhắc việc 8h`; Schedule **Weekly**, chọn **thứ 2 đến thứ 6**, giờ **8:00**.
3. Bot mới **Báo chủ 8h**: Schedule **Weekly**, thứ 2 – thứ 6, 8:00, múi giờ GMT+07:00; For each row in table **Sale**, Filter `AND([Đang làm], [Vai trò] = "Chủ")`; Bypass Security Filters bật. Task **Send an email**, To `[Email]`, Subject `Tình hình chăm sóc lead hôm nay`, Body:

```
Chào <<[Tên]>>,

Lead mới chưa ai liên hệ (đã quá hạn): <<COUNT(SELECT(Hồ sơ lead[Mã lead], [Lead mới chưa liên hệ]))>>
<<Start: SELECT(Hồ sơ lead[Mã lead], [Lead mới chưa liên hệ])>>
- <<[Tên phụ huynh]>> · sale <<[Sale phụ trách].[Tên]>> · nhận <<TEXT([Ngày nhận], "DD/MM")>>
<<End>>

Lead bỏ quên (đang chăm sóc mà quá hạn): <<COUNT(SELECT(Hồ sơ lead[Mã lead], [Bỏ quên]))>>
Nên gửi ưu đãi hôm nay: <<COUNT(SELECT(Hồ sơ lead[Mã lead], [Nên gửi ưu đãi]))>> phụ huynh
Nên gửi thông tin hoạt động: <<COUNT(SELECT(Hồ sơ lead[Mã lead], [Nên gửi thông tin]))>> phụ huynh

Mở app Casa Chăm sóc lead để xem chi tiết.
```

## Bước 9. Kiểm tra

**9a. So hạn với bản chuẩn.** Data → Chăm sóc → bấm công thức **Hạn liên hệ tiếp** → **Test**. Với dữ liệu mẫu v2, cột kết quả phải đúng như cột Hạn liên hệ tiếp trên Sheet (bản Python tính sẵn):

| Hàng | Tình huống | Phải ra |
|---|---|---|
| C0002 | L2, gọi thứ 4 14/10, +3 = thứ 7 | **19/10** (dời sang thứ 2) |
| C0003 | L3, gọi thứ 7 17/10, +7 = thứ 7 | **26/10** |
| C0006 | L1, gọi thứ 6 23/10 | **26/10** |
| C0007 | lần 4 | **trống** (dài hạn) |
| C0009 | hẹn tham quan 04/11 | **03/11** |
| C0010 | chưa liên lạc được, thứ 3 27/10 | **28/10** |
| C0011 | hẹn gọi lại chọn ngày 02/11 | **02/11** |
| C0013 | đã tham quan thứ 6 30/10 | **02/11** |
| C0014 | đặt cọc Chủ nhật 01/11, chưa gửi thư mời | **02/11** |

Nếu mọi hàng đều lệch đúng kiểu "không dời qua thứ 7, Chủ nhật" thì `WORKDAY` chưa chạy: chụp kết quả gửi lại.

**9b. Giai đoạn và danh sách** (thử trong khoảng 04/11 – 16/12/2026):

| Lead | Giai đoạn | Gửi ưu đãi | Gửi thông tin |
|---|---|---|---|
| Lan Thử, Đào Thử | Đang chăm sóc | không (băn khoăn học phí, chưa đủ 60 ngày) | không |
| Hoa, Minh, Quang Thử | Đang chăm sóc | **có** | không |
| Hằng Thử | Đang chăm sóc (chờ thư mời) | không (đã đặt cọc) | không |
| Long Thử | Dài hạn (từ chối vì học phí) | không (chưa đủ 60 ngày) | **có** |
| Thu Thử | Dài hạn (hết L3) | **có** | **có** |

**9c. Thử thao tác** (trên một lead thử, ví dụ thêm lead "Thử V2" của bạn; nhớ ghi ngày hôm nay là thứ mấy):

1. Ghi **Chưa liên lạc được** 3 lần **bằng form** (bấm Ghi nhận 3 lần liền cũng được): lần 1, 2 có hạn là ngày làm việc kế tiếp; lần 3 hạn trống, Giai đoạn **Dài hạn**, lead vào màn Gửi thông tin. Ca này phải thử bằng form, vì nút Test chỉ chạy trên các hàng đã lưu.
2. Ghi tiếp một lần bật **PH chủ động**, Đang cân nhắc: hạn là ngày làm việc kế tiếp (L1), Giai đoạn **Đang chăm sóc**.
3. Ghi **Yêu cầu gọi lại sau**, Hẹn lại sau **1 tuần**: hạn đúng 7 ngày sau (dời nếu rơi vào cuối tuần).
4. Ghi **Đã hẹn tham quan**, ngày tham quan là **thứ 2 tuần sau**: hạn là **thứ 6 tuần này** (ngày làm việc liền trước, không phải Chủ nhật). Nếu hôm nay đã là thứ 6 đó (gọi xác nhận xong, ghi lại một lần Đã hẹn tham quan): hạn chuyển sang **thứ 3** (hỏi cảm nhận sau buổi tham quan).
5. Ghi **Hẹn nhưng không đến**: hạn hôm nay (hoặc thứ 2 nếu hôm nay là cuối tuần).
6. Ghi **Đã đặt cọc**, để Đã gửi thư mời tắt: lead hiện ở màn **Hôm nay**, trong chi tiết có nút **Đã gửi thư mời**. Bấm nút: Giai đoạn **Đã chốt**, lead rời màn Hôm nay.
7. Thêm lead thử khác, ghi **Từ chối** vì **Chọn trường khác**: hạn khoảng 6 tháng sau, nhưng không quá 01/07 kế tiếp. Vì **Xa nhà**: hạn trống, Giai đoạn **Dừng**.
8. Màn **Gửi ưu đãi**: chọn Hoa Thử, bấm **Đã gửi ưu đãi**: Hoa biến khỏi danh sách (lần sau sau 60 ngày), tab `Gửi thông tin` có một hàng mới, chi tiết Hoa Thử có dòng Related Gửi thông tins.
9. Bot **Báo chủ 8h**: bấm **Run**, hộp thư nhận email liệt kê Quang Thử là lead mới chưa liên hệ.

Thử xong xoá các lead và hàng thử trên Sheet.

## Ghi chú

- Hạn liên hệ tiếp là App formula: chỉ tính lại khi hàng Chăm sóc được lưu. Các hàng cũ trên Sheet giữ hạn tính theo quy tắc cũ cho tới khi có lần chăm sóc mới (đó là lý do bước 1 chép lại dữ liệu mẫu v2).
- Tab `Tổng hợp lead`: muốn lọc được tình trạng "Hẹn nhưng không đến" thì thêm chữ đó vào danh sách ở ô `V1` (xem `mau/tong-hop-lead-cong-thuc.md`). Không thêm cũng không sao.
- Bot Telegram không đổi.
