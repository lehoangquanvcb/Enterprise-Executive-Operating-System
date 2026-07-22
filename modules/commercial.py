
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from ui import tieu_de_trang, dong_chi_so, bieu_do_toi, hien_thi_bang

def render(data, scenario):
    tieu_de_trang("Thương mại & Tăng trưởng", "Bán hàng, phễu khách hàng, pipeline, giá bán và giao xe")
    funnel = data.tables["Customer_Funnel"]
    pipeline = data.tables["Lead_Pipeline"]
    pricing = data.tables["Pricing_Discount"]
    orders = data.tables["Order_Delivery"]
    sales = data.tables["Ban_hang"]
    tabs = st.tabs(["Tổng quan bán hàng","Phễu khách hàng","Pipeline","Kiểm soát giá","Đơn hàng & Giao xe"])
    with tabs[0]:
        monthly = sales.groupby("Tháng", as_index=False)[["Số xe bán","Doanh thu (tỷ)","Lợi nhuận gộp (tỷ)"]].sum()
        left, right = st.columns(2)
        left.plotly_chart(bieu_do_toi(px.line(monthly, x="Tháng", y="Doanh thu (tỷ)", markers=True),
                                     "Doanh thu theo tháng"), use_container_width=True)
        by_brand = sales.groupby("Thương hiệu", as_index=False)[["Số xe bán","Doanh thu (tỷ)"]].sum()
        right.plotly_chart(bieu_do_toi(px.bar(by_brand, x="Thương hiệu", y="Doanh thu (tỷ)",
                                             color="Thương hiệu"), "Doanh thu theo thương hiệu"),
                           use_container_width=True)
    with tabs[1]:
        totals = [funnel[c].sum() for c in ["Lead","Lead đạt chuẩn","Test drive","Đơn hàng","Giao xe"]]
        fig = go.Figure(go.Funnel(y=["Khách hàng tiềm năng","Đạt chuẩn","Lái thử","Đơn hàng","Giao xe"], x=totals))
        st.plotly_chart(bieu_do_toi(fig, "Phễu thương mại đầu cuối"), use_container_width=True)
        score = funnel.groupby("Đại lý", as_index=False)[["Lead→Order","Order→Delivery"]].mean()
        hien_thi_bang(score.sort_values("Lead→Order"))
    with tabs[2]:
        stage = pipeline.groupby("Giai đoạn", as_index=False)["Giá trị dự kiến (tỷ)"].sum()
        left, right = st.columns(2)
        left.plotly_chart(bieu_do_toi(px.bar(stage, x="Giai đoạn", y="Giá trị dự kiến (tỷ)"),
                                     "Giá trị Pipeline"), use_container_width=True)
        right.plotly_chart(bieu_do_toi(px.histogram(pipeline, x="Tuổi lead (ngày)", color="Giai đoạn"),
                                      "Tuổi khách hàng tiềm năng"), use_container_width=True)
        hien_thi_bang(pipeline.sort_values("Tuổi lead (ngày)", ascending=False))
    with tabs[3]:
        dong_chi_so([
            ("Chiết khấu bình quân", f"{pricing['Chiết khấu thực tế'].mean():.1%}", None),
            ("Vi phạm chính sách giá", int((pricing["Cờ kiểm soát"] == "BREACH").sum()), None),
            ("Rò rỉ chiết khấu", f"{pricing['Discount leakage (tỷ)'].sum():,.2f} tỷ", None),
        ])
        st.plotly_chart(
            bieu_do_toi(px.box(pricing, x="Thương hiệu", y="Chiết khấu thực tế",
                               color="Thương hiệu", points="outliers"), "Phân tán chiết khấu"),
            use_container_width=True,
        )
        hien_thi_bang(pricing[pricing["Cờ kiểm soát"] == "BREACH"]
                      .sort_values("Discount leakage (tỷ)", ascending=False))
    with tabs[4]:
        delivered = orders[orders["Đúng hạn"].isin(["Yes","No"])]
        dong_chi_so([
            ("Giao đúng hạn", f"{(delivered['Đúng hạn'] == 'Yes').mean():.1%}", None),
            ("Đơn giao chậm", int((delivered["Đúng hạn"] == "No").sum()), None),
            ("Chậm bình quân", f"{delivered['Chậm giao (ngày)'].clip(lower=0).mean():.1f} ngày", None),
        ])
        st.plotly_chart(
            bieu_do_toi(px.histogram(delivered, x="Chậm giao (ngày)", color="Thương hiệu"),
                        "Phân bố thời gian giao chậm"),
            use_container_width=True,
        )
        hien_thi_bang(orders.sort_values("Chậm giao (ngày)", ascending=False))
