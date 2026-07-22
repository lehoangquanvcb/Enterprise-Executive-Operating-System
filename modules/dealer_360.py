
import plotly.express as px
import streamlit as st
from model import dealer_health
from ui import tieu_de_trang, dong_chi_so, the_dieu_hanh, bieu_do_toi, hien_thi_bang

def render(data, scenario):
    tieu_de_trang("Đại lý 360°", "Chẩn đoán và phân tích sâu theo từng đại lý")
    health = dealer_health(data)
    dealer = st.selectbox("Chọn đại lý", health["Đại lý"].tolist())
    row = health[health["Đại lý"] == dealer].iloc[0]
    dong_chi_so([
        ("Điểm sức khỏe", f"{row['Health Score']:.1f}/100", None),
        ("EBITDA", f"{row['EBITDA']:.1f} tỷ", None),
        ("Biên EBITDA", f"{row['Biên EBITDA']:.1%}", None),
        ("DIO", f"{row['DIO']:.1f} ngày", None),
        ("Chu kỳ tiền mặt", f"{row['Cash Conversion Cycle']:.1f} ngày", None),
        ("Lead→Đơn hàng", f"{row['Lead→Order']:.1%}", None),
        ("EWS", f"{row['Composite EWS']:.1f}", None),
    ])
    tabs = st.tabs(["Chẩn đoán","Tài chính","Thương mại","Tồn kho","Aftersales","Khách hàng & Rủi ro"])
    with tabs[0]:
        obs = []
        if row["Biên EBITDA"] < 0.06:
            obs.append(("Biên lợi nhuận", "Biên EBITDA thấp hơn 6%.", "Thực hiện chương trình phục hồi giá, cơ cấu và chi phí."))
        if row["Cash Conversion Cycle"] > 70:
            obs.append(("Thanh khoản", "Chu kỳ chuyển đổi tiền mặt vượt 70 ngày.", "Giảm tồn kho và tăng tốc thu hồi công nợ."))
        if row["Lead→Order"] < 0.10:
            obs.append(("Bán hàng", "Tỷ lệ chuyển đổi lead dưới 10%.", "Triển khai chiến dịch cải thiện chuyển đổi trong 30 ngày."))
        if row["Composite EWS"] >= 60:
            obs.append(("Rủi ro", "Điểm cảnh báo sớm cần được quản lý chú ý.", "Theo dõi kế hoạch khắc phục hàng tuần."))
        if not obs:
            obs.append(("Trạng thái", "Đại lý đang vận hành trong các ngưỡng quản trị cốt lõi.", "Duy trì kiểm soát và rà soát hàng tháng."))
        for topic, finding, action in obs:
            the_dieu_hanh(topic, finding, action, "Giám đốc đại lý / COO", "7 ngày", "warning")
    with tabs[1]:
        hien_thi_bang(data.tables["Dealer_PnL"][data.tables["Dealer_PnL"]["Đại lý"] == dealer])
    with tabs[2]:
        f = data.tables["Customer_Funnel"]
        f = f[f["Đại lý"] == dealer]
        st.plotly_chart(bieu_do_toi(px.line(f, x="Tháng", y=["Lead","Đơn hàng","Giao xe"],
                                           markers=True), "Xu hướng phễu đại lý"),
                        use_container_width=True)
        hien_thi_bang(data.tables["Lead_Pipeline"][data.tables["Lead_Pipeline"]["Đại lý"] == dealer])
    with tabs[3]:
        hien_thi_bang(data.tables["Ton_kho"][data.tables["Ton_kho"]["Đại lý"] == dealer])
        hien_thi_bang(data.tables["Working_Capital"][data.tables["Working_Capital"]["Đại lý"] == dealer])
    with tabs[4]:
        hien_thi_bang(data.tables["Dich_vu"][data.tables["Dich_vu"]["Đại lý"] == dealer])
        hien_thi_bang(data.tables["Phu_tung"][data.tables["Phu_tung"]["Đại lý"] == dealer])
    with tabs[5]:
        hien_thi_bang(data.tables["Order_Delivery"][data.tables["Order_Delivery"]["Đại lý"] == dealer])
        hien_thi_bang(data.tables["Early_Warning"][data.tables["Early_Warning"]["Đại lý"] == dealer])
