
import streamlit as st
from model import dealer_health
from ui import tieu_de_trang, hien_thi_bang

def render(data, scenario):
    tieu_de_trang("Trợ lý Điều hành", "Truy vấn dựa trên bằng chứng trong toàn bộ workbook")
    query = st.text_input(
        "Nhập câu hỏi",
        placeholder="Đại lý nào yếu nhất? Tiền mặt đang bị kẹt ở đâu? Vì sao biên lợi nhuận có rủi ro?"
    )
    prompts = ["Đại lý yếu nhất","Áp lực thanh khoản","Rò rỉ chiết khấu",
               "Quyết định của Chủ tịch","Hành động quá hạn","Rủi ro hàng đầu"]
    cols = st.columns(len(prompts))
    for col, prompt in zip(cols, prompts):
        if col.button(prompt, use_container_width=True):
            query = prompt
    if not query:
        return

    q = query.lower()
    health = dealer_health(data)
    if "yếu" in q or "đại lý" in q:
        row = health.iloc[-1]
        st.error(f"Phát hiện: {row['Đại lý']} có điểm sức khỏe thấp nhất, đạt {row['Health Score']:.1f}/100.")
        st.write(
            f"Bằng chứng: Biên EBITDA {row['Biên EBITDA']:.1%}; "
            f"chu kỳ tiền mặt {row['Cash Conversion Cycle']:.1f} ngày; "
            f"chuyển đổi lead {row['Lead→Order']:.1%}; EWS {row['Composite EWS']:.1f}."
        )
        st.write("Khuyến nghị: Phê duyệt kế hoạch phục hồi đại lý trong 30 ngày với mốc theo dõi hàng tuần.")
    elif "tiền" in q or "thanh khoản" in q:
        cash = data.tables["Cash_Flow_13W"]
        row = cash.loc[cash["Tiền cuối kỳ"].idxmin()]
        st.warning(
            f"Phát hiện: Tiền mặt thấp nhất dự kiến là {row['Tiền cuối kỳ']:,.1f} tỷ "
            f"tại tuần {int(row['Tuần'])}; mức đệm còn lại {row['Headroom']:,.1f} tỷ."
        )
        st.write("Khuyến nghị: Hạn chế nhập thêm xe chậm luân chuyển và đẩy nhanh thu hồi công nợ.")
    elif "chiết khấu" in q or "biên" in q:
        pricing = data.tables["Pricing_Discount"]
        st.warning(
            f"Phát hiện: {int((pricing['Cờ kiểm soát'] == 'BREACH').sum())} giao dịch vi phạm "
            f"gây rò rỉ {pricing['Discount leakage (tỷ)'].sum():,.2f} tỷ đồng."
        )
        hien_thi_bang(pricing[pricing["Cờ kiểm soát"] == "BREACH"]
                      .sort_values("Discount leakage (tỷ)", ascending=False).head(20))
    elif "chủ tịch" in q or "quyết định" in q:
        hien_thi_bang(
            data.tables["Quyet_dinh"][
                data.tables["Quyet_dinh"]["Trạng thái"].isin(["Đang xem xét","Chờ quyết định"])
            ]
        )
    elif "quá hạn" in q or "hành động" in q:
        hien_thi_bang(
            data.tables["Action_Impact"][data.tables["Action_Impact"]["Status"] == "Overdue"]
        )
    elif "rủi ro" in q:
        hien_thi_bang(data.tables["Rui_ro"].sort_values("Điểm rủi ro", ascending=False).head(10))
    else:
        st.info("Các chủ đề hỗ trợ: sức khỏe đại lý, thanh khoản, giá/biên lợi nhuận, quyết định, hành động và rủi ro.")
