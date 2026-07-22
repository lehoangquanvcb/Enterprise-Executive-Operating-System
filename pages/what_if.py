
import streamlit as st
from ui import page_header
def render(data,scenario):
    page_header("What-if Simulator","Interactive executive decision support")
    pnl=data.tables["Dealer_PnL"]
    base_rev=float((pnl["Doanh thu xe"]+pnl["Doanh thu dịch vụ"]).sum())
    base_ebitda=float(pnl["EBITDA"].sum())
    c1,c2,c3,c4=st.columns(4)
    volume=c1.slider("Vehicle volume change",-30,30,8)/100
    price=c2.slider("Average price change",-10,10,2)/100
    discount=c3.slider("Discount change",-5,5,0)/100
    service=c4.slider("Aftersales growth",-20,40,10)/100
    inv=st.slider("Inventory days reduction",0,40,10)
    revenue=base_rev*(1+volume+price)+pnl["Doanh thu dịch vụ"].sum()*service
    ebitda=base_ebitda+base_rev*(volume*.07+price*.65-discount*.75)+pnl["Doanh thu dịch vụ"].sum()*service*.35
    cash_release=inv*(data.tables["Working_Capital"]["Giá vốn tháng"].sum()/30)
    c=st.columns(4)
    c[0].metric("Simulated Revenue",f"{revenue:,.1f} bn",f"{revenue/base_rev-1:.1%}")
    c[1].metric("Simulated EBITDA",f"{ebitda:,.1f} bn",f"{ebitda-base_ebitda:,.1f} bn")
    c[2].metric("EBITDA Margin",f"{ebitda/revenue:.1%}")
    c[3].metric("Cash Released",f"{cash_release:,.1f} bn")
    st.info("This simulator is an executive sensitivity model using synthetic assumptions, not a statutory forecast.")
