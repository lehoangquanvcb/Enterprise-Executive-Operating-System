
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
    "Lead→Order": "Lead→Đơn hàng",
    "Order→Delivery": "Đơn hàng→Giao xe",
    "Lead→Delivery": "Lead→Giao xe",
    "Traffic Light": "Mức cảnh báo KPI",
}

DOI_GIA_TRI = {
    # Board pack
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
    "Command Center": "Trung tâm điều hành",
    "Strategy & KPI": "Chiến lược & KPI",
    "Dealer P&L": "P&L đại lý",
    "13-Week Cash": "Dòng tiền 13 tuần",
    "Commercial Funnel": "Phễu thương mại",
    "Dealer 360": "Đại lý 360°",
    "Risk & EWS": "Rủi ro & Cảnh báo sớm",
    "Chairman Office": "Văn phòng Chủ tịch",
    "Revenue, EBITDA, liquidity, EWS and decisions":
        "Doanh thu, EBITDA, thanh khoản, cảnh báo sớm và quyết định",
    "Strategy map, KPI attainment and key gaps":
        "Bản đồ chiến lược, mức độ hoàn thành KPI và các khoảng cách trọng yếu",
    "Dealer contribution, margin and variance":
        "Đóng góp của đại lý, biên lợi nhuận và phân tích chênh lệch",
    "Cash runway, CCC and inventory release":
        "Khả năng duy trì tiền mặt, chu kỳ tiền mặt và giải phóng tồn kho",
    "Lead conversion, orders and deliveries":
        "Chuyển đổi khách hàng, đơn hàng và giao xe",
    "Health score and value-at-risk dealers":
        "Điểm sức khỏe và các đại lý có giá trị gặp rủi ro",
    "Top risks, audit findings and control breaches":
        "Rủi ro trọng yếu, phát hiện kiểm toán và vi phạm kiểm soát",
    "Project delivery, CAPEX and investment decisions":
        "Tiến độ dự án, CAPEX và quyết định đầu tư",
    "Capability, succession and sustainability":
        "Năng lực, kế nhiệm và phát triển bền vững",
    "Decision backlog and recommended approvals":
        "Các quyết định tồn đọng và đề xuất phê duyệt",
    "Mandatory": "Bắt buộc",
    "Optional": "Tùy chọn",
    "Board": "HĐQT",
    "Board/CFO": "HĐQT/CFO",
    "CEO/COO": "CEO/COO",
    "Audit Committee": "Ủy ban Kiểm toán",
    "Chairman": "Chủ tịch",
    "Chairman/CEO": "Chủ tịch/CEO",

    # Generic status / severity
    "Base": "Cơ sở",
    "Upside": "Tích cực",
    "Downside": "Bất lợi",
    "Green": "Xanh",
    "Amber": "Vàng",
    "Red": "Đỏ",
    "High": "Cao",
    "Medium": "Trung bình",
    "Low": "Thấp",
    "Open": "Đang mở",
    "Closed": "Đã đóng",
    "In Progress": "Đang thực hiện",
    "Not Started": "Chưa bắt đầu",
    "At Risk": "Có rủi ro",
    "Completed": "Hoàn thành",
    "Overdue": "Quá hạn",
    "Compliant": "Tuân thủ",
    "Conditional": "Có điều kiện",
    "Non-compliant": "Không tuân thủ",
    "Renew": "Gia hạn",
    "Renegotiate": "Đàm phán lại",
    "Monitor": "Theo dõi",
    "Exit": "Chấm dứt",
    "Actual": "Thực hiện",
    "Forecast": "Dự báo",
    "Budget": "Kế hoạch",

    # Funnel / lead / governance
    "New": "Mới",
    "Contacted": "Đã liên hệ",
    "Qualified": "Đạt chuẩn",
    "Test Drive": "Lái thử",
    "Negotiation": "Đàm phán",
    "Order": "Đơn hàng",
    "Lost": "Thất bại",
    "Digital": "Kênh số",
    "Walk-in": "Khách trực tiếp",
    "Referral": "Giới thiệu",
    "Corporate/Fleet": "Doanh nghiệp/Đội xe",
    "Event": "Sự kiện",
    "Normal": "Bình thường",
    "Priority": "Ưu tiên",
    "Hot": "Nóng",
    "Delivered": "Đã giao",
    "In Transit": "Đang vận chuyển",
    "Awaiting Registration": "Chờ đăng ký",
    "Ready": "Sẵn sàng",
    "Yes": "Có",
    "No": "Không",
    "Pending": "Đang chờ",
    "Cash": "Tiền mặt",
    "Bank Loan": "Vay ngân hàng",
    "Leasing": "Thuê tài chính",
    "BREACH": "VI PHẠM",
    "OK": "Đạt",

    # Executive brief
    "Liquidity": "Thanh khoản",
    "Inventory": "Tồn kho",
    "Sales Funnel": "Phễu bán hàng",
    "Margin": "Biên lợi nhuận",
    "Customer": "Khách hàng",
    "Governance": "Quản trị",
    "13-week cash headroom falls below management buffer in week 9":
        "Mức đệm tiền mặt 13 tuần giảm dưới ngưỡng quản trị tại tuần 9",
    "Approve temporary inventory cap and weekly cash war-room":
        "Phê duyệt giới hạn tồn kho tạm thời và họp điều hành tiền mặt hàng tuần",
    "Three dealers show composite inventory risk above 80":
        "Ba đại lý có điểm rủi ro tồn kho tổng hợp trên 80",
    "Reallocate stock and activate model-specific campaigns":
        "Tái phân bổ tồn kho và triển khai chiến dịch theo từng mẫu xe",
    "Lead-to-order conversion below target at selected EV dealers":
        "Tỷ lệ chuyển đổi lead sang đơn hàng dưới mục tiêu tại một số đại lý xe điện",
    "Launch conversion sprint and coaching by salesperson":
        "Triển khai chương trình tăng tốc chuyển đổi và huấn luyện nhân viên bán hàng",
    "Discount leakage concentrated in 12 transactions":
        "Rò rỉ chiết khấu tập trung tại 12 giao dịch",
    "Review delegation and block discounts beyond approval threshold":
        "Rà soát phân quyền và chặn chiết khấu vượt ngưỡng phê duyệt",
    "Delivery delays correlate with lower CSI":
        "Giao xe chậm có tương quan với điểm CSI thấp hơn",
    "Escalate registration and logistics bottlenecks":
        "Xử lý ở cấp cao hơn các điểm nghẽn đăng ký và logistics",
    "Open audit findings exceed remediation SLA":
        "Các phát hiện kiểm toán chưa đóng đã vượt thời hạn khắc phục",
    "Assign accountable executives and report weekly":
        "Chỉ định lãnh đạo chịu trách nhiệm và báo cáo hàng tuần",
    "48 hours": "48 giờ",
    "72 hours": "72 giờ",
    "7 days": "7 ngày",
    "14 days": "14 ngày",
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
    [data-testid="stSidebar"] {{background:{MAU['be_mat']};border-right:1px solid {MAU['vien']};}}
    .block-container {{padding-top:.55rem;padding-bottom:2rem;max-width:1720px;}}
    div[data-testid="stMetric"] {{
      background:linear-gradient(145deg,{MAU['be_mat']},{MAU['be_mat_2']});
      border:1px solid {MAU['vien']};border-radius:14px;padding:13px;
      box-shadow:0 5px 18px rgba(0,0,0,.22);
    }}
    div[data-testid="stMetricLabel"] {{color:{MAU['chu_phu']};}}
    div[data-testid="stMetricValue"] {{color:#F8FAFC;}}
    .exec-card {{
      background:{MAU['be_mat']};border:1px solid {MAU['vien']};
      border-left:5px solid {MAU['chinh']};padding:13px 16px;
      border-radius:9px;margin:7px 0;color:{MAU['chu']};
    }}
    .critical {{border-left-color:{MAU['nghiem_trong']};}}
    .warning {{border-left-color:{MAU['canh_bao']};}}
    .positive {{border-left-color:{MAU['tich_cuc']};}}
    .info {{border-left-color:{MAU['thong_tin']};}}
    div[data-testid="stDataFrame"] {{border:1px solid {MAU['vien']};border-radius:10px;}}
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
        f'<div class="exec-card {muc_do}"><b>{dich_gia_tri(chu_de)}</b> — '
        f'{dich_gia_tri(phat_hien)}<br>'
        f'<b>Khuyến nghị:</b> {dich_gia_tri(khuyen_nghi)} · '
        f'<b>Phụ trách:</b> {dich_gia_tri(phu_trach)} · '
        f'<b>Thời hạn:</b> {dich_gia_tri(thoi_han)}</div>',
        unsafe_allow_html=True,
    )


def dong_chi_so(danh_sach) -> None:
    cot = st.columns(len(danh_sach))
    for c, muc in zip(cot, danh_sach):
        nhan, gia_tri, thay_doi = muc
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
