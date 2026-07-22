
import plotly.graph_objects as go
import streamlit as st
from model import scenario_output
from ui import tieu_de_trang, dong_chi_so, bieu_do_toi, hien_thi_bang

def render(data, scenario):
    tieu_de_trang("Phòng thí nghiệm Kịch bản", "Mô phỏng độ nhạy doanh thu, EBITDA và tiền mặt")
    presets = {
        "Base": (0.08, 0.02, 0.00, 0.11, 0.07, 10),
        "Upside": (0.16, 0.035, -0.007, 0.18, 0.06, 20),
        "Downside": (-0.08, -0.01, 0.018, 0.03, 0.10, 0),
    }
    preset = presets[scenario]
    a, b, c = st.columns(3)
    volume = a.slider("Thay đổi sản lượng xe", -30, 30, int(preset[0]*100)) / 100
    price = b.slider("Thay đổi giá / cơ cấu", -10, 10, int(preset[1]*100)) / 100
    discount = c.slider("Chiết khấu bổ sung", -5, 8, int(preset[2]*100)) / 100
    a, b, c = st.columns(3)
    service = a.slider("Tăng trưởng aftersales", -20, 40, int(preset[3]*100)) / 100
    personnel = b.slider("Tăng chi phí nhân sự", -10, 25, int(preset[4]*100)) / 100
    inventory = c.slider("Giảm số ngày tồn kho", 0, 40, preset[5])
    result = scenario_output(data, volume, price, discount, service, personnel, inventory)
    dong_chi_so([
        ("Doanh thu mô phỏng", f"{result['revenue']:,.1f} tỷ",
         f"{result['revenue']/result['base_revenue']-1:.1%}"),
        ("EBITDA mô phỏng", f"{result['ebitda']:,.1f} tỷ",
         f"{result['ebitda']-result['base_ebitda']:,.1f} tỷ"),
        ("Biên EBITDA", f"{result['margin']:.1%}", None),
        ("Tiền mặt giải phóng", f"{result['cash_release']:,.1f} tỷ", None),
    ])
    pnl = data.tables["Dealer_PnL"]
    fig = go.Figure(go.Waterfall(
        x=["EBITDA cơ sở","Sản lượng","Giá / Cơ cấu","Chiết khấu","Aftersales","Nhân sự","EBITDA mô phỏng"],
        y=[
            result["base_ebitda"],
            result["base_revenue"] * volume * 0.075,
            result["base_revenue"] * price * 0.68,
            -result["base_revenue"] * discount * 0.80,
            float(pnl["Doanh thu dịch vụ"].sum()) * service * 0.35,
            -float(pnl["Chi phí nhân sự"].sum()) * personnel,
            result["ebitda"],
        ],
        measure=["absolute","relative","relative","relative","relative","relative","total"],
    ))
    st.plotly_chart(bieu_do_toi(fig, "Cầu nối EBITDA theo kịch bản"), use_container_width=True)
    hien_thi_bang(data.tables["Scenario_Drivers"][data.tables["Scenario_Drivers"]["Scenario"] == scenario])
    st.info("Đây là mô hình độ nhạy quản trị sử dụng dữ liệu giả lập, không phải dự báo pháp định.")
