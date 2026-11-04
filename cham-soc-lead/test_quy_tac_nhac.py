"""Kiểm tra quy tắc nhắc (bản tham chiếu của công thức AppSheet).

Chạy: python3 -m unittest discover -s cham-soc-lead -v
"""

import csv
import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import quy_tac_nhac as q  # noqa: E402


def lan(ngay, gio, tinh_trang, goi_lai=None, tham_quan=None, ly_do="", chu_dong=False, thu_moi=False, thang=11):
    return q.LanChamSoc(datetime(2026, thang, ngay, gio), tinh_trang, goi_lai, tham_quan, ly_do, chu_dong, thu_moi)


def han(lich_su):
    """Hạn liên hệ tiếp của lần cuối trong `lich_su` (các lần trước là lịch sử)."""
    return q.han_lien_he_tiep(lich_su[-1], lich_su[:-1])


D = date
# Tháng 11/2026: thứ 2 là ngày 2, 9, 16, 23, 30; thứ 6 là 6, 13, 20, 27; thứ 7 là 7, 14, 21, 28.


class NgayLamViec(unittest.TestCase):
    def test_doi_toi_va_lui(self):
        self.assertEqual(q.ngay_lam_viec_toi(D(2026, 11, 7)), D(2026, 11, 9))  # thứ 7 -> thứ 2
        self.assertEqual(q.ngay_lam_viec_toi(D(2026, 11, 8)), D(2026, 11, 9))  # CN -> thứ 2
        self.assertEqual(q.ngay_lam_viec_lui(D(2026, 11, 8)), D(2026, 11, 6))  # CN -> thứ 6
        self.assertEqual(q.ngay_lam_viec_toi(D(2026, 11, 10)), D(2026, 11, 10))

    def test_ngay_le(self):
        nghi = {D(2026, 11, 9), D(2026, 11, 10)}
        self.assertEqual(q.ngay_lam_viec_toi(D(2026, 11, 7), nghi), D(2026, 11, 11))
        self.assertEqual(q.ngay_lam_viec_lui(D(2026, 11, 10), nghi), D(2026, 11, 6))

    def test_le_trong_han_lien_he(self):
        c = lan(5, 9, q.CAN_NHAC)  # thứ 5, L1 -> thứ 6 6/11 là ngày lễ -> thứ 2 9/11
        self.assertEqual(q.han_lien_he_tiep(c, [], nghi={D(2026, 11, 6)}), D(2026, 11, 9))


class A_LeadMoi(unittest.TestCase):
    def test_nhac_ngay_khi_giao(self):
        self.assertEqual(q.han_lead_moi(datetime(2026, 11, 4, 10)), D(2026, 11, 4))
        self.assertEqual(q.han_lead_moi(datetime(2026, 11, 7, 10)), D(2026, 11, 9))  # nhận thứ 7: nhắc thứ 2

    def test_qua_1_ngay_hien_do(self):
        h = q.han_lead_moi(datetime(2026, 11, 4, 10))
        self.assertEqual(q.muc_khan(h, D(2026, 11, 5)), "Quá hạn")
        self.assertTrue(q.bo_quen(q.giai_doan(None, h), "Quá hạn"))


class A_ChuaLienLac(unittest.TestCase):
    def test_nhac_hom_sau_khong_tinh_L(self):
        a = lan(2, 9, q.CHUA_LIEN_LAC)
        b = lan(3, 9, q.CHUA_LIEN_LAC)
        c = lan(4, 9, q.CAN_NHAC)
        self.assertEqual(han([a]), D(2026, 11, 3))
        self.assertEqual(han([a, b]), D(2026, 11, 4))
        self.assertEqual(q.lan_thu([a, b], c), 1)  # lần liên lạc được đầu tiên vẫn là L1
        self.assertEqual(han([a, b, c]), D(2026, 11, 5))

    def test_thu_6_nhac_thu_2(self):
        self.assertEqual(han([lan(6, 9, q.CHUA_LIEN_LAC)]), D(2026, 11, 9))

    def test_3_lan_lien_tiep_chuyen_dai_han(self):
        ls = [lan(2, 9, q.CHUA_LIEN_LAC), lan(3, 9, q.CHUA_LIEN_LAC), lan(4, 9, q.CHUA_LIEN_LAC)]
        self.assertEqual(q.chua_lien_lac_lien_tiep(ls[:2], ls[2]), 3)
        self.assertIsNone(han(ls))
        self.assertEqual(q.giai_doan(ls[-1], None), q.GD_DAI_HAN)

    def test_dut_quang_thi_dem_lai(self):
        ls = [lan(2, 9, q.CHUA_LIEN_LAC), lan(3, 9, q.CHUA_LIEN_LAC), lan(4, 9, q.CAN_NHAC), lan(5, 9, q.CHUA_LIEN_LAC)]
        self.assertEqual(q.chua_lien_lac_lien_tiep(ls[:3], ls[3]), 1)
        self.assertEqual(han(ls), D(2026, 11, 6))


class B_DangChamSoc(unittest.TestCase):
    def test_hen_ngay_nhac_dung_ngay(self):
        self.assertEqual(han([lan(4, 9, q.GOI_LAI, goi_lai=D(2026, 11, 20))]), D(2026, 11, 20))
        self.assertEqual(han([lan(4, 9, q.GOI_LAI, goi_lai=D(2026, 11, 22))]), D(2026, 11, 23))  # hẹn CN: thứ 2

    def test_nut_chon_nhanh(self):
        n = D(2026, 11, 4)
        self.assertEqual(q.ngay_hen_nhanh("1 tuần", n), D(2026, 11, 11))
        self.assertEqual(q.ngay_hen_nhanh("2 tuần", n), D(2026, 11, 18))
        self.assertEqual(q.ngay_hen_nhanh("1 tháng", n), D(2026, 12, 4))
        self.assertEqual(q.ngay_hen_nhanh("3 tháng", n), D(2027, 2, 4))
        self.assertEqual(q.ngay_hen_nhanh("1 tháng", D(2027, 1, 31)), D(2027, 2, 28))
        self.assertIsNone(q.ngay_hen_nhanh("Chọn ngày", n))

    def test_L1_L2_L3_roi_dai_han(self):
        ls = [lan(2, 9, q.CAN_NHAC)]
        self.assertEqual(han(ls), D(2026, 11, 3))  # L1 +1
        ls.append(lan(3, 9, q.CAN_NHAC))
        self.assertEqual(han(ls), D(2026, 11, 6))  # L2 +3
        ls.append(lan(6, 9, q.CAN_NHAC))
        self.assertEqual(han(ls), D(2026, 11, 13))  # L3 +7
        ls.append(lan(13, 9, q.CAN_NHAC))
        self.assertIsNone(han(ls))  # sau L3 vẫn chưa chốt
        self.assertEqual(q.giai_doan(ls[-1], None), q.GD_DAI_HAN)

    def test_ph_tu_lien_he_lai_dem_lai(self):
        ls = [lan(2, 9, q.CAN_NHAC), lan(3, 9, q.CAN_NHAC), lan(6, 9, q.CAN_NHAC), lan(13, 9, q.CAN_NHAC)]
        chu_dong = lan(20, 9, q.CAN_NHAC, chu_dong=True)
        self.assertEqual(q.lan_thu(ls, chu_dong), 1)
        self.assertEqual(han(ls + [chu_dong]), D(2026, 11, 23))  # thứ 6 +1 = thứ 7 -> thứ 2
        sau = lan(23, 9, q.CAN_NHAC)
        self.assertEqual(q.lan_thu(ls + [chu_dong], sau), 2)
        self.assertEqual(han(ls + [chu_dong, sau]), D(2026, 11, 26))
        self.assertEqual(q.giai_doan(sau, D(2026, 11, 26)), q.GD_DANG)

    def test_cau_hinh_doi_duoc(self):
        ch = dict(q.CAU_HINH_MAC_DINH, L1=2)
        self.assertEqual(q.han_lien_he_tiep(lan(2, 9, q.CAN_NHAC), [], ch), D(2026, 11, 4))


class C_ThamQuan(unittest.TestCase):
    def test_xac_nhan_truoc_1_ngay(self):
        self.assertEqual(han([lan(2, 9, q.DA_HEN, tham_quan=D(2026, 11, 5))]), D(2026, 11, 4))

    def test_tham_quan_thu_2_xac_nhan_thu_6(self):
        self.assertEqual(han([lan(3, 9, q.DA_HEN, tham_quan=D(2026, 11, 16))]), D(2026, 11, 13))

    def test_tham_quan_thu_7(self):
        self.assertEqual(han([lan(3, 9, q.DA_HEN, tham_quan=D(2026, 11, 14))]), D(2026, 11, 13))
        # gọi xác nhận xong (thứ 6): nhắc hỏi cảm nhận sau buổi thứ 7 -> CN -> thứ 2
        self.assertEqual(han([lan(13, 9, q.DA_HEN, tham_quan=D(2026, 11, 14))]), D(2026, 11, 16))

    def test_hen_ma_khong_den(self):
        self.assertEqual(han([lan(5, 17, q.KHONG_DEN)]), D(2026, 11, 5))
        self.assertEqual(han([lan(7, 11, q.KHONG_DEN)]), D(2026, 11, 9))  # buổi thứ 7: hẹn lại thứ 2

    def test_da_tham_quan_cam_nhan_roi_chot(self):
        moc = lan(3, 10, q.DA_THAM_QUAN)
        self.assertEqual(han([moc]), D(2026, 11, 4))  # hỏi cảm nhận sau 1 ngày
        cam_nhan = lan(4, 9, q.CAN_NHAC)
        self.assertEqual(han([moc, cam_nhan]), D(2026, 11, 9))  # nhắc chốt sau 3 ngày: thứ 7 -> thứ 2
        # đổi L2 không ảnh hưởng nhắc chốt sau tham quan
        ch = dict(q.CAU_HINH_MAC_DINH, L2=10)
        self.assertEqual(q.han_lien_he_tiep(cam_nhan, [moc], ch), D(2026, 11, 9))

    def test_dat_coc_nhac_thu_moi(self):
        coc = lan(4, 15, q.DAT_COC)
        self.assertEqual(han([coc]), D(2026, 11, 4))
        self.assertEqual(q.giai_doan(coc, D(2026, 11, 4)), q.GD_DANG)
        da_gui = lan(4, 15, q.DAT_COC, thu_moi=True)
        self.assertIsNone(han([da_gui]))
        self.assertEqual(q.giai_doan(da_gui, None), q.GD_CHOT)
        self.assertEqual(han([lan(8, 10, q.DAT_COC)]), D(2026, 11, 9))  # cọc CN: viết thư thứ 2


class D_TuChoi(unittest.TestCase):
    def test_hoc_phi_sang_danh_sach_uu_dai(self):
        c = lan(4, 9, q.TU_CHOI, ly_do=q.LD_HOC_PHI)
        self.assertIsNone(han([c]))
        self.assertEqual(q.giai_doan(c, None), q.GD_DAI_HAN)
        self.assertTrue(q.bang_khoan_hoc_phi(c, "", []))

    def test_truong_khac_6_thang_hoac_dau_nam_hoc(self):
        self.assertEqual(han([lan(4, 9, q.TU_CHOI, ly_do=q.LD_TRUONG_KHAC)]), D(2027, 5, 3))  # 6 tháng trước 1/7
        # Từ chối 10/01/2027: 6 tháng là 09/07, đầu năm học 01/07 đến trước
        c = q.LanChamSoc(datetime(2027, 1, 10, 9), q.TU_CHOI, ly_do_tu_choi=q.LD_TRUONG_KHAC)
        self.assertEqual(q.han_lien_he_tiep(c, []), D(2027, 7, 1))
        # Từ chối 15/06/2027: đầu năm học chỉ còn 16 ngày -> ít nhất 30 ngày (15/07)
        c = q.LanChamSoc(datetime(2027, 6, 15, 9), q.TU_CHOI, ly_do_tu_choi=q.LD_TRUONG_KHAC)
        self.assertEqual(q.han_lien_he_tiep(c, []), D(2027, 7, 15))

    def test_dau_nam_hoc_doi_duoc(self):
        ch = dict(q.CAU_HINH_MAC_DINH, **{"Đầu năm học tháng": 8})
        c = q.LanChamSoc(datetime(2027, 1, 10, 9), q.TU_CHOI, ly_do_tu_choi=q.LD_TRUONG_KHAC)
        self.assertEqual(q.han_lien_he_tiep(c, [], ch), D(2027, 7, 9))

    def test_chua_nhu_cau_va_khac_3_thang(self):
        self.assertEqual(han([lan(4, 9, q.TU_CHOI, ly_do=q.LD_CHUA_NHU_CAU)]), D(2027, 2, 2))
        self.assertEqual(han([lan(4, 9, q.TU_CHOI, ly_do=q.LD_KHAC)]), D(2027, 2, 2))

    def test_dung_cham_soc(self):
        for ld in (q.LD_XA_NHA, q.LD_SAI_TUOI, q.LD_SAI_SDT):
            with self.subTest(ly_do=ld):
                c = lan(4, 9, q.TU_CHOI, ly_do=ld)
                self.assertIsNone(han([c]))
                self.assertEqual(q.giai_doan(c, None), q.GD_DUNG)

    def test_lien_he_lai_sau_tu_choi_dem_tu_moc(self):
        ls = [lan(2, 9, q.CAN_NHAC), lan(3, 9, q.CAN_NHAC), lan(6, 9, q.CAN_NHAC), lan(13, 9, q.TU_CHOI, ly_do=q.LD_KHAC)]
        lai = q.LanChamSoc(datetime(2027, 2, 2, 9), q.CAN_NHAC)
        self.assertEqual(q.lan_thu(ls, lai), 2)  # từ chối là mốc (lần 1)


class ChuTuGui(unittest.TestCase):
    def ud(self, *ngay):
        return [q.LanGui(datetime(*n, 9), q.GUI_UU_DAI) for n in ngay]

    def test_hoc_phi_lan_dau_sau_2_thang(self):
        lc = datetime(2026, 9, 1, 9)
        self.assertFalse(q.nen_gui_uu_dai(q.GD_DAI_HAN, True, True, lc, [], D(2026, 10, 30)))
        self.assertTrue(q.nen_gui_uu_dai(q.GD_DAI_HAN, True, True, lc, [], D(2026, 10, 31)))

    def test_hoc_phi_lan_2_va_toi_da(self):
        lc = datetime(2026, 9, 1, 9)
        g1 = self.ud((2026, 11, 1))
        self.assertFalse(q.nen_gui_uu_dai(q.GD_DAI_HAN, True, True, lc, g1, D(2026, 12, 30)))
        self.assertTrue(q.nen_gui_uu_dai(q.GD_DAI_HAN, True, True, lc, g1, D(2026, 12, 31)))
        self.assertFalse(q.nen_gui_uu_dai(q.GD_DAI_HAN, True, True, lc, g1, D(2027, 5, 1)))  # quá 180 ngày
        g2 = self.ud((2026, 11, 1), (2027, 1, 5))
        self.assertFalse(q.nen_gui_uu_dai(q.GD_DAI_HAN, True, True, lc, g2, D(2027, 6, 1)))  # đủ 2 lần

    def test_lead_khac_thi_thoang(self):
        self.assertTrue(q.nen_gui_uu_dai(q.GD_DANG, True, False, None, [], D(2026, 11, 4)))
        g = self.ud((2026, 9, 6))
        self.assertFalse(q.nen_gui_uu_dai(q.GD_DANG, True, False, None, g, D(2026, 11, 4)))
        self.assertTrue(q.nen_gui_uu_dai(q.GD_DANG, True, False, None, g, D(2026, 11, 5)))

    def test_khong_gui(self):
        for gd, sdt, coc in ((q.GD_CHOT, True, False), (q.GD_DUNG, True, False), (q.GD_DANG, False, False), (q.GD_DANG, True, True)):
            with self.subTest(gd=gd, sdt=sdt, coc=coc):
                self.assertFalse(q.nen_gui_uu_dai(gd, sdt, False, None, [], D(2026, 11, 4), da_dat_coc=coc))

    def test_bang_khoan_hoc_phi(self):
        self.assertTrue(q.bang_khoan_hoc_phi(None, "Học phí vượt khả năng", []))
        self.assertTrue(q.bang_khoan_hoc_phi(None, "", ["Băn khoăn Học phí, muốn hỏi chồng"]))
        self.assertFalse(q.bang_khoan_hoc_phi(None, "", ["Hỏi thực đơn"]))

    def test_thong_tin_dai_han_moi_thang(self):
        g = [q.LanGui(datetime(2026, 10, 5, 9), q.GUI_THONG_TIN)]
        self.assertTrue(q.nen_gui_thong_tin(q.GD_DAI_HAN, True, [], D(2026, 11, 4)))
        self.assertFalse(q.nen_gui_thong_tin(q.GD_DAI_HAN, True, g, D(2026, 11, 3)))
        self.assertTrue(q.nen_gui_thong_tin(q.GD_DAI_HAN, True, g, D(2026, 11, 4)))
        self.assertFalse(q.nen_gui_thong_tin(q.GD_DANG, True, [], D(2026, 11, 4)))


class GiaiDoan(unittest.TestCase):
    def test_tam_dung_cua_chu(self):
        self.assertEqual(q.giai_doan(lan(2, 9, q.CAN_NHAC), D(2026, 11, 3), tam_dung=True), q.GD_DUNG)

    def test_muc_khan(self):
        hom_nay = D(2026, 11, 10)
        self.assertEqual(q.muc_khan(D(2026, 11, 9), hom_nay), "Quá hạn")
        self.assertEqual(q.muc_khan(hom_nay, hom_nay), "Hôm nay")
        self.assertEqual(q.muc_khan(D(2026, 11, 11), hom_nay), "Sắp tới")
        self.assertEqual(q.muc_khan(None, hom_nay), "")

    def test_bo_quen_chi_khi_dang_cham_soc(self):
        self.assertTrue(q.bo_quen(q.GD_DANG, "Quá hạn"))
        self.assertFalse(q.bo_quen(q.GD_DAI_HAN, "Quá hạn"))
        self.assertFalse(q.bo_quen(q.GD_DANG, "Hôm nay"))


class ThongKeThang(unittest.TestCase):
    def test_buoc_dat_duoc(self):
        self.assertEqual(q.buoc_dat_duoc([]), {"Lead mới"})
        self.assertEqual(q.buoc_dat_duoc([q.CHUA_LIEN_LAC]), {"Lead mới"})
        self.assertEqual(q.buoc_dat_duoc([q.CHUA_LIEN_LAC, q.CAN_NHAC]), {"Lead mới", "Đã tư vấn"})
        # Nhảy thẳng tới đặt cọc vẫn tính là đã tham quan (bước trước).
        self.assertEqual(q.buoc_dat_duoc([q.DAT_COC]), {"Lead mới", "Đã tư vấn", "Đã tham quan", "Đã đặt cọc"})
        self.assertEqual(len(q.buoc_dat_duoc([q.NHAP_HOC])), 5)
        # Mới hẹn tham quan thì chưa tính là đã tham quan.
        self.assertNotIn("Đã tham quan", q.buoc_dat_duoc([q.DA_HEN]))

    def test_mau_thang_10(self):
        goc = Path(__file__).resolve().parent / "mau"
        h = list(csv.DictReader(open(goc / "ho-so-lead.csv", encoding="utf-8")))
        c = list(csv.DictReader(open(goc / "cham-soc.csv", encoding="utf-8")))
        self.assertEqual(list(q.thong_ke_thang(h, c, "2026-10").values()), [7, 7, 1, 1, 0])
        self.assertEqual(list(q.thong_ke_thang(h, c, "2026-10", "Chùa Láng").values()), [3, 3, 0, 0, 0])
        self.assertEqual(list(q.thong_ke_thang(h, c, "2026-10", "Mỹ Đình").values()), [2, 2, 1, 1, 0])
        self.assertEqual(list(q.thong_ke_thang(h, c, "2026-11").values()), [1, 0, 0, 0, 0])


class DuLieuMau(unittest.TestCase):
    def test_mau_trong_repo_khop_quy_tac(self):
        """CSV mẫu trong repo phải đúng bằng bản tạo lại từ quy tắc hiện tại (ngày gốc 02/11/2026)."""
        goc = Path(__file__).resolve().parent / "mau"
        with tempfile.TemporaryDirectory() as tmp:
            q.tao_mau(Path(tmp), date(2026, 11, 2))
            for f in sorted(goc.glob("*.csv")):
                with self.subTest(file=f.name):
                    self.assertEqual((Path(tmp) / f.name).read_text(encoding="utf-8"), f.read_text(encoding="utf-8"))

    def test_moi_trang_thai_mau(self):
        goc = Path(__file__).resolve().parent / "mau"
        rows = list(csv.DictReader(open(goc / "cham-soc.csv", encoding="utf-8")))
        cuoi = {}
        for r in rows:
            cuoi[r["Mã lead"]] = r
        hom_nay = date(2026, 11, 2)
        khan = {k: q.muc_khan(date.fromisoformat(v["Hạn liên hệ tiếp"]) if v["Hạn liên hệ tiếp"] else None, hom_nay) for k, v in cuoi.items()}
        self.assertEqual(khan["L0003"], "Quá hạn")
        self.assertEqual(khan["L0002"], "Hôm nay")
        self.assertEqual(khan["L0001"], "Sắp tới")
        self.assertEqual(cuoi["L0006"]["Lần thứ"], "4")  # hết L3: dài hạn
        self.assertEqual(cuoi["L0006"]["Hạn liên hệ tiếp"], "")
        self.assertEqual(cuoi["L0004"]["Hạn liên hệ tiếp"], "2026-11-02")  # đặt cọc CN: viết thư mời thứ 2


if __name__ == "__main__":
    unittest.main()
