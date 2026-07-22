
import streamlit as st
from model import validate_data
from ui import page_header
def render(data,scenario):
    page_header("Data Validation Center","Automated readiness and integrity checks")
    score,issues=validate_data(data)
    c=st.columns(4)
    c[0].metric("Data Readiness Score",f"{score}/100")
    c[1].metric("Critical Errors",int((issues["Severity"]=="Critical").sum()) if len(issues) else 0)
    c[2].metric("High Warnings",int((issues["Severity"]=="High").sum()) if len(issues) else 0)
    c[3].metric("Rules",len(data.tables["Validation_Rules"]))
    if len(issues):
        st.dataframe(issues,use_container_width=True,hide_index=True)
    else:
        st.success("All automated validation checks passed.")
    st.subheader("Validation Catalogue")
    st.dataframe(data.tables["Validation_Rules"],use_container_width=True,hide_index=True)
    st.subheader("Data Lineage")
    st.dataframe(data.tables["Data_Lineage"],use_container_width=True,hide_index=True)
