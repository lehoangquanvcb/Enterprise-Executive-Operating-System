
from __future__ import annotations

import io
import zipfile

import pandas as pd
import streamlit as st

from model import enterprise_metrics, dealer_health
from ui import tieu_de_trang, viet_hoa_bang


SECTION_VI = {
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

SOURCE_VI = {
    "Command Center": "Trung tâm điều hành",
    "Strategy & KPI": "Chiến lược & KPI",
    "Dealer P&L": "P&L đại lý",
    "13-Week Cash": "Dòng tiền 13 tuần",
    "Commercial Funnel": "Phễu thương mại",
    "Dealer 360": "Đại lý 360°",
    "Risk & EWS": "Rủi ro & Cảnh báo sớm",
    "PMO & Investment": "Quản lý dự án & Đầu tư",
    "People / ESG": "Con người / ESG",
    "Chairman Office": "Văn phòng Chủ tịch",
}

CONTENT_VI = {
    "Revenue, EBITDA, liquidity, EWS and decisions":
        "Doanh thu, EBITDA, thanh khoản, cảnh báo sớm và các quyết định",
    "Strategy map, KPI attainment and key gaps":
        "Bản đồ chiến lược, mức độ hoàn thành KPI và các khoảng cách trọng yếu",
    "Dealer contribution, margin and variance":
        "Đóng góp của đại lý, biên lợi nhuận và phân tích chênh lệch",
    "Cash runway, CCC and inventory release":
        "Khả năng duy trì tiền mặt, chu kỳ tiền mặt và giải phóng tồn kho",
    "Lead conversion, orders and deliveries":
        "Chuyển đổi khách hàng, đơn hàng và hoạt động giao xe",
    "Health score and value-at-risk dealers":
        "Điểm sức khỏe và các đại lý có giá trị gặp rủi ro",
    "Top risks, audit findings and control breaches":
        "Rủi ro trọng yếu, phát hiện kiểm toán và vi phạm kiểm soát",
    "Project delivery, CAPEX and investment decisions":
        "Tiến độ dự án, CAPEX và các quyết định đầu tư",
    "Capability, succession and sustainability":
        "Năng lực, kế nhiệm và phát triển bền vững",
    "Decision backlog and recommended approvals":
        "Các quyết định tồn đọng và đề xuất phê duyệt",
}

AUDIENCE_VI = {
    "Chairman/CEO": "Chủ tịch/CEO",
    "Board": "HĐQT",
    "Board/CFO": "HĐQT/CFO",
    "CEO": "CEO",
    "CEO/COO": "CEO/COO",
    "Audit Committee": "Ủy ban Kiểm toán",
    "Chairman": "Chủ tịch",
}

REQUIREMENT_VI = {
    "Mandatory": "Bắt buộc",
    "Optional": "Tùy chọn",
}

REVERSE_SECTION = {value: key for key, value in SECTION_VI.items()}


def _board_map_vietnamese(source: pd.DataFrame) -> pd.DataFrame:
    """Return a fully Vietnamese board-pack table."""
    result = source.copy()
    result["Section"] = result["Section"].map(
        lambda x: SECTION_VI.get(x, x)
    )
    result["Source Module"] = result["Source Module"].map(
        lambda x: SOURCE_VI.get(x, x)
    )
    result["Contents"] = result["Contents"].map(
        lambda x: CONTENT_VI.get(x, x)
    )
    result["Audience"] = result["Audience"].map(
        lambda x: AUDIENCE_VI.get(x, x)
    )
    result["Requirement"] = result["Requirement"].map(
        lambda x: REQUIREMENT_VI.get(x, x)
    )
    return result.rename(
        columns={
            "Order": "Thứ tự",
            "Section": "Phần báo cáo",
            "Source Module": "Module nguồn",
            "Contents": "Nội dung",
            "Audience": "Đối tượng",
            "Requirement": "Yêu cầu",
        }
    )


def render(data, scenario):
    tieu_de_trang(
        "Báo cáo HĐQT",
        "Tạo bản tóm tắt điều hành và các phụ lục báo cáo",
    )

    metrics = enterprise_metrics(data)
    board_map_original = data.tables["Board_Pack_Map"].copy()
    board_map_vi = _board_map_vietnamese(board_map_original)

    mandatory_original = board_map_original.loc[
        board_map_original["Requirement"] == "Mandatory",
        "Section",
    ].tolist()
    default_vi = [
        SECTION_VI.get(section, section)
        for section in mandatory_original
    ]

    selected_vi = st.multiselect(
        "Chọn các phần của gói báo cáo",
        options=board_map_vi["Phần báo cáo"].tolist(),
        default=default_vi,
        placeholder="Chọn các phần báo cáo",
    )

    selected_original = [
        REVERSE_SECTION.get(section_vi, section_vi)
        for section_vi in selected_vi
    ]

    display_table = board_map_vi[
        board_map_vi["Phần báo cáo"].isin(selected_vi)
    ]
    st.dataframe(
        display_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Thứ tự": st.column_config.NumberColumn(
                "Thứ tự",
                format="%d",
                width="small",
            ),
            "Phần báo cáo": st.column_config.TextColumn(
                "Phần báo cáo",
                width="medium",
            ),
            "Module nguồn": st.column_config.TextColumn(
                "Module nguồn",
                width="medium",
            ),
            "Nội dung": st.column_config.TextColumn(
                "Nội dung",
                width="large",
            ),
            "Đối tượng": st.column_config.TextColumn(
                "Đối tượng",
                width="medium",
            ),
            "Yêu cầu": st.column_config.TextColumn(
                "Yêu cầu",
                width="small",
            ),
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

    output_mapping = {
        "Strategic Performance":
            ("KPI", "02_Hieu_qua_Chien_luoc.csv"),
        "Financial Performance":
            ("Dealer_PnL", "03_Hieu_qua_Tai_chinh.csv"),
        "Cash & Working Capital":
            ("Working_Capital", "04_Tien_mat_Von_luu_dong.csv"),
        "Commercial Performance":
            ("Customer_Funnel", "05_Hieu_qua_Thuong_mai.csv"),
        "Dealer Portfolio":
            ("Dealer_KPI", "06_Danh_muc_Dai_ly.csv"),
        "Risk & Governance":
            ("Early_Warning", "07_Rui_ro_Quan_tri.csv"),
        "Investment & PMO":
            ("Du_an", "08_Dau_tu_Quan_ly_Du_an.csv"),
        "People & ESG":
            ("Workforce", "09_Con_nguoi_ESG.csv"),
        "Decisions Required":
            ("Quyet_dinh", "10_Quyet_dinh_Can_phe_duyet.csv"),
    }

    package = io.BytesIO()
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("00_Tom_tat_Dieu_hanh.md", summary)
        archive.writestr(
            "01_Suc_khoe_Dai_ly.csv",
            viet_hoa_bang(dealer_health(data))
            .to_csv(index=False)
            .encode("utf-8-sig"),
        )

        for section_original in selected_original:
            if section_original in output_mapping:
                sheet_name, output_name = output_mapping[section_original]
                archive.writestr(
                    output_name,
                    viet_hoa_bang(data.tables[sheet_name])
                    .to_csv(index=False)
                    .encode("utf-8-sig"),
                )

    st.download_button(
        "Tải gói Báo cáo HĐQT",
        data=package.getvalue(),
        file_name="EEOS_V7_Bao_cao_HDQT.zip",
        mime="application/zip",
        use_container_width=True,
    )
