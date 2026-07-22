
import io
import zipfile
import streamlit as st
from model import enterprise_metrics, dealer_health
from ui import tieu_de_trang, hien_thi_bang

def render(data, scenario):
    tieu_de_trang("Báo cáo HĐQT", "Tạo bản tóm tắt điều hành và các phụ lục báo cáo")
    metrics = enterprise_metrics(data)
    map_df = data.tables["Board_Pack_Map"]
    selected = st.multiselect(
        "Chọn các phần của gói báo cáo",
        map_df["Section"].tolist(),
        default=map_df[map_df["Requirement"] == "Mandatory"]["Section"].tolist(),
    )
    hien_thi_bang(map_df[map_df["Section"].isin(selected)])

    summary = f"""# Gói Báo cáo Điều hành HĐQT

Kịch bản: {scenario}

## Tóm tắt điều hành
- Doanh thu: {metrics['revenue']:,.1f} tỷ đồng
- EBITDA: {metrics['ebitda']:,.1f} tỷ đồng
- Biên EBITDA: {metrics['margin']:.1%}
- Tiền mặt thấp nhất dự kiến: {metrics['cash_min']:,.1f} tỷ đồng
- Số đại lý cảnh báo đỏ: {metrics['red_ews']}
- Rò rỉ chiết khấu: {metrics['discount_leakage']:,.2f} tỷ đồng
- Hành động quá hạn: {metrics['overdue_actions']}
- Quyết định đang chờ: {metrics['pending_decisions']}

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
        archive.writestr("00_Tom_tat_Dieu_hanh.md", summary)
        archive.writestr("01_Suc_khoe_Dai_ly.csv", dealer_health(data).to_csv(index=False))
        for section in selected:
            if section in mapping:
                archive.writestr(
                    section.replace(" ", "_") + ".csv",
                    data.tables[mapping[section]].to_csv(index=False),
                )
    st.download_button(
        "Tải gói Báo cáo HĐQT",
        package.getvalue(),
        "EEOS_V7_Bao_cao_HDQT.zip",
        "application/zip",
        use_container_width=True,
    )
