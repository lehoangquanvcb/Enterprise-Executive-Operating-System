
import plotly.express as px, streamlit as st
from ui import *
def render(d,sc):
    page_header("People, Capability & ESG","Workforce productivity, succession and sustainability")
    w=d.tables["Workforce"];e=d.tables["ESG"]
    tabs=st.tabs(["Workforce","Capability","ESG"])
    with tabs[0]:
        metric_row([("Headcount",int(w["Headcount"].sum()),None),("Technicians",int(w["Kỹ thuật viên"].sum()),None),("Avg turnover",f"{w['Turnover'].mean():.1%}",None),("Engagement",f"{w['Engagement'].mean():.1f}",None)])
        st.plotly_chart(dark_chart(px.scatter(w,x="Headcount",y="Engagement",size="Kỹ thuật viên",color="Thương hiệu",hover_name="Đại lý"),"People Capacity"),use_container_width=True)
        st.dataframe(w,use_container_width=True,hide_index=True)
    with tabs[1]:
        st.plotly_chart(dark_chart(px.scatter(w,x="Đào tạo hoàn thành",y="Succession Coverage",size="Headcount",color="Thương hiệu",hover_name="Đại lý"),"Capability & Succession"),use_container_width=True)
    with tabs[2]:
        st.plotly_chart(dark_chart(px.scatter(e,x="Tỷ lệ điện mặt trời",y="Tái chế chất thải",size="Điện năng (MWh)",color="Thương hiệu",hover_name="Đại lý"),"Dealer ESG"),use_container_width=True)
        st.dataframe(e,use_container_width=True,hide_index=True)
