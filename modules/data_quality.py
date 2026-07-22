
import streamlit as st
from model import validate_data
from ui import page_header, metric_row

def render(data, scenario):
    page_header("Data Quality", "Validation, lineage, master data and workbook inventory")
    score, issues = validate_data(data)
    metric_row([
        ("Readiness", f"{score}/100", None),
        ("Critical", int((issues["Severity"] == "Critical").sum()) if len(issues) else 0, None),
        ("High", int((issues["Severity"] == "High").sum()) if len(issues) else 0, None),
        ("Validation rules", len(data.tables["Validation_Rules"]), None),
    ])
    tabs = st.tabs(["Results","Rules","Lineage","Master Data","Workbook Inventory"])
    with tabs[0]:
        if len(issues):
            st.dataframe(issues, use_container_width=True, hide_index=True)
        else:
            st.success("All automated validation checks passed.")
    with tabs[1]:
        st.dataframe(data.tables["Validation_Rules"], use_container_width=True, hide_index=True)
    with tabs[2]:
        st.dataframe(data.tables["Data_Lineage"], use_container_width=True, hide_index=True)
    with tabs[3]:
        st.dataframe(data.tables["Don_vi"], use_container_width=True, hide_index=True)
    with tabs[4]:
        inventory = [{"Sheet": name, "Rows": len(df), "Columns": len(df.columns)}
                     for name, df in data.tables.items()]
        st.dataframe(inventory, use_container_width=True, hide_index=True)
