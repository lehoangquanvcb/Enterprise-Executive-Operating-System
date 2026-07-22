
import plotly.graph_objects as go, streamlit as st
from model import scenario_output
from ui import *
def render(d,sc):
    page_header("What-if & Scenario Simulator","Interactive revenue, EBITDA, working-capital and cash sensitivity")
    presets={"Base":(.08,.02,.00,.11,.07,10),"Upside":(.16,.035,-.007,.18,.06,20),"Downside":(-.08,-.01,.018,.03,.10,0)}
    pv=presets[sc]
    a,b,c=st.columns(3);volume=a.slider("Vehicle volume change",-30,30,int(pv[0]*100))/100;price=b.slider("Price / mix change",-10,10,int(pv[1]*100))/100;disc=c.slider("Additional discount",-5,8,int(pv[2]*100))/100
    a,b,c=st.columns(3);service=a.slider("Aftersales growth",-20,40,int(pv[3]*100))/100;personnel=b.slider("Personnel cost growth",-10,25,int(pv[4]*100))/100;inv=c.slider("Inventory days reduction",0,40,pv[5])
    x=scenario_output(d,volume,price,disc,service,personnel,inv)
    metric_row([("Simulated Revenue",f"{x['revenue']:,.1f} bn",f"{x['revenue']/x['base_revenue']-1:.1%}"),("Simulated EBITDA",f"{x['ebitda']:,.1f} bn",f"{x['ebitda']-x['base_ebitda']:,.1f} bn"),
    ("EBITDA Margin",f"{x['margin']:.1%}",None),("Cash Released",f"{x['cash_release']:,.1f} bn",None)])
    fig=go.Figure(go.Waterfall(x=["Base EBITDA","Volume","Price/Mix","Discount","Aftersales","Personnel","Simulated EBITDA"],
      measure=["absolute","relative","relative","relative","relative","relative","total"],
      y=[x["base_ebitda"],x["base_revenue"]*volume*.075,x["base_revenue"]*price*.68,-x["base_revenue"]*disc*.8,
      d.tables["Dealer_PnL"]["Doanh thu dịch vụ"].sum()*service*.35,-d.tables["Dealer_PnL"]["Chi phí nhân sự"].sum()*personnel,x["ebitda"]]))
    st.plotly_chart(dark_chart(fig,"Scenario EBITDA Bridge"),use_container_width=True)
    st.warning("Synthetic management sensitivity model; not a statutory forecast.")
