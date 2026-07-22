
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO
import numpy as np
import pandas as pd

SHEETS = [
    "Cau_hinh","Don_vi","Thuong_hieu","Mau_xe","Dealer_KPI","Ban_hang","Ton_kho",
    "Dich_vu","Phu_tung","Tai_chinh","Forecast","Scenario","KPI","Du_an","Rui_ro",
    "RCM","Quyet_dinh","Hanh_dong","Lich_hop","Nghi_quyet","Dau_tu","Chat_luong_DL"
]

@dataclass
class HTAData:
    tables: dict[str,pd.DataFrame]
    reporting_period: str
    company_name: str

def load_master_excel(source: str | Path | BinaryIO) -> HTAData:
    tables = pd.read_excel(source, sheet_name=None, engine="openpyxl")
    missing=[s for s in SHEETS if s not in tables]
    if missing:
        raise ValueError(f"Thiếu sheet bắt buộc: {', '.join(missing)}")
    cfg=tables["Cau_hinh"].set_index("Thông số")["Giá trị"].to_dict()
    return HTAData(tables=tables, reporting_period=str(cfg.get("Kỳ báo cáo","")), company_name=str(cfg.get("Doanh nghiệp mô phỏng","Hà Thành Auto")))

def prepare_data(data: HTAData) -> HTAData:
    t=data.tables
    date_cols={
        "Ban_hang":["Tháng"],"Ton_kho":["Ngày báo cáo"],"Dich_vu":["Tháng"],"Phu_tung":["Ngày báo cáo"],
        "Tai_chinh":["Tháng"],"Forecast":["Tháng"],"Du_an":["Hạn hoàn thành"],
        "Quyet_dinh":["Ngày trình","Hạn quyết định"],"Hanh_dong":["Ngày giao","Hạn hoàn thành"],
        "Lich_hop":["Bắt đầu","Kết thúc"],"Nghi_quyet":["Ngày ban hành","Hạn hoàn thành"],
    }
    for sheet,cols in date_cols.items():
        for c in cols:
            t[sheet][c]=pd.to_datetime(t[sheet][c],errors="coerce")
    numeric_cols={
        "Dealer_KPI":["Doanh thu KH (tỷ)","Doanh thu TH (tỷ)","Xe bán","Doanh thu dịch vụ (tỷ)","Tồn kho xe (tỷ)","CSI","EBITDA (tỷ)"],
        "Ban_hang":["Số xe bán","Doanh thu (tỷ)","Giá vốn (tỷ)","Lợi nhuận gộp (tỷ)","Biên LN gộp"],
        "Ton_kho":["Số xe tồn","Bán TB/tháng","Số ngày tồn kho","Xe tồn >90 ngày","Giá trị tồn kho (tỷ)"],
        "Dich_vu":["Lệnh sửa chữa","Doanh thu công (tỷ)","Doanh thu phụ tùng (tỷ)","Chi phí bảo hành (tỷ)","Hiệu suất khoang","Năng suất KTV","Tỷ lệ sửa lại","CSI","Doanh thu dịch vụ (tỷ)"],
        "Tai_chinh":["Doanh thu KH","Doanh thu xe TH","Doanh thu dịch vụ TH","EBITDA KH","EBITDA TH","OCF","CAPEX"],
        "Forecast":["Doanh thu hợp nhất","EBITDA","Biên EBITDA"],
        "KPI":["Mục tiêu","Thực hiện","Trọng số","Tỷ lệ hoàn thành"],
        "Du_an":["Ngân sách (tỷ)","Tiến độ KH","Tiến độ TH","Sai lệch"],
        "Rui_ro":["Xác suất","Tác động","Điểm rủi ro"],
        "Hanh_dong":["Tiến độ"],"Nghi_quyet":["Tiến độ"],
        "Dau_tu":["Tổng mức đầu tư","NPV","IRR","Payback","Điểm rủi ro","Điểm chiến lược"],
    }
    for sheet,cols in numeric_cols.items():
        for c in cols:
            if c in t[sheet]:
                t[sheet][c]=pd.to_numeric(t[sheet][c],errors="coerce").fillna(0)
    # Recalculate formulas in Python for robustness on Streamlit.
    dk=t["Dealer_KPI"]
    dk["Tỷ lệ hoàn thành"]=np.where(dk["Doanh thu KH (tỷ)"]!=0,dk["Doanh thu TH (tỷ)"]/dk["Doanh thu KH (tỷ)"],0)
    dk["Biên EBITDA"]=np.where((dk["Doanh thu TH (tỷ)"]+dk["Doanh thu dịch vụ (tỷ)"])!=0,dk["EBITDA (tỷ)"]/(dk["Doanh thu TH (tỷ)"]+dk["Doanh thu dịch vụ (tỷ)"]),0)
    dk["Xếp hạng"]=dk["Tỷ lệ hoàn thành"].rank(method="min",ascending=False).astype(int)
    inv=t["Ton_kho"]
    inv["Số ngày tồn kho"]=np.where(inv["Bán TB/tháng"]!=0,inv["Số xe tồn"]/inv["Bán TB/tháng"]*30,0)
    risks=t["Rui_ro"]; risks["Điểm rủi ro"]=risks["Xác suất"]*risks["Tác động"]
    pr=t["Du_an"]; pr["Sai lệch"]=pr["Tiến độ TH"]-pr["Tiến độ KH"]
    return data

def executive_metrics(data: HTAData) -> dict:
    t=data.tables
    dk=t["Dealer_KPI"]; inv=t["Ton_kho"]; service=t["Dich_vu"]; risks=t["Rui_ro"]
    actions=t["Hanh_dong"]; decisions=t["Quyet_dinh"]; projects=t["Du_an"]
    revenue=float(dk["Doanh thu TH (tỷ)"].sum()+dk["Doanh thu dịch vụ (tỷ)"].sum())
    ebitda=float(dk["EBITDA (tỷ)"].sum())
    return {
        "revenue":revenue,
        "vehicle_units":int(dk["Xe bán"].sum()),
        "ebitda":ebitda,
        "ebitda_margin":ebitda/revenue if revenue else 0,
        "inventory_value":float(inv["Giá trị tồn kho (tỷ)"].sum()),
        "inventory_days":float(inv["Số ngày tồn kho"].mean()),
        "service_revenue":float(dk["Doanh thu dịch vụ (tỷ)"].sum()),
        "csi":float(dk["CSI"].mean()),
        "high_risks":int((risks["Điểm rủi ro"]>=15).sum()),
        "overdue_actions":int((actions["Trạng thái"]=="Quá hạn").sum()),
        "pending_decisions":int(decisions["Trạng thái"].isin(["Đang xem xét","Chờ quyết định"]).sum()),
        "projects_at_risk":int(projects["Trạng thái"].isin(["Cảnh báo","Theo dõi"]).sum()),
    }

def executive_brief(data: HTAData) -> list[str]:
    m=executive_metrics(data)
    notes=[]
    notes.append(f"Doanh thu hợp nhất giả định đạt {m['revenue']:,.1f} tỷ đồng; biên EBITDA {m['ebitda_margin']:.1%}.")
    if m["inventory_days"]>60:
        notes.append(f"Số ngày tồn kho bình quân {m['inventory_days']:.1f} ngày, vượt ngưỡng quản trị 60 ngày.")
    notes.append(f"Hệ thống có {m['high_risks']} rủi ro điểm cao, {m['overdue_actions']} hành động quá hạn và {m['pending_decisions']} hồ sơ đang chờ xử lý.")
    return notes

def dealer_health_score(df: pd.DataFrame) -> pd.Series:
    completion=np.clip(df["Tỷ lệ hoàn thành"],0,1.2)/1.2
    margin=np.clip(df["Biên EBITDA"],0,0.14)/0.14
    csi=np.clip((df["CSI"]-80)/20,0,1)
    return (completion*0.45+margin*0.30+csi*0.25)*100
