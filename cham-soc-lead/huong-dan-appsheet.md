# Hướng dẫn dựng app chăm sóc lead bằng AppSheet

Làm trên máy tính, trình duyệt Chrome. Khoảng 2 – 3 giờ cho lần đầu. Mọi tên cột, công thức nằm trong [thiet-ke.md](thiet-ke.md); hướng dẫn này chỉ chỗ bấm.

Quy tắc nhắc hiện tại là **v2** (theo phản hồi của trường, 11/2026). Dựng mới: làm theo hướng dẫn này, các phần mới của v2 (bảng `Ngày nghỉ`, `Gửi thông tin`, 4 cột mới của `Chăm sóc`, danh sách Gửi ưu đãi / Gửi thông tin, nút Đã gửi thư mời, email 8h) làm theo bước 2, 6, 7, 8 của [nang-cap-quy-tac-v2.md](nang-cap-quy-tac-v2.md). App đã dựng theo bản cũ: chỉ cần làm theo [nang-cap-quy-tac-v2.md](nang-cap-quy-tac-v2.md). Sau đó làm tiếp **đợt 2** (tuổi bé, em nhỏ, sau nhập học: 3 cột mới của `Hồ sơ lead`, nút Tạo lead cho em, cột Việc cần làm) theo [nang-cap-quy-tac-dot-2.md](nang-cap-quy-tac-dot-2.md), cả khi dựng mới.

Tên nút trong AppSheet là tiếng Anh, ghi đúng như trên màn hình. Giao diện AppSheet thay đổi theo thời gian, nên vị trí nút có thể khác một chút.

## Bước 0. Chuẩn bị Sheet

1. Đăng nhập Google bằng **tài khoản Workspace của trường** (tài khoản có gói AppSheet Core).
2. Mở Sheet mẫu **"Casa – Chăm sóc lead (mẫu, dữ liệu giả)"**, chọn **Tệp → Tạo bản sao**, lưu vào Drive của tài khoản trường. App sẽ dựng trên bản sao này, để app và dữ liệu cùng thuộc tài khoản trường.
3. Để một mình bạn thử được cả màn hình của sale lẫn của chủ:
   - Dùng **Chỉnh sửa → Tìm và thay thế**, tick **Tìm kiếm trên mọi trang tính**, đổi `sale1@example.com` thành **email của bạn**.
   - Ở tab `Sale`, xoá hàng `chu@example.com`, rồi đổi **Vai trò** của hàng mang email của bạn thành `Chủ`.
   - Khi đó bạn là sale phụ trách lead Hoa Thử và Đào Thử, và thấy thêm các màn hình của chủ.

Sheet có 10 tab: `Tổng hợp lead` (bảng cho chủ, chỉ có công thức), `Hồ sơ lead`, `Chăm sóc`, `Sale`, `Danh mục`, `Cấu hình`, `Thống kê` (chỉ có công thức, tự tính theo tháng), `Leads` (bản giả của tab bot ghi), `Ngày nghỉ` (ngày lễ) và `Gửi thông tin` (các lần chủ gửi ưu đãi, thông tin).

## Bước 1. Tạo app

1. Vào **appsheet.com** → **Create** → **App** → **Start with existing data**.
2. Tên app: `Casa Chăm sóc lead`. Category: để mặc định. **Choose your data** → chọn bản sao Sheet ở bước 0.
3. AppSheet tự tạo app từ **tab đầu tiên** của Sheet. Trước khi tạo, kéo tab `Hồ sơ lead` lên đầu (bản sao có thể để `Tổng hợp lead` đứng đầu; tab đó chỉ có công thức, không dùng làm bảng). Chờ app dựng xong.

## Bước 2. Thêm các bảng

Vào **Data** (biểu tượng cơ sở dữ liệu bên trái) → **+** (Add new data) → chọn cùng file Sheet → chọn lần lượt tab `Chăm sóc`, `Sale`, `Danh mục`, `Cấu hình`, `Thống kê`, `Leads`, `Ngày nghỉ`, `Gửi thông tin` (hai bảng cuối chỉnh như bước 2 của `nang-cap-quy-tac-v2.md`).

- Bảng `Leads`: đổi tên hiển thị thành `Messenger`. Trong **Table settings**, mục **Are updates allowed?** chọn **Read-Only**. App không được sửa tab của bot.
- Bảng `Danh mục`, `Cấu hình`: chọn **Read-Only** (chủ sửa trực tiếp trên Sheet).
- Bảng `Cấu hình`: cột `Khóa` Type **Text**, tick **Key** và **Label**; `Giá trị` Type **Number**; bỏ Key/Label ở `Ý nghĩa`. AppSheet hay đoán `Khóa` là **Price** và đặt Key vào `Ý nghĩa`; khi đó mọi `LOOKUP(..., "Cấu hình", ...)` ra rỗng và hạn liên hệ tiếp chỉ bằng ngày gọi. Kiểm tra: Test `LOOKUP("L2", "Cấu hình", "Khóa", "Giá trị")` ra 3.
- Bảng `Thống kê`: **Read-Only**; cột `Mã` là **Key**; cột `Tháng` đổi Type thành **Text** (AppSheet đoán `2026-10` là ngày 01/10/2026, làm ô chọn tháng ở bước 4a không khớp); cột Tỷ lệ… chọn Type **Percent**.

## Bước 3. Cột của từng bảng

Trong **Data** → chọn bảng → **Columns**. Với mỗi cột, chỉnh **Type** và các ô khác đúng như bảng ở thiet-ke.md mục 3. Những chỗ hay sai:

**`Hồ sơ lead`**
- `Mã lead`: tick **Key**; **Initial value** `UNIQUEID()`; bỏ tick **Show**.
- `Ngày nhận`: Initial value `NOW()`; **Editable** tắt.
- `SĐT`: Type **Phone**.
- `Cơ sở`, `Nguồn`: Type **Enum** (`Nguồn` tick **Require**, báo cáo theo nguồn cần cột này); trong **Valid If** nhập `SELECT(Danh mục[Giá trị], [Loại] = "Cơ sở")` (với Nguồn đổi chữ "Cơ sở" thành "Nguồn").
- `PH quan tâm`: Type **EnumList**, Valid If `SELECT(Danh mục[Giá trị], [Loại] = "Mối quan tâm")`.
- `Sale phụ trách`: Type **Ref**, Source table `Sale`; Initial value `USEREMAIL()`; **Editable If** là công thức "ai là chủ" ở thiet-ke.md mục 4.
- `Chất lượng lead`: Enum `Tốt`, `Trung bình`, `Kém`.
- `Lý do chất lượng`: Enum, Valid If `SELECT(Danh mục[Giá trị], [Loại] = "Lý do chất lượng")`; **Show If** `IN([Chất lượng lead], LIST("Trung bình", "Kém"))`.
- `Customer ID`: bỏ tick **Show**.
- `Tên phụ huynh`, `Tên bé`, `SĐT`: tick **Search** (để ô tìm kiếm tìm được theo các cột này). Bỏ tick Search ở các cột còn lại cho kết quả gọn.
- `Tạm dừng`: Type **Yes/No**; Editable If là công thức "ai là chủ"; **Initial value** `FALSE`; **không** tick Require (sale không sửa được ô này, nếu bắt buộc thì sale không lưu được lead mới).
- `Chủ nhắc lúc`: Type **DateTime**; **Initial value để trống** (nếu AppSheet tự điền `NOW()`, mọi lead mới đều bị coi là chủ vừa nhắc và gửi email nhắc nhầm); **Editable** tắt (chỉ nút Nhắc sale ghi vào); Show If `ISNOTBLANK([Chủ nhắc lúc])`; Display name `Chủ đã nhắc lúc`.

**`Chăm sóc`**
- `Mã`: Key, Initial value `UNIQUEID()`, ẩn.
- `Mã lead`: Type **Ref**, Source table `Hồ sơ lead`, tick **Is a part of**.
- `Thời gian`: Initial value `NOW()`, Editable tắt. `Sale`: Type Ref → `Sale`, Initial value `USEREMAIL()`, Editable tắt.
- `Phương thức`, `Tình trạng`, `Mức quan tâm`: Type **Enum**, nhập các giá trị như thiet-ke.md; **Input mode** chọn **Buttons**; tick **Require**.
- `Mức quan tâm`: Show If `NOT(IN([Tình trạng], LIST("Từ chối", "Chưa liên lạc được")))`; **Required If** dùng cùng công thức (bỏ tick Require).
- `Lý do từ chối`: Enum, Valid If loại "Lý do từ chối"; Show If và Required If: `[Tình trạng] = "Từ chối"`.
- `Ngày hẹn gọi lại`: Type Date; **Initial value để trống** (AppSheet hay tự điền hôm nay, làm hạn liên hệ tiếp thành hôm nay; `Ngày hẹn tham quan` cũng vậy); Show If `NOT(IN([Tình trạng], LIST("Từ chối", "Đã nhập học")))`; Required If `[Tình trạng] = "Yêu cầu gọi lại sau"`.
- `Ngày hẹn tham quan`: Type Date; Show If và Required If `[Tình trạng] = "Đã hẹn tham quan / học thử"`.
- `Lần thứ`, `Hạn liên hệ tiếp`: điền **App formula** từ thiet-ke.md mục 4; bỏ tick Show trong form (vẫn hiện ở trang chi tiết nếu muốn).
- **Thêm cột ảo** `Mốc gần nhất` (nút **Add virtual column**), Type Ref → `Chăm sóc`, công thức ở thiet-ke.md. Làm cột này **trước** khi nhập công thức `Lần thứ`.

**`Sale`**: `Email` là Key, Type Email (bỏ Key ở `_RowNumber`); `Tên` là Label; `Vai trò` Enum `Sale`, `Chủ`; `Đang làm` Yes/No.

**`Messenger`** (tab `Leads`): Key là `Customer ID` (AppSheet hay tự chọn `Thời gian`, phải đổi); Label là `Tên Facebook`; `SĐT` đổi Type thành **Phone** (AppSheet đoán Number, làm mất số 0 đầu); bỏ Require ở `Thời gian`, `SĐT`. Nếu AppSheet báo tên cột có dấu `/` (như `Cơ sở/hệ`) không hợp lệ, nó sẽ tự đổi tên hiển thị; ghi lại tên mới để dùng ở bước 6.

Mỗi bảng chỉ để **một** cột tick Label (AppSheet có khi tick sẵn nhiều cột). Ngày trong app hiển thị theo ngôn ngữ của trình duyệt hoặc điện thoại (máy tiếng Anh hiện 10/19/2026, máy tiếng Việt hiện 19/10/2026); không có ô chỉnh trong AppSheet. Đừng đổi **Data locale** của bảng nếu ngày đang đọc đúng.

Sau đó thêm các **cột ảo** của `Hồ sơ lead` và `Sale` đúng như bảng ở thiet-ke.md mục 4. Thêm theo thứ tự trong bảng, vì cột sau dùng cột trước.

## Bước 4a. Nút chọn tháng và cơ sở cho chủ (User settings)

**Settings** → **User settings** (cài đặt riêng của từng người dùng):

- Bật một ô tùy chỉnh, đặt tên `Tháng`: Type **Enum**; **Valid If** `SORT(UNIQUE(Thống kê[Tháng]), TRUE)`; **Initial value** `TEXT(TODAY(), "YYYY-MM")`.
- Ô thứ hai `Cơ sở`: Type **Enum**; Valid If `UNIQUE(Thống kê[Cơ sở])`; Initial value `"Tất cả"`.
- Ô thứ ba `Sale`: Type **Enum**; Valid If `LIST("Tất cả") + SELECT(Sale[Tên], [Vai trò] = "Sale")`; Initial value `"Tất cả"`.

Chủ đổi tháng, cơ sở, sale trong menu **Settings** của app; màn **Tất cả lead** và các màn báo cáo đổi theo. (Sale cũng thấy các ô này nhưng chỉ có dữ liệu của mình, nên không ảnh hưởng.)

## Bước 4. Lát cắt dữ liệu (Slices)

**Data** → rê chuột lên tên bảng → **+** → **Create a new slice** (bỏ qua các gợi ý có sẵn).

Ô **Row filter condition** mặc định là ô "Describe the expression in your own words" (mô tả bằng lời cho AI). Dán công thức thẳng vào đó thì **không được lưu**. Bấm vào ô, gõ dấu `=` trước rồi dán công thức ngay sau; ô chuyển sang chữ kiểu code là đúng. **Preview data** ở góc trên phải slice chỉ đọc dữ liệu thô trong Sheet, không tính cột ảo: slice lọc theo cột ảo (Bỏ quên, Rất quan tâm chưa chốt…) sẽ ra 0 dòng ở đó dù đúng. Kiểm tra các slice này bằng nút **Test** trong Expression Assistant, hoặc trong app sau bước 5.

| Slice | Bảng | Điều kiện (Row filter condition) |
|---|---|---|
| Hôm nay của tôi | Hồ sơ lead | `AND([Sale phụ trách] = USEREMAIL(), IN([Mức khẩn], LIST("Quá hạn", "Hôm nay")))` |
| Lead của tôi | Hồ sơ lead | `[Sale phụ trách] = USEREMAIL()` |
| Bỏ quên | Hồ sơ lead | `[Bỏ quên]` |
| Rất quan tâm chưa chốt | Hồ sơ lead | `AND([Mức quan tâm hiện tại] = "Rất quan tâm", NOT([Đã kết thúc]), [Tình trạng hiện tại] <> "Đã đặt cọc")` |
| Cần gửi ưu đãi | Hồ sơ lead | `[Nên gửi ưu đãi]` |
| Cần gửi thông tin | Hồ sơ lead | `[Nên gửi thông tin]` (không đặt tên `Gửi thông tin`: trùng tên bảng) |
| Messenger chưa nhận | Messenger | `AND(ISNOTBLANK([SĐT]), NOT(IN([Customer ID], Hồ sơ lead[Customer ID])), [Giai đoạn] <> "Không quan tâm")` |
| Tháng đang chọn | Thống kê | `AND([Tháng] = USERSETTINGS("Tháng"), [Cơ sở] = USERSETTINGS("Cơ sở"))` |
| Lead theo bộ lọc | Hồ sơ lead | `AND(OR(USERSETTINGS("Cơ sở") = "Tất cả", [Cơ sở] = USERSETTINGS("Cơ sở")), OR(USERSETTINGS("Sale") = "Tất cả", [Sale phụ trách].[Tên] = USERSETTINGS("Sale")))` |
| Lead tháng đang chọn | Hồ sơ lead | `AND(TEXT([Ngày nhận], "YYYY-MM") = USERSETTINGS("Tháng"), OR(USERSETTINGS("Cơ sở") = "Tất cả", [Cơ sở] = USERSETTINGS("Cơ sở")))` |

## Bước 5. Màn hình (Views)

Vào **Views** (biểu tượng điện thoại bên trái) → **+ New view**. Mỗi view chọn **For this data** là slice hoặc bảng, **View type**, và **Position**.

| View | Dữ liệu | Kiểu | Vị trí | Ghi chú |
|---|---|---|---|---|
| Hôm nay | Hôm nay của tôi | Deck | first | Sort by `Hạn liên hệ` tăng dần. Hai màn deck của sale: Primary header `Tên phụ huynh`, Secondary header `Mức khẩn`, Summary column `Lần cuối tóm tắt`. Slice của sale bỏ **Deletes** ở Update mode. Đặt làm **Starting view** (Settings → Views → General) |
| Của tôi | Lead của tôi | Deck | next | Group by cột ảo `Nhóm` (Hồ sơ lead, Text: `IFS([Mức khẩn] = "Quá hạn", "1 · Quá hạn", [Mức khẩn] = "Hôm nay", "2 · Hôm nay", AND([Mức khẩn] = "Sắp tới", [Giai đoạn] = "Đang chăm sóc"), "3 · Sắp tới", TRUE, CONCATENATE("4 · ", [Giai đoạn]))`) để Quá hạn lên đầu. Ô tìm kiếm có sẵn ở góc trên: phụ huynh tự gọi tới thì sale gõ tên hoặc vài số cuối SĐT |
| Messenger | Messenger chưa nhận | Table | menu | **Chỉ chủ** (Show if như các view của chủ) |
| Theo sale | Sale | Table | menu | Hiện các cột ảo Đang giữ, Liên hệ hôm nay, Quá hạn, Tỷ lệ chốt, Số lần chăm sóc |
| Bỏ quên | Bỏ quên | Table | menu | **Group by** `Sale phụ trách`; Sort by `Số ngày quá hạn` giảm dần; cột hiện: Tên phụ huynh, Tên bé, Cơ sở, Số ngày quá hạn, Ngày không cập nhật, Lần cuối tóm tắt, Chủ nhắc lúc |
| Rất quan tâm chưa chốt | Rất quan tâm chưa chốt | Table | menu | Group by `Sale phụ trách`; cột hiện: Tên phụ huynh, Tên bé, Cơ sở, Tình trạng hiện tại, Hạn liên hệ, Ngày không cập nhật, Lần cuối tóm tắt, Chủ nhắc lúc |
| Gửi ưu đãi | Cần gửi ưu đãi | Table | menu | Xem bước 6 của `nang-cap-quy-tac-v2.md` |
| Gửi thông tin | Cần gửi thông tin | Table | menu | Xem bước 6 của `nang-cap-quy-tac-v2.md` |
| Tất cả lead | Lead theo bộ lọc | Deck | menu | **Chỉ chủ** (Show if là công thức "ai là chủ"). Ô tìm kiếm có sẵn ở góc trên; lọc Cơ sở, Sale bằng User settings (bước 4a). Hiện Tên phụ huynh, Tên bé, Cơ sở, Sale phụ trách, Mức khẩn, Tình trạng hiện tại. Bấm vào mở trang chi tiết có dòng thời gian tư vấn (xem dưới) |
| Báo cáo tháng | Tháng đang chọn | Detail | menu | Hiện Tháng, Cơ sở, Lead mới, Lead mới tháng trước, rồi từng bước kèm tỷ lệ. Thêm cột ảo nếu muốn % so với bước trước, vd `IF([Đã tư vấn] = 0, 0, [Đã tham quan] / [Đã tư vấn])` |
| Lead của tháng | Lead tháng đang chọn | Table | menu | Danh sách lead của tháng và cơ sở đang chọn, cột Tình trạng hiện tại, Nguồn, Sale phụ trách |
| Các tháng | Thống kê | Table | menu | Group by `Tháng`; so sánh các tháng, các cơ sở |
| Lead theo tháng | Thống kê | Chart (Column) | menu | Trục ngang `Tháng`, giá trị `Lead mới`, chỉ dòng "Tất cả" (dùng một slice `[Cơ sở] = "Tất cả"`) |
| Theo nguồn | Hồ sơ lead | Chart | menu | Cột `Nguồn`; thêm một chart nữa cho `Chất lượng lead` |
| Lý do từ chối | Chăm sóc | Chart | menu | Cột `Lý do từ chối` |

Với 6 view cuối (của chủ), trong mục **Display** → **Show if** nhập công thức "ai là chủ" (thiet-ke.md mục 4).

**Mọi màn mở chung một trang chi tiết.** Mỗi slice có trang chi tiết riêng do AppSheet tự tạo (`Lead của tôi_Detail`, `Lead theo bộ lọc_Detail`…), nên chỉnh `Hồ sơ lead_Detail` không đủ. Tạo action **Mở hồ sơ** (bảng `Hồ sơ lead`, Do this **App: go to another view within this app**, Target `LINKTOROW([Mã lead], "Hồ sơ lead_Detail")`, Position **Hide**), rồi ở mỗi view danh sách lead (Hôm nay, Của tôi, Tất cả lead, Bỏ quên, Rất quan tâm chưa chốt, Gửi ưu đãi, Gửi thông tin, Lead của tháng) đặt **Behavior → Row Selected** = `Mở hồ sơ`.

**Form `Chăm sóc`** (view `Chăm sóc_Form` AppSheet tự tạo): sắp thứ tự cột: Phương thức, Tình trạng, Mức quan tâm, Phản hồi, Lý do từ chối, Ngày hẹn gọi lại, Ngày hẹn tham quan. Ẩn Mã, Mã lead, Thời gian, Sale, Lần thứ, Hạn liên hệ tiếp.

**Trang chi tiết `Hồ sơ lead`**: để `Tên phụ huynh`, `SĐT`, `Mức khẩn`, `Hạn liên hệ`, `Tình trạng hiện tại`, `Sale phụ trách`, `Chủ đã nhắc lúc` lên đầu. Danh sách lần chăm sóc (`Related Chăm sócs`) hiện ở cuối làm **dòng thời gian tư vấn**, kèm nút **Add** để ghi lần mới. Chỉnh view `Chăm sóc_Inline` (AppSheet tự tạo): Sort by `Thời gian` **giảm dần** (mới nhất trên cùng); cột hiện: Thời gian, Sale, Phương thức, Tình trạng, Mức quan tâm, Phản hồi.

## Bước 6. Nút bấm (Actions)

Vào **Actions** (biểu tượng tia chớp) → **+ New action**:

1. **Mở Zalo** (bảng `Hồ sơ lead`): Do this **External: go to a website**; Target `CONCATENATE("https://zalo.me/", SUBSTITUTE([SĐT], " ", ""))`; Position **Prominent**.
2. **Ghi nhận lần chăm sóc** (bảng `Hồ sơ lead`): Do this **App: go to another view within this app**; Target `LINKTOFORM("Chăm sóc_Form", "Mã lead", [Mã lead])`; Position **Prominent**.
3. **Giao lead** (bảng `Messenger`, chỉ chủ): Do this **App: go to another view within this app**; Target:

   ```
   LINKTOFORM("Hồ sơ lead_Form",
     "Tên phụ huynh", [Tên Facebook], "Tên bé", [Tên bé], "Tuổi bé", [Tuổi bé], "SĐT", [SĐT],
     "Nguồn", "Facebook Messenger", "Chiến dịch", [Quảng cáo], "Customer ID", [Customer ID],
     "Ghi chú", CONCATENATE("Bot ghi cơ sở: ", [Cơ sở/hệ], ". Tin cuối: ", [Tin cuối của phụ huynh]))
   ```

   (đổi tên cột nếu AppSheet đã đổi ở bước 3). Form mở ra đã điền sẵn; chủ chọn **Sale phụ trách** và **Cơ sở** rồi lưu. Only if `AND(<công thức ai là chủ>, NOT(IN([Customer ID], Hồ sơ lead[Customer ID])))`. Position **Prominent**.

4. **Nhắc sale** (bảng `Hồ sơ lead`): Do this **Data: set the values of some columns in this row**; đặt `Chủ nhắc lúc` = `NOW()`; Position **Inline** (gắn vào cột Tên phụ huynh) hoặc **Prominent**; **Only if** là công thức "ai là chủ". Bật **Needs confirmation**, nội dung `Gửi email nhắc sale phụ trách lead này?`.

AppSheet tự có nút Gọi và SMS cho cột kiểu Phone.

## Bước 7. Tô màu (Format rules)

**Views** → **Format rules** → **+ New format rule**, bảng `Hồ sơ lead`:

- `[Mức khẩn] = "Quá hạn"`: chữ đỏ, đậm, biểu tượng cảnh báo.
- `[Mức khẩn] = "Hôm nay"`: chữ cam.
- `[Giai đoạn] = "Dài hạn"`: chữ xanh dương (xám nhìn gần như đen).

## Bước 8. Email nhắc mỗi sáng

**Automation** → **+ New bot** → tên `Nhắc việc 8h`:

1. **Event**: **Schedule**, **Weekly**, chọn thứ 2 đến thứ 6, lúc **08:00**, múi giờ **(GMT+07:00)**. **For each row in table** `Sale`, điều kiện `AND([Đang làm], [Vai trò] = "Sale")`.
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

Bật **Bypass Security Filters?** ở mọi bot (Nhắc việc, Chủ nhắc sale, Lead trùng, Được giao lead): bot cần thấy lead của mọi sale, không bị bộ lọc ở bước 9 che.

**Thử bot mà không làm phiền sale:** chừng nào app chưa **Deploy** (bước 11), AppSheet gửi mọi email về người tạo app, kèm dòng "App version … is not deployed". Để ô To đúng công thức (`[Email]`), bấm **Run** ở trang bot, rồi đọc thư trong hộp thư của người tạo: mỗi sale một thư.

### Email khi chủ nhắc sale

**Automation** → **+ New bot** → tên `Chủ nhắc sale`:

1. **Event**: **Data change**, bảng `Hồ sơ lead`, loại **Updates only**; **Condition** `[_THISROW_BEFORE].[Chủ nhắc lúc] <> [_THISROW_AFTER].[Chủ nhắc lúc]`.
2. **Process** → **Send an email**: To `[Sale phụ trách].[Email]`; Subject `Chủ nhắc: liên hệ <<[Tên phụ huynh]>>`; Body:

```
Chào <<[Sale phụ trách].[Tên]>>,

Chủ nhắc bạn liên hệ phụ huynh <<[Tên phụ huynh]>> (bé <<[Tên bé]>>, cơ sở <<[Cơ sở]>>).
Tình trạng: <<[Mức khẩn]>>. Lần cuối: <<[Lần cuối tóm tắt]>>.

Mở lead trong app: <<CONCATENATE("https://www.appsheet.com/start/<MÃ APP>", LINKTOROW([Mã lead], "Hồ sơ lead_Detail"))>>
Sau khi liên hệ, nhớ bấm "Ghi nhận lần chăm sóc".
```

Trong email, `LINKTOROW` chỉ cho nửa sau của link (`#control=…&row=…`), bấm không mở được. Ghép phía trước địa chỉ app `https://www.appsheet.com/start/<MÃ APP>` (mở app trong tab riêng, lấy đoạn trên thanh địa chỉ trước dấu `?` hoặc `#`).

### Email báo chủ khi có lead trùng, báo sale khi được giao lead

**Automation** → **+ New bot** → `Lead trùng`: Event **Data change**, bảng `Hồ sơ lead`, **Adds only**; Condition `COUNT(SELECT(Hồ sơ lead[Mã lead], AND([SĐT] = [_THISROW].[SĐT], [Mã lead] <> [_THISROW].[Mã lead]))) > 0`. Task **Send an email** tới các email có Vai trò "Chủ": To `SELECT(Sale[Email], [Vai trò] = "Chủ")`; Subject `Lead trùng SĐT: <<[Tên phụ huynh]>>`; Body nêu lead mới (tên, sale phụ trách) và các lead cũ cùng SĐT: `<<Start: SELECT(Hồ sơ lead[Mã lead], AND([SĐT] = [_THISROW].[SĐT], [Mã lead] <> [_THISROW].[Mã lead]))>><<[Tên phụ huynh]>> · <<[Sale phụ trách].[Tên]>> · <<[Tình trạng hiện tại]>><<End>>`.

**Automation** → **+ New bot** → `Được giao lead`: Event **Data change**, bảng `Hồ sơ lead`, **Adds and updates**; Condition `AND(LOOKUP(USEREMAIL(), "Sale", "Email", "Vai trò") = "Chủ", [Sale phụ trách] <> USEREMAIL(), OR(ISBLANK([_THISROW_BEFORE].[Mã lead]), [_THISROW_BEFORE].[Sale phụ trách] <> [_THISROW_AFTER].[Sale phụ trách]))` (người làm thay đổi là chủ, không giao cho chính mình, lead mới hoặc vừa đổi sale). Task **Send an email** To `[Sale phụ trách].[Email]`, Subject `Bạn được giao lead mới: <<[Tên phụ huynh]>>`, kèm link ghép địa chỉ app như bot Chủ nhắc sale.

Hai bot này chạy trên máy chủ của AppSheet; bật **Bypass Security Filters?** để bot `Lead trùng` thấy lead của mọi sale. Đã thử trên Sheet mẫu: cả 4 bot gửi đúng nội dung. Bot `Lead trùng` so SĐT y nguyên chữ: `0900 000 604` hay `+84900000604` không được coi là trùng với `0900000604`.

## Bước 9. Người dùng và quyền

1. **Security** → **Require sign-in**: bật, provider Google, **Allow all signed-in users** tắt (chỉ người trong danh sách Manage users). **Domain Authentication** để **tắt**: mục này cần gói Enterprise, gói Core của trường không dùng được; danh sách người dùng đã đủ chặn người lạ.
2. Chỉ cho email trong tab `Sale` dùng: ở **Settings → Users** (hoặc nút **Share**), thêm 6 email sale và email chủ.
3. **Sale chỉ thấy lead của mình**: **Security** → **Security filters**, đặt cho từng bảng (với "ai là chủ" là công thức ở thiet-ke.md mục 4):
   - `Hồ sơ lead`: `OR(<ai là chủ>, [Sale phụ trách] = USEREMAIL())`
   - `Chăm sóc`: `OR(<ai là chủ>, [Mã lead].[Sale phụ trách] = USEREMAIL())`
   - `Messenger` (tab Leads của bot) và `Thống kê`: `<ai là chủ>` (sale không tải về)
   - `Sale`, `Danh mục`, `Cấu hình`: không đặt (ai cũng cần).

   Security filter chặn cả dữ liệu tải về máy, không chỉ ẩn trên màn hình. Lưu ý: filter của `Chăm sóc` tham chiếu bảng khác, nên `Hồ sơ lead` phải được tải trước; AppSheet tự lo việc này.
4. Bảng `Chăm sóc` → **Are updates allowed?** để **Adds and Updates** (không cho xoá). Cột `Phản hồi`, `Tình trạng`… có **Editable If** `OR([Sale] = USEREMAIL(), <công thức ai là chủ>)`.
5. Bảng `Hồ sơ lead` → **Adds and Updates** (không cho xoá; lead không còn theo thì chủ bật Tạm dừng).

## Bước 10. Thử với dữ liệu mẫu

Mở app (nút **Preview** bên phải, hoặc mở link app trên điện thoại). Với Sheet mẫu tạo ngày 02/11/2026 và `sale1@example.com` đã đổi thành email của bạn (bước 0), kết quả đúng là:

- [ ] Màn hình **Hôm nay** có **Hoa Thử** (hẹn gọi lại hôm nay) và **Đào Thử** (quá hạn, chữ đỏ).
- [ ] Với vai trò **Chủ**: **Tất cả lead** có 8 lead; gõ "Minh" ra Minh Thử, gõ "0604" ra Hằng Thử.
- [ ] Thử vai trò **Sale**: ở tab `Sale`, tạm đổi Vai trò của email bạn thành `Sale`, mở lại app (Sync). **Của tôi** chỉ còn Hoa Thử và Đào Thử; menu không còn Tất cả lead, Messenger, Báo cáo. Gõ "0604" vào ô tìm: không ra gì (Hằng Thử là lead của Sale 4). Thêm lead mới với SĐT `0900000604`: lưu được, và email chủ (thư của bạn khi đổi lại Vai trò Chủ, hoặc email chủ thật) nhận "Lead trùng SĐT". Đổi Vai trò về `Chủ` sau khi thử.
- [ ] Settings chọn Tháng **2026-10**, Cơ sở **Tất cả** → **Báo cáo tháng**: Lead mới 7, Đã tư vấn 7, Đã tham quan 1, Đã đặt cọc 1, Đã nhập học 0, Tỷ lệ tham quan 14%. Đổi Cơ sở sang **Mỹ Đình**: 2, 2, 1, 1, 0. Chọn Tháng **2026-11**, Tất cả: Lead mới 1, Lead mới tháng trước 7.
- [ ] Mở **Thu Thử**: Tình trạng hiện tại "Đang cân nhắc", Lần thứ 4, Giai đoạn **Dài hạn**, nằm trong màn **Gửi thông tin** (và Gửi ưu đãi).
- [ ] Mở **Lan Thử**: hạn liên hệ 03/11/2026 (xác nhận lịch tham quan ngày 04/11).
- [ ] Mở **Hoa Thử** → **Ghi nhận lần chăm sóc** → bấm Gọi điện, Đang cân nhắc, Quan tâm bình thường → Lưu. Hoa Thử đã có 1 lần "Chưa liên lạc được" (không tính) và 1 lần liên lạc được, nên lần này là L2: hạn liên hệ thành **hôm nay + 3 ngày** (dời qua thứ 7, Chủ nhật), và Hoa Thử rời màn hình Hôm nay. Trên Sheet, tab `Chăm sóc` có hàng mới với `Lần thứ` = 2.
- [ ] **Messenger** (chủ): có **Cúc Thử** và **Nga Thử** (có SĐT, chưa nhận); không có Lan Thử (đã có hồ sơ) và khách chưa rõ tên (chưa có SĐT). Bấm **Giao lead** cho Cúc Thử: form mở ra đã điền tên, tuổi, SĐT; chọn Sale phụ trách là Sale 3, lưu. Cúc Thử biến mất khỏi danh sách Messenger và có trong Tất cả lead với sale là Sale 3.
- [ ] **Theo sale**: Sale 6 đang giữ 0 lead (Thu Thử đã sang Dài hạn); bạn (sale1) đang giữ 2, quá hạn 1 lead.
- [ ] Thêm một lần chăm sóc "Từ chối": app bắt chọn Lý do từ chối, không hỏi Mức quan tâm.
- [ ] **Tất cả lead** với bộ lọc: Settings chọn Cơ sở **Mỹ Đình**, Sale **Tất cả** → ra Quang Thử, Hằng Thử, Lan Thử. Bấm Lan Thử → dòng thời gian 3 lần: 27/10 Đã hẹn tham quan (trên cùng), 24/10 Đang cân nhắc, 23/10 Đang cân nhắc. Chọn thêm Sale **Sale 1** → danh sách trống.
- [ ] Tab **Tổng hợp lead** trên Sheet: chọn B1 = Mỹ Đình ra đúng 3 lead trên; cột Quá trình tư vấn của Lan Thử có 3 dòng.
- [ ] **Bỏ quên** (màn của chủ): có đúng 2 lead đang chăm sóc mà quá hạn: Đào Thử (của bạn, quá hạn 14 ngày) và Minh Thử (Sale 5, quá hạn 3 ngày), nhóm theo sale. Thu Thử không có (đã sang Dài hạn); Lan Thử, Hoa Thử, Hằng Thử, Quang Thử không có (hạn chưa qua). Mỗi dòng có "Lần cuối" như "29/10 · Đang cân nhắc · Hỏi thực đơn…". Bấm **Nhắc sale** ở Đào Thử: cột Chủ nhắc lúc có giờ hiện tại, và email của bạn nhận được thư "Chủ nhắc: liên hệ Đào Thử".
- [ ] Các ca của quy tắc v2 (dời ngày nghỉ, chưa liên lạc 3 lần, đặt cọc và thư mời, từ chối theo lý do, danh sách gửi): bước 9 của `nang-cap-quy-tac-v2.md`.

Nếu một bước sai, so công thức với thiet-ke.md mục 4. `quy_tac_nhac.py` tính được kết quả đúng cho mọi trường hợp để đối chiếu.

## Bước 11. Chuyển sang dữ liệu thật

Chỉ làm sau khi thử xong với 1 – 2 sale:

1. Mở file Sheet thật của bot. Sao chép 9 tab `Tổng hợp lead`, `Hồ sơ lead`, `Chăm sóc`, `Sale`, `Danh mục`, `Cấu hình`, `Thống kê`, `Ngày nghỉ`, `Gửi thông tin` từ Sheet mẫu sang (chuột phải tên tab → **Sao chép vào** → chọn file thật). Đổi tên các tab sao chép cho bỏ chữ "Bản sao của". **Không** sao chép tab `Leads` mẫu: file thật đã có tab `Leads` của bot.
2. Trong file thật, xoá dữ liệu giả ở `Hồ sơ lead` và `Chăm sóc` (giữ hàng tiêu đề), điền email thật của 6 sale và chủ vào `Sale`.
3. Trong AppSheet: **Data** → từng bảng → **Source** → đổi sang file thật (cùng tên tab). Chỉ bấm **Regenerate structure** khi AppSheet bắt buộc; nếu đã bấm, kiểm tra lại những chỗ AppSheet hay đoán sai: `Cấu hình`.`Khóa` là Text + Key; `Thống kê`.`Tháng` là Text, `Mã` là Key; `Leads`: Key `Customer ID`, `SĐT` kiểu Phone; mọi bảng chỉ một cột Label; Initial value của `Chủ nhắc lúc`, `Ngày hẹn gọi lại`, `Ngày hẹn tham quan` trống. Mở tab `Thống kê`, `Tổng hợp lead` trên file thật xem công thức không báo `#REF!` (tên tab phải đúng như cũ, không còn chữ "Bản sao của").
4. **Không** đổi gì ở tab `Leads` của bot, và không gõ tay lead nào vào tab đó. Lead từ Zalo, hotline, giới thiệu, đến trực tiếp… thêm bằng nút **Thêm lead** trong app (hoặc gõ vào tab `Hồ sơ lead`, xem thiet-ke.md mục 2).
5. **Security → Require sign-in → Manage users**: thêm email thật của sale và chủ. **Không** chia sẻ file Sheet cho sale (Access mode của security filter để **as app creator**: app đọc Sheet bằng quyền người tạo, sale không cần quyền mở file).
6. **Manage → Deploy**: chạy **Deployment check**, rồi chuyển app sang trạng thái **Deployed**. Trước khi deploy, mọi email của bot chỉ gửi về người tạo app; sau khi deploy mới tới sale.
7. Gửi link app cho sale (trên điện thoại: cài app **AppSheet**, đăng nhập bằng email đã thêm). Link mở lead trong email của bot vẫn đúng vì mã app không đổi.
