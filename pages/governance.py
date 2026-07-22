
import streamlit as st
from ui import page_header
def render(data,scenario):
    page_header("Audit, Compliance & Action Impact","Governance execution and financial impact")
    a=data.tables["Action_Impact"]
    c=st.columns(4)
    c[0].metric("Expected Impact",f"{a['Expected Impact (bn)'].sum():,.1f} bn")
    c[1].metric("Actual Impact",f"{a['Actual Impact (bn)'].sum():,.1f} bn")
    c[2].metric("Overdue",int((a["Status"]=="Overdue").sum()))
    c[3].metric("At Risk",int((a["Status"]=="At Risk").sum()))
    st.dataframe(a.sort_values(["Status","Due Date"]),use_container_width=True,hide_index=True)
    st.subheader("Audit Findings")
    st.dataframe(data.tables["Audit_Findings"],use_container_width=True,hide_index=True)
    st.subheader("Policy Register")
    st.dataframe(data.tables["Policy_Register"],use_container_width=True,hide_index=True)
