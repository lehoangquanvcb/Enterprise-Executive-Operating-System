
import streamlit as st
from model import dealer_health, enterprise_metrics
from ui import page_header

def render(data, scenario):
    page_header("Executive Copilot", "Evidence queries across the operating workbook")
    query = st.text_input(
        "Ask the operating system",
        placeholder="Which dealer is weakest? Where is cash trapped? Why is margin at risk?"
    )
    prompts = ["Weakest dealer","Liquidity pressure","Discount leakage",
               "Chairman decisions","Overdue actions","Top risks"]
    cols = st.columns(len(prompts))
    for col, prompt in zip(cols, prompts):
        if col.button(prompt, use_container_width=True):
            query = prompt
    if not query:
        return

    q = query.lower()
    health = dealer_health(data)
    metrics = enterprise_metrics(data)
    if "weak" in q or "dealer" in q or "đại lý" in q:
        row = health.iloc[-1]
        st.error(f"Finding: {row['Đại lý']} has the lowest health score at {row['Health Score']:.1f}/100.")
        st.write(
            f"Evidence: EBITDA margin {row['Biên EBITDA']:.1%}; "
            f"cash cycle {row['Cash Conversion Cycle']:.1f} days; "
            f"lead conversion {row['Lead→Order']:.1%}; EWS {row['Composite EWS']:.1f}."
        )
        st.write("Recommended decision: approve a 30-day dealer recovery plan with weekly milestones.")
    elif "cash" in q or "liquid" in q:
        cash = data.tables["Cash_Flow_13W"]
        row = cash.loc[cash["Tiền cuối kỳ"].idxmin()]
        st.warning(
            f"Finding: minimum projected cash is {row['Tiền cuối kỳ']:,.1f} bn "
            f"in week {int(row['Tuần'])}; headroom is {row['Headroom']:,.1f} bn."
        )
        st.write("Recommended decision: cap slow-moving inventory orders and accelerate collections.")
    elif "discount" in q or "margin" in q:
        pricing = data.tables["Pricing_Discount"]
        st.warning(
            f"Finding: {int((pricing['Cờ kiểm soát'] == 'BREACH').sum())} pricing breaches "
            f"created {pricing['Discount leakage (tỷ)'].sum():,.2f} bn leakage."
        )
        st.dataframe(
            pricing[pricing["Cờ kiểm soát"] == "BREACH"]
            .sort_values("Discount leakage (tỷ)", ascending=False).head(20),
            use_container_width=True, hide_index=True
        )
    elif "chairman" in q or "decision" in q:
        st.dataframe(
            data.tables["Quyet_dinh"][
                data.tables["Quyet_dinh"]["Trạng thái"].isin(["Đang xem xét","Chờ quyết định"])
            ],
            use_container_width=True, hide_index=True
        )
    elif "overdue" in q or "action" in q:
        st.dataframe(
            data.tables["Action_Impact"][data.tables["Action_Impact"]["Status"] == "Overdue"],
            use_container_width=True, hide_index=True
        )
    elif "risk" in q:
        st.dataframe(
            data.tables["Rui_ro"].sort_values("Điểm rủi ro", ascending=False).head(10),
            use_container_width=True, hide_index=True
        )
    else:
        st.info("Supported topics: dealer health, liquidity, pricing/margin, decisions, actions and risks.")
