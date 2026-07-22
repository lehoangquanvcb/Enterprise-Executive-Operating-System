
import plotly.express as px
import streamlit as st
from model import enterprise_metrics, dealer_health
from ui import page_header, metric_row, executive_card, dark_chart, download_df

def render(data, scenario):
    page_header("Executive Command Center", f"{data.company_name} · {data.reporting_period} · {scenario}")
    m = enterprise_metrics(data)
    metric_row([
        ("Revenue", f"{m['revenue']:,.0f} bn", None),
        ("EBITDA", f"{m['ebitda']:,.1f} bn", f"{m['margin']:.1%}"),
        ("Minimum cash", f"{m['cash_min']:,.1f} bn", None),
        ("Lead→Order", f"{m['lead_conversion']:.1%}", None),
        ("On-time delivery", f"{m['on_time_delivery']:.1%}", None),
        ("Red EWS", m["red_ews"], None),
        ("Discount leakage", f"{m['discount_leakage']:,.2f} bn", None),
        ("Overdue actions", m["overdue_actions"], None),
    ])
    tabs = st.tabs(["Morning Brief","Dealer Portfolio","Liquidity & Margin","Decision Queue"])
    with tabs[0]:
        for _, row in data.tables["Executive_Brief"].sort_values("Ưu tiên").iterrows():
            executive_card(
                row["Chủ đề"], row["Phát hiện"], row["Khuyến nghị điều hành"],
                row["Owner"], row["SLA"], "critical" if row["Mức độ"] == "High" else "warning"
            )
    with tabs[1]:
        h = dealer_health(data)
        left, right = st.columns(2)
        left.plotly_chart(
            dark_chart(px.bar(h.head(12), x="Health Score", y="Đại lý", orientation="h",
                              color="Thương hiệu"), "Dealer Health Ranking"),
            use_container_width=True,
        )
        right.plotly_chart(
            dark_chart(px.scatter(h, x="Cash Conversion Cycle", y="Biên EBITDA",
                                  size="EBITDA", color="Mức cảnh báo", hover_name="Đại lý"),
                       "Value–Liquidity Matrix"),
            use_container_width=True,
        )
        st.dataframe(h, use_container_width=True, hide_index=True)
        download_df(h, "Download Dealer Health", "dealer_health.csv")
    with tabs[2]:
        cash = data.tables["Cash_Flow_13W"]
        pnl = data.tables["Dealer_PnL"]
        left, right = st.columns(2)
        left.plotly_chart(
            dark_chart(px.line(cash, x="Bắt đầu", y=["Tiền cuối kỳ","Mức tiền tối thiểu"],
                               markers=True), "13-Week Cash"),
            use_container_width=True,
        )
        right.plotly_chart(
            dark_chart(px.scatter(pnl, x="Doanh thu xe", y="Biên EBITDA",
                                  size="EBITDA", color="Thương hiệu", hover_name="Đại lý"),
                       "Dealer Margin Portfolio"),
            use_container_width=True,
        )
    with tabs[3]:
        st.subheader("Pending decisions")
        st.dataframe(
            data.tables["Quyet_dinh"].sort_values("Trạng thái"),
            use_container_width=True, hide_index=True
        )
        st.subheader("Actions requiring attention")
        st.dataframe(
            data.tables["Action_Impact"].sort_values(["Status","Due Date"]),
            use_container_width=True, hide_index=True
        )
