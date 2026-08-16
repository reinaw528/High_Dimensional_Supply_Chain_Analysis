# High Dimensional Supply Chain Analysis

## Project Overview

This project analyzes end-to-end supply chain operations across suppliers, warehouses, products, and regions using Python, SQL, and Power BI.

The objective is to evaluate inventory health, demand forecasting performance, and supplier reliability while identifying operational risks and improvement opportunities.

The final deliverable is an interactive Power BI dashboard designed to support data-driven decision-making for supply chain managers.

---

## Business Problem

Supply chain organizations often face challenges such as:

- Excess inventory and high carrying costs
- Stockout risks caused by inaccurate forecasting
- Long supplier lead times
- Inventory imbalance across warehouses
- Limited visibility into supplier performance

This project provides a centralized analytics solution to monitor key supply chain KPIs and support inventory optimization decisions.

---

## Business Questions

1. How healthy is the current inventory position?
2. Which warehouses have the highest inventory levels and DOI?
3. Which SKUs are at risk of stockout?
4. How accurate are demand forecasts?
5. Which suppliers present the highest operational risk?
6. Which suppliers meet performance targets?
7. What actions can improve inventory efficiency?

---

## Tools & Technologies

- Python
- Pandas
- NumPy
- SQL
- Power BI
- DAX
- Git
- GitHub

---

## Project Workflow

### Data Cleaning

- Handle missing values
- Remove duplicates
- Standardize data types
- Validate business rules

### Data Profiling

- Missing value analysis
- Duplicate detection
- Outlier identification
- Data quality assessment

### Feature Engineering

Created analytical features including:

- Inventory Gap
- Forecast Error
- Forecast Bias
- Inventory Risk Flag
- Supplier Risk Classification

### KPI Development

Developed KPIs covering:

- Financial Performance
- Inventory Management
- Demand Forecasting
- Supplier Performance

### Dashboard Development

Built interactive Power BI dashboards to support operational analysis and executive reporting.

---

## Key KPIs

### Financial

- Total Sales
- Total Profit
- Gross Margin
- Inventory Value

### Inventory

- Inventory Turnover
- Days of Inventory (DOI)
- Average Daily Inventory
- At-Risk SKU Count

### Forecasting

- Total Demand
- Forecast Accuracy
- Forecast Bias
- WAPE

### Supplier Performance

- Active Suppliers
- Average Lead Time
- Average Forecast Accuracy
- High Risk Supplier Count
- Suppliers Meeting Target

---

## Dashboard Pages

### Executive Overview

High-level summary of supply chain performance.

### Inventory Analysis

Focuses on:

- Inventory trends
- Inventory turnover
- DOI analysis
- Inventory gap monitoring
- At-risk SKU identification

### Demand Forecast Analysis

Focuses on:

- Forecast accuracy
- Forecast bias
- Forecast error
- Demand trends

### Supplier Performance Analysis

Focuses on:

- Lead time performance
- Forecast accuracy by supplier
- Supplier risk assessment
- Supplier action recommendations

---

## Dashboard Screenshots

### Executive Overview

(Add Screenshot Here)

### Inventory Analysis

(Add Screenshot Here)

### Demand Forecast Analysis

(Add Screenshot Here)

### Supplier Performance Analysis

(Add Screenshot Here)

---

## Key Findings

- Inventory turnover remained healthy across warehouses.
- Several SKUs showed significant inventory gaps and require monitoring.
- Forecast accuracy exceeded target levels for most suppliers.
- A small group of suppliers contributed disproportionately to operational risk.
- Warehouse inventory distribution revealed opportunities for inventory optimization.

---

## Repository Structure

```text
High_Dimensional_Supply_Chain_Analysis
│
├── data/
├── notebooks/
├── src/
├── config/
├── docs/
├── dashboard/
├── images/
└── README.md
```

## Future Improvements

- Implement star schema data modeling
- Add a dedicated Date Dimension table
- Automate ETL workflows
- Deploy dashboard to Power BI Service
- Integrate ERP-style operational datasets
- Add OTD (On-Time Delivery) and Service Level metrics

---

## Skills Demonstrated

- Supply Chain Analytics
- Business Analysis
- Inventory Optimization
- Demand Forecasting
- KPI Design
- Power BI Dashboard Development
- Python Data Processing
- SQL Analysis
- Data Quality Management
- Git Version Control
