
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO
import numpy as np
import pandas as pd

REQUIRED_SHEETS = [
    "Cau_hinh","Don_vi","Dealer_KPI","Ban_hang","Ton_kho","Dich_vu","Phu_tung",
    "Tai_chinh","Forecast","Scenario","KPI","Du_an","Rui_ro","RCM","Quyet_dinh",
    "Hanh_dong","Lich_hop","Nghi_quyet","Dau_tu","Chat_luong_DL","Strategy_Map",
    "KPI_Tree","Customer_Funnel","Lead_Pipeline","Order_Delivery","Pricing_Discount",
    "Dealer_PnL","Working_Capital","Cash_Flow_13W","Workforce","Vendor_Performance",
    "Audit_Findings","Policy_Register","ESG","Early_Warning","Executive_Brief",
    "Data_Lineage","Action_Impact","Scenario_Drivers","Board_Pack_Map",
    "Validation_Rules","Module_Map","App_Config"
]

@dataclass
class EEOSData:
    tables: dict[str, pd.DataFrame]
    company_name: str
    reporting_period: str

def load_master(source: str | Path | BinaryIO) -> EEOSData:
    tables = pd.read_excel(source, sheet_name=None, engine="openpyxl")
    missing = [s for s in REQUIRED_SHEETS if s not in tables]
    if missing:
        raise ValueError("Missing required sheets: " + ", ".join(missing))
    config = tables["Cau_hinh"].set_index("Thông số")["Giá trị"].to_dict()
    return EEOSData(
        tables=tables,
        company_name=str(config.get("Doanh nghiệp mô phỏng", "Hà Thành Auto")),
        reporting_period=str(config.get("Kỳ báo cáo", "2026")),
    )

def _date_columns(tables: dict[str, pd.DataFrame]) -> None:
    mapping = {
        "Ban_hang":["Tháng"], "Ton_kho":["Ngày báo cáo"], "Dich_vu":["Tháng"],
        "Tai_chinh":["Tháng"], "Forecast":["Tháng"], "Customer_Funnel":["Tháng"],
        "Lead_Pipeline":["Ngày tạo"],
        "Order_Delivery":["Ngày đặt","Ngày hứa giao","Ngày giao dự kiến/thực tế"],
        "Pricing_Discount":["Ngày"], "Cash_Flow_13W":["Bắt đầu"],
        "Audit_Findings":["Ngày ghi nhận","Hạn khắc phục"], "Action_Impact":["Due Date"],
    }
    for sheet, columns in mapping.items():
        for column in columns:
            if column in tables[sheet].columns:
                tables[sheet][column] = pd.to_datetime(tables[sheet][column], errors="coerce")

def prepare(data: EEOSData) -> EEOSData:
    t = data.tables
    _date_columns(t)
    funnel = t["Customer_Funnel"]
    funnel["Lead→Order"] = np.where(funnel["Lead"] > 0, funnel["Đơn hàng"] / funnel["Lead"], 0)
    funnel["Order→Delivery"] = np.where(funnel["Đơn hàng"] > 0, funnel["Giao xe"] / funnel["Đơn hàng"], 0)
    funnel["Lead→Delivery"] = np.where(funnel["Lead"] > 0, funnel["Giao xe"] / funnel["Lead"], 0)

    pnl = t["Dealer_PnL"]
    pnl["EBITDA"] = (
        pnl["LN gộp xe"] + pnl["LN gộp dịch vụ"] - pnl["Chi phí nhân sự"]
        - pnl["Chi phí mặt bằng"] - pnl["Marketing"] - pnl["Chi phí khác"]
    )
    total_revenue = pnl["Doanh thu xe"] + pnl["Doanh thu dịch vụ"]
    pnl["Biên EBITDA"] = np.where(total_revenue > 0, pnl["EBITDA"] / total_revenue, 0)

    wc = t["Working_Capital"]
    wc["DIO"] = np.where(wc["Giá vốn tháng"] > 0, wc["Tồn kho"] / wc["Giá vốn tháng"] * 30, 0)
    wc["DSO"] = np.where(wc["Doanh thu tháng"] > 0, wc["Phải thu"] / wc["Doanh thu tháng"] * 30, 0)
    wc["DPO"] = np.where(wc["Giá vốn tháng"] > 0, wc["Phải trả"] / wc["Giá vốn tháng"] * 30, 0)
    wc["Cash Conversion Cycle"] = wc["DIO"] + wc["DSO"] - wc["DPO"]

    kpi = t["KPI"]
    kpi["Traffic Light"] = np.select(
        [kpi["Tỷ lệ hoàn thành"] >= 1.0, kpi["Tỷ lệ hoàn thành"] >= 0.9],
        ["Xanh", "Vàng"],
        default="Đỏ",
    )
    return data

def filter_data(data: EEOSData, brands=None, dealers=None) -> EEOSData:
    output = {}
    dealer_codes = None
    if dealers:
        dm = data.tables["Don_vi"]
        dealer_codes = set(dm[dm["Tên đại lý"].isin(dealers)]["Mã đại lý"])
    for name, frame in data.tables.items():
        x = frame.copy()
        if brands and "Thương hiệu" in x.columns:
            x = x[x["Thương hiệu"].isin(brands)]
        if dealers:
            if "Đại lý" in x.columns:
                x = x[x["Đại lý"].isin(dealers)]
            elif "Tên đại lý" in x.columns:
                x = x[x["Tên đại lý"].isin(dealers)]
            elif "Mã đại lý" in x.columns:
                x = x[x["Mã đại lý"].isin(dealer_codes)]
        output[name] = x
    return EEOSData(output, data.company_name, data.reporting_period)

def enterprise_metrics(data: EEOSData) -> dict:
    t = data.tables
    pnl = t["Dealer_PnL"]
    revenue = float((pnl["Doanh thu xe"] + pnl["Doanh thu dịch vụ"]).sum())
    ebitda = float(pnl["EBITDA"].sum())
    delivery = t["Order_Delivery"]
    delivery = delivery[delivery["Đúng hạn"].isin(["Yes", "No"])]
    return {
        "revenue": revenue,
        "ebitda": ebitda,
        "margin": ebitda / revenue if revenue else 0,
        "cash_min": float(t["Cash_Flow_13W"]["Tiền cuối kỳ"].min()),
        "red_ews": int((t["Early_Warning"]["Mức cảnh báo"] == "Red").sum()),
        "discount_leakage": float(t["Pricing_Discount"]["Discount leakage (tỷ)"].sum()),
        "overdue_actions": int((t["Action_Impact"]["Status"] == "Overdue").sum()),
        "pending_decisions": int(t["Quyet_dinh"]["Trạng thái"].isin(["Đang xem xét", "Chờ quyết định"]).sum()),
        "lead_conversion": float(t["Customer_Funnel"]["Lead→Order"].mean()),
        "on_time_delivery": float((delivery["Đúng hạn"] == "Yes").mean()) if len(delivery) else 0,
    }

def dealer_health(data: EEOSData) -> pd.DataFrame:
    t = data.tables
    health = (
        t["Dealer_PnL"][["Mã đại lý","Đại lý","Thương hiệu","EBITDA","Biên EBITDA"]]
        .merge(t["Working_Capital"][["Mã đại lý","DIO","Cash Conversion Cycle"]], on="Mã đại lý")
        .merge(t["Early_Warning"][["Mã đại lý","Composite EWS","Mức cảnh báo"]], on="Mã đại lý")
        .merge(
            t["Customer_Funnel"].groupby("Mã đại lý", as_index=False)[["Lead→Order","Order→Delivery"]].mean(),
            on="Mã đại lý",
        )
    )
    health["Health Score"] = (
        np.clip(health["Biên EBITDA"] / 0.12, 0, 1) * 0.30
        + np.clip(1 - health["Cash Conversion Cycle"] / 120, 0, 1) * 0.20
        + np.clip(health["Lead→Order"] / 0.14, 0, 1) * 0.20
        + np.clip(health["Order→Delivery"] / 0.92, 0, 1) * 0.10
        + np.clip(1 - health["Composite EWS"] / 100, 0, 1) * 0.20
    ) * 100
    return health.sort_values("Health Score", ascending=False)

def dynamic_ews(data: EEOSData, weights: dict) -> pd.DataFrame:
    h = dealer_health(data).copy()
    h["Dynamic EWS"] = (
        h["Composite EWS"] * weights["base"]
        + np.clip(h["Cash Conversion Cycle"] / 120 * 100, 0, 100) * weights["working_capital"]
        + np.clip((0.14 - h["Lead→Order"]) / 0.14 * 100, 0, 100) * weights["commercial"]
        + np.clip((0.10 - h["Biên EBITDA"]) / 0.10 * 100, 0, 100) * weights["margin"]
    )
    h["Dynamic Level"] = np.select(
        [h["Dynamic EWS"] >= 75, h["Dynamic EWS"] >= 60],
        ["Đỏ", "Vàng"],
        default="Xanh",
    )
    return h.sort_values("Dynamic EWS", ascending=False)

def scenario_output(data, volume, price, discount, service_growth, personnel_growth, inventory_reduction):
    pnl = data.tables["Dealer_PnL"]
    vehicle_revenue = float(pnl["Doanh thu xe"].sum())
    service_revenue = float(pnl["Doanh thu dịch vụ"].sum())
    base_revenue = vehicle_revenue + service_revenue
    base_ebitda = float(pnl["EBITDA"].sum())
    revenue = vehicle_revenue * (1 + volume + price) + service_revenue * (1 + service_growth)
    ebitda = (
        base_ebitda
        + vehicle_revenue * (volume * 0.075 + price * 0.68 - discount * 0.80)
        + service_revenue * service_growth * 0.35
        - float(pnl["Chi phí nhân sự"].sum()) * personnel_growth
    )
    cash_release = inventory_reduction * (float(data.tables["Working_Capital"]["Giá vốn tháng"].sum()) / 30)
    return {
        "base_revenue": base_revenue,
        "revenue": revenue,
        "base_ebitda": base_ebitda,
        "ebitda": ebitda,
        "margin": ebitda / revenue if revenue else 0,
        "cash_release": cash_release,
    }

def validate_data(data: EEOSData):
    issues = []
    t = data.tables
    dealer_codes = set(t["Don_vi"]["Mã đại lý"].dropna())
    for sheet in REQUIRED_SHEETS:
        if sheet not in t:
            issues.append(["Critical", sheet, "Required sheet missing"])
    for sheet in ["Dealer_PnL","Working_Capital","Early_Warning","Customer_Funnel"]:
        invalid = set(t[sheet]["Mã đại lý"].dropna()) - dealer_codes
        if invalid:
            issues.append(["Critical", sheet, f"Unknown dealer codes: {len(invalid)}"])
    for sheet, column in [("Lead_Pipeline","Lead ID"),("Order_Delivery","Order ID"),("Pricing_Discount","Giao dịch")]:
        if t[sheet][column].duplicated().any():
            issues.append(["High", sheet, f"Duplicate {column}"])
    for sheet, column in [("Dealer_PnL","Doanh thu xe"),("Working_Capital","Tồn kho"),("Customer_Funnel","Lead")]:
        if (t[sheet][column] < 0).any():
            issues.append(["High", sheet, f"Negative {column}"])
    action = t["Action_Impact"]
    if action["Owner"].isna().any() or action["Due Date"].isna().any():
        issues.append(["High", "Action_Impact", "Owner or due date missing"])
    score = max(0, 100 - len(issues) * 8)
    return score, pd.DataFrame(issues, columns=["Severity","Object","Issue"])
