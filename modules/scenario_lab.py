
import plotly.graph_objects as go
import streamlit as st
from model import scenario_output
from ui import page_header, metric_row, dark_chart

def render(data, scenario):
    page_header("Scenario Lab", "Interactive revenue, EBITDA and cash sensitivity")
    presets = {
        "Base": (0.08, 0.02, 0.00, 0.11, 0.07, 10),
        "Upside": (0.16, 0.035, -0.007, 0.18, 0.06, 20),
        "Downside": (-0.08, -0.01, 0.018, 0.03, 0.10, 0),
    }
    preset = presets[scenario]
    a, b, c = st.columns(3)
    volume = a.slider("Vehicle volume change", -30, 30, int(preset[0]*100)) / 100
    price = b.slider("Price / mix change", -10, 10, int(preset[1]*100)) / 100
    discount = c.slider("Additional discount", -5, 8, int(preset[2]*100)) / 100
    a, b, c = st.columns(3)
    service = a.slider("Aftersales growth", -20, 40, int(preset[3]*100)) / 100
    personnel = b.slider("Personnel cost growth", -10, 25, int(preset[4]*100)) / 100
    inventory = c.slider("Inventory days reduction", 0, 40, preset[5])
    result = scenario_output(data, volume, price, discount, service, personnel, inventory)
    metric_row([
        ("Simulated revenue", f"{result['revenue']:,.1f} bn",
         f"{result['revenue']/result['base_revenue']-1:.1%}"),
        ("Simulated EBITDA", f"{result['ebitda']:,.1f} bn",
         f"{result['ebitda']-result['base_ebitda']:,.1f} bn"),
        ("EBITDA margin", f"{result['margin']:.1%}", None),
        ("Cash released", f"{result['cash_release']:,.1f} bn", None),
    ])
    pnl = data.tables["Dealer_PnL"]
    fig = go.Figure(go.Waterfall(
        x=["Base EBITDA","Volume","Price / Mix","Discount","Aftersales","Personnel","Simulated EBITDA"],
        y=[
            result["base_ebitda"],
            result["base_revenue"] * volume * 0.075,
            result["base_revenue"] * price * 0.68,
            -result["base_revenue"] * discount * 0.80,
            float(pnl["Doanh thu dịch vụ"].sum()) * service * 0.35,
            -float(pnl["Chi phí nhân sự"].sum()) * personnel,
            result["ebitda"],
        ],
        measure=["absolute","relative","relative","relative","relative","relative","total"],
    ))
    st.plotly_chart(dark_chart(fig, "Scenario EBITDA Bridge"), use_container_width=True)
    st.dataframe(
        data.tables["Scenario_Drivers"][data.tables["Scenario_Drivers"]["Scenario"] == scenario],
        use_container_width=True, hide_index=True
    )
    st.info("Synthetic management sensitivity model; not a statutory forecast.")
