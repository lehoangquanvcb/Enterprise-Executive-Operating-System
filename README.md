
# Hệ thống Điều hành Doanh nghiệp — V7

**Tác giả: Lê Hoàng Quân**

## Nâng cấp trọng yếu của V7

- Việt hóa toàn bộ menu, tiêu đề, tab, nút, thông báo, KPI và phần lớn tên cột hiển thị.
- Sidebar chỉ còn chức năng điều hướng.
- Upload Master Excel, bộ lọc Thương hiệu, Đại lý, Kịch bản, Kỳ báo cáo và Chế độ xem được chuyển lên panel ngang.
- Giữ nguyên dark theme, bộ dữ liệu 47 sheet, Dealer Health Score, Dynamic EWS, Scenario Lab, Board Reporting và Executive Copilot.
- Kế thừa các sửa lỗi của V6:
  - Không sử dụng thư mục `pages/`.
  - Một router duy nhất.
  - Forecast dùng đúng các cột thực tế.
  - KPI Traffic Light được tính tự động.
  - Lỗi của một module không làm toàn bộ app dừng.

## Chạy trên máy

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Cập nhật repository hiện tại

```bash
git add .
git commit -m "Release V7 Vietnamese Horizontal Control Panel"
git push
```

## Tạo repository mới

```bash
git init
git branch -M main
git add .
git commit -m "Initial release of Enterprise Executive Operating System"
git remote add origin https://github.com/lehoangquanvcb/Enterprise-Executive-Operating-System.git
git push -u origin main
```
