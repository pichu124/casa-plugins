# Nâng cấp app: quy tắc nhắc đợt 2 (tuổi bé, em nhỏ, sau nhập học)

Dành cho app **đã nâng cấp đợt 1** theo `nang-cap-quy-tac-v2.md`. Quy tắc nằm ở `thiet-ke.md` mục 4 (dòng 0a – 0c); `quy_tac_nhac.py` (hàm `trang_thai_lead`) là bản chuẩn có test. Đợt 2 gồm:

- **Bé chưa đủ tuổi nhận học** (dưới 15 tháng): phụ huynh còn cân nhắc, hoặc từ chối vì chưa có nhu cầu / lý do khác → lead **Dài hạn**, app nhắc **30 ngày trước** ngày bé đủ 15 tháng, rồi đúng ngày đủ tuổi.
- **Bé đã quá tuổi** (đủ 6 tuổi vào lúc cần nhắc), hoặc từ chối vì **Sai độ tuổi** → app nhắc sale hỏi một lần: gia đình có em nhỏ hoặc sắp sinh em không. Sale ghi câu trả lời vào ô **Em nhỏ** → lead **Dừng**. Có em thì bấm **Tạo lead cho em**: lead mới của em, app tự nhắc khi em gần đủ tuổi.
- **Sau nhập học**: lead đã chốt (đặt cọc đã gửi thư mời, hoặc Đã nhập học) → 90 ngày sau **ngày vào học** app nhắc sale giới thiệu **chương trình đại sứ phụ huynh**. Ngày vào học là **Ngày nhập học dự kiến** sale điền lúc đặt cọc; không điền thì là ngày sale ghi Đã nhập học lần đầu. Sale ghi lần chăm sóc giới thiệu đại sứ (vào hoặc sau ngày nhắc) là xong.
- Cột **Việc cần làm** cho sale biết lần nhắc này để làm gì (liên hệ lần đầu, xác nhận lịch, hỏi cảm nhận, viết thư mời, hỏi em nhỏ…), hiện trên thẻ lead và trong email 8h.

Tuổi bé: sale nhập **Ngày sinh bé** khi phụ huynh cho ngày cụ thể. Không có thì app **ước tính** từ chữ ở ô Tuổi bé ("18 tháng", "10 tháng tuổi", "2 tuổi", "3-4 tuổi", "dưới 2 tuổi", "2 tuổi rưỡi", "sinh năm 2022", "sinh tháng 3/2023", "02/12/2025"…; có cả tuổi lẫn năm như "8 tháng, sinh 2026" thì dùng tuổi), lấy điểm giữa, lệch vài tuần (trường đã đồng ý). Chữ không có số ("hai tuổi", "mẫu giáo") thì app không đoán, lead chạy như đợt 1.

Mọi công thức đã viết đầy đủ để dán thẳng. Ô công thức nào cũng **gõ `=` trước** rồi dán (hoặc dán vào Expression Assistant). Làm đúng thứ tự: cột sau dùng cột trước. Ước tính: 1 – 1,5 giờ.

## Bước 1. Sheet

Trên bản sao của bạn:

1. Tab **`Hồ sơ lead`**: gõ tiêu đề 3 cột mới vào ô **R1, S1, T1**: `Ngày sinh bé`, `Em nhỏ`, `Ngày sinh em`. Tab `Tổng hợp lead` chỉ đọc cột A – Q nên không phải sửa.
2. Tab **`Cấu hình`**: thêm 4 hàng ở cuối (cột A, B, C):

   | Khóa | Giá trị | Ý nghĩa |
   |---|---|---|
   | Tuổi nhận học (tháng) | 15 | Bé nhỏ hơn tuổi này (tháng) thì chờ, nhắc khi bé sắp đủ tuổi |
   | Nhắc trước tuổi nhận học | 30 | Nhắc trước ngày bé đủ tuổi nhận học chừng này ngày |
   | Tuổi tối đa (tháng) | 72 | Bé đủ tuổi này (tháng) thì nhắc sale hỏi phụ huynh về em nhỏ |
   | Sau nhập học | 90 | Chừng này ngày sau ngày bé vào học thì nhắc giới thiệu chương trình đại sứ |

   Gõ khóa **y hệt** (kể cả "(tháng)"): công thức tra đúng chữ này.
3. Tab **`Danh mục`**: thêm hàng `Nguồn` | `Em nhỏ trong gia đình`.
4. (Để thử ở bước 7) Chép 2 lead mẫu mới và 1 lần chăm sóc từ Sheet mẫu gốc **"Casa – Chăm sóc lead (mẫu, dữ liệu giả)"**: tab `Hồ sơ lead` hàng **L0009** (Tú Thử) và **L0010** (Vy Thử), dán vào hàng trống đầu tiên của bản sao; tab `Chăm sóc` hàng **C0015**, dán vào hàng trống đầu tiên. Đổi `sale2@example.com`, `sale5@example.com` thành email của bạn (như bước 1 của đợt 1).

## Bước 2. Cột mới của `Hồ sơ lead`

**Data → Hồ sơ lead** → nút ↻ (**Regenerate structure**). Kiểm tra lại sau khi regenerate: `Mã lead` vẫn là Key, `Sale phụ trách` vẫn là Ref → Sale, `Chủ nhắc lúc` vẫn trống Initial value. Rồi chỉnh 3 cột mới:

| Cột | Chỉnh |
|---|---|
| Ngày sinh bé | Type **Date**; Initial value trống; không Required; Description `Điền khi phụ huynh cho ngày sinh. Để trống thì app ước tính từ Tuổi bé` |
| Em nhỏ | Type **Enum**, Values `Có em nhỏ`, `Sắp sinh em`, `Không`; Input mode **Buttons**; Initial value trống; Display name `Gia đình có em nhỏ?` |
| Ngày sinh em | Type **Date**; Show? và Required? đều là `IN([Em nhỏ], LIST("Có em nhỏ", "Sắp sinh em"))`; Display name `Ngày sinh (hoặc dự sinh) của em`. Bắt buộc vì không có ngày này thì lead em không được nhắc đúng lúc |

Bấm **SAVE** trước khi sang bước 3 (regenerate mà chưa lưu thì mất).

## Bước 3. Cột ảo mới của `Hồ sơ lead`

**Data → Hồ sơ lead → + Add virtual column**, theo đúng thứ tự dưới. Số 1 – 3 lấy số **thẳng từ ô Tuổi bé**, không qua cột Số tuổi: lấy `INDEX([Số tuổi], 1)` từ cột ảo kiểu List thì AppSheet ra 0 (đã gặp trên app thật). Cột **Tuổi bé chuẩn** chuẩn bị chữ trước khi lấy số: EXTRACTNUMBERS không lấy được số dính chữ ("2t", "18th"), và đọc "02/12/2025" thành một số khổng lồ. Số đó bị coi là năm sinh, làm hàm EOMONTH lỗi và **sập cả app** (đã gặp trên app thật). Vì vậy công thức đổi "/", "-" thành dấu cách, chèn dấu cách trước chữ t, chỉ nhận năm từ 1900 đến 2100, và bỏ qua tuổi trên 240 tháng (ví dụ khi gõ nhầm SĐT vào ô Tuổi bé). AppSheet **tính mọi nhánh của IFS** kể cả nhánh không được chọn, nên số đưa vào EOMONTH còn được kẹp tại chỗ (tháng 1–12, ngày 1–31, tối đa 240 tháng tuổi). Trong `LIST(...)` không trộn số nguyên với số thập phân (`0.0` chứ không `0`). Mọi cột ở bước này **bỏ tick Show** (chỉ dùng để tính), trừ **Ngày sinh dùng** và **Đủ tuổi nhận học** (để Show, sale thấy app hiểu tuổi bé thế nào).

**1. Tuổi bé chuẩn** (cột ảo, kiểu Text)

```
SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE([Tuổi bé], ",", "."), "/", " "), "-", " "), "t", " t"), "T", " T")
```

**2. Số tuổi** (cột ảo, kiểu List (Item type Decimal))

```
EXTRACTNUMBERS([Tuổi bé chuẩn])
```

**3. Số 1** (cột ảo, kiểu Decimal)

```
IF(COUNT(EXTRACTNUMBERS([Tuổi bé chuẩn])) >= 1, ABS(INDEX(EXTRACTNUMBERS([Tuổi bé chuẩn]), 1)), 0)
```

**4. Số 2** (cột ảo, kiểu Decimal)

```
IF(COUNT(EXTRACTNUMBERS([Tuổi bé chuẩn])) >= 2, ABS(INDEX(EXTRACTNUMBERS([Tuổi bé chuẩn]), 2)), 0)
```

**5. Số 3** (cột ảo, kiểu Decimal)

```
IF(COUNT(EXTRACTNUMBERS([Tuổi bé chuẩn])) >= 3, ABS(INDEX(EXTRACTNUMBERS([Tuổi bé chuẩn]), 3)), 0)
```

**6. Năm trong tuổi** (cột ảo, kiểu Number)

```
IF(AND(MAX(LIST([Số 1], [Số 2], [Số 3])) >= 1900, MAX(LIST([Số 1], [Số 2], [Số 3])) <= 2100), ROUND(MAX(LIST([Số 1], [Số 2], [Số 3]))), 0)
```

**7. Số đếm** (cột ảo, kiểu Number)

```
IFS([Năm trong tuổi] = 0, COUNT([Số tuổi]), [Số 1] >= 1900, 0, [Số 2] >= 1900, 1, TRUE, 2)
```

**8. Tháng tuổi lúc nhận** (cột ảo, kiểu Decimal)

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

**9. Ngày sinh dùng** (cột ảo, kiểu Date)

```
IFS(
  ISNOTBLANK([Ngày sinh bé]), [Ngày sinh bé],
  AND([Năm trong tuổi] > 0, [Số 3] >= 1900, [Số 2] >= 1, [Số 2] <= 12, [Số 1] >= 1, [Số 1] <= 31, OR(CONTAINS([Tuổi bé], "/"), CONTAINS([Tuổi bé], "-"))),
    MIN(LIST(
      EOMONTH(DATE([Ngày nhận]), ([Năm trong tuổi] - YEAR([Ngày nhận])) * 12 - MONTH([Ngày nhận]) + MIN(LIST(12, MAX(LIST(1, ROUND([Số 2]))))) - 1) + MIN(LIST(31, MAX(LIST(1, ROUND([Số 1]))))),
      EOMONTH(DATE([Ngày nhận]), ([Năm trong tuổi] - YEAR([Ngày nhận])) * 12 - MONTH([Ngày nhận]) + MIN(LIST(12, MAX(LIST(1, ROUND([Số 2])))))))),
  AND([Năm trong tuổi] > 0, [Số 2] >= 1900, [Số 1] >= 1, [Số 1] <= 12, OR(CONTAINS([Tuổi bé], "/"), CONTAINS([Tuổi bé], "-"), CONTAINS([Tuổi bé], CONCATENATE("tháng ", ROUND([Số 1]))), CONTAINS([Tuổi bé], CONCATENATE("thang ", ROUND([Số 1]))))),
    EOMONTH(DATE([Ngày nhận]), ([Năm trong tuổi] - YEAR([Ngày nhận])) * 12 - MONTH([Ngày nhận]) + MIN(LIST(12, MAX(LIST(1, ROUND([Số 1]))))) - 1) + 15,
  AND(ISNOTBLANK([Tháng tuổi lúc nhận]), [Tháng tuổi lúc nhận] <= 240), DATE([Ngày nhận]) - ROUND(MIN(LIST(240.0, [Tháng tuổi lúc nhận])) * 30.44),
  [Năm trong tuổi] > 0,
    EOMONTH(DATE([Ngày nhận]), ([Năm trong tuổi] - YEAR([Ngày nhận])) * 12 - MONTH([Ngày nhận]) + 6) + 1,
  TRUE, ""
)
```

**10. Đủ tuổi nhận học** (cột ảo, kiểu Date)

```
IF(ISBLANK([Ngày sinh dùng]), "", MIN(LIST(EOMONTH([Ngày sinh dùng], LOOKUP("Tuổi nhận học (tháng)", "Cấu hình", "Khóa", "Giá trị") - 1) + DAY([Ngày sinh dùng]), EOMONTH([Ngày sinh dùng], LOOKUP("Tuổi nhận học (tháng)", "Cấu hình", "Khóa", "Giá trị")))))
```

**11. Hết tuổi** (cột ảo, kiểu Date)

```
IF(ISBLANK([Ngày sinh dùng]), "", MIN(LIST(EOMONTH([Ngày sinh dùng], LOOKUP("Tuổi tối đa (tháng)", "Cấu hình", "Khóa", "Giá trị") - 1) + DAY([Ngày sinh dùng]), EOMONTH([Ngày sinh dùng], LOOKUP("Tuổi tối đa (tháng)", "Cấu hình", "Khóa", "Giá trị")))))
```

**12. Hạn cơ bản** (cột ảo, kiểu Date)

```
IF(ISBLANK([Lần cuối]), WORKDAY(DATE([Ngày nhận]) - 1, 1, Ngày nghỉ[Ngày]), [Lần cuối].[Hạn liên hệ tiếp])
```

**13. Chốt rồi** (cột ảo, kiểu Yes/No)

```
OR([Lần cuối].[Tình trạng] = "Đã nhập học", AND([Lần cuối].[Tình trạng] = "Đã đặt cọc", [Lần cuối].[Đã gửi thư mời]))
```

**14. Mốc hỏi em** (cột ảo, kiểu Date)

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

**15. Chờ đủ tuổi** (cột ảo, kiểu Yes/No)

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

**16. Hạn chờ tuổi** (cột ảo, kiểu Date)

```
IF(DATE([Liên hệ cuối lúc]) < [Đủ tuổi nhận học] - LOOKUP("Nhắc trước tuổi nhận học", "Cấu hình", "Khóa", "Giá trị"), [Đủ tuổi nhận học] - LOOKUP("Nhắc trước tuổi nhận học", "Cấu hình", "Khóa", "Giá trị"), [Đủ tuổi nhận học])
```

**17. Ngày vào học** (cột ảo, kiểu Date)

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

**18. Hạn đại sứ** (cột ảo, kiểu Date)

```
IF(AND(ISNOTBLANK([Ngày vào học]), DATE([Liên hệ cuối lúc]) < [Ngày vào học] + LOOKUP("Sau nhập học", "Cấu hình", "Khóa", "Giá trị")), [Ngày vào học] + LOOKUP("Sau nhập học", "Cấu hình", "Khóa", "Giá trị"), "")
```


## Bước 4. Sửa 2 cột ảo cũ, thêm Việc cần làm

**Hạn liên hệ** và **Giai đoạn** đã có: mở từng cột, xoá công thức cũ, dán công thức mới. **Việc cần làm** là cột ảo mới (Show bật).

**19. Hạn liên hệ** (cột ảo, kiểu Date)

```
IFS(
  [Tạm dừng], "",
  ISNOTBLANK([Mốc hỏi em]), IF(ISBLANK([Em nhỏ]), WORKDAY([Mốc hỏi em] - 1, 1, Ngày nghỉ[Ngày]), ""),
  ISNOTBLANK([Hạn đại sứ]), WORKDAY([Hạn đại sứ] - 1, 1, Ngày nghỉ[Ngày]),
  [Chờ đủ tuổi], WORKDAY([Hạn chờ tuổi] - 1, 1, Ngày nghỉ[Ngày]),
  TRUE, [Hạn cơ bản]
)
```

**20. Giai đoạn** (cột ảo, kiểu Text)

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

**21. Việc cần làm** (cột ảo, kiểu Text)

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


**22. Nhóm** (sửa cột cũ, Text): lead Dài hạn hay Đã chốt có hạn còn xa (chờ đủ tuổi, nhắc đại sứ) nằm ở nhóm "4 · Dài hạn" / "4 · Đã chốt" của màn Của tôi, không lẫn vào "3 · Sắp tới"; tới hạn thì lên "Hôm nay" như thường.

```
IFS([Mức khẩn] = "Quá hạn", "1 · Quá hạn", [Mức khẩn] = "Hôm nay", "2 · Hôm nay", AND([Mức khẩn] = "Sắp tới", [Giai đoạn] = "Đang chăm sóc"), "3 · Sắp tới", TRUE, CONCATENATE("4 · ", [Giai đoạn]))
```

Các cột Mức khẩn, Bỏ quên, Nên gửi ưu đãi, Nên gửi thông tin… dùng Hạn liên hệ và Giai đoạn nên tự theo, không phải sửa.

## Bước 5. Màn hình, nút, email

1. **`Hồ sơ lead_Form`**, Column order: thêm **Ngày sinh bé** ngay sau Tuổi bé; **Em nhỏ**, **Ngày sinh em** sau Ghi chú.
2. **`Hồ sơ lead_Detail`**: thêm **Việc cần làm** ngay sau Giai đoạn; **Ngày sinh bé**, **Ngày sinh dùng**, **Đủ tuổi nhận học** sau Tuổi bé; **Em nhỏ**, **Ngày sinh em** sau Ghi chú.
3. Màn **Hôm nay** (deck của sale): **Secondary header** = `Việc cần làm`.
4. Nút mới **Tạo lead cho em** (bảng **Hồ sơ lead**): Do this **App: go to another view within this app**; Target:

   ```
   LINKTOFORM("Hồ sơ lead_Form",
     "Tên phụ huynh", [Tên phụ huynh], "SĐT", [SĐT], "Cơ sở", [Cơ sở],
     "Nguồn", "Em nhỏ trong gia đình", "Ngày sinh bé", [Ngày sinh em],
     "Sale phụ trách", [Sale phụ trách],
     "Ghi chú", CONCATENATE("Em của ", [Tên bé], " (lead ", [Mã lead], ")"))
   ```

   Position **Prominent**; icon em bé hoặc dấu cộng. Only if:

   ```
   AND(IN([Em nhỏ], LIST("Có em nhỏ", "Sắp sinh em")), ISNOTBLANK([Ngày sinh em]), COUNT(SELECT(Hồ sơ lead[Mã lead], AND([SĐT] = [_THISROW].[SĐT], [Nguồn] = "Em nhỏ trong gia đình"))) = 0)
   ```

   (hết hiện sau khi đã tạo lead em, để không tạo hai lần). Form mở ra đã điền sẵn; sale điền Tên bé nếu đã có rồi lưu.
5. Bot **Lead trùng** (Automation): Condition thêm điều kiện nguồn, để lead em (cùng SĐT với anh/chị) không bị báo trùng:

   ```
   AND([Nguồn] <> "Em nhỏ trong gia đình", COUNT(SELECT(Hồ sơ lead[Mã lead], AND([SĐT] = [_THISROW].[SĐT], [Mã lead] <> [_THISROW].[Mã lead]))) > 0)
   ```

6. Bot **Nhắc việc 8h**, Email body: đổi dòng giữa `<<Start …>>` và `<<End>>` thành

   ```
   - <<[Tên phụ huynh]>> (bé <<[Tên bé]>>), <<[Mức khẩn]>>: <<[Việc cần làm]>>
   ```

## Bước 6. Cách sale dùng (dặn sale)

- Phụ huynh cho ngày sinh cụ thể → điền **Ngày sinh bé**. Chỉ nói chung chung → để trống, ghi Tuổi bé như phụ huynh nói (có số: "18 tháng", "2 tuổi rưỡi", "sinh năm 2022").
- Bé còn nhỏ, phụ huynh hẹn khi nào bé đủ tuổi → ghi **Đang cân nhắc** (đừng chọn Hẹn lại sau): app tự nhắc trước ngày bé đủ 15 tháng.
- Thẻ lead ghi **Hỏi phụ huynh có em nhỏ hoặc sắp sinh em** → gọi hỏi, rồi mở lead, bấm sửa (bút chì), chọn **Gia đình có em nhỏ?** và ngày sinh / dự sinh của em. Không cần ghi thêm lần chăm sóc nếu chỉ hỏi chuyện này. Có em → bấm **Tạo lead cho em**.
- Đặt cọc → điền **Ngày nhập học dự kiến** ngay trong lần ghi nhận Đã đặt cọc. Ngày bé vào học cứ ghi **Đã nhập học** như trước (tab Thống kê đếm theo lần ghi này).
- 90 ngày sau ngày vào học, thẻ lead ghi **Giới thiệu chương trình đại sứ phụ huynh**. Gọi giới thiệu xong, ghi một lần chăm sóc tình trạng **Đã nhập học**, Phản hồi ví dụ `Đã giới thiệu đại sứ`: app thôi nhắc.

## Bước 7. Kiểm tra

**7a. Hai lead mẫu** (sau bước 1.4). Mở chi tiết:

| Lead | Ngày sinh dùng | Đủ tuổi nhận học | Hạn liên hệ | Giai đoạn | Việc cần làm |
|---|---|---|---|---|---|
| Tú Thử ("sinh năm 2020") | 01/07/2020 | 01/10/2021 | 02/11/2026 (quá hạn) | Đang chăm sóc | Hỏi phụ huynh có em nhỏ hoặc sắp sinh em |
| Vy Thử ("10 tháng", đang cân nhắc) | 28/12/2025 | 28/03/2027 | 26/02/2027 | Dài hạn | Bé sắp đủ tuổi nhận học |

8 lead mẫu cũ phải **giữ nguyên** Hạn liên hệ và Giai đoạn như trước khi nâng cấp (bảng 9b của đợt 1).

**7b. Đọc tuổi.** Data → Hồ sơ lead → cột **Tháng tuổi lúc nhận** → **Test**: thấy giá trị của mọi lead. Rồi sửa Tuổi bé của Tú Thử lần lượt thành các chữ dưới, mỗi lần xem chi tiết lead (cột Tháng tuổi lúc nhận đang ẩn: bật Show tạm để xem, thử xong tắt), cuối cùng trả lại `sinh năm 2020`:

| Tuổi bé | Tháng tuổi lúc nhận | | Tuổi bé | Tháng tuổi lúc nhận |
|---|---|---|---|---|
| 2 tuổi | 30 | | 18 tháng | 18 |
| 3-4 tuổi | 48 | | dưới 18 tháng | 15 |
| dưới 2 tuổi | 18 | | 2t | 30 |
| 1,5 tuổi | 18 | | 18th | 18 |
| 2 tuổi 8 tháng | 32 | | sinh năm 2020 | trống (Ngày sinh dùng 01/07/2020) |
| 2 tuổi rưỡi | 30 | | sinh tháng 3/2023 | trống (Ngày sinh dùng 15/03/2023) |
| 10 tháng tuổi | 10 | | sinh 02/12/2025 | trống (Ngày sinh dùng 02/12/2025) |
| 30 tháng tuổi | 30 | | sinh 2021 | trống (Ngày sinh dùng 01/07/2021) |
| 8 tháng, sinh 2026 | 8 | | tháng 4 năm 2024 | trống (Ngày sinh dùng 15/04/2024) |
| dưới 2 tháng | 0 | | 2 tuổi 3 tháng, sinh 2024 | 27 |

Chữ nào ra khác bảng thì chụp màn hình gửi lại: AppSheet đọc số trong chữ (EXTRACTNUMBERS) có thể khác với dự tính ở các chữ như "2t", "3-4".

**7c. Thử tay** (ví dụ ngày thử là thứ 4, 04/11/2026; thử ngày khác thì ngày ra khác, xem quy tắc ở đầu file):

1. Thêm lead **Thử Nhỏ**, Tuổi bé `10 tháng`, ghi nhận **Đang cân nhắc** → Dài hạn, Hạn **05/03/2027**, Việc: Bé sắp đủ tuổi nhận học.
2. Thêm lead **Thử Lớn**, Ngày sinh bé `04/11/2020` (đủ 6 tuổi hôm nay) → Hạn hôm nay, Việc: Hỏi phụ huynh có em nhỏ… Sửa lead: Gia đình có em nhỏ? = **Sắp sinh em**, ngày `15/01/2027` → Giai đoạn **Dừng**, nút **Tạo lead cho em** hiện ra. Bấm, lưu form → lead mới nguồn Em nhỏ trong gia đình: Dài hạn, Hạn **16/03/2028**. Email chủ **không** nhận "Lead trùng SĐT". Nút Tạo lead cho em ở lead Thử Lớn biến mất.
3. Lead **Thử Lớn 2**, Tuổi bé `3 tuổi`, ghi nhận **Từ chối**, lý do **Sai độ tuổi** → Đang chăm sóc, Hạn hôm nay, Việc: Hỏi phụ huynh có em nhỏ… Chọn Em nhỏ = **Không** → Dừng.
4. Lead **Thử Cọc**, ghi nhận **Đã đặt cọc**, Ngày nhập học dự kiến `01/12/2026` → bấm **Đã gửi thư mời** → Đã chốt, Hạn **01/03/2027**, Việc: Giới thiệu chương trình đại sứ phụ huynh. Ghi nhận **Đã nhập học** (giả như bé vào học) → Hạn **vẫn 01/03/2027**. (Ghi lần chăm sóc vào hoặc sau 01/03/2027 thì hạn trống; hôm nay chưa thử được.)
5. Lead **Thử Vào Học**, ghi nhận thẳng **Đã nhập học** hôm nay → Đã chốt, Hạn **02/02/2027** (04/11 + 90 ngày).

Thử xong xoá các lead Thử… (và lần chăm sóc của chúng) trên Sheet.

## Ghi chú

- Tab `Tổng hợp lead` trên Sheet vẫn tính hạn theo đợt 1 (chưa biết tuổi bé): lead chờ đủ tuổi, hỏi em nhỏ, nhắc đại sứ có thể hiện hạn khác app. App là chuẩn.
- Lead **Tạm dừng** vẫn Dừng, không nhắc gì.
- Lead từ chối vì **Xa nhà** hoặc **Sai số điện thoại** không bị nhắc hỏi em nhỏ.
- **Ngay sau khi nâng cấp**, các lead cũ sau đây đổi cùng lúc và hiện ở màn Hôm nay, email 8h, danh sách Bỏ quên: lead từ chối vì Sai độ tuổi (trước là Dừng, nay nhắc hỏi em nhỏ), lead có bé đã đủ 6 tuổi (nhắc hỏi em nhỏ), lead đã nhập học hơn 90 ngày (nhắc đại sứ, quá hạn). Lead hỏi em nhỏ ở giai đoạn Đang chăm sóc nên cũng có thể vào danh sách Gửi ưu đãi. Hiện app chỉ có dữ liệu giả nên không sao; khi chuyển sang dữ liệu thật, báo trước cho sale, hoặc điền ô Em nhỏ = `Không` cho những lead không cần hỏi.
