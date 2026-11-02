# Công thức tab `Thống kê`

Dán vào **hàng 2** của tab `Thống kê` (hàng 1 là tiêu đề: Tháng, Cơ sở, Mã, Lead mới, Đã tư vấn, Đã tham quan, Đã đặt cọc, Đã nhập học, Tỷ lệ tư vấn, Tỷ lệ tham quan, Tỷ lệ đặt cọc, Tỷ lệ nhập học, Lead mới tháng trước). Mỗi ô một công thức, cả cột tự điền xuống.

Các công thức viết theo kiểu số tiếng Anh (dấu `,` ngăn tham số). Sheet đặt **Cài đặt bảng tính → Ngôn ngữ: Việt Nam** thì phải đổi `,` thành `;` (và trong `{...}` giữ `;`), hoặc tạm đổi ngôn ngữ của file sang Hoa Kỳ, dán công thức, rồi đổi lại; công thức đã dán vẫn chạy đúng. Cách dễ nhất: **sao chép cả tab `Thống kê` từ Sheet mẫu** sang file thật (chuột phải tên tab → Sao chép vào), không phải dán lại.

| Ô | Công thức |
|---|---|
| A2 (Tháng) | `=LET(s,DATE(YEAR(MIN('Hồ sơ lead'!B2:B)),MONTH(MIN('Hồ sơ lead'!B2:B)),1),n,DATEDIF(s,TODAY(),"M")+1,cs,{"Tất cả";FILTER('Danh mục'!B2:B,'Danh mục'!A2:A="Cơ sở")},ARRAYFORMULA(FLATTEN(TEXT(EDATE(s,SEQUENCE(n,1,n-1,-1)),"yyyy-mm")&IF(SEQUENCE(1,ROWS(cs)),""))))` |
| B2 (Cơ sở) | `=LET(s,DATE(YEAR(MIN('Hồ sơ lead'!B2:B)),MONTH(MIN('Hồ sơ lead'!B2:B)),1),n,DATEDIF(s,TODAY(),"M")+1,cs,{"Tất cả";FILTER('Danh mục'!B2:B,'Danh mục'!A2:A="Cơ sở")},ARRAYFORMULA(FLATTEN(IF(SEQUENCE(n),TRANSPOSE(cs)))))` |
| C2 (Mã) | `=ARRAYFORMULA(IF(A2:A="",,A2:A&" · "&B2:B))` |
| D2 (Lead mới) | `=MAP(A2:A,B2:B,LAMBDA(t,cs,IF(t="",,SUMPRODUCT((TEXT('Hồ sơ lead'!B2:B,"yyyy-mm")=t)*((('Hồ sơ lead'!G2:G=cs)+(cs="Tất cả"))>0)))))` |
| E2 (Đã tư vấn) | `=MAP(A2:A,B2:B,LAMBDA(t,cs,IF(t="",,SUMPRODUCT((TEXT('Hồ sơ lead'!B2:B,"yyyy-mm")=t)*((('Hồ sơ lead'!G2:G=cs)+(cs="Tất cả"))>0)*(COUNTIFS('Chăm sóc'!B2:B,'Hồ sơ lead'!A2:A,'Chăm sóc'!F2:F,"<>Chưa liên lạc được")>0)))))` |
| F2 (Đã tham quan) | `=MAP(A2:A,B2:B,LAMBDA(t,cs,IF(t="",,SUMPRODUCT((TEXT('Hồ sơ lead'!B2:B,"yyyy-mm")=t)*((('Hồ sơ lead'!G2:G=cs)+(cs="Tất cả"))>0)*((COUNTIFS('Chăm sóc'!B2:B,'Hồ sơ lead'!A2:A,'Chăm sóc'!F2:F,"Đã tham quan / học thử")+COUNTIFS('Chăm sóc'!B2:B,'Hồ sơ lead'!A2:A,'Chăm sóc'!F2:F,"Đã đặt cọc")+COUNTIFS('Chăm sóc'!B2:B,'Hồ sơ lead'!A2:A,'Chăm sóc'!F2:F,"Đã nhập học"))>0)))))` |
| G2 (Đã đặt cọc) | `=MAP(A2:A,B2:B,LAMBDA(t,cs,IF(t="",,SUMPRODUCT((TEXT('Hồ sơ lead'!B2:B,"yyyy-mm")=t)*((('Hồ sơ lead'!G2:G=cs)+(cs="Tất cả"))>0)*((COUNTIFS('Chăm sóc'!B2:B,'Hồ sơ lead'!A2:A,'Chăm sóc'!F2:F,"Đã đặt cọc")+COUNTIFS('Chăm sóc'!B2:B,'Hồ sơ lead'!A2:A,'Chăm sóc'!F2:F,"Đã nhập học"))>0)))))` |
| H2 (Đã nhập học) | `=MAP(A2:A,B2:B,LAMBDA(t,cs,IF(t="",,SUMPRODUCT((TEXT('Hồ sơ lead'!B2:B,"yyyy-mm")=t)*((('Hồ sơ lead'!G2:G=cs)+(cs="Tất cả"))>0)*((COUNTIFS('Chăm sóc'!B2:B,'Hồ sơ lead'!A2:A,'Chăm sóc'!F2:F,"Đã nhập học"))>0)))))` |
| I2 (Tỷ lệ tư vấn) | `=ARRAYFORMULA(IF(A2:A="",,IF(D2:D=0,0,E2:E/D2:D)))` |
| J2, K2, L2 | Như I2, đổi `E2:E` thành `F2:F`, `G2:G`, `H2:H` |
| M2 (Lead mới tháng trước) | `=MAP(A2:A,B2:B,LAMBDA(t,cs,IF(t="",,SUMIFS(D2:D,A2:A,TEXT(EDATE(DATE(LEFT(t,4),RIGHT(t,2),1),-1),"yyyy-mm"),B2:B,cs))))` |

Cột I – L định dạng **Phần trăm**.

Công thức dựa vào vị trí cột: `Hồ sơ lead` cột A = Mã lead, B = Ngày nhận, G = Cơ sở; `Chăm sóc` cột B = Mã lead, F = Tình trạng. Đổi thứ tự cột ở hai tab này thì phải sửa công thức.

Đã kiểm tra trên Sheet mẫu (02/11/2026): tháng 2026-10, Tất cả: 7 lead mới, 7 đã tư vấn, 1 đã tham quan, 1 đặt cọc, 0 nhập học; Chùa Láng 3/3/0/0/0; Mỹ Đình 2/2/1/1/0; Kim Mã 2/2/0/0/0. Khớp với `thong_ke_thang` trong `quy_tac_nhac.py`.
