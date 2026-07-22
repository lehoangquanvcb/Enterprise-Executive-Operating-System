
import plotly.express as px, streamlit as st
from ui import page_header,dark_chart
def render(data,scenario):
    page_header("People, Capability & ESG","Organizational resilience and sustainability")
    w=data.tables["Workforce"]; e=data.tables["ESG"]
    st.plotly_chart(dark_chart(px.scatter(w,x="Headcount",y="Engagement",size="Kỹ thuật viên",color="Thương hiệu",hover_name="Đại lý"),"People Capacity"),use_container_width=True)
    st.plotly_chart(dark_chart(px.scatter(e,x="Tỷ lệ điện mặt trời",y="Tái chế chất thải",size="Điện năng (MWh)",color="Thương hiệu",hover_name="Đại lý"),"Dealer ESG"),use_container_width=True)
