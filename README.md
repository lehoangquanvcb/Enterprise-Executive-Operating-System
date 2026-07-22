
# HTA Enterprise Executive Operating System (HTA-EOS)

**Enterprise portfolio project – Author: Le Hoang Quan**

HTA-EOS là nền tảng điều hành mô phỏng dành cho Chủ tịch HĐQT, Tổng Giám đốc, CFO, COO và Chief of Staff của một hệ thống phân phối ô tô đa thương hiệu.

## Cơ sở thiết kế

Cấu trúc thương hiệu và đơn vị được tham khảo từ trang giới thiệu công khai của Hà Thành Auto:

`https://hathanh-auto.com.vn/gioi-thieu`

Toàn bộ số liệu kinh doanh, tài chính, KPI, dự án, rủi ro và đầu tư trong package là **dữ liệu giả định hợp lý**, không phải dữ liệu thực tế của Hà Thành Auto.

## Các module

1. Executive Cockpit
2. Retail Network / Digital Twin
3. Dealer Performance
4. Vehicle Analytics
5. Aftersales Operations
6. CFO Office
7. Planning & Scenario
8. Chairman Office
9. Enterprise Governance
10. PMO & Investment
11. Executive Meeting Center
12. Executive Copilot
13. Data Quality Center

## Kiến trúc kỹ thuật

- Một Master Excel duy nhất
- Python + Pandas
- Streamlit
- Plotly
- GitHub-ready
- Streamlit Cloud-ready

## Cấu trúc file

```text
app.py
model.py
HTA_Enterprise_Executive_Operating_System_Master.xlsx
requirements.txt
README.md
DEPLOYMENT_GUIDE.md
.streamlit/config.toml
.gitignore
```

## Chạy trên máy

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Triển khai Streamlit Cloud

1. Tạo repository GitHub.
2. Upload toàn bộ file trong package.
3. Chọn `app.py` làm Main file path.
4. Deploy.
5. Không đưa dữ liệu thật hoặc dữ liệu mật lên repository công khai.

## Master Excel

Workbook gồm 22 sheet:

- Cau_hinh
- Don_vi
- Thuong_hieu
- Mau_xe
- Dealer_KPI
- Ban_hang
- Ton_kho
- Dich_vu
- Phu_tung
- Tai_chinh
- Forecast
- Scenario
- KPI
- Du_an
- Rui_ro
- RCM
- Quyet_dinh
- Hanh_dong
- Lich_hop
- Nghi_quyet
- Dau_tu
- Chat_luong_DL

Không đổi tên sheet hoặc tiêu đề cột nếu chưa cập nhật `model.py`.
