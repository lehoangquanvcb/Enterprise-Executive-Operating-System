
from io import BytesIO
import streamlit as st
from config import APP_NAME, APP_SUBTITLE, VERSION, AUTHOR, MASTER_FILE
from model import load_master, prepare
from ui import inject_css
from components.filters import global_filters

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

@st.cache_data(show_spinner=False)
def load_data(file_bytes=None):
    return prepare(load_master(BytesIO(file_bytes) if file_bytes else MASTER_FILE))

with st.sidebar:
    st.title("🚘 EEOS")
    st.caption(f"{VERSION}")
    st.caption(APP_SUBTITLE)
    st.caption(f"Author: {AUTHOR}")
    uploaded = st.file_uploader("Upload Master Excel V6", type=["xlsx"])
    st.download_button(
        "Download Master Excel V6",
        MASTER_FILE.read_bytes(),
        MASTER_FILE.name,
        use_container_width=True,
    )

try:
    raw_data = load_data(uploaded.getvalue() if uploaded else None)
except Exception as exc:
    st.error(f"Workbook loading error: {exc}")
    st.stop()

data, scenario = global_filters(raw_data)

navigation = {
    "Executive Command Center":"command_center",
    "Strategy & Performance":"strategy",
    "Commercial & Growth":"commercial",
    "Finance & Treasury":"finance",
    "Dealer 360°":"dealer_360",
    "Operations & Aftersales":"operations",
    "Risk & Governance":"risk_governance",
    "Scenario Lab":"scenario_lab",
    "People & ESG":"people_esg",
    "Board Reporting":"board_reporting",
    "Data Quality":"data_quality",
    "Executive Copilot":"copilot",
}

with st.sidebar:
    st.markdown('<div class="section-label">Navigation</div>', unsafe_allow_html=True)
    selected = st.radio("Module", list(navigation), label_visibility="collapsed")
    st.caption("All operating and financial figures are synthetic.")

try:
    module = __import__(f"modules.{navigation[selected]}", fromlist=["render"])
    module.render(data, scenario)
except Exception as exc:
    st.error(f"Module error: {exc}")
    with st.expander("Technical details"):
        st.exception(exc)

st.divider()
st.caption("Enterprise simulation · Synthetic demonstration data · Author: Le Hoang Quan")
