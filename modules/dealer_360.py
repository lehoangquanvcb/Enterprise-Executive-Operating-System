
import plotly.express as px, streamlit as st
from model import dealer_health
from ui import *
def render(d,sc):
    page_header("Dealer 360°","Single-dealer integrated management cockpit")
    h=dealer_health(d); dealer=st.selectbox("Select dealer",h["Đại lý"].tolist())
    r=h[h["Đại lý"]==dealer].iloc[0]
    metric_row([("Health",f"{r['Health Score']:.1f}/100",None),("EBITDA",f"{r['EBITDA']:.1f} bn",None),("Margin",f"{r['Biên EBITDA']:.1%}",None),
    ("DIO",f"{r['DIO']:.1f} days",None),("Cash cycle",f"{r['Cash Conversion Cycle']:.1f} days",None),("Lead→Order",f"{r['Lead→Order']:.1%}",None),("EWS",f"{r['Composite EWS']:.1f}",None)])
    tabs=st.tabs(["Diagnosis","Financial","Commercial","Inventory","Aftersales","Customer","Governance"])
    with tabs[0]:
        findings=[]
        if r["Biên EBITDA"]<.06:findings.append("EBITDA margin is below 6%.")
        if r["Cash Conversion Cycle"]>70:findings.append("Cash conversion cycle is elevated.")
        if r["Lead→Order"]<.10:findings.append("Lead conversion is below operating target.")
        if r["Composite EWS"]>=60:findings.append("Early-warning status requires management attention.")
        if not findings:findings=["Dealer is operating within core management thresholds."]
        for f in findings:executive_card("Dealer diagnosis",f,"Assign a 30-day recovery or sustainment plan","Dealer GM / COO","7 days","warning")
        st.dataframe(d.tables["Action_Impact"].sort_values(["Status","Due Date"]).head(15),use_container_width=True,hide_index=True)
    with tabs[1]:
        x=d.tables["Dealer_PnL"];st.dataframe(x[x["Đại lý"]==dealer],use_container_width=True,hide_index=True)
    with tabs[2]:
        x=d.tables["Customer_Funnel"];x=x[x["Đại lý"]==dealer]
        st.plotly_chart(dark_chart(px.line(x,x="Tháng",y=["Lead","Đơn hàng","Giao xe"],markers=True),"Dealer Funnel Trend"),use_container_width=True)
        st.dataframe(d.tables["Lead_Pipeline"][d.tables["Lead_Pipeline"]["Đại lý"]==dealer],use_container_width=True,hide_index=True)
    with tabs[3]:
        st.dataframe(d.tables["Working_Capital"][d.tables["Working_Capital"]["Đại lý"]==dealer],use_container_width=True,hide_index=True)
        st.dataframe(d.tables["Ton_kho"][d.tables["Ton_kho"]["Đại lý"]==dealer],use_container_width=True,hide_index=True)
    with tabs[4]:
        st.dataframe(d.tables["Dich_vu"][d.tables["Dich_vu"]["Đại lý"]==dealer],use_container_width=True,hide_index=True)
        st.dataframe(d.tables["Phu_tung"][d.tables["Phu_tung"]["Đại lý"]==dealer],use_container_width=True,hide_index=True)
    with tabs[5]:
        st.dataframe(d.tables["Order_Delivery"][d.tables["Order_Delivery"]["Đại lý"]==dealer],use_container_width=True,hide_index=True)
    with tabs[6]:
        st.dataframe(d.tables["Early_Warning"][d.tables["Early_Warning"]["Đại lý"]==dealer],use_container_width=True,hide_index=True)
