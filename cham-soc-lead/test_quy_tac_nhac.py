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


def lan(ngay, gio, tinh_trang, goi_lai=None, tham_quan=None):
    return q.LanChamSoc(datetime(2026, 11, ngay, gio), tinh_trang, goi_lai, tham_quan)


class LanThu(unittest.TestCase):
    def test_dem_tu_dau(self):
        a, b = lan(1, 9, q.CAN_NHAC), lan(2, 9, q.CAN_NHAC)
        self.assertEqual(q.lan_thu([], a), 1)
        self.assertEqual(q.lan_thu([a], b), 2)

    def test_moc_dem_lai(self):
        a = lan(1, 9, q.CAN_NHAC)
        moc = lan(2, 9, q.DA_THAM_QUAN)
        b = lan(3, 9, q.CAN_NHAC)
        self.assertEqual(q.lan_thu([a], moc), 1)  # bản thân mốc là lần 1
        self.assertEqual(q.lan_thu([a, moc], b), 2)  # mốc tính là lần 1, b là lần 2

    def test_bo_qua_lan_sau(self):
        a, b = lan(1, 9, q.CAN_NHAC), lan(5, 9, q.CAN_NHAC)
        self.assertEqual(q.lan_thu([a, b], a), 1)


class HanLienHe(unittest.TestCase):
    def test_l1_l2_l3_roi_tam_dung(self):
        c = lan(10, 9, q.CAN_NHAC)
        self.assertEqual(q.han_lien_he_tiep(c, 1), date(2026, 11, 11))
        self.assertEqual(q.han_lien_he_tiep(c, 2), date(2026, 11, 13))
        self.assertEqual(q.han_lien_he_tiep(c, 3), date(2026, 11, 17))
        self.assertIsNone(q.han_lien_he_tiep(c, 4))

    def test_ket_thuc(self):
        self.assertIsNone(q.han_lien_he_tiep(lan(10, 9, q.TU_CHOI), 1))
        self.assertIsNone(q.han_lien_he_tiep(lan(10, 9, q.NHAP_HOC), 1))

    def test_hen_goi_lai_thang_moi_quy_tac(self):
        c = lan(10, 9, q.CAN_NHAC, goi_lai=date(2026, 11, 20))
        self.assertEqual(q.han_lien_he_tiep(c, 5), date(2026, 11, 20))

    def test_chua_lien_lac(self):
        self.assertEqual(q.han_lien_he_tiep(lan(10, 9, q.CHUA_LIEN_LAC), 2), date(2026, 11, 11))
        self.assertIsNone(q.han_lien_he_tiep(lan(10, 9, q.CHUA_LIEN_LAC), 4))

    def test_da_hen_tham_quan(self):
        # Hẹn 15/11: nhắc xác nhận 14/11; gọi xác nhận xong thì nhắc hỏi cảm nhận 16/11.
        self.assertEqual(q.han_lien_he_tiep(lan(10, 9, q.DA_HEN, tham_quan=date(2026, 11, 15)), 1), date(2026, 11, 14))
        self.assertEqual(q.han_lien_he_tiep(lan(14, 9, q.DA_HEN, tham_quan=date(2026, 11, 15)), 1), date(2026, 11, 16))

    def test_dat_coc(self):
        self.assertEqual(q.han_lien_he_tiep(lan(10, 9, q.DAT_COC), 1), date(2026, 11, 17))

    def test_cau_hinh_doi_duoc(self):
        ch = dict(q.CAU_HINH_MAC_DINH, L1=2)
        self.assertEqual(q.han_lien_he_tiep(lan(10, 9, q.CAN_NHAC), 1, ch), date(2026, 11, 12))

    def test_muc_khan(self):
        hom_nay = date(2026, 11, 10)
        self.assertEqual(q.muc_khan(date(2026, 11, 9), hom_nay), "Quá hạn")
        self.assertEqual(q.muc_khan(hom_nay, hom_nay), "Hôm nay")
        self.assertEqual(q.muc_khan(date(2026, 11, 11), hom_nay), "Sắp tới")
        self.assertEqual(q.muc_khan(None, hom_nay), "")


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
        self.assertEqual(cuoi["L0006"]["Lần thứ"], "4")  # đề xuất tạm dừng
        self.assertEqual(cuoi["L0006"]["Hạn liên hệ tiếp"], "")


if __name__ == "__main__":
    unittest.main()
