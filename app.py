
from io import BytesIO
import streamlit as st
from config import TEN_UNG_DUNG, PHU_DE, PHIEN_BAN, TAC_GIA, FILE_MASTER
from model import load_master, prepare
from ui import chen_css
from components.filters import bang_dieu_khien_ngang

st.set_page_config(
    page_title=TEN_UNG_DUNG,
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)
chen_css()

@st.cache_data(show_spinner=False)
def tai_du_lieu(file_bytes=None):
    return prepare(load_master(BytesIO(file_bytes) if file_bytes else FILE_MASTER))

# Load default first so horizontal panel can be shown.
try:
    du_lieu_goc = tai_du_lieu()
except Exception as exc:
    st.error(f"Lỗi tải file Master mặc định: {exc}")
    st.stop()

st.markdown(f"## 🚘 {TEN_UNG_DUNG}")
st.caption(f"{PHU_DE} · {PHIEN_BAN} · Tác giả: {TAC_GIA}")

du_lieu_loc, kich_ban, uploaded, ky_bao_cao, che_do_xem = bang_dieu_khien_ngang(du_lieu_goc)

if uploaded is not None:
    try:
        du_lieu_tai_len = tai_du_lieu(uploaded.getvalue())
        du_lieu_loc, kich_ban, _, ky_bao_cao, che_do_xem = bang_dieu_khien_ngang(du_lieu_tai_len)
    except Exception as exc:
        st.error(f"File tải lên không hợp lệ: {exc}")
        st.stop()

dieu_huong = {
    "🏠 Tổng quan Điều hành":"command_center",
    "🎯 Chiến lược & Hiệu quả":"strategy",
    "📈 Thương mại & Tăng trưởng":"commercial",
    "💰 Tài chính & Nguồn vốn":"finance",
    "🏢 Đại lý 360°":"dealer_360",
    "🛠️ Vận hành & Aftersales":"operations",
    "🛡️ Rủi ro & Kiểm soát":"risk_governance",
    "🧪 Phòng thí nghiệm Kịch bản":"scenario_lab",
    "👥 Con người & ESG":"people_esg",
    "📄 Báo cáo HĐQT":"board_reporting",
    "🗂️ Chất lượng Dữ liệu":"data_quality",
    "🤖 Trợ lý Điều hành":"copilot",
}

with st.sidebar:
    st.markdown("### Điều hướng")
    lua_chon = st.radio("Module", list(dieu_huong), label_visibility="collapsed")
    st.divider()
    st.caption("Dữ liệu tài chính, vận hành và khách hàng đều là dữ liệu giả lập.")

try:
    module = __import__(f"modules.{dieu_huong[lua_chon]}", fromlist=["render"])
    module.render(du_lieu_loc, kich_ban)
except Exception as exc:
    st.error(f"Lỗi tại module: {exc}")
    with st.expander("Chi tiết kỹ thuật"):
        st.exception(exc)

st.divider()
st.caption(f"Hệ thống Điều hành Doanh nghiệp · {PHIEN_BAN} · Tác giả: {TAC_GIA}")
