
import streamlit as st
from model import validate_data
from ui import tieu_de_trang, dong_chi_so, hien_thi_bang

def render(data, scenario):
    tieu_de_trang("Chất lượng Dữ liệu", "Kiểm tra dữ liệu, dòng dữ liệu, dữ liệu chủ và danh mục workbook")
    score, issues = validate_data(data)
    dong_chi_so([
        ("Điểm sẵn sàng", f"{score}/100", None),
        ("Lỗi nghiêm trọng", int((issues["Severity"] == "Critical").sum()) if len(issues) else 0, None),
        ("Cảnh báo mức cao", int((issues["Severity"] == "High").sum()) if len(issues) else 0, None),
        ("Số quy tắc kiểm tra", len(data.tables["Validation_Rules"]), None),
    ])
    tabs = st.tabs(["Kết quả","Danh mục quy tắc","Dòng dữ liệu","Dữ liệu chủ","Danh mục Workbook"])
    with tabs[0]:
        if len(issues):
            hien_thi_bang(issues)
        else:
            st.success("Toàn bộ kiểm tra dữ liệu tự động đã đạt yêu cầu.")
    with tabs[1]:
        hien_thi_bang(data.tables["Validation_Rules"])
    with tabs[2]:
        hien_thi_bang(data.tables["Data_Lineage"])
    with tabs[3]:
        hien_thi_bang(data.tables["Don_vi"])
    with tabs[4]:
        inventory = [{"Sheet": name, "Rows": len(df), "Columns": len(df.columns)}
                     for name, df in data.tables.items()]
        hien_thi_bang(__import__("pandas").DataFrame(inventory))
