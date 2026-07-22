
import plotly.express as px
import streamlit as st
from ui import page_header, metric_row, dark_chart

def render(data, scenario):
    page_header("People & ESG", "Workforce productivity, capability, succession and sustainability")
    workforce = data.tables["Workforce"]
    esg = data.tables["ESG"]
    tabs = st.tabs(["Workforce","Capability","ESG"])
    with tabs[0]:
        metric_row([
            ("Headcount", int(workforce["Headcount"].sum()), None),
            ("Technicians", int(workforce["Kỹ thuật viên"].sum()), None),
            ("Average turnover", f"{workforce['Turnover'].mean():.1%}", None),
            ("Engagement", f"{workforce['Engagement'].mean():.1f}", None),
        ])
        st.plotly_chart(
            dark_chart(px.scatter(workforce, x="Headcount", y="Engagement",
                                  size="Kỹ thuật viên", color="Thương hiệu",
                                  hover_name="Đại lý"), "People Capacity"),
            use_container_width=True
        )
        st.dataframe(workforce, use_container_width=True, hide_index=True)
    with tabs[1]:
        st.plotly_chart(
            dark_chart(px.scatter(workforce, x="Đào tạo hoàn thành",
                                  y="Succession Coverage", size="Headcount",
                                  color="Thương hiệu", hover_name="Đại lý"),
                       "Capability & Succession"),
            use_container_width=True
        )
    with tabs[2]:
        st.plotly_chart(
            dark_chart(px.scatter(esg, x="Tỷ lệ điện mặt trời", y="Tái chế chất thải",
                                  size="Điện năng (MWh)", color="Thương hiệu",
                                  hover_name="Đại lý"), "Dealer ESG"),
            use_container_width=True
        )
        st.dataframe(esg, use_container_width=True, hide_index=True)
