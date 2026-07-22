
import plotly.express as px, streamlit as st
from ui import page_header,dark_chart
def render(data,scenario):
    page_header("Strategy & KPI","Strategy map, value drivers and execution status")
    st.dataframe(data.tables["Strategy_Map"],use_container_width=True,hide_index=True)
    st.dataframe(data.tables["KPI_Tree"],use_container_width=True,hide_index=True)
    k=data.tables["KPI"]
    st.plotly_chart(dark_chart(px.bar(k,x="Tỷ lệ hoàn thành",y="Chỉ tiêu",orientation="h",color="Trạng thái"),"Strategic KPI Attainment"),use_container_width=True)
