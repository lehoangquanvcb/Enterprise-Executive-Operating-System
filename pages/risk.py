
import plotly.express as px, streamlit as st
from model import dynamic_ews
from ui import page_header,dark_chart
def render(data,scenario):
    page_header("Risk & Dynamic Early Warning","Adjustable risk-weight engine")
    st.sidebar.subheader("EWS Weights")
    w1=st.sidebar.slider("Base risk",0.0,1.0,.40,.05)
    w2=st.sidebar.slider("Working capital",0.0,1.0,.25,.05)
    w3=st.sidebar.slider("Commercial",0.0,1.0,.20,.05)
    w4=st.sidebar.slider("Margin",0.0,1.0,.15,.05)
    total=w1+w2+w3+w4
    weights={"base_risk":w1/total,"working_capital":w2/total,"commercial":w3/total,"margin":w4/total}
    e=dynamic_ews(data,weights)
    st.plotly_chart(dark_chart(px.bar(e,x="Dynamic EWS",y="Đại lý",orientation="h",color="Dynamic Level"),"Dynamic Dealer EWS"),use_container_width=True)
    st.dataframe(e,use_container_width=True,hide_index=True)
