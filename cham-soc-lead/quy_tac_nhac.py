#!/usr/bin/env python3
"""Quy tắc nhắc chăm sóc lead của Casa dei Bambini, viết bằng Python để kiểm tra và dùng lại.

Đây là bản tham chiếu của các công thức AppSheet trong thiet-ke.md (mục 4): cùng đầu vào thì phải
ra cùng "Lần thứ", "Hạn liên hệ tiếp", "Giai đoạn" và cùng danh sách gửi ưu đãi / thông tin.
Quy tắc theo phản hồi của trường (11/2026); test_quy_tac_nhac.py có một ca cho mỗi dòng quy tắc.
Script cũng tạo dữ liệu mẫu (giả) cho Sheet mẫu.

Chạy: python3 quy_tac_nhac.py --tao-mau mau/   (ghi các file CSV mẫu)
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

# Tình trạng sau mỗi lần liên hệ.
CHUA_LIEN_LAC = "Chưa liên lạc được"
CAN_NHAC = "Đang cân nhắc"
GOI_LAI = "Yêu cầu gọi lại sau"
DA_HEN = "Đã hẹn tham quan / học thử"
KHONG_DEN = "Hẹn nhưng không đến"
DA_THAM_QUAN = "Đã tham quan / học thử"
DAT_COC = "Đã đặt cọc"
NHAP_HOC = "Đã nhập học"
TU_CHOI = "Từ chối"
TINH_TRANG = [CHUA_LIEN_LAC, CAN_NHAC, GOI_LAI, DA_HEN, KHONG_DEN, DA_THAM_QUAN, DAT_COC, NHAP_HOC, TU_CHOI]

# Mốc: đếm lại L1/L2/L3 từ lần này (bản thân mốc là lần 1). Lần "PH chủ động liên hệ" cũng là mốc.
MOC = {DA_HEN, DA_THAM_QUAN, DAT_COC, TU_CHOI}

# Lý do từ chối.
LD_HOC_PHI = "Học phí"
LD_TRUONG_KHAC = "Chọn trường khác"
LD_CHUA_NHU_CAU = "Chưa có nhu cầu"
LD_XA_NHA = "Xa nhà"
LD_SAI_TUOI = "Sai độ tuổi"
LD_SAI_SDT = "Sai số điện thoại"
LD_KHAC = "Khác"
LY_DO_TU_CHOI = [LD_HOC_PHI, LD_TRUONG_KHAC, LD_CHUA_NHU_CAU, LD_XA_NHA, LD_SAI_TUOI, LD_SAI_SDT, LD_KHAC]
LY_DO_DUNG = {LD_XA_NHA, LD_SAI_TUOI, LD_SAI_SDT}  # dừng chăm sóc, không nhắc

# Nút chọn nhanh "Hẹn lại sau" (phụ huynh hẹn ngày liên hệ lại).
HEN_NHANH = {"1 tuần": ("ngày", 7), "2 tuần": ("ngày", 14), "1 tháng": ("tháng", 1), "3 tháng": ("tháng", 3)}
HEN_CHON_NGAY = "Chọn ngày"

# Giai đoạn của lead.
GD_DANG = "Đang chăm sóc"
GD_DAI_HAN = "Dài hạn"
GD_CHOT = "Đã chốt"
GD_DUNG = "Dừng"

# Loại thông tin chủ tự gửi cho phụ huynh (không làm đổi lịch nhắc của sale).
GUI_UU_DAI = "Ưu đãi học phí"
GUI_THONG_TIN = "Thông tin hoạt động"

CAU_HINH_MAC_DINH = {
    "L1": 1, "L2": 3, "L3": 7,
    "Chưa liên lạc tối đa": 3,
    "Sau tham quan": 1, "Chốt sau tham quan": 3,
    "Từ chối trường khác": 180, "Từ chối trường khác tối thiểu": 30,
    "Đầu năm học tháng": 7, "Đầu năm học ngày": 1,
    "Từ chối chưa nhu cầu": 90, "Từ chối khác": 90,
    "Ưu đãi lần đầu": 60, "Ưu đãi cách nhau": 60, "Ưu đãi tối đa": 2, "Ưu đãi lần 2 trong vòng": 180,
    "Thông tin dài hạn": 30,
}


@dataclass
class LanChamSoc:
    thoi_gian: datetime
    tinh_trang: str
    ngay_hen_goi_lai: date | None = None
    ngay_hen_tham_quan: date | None = None
    ly_do_tu_choi: str = ""
    ph_chu_dong: bool = False
    da_gui_thu_moi: bool = False


def la_moc(c: LanChamSoc) -> bool:
    return c.tinh_trang in MOC or c.ph_chu_dong


def _truoc(truoc: list[LanChamSoc], c: LanChamSoc) -> list[LanChamSoc]:
    return sorted((x for x in truoc if x.thoi_gian < c.thoi_gian), key=lambda x: x.thoi_gian)


def moc_gan_nhat(truoc: list[LanChamSoc], c: LanChamSoc) -> LanChamSoc | None:
    """Mốc gần nhất TRƯỚC lần `c` (không tính chính `c`)."""
    moc = [x for x in _truoc(truoc, c) if la_moc(x)]
    return moc[-1] if moc else None


def lan_thu(truoc: list[LanChamSoc], c: LanChamSoc) -> int:
    """Lần thứ mấy kể từ mốc gần nhất (mốc là lần 1). Lần "Chưa liên lạc được" không được đếm.

    `truoc`: các lần chăm sóc khác của cùng lead, thứ tự bất kỳ (lần sau `c` bị bỏ qua).
    """
    if la_moc(c):
        return 1
    m = moc_gan_nhat(truoc, c)
    return 1 + sum(
        1 for x in _truoc(truoc, c)
        if x.tinh_trang != CHUA_LIEN_LAC and (m is None or x.thoi_gian >= m.thoi_gian)
    )


def chua_lien_lac_lien_tiep(truoc: list[LanChamSoc], c: LanChamSoc) -> int:
    """Số lần "Chưa liên lạc được" liên tiếp tính tới `c` (gồm cả `c`). 0 nếu `c` liên lạc được."""
    if c.tinh_trang != CHUA_LIEN_LAC:
        return 0
    n = 1
    for x in reversed(_truoc(truoc, c)):
        if x.tinh_trang != CHUA_LIEN_LAC:
            break
        n += 1
    return n


# ---------------------------------------------------------------- ngày làm việc

def la_ngay_nghi(d: date, nghi: set[date]) -> bool:
    """Thứ 7, Chủ nhật, hoặc ngày lễ trong tab `Ngày nghỉ`."""
    return d.weekday() >= 5 or d in nghi


def ngay_lam_viec_toi(d: date, nghi: set[date] = frozenset()) -> date:
    """`d` nếu là ngày làm việc, không thì ngày làm việc kế tiếp. AppSheet: WORKDAY(d - 1, 1, nghỉ)."""
    while la_ngay_nghi(d, nghi):
        d += timedelta(days=1)
    return d


def ngay_lam_viec_lui(d: date, nghi: set[date] = frozenset()) -> date:
    """`d` nếu là ngày làm việc, không thì ngày làm việc liền trước. AppSheet: WORKDAY(d + 1, -1, nghỉ)."""
    while la_ngay_nghi(d, nghi):
        d -= timedelta(days=1)
    return d


def cong_thang(d: date, n: int) -> date:
    """Như EDATE: cùng ngày của n tháng sau, ngày không có (31/4) thì lấy ngày cuối tháng."""
    y, m = divmod(d.month - 1 + n, 12)
    y, m = d.year + y, m + 1
    cuoi = (date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)).day
    return date(y, m, min(d.day, cuoi))


def ngay_hen_nhanh(lua_chon: str, ngay: date) -> date | None:
    """Ngày hẹn gọi lại theo nút chọn nhanh. "Chọn ngày" hoặc trống: None (sale tự chọn ngày)."""
    if lua_chon not in HEN_NHANH:
        return None
    kieu, n = HEN_NHANH[lua_chon]
    return ngay + timedelta(days=n) if kieu == "ngày" else cong_thang(ngay, n)


def dau_nam_hoc_toi(ngay: date, ch: dict[str, int] = CAU_HINH_MAC_DINH) -> date:
    """Ngày đầu năm học gần nhất SAU `ngay`."""
    d = date(ngay.year, ch["Đầu năm học tháng"], ch["Đầu năm học ngày"])
    return d if d > ngay else date(ngay.year + 1, d.month, d.day)


# ---------------------------------------------------------------- hạn liên hệ tiếp

def han_tho(c: LanChamSoc, truoc: list[LanChamSoc], ch: dict[str, int] = CAU_HINH_MAC_DINH) -> tuple[date | None, bool]:
    """(Ngày nhắc trước khi dời qua ngày nghỉ, có dời lùi không). None: không nhắc sale.

    Dời lùi chỉ dùng cho nhắc TRƯỚC một việc (xác nhận lịch tham quan): rơi vào ngày nghỉ thì lùi về
    ngày làm việc trước, để không nhắc sau buổi tham quan. Mọi nhắc khác dời tới ngày làm việc kế tiếp.
    """
    ngay = c.thoi_gian.date()
    d = timedelta
    if c.tinh_trang == NHAP_HOC:
        return None, False
    if c.tinh_trang == TU_CHOI:
        ly_do = c.ly_do_tu_choi
        if ly_do in LY_DO_DUNG or ly_do == LD_HOC_PHI:
            return None, False  # học phí: chủ gửi ưu đãi (danh sách "Gửi ưu đãi"), sale không nhắc
        if ly_do == LD_TRUONG_KHAC:
            sau_6_thang = ngay + d(days=ch["Từ chối trường khác"])
            som_nhat = ngay + d(days=ch["Từ chối trường khác tối thiểu"])
            return max(min(sau_6_thang, dau_nam_hoc_toi(ngay, ch)), som_nhat), False
        if ly_do == LD_CHUA_NHU_CAU:
            return ngay + d(days=ch["Từ chối chưa nhu cầu"]), False
        return ngay + d(days=ch["Từ chối khác"]), False  # "Khác" hoặc để trống
    if c.tinh_trang == DAT_COC:
        return (None, False) if c.da_gui_thu_moi else (ngay, False)  # nhắc viết thư mời ngay trong ngày
    if c.ngay_hen_goi_lai:
        return c.ngay_hen_goi_lai, False
    if c.tinh_trang == DA_HEN and c.ngay_hen_tham_quan:
        xac_nhan = c.ngay_hen_tham_quan - d(days=1)
        if ngay < xac_nhan:
            return xac_nhan, True
        return c.ngay_hen_tham_quan + d(days=ch["Sau tham quan"]), False
    if c.tinh_trang == KHONG_DEN:
        return ngay, False  # hẹn lại ngay trong ngày (hoặc sáng hôm sau nếu ghi ngoài giờ)
    if c.tinh_trang == CHUA_LIEN_LAC:
        if chua_lien_lac_lien_tiep(truoc, c) >= ch["Chưa liên lạc tối đa"]:
            return None, False  # chuyển dài hạn
        return ngay + d(days=1), False
    if c.tinh_trang == DA_THAM_QUAN:
        return ngay + d(days=ch["Sau tham quan"]), False
    n = lan_thu(truoc, c)
    if n > 3:
        return None, False  # sau L3 chưa chốt: chuyển dài hạn
    m = moc_gan_nhat(truoc, c)
    if n == 2 and m is not None and m.tinh_trang == DA_THAM_QUAN:
        return ngay + d(days=ch["Chốt sau tham quan"]), False
    return ngay + d(days=ch[f"L{n}"]), False


def han_lien_he_tiep(c: LanChamSoc, truoc: list[LanChamSoc], ch: dict[str, int] = CAU_HINH_MAC_DINH,
                     nghi: set[date] = frozenset()) -> date | None:
    """Ngày sale cần liên hệ tiếp sau lần `c`, đã dời qua thứ 7, Chủ nhật, ngày lễ. None: không nhắc."""
    tho, lui = han_tho(c, truoc, ch)
    if tho is None:
        return None
    return ngay_lam_viec_lui(tho, nghi) if lui else ngay_lam_viec_toi(tho, nghi)


def han_lead_moi(ngay_nhan: datetime, nghi: set[date] = frozenset()) -> date:
    """Lead chưa liên hệ lần nào: nhắc ngay ngày nhận (dời tới ngày làm việc)."""
    return ngay_lam_viec_toi(ngay_nhan.date(), nghi)


def giai_doan(cuoi: LanChamSoc | None, han: date | None, tam_dung: bool = False) -> str:
    """Giai đoạn của lead theo lần chăm sóc mới nhất `cuoi` và hạn liên hệ của lần đó."""
    if tam_dung:
        return GD_DUNG
    if cuoi is None:
        return GD_DANG
    if cuoi.tinh_trang == NHAP_HOC or (cuoi.tinh_trang == DAT_COC and cuoi.da_gui_thu_moi):
        return GD_CHOT
    if cuoi.tinh_trang == TU_CHOI:
        return GD_DUNG if cuoi.ly_do_tu_choi in LY_DO_DUNG else GD_DAI_HAN
    return GD_DANG if han is not None else GD_DAI_HAN


def muc_khan(han: date | None, hom_nay: date) -> str:
    if han is None:
        return ""
    if han < hom_nay:
        return "Quá hạn"
    if han == hom_nay:
        return "Hôm nay"
    return "Sắp tới"


def bo_quen(gd: str, khan: str) -> bool:
    """Chủ cần nhắc sale: lead đang chăm sóc mà quá hạn."""
    return gd == GD_DANG and khan == "Quá hạn"


# ---------------------------------------------------------------- danh sách chủ tự gửi

@dataclass
class LanGui:
    thoi_gian: datetime
    loai: str  # GUI_UU_DAI hoặc GUI_THONG_TIN


def bang_khoan_hoc_phi(cuoi: LanChamSoc | None, ly_do_chat_luong: str, phan_hoi: list[str]) -> bool:
    """Nhóm ưu tiên gửi ưu đãi: từ chối vì học phí, chất lượng lead "Học phí vượt khả năng",
    hoặc phản hồi của sale có chữ "học phí"."""
    if cuoi is not None and cuoi.tinh_trang == TU_CHOI and cuoi.ly_do_tu_choi == LD_HOC_PHI:
        return True
    if ly_do_chat_luong == "Học phí vượt khả năng":
        return True
    return any("học phí" in (p or "").lower() for p in phan_hoi)


def nen_gui_uu_dai(gd: str, co_sdt: bool, hoc_phi: bool, lan_cuoi: datetime, gui: list[LanGui],
                   hom_nay: date, ch: dict[str, int] = CAU_HINH_MAC_DINH, da_dat_coc: bool = False) -> bool:
    """Lead có vào danh sách "Gửi ưu đãi" của chủ hôm nay không.

    `lan_cuoi`: thời gian lần chăm sóc mới nhất (hoặc ngày nhận nếu chưa có). `gui`: các lần chủ đã gửi.
    Nhóm băn khoăn học phí: lần đầu sau "Ưu đãi lần đầu" ngày kể từ lần cuối; tối đa "Ưu đãi tối đa" lần;
    lần 2 cách lần 1 ít nhất "Ưu đãi cách nhau" ngày và trong vòng "Ưu đãi lần 2 trong vòng" ngày.
    Các lead khác: cách lần gửi trước ít nhất "Ưu đãi cách nhau" ngày.
    Không gửi cho lead đã chốt, dừng, đã đặt cọc (đang chờ thư mời), hoặc không có SĐT.
    """
    if gd not in (GD_DANG, GD_DAI_HAN) or not co_sdt or da_dat_coc:
        return False
    ud = sorted(g.thoi_gian.date() for g in gui if g.loai == GUI_UU_DAI)
    cach = timedelta(days=ch["Ưu đãi cách nhau"])
    if not hoc_phi:
        return not ud or hom_nay - ud[-1] >= cach
    if not ud:
        return hom_nay - lan_cuoi.date() >= timedelta(days=ch["Ưu đãi lần đầu"])
    if len(ud) >= ch["Ưu đãi tối đa"]:
        return False
    return cach <= hom_nay - ud[-1] <= timedelta(days=ch["Ưu đãi lần 2 trong vòng"])


def nen_gui_thong_tin(gd: str, co_sdt: bool, gui: list[LanGui], hom_nay: date,
                      ch: dict[str, int] = CAU_HINH_MAC_DINH) -> bool:
    """Lead dài hạn có vào danh sách "Gửi thông tin" (sự kiện, hội thảo, video) của chủ hôm nay không."""
    if gd != GD_DAI_HAN or not co_sdt:
        return False
    tt = [g.thoi_gian.date() for g in gui if g.loai == GUI_THONG_TIN]
    return not tt or hom_nay - max(tt) >= timedelta(days=ch["Thông tin dài hạn"])


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
    "Chủ nhắc lúc",
]
COT_CHAM_SOC = [
    "Mã", "Mã lead", "Thời gian", "Sale", "Phương thức", "Tình trạng", "Mức quan tâm", "Phản hồi",
    "Lý do từ chối", "Ngày hẹn gọi lại", "Ngày hẹn tham quan", "Lần thứ", "Hạn liên hệ tiếp",
    # thêm ở cuối để công thức tab Thống kê, Tổng hợp lead (dựa vào vị trí cột) không phải sửa
    "PH chủ động", "Hẹn lại sau", "Đã gửi thư mời", "Ngày nhập học dự kiến",
]
COT_NGAY_NGHI = ["Ngày", "Tên"]
COT_GUI = ["Mã", "Mã lead", "Thời gian", "Loại", "Người gửi", "Ghi chú"]
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
    + [["Nguồn", x] for x in ["Facebook Messenger", "Facebook", "Zalo", "Gọi hotline", "Website", "Tự tìm hiểu", "Giới thiệu", "Đến trực tiếp", "Sự kiện", "Khác"]]
    + [["Mối quan tâm", x] for x in ["Học phí", "Chương trình", "Giờ học", "Đưa đón", "Ăn uống", "Cơ sở vật chất", "Giáo viên", "Tiếng Anh", "Khác"]]
    + [["Lý do từ chối", x] for x in LY_DO_TU_CHOI]
    + [["Lý do chất lượng", x] for x in [
        "Sai độ tuổi", "Ở quá xa", "Sai hoặc thiếu SĐT", "Chỉ để lại thông tin xem thử, không có nhu cầu",
        "Học phí vượt khả năng", "Trùng lead", "Khác"]]
)

Y_NGHIA_CAU_HINH = {
    "L1": "Số ngày nhắc lần 1 (sau lần liên hệ đầu, hoặc sau mốc)",
    "L2": "Số ngày nhắc lần 2",
    "L3": "Số ngày nhắc lần 3. Hết L3 chưa chốt thì chuyển dài hạn",
    "Chưa liên lạc tối đa": "Số lần \"Chưa liên lạc được\" liên tiếp thì chuyển dài hạn",
    "Sau tham quan": "Số ngày sau buổi tham quan thì nhắc hỏi cảm nhận",
    "Chốt sau tham quan": "Số ngày sau lần hỏi cảm nhận thì nhắc chốt",
    "Từ chối trường khác": "Từ chối vì chọn trường khác: nhắc lại sau chừng này ngày (hoặc đầu năm học, mốc nào đến trước)",
    "Từ chối trường khác tối thiểu": "Nhưng không sớm hơn chừng này ngày sau khi từ chối",
    "Đầu năm học tháng": "Tháng bắt đầu năm học",
    "Đầu năm học ngày": "Ngày bắt đầu năm học",
    "Từ chối chưa nhu cầu": "Từ chối vì chưa có nhu cầu: nhắc lại sau chừng này ngày",
    "Từ chối khác": "Từ chối vì lý do khác: nhắc lại sau chừng này ngày",
    "Ưu đãi lần đầu": "Nhóm băn khoăn học phí: gửi ưu đãi lần đầu sau chừng này ngày kể từ lần liên hệ cuối",
    "Ưu đãi cách nhau": "Hai lần gửi ưu đãi cách nhau ít nhất chừng này ngày",
    "Ưu đãi tối đa": "Nhóm băn khoăn học phí: gửi ưu đãi tối đa chừng này lần",
    "Ưu đãi lần 2 trong vòng": "Nhóm băn khoăn học phí: quá chừng này ngày sau lần 1 mà chưa gửi lần 2 thì thôi",
    "Thông tin dài hạn": "Lead dài hạn: gửi thông tin hoạt động cách nhau chừng này ngày",
}
CAU_HINH_MAU = [[k, v, Y_NGHIA_CAU_HINH[k]] for k, v in CAU_HINH_MAC_DINH.items()]

# Ngày lễ dương lịch chắc chắn. Tết, Giỗ Tổ (âm lịch) và ngày nghỉ bù: chủ điền theo thông báo của trường.
NGAY_NGHI_MAU = [
    [date(2027, 1, 1), "Tết Dương lịch"],
    [date(2027, 4, 30), "Giải phóng miền Nam"],
    [date(2027, 5, 1), "Quốc tế Lao động"],
    [date(2027, 9, 2), "Quốc khánh"],
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
        ["L0004", d(1, 9), "sale4@example.com", "Gọi điện", DAT_COC, "Rất quan tâm", "Đã chuyển khoản đặt cọc", "", None, None, False, "", False, date(2026, 12, 1)],
        ["L0005", d(12, 9), "sale2@example.com", "Gọi điện", TU_CHOI, "", "Thấy học phí cao", "Học phí", None, None],
        ["L0006", d(20, 9), "sale6@example.com", "Gọi điện", CAN_NHAC, "Quan tâm bình thường", "", "", None, None],
        ["L0006", d(19, 9), "sale6@example.com", "Zalo", CAN_NHAC, "Hời hợt", "Chưa trả lời tin", "", None, None],
        ["L0006", d(16, 9), "sale6@example.com", "Gọi điện", CAN_NHAC, "Hời hợt", "Hẹn suy nghĩ thêm", "", None, None],
        ["L0006", d(9, 9), "sale6@example.com", "Zalo", CAN_NHAC, "Hời hợt", "Chưa phản hồi", "", None, None],
        ["L0008", d(15, 10), "sale1@example.com", "Messenger (Facebook)", CAN_NHAC, "Quan tâm bình thường", "Hỏi học phí lớp 4 tuổi", "", None, None],
    ]
    lan = [r + [False, "", False, None][len(r) - 10:] for r in lan]  # mặc định cho 4 cột mới
    nghi = {r[0] for r in NGAY_NGHI_MAU}
    cham_soc, da_co = [], {}
    for i, (ma_lead, tg, sale, pt, tt, muc, ph, ly_do, goi_lai, tham_quan, chu_dong, hen_nhanh, thu_moi, nhap_hoc) in enumerate(sorted(lan, key=lambda r: r[1]), 1):
        if goi_lai and not hen_nhanh:
            hen_nhanh = HEN_CHON_NGAY
        c = LanChamSoc(tg, tt, goi_lai, tham_quan, ly_do, chu_dong, thu_moi)
        truoc = da_co.get(ma_lead, [])
        n = lan_thu(truoc, c)
        han = han_lien_he_tiep(c, truoc, nghi=nghi)
        da_co.setdefault(ma_lead, []).append(c)
        b = lambda v: "TRUE" if v else "FALSE"  # noqa: E731
        cham_soc.append([
            f"C{i:04d}", ma_lead, tg, sale, pt, tt, muc, ph, ly_do, goi_lai or "", tham_quan or "", n, han or "",
            b(chu_dong), hen_nhanh, b(thu_moi), nhap_hoc or "",
        ])
    bot = [
        [d(1, 20), "SĐT mới", "Cúc Thử", "GIA-M3", "0900000611", "", "3 tuổi", "FLC", "Nam Từ Liêm", "", "", "QC Cambridge T10", "Đã có SĐT", "0900000611", d(1, 19), d(1, 20)],
        [d(2, 9), "Muốn hẹn tham quan/học thử", "Nga Thử", "GIA-M4", "0900000612", "", "2 tuổi", "Hongkong", "", "", "sáng thứ 7", "", "Muốn hẹn tham quan/học thử", "cho chị qua xem trường", d(2, 8), d(2, 9)],
        [d(0, 7), "", "khách chưa rõ tên", "GIA-M5", "", "", "", "", "", "", "", "QC Học phí", "Mới", "học phí bao nhiêu ạ", d(0, 7), d(0, 7)],
        [d(10, 9), "SĐT mới", "Lan Thử", "GIA-M1", "0900000601", "Bé Na", "3 tuổi", "Mỹ Đình", "", "", "", "QC Cambridge T10", "Đã có SĐT", "0900000601", d(10, 8), d(10, 9)],
    ]
    bang = {
        "ho-so-lead.csv": (COT_HO_SO, [r + ["FALSE", ""] for r in ho_so]),
        "cham-soc.csv": (COT_CHAM_SOC, cham_soc),
        "sale.csv": (COT_SALE, SALE_MAU),
        "danh-muc.csv": (COT_DANH_MUC, DANH_MUC_MAU),
        "cau-hinh.csv": (COT_CAU_HINH, CAU_HINH_MAU),
        "leads-bot.csv": (COT_BOT, bot),
        "ngay-nghi.csv": (COT_NGAY_NGHI, NGAY_NGHI_MAU),
        "gui-thong-tin.csv": (COT_GUI, []),
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
