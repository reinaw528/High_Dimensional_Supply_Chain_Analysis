# KPI Dictionary

## Overview

This document defines the key performance indicators (KPIs) used in the Supply Chain Analytics Dashboard.

---

## Executive Performance KPIs

| KPI | Formula | Business Meaning |
|------|----------|----------|
| Total Sales | SUM(Sales Amount) | Total revenue generated from customer sales. |
| Total Profit | SUM(Profit) | Total profit earned after costs. |
| Gross Margin | Total Profit / Total Sales | Measures overall profitability. |
| Inventory Value | SUM(Inventory Value) | Total value of inventory currently held. |

---

## Inventory Management KPIs

| KPI | Formula | Business Meaning |
|------|----------|----------|
| Inventory Turnover | Total Units Sold / Average Inventory | Measures how efficiently inventory is sold and replenished. Higher values indicate better inventory utilization. |
| Days of Inventory (DOI) | 365 / Inventory Turnover | Estimates how many days inventory remains in stock before being sold. Lower values are generally preferred. |
| Average Daily Inventory | Average(Inventory Value by Date) | Average inventory held during the analysis period. |
| At-Risk SKU Count | Count of SKUs with Inventory Gap above threshold | Number of products that may face stockout or inventory imbalance risks. |

---

## Demand Forecasting KPIs

| KPI | Formula | Business Meaning |
|------|----------|----------|
| Total Demand | SUM(Actual Demand) | Total customer demand during the analysis period. |
| Forecast Accuracy | 1 - ABS(Forecast - Actual) / Actual | Measures how closely forecasted demand matches actual demand. Higher values indicate better forecasting performance. |
| Forecast Bias | (Forecast - Actual) / Actual | Indicates whether forecasts systematically overestimate or underestimate demand. |
| WAPE | SUM(ABS(Forecast - Actual)) / SUM(Actual) | Weighted Absolute Percentage Error. Measures overall forecast error across all products. |

---

## Supplier Performance KPIs

| KPI | Formula | Business Meaning |
|------|----------|----------|
| Active Suppliers | DISTINCTCOUNT(Supplier ID) | Total number of suppliers participating in the supply chain. |
| Average Lead Time | AVERAGE(Lead Time Days) | Average supplier delivery lead time. Lower values indicate faster supplier response. |
| Average Forecast Accuracy | Average Forecast Accuracy by Supplier | Measures forecasting performance at the supplier level. |
| High Risk Supplier Count | Count of suppliers classified as High Risk | Number of suppliers requiring immediate attention due to performance concerns. |
| Lowest Supplier Accuracy | MIN(Supplier Forecast Accuracy) | Identifies the poorest performing supplier in terms of forecast accuracy. |
| Suppliers Meeting Target | Count of suppliers with Forecast Accuracy ≥ Target | Number of suppliers meeting the defined forecast accuracy benchmark. |

---

## Risk Definitions

| Risk Category | Criteria |
|--------------|----------|
| Low Risk | Lead Time and Forecast Accuracy both meet target thresholds. |
| Medium Risk | Either Lead Time or Forecast Accuracy fails to meet target. |
| High Risk | Both Lead Time and Forecast Accuracy fail to meet target. |

---

## Dashboard Usage

These KPIs are used across four analytical areas:

1. Executive Overview
2. Inventory Analysis
3. Demand & Forecast Analysis
4. Supplier Performance Analysis

The KPI framework supports inventory optimization, forecasting improvement, supplier evaluation, and operational decision-making.