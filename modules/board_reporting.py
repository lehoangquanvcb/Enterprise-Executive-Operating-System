
import io
import zipfile

import streamlit as st

from model import enterprise_metrics, dealer_health
from ui import tieu_de_trang, hien_thi_bang, viet_hoa_bang


BAN_DICH_PHAN = {
    "Executive Summary": "Tóm tắt điều hành",
    "Strategic Performance": "Hiệu quả chiến lược",
    "Financial Performance": "Hiệu quả tài chính",
    "Cash & Working Capital": "Tiền mặt & Vốn lưu động",
    "Commercial Performance": "Hiệu quả thương mại",
    "Dealer Portfolio": "Danh mục đại lý",
    "Risk & Governance": "Rủi ro & Quản trị",
    "Investment & PMO": "Đầu tư & Quản lý dự án",
    "People & ESG": "Con người & ESG",
    "Decisions Required": "Các quyết định cần phê duyệt",
}

BAN_DICH_NGUOC = {value: key for key, value in BAN_DICH_PHAN.items()}


def render(data, scenario):
    tieu_de_trang(
        "Báo cáo HĐQT",
        "Tạo bản tóm tắt điều hành và các phụ lục báo cáo",
    )

    metrics = enterprise_metrics(data)
    map_df = data.tables["Board_Pack_Map"].copy()

    mandatory_original = map_df[
        map_df["Requirement"] == "Mandatory"
    ]["Section"].tolist()

    options_vi = [
        BAN_DICH_PHAN.get(section, section)
        for section in map_df["Section"].tolist()
    ]
    defaults_vi = [
        BAN_DICH_PHAN.get(section, section)
        for section in mandatory_original
    ]

    selected_vi = st.multiselect(
        "Chọn các phần của gói báo cáo",
        options_vi,
        default=defaults_vi,
    )
    selected_original = [
        BAN_DICH_NGUOC.get(section, section)
        for section in selected_vi
    ]

    hien_thi_bang(
        map_df[map_df["Section"].isin(selected_original)]
    )

    scenario_vi = {
        "Base": "Cơ sở",
        "Upside": "Tích cực",
        "Downside": "Bất lợi",
    }.get(scenario, scenario)

    summary = f"""# Gói Báo cáo Điều hành HĐQT

Kịch bản: {scenario_vi}

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
        "Strategic Performance": ("KPI", "02_Hieu_qua_Chien_luoc.csv"),
        "Financial Performance": ("Dealer_PnL", "03_Hieu_qua_Tai_chinh.csv"),
        "Cash & Working Capital": ("Working_Capital", "04_Tien_mat_Von_luu_dong.csv"),
        "Commercial Performance": ("Customer_Funnel", "05_Hieu_qua_Thuong_mai.csv"),
        "Dealer Portfolio": ("Dealer_KPI", "06_Danh_muc_Dai_ly.csv"),
        "Risk & Governance": ("Early_Warning", "07_Rui_ro_Quan_tri.csv"),
        "Investment & PMO": ("Du_an", "08_Dau_tu_Quan_ly_Du_an.csv"),
        "People & ESG": ("Workforce", "09_Con_nguoi_ESG.csv"),
        "Decisions Required": ("Quyet_dinh", "10_Quyet_dinh_Can_phe_duyet.csv"),
    }

    package = io.BytesIO()
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("00_Tom_tat_Dieu_hanh.md", summary)
        archive.writestr(
            "01_Suc_khoe_Dai_ly.csv",
            viet_hoa_bang(dealer_health(data)).to_csv(index=False),
        )

        for section in selected_original:
            if section in mapping:
                sheet_name, output_name = mapping[section]
                archive.writestr(
                    output_name,
                    viet_hoa_bang(data.tables[sheet_name]).to_csv(index=False),
                )

    st.download_button(
        "Tải gói Báo cáo HĐQT",
        package.getvalue(),
        "EEOS_V7_Bao_cao_HDQT.zip",
        "application/zip",
        use_container_width=True,
    )
