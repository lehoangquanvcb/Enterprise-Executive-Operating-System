
# V6 Deployment Guide

## Important cleanup

Before copying V6 into an existing repository, remove old project contents, especially:

```text
pages/
modules/
__pycache__/
Enterprise_Executive_Operating_System_Master_V5.xlsx
```

Do not delete the `.git` directory.

Then copy all V6 files into the repository folder.

## Local verification

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Existing repository update

```bash
git add .
git commit -m "Release V6 Consolidated Enterprise Edition"
git push
```

## Streamlit Community Cloud

- Repository: `lehoangquanvcb/Enterprise-Executive-Operating-System`
- Branch: `main`
- Main file path: `app.py`
