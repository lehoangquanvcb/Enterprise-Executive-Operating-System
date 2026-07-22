
# Enterprise Executive Operating System — V5 Full

**Author: Le Hoang Quan**

This release fixes the Streamlit auto-page conflict in V4 by removing the reserved `pages/` directory and using one internal router with modules stored under `modules/`.

## Ready-to-use modules

1. Executive Command Center
2. Strategy & Performance
3. Commercial & Growth
4. Finance & Treasury
5. Dealer 360°
6. Operations & Aftersales
7. Risk & Resilience
8. Governance & Execution
9. What-if Simulator
10. People & ESG
11. Board Pack Generator
12. Data Quality
13. Executive Copilot

Each module contains populated KPI cards, charts, drill-down tables and downloads. The Board Pack Generator exports a ZIP bundle with an executive summary and supporting CSV schedules.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Git

```bash
git init
git branch -M main
git add .
git commit -m "Initial release of Enterprise Executive Operating System"
git remote add origin https://github.com/lehoangquanvcb/Enterprise-Executive-Operating-System.git
git push -u origin main
```

Existing repository:

```bash
git add .
git commit -m "Release V5 Full"
git push
```
