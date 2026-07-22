
import plotly.express as px, streamlit as st
from model import metrics,dealer_health
from ui import *
def render(d,sc):
    page_header("Executive Command Center",f"{d.company_name} · {d.reporting_period} · {sc}")
    m=metrics(d);metric_row([("Revenue",f"{m['revenue']:,.0f} bn",None),("EBITDA",f"{m['ebitda']:,.1f} bn",f"{m['margin']:.1%}"),
    ("Minimum cash",f"{m['cash_min']:,.1f} bn",None),("Lead→Order",f"{m['conversion']:.1%}",None),("On-time delivery",f"{m['otd']:.1%}",None),
    ("Red EWS",m["red_ews"],None),("Discount leakage",f"{m['discount']:,.2f} bn",None),("Overdue actions",m["overdue"],None)])
    tabs=st.tabs(["Morning Brief","Dealer Portfolio","Cash & Margin","Decisions"])
    with tabs[0]:
        for _,r in d.tables["Executive_Brief"].sort_values("Ưu tiên").iterrows():
            executive_card(r["Chủ đề"],r["Phát hiện"],r["Khuyến nghị điều hành"],r["Owner"],r["SLA"],"critical" if r["Mức độ"]=="High" else "warning")
    with tabs[1]:
        h=dealer_health(d);a,b=st.columns(2)
        a.plotly_chart(dark_chart(px.bar(h.head(12),x="Health Score",y="Đại lý",orientation="h",color="Thương hiệu"),"Dealer Health Ranking"),use_container_width=True)
        b.plotly_chart(dark_chart(px.scatter(h,x="Cash Conversion Cycle",y="Biên EBITDA",size="EBITDA",color="Mức cảnh báo",hover_name="Đại lý"),"Value–Liquidity Matrix"),use_container_width=True)
        st.dataframe(h,use_container_width=True,hide_index=True);download_df(h,"Download Dealer Health","dealer_health.csv")
    with tabs[2]:
        cf=d.tables["Cash_Flow_13W"];p=d.tables["Dealer_PnL"]
        a,b=st.columns(2)
        a.plotly_chart(dark_chart(px.line(cf,x="Bắt đầu",y=["Tiền cuối kỳ","Mức tiền tối thiểu"],markers=True),"13-Week Cash"),use_container_width=True)
        b.plotly_chart(dark_chart(px.scatter(p,x="Doanh thu xe",y="Biên EBITDA",size="EBITDA",color="Thương hiệu",hover_name="Đại lý"),"Dealer Margin Portfolio"),use_container_width=True)
    with tabs[3]:
        st.dataframe(d.tables["Quyet_dinh"],use_container_width=True,hide_index=True)
        st.dataframe(d.tables["Action_Impact"].sort_values(["Status","Due Date"]),use_container_width=True,hide_index=True)
