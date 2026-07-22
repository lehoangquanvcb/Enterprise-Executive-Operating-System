
import streamlit as st
from model import dealer_health
from ui import page_header
def render(data,scenario):
    page_header("Executive Copilot","Evidence-based executive answers")
    q=st.text_input("Ask a question",placeholder="Which dealer is destroying value? Where is cash trapped? What needs Chairman escalation?")
    if q:
        ql=q.lower(); h=dealer_health(data)
        if "dealer" in ql or "đại lý" in ql or "value" in ql:
            r=h.iloc[-1]
            st.error(f"Finding: {r['Đại lý']} has the lowest health score ({r['Health Score']:.1f}).")
            st.write(f"Evidence: EBITDA margin {r['Biên EBITDA']:.1%}; cash cycle {r['Cash Conversion Cycle']:.1f} days; conversion {r['Lead→Order']:.1%}; EWS {r['Composite EWS']:.1f}.")
            st.write("Recommendation: freeze slow-moving allocation, launch a 30-day margin and conversion recovery plan, and track weekly cash release.")
        elif "cash" in ql:
            cf=data.tables["Cash_Flow_13W"]; r=cf.loc[cf["Tiền cuối kỳ"].idxmin()]
            st.warning(f"Lowest projected cash is {r['Tiền cuối kỳ']:,.1f} bn in week {int(r['Tuần'])}.")
        elif "chairman" in ql or "decision" in ql:
            st.dataframe(data.tables["Quyet_dinh"][data.tables["Quyet_dinh"]["Trạng thái"].isin(["Đang xem xét","Chờ quyết định"])],use_container_width=True,hide_index=True)
        else:
            st.info("Try asking about dealer value, cash pressure or Chairman decisions.")
