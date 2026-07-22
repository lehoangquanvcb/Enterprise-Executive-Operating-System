
import plotly.express as px
import streamlit as st
from model import dynamic_ews
from ui import page_header, metric_row, dark_chart

def render(data, scenario):
    page_header("Risk & Governance", "Early warning, enterprise risk, controls, audit and execution")
    tabs = st.tabs(["Dynamic EWS","Risk Register","Controls","Audit & Policy","Action Impact"])
    with tabs[0]:
        c1, c2, c3, c4 = st.columns(4)
        a = c1.slider("Base risk", 0, 100, 40) / 100
        b = c2.slider("Working capital", 0, 100, 25) / 100
        c = c3.slider("Commercial", 0, 100, 20) / 100
        e = c4.slider("Margin", 0, 100, 15) / 100
        total = a + b + c + e or 1
        ews = dynamic_ews(data, {
            "base": a/total, "working_capital": b/total,
            "commercial": c/total, "margin": e/total
        })
        st.plotly_chart(
            dark_chart(px.bar(ews, x="Dynamic EWS", y="Đại lý", orientation="h",
                              color="Dynamic Level",
                              color_discrete_map={"Green":"#22C55E","Amber":"#F59E0B","Red":"#EF4444"}),
                       "Dynamic Dealer EWS"),
            use_container_width=True
        )
        st.dataframe(ews, use_container_width=True, hide_index=True)
    with tabs[1]:
        risks = data.tables["Rui_ro"]
        st.plotly_chart(
            dark_chart(px.scatter(risks, x="Khả năng", y="Tác động",
                                  size="Điểm rủi ro", color="Trạng thái",
                                  hover_name="Rủi ro"), "Enterprise Risk Map"),
            use_container_width=True
        )
        st.dataframe(risks.sort_values("Điểm rủi ro", ascending=False),
                     use_container_width=True, hide_index=True)
    with tabs[2]:
        st.dataframe(data.tables["RCM"], use_container_width=True, hide_index=True)
    with tabs[3]:
        st.subheader("Audit findings")
        st.dataframe(data.tables["Audit_Findings"], use_container_width=True, hide_index=True)
        st.subheader("Policy register")
        st.dataframe(data.tables["Policy_Register"], use_container_width=True, hide_index=True)
    with tabs[4]:
        action = data.tables["Action_Impact"]
        expected = float(action["Expected Impact (bn)"].sum())
        actual = float(action["Actual Impact (bn)"].sum())
        metric_row([
            ("Expected impact", f"{expected:,.1f} bn", None),
            ("Actual impact", f"{actual:,.1f} bn", None),
            ("Realization", f"{actual/expected:.1%}" if expected else "-", None),
            ("Overdue", int((action["Status"] == "Overdue").sum()), None),
        ])
        st.plotly_chart(
            dark_chart(px.scatter(action, x="Expected Impact (bn)", y="Actual Impact (bn)",
                                  color="Status", size="Expected Impact (bn)",
                                  hover_name="Action"), "Action Value Realization"),
            use_container_width=True
        )
        st.dataframe(action.sort_values(["Status","Due Date"]), use_container_width=True, hide_index=True)
