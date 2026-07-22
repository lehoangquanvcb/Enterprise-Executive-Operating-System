
from io import BytesIO
import streamlit as st
from config import *
from model import load_master,prepare
from ui import inject_css
from components.filters import global_filters

st.set_page_config(page_title=APP_NAME,page_icon="🚘",layout="wide",initial_sidebar_state="expanded")
inject_css()

@st.cache_data(show_spinner=False)
def load_data(b=None):
    return prepare(load_master(BytesIO(b) if b else MASTER_FILE))

with st.sidebar:
    st.title("🚘 EEOS")
    st.caption(f"{VERSION} · {APP_SUBTITLE}")
    st.caption(f"Author: {AUTHOR}")
    up=st.file_uploader("Upload Master Excel",type=["xlsx"])
    st.download_button("Download Master Excel",MASTER_FILE.read_bytes(),MASTER_FILE.name,use_container_width=True)
try:data0=load_data(up.getvalue() if up else None)
except Exception as e:st.error(f"Workbook error: {e}");st.stop()
data,scenario=global_filters(data0)

NAV={
"Executive Command Center":"command_center","Strategy & Performance":"strategy","Commercial & Growth":"commercial",
"Finance & Treasury":"finance","Dealer 360°":"dealer_360","Operations & Aftersales":"operations",
"Risk & Resilience":"risk","Governance & Execution":"governance","What-if Simulator":"what_if",
"People & ESG":"people_esg","Board Pack Generator":"board_pack","Data Quality":"data_quality","Executive Copilot":"copilot"}
with st.sidebar:
    st.markdown('<div class="section-label">Navigation</div>',unsafe_allow_html=True)
    choice=st.radio("Module",list(NAV),label_visibility="collapsed")
    st.caption("Synthetic demonstration data only.")
module=__import__(f"modules.{NAV[choice]}",fromlist=["render"])
module.render(data,scenario)
st.divider();st.caption("Enterprise simulation. All financial, operational and customer values are synthetic.")
