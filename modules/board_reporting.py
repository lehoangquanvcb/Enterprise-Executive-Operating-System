
from __future__ import annotations

import io
import zipfile

import streamlit as st

from model import enterprise_metrics, dealer_health
from ui import tieu_de_trang, viet_hoa_bang


OUTPUT_MAPPING = {
    "Hiệu quả chiến lược": ("KPI", "02_Hieu_qua_Chien_luoc.csv"),
    "Hiệu quả tài chính": ("Dealer_PnL", "03_Hieu_qua_Tai_chinh.csv"),
    "Tiền mặt & Vốn lưu động": ("Working_Capital", "04_Tien_mat_Von_luu_dong.csv"),
    "Hiệu quả thương mại": ("Customer_Funnel", "05_Hieu_qua_Thuong_mai.csv"),
    "Danh mục đại lý": ("Dealer_KPI", "06_Danh_muc_Dai_ly.csv"),
    "Rủi ro & Quản trị": ("Early_Warning", "07_Rui_ro_Quan_tri.csv"),
    "Đầu tư & Quản lý dự án": ("Du_an", "08_Dau_tu_Quan_ly_Du_an.csv"),
    "Con người & ESG": ("Workforce", "09_Con_nguoi_ESG.csv"),
    "Các quyết định cần phê duyệt": ("Quyet_dinh", "10_Quyet_dinh_Can_phe_duyet.csv"),
}


def render(data, scenario):
    tieu_de_trang(
        "Báo cáo HĐQT",
        "Tạo bản tóm tắt điều hành và các phụ lục báo cáo",
    )

    metrics = enterprise_metrics(data)
    board_map = data.tables["Board_Pack_Map"].copy()

    mandatory = board_map.loc[
        board_map["Requirement"] == "Bắt buộc",
        "Section",
    ].tolist()

    selected = st.multiselect(
        "Chọn các phần của gói báo cáo",
        options=board_map["Section"].tolist(),
        default=mandatory,
        placeholder="Chọn các phần báo cáo",
    )

    display = board_map[board_map["Section"].isin(selected)].rename(
        columns={
            "Order": "Thứ tự",
            "Section": "Phần báo cáo",
            "Source Module": "Module nguồn",
            "Contents": "Nội dung",
            "Audience": "Đối tượng",
            "Requirement": "Yêu cầu",
        }
    )

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Thứ tự": st.column_config.NumberColumn(format="%d", width="small"),
            "Phần báo cáo": st.column_config.TextColumn(width="medium"),
            "Module nguồn": st.column_config.TextColumn(width="medium"),
            "Nội dung": st.column_config.TextColumn(width="large"),
            "Đối tượng": st.column_config.TextColumn(width="medium"),
            "Yêu cầu": st.column_config.TextColumn(width="small"),
        },
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

    package = io.BytesIO()
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("00_Tom_tat_Dieu_hanh.md", summary.encode("utf-8"))
        archive.writestr(
            "01_Suc_khoe_Dai_ly.csv",
            viet_hoa_bang(dealer_health(data)).to_csv(index=False).encode("utf-8-sig"),
        )

        for section in selected:
            if section in OUTPUT_MAPPING:
                sheet_name, output_name = OUTPUT_MAPPING[section]
                archive.writestr(
                    output_name,
                    viet_hoa_bang(data.tables[sheet_name])
                    .to_csv(index=False)
                    .encode("utf-8-sig"),
                )

    st.download_button(
        "Tải gói Báo cáo HĐQT",
        package.getvalue(),
        "EEOS_V8_Bao_cao_HDQT.zip",
        "application/zip",
        use_container_width=True,
    )
