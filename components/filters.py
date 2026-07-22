
import streamlit as st
from model import filter_data

def global_filters(data):
    dealer_master = data.tables["Don_vi"]
    brands = sorted(dealer_master["Thương hiệu"].dropna().unique().tolist())
    selected_brands = st.sidebar.multiselect("Brand", brands, default=brands, key="global_brands_v6")
    available = sorted(
        dealer_master[dealer_master["Thương hiệu"].isin(selected_brands)]["Tên đại lý"]
        .dropna().unique().tolist()
    )
    selected_dealers = st.sidebar.multiselect("Dealer", available, default=available, key="global_dealers_v6")
    scenario = st.sidebar.selectbox("Scenario", ["Base","Upside","Downside"], key="global_scenario_v6")
    return filter_data(data, selected_brands, selected_dealers), scenario
