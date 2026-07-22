
import plotly.express as px
import streamlit as st
from model import dealer_health
from ui import page_header, metric_row, executive_card, dark_chart

def render(data, scenario):
    page_header("Dealer 360°", "Integrated dealer diagnosis and drill-down")
    health = dealer_health(data)
    dealer = st.selectbox("Select dealer", health["Đại lý"].tolist())
    row = health[health["Đại lý"] == dealer].iloc[0]
    metric_row([
        ("Health score", f"{row['Health Score']:.1f}/100", None),
        ("EBITDA", f"{row['EBITDA']:.1f} bn", None),
        ("EBITDA margin", f"{row['Biên EBITDA']:.1%}", None),
        ("DIO", f"{row['DIO']:.1f} days", None),
        ("Cash cycle", f"{row['Cash Conversion Cycle']:.1f} days", None),
        ("Lead→Order", f"{row['Lead→Order']:.1%}", None),
        ("EWS", f"{row['Composite EWS']:.1f}", None),
    ])
    tabs = st.tabs(["Diagnosis","Financial","Commercial","Inventory","Aftersales","Customer & Risk"])
    with tabs[0]:
        observations = []
        if row["Biên EBITDA"] < 0.06:
            observations.append(("Margin", "EBITDA margin is below 6%.", "Launch price, mix and cost recovery."))
        if row["Cash Conversion Cycle"] > 70:
            observations.append(("Liquidity", "Cash conversion cycle exceeds 70 days.", "Reduce inventory and accelerate collections."))
        if row["Lead→Order"] < 0.10:
            observations.append(("Sales", "Lead conversion is below 10%.", "Run a 30-day conversion sprint."))
        if row["Composite EWS"] >= 60:
            observations.append(("Risk", "Early-warning score requires management attention.", "Assign weekly remediation tracking."))
        if not observations:
            observations.append(("Status", "Dealer operates within core management thresholds.", "Maintain controls and monthly review."))
        for topic, finding, action in observations:
            executive_card(topic, finding, action, "Dealer GM / COO", "7 days", "warning")
    with tabs[1]:
        st.dataframe(data.tables["Dealer_PnL"][data.tables["Dealer_PnL"]["Đại lý"] == dealer],
                     use_container_width=True, hide_index=True)
    with tabs[2]:
        f = data.tables["Customer_Funnel"]
        f = f[f["Đại lý"] == dealer]
        st.plotly_chart(dark_chart(px.line(f, x="Tháng", y=["Lead","Đơn hàng","Giao xe"],
                                          markers=True), "Dealer Funnel Trend"),
                        use_container_width=True)
        st.dataframe(data.tables["Lead_Pipeline"][data.tables["Lead_Pipeline"]["Đại lý"] == dealer],
                     use_container_width=True, hide_index=True)
    with tabs[3]:
        st.dataframe(data.tables["Ton_kho"][data.tables["Ton_kho"]["Đại lý"] == dealer],
                     use_container_width=True, hide_index=True)
        st.dataframe(data.tables["Working_Capital"][data.tables["Working_Capital"]["Đại lý"] == dealer],
                     use_container_width=True, hide_index=True)
    with tabs[4]:
        st.dataframe(data.tables["Dich_vu"][data.tables["Dich_vu"]["Đại lý"] == dealer],
                     use_container_width=True, hide_index=True)
        st.dataframe(data.tables["Phu_tung"][data.tables["Phu_tung"]["Đại lý"] == dealer],
                     use_container_width=True, hide_index=True)
    with tabs[5]:
        st.dataframe(data.tables["Order_Delivery"][data.tables["Order_Delivery"]["Đại lý"] == dealer],
                     use_container_width=True, hide_index=True)
        st.dataframe(data.tables["Early_Warning"][data.tables["Early_Warning"]["Đại lý"] == dealer],
                     use_container_width=True, hide_index=True)
