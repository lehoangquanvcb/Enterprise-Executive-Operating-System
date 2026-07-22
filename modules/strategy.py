
import plotly.express as px, streamlit as st
from ui import *
def render(d,sc):
    page_header("Strategy & Performance","Strategy map, KPI tree, execution and forecast")
    tabs=st.tabs(["Strategy Map","KPI Scorecard","Forecast","Initiatives"])
    with tabs[0]:
        st.dataframe(d.tables["Strategy_Map"],use_container_width=True,hide_index=True)
        st.dataframe(d.tables["KPI_Tree"],use_container_width=True,hide_index=True)
    with tabs[1]:
        k=d.tables["KPI"];metric_row([("KPIs",len(k),None),("Green",int((k["Trạng thái"]=="Xanh").sum()),None),("Amber",int((k["Trạng thái"]=="Vàng").sum()),None),("Red",int((k["Trạng thái"]=="Đỏ").sum()),None)])
        st.plotly_chart(dark_chart(px.bar(k.sort_values("Tỷ lệ hoàn thành"),x="Tỷ lệ hoàn thành",y="Chỉ tiêu",orientation="h",color="Trạng thái"),"KPI Attainment"),use_container_width=True)
        st.dataframe(k,use_container_width=True,hide_index=True)
    with tabs[2]:
        f=d.tables["Forecast"];st.plotly_chart(dark_chart(px.line(f,x="Tháng",y=["Doanh thu KH (tỷ)","Doanh thu dự báo (tỷ)"],color_discrete_sequence=None,markers=True),"Revenue Forecast"),use_container_width=True)
        st.dataframe(d.tables["Scenario_Drivers"][d.tables["Scenario_Drivers"]["Scenario"]==sc],use_container_width=True,hide_index=True)
    with tabs[3]:
        st.dataframe(d.tables["Du_an"],use_container_width=True,hide_index=True)
        st.dataframe(d.tables["Action_Impact"],use_container_width=True,hide_index=True)
