
import plotly.express as px
import streamlit as st
from ui import tieu_de_trang, dong_chi_so, bieu_do_toi, hien_thi_bang

def render(data, scenario):
    tieu_de_trang("Con người & ESG", "Năng suất nhân sự, năng lực, kế nhiệm và phát triển bền vững")
    workforce = data.tables["Workforce"]
    esg = data.tables["ESG"]
    tabs = st.tabs(["Nhân sự","Năng lực & Kế nhiệm","ESG"])
    with tabs[0]:
        dong_chi_so([
            ("Tổng nhân sự", int(workforce["Headcount"].sum()), None),
            ("Kỹ thuật viên", int(workforce["Kỹ thuật viên"].sum()), None),
            ("Tỷ lệ nghỉ việc bình quân", f"{workforce['Turnover'].mean():.1%}", None),
            ("Điểm gắn kết", f"{workforce['Engagement'].mean():.1f}", None),
        ])
        st.plotly_chart(
            bieu_do_toi(px.scatter(workforce, x="Headcount", y="Engagement",
                                   size="Kỹ thuật viên", color="Thương hiệu",
                                   hover_name="Đại lý"), "Năng lực nhân sự"),
            use_container_width=True
        )
        hien_thi_bang(workforce)
    with tabs[1]:
        st.plotly_chart(
            bieu_do_toi(px.scatter(workforce, x="Đào tạo hoàn thành",
                                   y="Succession Coverage", size="Headcount",
                                   color="Thương hiệu", hover_name="Đại lý"),
                        "Năng lực & Kế nhiệm"),
            use_container_width=True
        )
    with tabs[2]:
        st.plotly_chart(
            bieu_do_toi(px.scatter(esg, x="Tỷ lệ điện mặt trời", y="Tái chế chất thải",
                                   size="Điện năng (MWh)", color="Thương hiệu",
                                   hover_name="Đại lý"), "Hiệu quả ESG đại lý"),
            use_container_width=True
        )
        hien_thi_bang(esg)
