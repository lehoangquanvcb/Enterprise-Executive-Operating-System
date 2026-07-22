
# Deployment Guide – V4

## Local test

```bash
cd /d E:\Enterprise-Executive-Operating-System
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## First push

```bash
git init
git branch -M main
git add .
git commit -m "Initial release of Enterprise Executive Operating System"
git remote add origin https://github.com/lehoangquanvcb/Enterprise-Executive-Operating-System.git
git push -u origin main
```

## Existing repository update

```bash
git add .
git commit -m "Release V4"
git push
```

## Streamlit Cloud

- Repository: `lehoangquanvcb/Enterprise-Executive-Operating-System`
- Branch: `main`
- Main file path: `app.py`
