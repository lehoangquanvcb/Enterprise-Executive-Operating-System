
import streamlit as st
from model import dealer_health,metrics
from ui import *
def render(d,sc):
    page_header("Executive Copilot","Rule-based evidence engine across the full workbook")
    q=st.text_input("Ask the operating system",placeholder="Which dealer is weakest? Where is cash trapped? Why is margin at risk? What needs Chairman approval?")
    prompts=["Weakest dealer","Liquidity pressure","Discount leakage","Chairman decisions","Overdue actions","Top risks"]
    cols=st.columns(len(prompts))
    for c,p in zip(cols,prompts):
        if c.button(p,use_container_width=True):q=p
    if not q:return
    q=q.lower();h=dealer_health(d);m=metrics(d)
    if "weak" in q or "dealer" in q or "đại lý" in q:
        r=h.iloc[-1];st.error(f"Finding: {r['Đại lý']} has the lowest health score at {r['Health Score']:.1f}/100.")
        st.write(f"Evidence: EBITDA margin {r['Biên EBITDA']:.1%}; CCC {r['Cash Conversion Cycle']:.1f} days; lead conversion {r['Lead→Order']:.1%}; EWS {r['Composite EWS']:.1f}.")
        st.write("Decision: approve a 30-day dealer recovery plan with weekly cash, inventory, pricing and conversion milestones.")
    elif "cash" in q or "liquid" in q:
        cf=d.tables["Cash_Flow_13W"];r=cf.loc[cf["Tiền cuối kỳ"].idxmin()]
        st.warning(f"Finding: minimum projected cash is {r['Tiền cuối kỳ']:,.1f} bn in week {int(r['Tuần'])}, headroom {r['Headroom']:,.1f} bn.")
        st.write("Decision: cap slow-moving inventory orders and prioritize receivable collection.")
    elif "discount" in q or "margin" in q:
        p=d.tables["Pricing_Discount"];st.warning(f"Finding: {int((p['Cờ kiểm soát']=='BREACH').sum())} pricing breaches created {p['Discount leakage (tỷ)'].sum():,.2f} bn leakage.")
        st.dataframe(p[p["Cờ kiểm soát"]=="BREACH"].sort_values("Discount leakage (tỷ)",ascending=False).head(20),use_container_width=True,hide_index=True)
    elif "chairman" in q or "decision" in q:
        st.dataframe(d.tables["Quyet_dinh"][d.tables["Quyet_dinh"]["Trạng thái"].isin(["Đang xem xét","Chờ quyết định"])],use_container_width=True,hide_index=True)
    elif "overdue" in q or "action" in q:
        st.dataframe(d.tables["Action_Impact"][d.tables["Action_Impact"]["Status"]=="Overdue"],use_container_width=True,hide_index=True)
    elif "risk" in q:
        st.dataframe(d.tables["Rui_ro"].sort_values("Điểm rủi ro",ascending=False).head(10),use_container_width=True,hide_index=True)
    else:
        st.info("Supported topics: dealer health, liquidity, pricing/margin, Chairman decisions, overdue actions and top risks.")
