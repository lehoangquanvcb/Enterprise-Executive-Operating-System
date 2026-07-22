
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from ui import page_header, metric_row, dark_chart

def render(data, scenario):
    page_header("Commercial & Growth", "Sales, funnel, pipeline, pricing and delivery")
    funnel = data.tables["Customer_Funnel"]
    pipeline = data.tables["Lead_Pipeline"]
    pricing = data.tables["Pricing_Discount"]
    orders = data.tables["Order_Delivery"]
    sales = data.tables["Ban_hang"]
    tabs = st.tabs(["Sales Overview","Funnel","Pipeline","Pricing Control","Delivery"])
    with tabs[0]:
        monthly = sales.groupby("Tháng", as_index=False)[["Số xe bán","Doanh thu (tỷ)","Lợi nhuận gộp (tỷ)"]].sum()
        left, right = st.columns(2)
        left.plotly_chart(dark_chart(px.line(monthly, x="Tháng", y="Doanh thu (tỷ)", markers=True),
                                    "Monthly Revenue"), use_container_width=True)
        by_brand = sales.groupby("Thương hiệu", as_index=False)[["Số xe bán","Doanh thu (tỷ)"]].sum()
        right.plotly_chart(dark_chart(px.bar(by_brand, x="Thương hiệu", y="Doanh thu (tỷ)",
                                            color="Thương hiệu"), "Revenue by Brand"), use_container_width=True)
    with tabs[1]:
        totals = [funnel[c].sum() for c in ["Lead","Lead đạt chuẩn","Test drive","Đơn hàng","Giao xe"]]
        fig = go.Figure(go.Funnel(y=["Lead","Qualified","Test drive","Order","Delivery"], x=totals))
        st.plotly_chart(dark_chart(fig, "End-to-End Funnel"), use_container_width=True)
        score = funnel.groupby("Đại lý", as_index=False)[["Lead→Order","Order→Delivery"]].mean()
        st.dataframe(score.sort_values("Lead→Order"), use_container_width=True, hide_index=True)
    with tabs[2]:
        stage = pipeline.groupby("Giai đoạn", as_index=False)["Giá trị dự kiến (tỷ)"].sum()
        left, right = st.columns(2)
        left.plotly_chart(dark_chart(px.bar(stage, x="Giai đoạn", y="Giá trị dự kiến (tỷ)"),
                                    "Pipeline Value"), use_container_width=True)
        right.plotly_chart(dark_chart(px.histogram(pipeline, x="Tuổi lead (ngày)", color="Giai đoạn"),
                                     "Lead Aging"), use_container_width=True)
        st.dataframe(pipeline.sort_values("Tuổi lead (ngày)", ascending=False),
                     use_container_width=True, hide_index=True)
    with tabs[3]:
        metric_row([
            ("Average discount", f"{pricing['Chiết khấu thực tế'].mean():.1%}", None),
            ("Pricing breaches", int((pricing["Cờ kiểm soát"] == "BREACH").sum()), None),
            ("Discount leakage", f"{pricing['Discount leakage (tỷ)'].sum():,.2f} bn", None),
        ])
        st.plotly_chart(
            dark_chart(px.box(pricing, x="Thương hiệu", y="Chiết khấu thực tế",
                              color="Thương hiệu", points="outliers"), "Discount Dispersion"),
            use_container_width=True,
        )
        st.dataframe(
            pricing[pricing["Cờ kiểm soát"] == "BREACH"].sort_values(
                "Discount leakage (tỷ)", ascending=False
            ),
            use_container_width=True, hide_index=True
        )
    with tabs[4]:
        delivered = orders[orders["Đúng hạn"].isin(["Yes","No"])]
        metric_row([
            ("On-time delivery", f"{(delivered['Đúng hạn'] == 'Yes').mean():.1%}", None),
            ("Delayed", int((delivered["Đúng hạn"] == "No").sum()), None),
            ("Average delay", f"{delivered['Chậm giao (ngày)'].clip(lower=0).mean():.1f} days", None),
        ])
        st.plotly_chart(
            dark_chart(px.histogram(delivered, x="Chậm giao (ngày)", color="Thương hiệu"),
                       "Delivery Delay"),
            use_container_width=True,
        )
        st.dataframe(orders.sort_values("Chậm giao (ngày)", ascending=False),
                     use_container_width=True, hide_index=True)
