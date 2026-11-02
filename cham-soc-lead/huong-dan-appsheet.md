# Hướng dẫn dựng app chăm sóc lead bằng AppSheet

Làm trên máy tính, trình duyệt Chrome. Khoảng 2 – 3 giờ cho lần đầu. Mọi tên cột, công thức nằm trong [thiet-ke.md](thiet-ke.md); hướng dẫn này chỉ chỗ bấm.

Tên nút trong AppSheet là tiếng Anh, ghi đúng như trên màn hình. Giao diện AppSheet thay đổi theo thời gian, nên vị trí nút có thể khác một chút.

## Bước 0. Chuẩn bị Sheet

1. Đăng nhập Google bằng **tài khoản Workspace của trường** (tài khoản có gói AppSheet Core).
2. Mở Sheet mẫu **"Casa – Chăm sóc lead (mẫu, dữ liệu giả)"**, chọn **Tệp → Tạo bản sao**, lưu vào Drive của tài khoản trường. App sẽ dựng trên bản sao này, để app và dữ liệu cùng thuộc tài khoản trường.
3. Để một mình bạn thử được cả màn hình của sale lẫn của chủ:
   - Dùng **Chỉnh sửa → Tìm và thay thế**, tick **Tìm kiếm trên mọi trang tính**, đổi `sale1@example.com` thành **email của bạn**.
   - Ở tab `Sale`, xoá hàng `chu@example.com`, rồi đổi **Vai trò** của hàng mang email của bạn thành `Chủ`.
   - Khi đó bạn là sale phụ trách lead Hoa Thử và Đào Thử, và thấy thêm các màn hình của chủ.

Sheet có 7 tab: `Hồ sơ lead`, `Chăm sóc`, `Sale`, `Danh mục`, `Cấu hình`, `Thống kê` (chỉ có công thức, tự tính theo tháng), và `Leads` (bản giả của tab bot ghi).

## Bước 1. Tạo app

1. Vào **appsheet.com** → **Create** → **App** → **Start with existing data**.
2. Tên app: `Casa Chăm sóc lead`. Category: để mặc định. **Choose your data** → chọn bản sao Sheet ở bước 0.
3. AppSheet tự tạo app từ tab đầu tiên (`Hồ sơ lead`). Chờ nó dựng xong.

## Bước 2. Thêm các bảng

Vào **Data** (biểu tượng cơ sở dữ liệu bên trái) → **+** (Add new data) → chọn cùng file Sheet → chọn lần lượt tab `Chăm sóc`, `Sale`, `Danh mục`, `Cấu hình`, `Thống kê`, `Leads`.

- Bảng `Leads`: đổi tên hiển thị thành `Messenger`. Trong **Table settings**, mục **Are updates allowed?** chọn **Read-Only**. App không được sửa tab của bot.
- Bảng `Danh mục`, `Cấu hình`: chọn **Read-Only** (chủ sửa trực tiếp trên Sheet).
- Bảng `Thống kê`: **Read-Only**; cột `Mã` là **Key**; cột Tỷ lệ… chọn Type **Percent**.

## Bước 3. Cột của từng bảng

Trong **Data** → chọn bảng → **Columns**. Với mỗi cột, chỉnh **Type** và các ô khác đúng như bảng ở thiet-ke.md mục 3. Những chỗ hay sai:

**`Hồ sơ lead`**
- `Mã lead`: tick **Key**; **Initial value** `UNIQUEID()`; bỏ tick **Show**.
- `Ngày nhận`: Initial value `NOW()`; **Editable** tắt.
- `SĐT`: Type **Phone**.
- `Cơ sở`, `Nguồn`: Type **Enum**; trong **Valid If** nhập `SELECT(Danh mục[Giá trị], [Loại] = "Cơ sở")` (với Nguồn đổi chữ "Cơ sở" thành "Nguồn").
- `PH quan tâm`: Type **EnumList**, Valid If `SELECT(Danh mục[Giá trị], [Loại] = "Mối quan tâm")`.
- `Sale phụ trách`: Type **Ref**, Source table `Sale`; Initial value `USEREMAIL()`; **Editable If** là công thức "ai là chủ" ở thiet-ke.md mục 4.
- `Chất lượng lead`: Enum `Tốt`, `Trung bình`, `Kém`.
- `Lý do chất lượng`: Enum, Valid If `SELECT(Danh mục[Giá trị], [Loại] = "Lý do chất lượng")`; **Show If** `IN([Chất lượng lead], LIST("Trung bình", "Kém"))`.
- `Customer ID`: bỏ tick **Show**.
- `Tên phụ huynh`, `Tên bé`, `SĐT`: tick **Search** (để ô tìm kiếm tìm được theo các cột này). Bỏ tick Search ở các cột còn lại cho kết quả gọn.
- `Tạm dừng`: Type **Yes/No**; Editable If là công thức "ai là chủ".

**`Chăm sóc`**
- `Mã`: Key, Initial value `UNIQUEID()`, ẩn.
- `Mã lead`: Type **Ref**, Source table `Hồ sơ lead`, tick **Is a part of**.
- `Thời gian`: Initial value `NOW()`, Editable tắt. `Sale`: Type Ref → `Sale`, Initial value `USEREMAIL()`, Editable tắt.
- `Phương thức`, `Tình trạng`, `Mức quan tâm`: Type **Enum**, nhập các giá trị như thiet-ke.md; **Input mode** chọn **Buttons**; tick **Require**.
- `Mức quan tâm`: Show If `NOT(IN([Tình trạng], LIST("Từ chối", "Chưa liên lạc được")))`; **Required If** dùng cùng công thức (bỏ tick Require).
- `Lý do từ chối`: Enum, Valid If loại "Lý do từ chối"; Show If và Required If: `[Tình trạng] = "Từ chối"`.
- `Ngày hẹn gọi lại`: Type Date; Show If `NOT(IN([Tình trạng], LIST("Từ chối", "Đã nhập học")))`; Required If `[Tình trạng] = "Yêu cầu gọi lại sau"`.
- `Ngày hẹn tham quan`: Type Date; Show If và Required If `[Tình trạng] = "Đã hẹn tham quan / học thử"`.
- `Lần thứ`, `Hạn liên hệ tiếp`: điền **App formula** từ thiet-ke.md mục 4; bỏ tick Show trong form (vẫn hiện ở trang chi tiết nếu muốn).
- **Thêm cột ảo** `Mốc gần nhất` (nút **Add virtual column**), Type Ref → `Chăm sóc`, công thức ở thiet-ke.md. Làm cột này **trước** khi nhập công thức `Lần thứ`.

**`Sale`**: `Email` là Key, Type Email; `Vai trò` Enum `Sale`, `Chủ`; `Đang làm` Yes/No.

**`Messenger`** (tab `Leads`): Key là `Customer ID`. Nếu AppSheet báo tên cột có dấu `/` (như `Cơ sở/hệ`) không hợp lệ, nó sẽ tự đổi tên hiển thị; ghi lại tên mới để dùng ở bước 6.

Sau đó thêm các **cột ảo** của `Hồ sơ lead` và `Sale` đúng như bảng ở thiet-ke.md mục 4. Thêm theo thứ tự trong bảng, vì cột sau dùng cột trước.

## Bước 4a. Nút chọn tháng và cơ sở cho chủ (User settings)

**Settings** → **User settings** (cài đặt riêng của từng người dùng):

- Bật một ô tùy chỉnh, đặt tên `Tháng`: Type **Enum**; **Valid If** `SORT(UNIQUE(Thống kê[Tháng]), TRUE)`; **Initial value** `TEXT(TODAY(), "YYYY-MM")`.
- Ô thứ hai `Cơ sở`: Type **Enum**; Valid If `UNIQUE(Thống kê[Cơ sở])`; Initial value `"Tất cả"`.

Người dùng đổi tháng, cơ sở trong menu **Settings** của app; mọi màn hình báo cáo đổi theo.

## Bước 4. Lát cắt dữ liệu (Slices)

**Data** → bảng → **Slices** → **New slice**:

| Slice | Bảng | Điều kiện (Row filter condition) |
|---|---|---|
| Hôm nay của tôi | Hồ sơ lead | `AND([Sale phụ trách] = USEREMAIL(), IN([Mức khẩn], LIST("Quá hạn", "Hôm nay")))` |
| Lead của tôi | Hồ sơ lead | `[Sale phụ trách] = USEREMAIL()` |
| Bỏ quên | Hồ sơ lead | `[Bỏ quên]` |
| Rất quan tâm chưa chốt | Hồ sơ lead | `AND([Mức quan tâm hiện tại] = "Rất quan tâm", NOT([Đã kết thúc]), [Tình trạng hiện tại] <> "Đã đặt cọc")` |
| Đề xuất tạm dừng | Hồ sơ lead | `[Đề xuất tạm dừng]` |
| Messenger chưa nhận | Messenger | `AND(ISNOTBLANK([SĐT]), NOT(IN([Customer ID], Hồ sơ lead[Customer ID])), [Giai đoạn] <> "Không quan tâm")` |
| Tháng đang chọn | Thống kê | `AND([Tháng] = USERSETTINGS("Tháng"), [Cơ sở] = USERSETTINGS("Cơ sở"))` |
| Lead tháng đang chọn | Hồ sơ lead | `AND(TEXT([Ngày nhận], "YYYY-MM") = USERSETTINGS("Tháng"), OR(USERSETTINGS("Cơ sở") = "Tất cả", [Cơ sở] = USERSETTINGS("Cơ sở")))` |

## Bước 5. Màn hình (Views)

Vào **Views** (biểu tượng điện thoại bên trái) → **+ New view**. Mỗi view chọn **For this data** là slice hoặc bảng, **View type**, và **Position**.

| View | Dữ liệu | Kiểu | Vị trí | Ghi chú |
|---|---|---|---|---|
| Hôm nay | Hôm nay của tôi | Deck | first | Sort by `Hạn liên hệ` tăng dần. Đặt làm **Starting view** (Settings → Views → General) |
| Của tôi | Lead của tôi | Deck | next | Group by `Mức khẩn` |
| Tìm phụ huynh | Hồ sơ lead | Deck | next | Toàn bộ lead của trường. Ô tìm kiếm có sẵn ở góc trên; Group by `Cơ sở`. Khi phụ huynh tự gọi tới: gõ tên hoặc vài số cuối SĐT, mở ra, ghi nhận |
| Messenger | Messenger chưa nhận | Table | menu | |
| Theo sale | Sale | Table | menu | Hiện các cột ảo Đang giữ, Liên hệ hôm nay, Quá hạn, Tỷ lệ chốt, Số lần chăm sóc |
| Bỏ quên | Bỏ quên | Table | menu | |
| Rất quan tâm chưa chốt | Rất quan tâm chưa chốt | Table | menu | |
| Đề xuất tạm dừng | Đề xuất tạm dừng | Table | menu | |
| Báo cáo tháng | Tháng đang chọn | Detail | menu | Hiện Tháng, Cơ sở, Lead mới, Lead mới tháng trước, rồi từng bước kèm tỷ lệ. Thêm cột ảo nếu muốn % so với bước trước, vd `IF([Đã tư vấn] = 0, 0, [Đã tham quan] / [Đã tư vấn])` |
| Lead của tháng | Lead tháng đang chọn | Table | menu | Danh sách lead của tháng và cơ sở đang chọn, cột Tình trạng hiện tại, Nguồn, Sale phụ trách |
| Các tháng | Thống kê | Table | menu | Group by `Tháng`; so sánh các tháng, các cơ sở |
| Lead theo tháng | Thống kê | Chart (Column) | menu | Trục ngang `Tháng`, giá trị `Lead mới`, chỉ dòng "Tất cả" (dùng một slice `[Cơ sở] = "Tất cả"`) |
| Theo nguồn | Hồ sơ lead | Chart | menu | Cột `Nguồn`; thêm một chart nữa cho `Chất lượng lead` |
| Lý do từ chối | Chăm sóc | Chart | menu | Cột `Lý do từ chối` |

Với 6 view cuối (của chủ), trong mục **Display** → **Show if** nhập công thức "ai là chủ" (thiet-ke.md mục 4).

**Form `Chăm sóc`** (view `Chăm sóc_Form` AppSheet tự tạo): sắp thứ tự cột: Phương thức, Tình trạng, Mức quan tâm, Phản hồi, Lý do từ chối, Ngày hẹn gọi lại, Ngày hẹn tham quan. Ẩn Mã, Mã lead, Thời gian, Sale, Lần thứ, Hạn liên hệ tiếp.

**Trang chi tiết `Hồ sơ lead`**: để `Tên phụ huynh`, `SĐT`, `Mức khẩn`, `Hạn liên hệ`, `Tình trạng hiện tại` lên đầu. Danh sách lần chăm sóc (`Related Chăm sócs`) hiện ở cuối, kèm nút **Add** để ghi lần mới.

## Bước 6. Nút bấm (Actions)

Vào **Actions** (biểu tượng tia chớp) → **+ New action**:

1. **Mở Zalo** (bảng `Hồ sơ lead`): Do this **External: go to a website**; Target `CONCATENATE("https://zalo.me/", SUBSTITUTE([SĐT], " ", ""))`; Position **Prominent**.
2. **Ghi nhận lần chăm sóc** (bảng `Hồ sơ lead`): Do this **App: go to another view within this app**; Target `LINKTOFORM("Chăm sóc_Form", "Mã lead", [Mã lead])`; Position **Prominent**.
3. **Nhận lead này** (bảng `Messenger`): Do this **Data: add a new row to another table using values from this row**; Table `Hồ sơ lead`; đặt giá trị:
   - Mã lead `UNIQUEID()`; Ngày nhận `NOW()`; Tên phụ huynh `[Tên Facebook]`; Tên bé `[Tên bé]`; Tuổi bé `[Tuổi bé]`; SĐT `[SĐT]`
   - Nguồn `"Facebook Messenger"`; Chiến dịch `[Quảng cáo]`; Sale phụ trách `USEREMAIL()`; Customer ID `[Customer ID]`; Tạm dừng `FALSE`
   - Ghi chú `CONCATENATE("Bot ghi cơ sở: ", [Cơ sở/hệ], ". Tin cuối: ", [Tin cuối của phụ huynh])` (đổi tên cột nếu AppSheet đã đổi ở bước 3)

   Only if `NOT(IN([Customer ID], Hồ sơ lead[Customer ID]))`. Position **Prominent**.

AppSheet tự có nút Gọi và SMS cho cột kiểu Phone.

## Bước 7. Tô màu (Format rules)

**Views** → **Format rules** → **+ New format rule**, bảng `Hồ sơ lead`:

- `[Mức khẩn] = "Quá hạn"`: chữ đỏ, đậm, biểu tượng cảnh báo.
- `[Mức khẩn] = "Hôm nay"`: chữ cam.
- `[Đề xuất tạm dừng]`: chữ xám.

## Bước 8. Email nhắc mỗi sáng

**Automation** → **+ New bot** → tên `Nhắc việc 7h30`:

1. **Event**: **Schedule**, mỗi ngày (Daily) lúc **07:30**, múi giờ **(GMT+07:00) Indochina Time**. **For each row in table** `Sale`, điều kiện `AND([Đang làm], [Vai trò] = "Sale")`.
2. **Process** → **Run a task** → **Send an email**: To `[Email]`; Subject `Hôm nay cần liên hệ phụ huynh`; Body (nhập ở ô Email body):

```
Chào <<[Tên]>>,

Hôm nay bạn có <<COUNT(SELECT(Hồ sơ lead[Mã lead], AND([Sale phụ trách] = [_THISROW].[Email], [Mức khẩn] = "Hôm nay")))>> phụ huynh cần liên hệ và <<COUNT(SELECT(Hồ sơ lead[Mã lead], AND([Sale phụ trách] = [_THISROW].[Email], [Mức khẩn] = "Quá hạn")))>> phụ huynh đã quá hạn.

<<Start: ORDERBY(SELECT(Hồ sơ lead[Mã lead], AND([Sale phụ trách] = [_THISROW].[Email], IN([Mức khẩn], LIST("Quá hạn", "Hôm nay")))), [Hạn liên hệ])>>
- <<[Tên phụ huynh]>> (bé <<[Tên bé]>>), <<[Mức khẩn]>>, <<[Tình trạng hiện tại]>>
<<End>>

Mở app Casa Chăm sóc lead để ghi nhận sau mỗi lần liên hệ.
```

Email không ghi SĐT.

## Bước 9. Người dùng và quyền

1. **Security** → **Require Sign-In**: bật. **Domain authentication**: chỉ người trong tên miền của trường.
2. Chỉ cho email trong tab `Sale` dùng: **Security** → **Security filters** không cần; thay vào đó ở **Settings → Users**, thêm 6 email sale (hoặc chia sẻ app cho nhóm Google của sale).
3. Bảng `Chăm sóc` → **Are updates allowed?** để **Adds and Updates** (không cho xoá). Cột `Phản hồi`, `Tình trạng`… có **Editable If** `OR([Sale] = USEREMAIL(), <công thức ai là chủ>)`.
4. Bảng `Hồ sơ lead` → **Adds and Updates** (không cho xoá; lead không còn theo thì chủ bật Tạm dừng).

## Bước 10. Thử với dữ liệu mẫu

Mở app (nút **Preview** bên phải, hoặc mở link app trên điện thoại). Với Sheet mẫu tạo ngày 02/11/2026 và `sale1@example.com` đã đổi thành email của bạn (bước 0), kết quả đúng là:

- [ ] Màn hình **Hôm nay** có **Hoa Thử** (hẹn gọi lại hôm nay) và **Đào Thử** (quá hạn, chữ đỏ).
- [ ] **Tìm phụ huynh** có 8 lead. Gõ "Minh" ra Minh Thử; gõ "0604" ra Hằng Thử (lead của Sale 4). Mở Hằng Thử, ghi nhận một lần: lưu được, và lần đó mang email của bạn.
- [ ] Settings chọn Tháng **2026-10**, Cơ sở **Tất cả** → **Báo cáo tháng**: Lead mới 7, Đã tư vấn 7, Đã tham quan 1, Đã đặt cọc 1, Đã nhập học 0, Tỷ lệ tham quan 14%. Đổi Cơ sở sang **Mỹ Đình**: 2, 2, 1, 1, 0. Chọn Tháng **2026-11**, Tất cả: Lead mới 1, Lead mới tháng trước 7.
- [ ] Mở **Thu Thử**: Tình trạng hiện tại "Đang cân nhắc", Lần thứ 4, nằm trong **Đề xuất tạm dừng**.
- [ ] Mở **Lan Thử**: hạn liên hệ 03/11/2026 (xác nhận lịch tham quan ngày 04/11).
- [ ] Mở **Hoa Thử** → **Ghi nhận lần chăm sóc** → bấm Gọi điện, Đang cân nhắc, Quan tâm bình thường → Lưu. Đây là lần chăm sóc thứ 3 của Hoa Thử (chưa có mốc tiến triển nào), nên áp dụng L3: hạn liên hệ thành **hôm nay + 7 ngày**, và Hoa Thử rời màn hình Hôm nay. Trên Sheet, tab `Chăm sóc` có hàng mới với `Lần thứ` = 3.
- [ ] **Messenger**: có **Cúc Thử** và **Nga Thử** (có SĐT, chưa nhận); không có Lan Thử (đã có hồ sơ) và khách chưa rõ tên (chưa có SĐT). Bấm **Nhận lead này** cho Cúc Thử: hồ sơ mới xuất hiện trong **Của tôi**, Cúc Thử biến mất khỏi danh sách Messenger.
- [ ] **Theo sale**: Sale 6 đang giữ 1 lead; bạn (sale1) quá hạn 1 lead.
- [ ] Thêm một lần chăm sóc "Từ chối": app bắt chọn Lý do từ chối, không hỏi Mức quan tâm.

Nếu một bước sai, so công thức với thiet-ke.md mục 4. `quy_tac_nhac.py` tính được kết quả đúng cho mọi trường hợp để đối chiếu.

## Bước 11. Chuyển sang dữ liệu thật

Chỉ làm sau khi thử xong với 1 – 2 sale:

1. Mở file Sheet thật của bot. Sao chép 6 tab `Hồ sơ lead`, `Chăm sóc`, `Sale`, `Danh mục`, `Cấu hình`, `Thống kê` từ Sheet mẫu sang (chuột phải tên tab → **Sao chép vào** → chọn file thật). Đổi tên các tab sao chép cho bỏ chữ "Bản sao của". **Không** sao chép tab `Leads` mẫu: file thật đã có tab `Leads` của bot.
2. Trong file thật, xoá dữ liệu giả ở `Hồ sơ lead` và `Chăm sóc` (giữ hàng tiêu đề), điền email thật của 6 sale và chủ vào `Sale`.
3. Trong AppSheet: **Data** → từng bảng → **Source** → đổi sang file thật (cùng tên tab). Bấm **Regenerate structure** nếu được hỏi, kiểm tra lại kiểu cột.
4. **Không** đổi gì ở tab `Leads` của bot.
