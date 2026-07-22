
import io
import zipfile
import streamlit as st
from model import enterprise_metrics, dealer_health
from ui import page_header

def render(data, scenario):
    page_header("Board Reporting", "Create an executive summary and supporting reporting schedules")
    metrics = enterprise_metrics(data)
    map_df = data.tables["Board_Pack_Map"]
    selected = st.multiselect(
        "Board-pack sections",
        map_df["Section"].tolist(),
        default=map_df[map_df["Requirement"] == "Mandatory"]["Section"].tolist(),
    )
    st.dataframe(map_df[map_df["Section"].isin(selected)], use_container_width=True, hide_index=True)

    summary = f"""# Enterprise Executive Board Pack

Scenario: {scenario}

## Executive Summary
- Revenue: {metrics['revenue']:,.1f} bn VND
- EBITDA: {metrics['ebitda']:,.1f} bn VND
- EBITDA margin: {metrics['margin']:.1%}
- Minimum projected cash: {metrics['cash_min']:,.1f} bn VND
- Red EWS dealers: {metrics['red_ews']}
- Discount leakage: {metrics['discount_leakage']:,.2f} bn VND
- Overdue actions: {metrics['overdue_actions']}
- Pending decisions: {metrics['pending_decisions']}

"""
    mapping = {
        "Strategic Performance":"KPI",
        "Financial Performance":"Dealer_PnL",
        "Cash & Working Capital":"Working_Capital",
        "Commercial Performance":"Customer_Funnel",
        "Dealer Portfolio":"Dealer_KPI",
        "Risk & Governance":"Early_Warning",
        "Investment & PMO":"Du_an",
        "People & ESG":"Workforce",
        "Decisions Required":"Quyet_dinh",
    }
    package = io.BytesIO()
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("00_Executive_Summary.md", summary)
        archive.writestr("01_Dealer_Health.csv", dealer_health(data).to_csv(index=False))
        for section in selected:
            summary += f"## {section}\nSee supporting schedule in the reporting package.\n\n"
            if section in mapping:
                archive.writestr(
                    section.replace(" ", "_") + ".csv",
                    data.tables[mapping[section]].to_csv(index=False),
                )
    st.download_button(
        "Download Board Reporting Bundle",
        package.getvalue(),
        "EEOS_V6_Board_Reporting.zip",
        "application/zip",
        use_container_width=True,
    )
