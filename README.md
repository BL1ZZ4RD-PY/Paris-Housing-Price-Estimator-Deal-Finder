<div align="center">

  # Paris Housing Market Price Estimator & Deal Finder

  **An end-to-end Data Science pipeline to estimate Parisian rents and automatically detect the best market deals.**

  ![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![Playwright](https://img.shields.io/badge/Playwright-Automated-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
  ![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Machine_Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
  ![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
  ![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</div>

---

## Project Overview

Finding a apartment at a fair price in Paris is a major challenge due to high demand and significant price variance.

This project solves this by **automating the complete data lifecycle**:
1. **Real-time Web Scraping** of active rental listings across all Parisian districts.
2. **Data Cleaning & Filtering** to purge price/m² anomalies and outliers.
3. **ML Modeling** to predict fair market rent based on property size and location (Randome Forest Regressor).
4. **Deal Engine Detection** that isolates properties listed with a discount $\ge 15\%$ compared to estimated market value.

---

## 🛠️ Pipeline Architecture

```text
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐     ┌────────────────┐
│   Web Scraping  │ ──► │  Data Preprocess │ ──► │ Machine Learning  │ ──► │  Deal Engine   │
│  (Playwright)   │     │ (Pandas & Regex) │     │  (Random Forest)  │     │  (Export CSV)  │
└─────────────────┘     └──────────────────┘     └───────────────────┘     └────────────────┘
