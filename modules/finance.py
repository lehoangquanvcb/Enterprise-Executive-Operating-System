
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from ui import tieu_de_trang, dong_chi_so, bieu_do_toi, hien_thi_bang

def render(data, scenario):
    tieu_de_trang("Tài chính & Nguồn vốn", "P&L, phân tích chênh lệch, vốn lưu động và thanh khoản")
    pnl = data.tables["Dealer_PnL"]
    wc = data.tables["Working_Capital"]
    cash = data.tables["Cash_Flow_13W"]
    financial = data.tables["Tai_chinh"]
    tabs = st.tabs(["P&L Điều hành","P&L Đại lý","Cầu nối chênh lệch","Vốn lưu động","Dòng tiền 13 tuần"])
    with tabs[0]:
        revenue = float((pnl["Doanh thu xe"] + pnl["Doanh thu dịch vụ"]).sum())
        ebitda = float(pnl["EBITDA"].sum())
        dong_chi_so([
            ("Doanh thu", f"{revenue:,.1f} tỷ", None),
            ("EBITDA", f"{ebitda:,.1f} tỷ", None),
            ("Biên EBITDA", f"{ebitda/revenue:.1%}", None),
            ("Tỷ trọng dịch vụ", f"{pnl['Doanh thu dịch vụ'].sum()/revenue:.1%}", None),
        ])
        trend = financial[["Tháng","Doanh thu KH","Doanh thu xe TH","Doanh thu dịch vụ TH","EBITDA KH","EBITDA TH"]]
        left, right = st.columns(2)
        left.plotly_chart(
            bieu_do_toi(px.line(trend, x="Tháng", y=["Doanh thu KH","Doanh thu xe TH","Doanh thu dịch vụ TH"],
                                markers=True), "Doanh thu Kế hoạch & Thực hiện"),
            use_container_width=True
        )
        right.plotly_chart(
            bieu_do_toi(px.line(trend, x="Tháng", y=["EBITDA KH","EBITDA TH"], markers=True),
                        "EBITDA Kế hoạch & Thực hiện"),
            use_container_width=True
        )
    with tabs[1]:
        st.plotly_chart(
            bieu_do_toi(px.scatter(pnl, x="Doanh thu xe", y="Biên EBITDA",
                                   size="EBITDA", color="Thương hiệu", hover_name="Đại lý"),
                        "Danh mục P&L Đại lý"),
            use_container_width=True,
        )
        hien_thi_bang(pnl.sort_values("EBITDA", ascending=False))
    with tabs[2]:
        base = float(pnl["EBITDA"].sum())
        drivers = {
            "Sản lượng": float((pnl["Doanh thu xe"] + pnl["Doanh thu dịch vụ"]).sum()) * 0.012,
            "Giá / Cơ cấu": float(pnl["Doanh thu xe"].sum()) * 0.006,
            "Aftersales": float(pnl["Doanh thu dịch vụ"].sum()) * 0.04,
            "Rò rỉ chiết khấu": -float(data.tables["Pricing_Discount"]["Discount leakage (tỷ)"].sum()),
            "Nhân sự": -float(pnl["Chi phí nhân sự"].sum()) * 0.03,
        }
        budget = base - sum(drivers.values())
        fig = go.Figure(go.Waterfall(
            x=["EBITDA Kế hoạch"] + list(drivers.keys()) + ["EBITDA Thực hiện"],
            y=[budget] + list(drivers.values()) + [base],
            measure=["absolute"] + ["relative"] * len(drivers) + ["total"],
        ))
        st.plotly_chart(bieu_do_toi(fig, "Cầu nối chênh lệch EBITDA"), use_container_width=True)
    with tabs[3]:
        st.plotly_chart(
            bieu_do_toi(px.scatter(wc, x="DIO", y="Cash Conversion Cycle",
                                   size="Tồn kho", color="Thương hiệu", hover_name="Đại lý"),
                        "Hiệu quả vốn lưu động"),
            use_container_width=True,
        )
        hien_thi_bang(wc.sort_values("Cash Conversion Cycle", ascending=False))
    with tabs[4]:
        st.plotly_chart(
            bieu_do_toi(px.line(cash, x="Bắt đầu", y=["Tiền cuối kỳ","Mức tiền tối thiểu"],
                                markers=True), "Thanh khoản 13 tuần"),
            use_container_width=True,
        )
        st.plotly_chart(bieu_do_toi(px.bar(cash, x="Bắt đầu", y="Dòng tiền ròng"),
                                    "Dòng tiền ròng theo tuần"), use_container_width=True)
        hien_thi_bang(cash)
