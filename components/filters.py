
import streamlit as st
from model import filter_data
def global_filters(data):
    dm=data.tables["Don_vi"]
    brands=sorted(dm["Thương hiệu"].dropna().unique().tolist())
    selected_brands=st.sidebar.multiselect("Brand",brands,default=brands,key="global_brands")
    dealer_opts=sorted(dm[dm["Thương hiệu"].isin(selected_brands)]["Tên đại lý"].dropna().unique().tolist())
    selected_dealers=st.sidebar.multiselect("Dealer",dealer_opts,default=dealer_opts,key="global_dealers")
    scenario=st.sidebar.selectbox("Scenario",["Base","Upside","Downside"],key="global_scenario")
    return filter_data(data,selected_brands,selected_dealers),scenario
