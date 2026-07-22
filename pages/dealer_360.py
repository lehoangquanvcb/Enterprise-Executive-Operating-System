
import plotly.express as px, streamlit as st
from model import dealer_health
from ui import page_header,dark_chart
def render(data,scenario):
    page_header("Dealer 360°","Integrated financial, commercial, operational and risk view")
    h=dealer_health(data)
    dealer=st.selectbox("Select dealer",h["Đại lý"].tolist())
    r=h[h["Đại lý"]==dealer].iloc[0]
    c=st.columns(6)
    c[0].metric("Health Score",f"{r['Health Score']:.1f}")
    c[1].metric("EBITDA",f"{r['EBITDA']:.1f} bn")
    c[2].metric("EBITDA Margin",f"{r['Biên EBITDA']:.1%}")
    c[3].metric("Cash Cycle",f"{r['Cash Conversion Cycle']:.1f} days")
    c[4].metric("Lead→Order",f"{r['Lead→Order']:.1%}")
    c[5].metric("EWS",f"{r['Composite EWS']:.1f}")
    pnl=data.tables["Dealer_PnL"]; x=pnl[pnl["Đại lý"]==dealer]
    st.dataframe(x,use_container_width=True,hide_index=True)
    ai=data.tables["Action_Impact"]
    st.subheader("Recommended and tracked actions")
    st.dataframe(ai.sort_values(["Status","Due Date"]).head(12),use_container_width=True,hide_index=True)
