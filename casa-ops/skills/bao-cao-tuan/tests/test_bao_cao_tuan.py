"""Kiểm tra script báo cáo tuần bằng dữ liệu giả (leads_mau.csv).

Chạy: python3 -m unittest discover -s casa-ops/skills/bao-cao-tuan/tests -v
Kỳ báo cáo: tuần 26/10 – 01/11/2026, chạy lúc 08:00 thứ Hai 02/11/2026.
"""

import io
import re
import sys
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path

THU_MUC = Path(__file__).resolve().parent
sys.path.insert(0, str(THU_MUC.parent / "scripts"))

import bao_cao_tuan as bct  # noqa: E402

MAU = THU_MUC / "leads_mau.csv"
BAY_GIO = datetime(2026, 11, 2, 8, 0)


def lap():
    du_lieu = bct.doc_du_lieu(bct.doc_hang(MAU), BAY_GIO)
    bat_dau = bct.dau_tuan(BAY_GIO) - bct.timedelta(days=7)
    return bct.lap_bao_cao(du_lieu, bat_dau, BAY_GIO)


class ChuanHoa(unittest.TestCase):
    def test_co_so(self):
        cases = {
            "Hongkong": "Chùa Láng",
            "cơ sở HK": "Chùa Láng",
            "185 Huỳnh Thúc Khang": "Chùa Láng",
            "FLC": "Mỹ Đình",
            "Phạm Hùng": "Mỹ Đình",
            "song ngữ": "Kim Mã",
            "Vạn Phúc": "Kim Mã",
            "hệ quốc tế": "Quốc tế – chưa rõ cơ sở",
            "Mỹ Đình hoặc Kim Mã": "Chưa rõ",
            "": "Chưa rõ",
            "gần nhà": "Chưa rõ",
            "gần Lăng Bác": "Chưa rõ",
        }
        for vao, ra in cases.items():
            with self.subTest(vao=vao):
                self.assertEqual(bct.chuan_hoa_co_so(vao), ra)

    def test_tuoi(self):
        cases = {
            "18 tháng": "15 tháng – <2 tuổi",
            "1 tuổi": "15 tháng – <2 tuổi",
            "1 tuổi rưỡi": "15 tháng – <2 tuổi",
            "dưới 2 tuổi": "15 tháng – <2 tuổi",
            "10 tháng": "Ngoài độ tuổi",
            "2 tuổi": "2 – <3 tuổi",
            "hai tuổi": "2 – <3 tuổi",
            "2 tuổi 8 tháng": "2 – <3 tuổi",
            "3 tuổi rưỡi": "3 – <5 tuổi",
            "3-4 tuổi": "3 – <5 tuổi",
            "sinh năm 2022": "3 – <5 tuổi",
            "sinh tháng 3/2023": "3 – <5 tuổi",
            "5 tuổi": "5 – 6 tuổi",
            "6 tuổi": "5 – 6 tuổi",
            "2t": "2 – <3 tuổi",
            "bé 3t rồi": "3 – <5 tuổi",
            "30 tháng tuổi": "2 – <3 tuổi",
            "7 tuổi": "Ngoài độ tuổi",
            "": "Chưa rõ",
            "bé nhà mình còn nhỏ": "Chưa rõ",
        }
        for vao, ra in cases.items():
            with self.subTest(vao=vao):
                self.assertEqual(bct.nhom_tuoi(vao, BAY_GIO), ra)

    def test_giai_doan(self):
        self.assertEqual(bct.tach_giai_doan("Đã có SĐT · Đã liên hệ"), ("Đã có SĐT", True))
        self.assertEqual(bct.tach_giai_doan("Muốn hẹn tham quan/học thử"), (bct.MUON_HEN, False))
        self.assertEqual(bct.tach_giai_doan("Hẹn tham quan/học thử"), (bct.MUON_HEN, False))
        self.assertEqual(bct.tach_giai_doan("Không quan tâm"), (bct.KHONG_QUAN_TAM, False))

    def test_che_sdt(self):
        self.assertEqual(bct.che_sdt("090 000 0404"), "…0404")
        self.assertEqual(bct.che_sdt(""), "…")


class ChiSo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bc = lap()
        cls.t = cls.bc["tuan"]
        cls.tr = cls.bc["tuan_truoc"]

    def test_ky(self):
        self.assertEqual(self.t["bat_dau"], "2026-10-26")
        self.assertEqual(self.t["ket_thuc"], "2026-11-01")

    def test_lead_moi(self):
        # Gồm lead lúc 00:00 thứ Hai, 23:30 Chủ nhật; không gồm lead 00:00 thứ Hai tuần sau.
        self.assertEqual(self.t["lead_moi"], 9)
        self.assertEqual(self.tr["lead_moi"], 3)

    def test_giai_doan(self):
        self.assertEqual(
            self.t["theo_giai_doan"],
            {
                "Mới": 1,
                "Đã biết tuổi/cơ sở": 2,
                "Đã có SĐT": 2,
                "Muốn hẹn tham quan/học thử": 1,
                "Đã hẹn tham quan/học thử": 2,
                "Không quan tâm": 1,
            },
        )
        self.assertEqual(self.t["da_lien_he"], 2)

    def test_co_so(self):
        self.assertEqual(
            self.t["theo_co_so"],
            {"Chùa Láng": 2, "Mỹ Đình": 2, "Kim Mã": 3, "Quốc tế – chưa rõ cơ sở": 1, "Chưa rõ": 1},
        )

    def test_tuoi(self):
        self.assertEqual(
            self.t["theo_tuoi"],
            {
                "15 tháng – <2 tuổi": 2,
                "2 – <3 tuổi": 1,
                "3 – <5 tuổi": 3,
                "5 – 6 tuổi": 1,
                "Ngoài độ tuổi": 1,
                "Chưa rõ": 1,
            },
        )

    def test_sdt_hen(self):
        # "Muốn hẹn" chưa chốt không được tính là đã hẹn.
        self.assertEqual(self.t["co_sdt"], 6)
        self.assertEqual(self.t["da_hen"], 2)
        self.assertEqual(self.t["muon_hen_chua_chot"], 1)
        self.assertAlmostEqual(self.t["ty_le_sdt_hen"], 2 / 6)
        self.assertAlmostEqual(self.tr["ty_le_sdt_hen"], 1 / 2)

    def test_quang_cao(self):
        self.assertEqual(self.t["lead_tu_quang_cao"], 6)
        self.assertEqual(self.t["theo_quang_cao"]["QC Cambridge T10"]["lead"], 3)
        self.assertEqual(self.t["theo_quang_cao"]["QC Cambridge T10"]["co_sdt"], 3)
        self.assertEqual(self.t["theo_quang_cao"]["QC Học phí"]["lead"], 3)
        self.assertEqual(self.t["theo_quang_cao"]["QC Học phí"]["co_sdt"], 1)
        self.assertEqual(self.tr["lead_tu_quang_cao"], 2)

    def test_so_sanh(self):
        ss = self.bc["so_sanh"]["lead_moi"]
        self.assertEqual(ss["chenh"], 6)
        self.assertAlmostEqual(ss["phan_tram"], 2.0)

    def test_cho_lien_he(self):
        ds = self.bc["cho_lien_he_qua_48h"]
        # Bình (lead tuần trước) đứng đầu vì chờ lâu nhất; Hoa muốn hẹn nhưng chưa ai liên hệ.
        # Minh mới chờ 47 giờ, Nam 8 giờ: chưa vào danh sách. Đã liên hệ, đã hẹn, không quan tâm: không vào.
        self.assertEqual([x["ten"] for x in ds], ["Bình Thử", "Hoa Thử"])
        self.assertEqual(ds[0]["sdt_4_so"], "…0412")
        self.assertEqual(ds[0]["gio_cho"], 262)
        self.assertEqual(ds[1]["gio_cho"], 138)

    def test_ghi_chu(self):
        g = self.bc["ghi_chu_du_lieu"]
        self.assertEqual(g["hang_bo_qua_loi_ngay"], 1)
        self.assertEqual(g["hang_trung_customer_id"], 1)


class TrinhBay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        f = io.StringIO()
        with redirect_stdout(f):
            bct.main([str(MAU), "--now", "2026-11-02 08:00"])
        cls.md = f.getvalue()

    def test_khong_lo_sdt(self):
        self.assertIsNone(re.search(r"(?<!\d)0\d{9}(?!\d)", self.md))
        self.assertIsNone(re.search(r"0\d{2}[ .]\d{3}[ .]\d{4}", self.md))

    def test_khong_lo_customer_id(self):
        self.assertNotIn("GIA-", self.md)

    def test_noi_dung(self):
        self.assertIn("Báo cáo lead tuần 26/10/2026 – 01/11/2026", self.md)
        self.assertIn("**9 lead mới**", self.md)
        self.assertIn("33,3%", self.md)
        self.assertIn("Bình Thử (…0412)", self.md)
        self.assertIn("Hoa Thử (…0402)", self.md)
        self.assertNotIn("Minh Thử (…0404)", self.md)

    def test_tuan_chon(self):
        f = io.StringIO()
        with redirect_stdout(f):
            bct.main([str(MAU), "--tuan", "2026-10-22", "--now", "2026-11-02 08:00"])
        self.assertIn("Báo cáo lead tuần 19/10/2026 – 25/10/2026", f.getvalue())
        self.assertIn("**3 lead mới**", f.getvalue())


class DuLieuEval(unittest.TestCase):
    def test_scaffold_giong_file_mau(self):
        """Script tạo dữ liệu của bộ eval phải ghi đúng nội dung leads_mau.csv."""
        sh = (THU_MUC.parents[2] / "evals" / "bao-cao-tuan-du-lieu-mau" / "tao-du-lieu.sh").read_text(encoding="utf-8")
        m = re.search(r"<<'CSV'\n(.*?)\nCSV\n", sh, re.S)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1) + "\n", MAU.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
