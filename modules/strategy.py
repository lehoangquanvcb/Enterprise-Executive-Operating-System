
import plotly.express as px
import streamlit as st
from ui import tieu_de_trang, dong_chi_so, bieu_do_toi, hien_thi_bang

def render(data, scenario):
    tieu_de_trang("Chiến lược & Hiệu quả", "Bản đồ chiến lược, thẻ điểm KPI, dự báo và sáng kiến")
    tabs = st.tabs(["Bản đồ chiến lược","Thẻ điểm KPI","Thực hiện & Dự báo","Sáng kiến"])
    with tabs[0]:
        hien_thi_bang(data.tables["Strategy_Map"])
        hien_thi_bang(data.tables["KPI_Tree"])
    with tabs[1]:
        kpi = data.tables["KPI"].copy()
        dong_chi_so([
            ("Tổng số KPI", len(kpi), None),
            ("Xanh", int((kpi["Traffic Light"] == "Xanh").sum()), None),
            ("Vàng", int((kpi["Traffic Light"] == "Vàng").sum()), None),
            ("Đỏ", int((kpi["Traffic Light"] == "Đỏ").sum()), None),
        ])
        fig = px.bar(
            kpi.sort_values("Tỷ lệ hoàn thành"),
            x="Tỷ lệ hoàn thành", y="Chỉ tiêu", orientation="h",
            color="Traffic Light",
            color_discrete_map={"Xanh":"#22C55E","Vàng":"#F59E0B","Đỏ":"#EF4444"},
        )
        st.plotly_chart(bieu_do_toi(fig, "Mức độ hoàn thành KPI"), use_container_width=True)
        hien_thi_bang(kpi)
    with tabs[2]:
        forecast = data.tables["Forecast"].dropna(subset=["Tháng","Doanh thu hợp nhất","EBITDA"])
        left, right = st.columns(2)
        left.plotly_chart(
            bieu_do_toi(px.line(forecast, x="Tháng", y="Doanh thu hợp nhất",
                                color="Loại dữ liệu", markers=True), "Doanh thu: Thực hiện & Dự báo"),
            use_container_width=True
        )
        right.plotly_chart(
            bieu_do_toi(px.line(forecast, x="Tháng", y="EBITDA",
                                color="Loại dữ liệu", markers=True), "EBITDA: Thực hiện & Dự báo"),
            use_container_width=True
        )
        hien_thi_bang(data.tables["Scenario_Drivers"][data.tables["Scenario_Drivers"]["Scenario"] == scenario])
    with tabs[3]:
        projects = data.tables["Du_an"]
        st.plotly_chart(
            bieu_do_toi(px.scatter(projects, x="Tiến độ KH", y="Tiến độ TH",
                                   size="Ngân sách (tỷ)", color="Trạng thái",
                                   hover_name="Tên dự án"), "Tiến độ sáng kiến chiến lược"),
            use_container_width=True,
        )
        hien_thi_bang(projects)
