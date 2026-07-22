
import plotly.express as px, streamlit as st
from model import metrics,dealer_health
from ui import page_header,dark_chart,executive_card
def render(data,scenario):
    page_header("Executive Command Center",f"Scenario: {scenario}")
    m=metrics(data); c=st.columns(6)
    c[0].metric("Revenue",f"{m['revenue']:,.0f} bn"); c[1].metric("EBITDA",f"{m['ebitda']:,.1f} bn",f"{m['margin']:.1%}")
    c[2].metric("Minimum Cash",f"{m['cash_min']:,.1f} bn"); c[3].metric("Red EWS",m["red_ews"])
    c[4].metric("Discount Leakage",f"{m['discount_leakage']:,.2f} bn"); c[5].metric("Overdue Actions",m["overdue_actions"])
    for _,r in data.tables["Executive_Brief"].sort_values("Ưu tiên").iterrows():
        sev="critical" if r["Mức độ"]=="High" else "warning"
        executive_card(r["Chủ đề"],r["Phát hiện"],r["Khuyến nghị điều hành"],r["Owner"],r["SLA"],sev)
    h=dealer_health(data)
    l,r=st.columns(2)
    l.plotly_chart(dark_chart(px.bar(h.head(10),x="Health Score",y="Đại lý",orientation="h",color="Thương hiệu"),"Top Dealer Health"),use_container_width=True)
    e=data.tables["Early_Warning"]
    r.plotly_chart(dark_chart(px.scatter(e,x="Inventory Risk",y="Financial Risk",size="Composite EWS",color="Mức cảnh báo",hover_name="Đại lý"),"Enterprise Risk Matrix"),use_container_width=True)
