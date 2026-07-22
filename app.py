
from io import BytesIO
import importlib.util
import streamlit as st

from config import APP_NAME,APP_SUBTITLE,AUTHOR,MASTER_FILE
from model import load_master,prepare
from ui import inject_css
from components.filters import global_filters

st.set_page_config(page_title=APP_NAME,page_icon="🚘",layout="wide",initial_sidebar_state="expanded")
inject_css()

@st.cache_data(show_spinner=False)
def load_data(file_bytes=None):
    return prepare(load_master(BytesIO(file_bytes) if file_bytes else MASTER_FILE))

with st.sidebar:
    st.title("🚘 EEOS V4")
    st.caption(APP_SUBTITLE)
    st.caption(f"Author: {AUTHOR}")
    uploaded=st.file_uploader("Upload Master Excel V4",type=["xlsx"])
    st.download_button("Download Master Excel V4",MASTER_FILE.read_bytes(),MASTER_FILE.name,use_container_width=True)

try:
    raw=load_data(uploaded.getvalue() if uploaded else None)
except Exception as exc:
    st.error(f"Unable to load workbook: {exc}")
    st.stop()

data,scenario=global_filters(raw)

PAGE_MAP = {
    "Executive Command Center":"command_center",
    "Strategy & KPI":"strategy",
    "Dealer 360°":"dealer_360",
    "Commercial Funnel":"commercial",
    "Finance & Working Capital":"finance",
    "What-if Simulator":"what_if",
    "Risk & Dynamic EWS":"risk",
    "Audit & Action Impact":"governance",
    "Board Pack Generator":"board_pack",
    "People & ESG":"people_esg",
    "Data Validation Center":"data_quality",
    "Executive Copilot":"copilot",
}
choice=st.sidebar.radio("Navigation",list(PAGE_MAP.keys()))
module=__import__(f"pages.{PAGE_MAP[choice]}",fromlist=["render"])
module.render(data,scenario)

st.divider()
st.caption("All financial, operational, customer and governance data are synthetic and intended for demonstration.")
