
import plotly.express as px
import streamlit as st
from ui import page_header, metric_row, dark_chart

def render(data, scenario):
    page_header("Operations & Aftersales", "Inventory, workshop, parts, vendors and network")
    inventory = data.tables["Ton_kho"]
    service = data.tables["Dich_vu"]
    vendor = data.tables["Vendor_Performance"]
    tabs = st.tabs(["Inventory","Aftersales","Parts","Vendors","Network"])
    with tabs[0]:
        metric_row([
            ("Inventory units", f"{inventory['Số xe tồn'].sum():,.0f}", None),
            ("Average inventory days", f"{inventory['Số ngày tồn kho'].mean():.1f}", None),
            ("Records >90 days", int((inventory["Số ngày tồn kho"] > 90).sum()), None),
        ])
        st.plotly_chart(
            dark_chart(px.bar(inventory.sort_values("Số ngày tồn kho"),
                              x="Số ngày tồn kho", y="Đại lý", orientation="h",
                              color="Thương hiệu"), "Inventory Days"),
            use_container_width=True
        )
        st.dataframe(inventory, use_container_width=True, hide_index=True)
    with tabs[1]:
        latest = service[service["Tháng"] == service["Tháng"].max()]
        st.plotly_chart(
            dark_chart(px.scatter(latest, x="Hiệu suất khoang", y="CSI",
                                  size="Doanh thu dịch vụ (tỷ)", color="Thương hiệu",
                                  hover_name="Đại lý"), "Workshop Productivity"),
            use_container_width=True
        )
        st.dataframe(latest, use_container_width=True, hide_index=True)
    with tabs[2]:
        st.dataframe(data.tables["Phu_tung"], use_container_width=True, hide_index=True)
    with tabs[3]:
        st.plotly_chart(
            dark_chart(px.scatter(vendor, x="On-time Delivery", y="Quality Score",
                                  size="Spend YTD (tỷ)", color="Compliance",
                                  hover_name="Nhà cung cấp"), "Vendor Performance"),
            use_container_width=True
        )
        st.dataframe(vendor, use_container_width=True, hide_index=True)
    with tabs[4]:
        st.dataframe(data.tables["Don_vi"], use_container_width=True, hide_index=True)
