#!/usr/bin/env bash
# Tạo leads.csv (dữ liệu giả) trong thư mục làm việc của lần chạy.
# Nội dung phải giống hệt skills/bao-cao-tuan/tests/leads_mau.csv (test kiểm tra điều này).
set -euo pipefail
cat > leads.csv <<'CSV'
Thời gian,Sự kiện,Tên Facebook,Customer ID,SĐT,Tên bé,Tuổi bé,Cơ sở/hệ,Khu vực,Dự kiến nhập học,Hẹn tham quan/học thử,Quảng cáo,Giai đoạn,Tin cuối của phụ huynh,Lần đầu liên hệ,Cập nhật lúc
2026-10-27 10:00:00,Chốt lịch hẹn,Lan Thử,GIA-A1,0900000401,Bé Na,18 tháng,Hongkong,Đống Đa,tháng 12,sáng thứ 7 31/10,QC Cambridge T10,Đã hẹn tham quan/học thử,dạ em cảm ơn,2026-10-26 09:00:00,2026-10-27 10:00:00
2026-10-27 15:00:00,Muốn hẹn tham quan/học thử,Hoa Thử,GIA-A2,0900000402,,2 tuổi,FLC,Nam Từ Liêm,,chiều thứ 5,QC Cambridge T10,Muốn hẹn tham quan/học thử,cho chị qua xem trường,2026-10-27 14:00:00,2026-10-27 15:00:00
2026-10-29 09:00:00,Đã liên hệ,Mai Thử,GIA-A3,0900000403,,3 tuổi rưỡi,Mỹ Đình,,,,,Đã có SĐT · Đã liên hệ,số chị đây,2026-10-28 11:00:00,2026-10-29 09:00:00
2026-10-31 09:00:00,SĐT mới,Minh Thử,GIA-A4,090 000 0404,,sinh năm 2022,song ngữ,Ba Đình,,,QC Học phí,Đã có SĐT,0900000404,2026-10-29 08:00:00,2026-10-31 09:00:00
2026-10-30 20:00:00,Cập nhật thông tin,khách chưa rõ tên,GIA-A5,,,dưới 2 tuổi,,,,,QC Học phí,Đã biết tuổi/cơ sở,học phí bao nhiêu ạ,2026-10-30 20:00:00,2026-10-30 20:00:00
2026-11-01 23:30:00,,Tú Thử,GIA-A6,,,,quốc tế,,,,,Mới,chào trường,2026-11-01 23:30:00,2026-11-01 23:30:00
2026-10-28 08:00:00,Không quan tâm,Hằng Thử,GIA-A7,0900000407,,5 tuổi,Chùa Láng,,,,QC Cambridge T10,Không quan tâm,nhà chị chọn trường khác rồi,2026-10-26 00:00:00,2026-10-28 08:00:00
2026-10-31 11:00:00,Đã liên hệ,Long Thử,GIA-A8,0900000408,,4 tuổi,Kim Mã,,,chiều thứ 2,,Đã hẹn tham quan/học thử · Đã liên hệ,ok em,2026-10-30 10:00:00,2026-10-31 11:00:00
2026-11-02 00:00:00,SĐT mới,Nam Thử,GIA-A9,0900000409,,3 tuổi,Mỹ Đình,,,,,Đã có SĐT,0900000409,2026-11-02 00:00:00,2026-11-02 00:00:00
2026-10-31 10:00:00,Cập nhật thông tin,Quang Thử,GIA-A10,,,7 tuổi,Kim Mã,,,,QC Học phí,Đã biết tuổi/cơ sở,bé 7 tuổi rồi,2026-10-31 10:00:00,2026-10-31 10:00:00
2026-10-21 09:00:00,Chốt lịch hẹn,Thu Thử,GIA-B1,0900000411,,2 tuổi,Chùa Láng,,,sáng 24/10,QC Cambridge T10,Đã hẹn tham quan/học thử,,2026-10-20 08:00:00,2026-10-21 09:00:00
2026-10-22 10:00:00,SĐT mới,Bình Thử,GIA-B2,0900000412,,3 tuổi,Kim Mã,,,,,Đã có SĐT,0900000412,2026-10-22 09:00:00,2026-10-22 10:00:00
2026-10-25 23:59:59,,Hà Thử,GIA-B3,,,,,,,,QC Học phí,Mới,,2026-10-25 23:59:59,2026-10-25 23:59:59
2026-10-02 09:00:00,Đã liên hệ,Cúc Thử,GIA-C1,0900000421,,4 tuổi,Mỹ Đình,,,,,Đã có SĐT · Đã liên hệ,,2026-10-01 08:00:00,2026-10-02 09:00:00
2026-10-05 09:00:00,,Đào Thử,GIA-C2,,,,,,,,,Mới,,,2026-10-05 09:00:00
2026-10-26 12:00:00,SĐT mới,Lan Thử,GIA-A1,0900000401,,18 tháng,Hongkong,,,,QC Cambridge T10,Đã có SĐT,,2026-10-26 09:00:00,2026-10-26 12:00:00
CSV
