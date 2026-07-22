
import streamlit as st
from model import validate_data
from ui import *
def render(d,sc):
    page_header("Data Quality & Governance","Readiness score, integrity controls, lineage and master-data inspection")
    score,issues=validate_data(d)
    metric_row([("Readiness",f"{score}/100",None),("Critical",int((issues["Severity"]=="Critical").sum()) if len(issues) else 0,None),
    ("High",int((issues["Severity"]=="High").sum()) if len(issues) else 0,None),("Validation rules",len(d.tables["Validation_Rules"]),None)])
    tabs=st.tabs(["Validation Results","Rule Catalogue","Data Lineage","Master Data","Workbook Inventory"])
    with tabs[0]:
        if len(issues):st.dataframe(issues,use_container_width=True,hide_index=True)
        else:st.success("All automated validation checks passed.")
    with tabs[1]:st.dataframe(d.tables["Validation_Rules"],use_container_width=True,hide_index=True)
    with tabs[2]:st.dataframe(d.tables["Data_Lineage"],use_container_width=True,hide_index=True)
    with tabs[3]:st.dataframe(d.tables["Don_vi"],use_container_width=True,hide_index=True)
    with tabs[4]:
        inv=[{"Sheet":k,"Rows":len(v),"Columns":len(v.columns)} for k,v in d.tables.items()]
        st.dataframe(inv,use_container_width=True,hide_index=True)
