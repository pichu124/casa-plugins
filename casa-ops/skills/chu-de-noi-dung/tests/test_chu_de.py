"""Kiểm tra script thống kê chủ đề bằng dữ liệu giả (chu_de_mau.csv).

Chạy: python3 -m unittest discover -s casa-ops/skills/chu-de-noi-dung/tests -v
Kỳ mặc định khi chạy lúc 08:00 02/11/2026: 03/10 – 01/11/2026; kỳ trước 03/09 – 02/10/2026.
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

import chu_de as cd  # noqa: E402

MAU = THU_MUC / "chu_de_mau.csv"
BAY_GIO = "2026-11-02 08:00"


def chay(*args) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        cd.main([str(MAU), "--now", BAY_GIO, *args])
    return f.getvalue()


def thong_ke(**loc):
    tin, loi = cd.doc_tin(cd.doc_hang(MAU, "Chủ đề"), datetime(2026, 11, 2, 8))
    loc = {"co_so": "", "nhom_tuoi": "", "quang_cao": ""} | loc
    return cd.lap_thong_ke(tin, datetime(2026, 10, 3), datetime(2026, 11, 1), 3, loc, loi)


class TachChuDe(unittest.TestCase):
    def test_tach(self):
        self.assertEqual(cd.tach_chu_de("Học phí, Ưu đãi"), ["Học phí", "Ưu đãi"])
        self.assertEqual(cd.tach_chu_de("hoc phi,  Hoc phi"), ["Học phí"])
        self.assertEqual(cd.tach_chu_de("Chủ đề mới"), ["Chủ đề mới"])
        self.assertEqual(cd.tach_chu_de(""), [])


class ThongKe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tk = thong_ke()
        cls.cd = {c["chu_de"]: c for c in cls.tk["chu_de"]}

    def test_ky(self):
        self.assertEqual((self.tk["tu"], self.tk["den"]), ("2026-10-03", "2026-11-01"))
        self.assertEqual((self.tk["ky_truoc_tu"], self.tk["ky_truoc_den"]), ("2026-09-03", "2026-10-02"))

    def test_tong(self):
        # Gồm tin 00:00 ngày đầu kỳ; không gồm tin 00:30 ngày sau kỳ; bỏ 2 dòng lỗi.
        self.assertEqual(self.tk["so_tin"], 16)
        self.assertEqual(self.tk["so_phu_huynh"], 13)
        self.assertEqual(self.tk["so_phu_huynh_ky_truoc"], 5)
        self.assertEqual(self.tk["dong_bo_qua"], 2)

    def test_xep_hang(self):
        thu_tu = [c["chu_de"] for c in self.tk["chu_de"]]
        self.assertEqual(thu_tu[:3], ["Học phí", "Chương trình/phương pháp", "Tiếng Anh/GV nước ngoài"])
        self.assertEqual(thu_tu[-1], "Khác")  # "Khác" luôn cuối

    def test_hoc_phi(self):
        h = self.cd["Học phí"]
        # 7 lượt hỏi nhưng chỉ 6 phụ huynh: một phụ huynh hỏi hai lần.
        self.assertEqual((h["luot"], h["phu_huynh"], h["chuyen_tvv"]), (7, 6, 2))
        self.assertEqual((h["phu_huynh_ky_truoc"], h["chenh_phu_huynh"]), (2, 4))
        self.assertAlmostEqual(h["ty_le_phu_huynh"], 6 / 13)

    def test_khong_con_hoi(self):
        self.assertEqual(self.tk["khong_con_hoi"], [{"chu_de": "Xe đưa đón", "phu_huynh_ky_truoc": 1}])

    def test_theo_co_so(self):
        cs = self.tk["theo_co_so"]
        self.assertEqual({k: v["phu_huynh"] for k, v in cs.items()}, {"Chùa Láng": 4, "Mỹ Đình": 6, "Kim Mã": 3})
        self.assertEqual(cs["Mỹ Đình"]["top"][0], {"chu_de": "Học phí", "luot": 6, "phu_huynh": 5, "chuyen_tvv": 2})
        self.assertNotIn("Khác", [x["chu_de"] for v in cs.values() for x in v["top"]])

    def test_theo_tuoi(self):
        self.assertEqual(
            {k: v["phu_huynh"] for k, v in self.tk["theo_tuoi"].items()},
            {"15 tháng – <2 tuổi": 1, "2 – <3 tuổi": 3, "3 – <5 tuổi": 7, "5 – 6 tuổi": 2},
        )

    def test_theo_quang_cao(self):
        qc = self.tk["theo_quang_cao"]
        self.assertEqual(list(qc), ["QC Học phí", "QC Cambridge T10"])
        self.assertEqual(qc["QC Học phí"]["phu_huynh"], 5)
        self.assertEqual(
            [x["chu_de"] for x in qc["QC Cambridge T10"]["top"][:2]],
            ["Chương trình/phương pháp", "Tiếng Anh/GV nước ngoài"],
        )
        self.assertEqual(self.tk["khong_tu_quang_cao"], 4)

    def test_cau_mau(self):
        mau = self.cd["Học phí"]["cau_mau"]
        self.assertEqual(len(mau), 3)
        self.assertEqual(mau[0], "Lớp 5 tuổi học phí bao nhiêu ạ")  # mới nhất trước
        self.assertIn("Học phí bao nhiêu em gọi chị [SĐT] nhé", mau)

    def test_loc_co_so(self):
        tk = thong_ke(co_so="Mỹ Đình")
        self.assertEqual(tk["so_phu_huynh"], 6)
        self.assertEqual(tk["chu_de"][0]["chu_de"], "Học phí")

    def test_loc_quang_cao(self):
        tk = thong_ke(quang_cao="cambridge")
        self.assertEqual(tk["so_phu_huynh"], 4)


class TrinhBay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.md = chay()

    def test_khong_lo_sdt(self):
        self.assertIsNone(re.search(r"(?<!\d)0\d{9}(?!\d)", self.md))

    def test_khong_lo_customer_id(self):
        self.assertNotIn("GIA-", self.md)

    def test_noi_dung(self):
        self.assertIn("Chủ đề phụ huynh hỏi 03/10/2026 – 01/11/2026", self.md)
        self.assertIn("**13 phụ huynh**", self.md)
        self.assertIn("| 1 | Học phí | 6 | 46,2% | 7 | 2 | +4 | 2/7 |", self.md)

    def test_tham_so(self):
        md = chay("--tu", "2026-09-01", "--den", "2026-09-30", "--co-so", "Kim Mã")
        self.assertIn("Chủ đề phụ huynh hỏi 01/09/2026 – 30/09/2026", md)
        self.assertIn("cơ sở: Kim Mã", md)
        self.assertIn("**2 phụ huynh**", md)


class DuLieuEval(unittest.TestCase):
    def test_scaffold_giong_file_mau(self):
        """Script tạo dữ liệu của bộ eval phải ghi đúng nội dung chu_de_mau.csv."""
        sh = (THU_MUC.parents[2] / "evals" / "chu-de-noi-dung-du-lieu-mau" / "tao-du-lieu.sh").read_text(encoding="utf-8")
        m = re.search(r"<<'CSV'\n(.*?)\nCSV\n", sh, re.S)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1) + "\n", MAU.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
