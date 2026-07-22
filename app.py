
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
    /* ===== BỐ CỤC CHUNG ===== */
    .block-container {
        padding-top: 1.05rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 1760px !important;
    }

    header[data-testid="stHeader"] {
        height: 2.55rem !important;
        background: rgba(7, 15, 28, 0.98) !important;
        border-bottom: 1px solid rgba(35, 49, 74, 0.72);
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    /* ===== HEADER ỨNG DỤNG ===== */
    .eeos-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-height: 58px;
        padding: 4px 2px 9px 2px;
        border-bottom: 1px solid #1E2C43;
        margin-bottom: 10px;
    }

    .eeos-header-main {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
    }

    .eeos-header-logo {
        display: grid;
        place-items: center;
        width: 38px;
        height: 38px;
        flex: 0 0 38px;
        border-radius: 11px;
        background: linear-gradient(145deg, #1D4ED8, #6D28D9);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.26);
        font-size: 1.15rem;
    }

    .eeos-header-title {
        color: #F8FAFC;
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: clamp(1.45rem, 1.8vw, 2rem);
        font-weight: 800;
        line-height: 1.2;
        letter-spacing: -0.015em;
        margin: 0;
    }

    .eeos-header-subtitle {
        color: #8FA0B8;
        font-size: 0.78rem;
        line-height: 1.4;
        margin-top: 3px;
    }

    .eeos-header-tools {
        display: flex;
        align-items: center;
        gap: 18px;
        color: #CBD5E1;
        font-size: 0.78rem;
        white-space: nowrap;
    }

    .eeos-tool {
        opacity: 0.9;
    }

    /* ===== PANEL BỘ LỌC NGANG ===== */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #263650 !important;
        border-radius: 12px !important;
        background: linear-gradient(145deg, #0E192B, #111D31) !important;
    }

    .eeos-filter-title {
        color: #73849F;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-weight: 700;
        margin-bottom: 1px;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stFileUploader"] label {
        color: #D9E2EF !important;
        font-size: 0.74rem !important;
        font-weight: 650 !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 38px !important;
        border-radius: 8px !important;
        background: #0A1425 !important;
        border-color: #1F304A !important;
    }

    div[data-testid="stPopover"] button {
        min-height: 38px !important;
        border-radius: 8px !important;
        background: #0A1425 !important;
        border-color: #30425E !important;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        width: 235px !important;
        min-width: 235px !important;
        background:
            radial-gradient(circle at 10% 0%, rgba(37, 99, 235, 0.12), transparent 28%),
            linear-gradient(180deg, #0D182A 0%, #091321 100%) !important;
        border-right: 1px solid #22324A !important;
        box-shadow: 7px 0 22px rgba(0, 0, 0, 0.18);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0.55rem !important;
    }

    .eeos-side-brand {
        display: flex;
        align-items: center;
        gap: 9px;
        margin: 0 2px 12px 2px;
        padding: 11px;
        border: 1px solid #263650;
        border-radius: 12px;
        background: linear-gradient(145deg, rgba(20, 32, 53, 0.98), rgba(12, 23, 40, 0.98));
    }

    .eeos-side-logo {
        display: grid;
        place-items: center;
        width: 32px;
        height: 32px;
        flex: 0 0 32px;
        border-radius: 9px;
        background: linear-gradient(145deg, #2563EB, #7C3AED);
        font-size: 0.95rem;
    }

    .eeos-side-name {
        color: #F8FAFC;
        font-size: 0.82rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .eeos-side-sub {
        color: #8292A9;
        font-size: 0.64rem;
        line-height: 1.25;
        margin-top: 2px;
    }

    .eeos-menu-group {
        color: #65758D;
        font-size: 0.60rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 11px 7px 4px 8px;
    }

    /* Các nút menu trong sidebar */
    section[data-testid="stSidebar"] div[data-testid="stButton"] {
        margin: 1px 1px !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button {
        width: 100% !important;
        min-height: 37px !important;
        justify-content: flex-start !important;
        text-align: left !important;
        padding: 7px 9px !important;
        border-radius: 8px !important;
        font-size: 0.74rem !important;
        line-height: 1.2 !important;
        transition: all 140ms ease !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"] {
        color: #C8D3E1 !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]:hover {
        color: #FFFFFF !important;
        background: rgba(59, 130, 246, 0.10) !important;
        border-color: rgba(96, 165, 250, 0.16) !important;
        transform: translateX(2px);
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] {
        color: #FFFFFF !important;
        background: linear-gradient(90deg, rgba(37, 99, 235, 0.80), rgba(109, 40, 217, 0.72)) !important;
        border: 1px solid rgba(96, 165, 250, 0.30) !important;
        box-shadow:
            inset 3px 0 0 #60A5FA,
            0 5px 13px rgba(0, 0, 0, 0.20) !important;
        font-weight: 750 !important;
    }

    .eeos-side-footer {
        margin: 14px 5px 0 5px;
        padding: 10px 6px 4px 6px;
        border-top: 1px solid #24344D;
        color: #61718A;
        font-size: 0.62rem;
        line-height: 1.45;
    }

    .eeos-system-status {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #8797AD;
        margin-bottom: 4px;
    }

    .eeos-status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #22C55E;
        box-shadow: 0 0 8px rgba(34, 197, 94, 0.72);
    }

    /* ===== KPI VÀ TAB ===== */
    div[data-testid="stMetric"] {
        min-height: 92px !important;
        padding: 12px !important;
        border-radius: 11px !important;
        background: linear-gradient(145deg, #111D31, #142037) !important;
        border: 1px solid #283A55 !important;
    }

    div[data-testid="stMetricLabel"] p {
        font-size: 0.72rem !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.55rem !important;
    }

    button[data-baseweb="tab"] {
        padding-left: 10px !important;
        padding-right: 10px !important;
        font-size: 0.75rem !important;
    }

    h1 {
        font-size: clamp(1.8rem, 2.3vw, 2.55rem) !important;
        margin-top: 0.35rem !important;
        margin-bottom: 0.15rem !important;
    }

    @media (max-width: 1200px) {
        .eeos-header-tools {
            display: none;
        }
        section[data-testid="stSidebar"] {
            width: 220px !important;
            min-width: 220px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def tai_du_lieu(file_bytes: bytes | None = None):
    source = BytesIO(file_bytes) if file_bytes else FILE_MASTER
    return prepare(load_master(source))


def lay_ky_bao_cao(data) -> list[str]:
    periods = (
        pd.to_datetime(data.tables["Forecast"]["Tháng"], errors="coerce")
        .dropna()
        .dt.strftime("%m/%Y")
        .unique()
        .tolist()
    )
    return sorted(periods) if periods else ["Toàn kỳ"]


def hien_thi_header() -> None:
    st.markdown(
        f"""
        <div class="eeos-header">
            <div class="eeos-header-main">
                <div class="eeos-header-logo">🚘</div>
                <div>
                    <div class="eeos-header-title">{TEN_UNG_DUNG}</div>
                    <div class="eeos-header-subtitle">
                        {PHU_DE} · {PHIEN_BAN} · Tác giả: {TAC_GIA}
                    </div>
                </div>
            </div>
            <div class="eeos-header-tools">
                <span class="eeos-tool">🔔 Thông báo</span>
                <span class="eeos-tool">🧰 Bộ công cụ</span>
                <span class="eeos-tool">⬇ Xuất báo cáo</span>
                <span class="eeos-tool">❔ Trợ giúp</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def panel_bo_loc(data):
    dealer_master = data.tables["Don_vi"].copy()
    brands = sorted(dealer_master["Thương hiệu"].dropna().unique().tolist())
    periods = lay_ky_bao_cao(data)

    with st.container(border=True):
        c0, c1, c2, c3, c4, c5 = st.columns(
            [1.05, 1.28, 1.85, 1.08, 1.15, 1.08],
            gap="small",
        )

        with c0:
            with st.popover("📥 Master Excel V7", use_container_width=True):
                uploaded = st.file_uploader(
                    "Chọn file Excel",
                    type=["xlsx"],
                    label_visibility="collapsed",
                    key="upload_master_v7_pro",
                )
                st.download_button(
                    "⬇ Tải Master mẫu",
                    FILE_MASTER.read_bytes(),
                    FILE_MASTER.name,
                    use_container_width=True,
                )

        brand_options = ["Tất cả thương hiệu", *brands]
        with c1:
            brand_choice = st.selectbox(
                "Thương hiệu",
                brand_options,
                key="brand_v7_pro",
            )

        if brand_choice == "Tất cả thương hiệu":
            selected_brands = brands
            dealer_frame = dealer_master
        else:
            selected_brands = [brand_choice]
            dealer_frame = dealer_master[
                dealer_master["Thương hiệu"] == brand_choice
            ]

        dealer_options = [
            "Tất cả đại lý",
            *sorted(dealer_frame["Tên đại lý"].dropna().unique().tolist()),
        ]
        if st.session_state.get("dealer_v7_pro", "Tất cả đại lý") not in dealer_options:
            st.session_state["dealer_v7_pro"] = "Tất cả đại lý"

        with c2:
            dealer_choice = st.selectbox(
                "Đại lý",
                dealer_options,
                key="dealer_v7_pro",
            )

        with c3:
            scenario_vi = st.selectbox(
                "Kịch bản",
                ["Cơ sở", "Tích cực", "Bất lợi"],
                key="scenario_v7_pro",
            )

        with c4:
            reporting_period = st.selectbox(
                "Kỳ báo cáo",
                periods,
                index=len(periods) - 1,
                key="period_v7_pro",
            )

        with c5:
            view_mode = st.selectbox(
                "Chế độ xem",
                ["Toàn doanh nghiệp", "Theo lựa chọn"],
                key="view_v7_pro",
            )

    selected_dealers = None if dealer_choice == "Tất cả đại lý" else [dealer_choice]
    filtered = filter_data(
        data,
        brands=selected_brands,
        dealers=selected_dealers,
    )
    scenario_map = {
        "Cơ sở": "Base",
        "Tích cực": "Upside",
        "Bất lợi": "Downside",
    }
    return filtered, scenario_map[scenario_vi], uploaded, reporting_period, view_mode


# Dữ liệu mặc định
try:
    du_lieu_goc = tai_du_lieu()
except Exception as exc:
    st.error(f"Lỗi tải file Master mặc định: {exc}")
    st.stop()

hien_thi_header()
du_lieu_loc, kich_ban, uploaded, ky_bao_cao, che_do_xem = panel_bo_loc(
    du_lieu_goc
)

if uploaded is not None:
    try:
        uploaded_data = tai_du_lieu(uploaded.getvalue())
        dealer_master = uploaded_data.tables["Don_vi"]

        selected_brand = st.session_state.get(
            "brand_v7_pro",
            "Tất cả thương hiệu",
        )
        selected_dealer = st.session_state.get(
            "dealer_v7_pro",
            "Tất cả đại lý",
        )

        available_brands = sorted(
            dealer_master["Thương hiệu"].dropna().unique().tolist()
        )
        brand_filter = (
            available_brands
            if selected_brand == "Tất cả thương hiệu"
            else [selected_brand]
        )
        dealer_filter = (
            None
            if selected_dealer == "Tất cả đại lý"
            else [selected_dealer]
        )
        du_lieu_loc = filter_data(
            uploaded_data,
            brands=brand_filter,
            dealers=dealer_filter,
        )
    except Exception as exc:
        st.error(f"File tải lên không hợp lệ: {exc}")
        st.stop()


MENU_GROUPS = [
    (
        "Tổng quan",
        [
            ("🏠 Tổng quan điều hành", "command_center"),
        ],
    ),
    (
        "Chiến lược & Hiệu quả",
        [
            ("🎯 Chiến lược & KPI", "strategy"),
        ],
    ),
    (
        "Thương mại & Tăng trưởng",
        [
            ("📈 Thương mại & Tăng trưởng", "commercial"),
        ],
    ),
    (
        "Tài chính & Nguồn vốn",
        [
            ("💰 Tài chính & Nguồn vốn", "finance"),
        ],
    ),
    (
        "Đại lý 360°",
        [
            ("🏢 Đại lý 360°", "dealer_360"),
        ],
    ),
    (
        "Vận hành & Aftersales",
        [
            ("🛠 Vận hành & Aftersales", "operations"),
        ],
    ),
    (
        "Rủi ro & Kiểm soát",
        [
            ("🛡 Rủi ro & Kiểm soát", "risk_governance"),
        ],
    ),
    (
        "Kịch bản",
        [
            ("🧪 Kịch bản & Mô phỏng", "scenario_lab"),
        ],
    ),
    (
        "Quản trị doanh nghiệp",
        [
            ("👥 Con người & ESG", "people_esg"),
            ("📄 Báo cáo Hội đồng", "board_reporting"),
            ("🗂 Dữ liệu & Chất lượng", "data_quality"),
            ("🤖 Trợ lý điều hành", "copilot"),
        ],
    ),
]

if "module_v7_professional" not in st.session_state:
    st.session_state["module_v7_professional"] = "command_center"

with st.sidebar:
    st.markdown(
        """
        <div class="eeos-side-brand">
            <div class="eeos-side-logo">🚘</div>
            <div>
                <div class="eeos-side-name">EEOS V7</div>
                <div class="eeos-side-sub">Hệ thống Điều hành Doanh nghiệp</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for group_name, entries in MENU_GROUPS:
        st.markdown(
            f'<div class="eeos-menu-group">{group_name}</div>',
            unsafe_allow_html=True,
        )
        for label, module_name in entries:
            active = st.session_state["module_v7_professional"] == module_name
            if st.button(
                label,
                key=f"nav_{module_name}",
                type="primary" if active else "secondary",
                use_container_width=True,
            ):
                st.session_state["module_v7_professional"] = module_name
                st.rerun()

    st.markdown(
        """
        <div class="eeos-side-footer">
            <div class="eeos-system-status">
                <span class="eeos-status-dot"></span>
                <span>Hệ thống hoạt động bình thường</span>
            </div>
            Dữ liệu trong ứng dụng là dữ liệu giả lập phục vụ trình diễn.
        </div>
        """,
        unsafe_allow_html=True,
    )


try:
    selected_module = st.session_state["module_v7_professional"]
    module = __import__(f"modules.{selected_module}", fromlist=["render"])
    module.render(du_lieu_loc, kich_ban)
except Exception as exc:
    st.error(f"Lỗi tại module: {exc}")
    with st.expander("Chi tiết kỹ thuật"):
        st.exception(exc)

st.divider()
st.caption(
    f"Hệ thống Điều hành Doanh nghiệp · {PHIEN_BAN} · Tác giả: {TAC_GIA}"
)
