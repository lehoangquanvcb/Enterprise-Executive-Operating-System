
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

# Bổ sung CSS riêng cho V7:
# - Không cắt tiêu đề.
# - Thu gọn panel điều khiển ngang.
# - Giữ dropdown ở một dòng, không hiển thị hàng loạt chip lựa chọn.
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0.35rem !important;
        max-width: 1720px !important;
    }

    .eeos-banner {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        padding: 8px 4px 12px 4px;
        overflow: visible;
    }

    .eeos-banner-icon {
        font-size: 2rem;
        line-height: 1.15;
        padding-top: 3px;
        flex: 0 0 auto;
    }

    .eeos-banner-copy {
        min-width: 0;
        overflow: visible;
    }

    .eeos-banner-title {
        margin: 0;
        padding: 0;
        color: #F8FAFC;
        font-size: clamp(1.65rem, 2.25vw, 2.55rem);
        font-weight: 800;
        line-height: 1.22;
        letter-spacing: -0.02em;
        white-space: normal;
        overflow: visible;
        text-overflow: clip;
    }

    .eeos-banner-subtitle {
        margin-top: 7px;
        color: #94A3B8;
        font-size: 0.92rem;
        line-height: 1.45;
        white-space: normal;
    }

    .eeos-control-panel {
        background: linear-gradient(145deg, #111827, #172033);
        border: 1px solid #263247;
        border-radius: 14px;
        padding: 10px 14px 4px 14px;
        margin: 2px 0 14px 0;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stFileUploader"] label {
        color: #E5E7EB !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 42px;
        border-radius: 9px;
    }

    div[data-testid="stPopover"] button {
        min-height: 42px;
        border-radius: 9px;
    }


    /* ===== SIDEBAR ĐIỀU HƯỚNG CHUYÊN NGHIỆP ===== */
    section[data-testid="stSidebar"] {
        width: 250px !important;
        min-width: 250px !important;
        background:
            radial-gradient(circle at 20% 0%, rgba(59, 130, 246, 0.10), transparent 36%),
            linear-gradient(180deg, #0F172A 0%, #0B1424 100%) !important;
        border-right: 1px solid #23314A !important;
        box-shadow: 8px 0 24px rgba(0, 0, 0, 0.18);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0.65rem;
    }

    .eeos-sidebar-brand {
        margin: 0 3px 14px 3px;
        padding: 13px 12px;
        border: 1px solid #263247;
        border-radius: 13px;
        background: linear-gradient(145deg, rgba(23, 32, 51, 0.98), rgba(15, 23, 42, 0.98));
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.18);
    }

    .eeos-sidebar-brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .eeos-sidebar-logo {
        display: grid;
        place-items: center;
        width: 35px;
        height: 35px;
        flex: 0 0 35px;
        border-radius: 10px;
        background: linear-gradient(145deg, #2563EB, #6D28D9);
        box-shadow: 0 5px 14px rgba(37, 99, 235, 0.28);
        font-size: 1.05rem;
    }

    .eeos-sidebar-brand-title {
        color: #F8FAFC;
        font-weight: 800;
        font-size: 0.90rem;
        line-height: 1.18;
        letter-spacing: 0.01em;
    }

    .eeos-sidebar-brand-subtitle {
        margin-top: 3px;
        color: #94A3B8;
        font-size: 0.70rem;
        line-height: 1.25;
    }

    .eeos-sidebar-section {
        margin: 4px 11px 7px 11px;
        color: #64748B;
        font-size: 0.66rem;
        font-weight: 750;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    /* Ẩn vòng tròn radio mặc định */
    section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 3px !important;
    }

    /* Mỗi mục menu */
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        display: flex !important;
        align-items: center !important;
        min-height: 42px !important;
        margin: 2px 3px !important;
        padding: 9px 11px !important;
        border: 1px solid transparent !important;
        border-radius: 9px !important;
        background: transparent !important;
        color: #CBD5E1 !important;
        cursor: pointer !important;
        transition:
            background 150ms ease,
            border-color 150ms ease,
            transform 150ms ease,
            color 150ms ease !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label p {
        margin: 0 !important;
        color: inherit !important;
        font-size: 0.82rem !important;
        font-weight: 560 !important;
        line-height: 1.25 !important;
        white-space: normal !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(59, 130, 246, 0.10) !important;
        border-color: rgba(59, 130, 246, 0.18) !important;
        color: #F8FAFC !important;
        transform: translateX(2px);
    }

    /* Mục đang chọn */
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background:
            linear-gradient(90deg, rgba(37, 99, 235, 0.34), rgba(109, 40, 217, 0.30)) !important;
        border-color: rgba(96, 165, 250, 0.23) !important;
        color: #FFFFFF !important;
        box-shadow:
            inset 3px 0 0 #60A5FA,
            0 5px 13px rgba(17, 24, 39, 0.26);
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
        font-weight: 720 !important;
        color: #FFFFFF !important;
    }

    .eeos-sidebar-footer {
        margin: 15px 7px 2px 7px;
        padding: 10px 9px;
        border-top: 1px solid #263247;
        color: #64748B;
        font-size: 0.68rem;
        line-height: 1.45;
    }

    .eeos-sidebar-status {
        display: flex;
        align-items: center;
        gap: 7px;
        margin-bottom: 5px;
        color: #94A3B8;
    }

    .eeos-status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #22C55E;
        box-shadow: 0 0 9px rgba(34, 197, 94, 0.75);
    }

    @media (max-width: 1100px) {
        .eeos-banner-title {
            font-size: 1.75rem;
        }
        .eeos-banner-subtitle {
            font-size: 0.84rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def tai_du_lieu(file_bytes: bytes | None = None):
    """Đọc và chuẩn hóa Master Excel mặc định hoặc file người dùng tải lên."""
    source = BytesIO(file_bytes) if file_bytes else FILE_MASTER
    return prepare(load_master(source))


def danh_sach_ky_bao_cao(data) -> list[str]:
    """Lấy danh sách kỳ báo cáo có trong sheet Forecast."""
    periods = (
        pd.to_datetime(data.tables["Forecast"]["Tháng"], errors="coerce")
        .dropna()
        .dt.strftime("%m/%Y")
        .unique()
        .tolist()
    )
    return sorted(periods) if periods else ["Toàn kỳ"]


def hien_thi_banner() -> None:
    """Banner HTML thay cho markdown heading để tránh mất/cắt chữ."""
    st.markdown(
        f"""
        <div class="eeos-banner">
            <div class="eeos-banner-icon">🚘</div>
            <div class="eeos-banner-copy">
                <div class="eeos-banner-title">{TEN_UNG_DUNG}</div>
                <div class="eeos-banner-subtitle">
                    {PHU_DE} · {PHIEN_BAN} · Tác giả: {TAC_GIA}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bang_dieu_khien_ngang(data):
    """
    Panel điều khiển ngang dạng dropdown gọn:
    - Thương hiệu: một thương hiệu hoặc tất cả.
    - Đại lý: một đại lý hoặc tất cả đại lý thuộc thương hiệu đã chọn.
    - Không hiển thị sẵn hàng loạt chip lựa chọn.
    """
    dealer_master = data.tables["Don_vi"].copy()
    brands = sorted(dealer_master["Thương hiệu"].dropna().unique().tolist())
    periods = danh_sach_ky_bao_cao(data)

    st.markdown('<div class="eeos-control-panel">', unsafe_allow_html=True)
    c0, c1, c2, c3, c4, c5 = st.columns(
        [1.12, 1.35, 1.85, 1.12, 1.20, 1.10],
        gap="small",
    )

    with c0:
        with st.popover("📤 Master Excel V7", use_container_width=True):
            uploaded = st.file_uploader(
                "Tải file Excel",
                type=["xlsx"],
                label_visibility="collapsed",
                key="tai_master_excel_v7",
            )
            st.download_button(
                "⬇️ Tải Master mẫu",
                FILE_MASTER.read_bytes(),
                FILE_MASTER.name,
                use_container_width=True,
            )

    brand_options = ["Tất cả thương hiệu", *brands]
    with c1:
        brand_choice = st.selectbox(
            "Thương hiệu",
            brand_options,
            index=0,
            key="thuong_hieu_dropdown_v7",
        )

    if brand_choice == "Tất cả thương hiệu":
        dealer_frame = dealer_master
        selected_brands = brands
    else:
        dealer_frame = dealer_master[
            dealer_master["Thương hiệu"] == brand_choice
        ]
        selected_brands = [brand_choice]

    dealers = sorted(dealer_frame["Tên đại lý"].dropna().unique().tolist())
    dealer_options = ["Tất cả đại lý", *dealers]

    # Khi đổi thương hiệu, nếu đại lý đang chọn không còn hợp lệ thì tự trả về "Tất cả đại lý".
    current_dealer = st.session_state.get("dai_ly_dropdown_v7", "Tất cả đại lý")
    if current_dealer not in dealer_options:
        st.session_state["dai_ly_dropdown_v7"] = "Tất cả đại lý"

    with c2:
        dealer_choice = st.selectbox(
            "Đại lý",
            dealer_options,
            index=0,
            key="dai_ly_dropdown_v7",
        )

    with c3:
        scenario_vn = st.selectbox(
            "Kịch bản",
            ["Cơ sở", "Tích cực", "Bất lợi"],
            index=0,
            key="kich_ban_dropdown_v7",
        )

    with c4:
        reporting_period = st.selectbox(
            "Kỳ báo cáo",
            periods,
            index=len(periods) - 1,
            key="ky_bao_cao_dropdown_v7",
        )

    with c5:
        view_mode = st.selectbox(
            "Chế độ xem",
            ["Toàn doanh nghiệp", "Theo lựa chọn"],
            index=0,
            key="che_do_xem_dropdown_v7",
        )

    st.markdown("</div>", unsafe_allow_html=True)

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
    return (
        filtered,
        scenario_map[scenario_vn],
        uploaded,
        reporting_period,
        view_mode,
    )


# Tải dữ liệu mặc định.
try:
    du_lieu_goc = tai_du_lieu()
except Exception as exc:
    st.error(f"Lỗi tải file Master mặc định: {exc}")
    st.stop()

hien_thi_banner()

# Hiển thị panel lần đầu để nhận file upload.
du_lieu_loc, kich_ban, uploaded, ky_bao_cao, che_do_xem = bang_dieu_khien_ngang(
    du_lieu_goc
)

# Khi người dùng tải file mới, đọc lại dữ liệu và áp dụng cùng bộ lọc hiện tại.
if uploaded is not None:
    try:
        du_lieu_tai_len = tai_du_lieu(uploaded.getvalue())

        dealer_master = du_lieu_tai_len.tables["Don_vi"]
        selected_brand = st.session_state.get(
            "thuong_hieu_dropdown_v7",
            "Tất cả thương hiệu",
        )
        selected_dealer = st.session_state.get(
            "dai_ly_dropdown_v7",
            "Tất cả đại lý",
        )

        available_brands = sorted(
            dealer_master["Thương hiệu"].dropna().unique().tolist()
        )
        if selected_brand == "Tất cả thương hiệu":
            brand_filter = available_brands
        elif selected_brand in available_brands:
            brand_filter = [selected_brand]
        else:
            brand_filter = available_brands

        if selected_dealer == "Tất cả đại lý":
            dealer_filter = None
        else:
            available_dealers = set(
                dealer_master["Tên đại lý"].dropna().tolist()
            )
            dealer_filter = (
                [selected_dealer]
                if selected_dealer in available_dealers
                else None
            )

        du_lieu_loc = filter_data(
            du_lieu_tai_len,
            brands=brand_filter,
            dealers=dealer_filter,
        )
    except Exception as exc:
        st.error(f"File tải lên không hợp lệ: {exc}")
        st.stop()


dieu_huong = {
    "🏠 Tổng quan Điều hành": "command_center",
    "🎯 Chiến lược & Hiệu quả": "strategy",
    "📈 Thương mại & Tăng trưởng": "commercial",
    "💰 Tài chính & Nguồn vốn": "finance",
    "🏢 Đại lý 360°": "dealer_360",
    "🛠️ Vận hành & Aftersales": "operations",
    "🛡️ Rủi ro & Kiểm soát": "risk_governance",
    "🧪 Phòng thí nghiệm Kịch bản": "scenario_lab",
    "👥 Con người & ESG": "people_esg",
    "📄 Báo cáo HĐQT": "board_reporting",
    "🗂️ Chất lượng Dữ liệu": "data_quality",
    "🤖 Trợ lý Điều hành": "copilot",
}

with st.sidebar:
    st.markdown(
        """
        <div class="eeos-sidebar-brand">
            <div class="eeos-sidebar-brand-row">
                <div class="eeos-sidebar-logo">🚘</div>
                <div>
                    <div class="eeos-sidebar-brand-title">EEOS V7</div>
                    <div class="eeos-sidebar-brand-subtitle">
                        Hệ thống Điều hành Doanh nghiệp
                    </div>
                </div>
            </div>
        </div>
        <div class="eeos-sidebar-section">Trung tâm điều hành</div>
        """,
        unsafe_allow_html=True,
    )

    lua_chon = st.radio(
        "Module",
        list(dieu_huong),
        label_visibility="collapsed",
        key="menu_dieu_huong_v7",
    )

    st.markdown(
        """
        <div class="eeos-sidebar-footer">
            <div class="eeos-sidebar-status">
                <span class="eeos-status-dot"></span>
                <span>Hệ thống hoạt động bình thường</span>
            </div>
            Dữ liệu trong ứng dụng là dữ liệu giả lập phục vụ trình diễn.
        </div>
        """,
        unsafe_allow_html=True,
    )

try:
    module = __import__(
        f"modules.{dieu_huong[lua_chon]}",
        fromlist=["render"],
    )
    module.render(du_lieu_loc, kich_ban)
except Exception as exc:
    st.error(f"Lỗi tại module: {exc}")
    with st.expander("Chi tiết kỹ thuật"):
        st.exception(exc)

st.divider()
st.caption(
    f"Hệ thống Điều hành Doanh nghiệp · {PHIEN_BAN} · Tác giả: {TAC_GIA}"
)
