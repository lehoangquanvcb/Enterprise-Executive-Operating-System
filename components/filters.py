
import streamlit as st
from model import filter_tables

def global_filters(data):
    dealers=data.tables["Don_vi"]
    brands=sorted(dealers["Thương hiệu"].dropna().unique())
    selected_brands=st.sidebar.multiselect("Brand",brands,default=brands)
    available=sorted(dealers[dealers["Thương hiệu"].isin(selected_brands)]["Tên đại lý"].dropna().unique())
    selected_dealers=st.sidebar.multiselect("Dealer",available,default=available)
    scenario=st.sidebar.selectbox("Scenario",["Base","Upside","Downside"])
    return filter_tables(data,selected_brands,selected_dealers),scenario
