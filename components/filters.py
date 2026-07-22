
from __future__ import annotations
import pandas as pd
import streamlit as st
from model import filter_data
from config import FILE_MASTER

NHAN_KICH_BAN = {"Cơ sở":"Base", "Tích cực":"Upside", "Bất lợi":"Downside"}

def bang_dieu_khien_ngang(data):
    dm = data.tables["Don_vi"]
    brands = sorted(dm["Thương hiệu"].dropna().unique().tolist())
    periods = sorted(
        pd.to_datetime(data.tables["Forecast"]["Tháng"], errors="coerce")
        .dropna().dt.strftime("%m/%Y").unique().tolist()
    )

    st.markdown('<div class="top-panel">', unsafe_allow_html=True)
    c0, c1, c2, c3, c4, c5 = st.columns([1.15, 1.45, 2.2, 1.25, 1.15, 1.1], gap="small")

    with c0:
        with st.popover("📤 Tải Master Excel V7", use_container_width=True):
            uploaded = st.file_uploader(
                "Chọn file Excel",
                type=["xlsx"],
                label_visibility="collapsed",
                key="tai_master_v7",
            )
            st.download_button(
                "⬇️ Tải file Master mẫu",
                FILE_MASTER.read_bytes(),
                FILE_MASTER.name,
                use_container_width=True,
            )

    with c1:
        selected_brands = st.multiselect(
            "Thương hiệu",
            brands,
            default=brands,
            key="thuong_hieu_v7",
        )

    dealer_options = sorted(
        dm[dm["Thương hiệu"].isin(selected_brands)]["Tên đại lý"]
        .dropna().unique().tolist()
    )
    with c2:
        selected_dealers = st.multiselect(
            "Đại lý",
            dealer_options,
            default=dealer_options,
            key="dai_ly_v7",
        )

    with c3:
        scenario_vn = st.selectbox(
            "Kịch bản",
            list(NHAN_KICH_BAN.keys()),
            key="kich_ban_v7",
        )

    with c4:
        period = st.selectbox(
            "Kỳ báo cáo",
            periods if periods else ["Toàn kỳ"],
            index=len(periods)-1 if periods else 0,
            key="ky_bao_cao_v7",
        )

    with c5:
        view_mode = st.selectbox(
            "Chế độ xem",
            ["Toàn doanh nghiệp", "Theo lựa chọn"],
            key="che_do_xem_v7",
        )

    st.markdown('</div>', unsafe_allow_html=True)
    filtered = filter_data(data, selected_brands, selected_dealers)
    return filtered, NHAN_KICH_BAN[scenario_vn], uploaded, period, view_mode
