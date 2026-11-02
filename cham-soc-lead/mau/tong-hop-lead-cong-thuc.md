# Công thức tab `Tổng hợp lead`

Tab cho chủ xem **mọi lead đang có** trên máy tính, lọc theo cơ sở, sale, tình trạng, mức khẩn; cột cuối là toàn bộ quá trình tư vấn của từng lead. Tab chỉ có công thức, không gõ dữ liệu vào.

Cách dễ nhất để có tab này trong file thật: **sao chép tab từ Sheet mẫu** (chuột phải tên tab → Sao chép vào), không phải dán lại. Công thức viết theo kiểu số tiếng Anh (dấu `,`); xem lưu ý ở `thong-ke-cong-thuc.md` nếu phải dán tay vào file đặt ngôn ngữ Việt Nam.

## Bố cục

- Hàng 1: `A1` "Cơ sở", `B1` ô chọn; `C1` "Sale", `D1` ô chọn; `E1` "Tình trạng", `F1` ô chọn; `G1` "Mức khẩn", `H1` ô chọn. Giá trị mặc định là `Tất cả`.
- Hàng 2: một dòng hướng dẫn.
- Hàng 3: tiêu đề: Mã lead, Ngày nhận, Phụ huynh, Bé, Cơ sở, Nguồn, Sale, Tình trạng hiện tại, Mức quan tâm, Lần cuối, Hạn liên hệ, Mức khẩn, Số lần chăm sóc, Quá trình tư vấn.
- `A4`: công thức chính (cả bảng tự trải ra), xếp lead mới nhận lên đầu.
- `T1:W1`: danh sách cho 4 ô chọn (cột T – W ẩn). Ô chọn dùng **Dữ liệu → Xác thực dữ liệu → Thả xuống (từ một dải ô)**: `B1` ← `T1:T20`, `D1` ← `U1:U30`, `F1` ← `V1:V12`, `H1` ← `W1:W8`.
- Cột Ngày nhận, Hạn liên hệ định dạng ngày `dd/mm/yyyy`. Cột Mức khẩn tô đỏ "Quá hạn", cam "Hôm nay" (định dạng có điều kiện).

## Công thức

`A4`:

```
=LET(hs,FILTER('Hồ sơ lead'!A2:Q,'Hồ sơ lead'!A2:A<>""),ma,CHOOSECOLS(hs,1),ngay,CHOOSECOLS(hs,2),ph,CHOOSECOLS(hs,3),be,ARRAYFORMULA(CHOOSECOLS(hs,4)&IF(CHOOSECOLS(hs,5)="","",", "&CHOOSECOLS(hs,5))),coso,CHOOSECOLS(hs,7),nguon,CHOOSECOLS(hs,8),email,CHOOSECOLS(hs,11),dung,CHOOSECOLS(hs,16),sale,MAP(email,LAMBDA(e,IFERROR(XLOOKUP(e,Sale!A2:A,Sale!B2:B),e))),lg,FILTER({'Chăm sóc'!B2:B,'Chăm sóc'!C2:C,'Chăm sóc'!D2:D,'Chăm sóc'!E2:E,'Chăm sóc'!F2:F,'Chăm sóc'!G2:G,'Chăm sóc'!H2:H,'Chăm sóc'!M2:M},'Chăm sóc'!B2:B<>""),g,LAMBDA(m,k,IFERROR(INDEX(SORT(FILTER(lg,CHOOSECOLS(lg,1)=m),2,FALSE),1,k),"")),tt,MAP(ma,LAMBDA(m,IF(g(m,5)="","Mới",g(m,5)))),muc,MAP(ma,LAMBDA(m,g(m,6))),lc,MAP(ma,LAMBDA(m,IF(g(m,2)="","Chưa liên hệ",TEXT(g(m,2),"dd/mm")&" · "&g(m,5)&IF(g(m,7)="",""," · "&g(m,7))))),han,MAP(ma,ngay,dung,LAMBDA(m,d,p,IF(p,"",IF(g(m,2)="",INT(d),g(m,8))))),khan,MAP(han,dung,LAMBDA(h,p,IF(p,"Tạm dừng",IF(ISNUMBER(h),IF(h<TODAY(),"Quá hạn",IF(h=TODAY(),"Hôm nay","Sắp tới")),"Không nhắc")))),solan,MAP(ma,LAMBDA(m,COUNTIF(CHOOSECOLS(lg,1),m))),qt,MAP(ma,LAMBDA(m,IFERROR(TEXTJOIN(CHAR(10),TRUE,BYROW(SORT(FILTER(lg,CHOOSECOLS(lg,1)=m),2,TRUE),LAMBDA(r,TEXT(INDEX(r,1,2),"dd/mm")&" · "&IFERROR(XLOOKUP(INDEX(r,1,3),Sale!A2:A,Sale!B2:B),INDEX(r,1,3))&" · "&INDEX(r,1,4)&" · "&INDEX(r,1,5)&IF(INDEX(r,1,7)="",""," · "&INDEX(r,1,7))))),""))),tbl,HSTACK(ma,ngay,ph,be,coso,nguon,sale,tt,muc,lc,han,khan,solan,qt),loc,FILTER(tbl,($B$1="Tất cả")+(coso=$B$1),($D$1="Tất cả")+(sale=$D$1),($F$1="Tất cả")+(tt=$F$1),($H$1="Tất cả")+(khan=$H$1)),IF(ISERROR(INDEX(loc,1,1)),"Không có lead nào khớp bộ lọc",SORT(loc,2,FALSE)))
```

`T1` (danh sách cơ sở): `=ARRAYFORMULA({"Tất cả";FILTER('Danh mục'!B2:B,'Danh mục'!A2:A="Cơ sở")})`

`U1` (danh sách sale, theo tên): `=ARRAYFORMULA({"Tất cả";FILTER(Sale!B2:B,Sale!B2:B<>"")})`

`V1` (danh sách tình trạng): `={"Tất cả";"Mới";"Chưa liên lạc được";"Đang cân nhắc";"Yêu cầu gọi lại sau";"Đã hẹn tham quan / học thử";"Đã tham quan / học thử";"Đã đặt cọc";"Đã nhập học";"Từ chối"}`

`W1` (mức khẩn): `={"Tất cả";"Quá hạn";"Hôm nay";"Sắp tới";"Không nhắc";"Tạm dừng"}`

## Cách tính

- **Tình trạng hiện tại, Mức quan tâm, Lần cuối, Hạn liên hệ** lấy từ lần chăm sóc **mới nhất** (theo Thời gian) của lead. Chưa có lần nào: tình trạng "Mới", hạn là ngày nhận.
- **Mức khẩn**: Quá hạn / Hôm nay / Sắp tới theo hạn liên hệ; "Không nhắc" khi đã kết thúc (từ chối, nhập học) hoặc đã nhắc 3 lần chưa chốt; "Tạm dừng" khi chủ bật Tạm dừng.
- **Quá trình tư vấn**: mỗi lần chăm sóc một dòng, cũ trước mới sau: `ngày · sale · phương thức · tình trạng · phản hồi`. Bấm vào ô để đọc hết (hoặc kéo giãn hàng).
- Công thức dựa vào vị trí cột: `Hồ sơ lead` A = Mã lead, B = Ngày nhận, C = Tên phụ huynh, D = Tên bé, E = Tuổi bé, G = Cơ sở, H = Nguồn, K = Sale phụ trách, P = Tạm dừng; `Chăm sóc` B = Mã lead, C = Thời gian, D = Sale, E = Phương thức, F = Tình trạng, G = Mức quan tâm, H = Phản hồi, M = Hạn liên hệ tiếp. Đổi thứ tự cột thì phải sửa công thức.

Đã kiểm tra trên Sheet mẫu (02/11/2026): không lọc ra 8 lead; lọc Cơ sở "Mỹ Đình" ra Quang Thử, Hằng Thử, Lan Thử; lọc thêm Sale "Sale 1" ra "Không có lead nào khớp bộ lọc". Lan Thử: tình trạng "Đã hẹn tham quan / học thử", hạn 03/11/2026, 3 lần chăm sóc.
