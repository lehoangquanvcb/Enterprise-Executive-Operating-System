
# Hướng dẫn triển khai V7

## 1. Thay thế phiên bản cũ

Xóa các file dự án cũ nhưng không xóa thư mục `.git`.

Chép toàn bộ nội dung V7 vào thư mục repository.

## 2. Chạy thử

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## 3. Cập nhật GitHub

```bash
git add .
git commit -m "Release V7 Vietnamese Horizontal Control Panel"
git push
```

## 4. Streamlit Community Cloud

- Repository: `lehoangquanvcb/Enterprise-Executive-Operating-System`
- Branch: `main`
- Main file path: `app.py`
