
import plotly.express as px, streamlit as st
from model import dynamic_ews
from ui import *
def render(d,sc):
    page_header("Risk, EWS & Resilience","Enterprise risk appetite, early warning and stress view")
    tabs=st.tabs(["Dynamic EWS","Risk Register","Control Matrix","Stress View"])
    with tabs[0]:
        c1,c2,c3,c4=st.columns(4)
        a=c1.slider("Base risk",0,100,40)/100;b=c2.slider("Working capital",0,100,25)/100;c=c3.slider("Commercial",0,100,20)/100;e=c4.slider("Margin",0,100,15)/100
        total=a+b+c+e or 1;x=dynamic_ews(d,{"base":a/total,"wc":b/total,"commercial":c/total,"margin":e/total})
        st.plotly_chart(dark_chart(px.bar(x,x="Dynamic EWS",y="Đại lý",orientation="h",color="Dynamic Level"),"Dynamic Dealer EWS"),use_container_width=True)
        st.dataframe(x,use_container_width=True,hide_index=True)
    with tabs[1]:
        rr=d.tables["Rui_ro"];st.plotly_chart(dark_chart(px.scatter(rr,x="Khả năng",y="Tác động",size="Điểm rủi ro",color="Trạng thái",hover_name="Rủi ro"),"Enterprise Risk Map"),use_container_width=True)
        st.dataframe(rr.sort_values("Điểm rủi ro",ascending=False),use_container_width=True,hide_index=True)
    with tabs[2]:
        st.dataframe(d.tables["RCM"],use_container_width=True,hide_index=True)
    with tabs[3]:
        st.info("Downside lens: higher discount, lower volume, higher inventory days and interest rates.")
        st.dataframe(d.tables["Scenario_Drivers"][d.tables["Scenario_Drivers"]["Scenario"]=="Downside"],use_container_width=True,hide_index=True)
