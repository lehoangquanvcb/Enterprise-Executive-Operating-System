
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import MAU


DOI_TEN_COT = {
    "Order": "Thứ tự",
    "Health Score": "Điểm sức khỏe",
    "Dynamic EWS": "Điểm cảnh báo động",
    "Dynamic Level": "Mức cảnh báo động",
    "Financial Risk": "Rủi ro tài chính",
    "Inventory Risk": "Rủi ro tồn kho",
    "Sales Risk": "Rủi ro bán hàng",
    "Customer Risk": "Rủi ro khách hàng",
    "Control Risk": "Rủi ro kiểm soát",
    "Composite EWS": "Điểm EWS tổng hợp",
    "Expected Impact (bn)": "Tác động kỳ vọng (tỷ)",
    "Actual Impact (bn)": "Tác động thực tế (tỷ)",
    "Due Date": "Hạn hoàn thành",
    "Status": "Trạng thái",
    "Confidence": "Mức tin cậy",
    "Evidence": "Bằng chứng",
    "Action": "Hành động",
    "Theme": "Chủ đề",
    "Owner": "Phụ trách",
    "Lead ID": "Mã khách hàng tiềm năng",
    "Order ID": "Mã đơn hàng",
    "Quality Score": "Điểm chất lượng",
    "Compliance": "Tuân thủ",
    "Criticality": "Mức độ trọng yếu",
    "Requirement": "Yêu cầu",
    "Section": "Phần báo cáo",
    "Source Module": "Module nguồn",
    "Contents": "Nội dung",
    "Audience": "Đối tượng",
    "Rule ID": "Mã quy tắc",
    "Domain": "Miền dữ liệu",
    "Field / Object": "Trường / Đối tượng",
    "Rule": "Quy tắc",
    "Severity": "Mức độ",
    "Control Type": "Loại kiểm soát",
    "Rows": "Số dòng",
    "Columns": "Số cột",
    "Sheet": "Trang dữ liệu",
    "Headcount": "Số lượng nhân sự",
    "Engagement": "Điểm gắn kết",
    "Turnover": "Tỷ lệ nghỉ việc",
    "Succession Coverage": "Mức độ bao phủ kế nhiệm",
    "On-time Delivery": "Tỷ lệ giao đúng hạn",
    "Spend YTD (tỷ)": "Chi tiêu lũy kế (tỷ)",
    "Cash Conversion Cycle": "Chu kỳ chuyển đổi tiền mặt",
    "Lead→Order": "Khách hàng tiềm năng→Đơn hàng",
    "Order→Delivery": "Đơn hàng→Giao xe",
    "Lead→Delivery": "Khách hàng tiềm năng→Giao xe",
    "Traffic Light": "Mức cảnh báo KPI",
    "Lead": "Khách hàng tiềm năng",
    "Lost": "Không chuyển đổi",
    "Test drive": "Lái thử",
    "Pipeline": "Cơ hội bán hàng",
}

DOI_GIA_TRI = {
    "High": "Cao", "Medium": "Trung bình", "Low": "Thấp",
    "Green": "Xanh", "Amber": "Vàng", "Red": "Đỏ",
    "Base": "Cơ sở", "Upside": "Tích cực", "Downside": "Bất lợi",
    "Open": "Đang mở", "Closed": "Đã đóng",
    "In Progress": "Đang thực hiện", "Not Started": "Chưa bắt đầu",
    "At Risk": "Có rủi ro", "Completed": "Hoàn thành",
    "Overdue": "Quá hạn", "Mandatory": "Bắt buộc",
    "Optional": "Tùy chọn", "Compliant": "Tuân thủ",
    "Conditional": "Có điều kiện", "Non-compliant": "Không tuân thủ",
    "Renew": "Gia hạn", "Renegotiate": "Đàm phán lại",
    "Monitor": "Theo dõi", "Exit": "Chấm dứt",
    "Actual": "Thực hiện", "Forecast": "Dự báo", "Budget": "Kế hoạch",
    "New": "Mới", "Contacted": "Đã liên hệ", "Qualified": "Đạt chuẩn",
    "Test Drive": "Lái thử", "Negotiation": "Đàm phán",
    "Order": "Đơn hàng", "Lost": "Không chuyển đổi",
    "Digital": "Kênh số", "Walk-in": "Khách trực tiếp",
    "Referral": "Giới thiệu", "Corporate/Fleet": "Doanh nghiệp/Đội xe",
    "Event": "Sự kiện", "Normal": "Bình thường",
    "Priority": "Ưu tiên", "Hot": "Nóng",
    "Delivered": "Đã giao", "In Transit": "Đang vận chuyển",
    "Awaiting Registration": "Chờ đăng ký", "Ready": "Sẵn sàng",
    "Yes": "Có", "No": "Không", "Pending": "Đang chờ",
    "Cash": "Tiền mặt", "Bank Loan": "Vay ngân hàng",
    "Leasing": "Thuê tài chính", "BREACH": "VI PHẠM", "OK": "Đạt",
    "Chairman": "Chủ tịch", "Chairman/CEO": "Chủ tịch/CEO",
    "Board": "HĐQT", "Board/CFO": "HĐQT/CFO",
    "Audit Committee": "Ủy ban Kiểm toán",
}


def dich_gia_tri(value):
    if pd.isna(value):
        return value
    if isinstance(value, str):
        return DOI_GIA_TRI.get(value, value)
    return value


def chen_css() -> None:
    st.markdown(f"""
    <style>
    .stApp {{background:{MAU['nen']};color:{MAU['chu']};}}
    [data-testid="stSidebar"] {{
        background:linear-gradient(180deg,#091729 0%,#071421 100%);
        border-right:1px solid {MAU['vien']};
    }}
    .block-container {{
        padding-top:.35rem;
        padding-bottom:1.5rem;
        max-width:1680px;
    }}
    div[data-testid="stMetric"] {{
        background:linear-gradient(145deg,{MAU['be_mat']},{MAU['be_mat_2']});
        border:1px solid {MAU['vien']};
        border-radius:9px;
        padding:11px 12px;
        box-shadow:none;
    }}
    div[data-testid="stMetricLabel"] {{color:{MAU['chu_phu']};}}
    div[data-testid="stMetricValue"] {{color:#F8FAFC;}}
    div[data-testid="stDataFrame"] {{
        border:1px solid {MAU['vien']};
        border-radius:9px;
    }}
    </style>
    """, unsafe_allow_html=True)


def bieu_do_toi(fig: go.Figure, tieu_de: str | None = None) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=MAU["nen"],
        plot_bgcolor=MAU["be_mat"],
        font=dict(color=MAU["chu"]),
        title=tieu_de,
        legend_title_text="",
        margin=dict(l=20, r=20, t=58, b=20),
    )
    fig.update_xaxes(gridcolor=MAU["vien"], zerolinecolor=MAU["vien"])
    fig.update_yaxes(gridcolor=MAU["vien"], zerolinecolor=MAU["vien"])
    return fig


def tieu_de_trang(tieu_de: str, phu_de: str | None = None) -> None:
    st.title(tieu_de)
    if phu_de:
        st.caption(phu_de)


def the_dieu_hanh(chu_de, phat_hien, khuyen_nghi, phu_trach, thoi_han, muc_do="warning") -> None:
    st.markdown(
        f'<div style="background:#0C192B;border:1px solid #1F3550;'
        f'border-left:4px solid #F59E0B;padding:11px 14px;border-radius:8px;'
        f'margin:7px 0;"><b>{dich_gia_tri(chu_de)}</b> — '
        f'{dich_gia_tri(phat_hien)}<br><b>Khuyến nghị:</b> '
        f'{dich_gia_tri(khuyen_nghi)} · <b>Phụ trách:</b> '
        f'{dich_gia_tri(phu_trach)} · <b>Thời hạn:</b> '
        f'{dich_gia_tri(thoi_han)}</div>',
        unsafe_allow_html=True,
    )


def dong_chi_so(danh_sach) -> None:
    cot = st.columns(len(danh_sach))
    for c, (nhan, gia_tri, thay_doi) in zip(cot, danh_sach):
        c.metric(nhan, gia_tri, thay_doi)


def viet_hoa_bang(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result = result.rename(columns={c: DOI_TEN_COT.get(c, c) for c in result.columns})
    for column in result.columns:
        if result[column].dtype == "object":
            result[column] = result[column].map(dich_gia_tri)
    return result


def hien_thi_bang(df: pd.DataFrame, **kwargs) -> None:
    st.dataframe(viet_hoa_bang(df), use_container_width=True, hide_index=True, **kwargs)


def tai_bang(df, nhan: str, ten_file: str) -> None:
    st.download_button(
        nhan,
        viet_hoa_bang(df).to_csv(index=False).encode("utf-8-sig"),
        ten_file,
        "text/csv",
        use_container_width=True,
    )
