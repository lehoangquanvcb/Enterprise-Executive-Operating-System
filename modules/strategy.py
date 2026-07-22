
import plotly.express as px
import streamlit as st
from ui import page_header, metric_row, dark_chart

def render(data, scenario):
    page_header("Strategy & Performance", "Strategy map, KPI scorecard, forecast and execution")
    tabs = st.tabs(["Strategy Map","KPI Scorecard","Actual & Forecast","Initiatives"])
    with tabs[0]:
        st.dataframe(data.tables["Strategy_Map"], use_container_width=True, hide_index=True)
        st.dataframe(data.tables["KPI_Tree"], use_container_width=True, hide_index=True)
    with tabs[1]:
        kpi = data.tables["KPI"].copy()
        metric_row([
            ("KPIs", len(kpi), None),
            ("Green", int((kpi["Traffic Light"] == "Green").sum()), None),
            ("Amber", int((kpi["Traffic Light"] == "Amber").sum()), None),
            ("Red", int((kpi["Traffic Light"] == "Red").sum()), None),
        ])
        fig = px.bar(
            kpi.sort_values("Tỷ lệ hoàn thành"),
            x="Tỷ lệ hoàn thành", y="Chỉ tiêu", orientation="h",
            color="Traffic Light",
            color_discrete_map={"Green":"#22C55E","Amber":"#F59E0B","Red":"#EF4444"},
        )
        st.plotly_chart(dark_chart(fig, "KPI Attainment"), use_container_width=True)
        st.dataframe(kpi, use_container_width=True, hide_index=True)
    with tabs[2]:
        forecast = data.tables["Forecast"].copy()
        forecast = forecast.dropna(subset=["Tháng","Doanh thu hợp nhất","EBITDA"])
        left, right = st.columns(2)
        revenue_fig = px.line(
            forecast, x="Tháng", y="Doanh thu hợp nhất",
            color="Loại dữ liệu", markers=True
        )
        ebitda_fig = px.line(
            forecast, x="Tháng", y="EBITDA",
            color="Loại dữ liệu", markers=True
        )
        left.plotly_chart(dark_chart(revenue_fig, "Revenue: Actual & Forecast"), use_container_width=True)
        right.plotly_chart(dark_chart(ebitda_fig, "EBITDA: Actual & Forecast"), use_container_width=True)
        st.dataframe(
            data.tables["Scenario_Drivers"][data.tables["Scenario_Drivers"]["Scenario"] == scenario],
            use_container_width=True, hide_index=True
        )
    with tabs[3]:
        projects = data.tables["Du_an"].copy()
        st.plotly_chart(
            dark_chart(
                px.scatter(projects, x="Tiến độ KH", y="Tiến độ TH",
                           size="Ngân sách (tỷ)", color="Trạng thái",
                           hover_name="Tên dự án"),
                "Strategic Initiative Delivery"
            ),
            use_container_width=True,
        )
        st.dataframe(projects, use_container_width=True, hide_index=True)
