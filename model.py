
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO
import numpy as np
import pandas as pd

REQUIRED_SHEETS = [
    "Cau_hinh","Don_vi","Dealer_KPI","Ban_hang","Ton_kho","Dich_vu","Tai_chinh",
    "Forecast","KPI","Du_an","Rui_ro","RCM","Quyet_dinh","Hanh_dong","Dau_tu",
    "Customer_Funnel","Lead_Pipeline","Order_Delivery","Pricing_Discount","Dealer_PnL",
    "Working_Capital","Cash_Flow_13W","Workforce","Audit_Findings","Policy_Register",
    "ESG","Early_Warning","Executive_Brief","Data_Lineage","Action_Impact",
    "Scenario_Drivers","Board_Pack_Map","Validation_Rules"
]

@dataclass
class EEOSData:
    tables: dict[str,pd.DataFrame]
    company_name: str
    reporting_period: str

def load_master(source: str | Path | BinaryIO) -> EEOSData:
    tables = pd.read_excel(source,sheet_name=None,engine="openpyxl")
    missing = [s for s in REQUIRED_SHEETS if s not in tables]
    if missing:
        raise ValueError("Missing required sheets: " + ", ".join(missing))
    cfg = tables["Cau_hinh"].set_index("Thông số")["Giá trị"].to_dict()
    return EEOSData(tables,str(cfg.get("Doanh nghiệp mô phỏng","Hà Thành Auto")),str(cfg.get("Kỳ báo cáo","2026")))

def prepare(data: EEOSData) -> EEOSData:
    t=data.tables
    date_cols={
        "Ban_hang":["Tháng"],"Ton_kho":["Ngày báo cáo"],"Dich_vu":["Tháng"],
        "Forecast":["Tháng"],"Customer_Funnel":["Tháng"],"Lead_Pipeline":["Ngày tạo"],
        "Order_Delivery":["Ngày đặt","Ngày hứa giao","Ngày giao dự kiến/thực tế"],
        "Pricing_Discount":["Ngày"],"Cash_Flow_13W":["Bắt đầu"],
        "Audit_Findings":["Ngày ghi nhận","Hạn khắc phục"],"Action_Impact":["Due Date"]
    }
    for sheet,cols in date_cols.items():
        for col in cols:
            if col in t[sheet]:
                t[sheet][col]=pd.to_datetime(t[sheet][col],errors="coerce")
    f=t["Customer_Funnel"]
    f["Lead→Order"]=np.where(f["Lead"]!=0,f["Đơn hàng"]/f["Lead"],0)
    f["Order→Delivery"]=np.where(f["Đơn hàng"]!=0,f["Giao xe"]/f["Đơn hàng"],0)
    p=t["Dealer_PnL"]
    p["EBITDA"]=p["LN gộp xe"]+p["LN gộp dịch vụ"]-p["Chi phí nhân sự"]-p["Chi phí mặt bằng"]-p["Marketing"]-p["Chi phí khác"]
    p["Biên EBITDA"]=p["EBITDA"]/(p["Doanh thu xe"]+p["Doanh thu dịch vụ"])
    wc=t["Working_Capital"]
    wc["DIO"]=wc["Tồn kho"]/wc["Giá vốn tháng"]*30
    wc["DSO"]=wc["Phải thu"]/wc["Doanh thu tháng"]*30
    wc["DPO"]=wc["Phải trả"]/wc["Giá vốn tháng"]*30
    wc["Cash Conversion Cycle"]=wc["DIO"]+wc["DSO"]-wc["DPO"]
    return data

def filter_tables(data, brands=None, dealers=None):
    result={}
    for name,df in data.tables.items():
        x=df.copy()
        if brands and "Thương hiệu" in x.columns:
            x=x[x["Thương hiệu"].isin(brands)]
        if dealers:
            dealer_col=next((c for c in ["Đại lý","Tên đại lý"] if c in x.columns),None)
            if dealer_col:
                x=x[x[dealer_col].isin(dealers)]
        result[name]=x
    return EEOSData(result,data.company_name,data.reporting_period)

def metrics(data):
    t=data.tables; pnl=t["Dealer_PnL"]; cf=t["Cash_Flow_13W"]; e=t["Early_Warning"]
    revenue=(pnl["Doanh thu xe"]+pnl["Doanh thu dịch vụ"]).sum()
    ebitda=pnl["EBITDA"].sum()
    return {
        "revenue":float(revenue),"ebitda":float(ebitda),
        "margin":float(ebitda/revenue if revenue else 0),
        "cash_min":float(cf["Tiền cuối kỳ"].min()),
        "red_ews":int((e["Mức cảnh báo"]=="Red").sum()),
        "discount_leakage":float(t["Pricing_Discount"]["Discount leakage (tỷ)"].sum()),
        "overdue_actions":int((t["Action_Impact"]["Status"]=="Overdue").sum()),
        "pending_decisions":int(t["Quyet_dinh"]["Trạng thái"].isin(["Đang xem xét","Chờ quyết định"]).sum())
    }

def dealer_health(data):
    t=data.tables
    pnl=t["Dealer_PnL"][["Mã đại lý","Đại lý","Thương hiệu","EBITDA","Biên EBITDA"]]
    wc=t["Working_Capital"][["Mã đại lý","Cash Conversion Cycle"]]
    e=t["Early_Warning"][["Mã đại lý","Composite EWS","Mức cảnh báo"]]
    f=t["Customer_Funnel"].groupby("Mã đại lý",as_index=False)["Lead→Order"].mean()
    x=pnl.merge(wc,on="Mã đại lý").merge(e,on="Mã đại lý").merge(f,on="Mã đại lý")
    x["Health Score"]=(np.clip(x["Biên EBITDA"]/0.12,0,1)*.35+
                       np.clip(1-x["Cash Conversion Cycle"]/120,0,1)*.20+
                       np.clip(x["Lead→Order"]/0.14,0,1)*.20+
                       np.clip(1-x["Composite EWS"]/100,0,1)*.25)*100
    return x.sort_values("Health Score",ascending=False)

def dynamic_ews(data, weights):
    h=dealer_health(data).copy()
    h["Dynamic EWS"]=(
        h["Composite EWS"]*weights["base_risk"]+
        np.clip(h["Cash Conversion Cycle"]/120*100,0,100)*weights["working_capital"]+
        np.clip((0.14-h["Lead→Order"])/0.14*100,0,100)*weights["commercial"]+
        np.clip((0.10-h["Biên EBITDA"])/0.10*100,0,100)*weights["margin"]
    )
    h["Dynamic Level"]=np.select(
        [h["Dynamic EWS"]>=75,h["Dynamic EWS"]>=60],["Red","Amber"],default="Green"
    )
    return h.sort_values("Dynamic EWS",ascending=False)

def validate_data(data):
    issues=[]
    t=data.tables
    for sheet in REQUIRED_SHEETS:
        if sheet not in t:
            issues.append(["Critical",sheet,"Missing required sheet"])
    for sheet,id_col in [("Lead_Pipeline","Lead ID"),("Order_Delivery","Order ID"),("Pricing_Discount","Giao dịch")]:
        if t[sheet][id_col].duplicated().any():
            issues.append(["High",sheet,f"Duplicated {id_col}"])
    for sheet,col in [("Dealer_PnL","Doanh thu xe"),("Working_Capital","Tồn kho"),("Customer_Funnel","Lead")]:
        if (t[sheet][col]<0).any():
            issues.append(["High",sheet,f"Negative values in {col}"])
    ai=t["Action_Impact"]
    if ai["Owner"].isna().any() or ai["Due Date"].isna().any():
        issues.append(["High","Action_Impact","Missing owner or due date"])
    score=max(0,100-len(issues)*8)
    return score,pd.DataFrame(issues,columns=["Severity","Object","Issue"])
