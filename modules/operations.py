
import plotly.express as px, streamlit as st
from ui import *
def render(d,sc):
    page_header("Operations & Aftersales","Inventory, workshop, parts, vendors and delivery")
    tabs=st.tabs(["Inventory","Aftersales","Parts","Vendor","Network"])
    with tabs[0]:
        x=d.tables["Ton_kho"]
        metric_row([("Inventory units",f"{x['Số xe tồn'].sum():,.0f}",None),("Average days",f"{x['Số ngày tồn kho'].mean():.1f}",None),("Dealers >90 days",int((x["Số ngày tồn kho"]>90).sum()),None)])
        st.plotly_chart(dark_chart(px.bar(x.sort_values("Số ngày tồn kho"),x="Số ngày tồn kho",y="Đại lý",orientation="h",color="Thương hiệu"),"Inventory Days"),use_container_width=True)
        st.dataframe(x,use_container_width=True,hide_index=True)
    with tabs[1]:
        s=d.tables["Dich_vu"];latest=s[s["Tháng"]==s["Tháng"].max()]
        st.plotly_chart(dark_chart(px.scatter(latest,x="Hiệu suất khoang",y="CSI",size="Doanh thu dịch vụ (tỷ)",color="Thương hiệu",hover_name="Đại lý"),"Workshop Productivity"),use_container_width=True)
        st.dataframe(latest,use_container_width=True,hide_index=True)
    with tabs[2]:
        st.dataframe(d.tables["Phu_tung"],use_container_width=True,hide_index=True)
    with tabs[3]:
        v=d.tables["Vendor_Performance"]
        st.plotly_chart(dark_chart(px.scatter(v,x="On-time Delivery",y="Quality Score",size="Spend YTD (tỷ)",color="Compliance",hover_name="Nhà cung cấp"),"Vendor Matrix"),use_container_width=True)
        st.dataframe(v,use_container_width=True,hide_index=True)
    with tabs[4]:
        st.dataframe(d.tables["Don_vi"],use_container_width=True,hide_index=True)
