#!/usr/bin/env python3
"""Thống kê chủ đề phụ huynh hỏi trên Messenger, từ tab Chủ đề của Sheet bot Casa dei Bambini.

Đầu vào: file CSV (hoặc XLSX nếu có openpyxl) xuất từ tab Chủ đề, hàng 1 là tiêu đề cột
(tiêu đề tiếng Việt như trên Sheet, hoặc khóa JSON của bot như `topics`).
Đầu ra: Markdown (mặc định) hoặc JSON gồm xếp hạng chủ đề, so với kỳ trước, cắt theo cơ sở,
độ tuổi, quảng cáo, tỷ lệ phải chuyển tư vấn viên và câu hỏi mẫu đã ẩn SĐT.
Không in Customer ID.

Ví dụ:
    python3 chu_de.py chu_de.csv
    python3 chu_de.py chu_de.csv --tu 2026-10-01 --den 2026-10-31 --co-so "Mỹ Đình"
    python3 chu_de.py chu_de.csv --now "2026-11-02 08:00" --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from casa_chung import (  # noqa: E402
    CO_SO,
    NHOM_TUOI,
    an_thong_tin,
    bang,
    bo_dau,
    chuan_hoa_co_so,
    doc_gio,
    doc_hang,
    gio_viet_nam,
    nhom_tuoi,
    pt,
)

SO_NGAY_MAC_DINH = 30
SO_MAU_MAC_DINH = 3

# Tiêu đề cột tab Chủ đề ↔ khóa JSON bot gửi (docs/google-sheet-leads.md của repo bot).
COT = OrderedDict(
    [
        ("time", "Thời gian"),
        ("customer_id", "Customer ID"),
        ("ad_title", "Quảng cáo"),
        ("campus", "Cơ sở/hệ"),
        ("kid_age", "Tuổi bé"),
        ("topics", "Chủ đề"),
        ("escalated", "Chuyển tư vấn viên"),
        ("question", "Câu hỏi"),
    ]
)

# Danh sách cố định trong app/topics.py của bot. Chủ đề lạ vẫn được đếm, đứng sau.
CHU_DE = [
    "Học phí",
    "Ưu đãi",
    "Chương trình/phương pháp",
    "Tiếng Anh/GV nước ngoài",
    "Giáo viên/tỷ lệ cô trò",
    "Cơ sở vật chất",
    "Ăn uống/thực đơn",
    "An toàn/sức khoẻ/camera",
    "Giờ học/đón trả/trông muộn",
    "Xe đưa đón",
    "Độ tuổi/nhập học/hồ sơ",
    "Học thử/tham quan",
    "Thích nghi/tâm lý bé",
    "So sánh trường khác",
    "Khác",
]
KHAC = "Khác"


@dataclass
class Tin:
    luc: datetime
    phu_huynh: str
    quang_cao: str
    co_so: str
    nhom_tuoi: str
    chu_de: list[str]
    chuyen_tvv: bool
    cau_hoi: str


def lay(hang: dict[str, str], khoa: str) -> str:
    muc_tieu = {bo_dau(COT[khoa]), bo_dau(khoa)}
    for k, v in hang.items():
        if bo_dau(k or "") in muc_tieu:
            return (v or "").strip()
    return ""


def tach_chu_de(s: str) -> list[str]:
    ra = []
    for phan in (s or "").split(","):
        phan = phan.strip()
        if not phan:
            continue
        ten = next((c for c in CHU_DE if bo_dau(c) == bo_dau(phan)), phan)
        if ten not in ra:
            ra.append(ten)
    return ra


def doc_tin(hang: list[dict[str, str]], ngay_tinh: datetime) -> tuple[list[Tin], int]:
    tin, loi = [], 0
    for i, h in enumerate(hang):
        if not any((v or "").strip() for v in h.values()):
            continue
        luc = doc_gio(lay(h, "time"))
        chu_de = tach_chu_de(lay(h, "topics"))
        if luc is None or not chu_de:
            loi += 1
            continue
        tin.append(
            Tin(
                luc=luc,
                # Không có Customer ID thì coi mỗi dòng là một phụ huynh khác nhau.
                phu_huynh=lay(h, "customer_id") or f"_dong_{i}",
                quang_cao=" ".join(lay(h, "ad_title").split()),
                co_so=chuan_hoa_co_so(lay(h, "campus")),
                nhom_tuoi=nhom_tuoi(lay(h, "kid_age"), ngay_tinh),
                chu_de=chu_de,
                chuyen_tvv=bo_dau(lay(h, "escalated")) in ("co", "yes", "true", "1"),
                cau_hoi=lay(h, "question"),
            )
        )
    return tin, loi


# ---------------------------------------------------------------- tính


def thu_tu(c: str) -> int:
    return CHU_DE.index(c) if c in CHU_DE else len(CHU_DE)


def dem(tin: list[Tin]) -> dict[str, dict]:
    """Mỗi chủ đề: số lượt hỏi, số phụ huynh khác nhau, số lượt phải chuyển tư vấn viên."""
    luot, ph, tvv = Counter(), defaultdict(set), Counter()
    for t in tin:
        for c in t.chu_de:
            luot[c] += 1
            ph[c].add(t.phu_huynh)
            tvv[c] += t.chuyen_tvv
    return {c: {"luot": luot[c], "phu_huynh": len(ph[c]), "chuyen_tvv": tvv[c]} for c in luot}


def xep_hang(so: dict[str, dict]) -> list[str]:
    """Theo số phụ huynh, rồi số lượt hỏi; "Khác" luôn đứng cuối vì không gợi ý được nội dung."""
    return sorted(so, key=lambda c: (c == KHAC, -so[c]["phu_huynh"], -so[c]["luot"], thu_tu(c), c))


def cau_mau(tin: list[Tin], chu_de: str, so_mau: int) -> list[str]:
    """Câu hỏi mẫu mới nhất của chủ đề, đã ẩn SĐT/email, bỏ câu trùng, mỗi phụ huynh một câu."""
    ra, da_co, da_hoi = [], set(), set()
    for t in sorted(tin, key=lambda t: t.luc, reverse=True):
        if chu_de not in t.chu_de or t.phu_huynh in da_hoi:
            continue
        cau = an_thong_tin(t.cau_hoi, 160)
        if not cau or bo_dau(cau) in da_co:
            continue
        ra.append(cau)
        da_co.add(bo_dau(cau))
        da_hoi.add(t.phu_huynh)
        if len(ra) >= so_mau:
            break
    return ra


def cat_theo(tin: list[Tin], thuoc_tinh: str, nhom: list[str] | None, top: int = 3) -> dict:
    """Mỗi nhóm (cơ sở, nhóm tuổi, quảng cáo): số phụ huynh và top chủ đề (trừ "Khác")."""
    gom: dict[str, list[Tin]] = defaultdict(list)
    for t in tin:
        gom[getattr(t, thuoc_tinh)].append(t)
    khoa = [n for n in (nhom or []) if gom.get(n)] + sorted(
        (k for k in gom if k not in (nhom or []) and k), key=lambda k: -len({t.phu_huynh for t in gom[k]})
    )
    ra = {}
    for k in khoa:
        so = dem(gom[k])
        ra[k] = {
            "phu_huynh": len({t.phu_huynh for t in gom[k]}),
            "top": [{"chu_de": c, **so[c]} for c in xep_hang(so) if c != KHAC][:top],
        }
    return ra


def lap_thong_ke(
    tin: list[Tin], tu: datetime, den: datetime, so_mau: int, loc: dict[str, str], dong_loi: int
) -> dict:
    """`tu`, `den`: ngày đầu và ngày cuối của kỳ (tính cả hai ngày)."""
    het = den + timedelta(days=1)
    so_ngay = (het - tu).days
    tu_truoc = tu - timedelta(days=so_ngay)

    def chon(t: Tin) -> bool:
        return all(
            not v or bo_dau(getattr(t, k)) == bo_dau(v) or (k == "quang_cao" and bo_dau(v) in bo_dau(t.quang_cao))
            for k, v in loc.items()
        )

    tin = [t for t in tin if chon(t)]
    ky = [t for t in tin if tu <= t.luc < het]
    truoc = [t for t in tin if tu_truoc <= t.luc < tu]
    so, so_truoc = dem(ky), dem(truoc)
    tong_ph = len({t.phu_huynh for t in ky})

    hang = []
    for c in xep_hang(so):
        s = so[c]
        p_truoc = so_truoc.get(c, {}).get("phu_huynh", 0)
        hang.append(
            {
                "chu_de": c,
                **s,
                "ty_le_phu_huynh": None if tong_ph == 0 else s["phu_huynh"] / tong_ph,
                "ty_le_chuyen_tvv": s["chuyen_tvv"] / s["luot"],
                "phu_huynh_ky_truoc": p_truoc,
                "chenh_phu_huynh": s["phu_huynh"] - p_truoc,
                "cau_mau": cau_mau(ky, c, so_mau),
            }
        )
    giam = [
        {"chu_de": c, "phu_huynh_ky_truoc": so_truoc[c]["phu_huynh"]}
        for c in xep_hang(so_truoc)
        if c not in so and c != KHAC
    ]
    return {
        "tu": tu.strftime("%Y-%m-%d"),
        "den": den.strftime("%Y-%m-%d"),
        "ky_truoc_tu": tu_truoc.strftime("%Y-%m-%d"),
        "ky_truoc_den": (tu - timedelta(days=1)).strftime("%Y-%m-%d"),
        "loc": {k: v for k, v in loc.items() if v},
        "so_tin": len(ky),
        "so_phu_huynh": tong_ph,
        "so_tin_ky_truoc": len(truoc),
        "so_phu_huynh_ky_truoc": len({t.phu_huynh for t in truoc}),
        "chu_de": hang,
        "khong_con_hoi": giam,
        "theo_co_so": cat_theo(ky, "co_so", CO_SO),
        "theo_tuoi": cat_theo(ky, "nhom_tuoi", NHOM_TUOI),
        "theo_quang_cao": cat_theo(ky, "quang_cao", None),
        "khong_tu_quang_cao": len({t.phu_huynh for t in ky if not t.quang_cao}),
        "dong_bo_qua": dong_loi,
    }


# ---------------------------------------------------------------- trình bày


def ngay(s: str) -> str:
    return datetime.strptime(s, "%Y-%m-%d").strftime("%d/%m/%Y")


def so_dau(x: int) -> str:
    return f"+{x}" if x > 0 else str(x)


def top_chu(nhom: dict) -> str:
    return "; ".join(f"{x['chu_de']} ({x['phu_huynh']})" for x in nhom["top"]) or "–"


def markdown(tk: dict) -> str:
    nhan = {"co_so": "cơ sở", "nhom_tuoi": "nhóm tuổi", "quang_cao": "quảng cáo"}
    loc = ", ".join(f"{nhan.get(k, k)}: {v}" for k, v in tk["loc"].items())
    out = [
        f"# Chủ đề phụ huynh hỏi {ngay(tk['tu'])} – {ngay(tk['den'])}",
        "",
        f"_Từ tab Chủ đề của Sheet bot Messenger{'. Lọc ' + loc if loc else ''}. "
        f"Kỳ so sánh: {ngay(tk['ky_truoc_tu'])} – {ngay(tk['ky_truoc_den'])}._",
        "",
        f"**{tk['so_phu_huynh']} phụ huynh** hỏi **{tk['so_tin']} tin** có chủ đề "
        f"(kỳ trước {tk['so_phu_huynh_ky_truoc']} phụ huynh, {tk['so_tin_ky_truoc']} tin).",
        "",
        "## Xếp hạng chủ đề",
        "",
    ]
    if not tk["chu_de"]:
        out += ["Không có tin nào trong kỳ.", ""]
        return "\n".join(out)
    out.append(
        bang(
            ["#", "Chủ đề", "Phụ huynh", "% phụ huynh", "Lượt hỏi", "Kỳ trước", "Chênh", "Phải chuyển TVV"],
            [
                [
                    i,
                    c["chu_de"],
                    c["phu_huynh"],
                    pt(c["ty_le_phu_huynh"]),
                    c["luot"],
                    c["phu_huynh_ky_truoc"],
                    so_dau(c["chenh_phu_huynh"]),
                    f"{c['chuyen_tvv']}/{c['luot']}",
                ]
                for i, c in enumerate(tk["chu_de"], 1)
            ],
        )
    )
    out += [
        "",
        "Xếp theo số phụ huynh khác nhau (một phụ huynh hỏi nhiều lần chỉ tính một). "
        "Cột cuối: số lượt bot phải chuyển tư vấn viên, cao là dấu hiệu nội dung hiện có chưa trả lời đủ.",
    ]
    if tk["khong_con_hoi"]:
        out += [
            "",
            "Kỳ trước có hỏi, kỳ này không ai hỏi: "
            + "; ".join(f"{x['chu_de']} ({x['phu_huynh_ky_truoc']})" for x in tk["khong_con_hoi"])
            + ".",
        ]
    out += ["", "## Theo cơ sở", "", bang(["Cơ sở", "Phụ huynh", "Hỏi nhiều nhất"], [[k, v["phu_huynh"], top_chu(v)] for k, v in tk["theo_co_so"].items()])]
    out += ["", "## Theo độ tuổi", "", bang(["Nhóm tuổi", "Phụ huynh", "Hỏi nhiều nhất"], [[k, v["phu_huynh"], top_chu(v)] for k, v in tk["theo_tuoi"].items()])]
    out += ["", "## Theo quảng cáo", ""]
    if tk["theo_quang_cao"]:
        out.append(bang(["Quảng cáo", "Phụ huynh", "Hỏi nhiều nhất"], [[k, v["phu_huynh"], top_chu(v)] for k, v in tk["theo_quang_cao"].items()]))
    else:
        out.append("Không có tin nào từ quảng cáo.")
    out += ["", f"{tk['khong_tu_quang_cao']} phụ huynh nhắn không qua quảng cáo."]
    out += ["", "## Câu hỏi mẫu", "", "_Đã thay SĐT, email bằng [SĐT], [email]. Đọc lại trước khi trích ra ngoài._"]
    for c in tk["chu_de"]:
        if c["chu_de"] == KHAC or not c["cau_mau"]:
            continue
        out += ["", f"**{c['chu_de']}**", ""] + [f"- {q}" for q in c["cau_mau"]]
    if tk["dong_bo_qua"]:
        out += ["", "## Ghi chú về dữ liệu", "", f"- {tk['dong_bo_qua']} dòng bị bỏ qua vì không đọc được thời gian hoặc không có chủ đề."]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- chạy


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Thống kê chủ đề phụ huynh hỏi (tab Chủ đề).")
    p.add_argument("file", type=Path, help="CSV hoặc XLSX xuất từ tab Chủ đề")
    p.add_argument("--tu", help="Ngày đầu kỳ (YYYY-MM-DD). Mặc định: 30 ngày trước ngày --den.")
    p.add_argument("--den", help="Ngày cuối kỳ, tính cả ngày này (YYYY-MM-DD). Mặc định: hôm qua.")
    p.add_argument("--now", help="Giờ chạy, giờ Việt Nam (YYYY-MM-DD HH:MM). Mặc định: bây giờ.")
    p.add_argument("--co-so", help="Chỉ lấy một cơ sở: Chùa Láng, Mỹ Đình, Kim Mã")
    p.add_argument("--nhom-tuoi", help='Chỉ lấy một nhóm tuổi, vd "3 – <5 tuổi"')
    p.add_argument("--quang-cao", help="Chỉ lấy quảng cáo có tên chứa chữ này")
    p.add_argument("--mau", type=int, default=SO_MAU_MAC_DINH, help="Số câu hỏi mẫu mỗi chủ đề")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    a = p.parse_args(argv)

    bay_gio = doc_gio(a.now) if a.now else gio_viet_nam()
    if bay_gio is None:
        p.error("--now không đúng dạng YYYY-MM-DD HH:MM")
    den = doc_gio(a.den) if a.den else (bay_gio - timedelta(days=1))
    if den is None:
        p.error("--den không đúng dạng YYYY-MM-DD")
    den = den.replace(hour=0, minute=0, second=0, microsecond=0)
    tu = doc_gio(a.tu) if a.tu else den - timedelta(days=SO_NGAY_MAC_DINH - 1)
    if tu is None or tu > den:
        p.error("--tu không đúng dạng YYYY-MM-DD hoặc sau --den")
    tu = tu.replace(hour=0, minute=0, second=0, microsecond=0)

    co_so = chuan_hoa_co_so(a.co_so) if a.co_so else ""
    tin, loi = doc_tin(doc_hang(a.file, "Chủ đề"), bay_gio)
    tk = lap_thong_ke(tin, tu, den, a.mau, {"co_so": co_so, "nhom_tuoi": a.nhom_tuoi or "", "quang_cao": a.quang_cao or ""}, loi)
    if a.format == "json":
        print(json.dumps(tk, ensure_ascii=False, indent=2))
    else:
        print(markdown(tk), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
