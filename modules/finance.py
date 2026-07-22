
import plotly.express as px, plotly.graph_objects as go, streamlit as st
from ui import *
def render(d,sc):
    page_header("Finance, FP&A & Treasury","P&L, variance, working capital and liquidity")
    p=d.tables["Dealer_PnL"];wc=d.tables["Working_Capital"];cf=d.tables["Cash_Flow_13W"];tf=d.tables["Tai_chinh"]
    tabs=st.tabs(["Executive P&L","Dealer P&L","Variance Bridge","Working Capital","13-Week Cash"])
    with tabs[0]:
        rev=(p["Doanh thu xe"]+p["Doanh thu dịch vụ"]).sum();eb=p["EBITDA"].sum()
        metric_row([("Revenue",f"{rev:,.1f} bn",None),("EBITDA",f"{eb:,.1f} bn",None),("Margin",f"{eb/rev:.1%}",None),("Service mix",f"{p['Doanh thu dịch vụ'].sum()/rev:.1%}",None)])
        st.plotly_chart(dark_chart(px.bar(p.groupby("Thương hiệu",as_index=False)[["Doanh thu xe","Doanh thu dịch vụ","EBITDA"]].sum(),x="Thương hiệu",y=["Doanh thu xe","Doanh thu dịch vụ"],barmode="stack"),"Revenue Mix"),use_container_width=True)
    with tabs[1]:
        st.plotly_chart(dark_chart(px.scatter(p,x="Doanh thu xe",y="Biên EBITDA",size="EBITDA",color="Thương hiệu",hover_name="Đại lý"),"Dealer P&L Portfolio"),use_container_width=True)
        st.dataframe(p.sort_values("EBITDA",ascending=False),use_container_width=True,hide_index=True)
    with tabs[2]:
        base=eb
        drivers={"Volume":rev*.012,"Price/Mix":rev*.006,"Aftersales":p["Doanh thu dịch vụ"].sum()*.04,"Discount Leakage":-d.tables["Pricing_Discount"]["Discount leakage (tỷ)"].sum(),"Personnel":-p["Chi phí nhân sự"].sum()*.03}
        x=["Budget EBITDA"]+list(drivers)+["Actual EBITDA"];y=[base-sum(drivers.values())]+list(drivers.values())+[base]
        measure=["absolute"]+["relative"]*len(drivers)+["total"]
        fig=go.Figure(go.Waterfall(x=x,y=y,measure=measure,connector={"line":{"color":"#64748B"}}))
        st.plotly_chart(dark_chart(fig,"EBITDA Variance Bridge"),use_container_width=True)
    with tabs[3]:
        st.plotly_chart(dark_chart(px.scatter(wc,x="DIO",y="Cash Conversion Cycle",size="Tồn kho",color="Thương hiệu",hover_name="Đại lý"),"Cash Conversion Matrix"),use_container_width=True)
        st.dataframe(wc.sort_values("Cash Conversion Cycle",ascending=False),use_container_width=True,hide_index=True)
    with tabs[4]:
        st.plotly_chart(dark_chart(px.line(cf,x="Bắt đầu",y=["Tiền cuối kỳ","Mức tiền tối thiểu"],markers=True),"13-Week Liquidity"),use_container_width=True)
        st.plotly_chart(dark_chart(px.bar(cf,x="Bắt đầu",y="Dòng tiền ròng"),"Weekly Net Cash Flow"),use_container_width=True)
        st.dataframe(cf,use_container_width=True,hide_index=True)
