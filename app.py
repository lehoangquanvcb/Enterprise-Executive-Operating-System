
from __future__ import annotations

from io import BytesIO

import pandas as pd
import streamlit as st

from config import TEN_UNG_DUNG, PHU_DE, PHIEN_BAN, TAC_GIA, FILE_MASTER
from model import filter_data, load_master, prepare
from ui import chen_css


st.set_page_config(
    page_title=TEN_UNG_DUNG,
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)
chen_css()

st.markdown(
    """
    <style>
    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display:none !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding-top:0 !important;
    }

    .eeos-topbar {
        display:flex;
        align-items:center;
        justify-content:space-between;
        min-height:66px;
        padding:9px 6px 10px 6px;
        border-bottom:1px solid #18304A;
        overflow:visible;
    }

    .eeos-topbar-left {
        display:flex;
        align-items:center;
        gap:12px;
    }

    .eeos-topbar-title {
        color:#F8FAFC;
        font-family:"Segoe UI",Arial,sans-serif;
        font-size:clamp(1.35rem,1.7vw,1.95rem);
        font-weight:800;
        line-height:1.42;
        letter-spacing:-.015em;
        padding:3px 0 4px 0;
        white-space:nowrap;
        overflow:visible;
    }

    .eeos-topbar-subtitle {
        color:#8293AC;
        font-size:.72rem;
    }

    .eeos-topbar-tools {
        display:flex;
        align-items:center;
        gap:20px;
        color:#DCE6F5;
        font-size:.72rem;
        white-space:nowrap;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:linear-gradient(180deg,#0A1728,#0C192B) !important;
        border:1px solid #1D3552 !important;
        border-radius:10px !important;
    }

    div[data-baseweb="select"] > div {
        min-height:36px !important;
        background:#081424 !important;
        border:1px solid #1C314B !important;
        border-radius:7px !important;
    }

    section[data-testid="stSidebar"] {
        width:210px !important;
        min-width:210px !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button {
        position:relative !important;
        display:flex !important;
        align-items:center !important;
        justify-content:flex-start !important;
        width:100% !important;
        min-height:37px !important;
        padding:7px 9px 7px 31px !important;
        text-align:left !important;
        border-radius:7px !important;
        font-size:.71rem !important;
        line-height:1.22 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button::before {
        content:"›";
        position:absolute;
        left:12px;
        top:50%;
        transform:translateY(-52%);
        width:10px;
        color:#8293AC;
        font-size:.86rem;
        font-weight:800;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button p,
    section[data-testid="stSidebar"] div[data-testid="stButton"] button span {
        width:100% !important;
        margin:0 !important;
        padding:0 !important;
        text-align:left !important;
        white-space:normal !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"] {
        color:#C8D4E3 !important;
        background:transparent !important;
        border:1px solid transparent !important;
        box-shadow:none !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]:hover {
        color:#FFFFFF !important;
        background:rgba(35,135,255,.10) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] {
        color:#FFFFFF !important;
        background:linear-gradient(90deg,rgba(27,103,211,.78),rgba(63,45,190,.72)) !important;
        border:1px solid rgba(70,137,255,.22) !important;
        box-shadow:inset 3px 0 0 #3DA0FF !important;
        font-weight:720 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"]::before {
        content:"⌂";
        color:#E8F2FF;
        font-size:.70rem;
    }

    .sidebar-status {
        margin:16px 6px 0 6px;
        padding:9px 3px;
        border-top:1px solid #1A3048;
        color:#64758E;
        font-size:.60rem;
        line-height:1.45;
    }

    @media(max-width:1250px) {
        .eeos-topbar-tools {display:none;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def tai_du_lieu(file_bytes: bytes | None = None):
    source = BytesIO(file_bytes) if file_bytes else FILE_MASTER
    return prepare(load_master(source))


def lay_ky_bao_cao(data):
    periods = (
        pd.to_datetime(data.tables["Forecast"]["Tháng"], errors="coerce")
        .dropna().dt.strftime("%m/%Y").unique().tolist()
    )
    return sorted(periods) if periods else ["Toàn kỳ"]


def header_app():
    st.markdown(
        f"""
        <div class="eeos-topbar">
            <div class="eeos-topbar-left">
                <div style="font-size:1.7rem;">🚘</div>
                <div>
                    <div class="eeos-topbar-title">
                        HỆ THỐNG ĐIỀU HÀNH DOANH NGHIỆP
                    </div>
                    <div class="eeos-topbar-subtitle">
                        {PHU_DE} · {PHIEN_BAN} · Tác giả: {TAC_GIA}
                    </div>
                </div>
            </div>
            <div class="eeos-topbar-tools">
                <span>🔔 Thông báo</span>
                <span>🧰 Bộ công cụ</span>
                <span>⬇ Xuất báo cáo</span>
                <span>❔ Trợ giúp</span>
                <span>◯ LQ</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


MENU = [
    ("Tổng quan điều hành", "command_center"),
    ("Chiến lược & Hiệu quả", "strategy"),
    ("Thương mại & Tăng trưởng", "commercial"),
    ("Tài chính & Nguồn vốn", "finance"),
    ("Đại lý 360°", "dealer_360"),
    ("Vận hành & Dịch vụ sau bán hàng", "operations"),
    ("Rủi ro & Kiểm soát", "risk_governance"),
    ("Kịch bản & Mô phỏng", "scenario_lab"),
    ("Con người & ESG", "people_esg"),
    ("Báo cáo HĐQT", "board_reporting"),
    ("Dữ liệu & Chất lượng", "data_quality"),
    ("Trợ lý điều hành", "copilot"),
]

if "module_v8" not in st.session_state:
    st.session_state["module_v8"] = "command_center"

# Sidebar is rendered first so uploaded data is available to the main panel.
with st.sidebar:
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:9px;padding:7px 7px 10px 7px;
                    border-bottom:1px solid #1A3048;margin-bottom:8px;">
            <div style="display:grid;place-items:center;width:29px;height:29px;
                        border-radius:8px;background:linear-gradient(145deg,#2563EB,#6D28D9);">
                🚘
            </div>
            <div>
                <div style="color:#F8FAFC;font-size:.75rem;font-weight:800;">EEOS V8</div>
                <div style="color:#71839C;font-size:.56rem;">Trung tâm điều hành</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.popover("📤 Tải Master Excel V8", use_container_width=True):
        sidebar_upload = st.file_uploader(
            "Chọn file Excel",
            type=["xlsx"],
            label_visibility="collapsed",
            key="sidebar_upload_v8",
        )
        st.download_button(
            "⬇ Tải Master mẫu",
            FILE_MASTER.read_bytes(),
            FILE_MASTER.name,
            use_container_width=True,
        )

    st.markdown(
        '<div style="height:7px;border-bottom:1px solid #1A3048;margin-bottom:7px;"></div>',
        unsafe_allow_html=True,
    )

    for label, module_name in MENU:
        active = st.session_state["module_v8"] == module_name
        if st.button(
            label,
            key=f"nav_v8_{module_name}",
            type="primary" if active else "secondary",
            use_container_width=True,
        ):
            st.session_state["module_v8"] = module_name
            st.rerun()

    st.markdown(
        """
        <div class="sidebar-status">
            <div style="color:#8A9BB1;margin-bottom:4px;">● Hệ thống hoạt động bình thường</div>
            Dữ liệu giả lập phục vụ trình diễn.
        </div>
        """,
        unsafe_allow_html=True,
    )

try:
    data_raw = tai_du_lieu(
        sidebar_upload.getvalue() if sidebar_upload is not None else None
    )
except Exception as exc:
    st.error(f"Lỗi tải file Master: {exc}")
    st.stop()

header_app()

dm = data_raw.tables["Don_vi"].copy()
brands = sorted(dm["Thương hiệu"].dropna().unique().tolist())
periods = lay_ky_bao_cao(data_raw)

with st.container(border=True):
    c1, c2, c3, c4, c5 = st.columns([1.25, 1.85, 1.05, 1.15, 1.05], gap="small")

    with c1:
        brand_choice = st.selectbox(
            "Thương hiệu",
            ["Tất cả thương hiệu", *brands],
            key="brand_v8",
        )

    if brand_choice == "Tất cả thương hiệu":
        selected_brands = brands
        dealer_frame = dm
    else:
        selected_brands = [brand_choice]
        dealer_frame = dm[dm["Thương hiệu"] == brand_choice]

    dealer_options = [
        "Tất cả đại lý",
        *sorted(dealer_frame["Tên đại lý"].dropna().unique().tolist()),
    ]
    if st.session_state.get("dealer_v8", "Tất cả đại lý") not in dealer_options:
        st.session_state["dealer_v8"] = "Tất cả đại lý"

    with c2:
        dealer_choice = st.selectbox("Đại lý", dealer_options, key="dealer_v8")
    with c3:
        scenario_vi = st.selectbox(
            "Kịch bản", ["Cơ sở", "Tích cực", "Bất lợi"], key="scenario_v8"
        )
    with c4:
        reporting_period = st.selectbox(
            "Kỳ báo cáo", periods, index=len(periods)-1, key="period_v8"
        )
    with c5:
        view_mode = st.selectbox(
            "Chế độ xem", ["Tổng quan", "Theo lựa chọn"], key="view_v8"
        )

selected_dealers = None if dealer_choice == "Tất cả đại lý" else [dealer_choice]
data = filter_data(data_raw, brands=selected_brands, dealers=selected_dealers)
scenario = {"Cơ sở":"Base", "Tích cực":"Upside", "Bất lợi":"Downside"}[scenario_vi]

try:
    selected_module = st.session_state["module_v8"]
    module = __import__(f"modules.{selected_module}", fromlist=["render"])
    module.render(data, scenario)
except Exception as exc:
    st.error(f"Lỗi tại module: {exc}")
    with st.expander("Chi tiết kỹ thuật"):
        st.exception(exc)
