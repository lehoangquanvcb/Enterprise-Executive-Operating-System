
import plotly.graph_objects as go, plotly.express as px, streamlit as st
from ui import page_header,dark_chart
def render(data,scenario):
    page_header("Commercial Funnel","Lead-to-delivery performance")
    f=data.tables["Customer_Funnel"]
    totals=[f[c].sum() for c in ["Lead","Lead đạt chuẩn","Test drive","Đơn hàng","Giao xe"]]
    fig=go.Figure(go.Funnel(y=["Lead","Qualified","Test drive","Order","Delivery"],x=totals))
    st.plotly_chart(dark_chart(fig,"End-to-End Funnel"),use_container_width=True)
    p=data.tables["Lead_Pipeline"]
    stage=p.groupby("Giai đoạn",as_index=False)["Giá trị dự kiến (tỷ)"].sum()
    st.plotly_chart(dark_chart(px.bar(stage,x="Giai đoạn",y="Giá trị dự kiến (tỷ)"),"Pipeline Value"),use_container_width=True)
    st.dataframe(p.sort_values("Tuổi lead (ngày)",ascending=False).head(100),use_container_width=True,hide_index=True)
