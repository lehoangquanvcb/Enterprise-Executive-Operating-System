
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO
import numpy as np, pandas as pd

REQUIRED=["Cau_hinh","Don_vi","Dealer_KPI","Ban_hang","Ton_kho","Dich_vu","Phu_tung","Tai_chinh",
"Forecast","Scenario","KPI","Du_an","Rui_ro","RCM","Quyet_dinh","Hanh_dong","Lich_hop","Nghi_quyet",
"Dau_tu","Chat_luong_DL","Strategy_Map","KPI_Tree","Customer_Funnel","Lead_Pipeline","Order_Delivery",
"Pricing_Discount","Dealer_PnL","Working_Capital","Cash_Flow_13W","Workforce","Vendor_Performance",
"Audit_Findings","Policy_Register","ESG","Early_Warning","Executive_Brief","Data_Lineage",
"Action_Impact","Scenario_Drivers","Board_Pack_Map","Validation_Rules"]

@dataclass
class EEOSData:
    tables:dict[str,pd.DataFrame]; company_name:str; reporting_period:str

def load_master(source: str|Path|BinaryIO)->EEOSData:
    t=pd.read_excel(source,sheet_name=None,engine="openpyxl")
    miss=[s for s in REQUIRED if s not in t]
    if miss: raise ValueError("Missing sheets: "+", ".join(miss))
    cfg=t["Cau_hinh"].set_index("Thông số")["Giá trị"].to_dict()
    return EEOSData(t,str(cfg.get("Doanh nghiệp mô phỏng","Hà Thành Auto")),str(cfg.get("Kỳ báo cáo","2026")))

def prepare(d):
    t=d.tables
    dates={"Ban_hang":["Tháng"],"Ton_kho":["Ngày báo cáo"],"Dich_vu":["Tháng"],"Tai_chinh":["Tháng"],
    "Forecast":["Tháng"],"Customer_Funnel":["Tháng"],"Lead_Pipeline":["Ngày tạo"],
    "Order_Delivery":["Ngày đặt","Ngày hứa giao","Ngày giao dự kiến/thực tế"],"Pricing_Discount":["Ngày"],
    "Cash_Flow_13W":["Bắt đầu"],"Audit_Findings":["Ngày ghi nhận","Hạn khắc phục"],"Action_Impact":["Due Date"]}
    for s,cs in dates.items():
        for c in cs:
            if c in t[s].columns:t[s][c]=pd.to_datetime(t[s][c],errors="coerce")
    f=t["Customer_Funnel"]; f["Lead→Order"]=np.where(f["Lead"]>0,f["Đơn hàng"]/f["Lead"],0)
    f["Order→Delivery"]=np.where(f["Đơn hàng"]>0,f["Giao xe"]/f["Đơn hàng"],0)
    f["Lead→Delivery"]=np.where(f["Lead"]>0,f["Giao xe"]/f["Lead"],0)
    p=t["Dealer_PnL"]; p["EBITDA"]=p["LN gộp xe"]+p["LN gộp dịch vụ"]-p["Chi phí nhân sự"]-p["Chi phí mặt bằng"]-p["Marketing"]-p["Chi phí khác"]
    p["Biên EBITDA"]=np.where((p["Doanh thu xe"]+p["Doanh thu dịch vụ"])>0,p["EBITDA"]/(p["Doanh thu xe"]+p["Doanh thu dịch vụ"]),0)
    wc=t["Working_Capital"]; wc["DIO"]=wc["Tồn kho"]/wc["Giá vốn tháng"]*30; wc["DSO"]=wc["Phải thu"]/wc["Doanh thu tháng"]*30
    wc["DPO"]=wc["Phải trả"]/wc["Giá vốn tháng"]*30; wc["Cash Conversion Cycle"]=wc["DIO"]+wc["DSO"]-wc["DPO"]
    return d

def filter_data(d,brands=None,dealers=None):
    out={}
    dealer_codes=None
    if dealers:
        dm=d.tables["Don_vi"]; dealer_codes=set(dm[dm["Tên đại lý"].isin(dealers)]["Mã đại lý"])
    for n,df in d.tables.items():
        x=df.copy()
        if brands and "Thương hiệu" in x:x=x[x["Thương hiệu"].isin(brands)]
        if dealers:
            if "Đại lý" in x:x=x[x["Đại lý"].isin(dealers)]
            elif "Tên đại lý" in x:x=x[x["Tên đại lý"].isin(dealers)]
            elif "Mã đại lý" in x:x=x[x["Mã đại lý"].isin(dealer_codes)]
        out[n]=x
    return EEOSData(out,d.company_name,d.reporting_period)

def metrics(d):
    t=d.tables;p=t["Dealer_PnL"];rev=(p["Doanh thu xe"]+p["Doanh thu dịch vụ"]).sum();eb=p["EBITDA"].sum()
    delivered=t["Order_Delivery"]; delivered=delivered[delivered["Đúng hạn"].isin(["Yes","No"])]
    return {"revenue":float(rev),"ebitda":float(eb),"margin":float(eb/rev if rev else 0),
    "cash_min":float(t["Cash_Flow_13W"]["Tiền cuối kỳ"].min()),"red_ews":int((t["Early_Warning"]["Mức cảnh báo"]=="Red").sum()),
    "discount":float(t["Pricing_Discount"]["Discount leakage (tỷ)"].sum()),"overdue":int((t["Action_Impact"]["Status"]=="Overdue").sum()),
    "decisions":int(t["Quyet_dinh"]["Trạng thái"].isin(["Đang xem xét","Chờ quyết định"]).sum()),
    "conversion":float(t["Customer_Funnel"]["Lead→Order"].mean()),"otd":float((delivered["Đúng hạn"]=="Yes").mean() if len(delivered) else 0)}

def dealer_health(d):
    t=d.tables
    x=t["Dealer_PnL"][["Mã đại lý","Đại lý","Thương hiệu","EBITDA","Biên EBITDA"]].merge(
      t["Working_Capital"][["Mã đại lý","DIO","Cash Conversion Cycle"]],on="Mã đại lý").merge(
      t["Early_Warning"][["Mã đại lý","Composite EWS","Mức cảnh báo"]],on="Mã đại lý").merge(
      t["Customer_Funnel"].groupby("Mã đại lý",as_index=False)[["Lead→Order","Order→Delivery"]].mean(),on="Mã đại lý")
    x["Health Score"]=(np.clip(x["Biên EBITDA"]/.12,0,1)*.30+np.clip(1-x["Cash Conversion Cycle"]/120,0,1)*.20+
    np.clip(x["Lead→Order"]/.14,0,1)*.20+np.clip(x["Order→Delivery"]/.92,0,1)*.10+
    np.clip(1-x["Composite EWS"]/100,0,1)*.20)*100
    return x.sort_values("Health Score",ascending=False)

def dynamic_ews(d,w):
    h=dealer_health(d).copy()
    h["Dynamic EWS"]=h["Composite EWS"]*w["base"]+np.clip(h["Cash Conversion Cycle"]/120*100,0,100)*w["wc"]+\
    np.clip((.14-h["Lead→Order"])/.14*100,0,100)*w["commercial"]+np.clip((.10-h["Biên EBITDA"])/.10*100,0,100)*w["margin"]
    h["Dynamic Level"]=np.select([h["Dynamic EWS"]>=75,h["Dynamic EWS"]>=60],["Red","Amber"],default="Green")
    return h.sort_values("Dynamic EWS",ascending=False)

def validate_data(d):
    issues=[];t=d.tables
    for s in REQUIRED:
        if s not in t:issues.append(["Critical",s,"Required sheet missing"])
    dealer_codes=set(t["Don_vi"]["Mã đại lý"].dropna())
    for s in ["Dealer_PnL","Working_Capital","Early_Warning","Customer_Funnel"]:
        invalid=set(t[s]["Mã đại lý"].dropna())-dealer_codes
        if invalid:issues.append(["Critical",s,f"Unknown dealer codes: {len(invalid)}"])
    for s,c in [("Lead_Pipeline","Lead ID"),("Order_Delivery","Order ID"),("Pricing_Discount","Giao dịch")]:
        if t[s][c].duplicated().any():issues.append(["High",s,f"Duplicate {c}"])
    for s,c in [("Dealer_PnL","Doanh thu xe"),("Working_Capital","Tồn kho"),("Customer_Funnel","Lead")]:
        if (t[s][c]<0).any():issues.append(["High",s,f"Negative {c}"])
    a=t["Action_Impact"]
    if a["Owner"].isna().any() or a["Due Date"].isna().any():issues.append(["High","Action_Impact","Owner or due date missing"])
    score=max(0,100-len(issues)*8)
    return score,pd.DataFrame(issues,columns=["Severity","Object","Issue"])

def scenario_output(d,volume,price,discount,service_growth,personnel_growth,inventory_reduction):
    p=d.tables["Dealer_PnL"]; rev_vehicle=p["Doanh thu xe"].sum();rev_service=p["Doanh thu dịch vụ"].sum()
    base_rev=rev_vehicle+rev_service;base_eb=p["EBITDA"].sum()
    rev=rev_vehicle*(1+volume+price)+rev_service*(1+service_growth)
    eb=base_eb+rev_vehicle*(volume*.075+price*.68-discount*.80)+rev_service*service_growth*.35-p["Chi phí nhân sự"].sum()*personnel_growth
    cash=inventory_reduction*(d.tables["Working_Capital"]["Giá vốn tháng"].sum()/30)
    return {"base_revenue":base_rev,"revenue":rev,"base_ebitda":base_eb,"ebitda":eb,"margin":eb/rev if rev else 0,"cash_release":cash}
