
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from ui import page_header, metric_row, dark_chart

def render(data, scenario):
    page_header("Finance & Treasury", "P&L, variance, working capital and liquidity")
    pnl = data.tables["Dealer_PnL"]
    wc = data.tables["Working_Capital"]
    cash = data.tables["Cash_Flow_13W"]
    financial = data.tables["Tai_chinh"]
    tabs = st.tabs(["Executive P&L","Dealer P&L","Variance Bridge","Working Capital","13-Week Cash"])
    with tabs[0]:
        revenue = float((pnl["Doanh thu xe"] + pnl["Doanh thu dịch vụ"]).sum())
        ebitda = float(pnl["EBITDA"].sum())
        metric_row([
            ("Revenue", f"{revenue:,.1f} bn", None),
            ("EBITDA", f"{ebitda:,.1f} bn", None),
            ("EBITDA margin", f"{ebitda/revenue:.1%}", None),
            ("Service mix", f"{pnl['Doanh thu dịch vụ'].sum()/revenue:.1%}", None),
        ])
        trend = financial[["Tháng","Doanh thu KH","Doanh thu xe TH","Doanh thu dịch vụ TH","EBITDA KH","EBITDA TH"]].copy()
        left, right = st.columns(2)
        left.plotly_chart(
            dark_chart(px.line(trend, x="Tháng", y=["Doanh thu KH","Doanh thu xe TH","Doanh thu dịch vụ TH"],
                               markers=True), "Revenue Plan vs Actual"),
            use_container_width=True
        )
        right.plotly_chart(
            dark_chart(px.line(trend, x="Tháng", y=["EBITDA KH","EBITDA TH"], markers=True),
                       "EBITDA Plan vs Actual"),
            use_container_width=True
        )
    with tabs[1]:
        st.plotly_chart(
            dark_chart(px.scatter(pnl, x="Doanh thu xe", y="Biên EBITDA",
                                  size="EBITDA", color="Thương hiệu", hover_name="Đại lý"),
                       "Dealer P&L Portfolio"),
            use_container_width=True,
        )
        st.dataframe(pnl.sort_values("EBITDA", ascending=False), use_container_width=True, hide_index=True)
    with tabs[2]:
        base = float(pnl["EBITDA"].sum())
        drivers = {
            "Volume": float((pnl["Doanh thu xe"] + pnl["Doanh thu dịch vụ"]).sum()) * 0.012,
            "Price / Mix": float(pnl["Doanh thu xe"].sum()) * 0.006,
            "Aftersales": float(pnl["Doanh thu dịch vụ"].sum()) * 0.04,
            "Discount Leakage": -float(data.tables["Pricing_Discount"]["Discount leakage (tỷ)"].sum()),
            "Personnel": -float(pnl["Chi phí nhân sự"].sum()) * 0.03,
        }
        budget = base - sum(drivers.values())
        fig = go.Figure(go.Waterfall(
            x=["Budget EBITDA"] + list(drivers.keys()) + ["Actual EBITDA"],
            y=[budget] + list(drivers.values()) + [base],
            measure=["absolute"] + ["relative"] * len(drivers) + ["total"],
            connector={"line":{"color":"#64748B"}},
        ))
        st.plotly_chart(dark_chart(fig, "EBITDA Variance Bridge"), use_container_width=True)
    with tabs[3]:
        st.plotly_chart(
            dark_chart(px.scatter(wc, x="DIO", y="Cash Conversion Cycle",
                                  size="Tồn kho", color="Thương hiệu", hover_name="Đại lý"),
                       "Working-Capital Efficiency"),
            use_container_width=True,
        )
        st.dataframe(wc.sort_values("Cash Conversion Cycle", ascending=False),
                     use_container_width=True, hide_index=True)
    with tabs[4]:
        st.plotly_chart(
            dark_chart(px.line(cash, x="Bắt đầu", y=["Tiền cuối kỳ","Mức tiền tối thiểu"],
                               markers=True), "13-Week Liquidity"),
            use_container_width=True,
        )
        st.plotly_chart(dark_chart(px.bar(cash, x="Bắt đầu", y="Dòng tiền ròng"),
                                   "Weekly Net Cash Flow"), use_container_width=True)
        st.dataframe(cash, use_container_width=True, hide_index=True)
