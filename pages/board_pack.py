
import streamlit as st
from ui import page_header
def render(data,scenario):
    page_header("Board Pack Generator","Generate a structured executive pack")
    sections=data.tables["Board_Pack_Map"]
    selected=st.multiselect("Sections",sections["Section"].tolist(),default=sections[sections["Requirement"]=="Mandatory"]["Section"].tolist())
    st.dataframe(sections[sections["Section"].isin(selected)],use_container_width=True,hide_index=True)
    md=["# Enterprise Executive Board Pack",f"Scenario: {scenario}",""]
    for _,r in sections[sections["Section"].isin(selected)].sort_values("Order").iterrows():
        md += [f"## {r['Section']}",str(r["Contents"]),""] 
    content="\n".join(md).encode("utf-8")
    st.download_button("Download Board Pack Outline",content,"EEOS_Board_Pack.md","text/markdown")
