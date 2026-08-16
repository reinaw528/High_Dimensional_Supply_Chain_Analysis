# KPI Definitions

## Inventory Turnover

Business Meaning:
Measures inventory efficiency.

Formula:
COGS / Average Inventory

DAX:

Inventory Turnover =
DIVIDE(
    SUM(inventory_clean[cogs]),
    AVERAGE(inventory_clean[inventory_level])
)

Source Columns:

- cogs
- inventory_level

Forecast Accuracy =
1 - WAPE

DAX:

Forecast Accuracy =
1 -
DIVIDE(
    SUM(inventory_clean[absolute_forecast_error]),
    SUM(inventory_clean[units_sold])
)

Stockout Rate =
DIVIDE(
    COUNTROWS(
        FILTER(
            inventory_clean,
            inventory_clean[stockout_flag] = TRUE()
        )
    ),
    COUNTROWS(inventory_clean)
)