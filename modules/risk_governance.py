
import plotly.express as px
import streamlit as st
from model import dynamic_ews
from ui import tieu_de_trang, dong_chi_so, bieu_do_toi, hien_thi_bang

def render(data, scenario):
    tieu_de_trang("Rủi ro & Kiểm soát", "Cảnh báo sớm, rủi ro doanh nghiệp, kiểm soát, kiểm toán và thực thi")
    tabs = st.tabs(["Cảnh báo sớm động","Danh mục rủi ro","Ma trận kiểm soát","Kiểm toán & Chính sách","Tác động hành động"])
    with tabs[0]:
        c1, c2, c3, c4 = st.columns(4)
        a = c1.slider("Rủi ro nền", 0, 100, 40) / 100
        b = c2.slider("Vốn lưu động", 0, 100, 25) / 100
        c = c3.slider("Thương mại", 0, 100, 20) / 100
        e = c4.slider("Biên lợi nhuận", 0, 100, 15) / 100
        total = a + b + c + e or 1
        ews = dynamic_ews(data, {
            "base": a/total, "working_capital": b/total,
            "commercial": c/total, "margin": e/total
        })
        st.plotly_chart(
            bieu_do_toi(px.bar(ews, x="Dynamic EWS", y="Đại lý", orientation="h",
                               color="Dynamic Level",
                               color_discrete_map={"Xanh":"#22C55E","Vàng":"#F59E0B","Đỏ":"#EF4444"}),
                        "Xếp hạng cảnh báo sớm động"),
            use_container_width=True
        )
        hien_thi_bang(ews)
    with tabs[1]:
        risks = data.tables["Rui_ro"]
        st.plotly_chart(
            bieu_do_toi(px.scatter(risks, x="Khả năng", y="Tác động",
                                   size="Điểm rủi ro", color="Trạng thái",
                                   hover_name="Rủi ro"), "Bản đồ rủi ro doanh nghiệp"),
            use_container_width=True
        )
        hien_thi_bang(risks.sort_values("Điểm rủi ro", ascending=False))
    with tabs[2]:
        hien_thi_bang(data.tables["RCM"])
    with tabs[3]:
        st.subheader("Phát hiện kiểm toán")
        hien_thi_bang(data.tables["Audit_Findings"])
        st.subheader("Danh mục chính sách")
        hien_thi_bang(data.tables["Policy_Register"])
    with tabs[4]:
        action = data.tables["Action_Impact"]
        expected = float(action["Expected Impact (bn)"].sum())
        actual = float(action["Actual Impact (bn)"].sum())
        dong_chi_so([
            ("Tác động kỳ vọng", f"{expected:,.1f} tỷ", None),
            ("Tác động thực tế", f"{actual:,.1f} tỷ", None),
            ("Tỷ lệ hiện thực hóa", f"{actual/expected:.1%}" if expected else "-", None),
            ("Quá hạn", int((action["Status"] == "Overdue").sum()), None),
        ])
        st.plotly_chart(
            bieu_do_toi(px.scatter(action, x="Expected Impact (bn)", y="Actual Impact (bn)",
                                   color="Status", size="Expected Impact (bn)",
                                   hover_name="Action"), "Hiện thực hóa giá trị hành động"),
            use_container_width=True
        )
        hien_thi_bang(action.sort_values(["Status","Due Date"]))
