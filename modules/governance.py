
import plotly.express as px, streamlit as st
from ui import *
def render(d,sc):
    page_header("Governance, Audit & Execution","Findings, policies, decisions, resolutions and action impact")
    tabs=st.tabs(["Action Impact","Audit","Policies","Chairman Office","Meetings"])
    a=d.tables["Action_Impact"]
    with tabs[0]:
        metric_row([("Expected impact",f"{a['Expected Impact (bn)'].sum():,.1f} bn",None),("Actual impact",f"{a['Actual Impact (bn)'].sum():,.1f} bn",None),
        ("Impact realization",f"{a['Actual Impact (bn)'].sum()/a['Expected Impact (bn)'].sum():.1%}",None),("Overdue",int((a["Status"]=="Overdue").sum()),None)])
        st.plotly_chart(dark_chart(px.scatter(a,x="Expected Impact (bn)",y="Actual Impact (bn)",color="Status",size="Expected Impact (bn)",hover_name="Action"),"Action Value Realization"),use_container_width=True)
        st.dataframe(a.sort_values(["Status","Due Date"]),use_container_width=True,hide_index=True)
    with tabs[1]:
        st.dataframe(d.tables["Audit_Findings"],use_container_width=True,hide_index=True)
    with tabs[2]:
        st.dataframe(d.tables["Policy_Register"],use_container_width=True,hide_index=True)
    with tabs[3]:
        st.dataframe(d.tables["Quyet_dinh"],use_container_width=True,hide_index=True)
        st.dataframe(d.tables["Nghi_quyet"],use_container_width=True,hide_index=True)
    with tabs[4]:
        st.dataframe(d.tables["Lich_hop"],use_container_width=True,hide_index=True)
        st.dataframe(d.tables["Hanh_dong"],use_container_width=True,hide_index=True)
