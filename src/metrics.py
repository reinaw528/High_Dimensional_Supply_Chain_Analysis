import pandas as pd
import numpy as np

def generate_metrics(df):

    return {

        "sales": sales_metrics(df),
        "inventory": inventory_metrics(df),
        "supplier": supplier_metrics(df),
        "forecast": forecast_metrics(df),
        "warehouse": warehouse_metrics(df),
        "region": region_metrics(df)
    }

'''def sales_metrics(df):
    metrics = {}
    metrics["total_units_sold"] = df["units_sold"].sum()
    metrics["average_units_sold"] = df["units_sold"].mean()
    metrics["max_units_sold"] = df["units_sold"].max()
    metrics["min_units_sold"] = df["units_sold"].min()
    return metrics'''
def sales_metrics(df):
    """Calculate overall sales and profitability metrics."""

    metrics = {}

    metrics["total_units_sold"] = (
        df["units_sold"].sum()
    )

    metrics["total_revenue"] = (
        df["revenue"].sum()
    )

    metrics["total_cogs"] = (
        df["cogs"].sum()
    )

    metrics["gross_profit"] = (
        df["profit"].sum()
    )

    metrics["gross_margin"] = (
        metrics["gross_profit"]
        / metrics["total_revenue"]
        if metrics["total_revenue"] != 0
        else 0
    )

    metrics["average_units_sold"] = (
        df["units_sold"].mean()
    )

    metrics["max_units_sold"] = (
        df["units_sold"].max()
    )

    metrics["min_units_sold"] = (
        df["units_sold"].min()
    )

    return metrics

'''def inventory_metrics(df):
    metrics = {}
    metrics["inventory_value"] = (df["inventory_level"] * df["unit_cost"]).sum()
    #metrics["average_inventory"] = df["inventory_level"].mean()
    metrics["max_inventory"] = df["inventory_level"].max()
    metrics["min_inventory"] = df["inventory_level"].min()
    metrics["stockout_rate"] = df["stockout_flag"].mean()
    return metrics'''
def inventory_metrics(df):
    """Calculate network-level inventory performance metrics."""

    metrics = {}

    # Daily inventory value across the network
    daily_inventory_value = (
        df.groupby("date")["inventory_value"]
        .sum()
    )

    average_inventory_value = (
        daily_inventory_value.mean()
    )

    ending_inventory_value = (
        daily_inventory_value.iloc[-1]
    )

    metrics["average_inventory_value"] = (
        average_inventory_value
    )

    metrics["ending_inventory_value"] = (
        ending_inventory_value
    )

    # Inventory units
    daily_inventory_units = (
        df.groupby("date")["inventory_level"]
        .sum()
    )

    metrics["average_inventory_units"] = (
        daily_inventory_units.mean()
    )

    metrics["max_inventory"] = (
        df["inventory_level"].max()
    )

    metrics["min_inventory"] = (
        df["inventory_level"].min()
    )

    # Inventory turnover
    total_cogs = df["cogs"].sum()

    metrics["inventory_turnover"] = (
        total_cogs / average_inventory_value
        if average_inventory_value != 0
        else 0
    )

    # Days Inventory Outstanding
    metrics["days_inventory_outstanding"] = (
        365 / metrics["inventory_turnover"]
        if metrics["inventory_turnover"] != 0
        else 0
    )

    # Replenishment risk
    metrics["reorder_risk_rate"] = (
        df["reorder_risk_flag"].mean()
    )

    # Forward-looking stockout risk
    metrics["projected_stockout_risk_rate"] = (
        df["projected_stockout_risk"].mean()
    )

    # Source-system stockout rate
    metrics["source_stockout_rate"] = (
        df["stockout_flag"].mean()
    )

    return metrics

'''def supplier_metrics(df):
    metrics = {}
    metrics["average_lead_time"] = df["supplier_lead_time_days"].mean()
    metrics["max_lead_time"] = df["supplier_lead_time_days"].max()
    metrics["min_lead_time"] = df["supplier_lead_time_days"].min()
    return metrics'''
def supplier_metrics(df):
    """Calculate supplier lead-time performance metrics."""

    lead_time = df["supplier_lead_time_days"]

    metrics = {}

    metrics["average_lead_time"] = (
        lead_time.mean()
    )

    metrics["median_lead_time"] = (
        lead_time.median()
    )

    metrics["lead_time_std"] = (
        lead_time.std()
    )

    metrics["lead_time_p90"] = (
        lead_time.quantile(0.90)
    )

    metrics["max_lead_time"] = (
        lead_time.max()
    )

    metrics["min_lead_time"] = (
        lead_time.min()
    )

    return metrics

'''def forecast_metrics(df):
    metrics = {}
    #metrics["forecast_accuracy"] = df["forecast_accuracy"].mean()
    metrics["forecast_error"] = df["forecast_error"].mean()
    metrics["overforecast_rate"] = (
        (df["forecast_bias"] == "overforecast").mean()
    )
    metrics["underforecast_rate"] = (
        (df["forecast_bias"] == "underforecast").mean()
    )
    return metrics'''
def forecast_metrics(df):
    """Calculate network-level forecast performance metrics."""

    metrics = {}

    total_actual = (
        df["units_sold"].sum()
    )

    total_absolute_error = (
        df["absolute_forecast_error"].sum()
    )

    total_forecast_error = (
        df["forecast_error"].sum()
    )

    # WAPE
    metrics["wape"] = (
        total_absolute_error / total_actual
        if total_actual != 0
        else 0
    )

    # Forecast accuracy derived from WAPE
    metrics["forecast_accuracy"] = (
        1 - metrics["wape"]
    )

    # Forecast bias
    metrics["forecast_bias"] = (
        total_forecast_error / total_actual
        if total_actual != 0
        else 0
    )

    # Directional error
    metrics["overforecast_rate"] = (
        (
            df["forecast_direction"]
            == "overforecast"
        ).mean()
    )

    metrics["underforecast_rate"] = (
        (
            df["forecast_direction"]
            == "underforecast"
        ).mean()
    )

    metrics["accurate_rate"] = (
        (
            df["forecast_direction"]
            == "accurate"
        ).mean()
    )

    return metrics

'''def warehouse_metrics(df):
    return (
        df.groupby("warehouse_id")
        .agg(
            units_sold=("units_sold","sum"),
            inventory=("inventory_level","mean"),
            stockout_rate=("stockout_flag","mean")
        )
    )'''
def warehouse_metrics(df):
    """Calculate warehouse-level operational metrics."""

    daily = (
        df.groupby(
            ["date", "warehouse_id"]
        )
        .agg(
            units_sold=("units_sold", "sum"),
            inventory_units=("inventory_level", "sum"),
            inventory_value=("inventory_value", "sum"),
            cogs=("cogs", "sum"),
            reorder_risk_rate=(
                "reorder_risk_flag",
                "mean"
            ),
            stockout_risk_rate=(
                "projected_stockout_risk",
                "mean"
            )
        )
        .reset_index()
    )

    result = (
        daily.groupby("warehouse_id")
        .agg(
            total_units_sold=(
                "units_sold",
                "sum"
            ),
            average_inventory_units=(
                "inventory_units",
                "mean"
            ),
            average_inventory_value=(
                "inventory_value",
                "mean"
            ),
            total_cogs=(
                "cogs",
                "sum"
            ),
            reorder_risk_rate=(
                "reorder_risk_rate",
                "mean"
            ),
            projected_stockout_risk_rate=(
                "stockout_risk_rate",
                "mean"
            )
        )
        .reset_index()
    )

    result["inventory_turnover"] = (
        result["total_cogs"]
        / result["average_inventory_value"]
    )

    result["days_inventory_outstanding"] = (
        365 / result["inventory_turnover"]
    )

    return result
'''def region_metrics(df):
    return (
        df.groupby("region")
        .agg(
            sales=("units_sold","sum"),
            inventory=("inventory_level","mean")
            #forecast_accuracy=("forecast_accuracy","mean")
        )
    )'''
def region_metrics(df):
    """Calculate region-level operational metrics."""

    daily = (
        df.groupby(["date", "region"])
        .agg(
            units_sold=("units_sold", "sum"),
            inventory_units=("inventory_level", "sum"),
            inventory_value=("inventory_value", "sum"),
            cogs=("cogs", "sum"),
            reorder_risk_rate=(
                "reorder_risk_flag",
                "mean"
            ),
            stockout_risk_rate=(
                "projected_stockout_risk",
                "mean"
            )
        )
        .reset_index()
    )

    result = (
        daily.groupby("region")
        .agg(
            total_units_sold=(
                "units_sold",
                "sum"
            ),
            average_inventory_units=(
                "inventory_units",
                "mean"
            ),
            average_inventory_value=(
                "inventory_value",
                "mean"
            ),
            total_cogs=(
                "cogs",
                "sum"
            ),
            reorder_risk_rate=(
                "reorder_risk_rate",
                "mean"
            ),
            projected_stockout_risk_rate=(
                "stockout_risk_rate",
                "mean"
            )
        )
        .reset_index()
    )

    result["inventory_turnover"] = (
        result["total_cogs"]
        / result["average_inventory_value"]
    )

    result["days_inventory_outstanding"] = (
        365 / result["inventory_turnover"]
    )

    return result