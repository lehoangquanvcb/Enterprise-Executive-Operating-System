
import plotly.express as px
import streamlit as st
from model import enterprise_metrics, dealer_health
from ui import tieu_de_trang, dong_chi_so, the_dieu_hanh, bieu_do_toi, hien_thi_bang, tai_bang

def render(data, scenario):
    tieu_de_trang("Tổng quan Điều hành", f"{data.company_name} · {data.reporting_period}")
    m = enterprise_metrics(data)
    dong_chi_so([
        ("Doanh thu hợp nhất", f"{m['revenue']:,.0f} tỷ", None),
        ("EBITDA", f"{m['ebitda']:,.1f} tỷ", f"{m['margin']:.1%}"),
        ("Tiền mặt thấp nhất", f"{m['cash_min']:,.1f} tỷ", None),
        ("Tỷ lệ Lead→Đơn hàng", f"{m['lead_conversion']:.1%}", None),
        ("Giao xe đúng hạn", f"{m['on_time_delivery']:.1%}", None),
        ("Đại lý cảnh báo đỏ", m["red_ews"], None),
        ("Rò rỉ chiết khấu", f"{m['discount_leakage']:,.2f} tỷ", None),
        ("Hành động quá hạn", m["overdue_actions"], None),
    ])
    tabs = st.tabs(["Bản tin buổi sáng","Danh mục đại lý","Thanh khoản & Biên lợi nhuận","Hàng đợi quyết định"])
    with tabs[0]:
        for _, row in data.tables["Executive_Brief"].sort_values("Ưu tiên").iterrows():
            the_dieu_hanh(
                row["Chủ đề"], row["Phát hiện"], row["Khuyến nghị điều hành"],
                row["Owner"], row["SLA"], "critical" if row["Mức độ"] == "High" else "warning"
            )
    with tabs[1]:
        h = dealer_health(data)
        left, right = st.columns(2)
        left.plotly_chart(
            bieu_do_toi(px.bar(h.head(12), x="Health Score", y="Đại lý", orientation="h",
                               color="Thương hiệu"), "Xếp hạng sức khỏe đại lý"),
            use_container_width=True,
        )
        right.plotly_chart(
            bieu_do_toi(px.scatter(h, x="Cash Conversion Cycle", y="Biên EBITDA",
                                   size="EBITDA", color="Mức cảnh báo", hover_name="Đại lý"),
                        "Ma trận Giá trị – Thanh khoản"),
            use_container_width=True,
        )
        hien_thi_bang(h)
        tai_bang(h, "Tải bảng sức khỏe đại lý", "suc_khoe_dai_ly.csv")
    with tabs[2]:
        cash = data.tables["Cash_Flow_13W"]
        pnl = data.tables["Dealer_PnL"]
        left, right = st.columns(2)
        left.plotly_chart(
            bieu_do_toi(px.line(cash, x="Bắt đầu", y=["Tiền cuối kỳ","Mức tiền tối thiểu"],
                                markers=True), "Dòng tiền 13 tuần"),
            use_container_width=True,
        )
        right.plotly_chart(
            bieu_do_toi(px.scatter(pnl, x="Doanh thu xe", y="Biên EBITDA",
                                   size="EBITDA", color="Thương hiệu", hover_name="Đại lý"),
                        "Danh mục biên lợi nhuận đại lý"),
            use_container_width=True,
        )
    with tabs[3]:
        st.subheader("Quyết định đang chờ")
        hien_thi_bang(data.tables["Quyet_dinh"].sort_values("Trạng thái"))
        st.subheader("Hành động cần chú ý")
        hien_thi_bang(data.tables["Action_Impact"].sort_values(["Status","Due Date"]))
