
import plotly.express as px, plotly.graph_objects as go, streamlit as st
from ui import *
def render(d,sc):
    page_header("Commercial & Revenue Growth","Funnel, pipeline, pricing, orders and delivery")
    tabs=st.tabs(["Sales Overview","Funnel","Lead Pipeline","Pricing","Order & Delivery"])
    f=d.tables["Customer_Funnel"];p=d.tables["Lead_Pipeline"];pr=d.tables["Pricing_Discount"];o=d.tables["Order_Delivery"]
    with tabs[0]:
        monthly=f.groupby("Tháng",as_index=False)[["Lead","Đơn hàng","Giao xe"]].sum()
        st.plotly_chart(dark_chart(px.line(monthly,x="Tháng",y=["Lead","Đơn hàng","Giao xe"],markers=True),"Commercial Trend"),use_container_width=True)
        bybrand=f.groupby("Thương hiệu",as_index=False)[["Lead","Đơn hàng","Giao xe"]].sum()
        st.plotly_chart(dark_chart(px.bar(bybrand,x="Thương hiệu",y=["Đơn hàng","Giao xe"],barmode="group"),"Brand Performance"),use_container_width=True)
    with tabs[1]:
        totals=[f[c].sum() for c in ["Lead","Lead đạt chuẩn","Test drive","Đơn hàng","Giao xe"]]
        fig=go.Figure(go.Funnel(y=["Lead","Qualified","Test drive","Order","Delivery"],x=totals))
        st.plotly_chart(dark_chart(fig,"End-to-End Funnel"),use_container_width=True)
        heat=f.groupby(["Đại lý"],as_index=False)[["Lead→Order","Order→Delivery"]].mean()
        st.dataframe(heat.sort_values("Lead→Order"),use_container_width=True,hide_index=True)
    with tabs[2]:
        stage=p.groupby("Giai đoạn",as_index=False)["Giá trị dự kiến (tỷ)"].sum()
        a,b=st.columns(2)
        a.plotly_chart(dark_chart(px.bar(stage,x="Giai đoạn",y="Giá trị dự kiến (tỷ)"),"Pipeline Value"),use_container_width=True)
        b.plotly_chart(dark_chart(px.histogram(p,x="Tuổi lead (ngày)",color="Giai đoạn"),"Lead Aging"),use_container_width=True)
        st.dataframe(p.sort_values(["Ưu tiên","Tuổi lead (ngày)"],ascending=[True,False]),use_container_width=True,hide_index=True)
    with tabs[3]:
        metric_row([("Avg discount",f"{pr['Chiết khấu thực tế'].mean():.1%}",None),("Breaches",int((pr["Cờ kiểm soát"]=="BREACH").sum()),None),("Leakage",f"{pr['Discount leakage (tỷ)'].sum():,.2f} bn",None)])
        st.plotly_chart(dark_chart(px.box(pr,x="Thương hiệu",y="Chiết khấu thực tế",color="Thương hiệu",points="outliers"),"Discount Dispersion"),use_container_width=True)
        st.dataframe(pr[pr["Cờ kiểm soát"]=="BREACH"].sort_values("Discount leakage (tỷ)",ascending=False),use_container_width=True,hide_index=True)
    with tabs[4]:
        dl=o[o["Đúng hạn"].isin(["Yes","No"])]
        metric_row([("On-time",f"{(dl['Đúng hạn']=='Yes').mean():.1%}",None),("Delayed",int((dl["Đúng hạn"]=="No").sum()),None),("Avg positive delay",f"{dl['Chậm giao (ngày)'].clip(lower=0).mean():.1f} days",None)])
        st.plotly_chart(dark_chart(px.histogram(dl,x="Chậm giao (ngày)",color="Thương hiệu"),"Delivery Delay"),use_container_width=True)
        st.dataframe(o.sort_values("Chậm giao (ngày)",ascending=False),use_container_width=True,hide_index=True)
