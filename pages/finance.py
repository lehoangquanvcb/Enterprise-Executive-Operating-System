
import plotly.express as px, streamlit as st
from ui import page_header,dark_chart
def render(data,scenario):
    page_header("Finance & Working Capital",f"Scenario: {scenario}")
    pnl=data.tables["Dealer_PnL"]; wc=data.tables["Working_Capital"]; cf=data.tables["Cash_Flow_13W"]
    st.plotly_chart(dark_chart(px.scatter(pnl,x="Doanh thu xe",y="Biên EBITDA",size="EBITDA",color="Thương hiệu",hover_name="Đại lý"),"Dealer P&L Portfolio"),use_container_width=True)
    st.plotly_chart(dark_chart(px.scatter(wc,x="DIO",y="Cash Conversion Cycle",size="Tồn kho",color="Thương hiệu",hover_name="Đại lý"),"Working Capital Efficiency"),use_container_width=True)
    st.plotly_chart(dark_chart(px.line(cf,x="Bắt đầu",y=["Tiền cuối kỳ","Mức tiền tối thiểu"],markers=True),"13-Week Cash Forecast"),use_container_width=True)
