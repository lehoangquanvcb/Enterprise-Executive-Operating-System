
from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from config import MAU

DOI_TEN_COT = {
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
    "Sheet": "Sheet",
}

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
    .section-label {{color:{MAU['chu_phu']};font-size:.77rem;text-transform:uppercase;
      letter-spacing:.12em;margin-top:12px;}}
    .top-panel {{
      background:linear-gradient(145deg,{MAU['be_mat']},{MAU['be_mat_2']});
      border:1px solid {MAU['vien']};border-radius:14px;padding:10px 14px;
      margin:4px 0 14px 0;
    }}
    div[data-testid="stDataFrame"] {{border:1px solid {MAU['vien']};border-radius:10px;}}
    [data-testid="stFileUploaderDropzone"] {{padding:.55rem;}}
    [data-testid="stFileUploaderDropzoneInstructions"] {{display:none;}}
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
        f'<div class="exec-card {muc_do}"><b>{chu_de}</b> — {phat_hien}<br>'
        f'<b>Khuyến nghị:</b> {khuyen_nghi} · <b>Phụ trách:</b> {phu_trach} · '
        f'<b>Thời hạn:</b> {thoi_han}</div>',
        unsafe_allow_html=True,
    )

def dong_chi_so(danh_sach) -> None:
    cot = st.columns(len(danh_sach))
    for c, muc in zip(cot, danh_sach):
        nhan, gia_tri, thay_doi = muc
        c.metric(nhan, gia_tri, thay_doi)

def viet_hoa_bang(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={c: DOI_TEN_COT.get(c, c) for c in df.columns})

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
