
from __future__ import annotations
from pathlib import Path
from io import BytesIO
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from model import load_master_excel, prepare_data, executive_metrics, executive_brief, dealer_health_score

APP_TITLE="HTA Enterprise Executive Operating System"
DEFAULT_FILE=Path(__file__).with_name("HTA_Enterprise_Executive_Operating_System_Master.xlsx")

st.set_page_config(page_title=APP_TITLE,page_icon="🚘",layout="wide",initial_sidebar_state="expanded")
st.markdown("""
<style>
.block-container{padding-top:1rem;padding-bottom:2rem}
div[data-testid="stMetric"]{border:1px solid #dbe5f1;border-radius:12px;padding:12px;background:white}
.exec-card{border-left:5px solid #17365D;background:#f5f8fc;padding:13px 16px;border-radius:7px;margin:8px 0}
.small-note{font-size:.85rem;color:#637083}
</style>
""",unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def get_data(file_bytes):
    source=BytesIO(file_bytes) if file_bytes else DEFAULT_FILE
    return prepare_data(load_master_excel(source))

def fmt(x): return f"{x:,.1f}"
def pct(x): return f"{x:.1%}"

with st.sidebar:
    st.title("🚘 HTA-EOS")
    st.caption("Enterprise Executive Operating System")
    st.caption("Author: Le Hoang Quan")
    uploaded=st.file_uploader("Tải Master Excel",type=["xlsx"])
    st.download_button("Tải Master Excel mẫu",DEFAULT_FILE.read_bytes(),DEFAULT_FILE.name,
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       use_container_width=True)
    st.divider()
    view=st.radio("Chế độ xem",["Chủ tịch HĐQT","Tổng Giám đốc","CFO/FP&A","COO/Vận hành"])
    st.info("Dữ liệu kinh doanh và tài chính là giả định minh họa, không phải số liệu thực tế của Hà Thành Auto.")

try:
    data=get_data(uploaded.getvalue() if uploaded else None)
except Exception as exc:
    st.error(f"Không thể đọc Master Excel: {exc}")
    st.stop()

t=data.tables
m=executive_metrics(data)

st.title(APP_TITLE)
st.caption(f"{data.company_name} · {data.reporting_period} · {view}")

tabs=st.tabs([
    "🏠 Executive Cockpit","🏢 Retail Network","🏆 Dealer Performance","🚙 Vehicle Analytics",
    "🔧 Aftersales","💰 CFO Office","📈 Planning & Scenario","🪑 Chairman Office",
    "🛡️ Governance","🗂️ PMO & Investment","📅 Meeting Center","🧠 Executive Copilot",
    "✅ Data Quality"
])

with tabs[0]:
    c=st.columns(6)
    c[0].metric("Doanh thu hợp nhất",f"{fmt(m['revenue'])} tỷ")
    c[1].metric("Xe bán",f"{m['vehicle_units']:,}")
    c[2].metric("EBITDA",f"{fmt(m['ebitda'])} tỷ",pct(m["ebitda_margin"]))
    c[3].metric("Tồn kho xe",f"{fmt(m['inventory_value'])} tỷ",f"{m['inventory_days']:.0f} ngày")
    c[4].metric("CSI",f"{m['csi']:.1f}/100")
    c[5].metric("Quyết định chờ",m["pending_decisions"])
    for note in executive_brief(data):
        st.markdown(f'<div class="exec-card">{note}</div>',unsafe_allow_html=True)
    left,right=st.columns(2)
    with left:
        dk=t["Dealer_KPI"].groupby("Thương hiệu",as_index=False)[["Doanh thu TH (tỷ)","Doanh thu dịch vụ (tỷ)","EBITDA (tỷ)"]].sum()
        dk["Doanh thu"]=dk["Doanh thu TH (tỷ)"]+dk["Doanh thu dịch vụ (tỷ)"]
        st.plotly_chart(px.bar(dk,x="Thương hiệu",y="Doanh thu",color="Thương hiệu",title="Doanh thu theo thương hiệu"),use_container_width=True)
    with right:
        r=t["Rui_ro"]
        st.plotly_chart(px.scatter(r,x="Xác suất",y="Tác động",size="Điểm rủi ro",color="Mức độ",
                                   hover_name="Mô tả",title="Bản đồ rủi ro doanh nghiệp"),use_container_width=True)

with tabs[1]:
    dealers=t["Don_vi"]
    c1,c2,c3=st.columns(3)
    c1.metric("Đại lý/đơn vị",len(dealers))
    c2.metric("Thương hiệu",dealers["Thương hiệu"].nunique())
    c3.metric("Địa bàn",dealers["Địa bàn"].nunique())
    st.plotly_chart(px.sunburst(dealers,path=["Thương hiệu","Địa bàn","Tên đại lý"],title="Digital Twin mạng lưới bán lẻ"),use_container_width=True)
    st.dataframe(dealers,use_container_width=True,hide_index=True)

with tabs[2]:
    dk=t["Dealer_KPI"].copy()
    dk["Health Score"]=dealer_health_score(dk)
    brand=st.multiselect("Thương hiệu",sorted(dk["Thương hiệu"].unique()),default=sorted(dk["Thương hiệu"].unique()))
    view_df=dk[dk["Thương hiệu"].isin(brand)].sort_values("Health Score",ascending=False)
    st.plotly_chart(px.bar(view_df,x="Health Score",y="Đại lý",orientation="h",color="Thương hiệu",
                           hover_data=["Doanh thu TH (tỷ)","Xe bán","CSI","Biên EBITDA"],title="Xếp hạng sức khỏe đại lý"),
                    use_container_width=True)
    st.dataframe(view_df,use_container_width=True,hide_index=True)

with tabs[3]:
    sales=t["Ban_hang"]
    brand=st.selectbox("Chọn thương hiệu",sorted(sales["Thương hiệu"].unique()))
    s=sales[sales["Thương hiệu"]==brand]
    by_model=s.groupby("Mẫu xe",as_index=False)[["Số xe bán","Doanh thu (tỷ)","Lợi nhuận gộp (tỷ)"]].sum()
    inv=t["Ton_kho"][t["Ton_kho"]["Thương hiệu"]==brand].groupby("Mẫu xe",as_index=False)[["Số xe tồn","Số ngày tồn kho","Xe tồn >90 ngày"]].sum()
    merged=by_model.merge(inv,on="Mẫu xe",how="left")
    st.plotly_chart(px.scatter(merged,x="Số xe bán",y="Số ngày tồn kho",size="Doanh thu (tỷ)",
                               color="Mẫu xe",hover_data=["Số xe tồn","Xe tồn >90 ngày","Lợi nhuận gộp (tỷ)"],
                               title="Ma trận doanh số – tồn kho theo mẫu xe"),use_container_width=True)
    st.dataframe(merged,use_container_width=True,hide_index=True)

with tabs[4]:
    srv=t["Dich_vu"]
    latest=srv[srv["Tháng"]==srv["Tháng"].max()]
    c=st.columns(5)
    c[0].metric("Doanh thu dịch vụ",f"{fmt(latest['Doanh thu dịch vụ (tỷ)'].sum())} tỷ")
    c[1].metric("RO",f"{int(latest['Lệnh sửa chữa'].sum()):,}")
    c[2].metric("Bay Utilization",pct(latest["Hiệu suất khoang"].mean()))
    c[3].metric("Năng suất KTV",f"{latest['Năng suất KTV'].mean():.2f}")
    c[4].metric("Tỷ lệ sửa lại",pct(latest["Tỷ lệ sửa lại"].mean()))
    st.plotly_chart(px.scatter(latest,x="Hiệu suất khoang",y="CSI",size="Doanh thu dịch vụ (tỷ)",
                               color="Thương hiệu",hover_name="Đại lý",title="Hiệu suất xưởng và trải nghiệm khách hàng"),use_container_width=True)
    st.dataframe(latest,use_container_width=True,hide_index=True)

with tabs[5]:
    fin=t["Tai_chinh"]
    c=st.columns(4)
    c[0].metric("Doanh thu xe YTD",f"{fmt(fin['Doanh thu xe TH'].sum())} tỷ")
    c[1].metric("Doanh thu dịch vụ YTD",f"{fmt(fin['Doanh thu dịch vụ TH'].sum())} tỷ")
    c[2].metric("EBITDA YTD",f"{fmt(fin['EBITDA TH'].sum())} tỷ")
    c[3].metric("OCF YTD",f"{fmt(fin['OCF'].sum())} tỷ")
    st.plotly_chart(px.line(fin,x="Tháng",y=["Doanh thu KH","Doanh thu xe TH"],markers=True,title="Doanh thu kế hoạch và thực hiện"),use_container_width=True)
    st.plotly_chart(px.bar(fin,x="Tháng",y=["EBITDA KH","EBITDA TH"],barmode="group",title="EBITDA kế hoạch và thực hiện"),use_container_width=True)

with tabs[6]:
    fc=t["Forecast"]
    st.plotly_chart(px.line(fc,x="Tháng",y=["Doanh thu hợp nhất","EBITDA"],color_discrete_sequence=None,
                            markers=True,title="Rolling Forecast 12 tháng"),use_container_width=True)
    sc=t["Scenario"]
    st.dataframe(sc,use_container_width=True,hide_index=True)
    st.plotly_chart(px.bar(sc,x="Kịch bản",y=["Doanh thu năm","EBITDA năm","OCF dự kiến"],barmode="group",
                           title="So sánh kịch bản"),use_container_width=True)

with tabs[7]:
    c=st.columns(4)
    c[0].metric("Quyết định đang chờ",m["pending_decisions"])
    c[1].metric("Hành động quá hạn",m["overdue_actions"])
    c[2].metric("Rủi ro cao",m["high_risks"])
    c[3].metric("Dự án cần chú ý",m["projects_at_risk"])
    st.subheader("Decision Center")
    st.dataframe(t["Quyet_dinh"],use_container_width=True,hide_index=True)
    st.subheader("Resolution Tracker")
    st.dataframe(t["Nghi_quyet"],use_container_width=True,hide_index=True)
    st.subheader("Executive Action Tracker")
    st.dataframe(t["Hanh_dong"],use_container_width=True,hide_index=True)

with tabs[8]:
    rt,rc=st.tabs(["Enterprise Risk","Risk & Control Matrix"])
    with rt:
        st.dataframe(t["Rui_ro"].sort_values("Điểm rủi ro",ascending=False),use_container_width=True,hide_index=True)
    with rc:
        st.dataframe(t["RCM"],use_container_width=True,hide_index=True)

with tabs[9]:
    p=t["Du_an"]
    st.plotly_chart(px.scatter(p,x="Tiến độ KH",y="Tiến độ TH",size="Ngân sách (tỷ)",color="Trạng thái",
                               hover_name="Tên dự án",title="Ma trận tiến độ dự án"),use_container_width=True)
    st.dataframe(p,use_container_width=True,hide_index=True)
    st.subheader("Investment Office")
    st.dataframe(t["Dau_tu"],use_container_width=True,hide_index=True)

with tabs[10]:
    mt=t["Lich_hop"]
    fig=px.timeline(mt,x_start="Bắt đầu",x_end="Kết thúc",y="Tên cuộc họp",color="Cấp họp",
                    hover_data=["Đơn vị chuẩn bị","Tài liệu","Trạng thái"])
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(mt,use_container_width=True,hide_index=True)

with tabs[11]:
    q=st.text_input("Hỏi hệ thống điều hành",placeholder="Ví dụ: Đại lý nào có hiệu quả thấp nhất?")
    if q:
        ql=q.lower()
        dk=t["Dealer_KPI"].copy(); dk["Health Score"]=dealer_health_score(dk)
        if "đại lý" in ql and ("thấp" in ql or "kém" in ql):
            row=dk.sort_values("Health Score").iloc[0]
            st.success(f"{row['Đại lý']} có Health Score thấp nhất ({row['Health Score']:.1f}/100), "
                       f"hoàn thành doanh thu {row['Tỷ lệ hoàn thành']:.1%}, biên EBITDA {row['Biên EBITDA']:.1%}, CSI {row['CSI']:.1f}.")
        elif "tồn kho" in ql:
            inv=t["Ton_kho"].sort_values("Số ngày tồn kho",ascending=False).head(5)
            st.write("5 mẫu xe/đại lý có số ngày tồn kho cao nhất:")
            st.dataframe(inv[["Đại lý","Thương hiệu","Mẫu xe","Số xe tồn","Số ngày tồn kho","Xe tồn >90 ngày"]],hide_index=True,use_container_width=True)
        elif "ebitda" in ql:
            st.write(f"EBITDA giả định toàn hệ thống là {m['ebitda']:,.1f} tỷ đồng, tương đương biên {m['ebitda_margin']:.1%}.")
        else:
            st.info("Copilot V1 hỗ trợ câu hỏi về đại lý yếu, tồn kho và EBITDA. Các câu hỏi khác sẽ được mở rộng ở phiên bản AI tích hợp.")
    st.subheader("CEO Morning Brief")
    for note in executive_brief(data):
        st.markdown(f'<div class="exec-card">{note}</div>',unsafe_allow_html=True)

with tabs[12]:
    dq=t["Chat_luong_DL"]
    st.dataframe(dq,use_container_width=True,hide_index=True)
    bad=dq[dq["Trạng thái"].isin(["Theo dõi","Cảnh báo"])]
    st.warning(f"Có {len(bad)} kiểm tra chất lượng dữ liệu cần xử lý.")

st.divider()
st.caption("Mô hình minh họa dựa trên cấu trúc công khai của Hà Thành Auto. Toàn bộ số liệu là giả định hợp lý, không phản ánh kết quả thực tế.")
