#!/usr/bin/env python3
"""Quy tắc nhắc chăm sóc lead của Casa dei Bambini, viết bằng Python để kiểm tra và dùng lại.

Đây là bản tham chiếu của các công thức AppSheet trong thiet-ke.md (mục 4): cùng đầu vào thì phải
ra cùng "Lần thứ" và "Hạn liên hệ tiếp". Script cũng tạo dữ liệu mẫu (giả) cho Sheet mẫu.

Chạy: python3 quy_tac_nhac.py --tao-mau mau/   (ghi các file CSV mẫu)
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

# Tình trạng sau mỗi lần liên hệ (đúng thứ tự trong file mô tả yêu cầu).
CHUA_LIEN_LAC = "Chưa liên lạc được"
CAN_NHAC = "Đang cân nhắc"
GOI_LAI = "Yêu cầu gọi lại sau"
DA_HEN = "Đã hẹn tham quan / học thử"
DA_THAM_QUAN = "Đã tham quan / học thử"
DAT_COC = "Đã đặt cọc"
NHAP_HOC = "Đã nhập học"
TU_CHOI = "Từ chối"
TINH_TRANG = [CHUA_LIEN_LAC, CAN_NHAC, GOI_LAI, DA_HEN, DA_THAM_QUAN, DAT_COC, NHAP_HOC, TU_CHOI]

KET_THUC = {NHAP_HOC, TU_CHOI}  # ngừng nhắc
MOC = {DA_HEN, DA_THAM_QUAN, DAT_COC}  # tiến triển: đếm lại lần nhắc từ đầu

CAU_HINH_MAC_DINH = {"L1": 1, "L2": 3, "L3": 7, "Bỏ quên": 3, "Hạn đặt cọc": 7}


@dataclass
class LanChamSoc:
    thoi_gian: datetime
    tinh_trang: str
    ngay_hen_goi_lai: date | None = None
    ngay_hen_tham_quan: date | None = None


def lan_thu(truoc: list[LanChamSoc], hien_tai: LanChamSoc) -> int:
    """Lần chăm sóc thứ mấy kể từ mốc tiến triển gần nhất (mốc tính là lần 1).

    `truoc`: các lần chăm sóc TRƯỚC lần hiện tại của cùng lead, thứ tự bất kỳ.
    """
    if hien_tai.tinh_trang in MOC:
        return 1
    truoc = sorted((c for c in truoc if c.thoi_gian < hien_tai.thoi_gian), key=lambda c: c.thoi_gian)
    moc = [c for c in truoc if c.tinh_trang in MOC]
    tu = moc[-1].thoi_gian if moc else None
    return 1 + sum(1 for c in truoc if tu is None or c.thoi_gian >= tu)


def han_lien_he_tiep(c: LanChamSoc, lan: int, cau_hinh: dict[str, int] = CAU_HINH_MAC_DINH) -> date | None:
    """Ngày cần liên hệ tiếp sau lần chăm sóc `c`. None: ngừng nhắc (kết thúc, hoặc đề xuất tạm dừng)."""
    ngay = c.thoi_gian.date()
    if c.tinh_trang in KET_THUC:
        return None
    if c.ngay_hen_goi_lai:
        return c.ngay_hen_goi_lai
    if c.tinh_trang == DA_HEN and c.ngay_hen_tham_quan:
        truoc_1_ngay = c.ngay_hen_tham_quan - timedelta(days=1)
        # Chưa tới ngày xác nhận lịch: nhắc xác nhận. Đã xác nhận rồi: nhắc hỏi cảm nhận sau buổi tham quan.
        return truoc_1_ngay if ngay < truoc_1_ngay else c.ngay_hen_tham_quan + timedelta(days=1)
    if c.tinh_trang == DAT_COC:
        return ngay + timedelta(days=cau_hinh["Hạn đặt cọc"])
    if lan > 3:
        return None  # sau L3 vẫn chưa chốt: đề xuất chủ chuyển "Tạm dừng"
    if c.tinh_trang == CHUA_LIEN_LAC:
        return ngay + timedelta(days=1)
    return ngay + timedelta(days=cau_hinh[f"L{lan}"])


def muc_khan(han: date | None, hom_nay: date) -> str:
    if han is None:
        return ""
    if han < hom_nay:
        return "Quá hạn"
    if han == hom_nay:
        return "Hôm nay"
    return "Sắp tới"


# ---------------------------------------------------------------- thống kê theo tháng

BUOC_PHEU = ["Lead mới", "Đã tư vấn", "Đã tham quan", "Đã đặt cọc", "Đã nhập học"]
TAT_CA = "Tất cả"


def buoc_dat_duoc(tinh_trang_cac_lan: list[str]) -> set[str]:
    """Các bước phễu một lead đã đạt, theo mọi lần chăm sóc của lead (tính tới hiện tại).

    Đã tư vấn: có ít nhất một lần liên hệ được (tình trạng khác "Chưa liên lạc được").
    Đã tham quan / đặt cọc / nhập học: từng có tình trạng đó hoặc một bước sau nó.
    """
    tt = set(tinh_trang_cac_lan)
    buoc = {"Lead mới"}
    if tt - {CHUA_LIEN_LAC}:
        buoc.add("Đã tư vấn")
    if tt & {DA_THAM_QUAN, DAT_COC, NHAP_HOC}:
        buoc.add("Đã tham quan")
    if tt & {DAT_COC, NHAP_HOC}:
        buoc.add("Đã đặt cọc")
    if NHAP_HOC in tt:
        buoc.add("Đã nhập học")
    return buoc


def thong_ke_thang(ho_so: list[dict], cham_soc: list[dict], thang: str, co_so: str = TAT_CA) -> dict[str, int]:
    """Phễu của các lead **nhận trong tháng** `thang` ("YYYY-MM"), theo cơ sở (hoặc "Tất cả").

    `ho_so`, `cham_soc`: các hàng của tab `Hồ sơ lead` và `Chăm sóc` (dict theo tiêu đề cột).
    Một lead nhận tháng 10 mà tháng 11 mới nhập học vẫn được tính cho tháng 10 (tính theo tháng nhận lead).
    """
    lan_theo_lead: dict[str, list[str]] = {}
    for c in cham_soc:
        lan_theo_lead.setdefault(c["Mã lead"], []).append(c["Tình trạng"])
    dem = {b: 0 for b in BUOC_PHEU}
    for h in ho_so:
        if not h["Ngày nhận"].startswith(thang):
            continue
        if co_so != TAT_CA and h["Cơ sở"] != co_so:
            continue
        for b in buoc_dat_duoc(lan_theo_lead.get(h["Mã lead"], [])):
            dem[b] += 1
    return dem


# ---------------------------------------------------------------- dữ liệu mẫu (giả)

COT_HO_SO = [
    "Mã lead", "Ngày nhận", "Tên phụ huynh", "Tên bé", "Tuổi bé", "SĐT", "Cơ sở", "Nguồn", "Chiến dịch",
    "PH quan tâm", "Sale phụ trách", "Customer ID", "Chất lượng lead", "Lý do chất lượng", "Ghi chú", "Tạm dừng",
]
COT_CHAM_SOC = [
    "Mã", "Mã lead", "Thời gian", "Sale", "Phương thức", "Tình trạng", "Mức quan tâm", "Phản hồi",
    "Lý do từ chối", "Ngày hẹn gọi lại", "Ngày hẹn tham quan", "Lần thứ", "Hạn liên hệ tiếp",
]
COT_SALE = ["Email", "Tên", "Cơ sở", "Vai trò", "Đang làm"]
COT_DANH_MUC = ["Loại", "Giá trị"]
COT_CAU_HINH = ["Khóa", "Giá trị", "Ý nghĩa"]
COT_BOT = [
    "Thời gian", "Sự kiện", "Tên Facebook", "Customer ID", "SĐT", "Tên bé", "Tuổi bé", "Cơ sở/hệ", "Khu vực",
    "Dự kiến nhập học", "Hẹn tham quan/học thử", "Quảng cáo", "Giai đoạn", "Tin cuối của phụ huynh",
    "Lần đầu liên hệ", "Cập nhật lúc",
]

SALE_MAU = [
    ["chu@example.com", "Chủ (thay bằng email thật)", "", "Chủ", "TRUE"],
    ["sale1@example.com", "Sale 1", "Chùa Láng", "Sale", "TRUE"],
    ["sale2@example.com", "Sale 2", "Chùa Láng", "Sale", "TRUE"],
    ["sale3@example.com", "Sale 3", "Mỹ Đình", "Sale", "TRUE"],
    ["sale4@example.com", "Sale 4", "Mỹ Đình", "Sale", "TRUE"],
    ["sale5@example.com", "Sale 5", "Kim Mã", "Sale", "TRUE"],
    ["sale6@example.com", "Sale 6", "Kim Mã", "Sale", "TRUE"],
]

DANH_MUC_MAU = (
    [["Cơ sở", x] for x in ["Chùa Láng", "Mỹ Đình", "Kim Mã"]]
    + [["Nguồn", x] for x in ["Facebook Messenger", "Facebook", "Zalo", "Website", "Giới thiệu", "Đến trực tiếp", "Sự kiện", "Khác"]]
    + [["Mối quan tâm", x] for x in ["Học phí", "Chương trình", "Giờ học", "Đưa đón", "Ăn uống", "Cơ sở vật chất", "Giáo viên", "Tiếng Anh", "Khác"]]
    + [["Lý do từ chối", x] for x in ["Học phí", "Xa nhà", "Chọn trường khác", "Chưa có nhu cầu", "Khác"]]
    + [["Lý do chất lượng", x] for x in [
        "Sai độ tuổi", "Ở quá xa", "Sai hoặc thiếu SĐT", "Chỉ để lại thông tin xem thử, không có nhu cầu",
        "Học phí vượt khả năng", "Trùng lead", "Khác"]]
)

CAU_HINH_MAU = [
    ["L1", 1, "Số ngày nhắc lần 1 sau lần liên hệ trước"],
    ["L2", 3, "Số ngày nhắc lần 2"],
    ["L3", 7, "Số ngày nhắc lần 3. Sau lần 3 chưa chốt thì đề xuất tạm dừng"],
    ["Bỏ quên", 3, "Quá chừng này ngày không cập nhật thì vào danh sách bỏ quên của chủ"],
    ["Hạn đặt cọc", 7, "Số ngày sau đặt cọc thì nhắc hoàn tất thủ tục nhập học"],
]


def tao_mau(thu_muc: Path, hom_nay: date) -> None:
    """Ghi CSV mẫu cho từng tab. Ngày tính lùi từ `hom_nay` để luôn có lead quá hạn, hôm nay, sắp tới."""
    d = lambda n, h=9, m=0: datetime.combine(hom_nay - timedelta(days=n), datetime.min.time()).replace(hour=h, minute=m)  # noqa: E731
    ho_so = [
        # mã, ngày nhận, PH, bé, tuổi, SĐT, cơ sở, nguồn, chiến dịch, quan tâm, sale, customer id, chất lượng, lý do, ghi chú
        ["L0001", d(10), "Lan Thử", "Bé Na", "3 tuổi", "0900000601", "Mỹ Đình", "Facebook Messenger", "QC Cambridge T10", "Học phí, Chương trình", "sale3@example.com", "GIA-M1", "Tốt", "", ""],
        ["L0002", d(6), "Hoa Thử", "Bé Bông", "2 tuổi", "0900000602", "Chùa Láng", "Zalo", "", "Giờ học", "sale1@example.com", "", "Trung bình", "Ở quá xa", ""],
        ["L0003", d(4), "Minh Thử", "Bé Su", "18 tháng", "0900000603", "Kim Mã", "Giới thiệu", "", "Ăn uống", "sale5@example.com", "", "", "", "Phụ huynh bé Tôm giới thiệu"],
        ["L0004", d(3), "Hằng Thử", "Bé Mít", "4 tuổi", "0900000604", "Mỹ Đình", "Website", "", "Tiếng Anh", "sale4@example.com", "", "Tốt", "", ""],
        ["L0005", d(12), "Long Thử", "Bé Bin", "5 tuổi", "0900000605", "Chùa Láng", "Facebook", "QC Học phí", "Học phí", "sale2@example.com", "", "Kém", "Học phí vượt khả năng", ""],
        ["L0006", d(20), "Thu Thử", "Bé Cún", "3 tuổi", "0900000606", "Kim Mã", "Sự kiện", "", "Chương trình", "sale6@example.com", "", "Tốt", "", ""],
        ["L0007", d(0, 8), "Quang Thử", "Bé Tin", "2 tuổi", "0900000607", "Mỹ Đình", "Đến trực tiếp", "", "", "sale3@example.com", "", "", "", "Mới nhận sáng nay, chưa gọi"],
        ["L0008", d(15), "Đào Thử", "Bé Gạo", "4 tuổi", "0900000608", "Chùa Láng", "Facebook Messenger", "QC Cambridge T10", "Học phí", "sale1@example.com", "GIA-M2", "Trung bình", "Học phí vượt khả năng", ""],
    ]
    # mã lead, thời gian, sale, phương thức, tình trạng, mức quan tâm, phản hồi, lý do từ chối, ngày hẹn gọi lại, ngày hẹn tham quan
    lan = [
        ["L0001", d(10, 10), "sale3@example.com", "Gọi điện", CAN_NHAC, "Quan tâm bình thường", "Băn khoăn học phí, muốn hỏi thêm chồng", "", None, None],
        ["L0001", d(9, 15), "sale3@example.com", "Zalo", CAN_NHAC, "Quan tâm bình thường", "Đã gửi thông tin chương trình", "", None, None],
        ["L0001", d(6, 9), "sale3@example.com", "Gọi điện", DA_HEN, "Rất quan tâm", "Hẹn đến xem trường", "", None, hom_nay + timedelta(days=2)],
        ["L0002", d(6, 11), "sale1@example.com", "Gọi điện", CHUA_LIEN_LAC, "", "Không nghe máy", "", None, None],
        ["L0002", d(5, 14), "sale1@example.com", "Zalo", GOI_LAI, "Hời hợt", "Bận, hẹn tuần sau", "", hom_nay, None],
        ["L0003", d(4, 16), "sale5@example.com", "Gọi điện", CAN_NHAC, "Quan tâm bình thường", "Hỏi thực đơn, đang so sánh trường khác", "", None, None],
        ["L0004", d(3, 10), "sale4@example.com", "Gặp trực tiếp tại trường", DA_THAM_QUAN, "Rất quan tâm", "Bé thích lớp, phụ huynh hỏi lịch nhập học", "", None, None],
        ["L0004", d(1, 9), "sale4@example.com", "Gọi điện", DAT_COC, "Rất quan tâm", "Đã chuyển khoản đặt cọc", "", None, None],
        ["L0005", d(12, 9), "sale2@example.com", "Gọi điện", TU_CHOI, "", "Thấy học phí cao", "Học phí", None, None],
        ["L0006", d(20, 9), "sale6@example.com", "Gọi điện", CAN_NHAC, "Quan tâm bình thường", "", "", None, None],
        ["L0006", d(19, 9), "sale6@example.com", "Zalo", CAN_NHAC, "Hời hợt", "Chưa trả lời tin", "", None, None],
        ["L0006", d(16, 9), "sale6@example.com", "Gọi điện", CAN_NHAC, "Hời hợt", "Hẹn suy nghĩ thêm", "", None, None],
        ["L0006", d(9, 9), "sale6@example.com", "Zalo", CAN_NHAC, "Hời hợt", "Chưa phản hồi", "", None, None],
        ["L0008", d(15, 10), "sale1@example.com", "Messenger (Facebook)", CAN_NHAC, "Quan tâm bình thường", "Hỏi học phí lớp 4 tuổi", "", None, None],
    ]
    cham_soc, da_co = [], {}
    for i, (ma_lead, tg, sale, pt, tt, muc, ph, ly_do, goi_lai, tham_quan) in enumerate(sorted(lan, key=lambda r: r[1]), 1):
        c = LanChamSoc(tg, tt, goi_lai, tham_quan)
        n = lan_thu(da_co.get(ma_lead, []), c)
        han = han_lien_he_tiep(c, n)
        da_co.setdefault(ma_lead, []).append(c)
        cham_soc.append([
            f"C{i:04d}", ma_lead, tg, sale, pt, tt, muc, ph, ly_do, goi_lai or "", tham_quan or "", n, han or "",
        ])
    bot = [
        [d(1, 20), "SĐT mới", "Cúc Thử", "GIA-M3", "0900000611", "", "3 tuổi", "FLC", "Nam Từ Liêm", "", "", "QC Cambridge T10", "Đã có SĐT", "0900000611", d(1, 19), d(1, 20)],
        [d(2, 9), "Muốn hẹn tham quan/học thử", "Nga Thử", "GIA-M4", "0900000612", "", "2 tuổi", "Hongkong", "", "", "sáng thứ 7", "", "Muốn hẹn tham quan/học thử", "cho chị qua xem trường", d(2, 8), d(2, 9)],
        [d(0, 7), "", "khách chưa rõ tên", "GIA-M5", "", "", "", "", "", "", "", "QC Học phí", "Mới", "học phí bao nhiêu ạ", d(0, 7), d(0, 7)],
        [d(10, 9), "SĐT mới", "Lan Thử", "GIA-M1", "0900000601", "Bé Na", "3 tuổi", "Mỹ Đình", "", "", "", "QC Cambridge T10", "Đã có SĐT", "0900000601", d(10, 8), d(10, 9)],
    ]
    bang = {
        "ho-so-lead.csv": (COT_HO_SO, [r + ["FALSE"] for r in ho_so]),
        "cham-soc.csv": (COT_CHAM_SOC, cham_soc),
        "sale.csv": (COT_SALE, SALE_MAU),
        "danh-muc.csv": (COT_DANH_MUC, DANH_MUC_MAU),
        "cau-hinh.csv": (COT_CAU_HINH, CAU_HINH_MAU),
        "leads-bot.csv": (COT_BOT, bot),
    }
    thu_muc.mkdir(parents=True, exist_ok=True)

    def o(v):
        if isinstance(v, datetime):
            return v.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(v, date):
            return v.strftime("%Y-%m-%d")
        return v

    for ten, (cot, hang) in bang.items():
        with open(thu_muc / ten, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(cot)
            w.writerows([[o(v) for v in r] for r in hang])


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--tao-mau", type=Path, help="Thư mục ghi CSV mẫu")
    p.add_argument("--hom-nay", help="Ngày gốc của dữ liệu mẫu (YYYY-MM-DD). Mặc định: hôm nay")
    a = p.parse_args()
    if a.tao_mau:
        hom_nay = datetime.strptime(a.hom_nay, "%Y-%m-%d").date() if a.hom_nay else date.today()
        tao_mau(a.tao_mau, hom_nay)
        print(f"Đã ghi CSV mẫu vào {a.tao_mau}")


if __name__ == "__main__":
    main()
