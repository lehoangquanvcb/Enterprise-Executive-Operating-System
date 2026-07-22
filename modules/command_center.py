
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from model import enterprise_metrics, dealer_health
from ui import bieu_do_toi


def _risk_donut(data):
    ews = data.tables["Early_Warning"].copy()
    counts = ews["Mức cảnh báo"].value_counts()
    labels = ["Green", "Amber", "Red"]
    vn_labels = ["Thấp", "Trung bình", "Cao"]
    values = [int(counts.get(x, 0)) for x in labels]
    colors = ["#22C55E", "#F59E0B", "#EF4444"]
    fig = go.Figure(
        go.Pie(
            labels=vn_labels,
            values=values,
            hole=0.62,
            marker=dict(colors=colors),
            textinfo="none",
        )
    )
    fig.add_annotation(
        text=f"<b>{sum(values)}</b><br>Đại lý",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=15, color="#F8FAFC"),
    )
    fig.update_layout(showlegend=True)
    return bieu_do_toi(fig, "RỦI RO DOANH NGHIỆP (EWS)")


def _initiative_donut(data):
    projects = data.tables["Du_an"].copy()
    status = projects["Trạng thái"].fillna("Chưa xác định").value_counts()
    labels = status.index.tolist()
    values = status.values.tolist()
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.62,
            textinfo="none",
        )
    )
    fig.add_annotation(
        text=f"<b>{sum(values)}</b><br>Tổng số",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=15, color="#F8FAFC"),
    )
    return bieu_do_toi(fig, "SÁNG KIẾN CHIẾN LƯỢC")


def render(data, scenario):
    m = enterprise_metrics(data)

    st.markdown("### BỨC TRANH HIỆU QUẢ TOÀN DOANH NGHIỆP")
    cols = st.columns(8, gap="small")
    metrics = [
        ("DOANH THU HỢP NHẤT", f"{m['revenue']:,.0f}", "tỷ VND"),
        ("EBITDA", f"{m['ebitda']:,.1f}", "tỷ VND"),
        ("BIÊN EBITDA", f"{m['margin']:.1%}", ""),
        ("TIỀN MẶT THẤP NHẤT (13T)", f"{m['cash_min']:,.1f}", "tỷ VND"),
        ("ĐẠI LÝ RỦI RO CAO", f"{m['red_ews']}", "đại lý"),
        ("LEAKAGE CHIẾT KHẤU", f"{m['discount_leakage']:,.2f}", "tỷ VND"),
        ("HÀNH ĐỘNG QUÁ HẠN", f"{m['overdue_actions']}", "hành động"),
        ("QUYẾT ĐỊNH CHỜ DUYỆT", f"{m['pending_decisions']}", "quyết định"),
    ]
    for col, (label, value, unit) in zip(cols, metrics):
        with col:
            st.metric(label, value)
            if unit:
                st.caption(unit)

    # Hàng 1: Doanh thu / Dealer Health / EWS
    left, middle, right = st.columns([1.55, 1.25, 1.0], gap="small")

    with left:
        financial = data.tables["Tai_chinh"].copy()
        financial["Tháng"] = pd.to_datetime(financial["Tháng"], errors="coerce")
        fig = go.Figure()
        fig.add_bar(
            x=financial["Tháng"],
            y=financial["Doanh thu xe TH"] + financial["Doanh thu dịch vụ TH"],
            name="Doanh thu",
            marker_color="#2387FF",
        )
        fig.add_scatter(
            x=financial["Tháng"],
            y=financial["EBITDA TH"],
            name="EBITDA",
            mode="lines+markers",
            yaxis="y2",
            line=dict(color="#22C55E", width=2),
        )
        fig.update_layout(
            yaxis2=dict(overlaying="y", side="right", showgrid=False),
            barmode="group",
        )
        st.plotly_chart(
            bieu_do_toi(fig, "DOANH THU & EBITDA THEO THÁNG"),
            use_container_width=True,
        )

    with middle:
        health = dealer_health(data).head(10).copy()
        health["Điểm"] = health["Health Score"].round(0).astype(int)
        health["EWS"] = health["Mức cảnh báo"].map(
            {"Green": "Thấp", "Amber": "Trung bình", "Red": "Cao"}
        ).fillna(health["Mức cảnh báo"])
        display = health[
            ["Đại lý", "Điểm", "EWS", "Biên EBITDA", "Cash Conversion Cycle"]
        ].rename(columns={"Cash Conversion Cycle": "CC Cycle"})
        st.markdown("##### XẾP HẠNG SỨC KHỎE ĐẠI LÝ (TOP 10)")
        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
            height=330,
            column_config={
                "Biên EBITDA": st.column_config.NumberColumn(format="%.1%%"),
                "CC Cycle": st.column_config.NumberColumn(format="%.0f ngày"),
            },
        )

    with right:
        st.plotly_chart(_risk_donut(data), use_container_width=True)

    # Hàng 2: Cash / Priority findings / initiatives
    left, middle, right = st.columns([1.55, 1.25, 1.0], gap="small")

    with left:
        cash = data.tables["Cash_Flow_13W"].copy()
        fig = go.Figure()
        fig.add_scatter(
            x=cash["Bắt đầu"],
            y=cash["Tiền cuối kỳ"],
            mode="lines+markers",
            line=dict(color="#7C5CFC", width=2),
            name="Tiền cuối kỳ",
        )
        fig.add_scatter(
            x=cash["Bắt đầu"],
            y=cash["Mức tiền tối thiểu"],
            mode="lines",
            line=dict(color="#F59E0B", width=1, dash="dash"),
            name="Mức tối thiểu",
        )
        st.plotly_chart(
            bieu_do_toi(fig, "DÒNG TIỀN 13 TUẦN (TỐI THIỂU)"),
            use_container_width=True,
        )

    with middle:
        brief = data.tables["Executive_Brief"].copy().head(5)
        display = brief[
            ["Mức độ", "Phát hiện", "Khuyến nghị điều hành", "SLA"]
        ].rename(
            columns={
                "Khuyến nghị điều hành": "Khuyến nghị",
                "SLA": "Hạn xử lý",
            }
        )
        st.markdown("##### PHÁT HIỆN ƯU TIÊN")
        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
            height=330,
        )

    with right:
        st.plotly_chart(_initiative_donut(data), use_container_width=True)
