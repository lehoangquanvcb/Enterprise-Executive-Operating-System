
# Enterprise Executive Operating System — V6

**Author: Le Hoang Quan**

V6 consolidates the strongest parts of V1–V5 and removes duplicated or unstable elements.

## What was fixed

- Corrected Strategy forecast charts to use the actual workbook columns:
  `Doanh thu hợp nhất`, `EBITDA`, and `Loại dữ liệu`.
- Removed the reserved Streamlit `pages/` directory and retained one router only.
- Consolidated Risk, Audit, Policy, Controls and Action Impact into one governance module.
- Removed repeated action tables from unrelated modules.
- Derived KPI traffic lights from KPI attainment instead of assuming nonexistent status labels.
- Added application-level exception handling so one chart cannot crash the entire app.
- Added `Module_Map` and `App_Config` sheets to the Master Excel.

## V6 modules

1. Executive Command Center
2. Strategy & Performance
3. Commercial & Growth
4. Finance & Treasury
5. Dealer 360°
6. Operations & Aftersales
7. Risk & Governance
8. Scenario Lab
9. People & ESG
10. Board Reporting
11. Data Quality
12. Executive Copilot

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Update the existing GitHub repository

Delete the old extracted project files, copy the full V6 contents into the repository folder, then run:

```bash
git add .
git commit -m "Release V6 Consolidated Enterprise Edition"
git push
```

## New repository workflow

```bash
git init
git branch -M main
git add .
git commit -m "Initial release of Enterprise Executive Operating System"
git remote add origin https://github.com/lehoangquanvcb/Enterprise-Executive-Operating-System.git
git push -u origin main
```

All financial, operating and customer data are synthetic.
