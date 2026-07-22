
import plotly.express as px
import streamlit as st
from ui import tieu_de_trang, dong_chi_so, bieu_do_toi, hien_thi_bang

def render(data, scenario):
    tieu_de_trang("Vận hành & Aftersales", "Tồn kho, xưởng dịch vụ, phụ tùng, nhà cung cấp và mạng lưới")
    inventory = data.tables["Ton_kho"]
    service = data.tables["Dich_vu"]
    vendor = data.tables["Vendor_Performance"]
    tabs = st.tabs(["Tồn kho","Dịch vụ sau bán hàng","Phụ tùng","Nhà cung cấp","Mạng lưới"])
    with tabs[0]:
        dong_chi_so([
            ("Số xe tồn kho", f"{inventory['Số xe tồn'].sum():,.0f}", None),
            ("Số ngày tồn kho bình quân", f"{inventory['Số ngày tồn kho'].mean():.1f}", None),
            ("Bản ghi trên 90 ngày", int((inventory["Số ngày tồn kho"] > 90).sum()), None),
        ])
        st.plotly_chart(
            bieu_do_toi(px.bar(inventory.sort_values("Số ngày tồn kho"),
                               x="Số ngày tồn kho", y="Đại lý", orientation="h",
                               color="Thương hiệu"), "Số ngày tồn kho"),
            use_container_width=True
        )
        hien_thi_bang(inventory)
    with tabs[1]:
        latest = service[service["Tháng"] == service["Tháng"].max()]
        st.plotly_chart(
            bieu_do_toi(px.scatter(latest, x="Hiệu suất khoang", y="CSI",
                                   size="Doanh thu dịch vụ (tỷ)", color="Thương hiệu",
                                   hover_name="Đại lý"), "Năng suất xưởng dịch vụ"),
            use_container_width=True
        )
        hien_thi_bang(latest)
    with tabs[2]:
        hien_thi_bang(data.tables["Phu_tung"])
    with tabs[3]:
        st.plotly_chart(
            bieu_do_toi(px.scatter(vendor, x="On-time Delivery", y="Quality Score",
                                   size="Spend YTD (tỷ)", color="Compliance",
                                   hover_name="Nhà cung cấp"), "Hiệu quả nhà cung cấp"),
            use_container_width=True
        )
        hien_thi_bang(vendor)
    with tabs[4]:
        hien_thi_bang(data.tables["Don_vi"])
