
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
    :root {
        --eeos-bg: #07111f;
        --eeos-panel: #0c192b;
        --eeos-panel-2: #101f34;
        --eeos-border: #1f3550;
        --eeos-text: #eef4ff;
        --eeos-muted: #8293ac;
        --eeos-blue: #2387ff;
        --eeos-purple: #4938d8;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: var(--eeos-bg) !important;
    }

    /* Ẩn header và toolbar mặc định của Streamlit.
       Header tùy chỉnh của ứng dụng sẽ là lớp trên cùng duy nhất. */
    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
    }

    .block-container {
        padding-top: 0.35rem !important;
        padding-bottom: 1.4rem !important;
        max-width: 1680px !important;
    }

    /* Header giống mẫu: mảnh, không tạo card lớn */
    .eeos-topbar {
        position: relative;
        z-index: 20;
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-height: 68px;
        padding: 9px 6px 10px 6px;
        border-bottom: 1px solid #18304a;
        overflow: visible !important;
    }

    .eeos-topbar-left {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
    }

    .eeos-topbar-logo {
        font-size: 1.75rem;
        line-height: 1;
    }

    .eeos-topbar-title {
        display: block;
        color: #f8fbff;
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: clamp(1.35rem, 1.7vw, 1.95rem);
        font-weight: 800;
        line-height: 1.42;
        letter-spacing: -0.015em;
        white-space: nowrap;
        padding: 3px 0 4px 0;
        overflow: visible !important;
    }

    .eeos-topbar-subtitle {
        color: #8092aa;
        font-size: 0.72rem;
        margin-top: 3px;
    }

    .eeos-topbar-tools {
        display: flex;
        align-items: center;
        gap: 22px;
        color: #dce6f5;
        font-size: 0.72rem;
        white-space: nowrap;
    }

    /* Panel lọc thấp, liền khối */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(180deg, #0a1728, #0c192b) !important;
        border: 1px solid #1d3552 !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        padding-top: 0.55rem !important;
        padding-bottom: 0.35rem !important;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stFileUploader"] label {
        color: #dce6f5 !important;
        font-size: 0.69rem !important;
        font-weight: 650 !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 35px !important;
        background: #081424 !important;
        border: 1px solid #1c314b !important;
        border-radius: 7px !important;
        font-size: 0.73rem !important;
    }

    div[data-testid="stPopover"] button {
        min-height: 35px !important;
        background: #081424 !important;
        border: 1px solid #27405f !important;
        border-radius: 7px !important;
        font-size: 0.72rem !important;
    }

    /* Sidebar giống mẫu: không có brand card, không có khoảng trống lớn */
    section[data-testid="stSidebar"] {
        width: 210px !important;
        min-width: 210px !important;
        background: linear-gradient(180deg, #091729 0%, #071421 100%) !important;
        border-right: 1px solid #1c324b !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0.75rem !important;
    }

    .side-mini-title {
        color: #6f829d;
        font-size: 0.57rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 12px 7px 5px 7px;
        padding-bottom: 4px;
        border-bottom: 1px solid rgba(31, 53, 80, 0.55);
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] {
        margin: 0 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button {
        width: 100% !important;
        min-height: 34px !important;
        justify-content: flex-start !important;
        text-align: left !important;
        padding: 6px 9px !important;
        border-radius: 6px !important;
        font-size: 0.69rem !important;
        line-height: 1.12 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"] {
        color: #c8d4e3 !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]:hover {
        color: #fff !important;
        background: rgba(35, 135, 255, 0.11) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] {
        color: #fff !important;
        background: linear-gradient(90deg, rgba(27, 103, 211, .75), rgba(63, 45, 190, .72)) !important;
        border: 1px solid rgba(70, 137, 255, .20) !important;
        box-shadow: inset 3px 0 0 #3da0ff !important;
        font-weight: 720 !important;
    }

    .side-footer {
        margin: 18px 8px 0 8px;
        padding: 9px 2px;
        border-top: 1px solid #1a3048;
        color: #60728c;
        font-size: 0.58rem;
        line-height: 1.45;
    }

    .side-status {
        color: #8596ac;
        margin-bottom: 4px;
    }

    /* KPI card sát mẫu */
    div[data-testid="stMetric"] {
        min-height: 100px !important;
        background: linear-gradient(145deg, #0e1d31, #112238) !important;
        border: 1px solid #223c5a !important;
        border-radius: 9px !important;
        padding: 11px 12px !important;
        box-shadow: none !important;
    }

    div[data-testid="stMetricLabel"] p {
        color: #aab9cc !important;
        font-size: 0.67rem !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fbff !important;
        font-size: 1.48rem !important;
    }

    h1 {
        font-size: 1.45rem !important;
        margin: 0.45rem 0 0.2rem 0 !important;
    }

    /* Panel biểu đồ */
    div[data-testid="stPlotlyChart"],
    div[data-testid="stDataFrame"] {
        border: 1px solid #1f3855;
        border-radius: 9px;
        background: #091729;
    }

    @media (max-width: 1250px) {
        .eeos-topbar-tools { display: none; }
        section[data-testid="stSidebar"] {
            width: 195px !important;
            min-width: 195px !important;
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


def header_app() -> None:
    st.markdown(
        f"""
        <div class="eeos-topbar">
            <div class="eeos-topbar-left">
                <div class="eeos-topbar-logo">🚘</div>
                <div>
                    <div class="eeos-topbar-title">HỆ THỐNG ĐIỀU HÀNH DOANH NGHIỆP</div>
                    <div class="eeos-topbar-subtitle">
                        {PHU_DE} · V7 · Tác giả: {TAC_GIA}
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


def panel_bo_loc(data):
    dm = data.tables["Don_vi"].copy()
    brands = sorted(dm["Thương hiệu"].dropna().unique().tolist())
    periods = lay_ky_bao_cao(data)

    with st.container(border=True):
        c0, c1, c2, c3, c4, c5 = st.columns(
            [0.95, 1.25, 1.75, 1.05, 1.15, 1.05],
            gap="small",
        )

        with c0:
            with st.popover("📤 Tải Master Excel V7", use_container_width=True):
                uploaded = st.file_uploader(
                    "Chọn file Excel",
                    type=["xlsx"],
                    label_visibility="collapsed",
                    key="upload_v7_exact",
                )
                st.download_button(
                    "⬇ Tải Master mẫu",
                    FILE_MASTER.read_bytes(),
                    FILE_MASTER.name,
                    use_container_width=True,
                )

        with c1:
            brand_choice = st.selectbox(
                "Thương hiệu",
                ["Tất cả thương hiệu", *brands],
                key="brand_v7_exact",
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
        if st.session_state.get("dealer_v7_exact", "Tất cả đại lý") not in dealer_options:
            st.session_state["dealer_v7_exact"] = "Tất cả đại lý"

        with c2:
            dealer_choice = st.selectbox(
                "Đại lý",
                dealer_options,
                key="dealer_v7_exact",
            )

        with c3:
            scenario_vi = st.selectbox(
                "Kịch bản",
                ["Cơ sở", "Tích cực", "Bất lợi"],
                key="scenario_v7_exact",
            )

        with c4:
            reporting_period = st.selectbox(
                "Kỳ báo cáo",
                periods,
                index=len(periods) - 1,
                key="period_v7_exact",
            )

        with c5:
            view_mode = st.selectbox(
                "Chế độ xem",
                ["Tổng quan", "Theo lựa chọn"],
                key="view_v7_exact",
            )

    selected_dealers = None if dealer_choice == "Tất cả đại lý" else [dealer_choice]
    filtered = filter_data(data, brands=selected_brands, dealers=selected_dealers)
    scenario_map = {"Cơ sở": "Base", "Tích cực": "Upside", "Bất lợi": "Downside"}
    return filtered, scenario_map[scenario_vi], uploaded, reporting_period, view_mode


try:
    du_lieu_goc = tai_du_lieu()
except Exception as exc:
    st.error(f"Lỗi tải Master: {exc}")
    st.stop()

header_app()
du_lieu_loc, kich_ban, uploaded, ky_bao_cao, che_do_xem = panel_bo_loc(du_lieu_goc)

if uploaded is not None:
    try:
        uploaded_data = tai_du_lieu(uploaded.getvalue())
        dm = uploaded_data.tables["Don_vi"]
        brand = st.session_state.get("brand_v7_exact", "Tất cả thương hiệu")
        dealer = st.session_state.get("dealer_v7_exact", "Tất cả đại lý")
        available_brands = sorted(dm["Thương hiệu"].dropna().unique().tolist())
        brand_filter = available_brands if brand == "Tất cả thương hiệu" else [brand]
        dealer_filter = None if dealer == "Tất cả đại lý" else [dealer]
        du_lieu_loc = filter_data(uploaded_data, brand_filter, dealer_filter)
    except Exception as exc:
        st.error(f"File tải lên không hợp lệ: {exc}")
        st.stop()


MENU = [
    (
        "ĐIỀU HÀNH",
        [
            ("⌂  Tổng quan điều hành", "command_center"),
            ("⌁  Chiến lược & KPI", "strategy"),
        ],
    ),
    (
        "KINH DOANH & TÀI CHÍNH",
        [
            ("⌁  Thương mại & Tăng trưởng", "commercial"),
            ("⌁  Tài chính & Nguồn vốn", "finance"),
            ("⌁  Đại lý 360°", "dealer_360"),
        ],
    ),
    (
        "VẬN HÀNH & KIỂM SOÁT",
        [
            ("⌁  Vận hành & Aftersales", "operations"),
            ("⌁  Rủi ro & Kiểm soát", "risk_governance"),
            ("⌁  Kịch bản & Mô phỏng", "scenario_lab"),
        ],
    ),
    (
        "QUẢN TRỊ DOANH NGHIỆP",
        [
            ("⌁  Con người & ESG", "people_esg"),
            ("⌁  Báo cáo Hội đồng", "board_reporting"),
            ("⌁  Dữ liệu & Chất lượng", "data_quality"),
            ("⌁  Trợ lý điều hành", "copilot"),
        ],
    ),
]

if "module_v7_exact" not in st.session_state:
    st.session_state["module_v7_exact"] = "command_center"

with st.sidebar:
    st.markdown(
        """
        <div style="
            display:flex;
            align-items:center;
            gap:9px;
            padding:6px 7px 10px 7px;
            margin-bottom:3px;
            border-bottom:1px solid #1a3048;
        ">
            <div style="
                display:grid;
                place-items:center;
                width:29px;
                height:29px;
                border-radius:8px;
                background:linear-gradient(145deg,#2563EB,#6D28D9);
                font-size:.88rem;
            ">🚘</div>
            <div>
                <div style="color:#F8FAFC;font-size:.75rem;font-weight:800;line-height:1.15;">
                    EEOS V7
                </div>
                <div style="color:#71839C;font-size:.56rem;line-height:1.2;margin-top:2px;">
                    Trung tâm điều hành
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for group, entries in MENU:
        st.markdown(f'<div class="side-mini-title">{group}</div>', unsafe_allow_html=True)
        for label, module_name in entries:
            active = st.session_state["module_v7_exact"] == module_name
            if st.button(
                label,
                key=f"menu_exact_{module_name}",
                type="primary" if active else "secondary",
                use_container_width=True,
            ):
                st.session_state["module_v7_exact"] = module_name
                st.rerun()

    st.markdown(
        """
        <div class="side-footer">
            <div class="side-status">● Hệ thống hoạt động bình thường</div>
            Dữ liệu giả lập phục vụ trình diễn.
        </div>
        """,
        unsafe_allow_html=True,
    )

try:
    selected_module = st.session_state["module_v7_exact"]
    module = __import__(f"modules.{selected_module}", fromlist=["render"])
    module.render(du_lieu_loc, kich_ban)
except Exception as exc:
    st.error(f"Lỗi tại module: {exc}")
    with st.expander("Chi tiết kỹ thuật"):
        st.exception(exc)
