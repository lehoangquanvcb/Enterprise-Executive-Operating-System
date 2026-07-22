
import io, zipfile, streamlit as st
from model import metrics,dealer_health
from ui import *
def render(d,sc):
    page_header("Board Pack Generator","Download an immediately usable executive reporting bundle")
    m=metrics(d);sections=d.tables["Board_Pack_Map"]
    selected=st.multiselect("Board-pack sections",sections["Section"].tolist(),default=sections[sections["Requirement"]=="Mandatory"]["Section"].tolist())
    st.dataframe(sections[sections["Section"].isin(selected)],use_container_width=True,hide_index=True)
    summary=f"""# Enterprise Executive Board Pack\n\nScenario: {sc}\n\n## Executive Summary\n- Revenue: {m['revenue']:,.1f} bn VND\n- EBITDA: {m['ebitda']:,.1f} bn VND\n- EBITDA margin: {m['margin']:.1%}\n- Minimum projected cash: {m['cash_min']:,.1f} bn VND\n- Red EWS dealers: {m['red_ews']}\n- Discount leakage: {m['discount']:,.2f} bn VND\n\n"""
    for s in selected:summary+=f"## {s}\nSee corresponding CSV in the reporting bundle.\n\n"
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("00_Executive_Summary.md",summary)
        z.writestr("01_Dealer_Health.csv",dealer_health(d).to_csv(index=False))
        maps={"Strategic Performance":"KPI","Financial Performance":"Dealer_PnL","Cash & Working Capital":"Working_Capital",
              "Commercial Performance":"Customer_Funnel","Dealer Portfolio":"Dealer_KPI","Risk & Governance":"Early_Warning",
              "Investment & PMO":"Du_an","People & ESG":"Workforce","Decisions Required":"Quyet_dinh"}
        for s in selected:
            if s in maps:z.writestr(s.replace(" ","_")+".csv",d.tables[maps[s]].to_csv(index=False))
    st.download_button("Download Complete Board Pack Bundle",buf.getvalue(),"EEOS_Board_Pack.zip","application/zip",use_container_width=True)
