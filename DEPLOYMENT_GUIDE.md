
# HƯỚNG DẪN ĐƯA HTA-EOS LÊN GITHUB VÀ STREAMLIT

## 1. Tạo GitHub repository

Tên gợi ý:

`hta-enterprise-executive-operating-system`

## 2. Upload package

Tại thư mục dự án:

```bash
git init
git add .
git commit -m "Initial HTA-EOS release"
git branch -M main
git remote add origin https://github.com/<username>/hta-enterprise-executive-operating-system.git
git push -u origin main
```

## 3. Streamlit Community Cloud

- New app
- Repository: repository vừa tạo
- Branch: `main`
- Main file path: `app.py`
- Deploy

## 4. Cập nhật dữ liệu

Chỉ cần thay nội dung trong Master Excel hoặc upload Master Excel mới trên sidebar của ứng dụng.

## 5. Lưu ý bảo mật

Dự án hiện dùng dữ liệu giả định. Không upload dữ liệu nội bộ, dữ liệu khách hàng hoặc dữ liệu tài chính thật lên repository công khai.
