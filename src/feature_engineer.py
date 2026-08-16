import pandas as pd
import numpy as np


def feature_engineer(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:
    """
    Perform feature engineering on the input DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Clean input DataFrame.

    Returns
    -------
    tuple[pd.DataFrame, dict]
        Feature-engineered DataFrame and feature creation report.
    """

    feature_df = df.copy()
    reports = {}

    feature_df, reports["financial"] = (
        _create_financial_features(feature_df)
    )

    feature_df, reports["inventory"] = (
        _create_inventory_features(feature_df)
    )

    feature_df, reports["time"] = (
        _create_time_features(feature_df)
    )

    feature_df, reports["supplier"] = (
        _create_supplier_features(feature_df)
    )

    feature_df, reports["forecast"] = (
        _create_forecast_features(feature_df)
    )

    return feature_df, reports


def _create_financial_features(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:

    df["revenue"] = (
        df["units_sold"].astype(float)
        * df["unit_price"].astype(float)
    )

    df["cogs"] = (
        df["units_sold"].astype(float)
        * df["unit_cost"].astype(float)
    )

    df["profit"] = (
        df["revenue"]
        - df["cogs"]
    )

    df["profit_margin"] = (
        df["profit"]
        / df["revenue"].replace(0, pd.NA)
    )

    report = {
        "created_features": [
            "revenue",
            "cogs",
            "profit",
            "profit_margin"
        ],
        "formulas": {
            "revenue": "units_sold * unit_price",
            "cogs": "units_sold * unit_cost",
            "profit": "revenue - cogs",
            "profit_margin": "profit / revenue"
        }
    }

    return df, report


def _create_inventory_features(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:

    df["inventory_value"] = (
        df["inventory_level"].astype(float)
        * df["unit_cost"].astype(float)
    )

    df["inventory_gap"] = (
        df["inventory_level"].astype(float)
        - df["reorder_point"].astype(float)
    )

    df["reorder_risk_flag"] = (
        df["inventory_level"].astype(float)
        < df["reorder_point"].astype(float)
    )

    df["days_of_supply"] = (
        df["inventory_level"].astype(float)
        / df["demand_forecast"].replace(0, pd.NA)
    )

    report = {
        "created_features": [
            "inventory_value",
            "inventory_gap",
            "reorder_risk_flag",
            "days_of_supply"
        ],
        "formulas": {
            "inventory_value":
                "inventory_level * unit_cost",
            "inventory_gap":
                "inventory_level - reorder_point",
            "reorder_risk_flag":
                "inventory_level < reorder_point",
            "days_of_supply":
                "inventory_level / demand_forecast"
        },
        "assumptions": {
            "days_of_supply":
                "demand_forecast represents daily demand."
        }
    }

    return df, report


def _create_time_features(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    df["day"] = df["date"].dt.day
    df["quarter"] = df["date"].dt.quarter

    report = {
        "created_features": [
            "year",
            "month",
            "month_name",
            "day",
            "quarter"
        ]
    }

    return df, report


def _create_supplier_features(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:

    bins = [0, 4, 10, float("inf")]
    df["lead_time_category"] = pd.cut(
        df["supplier_lead_time_days"],
        bins=bins,
        labels=["fast", "normal", "slow"],
        include_lowest=True
    )

    df["lead_time_demand"] = (
        df["supplier_lead_time_days"].astype(float)
        * df["demand_forecast"].astype(float)
    )

    df["projected_inventory_after_lead_time"] = (
        df["inventory_level"].astype(float)
        - df["lead_time_demand"]
    )

    df["lead_time_reorder_risk"] = (
        df["projected_inventory_after_lead_time"]
        < df["reorder_point"].astype(float)
    )

    df["projected_stockout_risk"] = (
        df["projected_inventory_after_lead_time"] < 0
    )

    report = {
        "created_features": [
            "lead_time_category",
            "lead_time_demand",
            "projected_inventory_after_lead_time",
            "lead_time_reorder_risk",
            "projected_stockout_risk"
        ],
        "formulas": {
            "lead_time_demand":
                "supplier_lead_time_days * demand_forecast",
            "projected_inventory_after_lead_time":
                "inventory_level - lead_time_demand",
            "lead_time_reorder_risk":
                "projected_inventory_after_lead_time < reorder_point",
            "projected_stockout_risk":
                "projected_inventory_after_lead_time < 0"
        }
    }

    return df, report


def _create_forecast_features(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:

    df["forecast_error"] = (
        df["demand_forecast"].astype(float)- df["units_sold"].astype(float)
    )

    df["absolute_forecast_error"] = (
        df["forecast_error"].abs()
    )

    df["forecast_direction"] = np.select(
        [
            df["forecast_error"] > 0,
            df["forecast_error"] < 0,
            df["forecast_error"] == 0
        ],
        [
            "overforecast",
            "underforecast",
            "accurate"
        ],
        default="unknown"
    )
    df["forecast_accuracy"] = np.where(df["units_sold"] == 0, np.nan, 1 - abs(df["forecast_error"]) / df["units_sold"])
    df["forecast_bias_pct"] = np.where(df["units_sold"] == 0, np.nan, df["forecast_error"] / df["units_sold"])  
    df["forecast_accuracy"] = df["forecast_accuracy"].clip(lower=0, upper=1)
    df["forecast_bias_pct"] = df["forecast_bias_pct"].clip(lower=-1, upper=1)



    report = {
        "created_features": [
            "forecast_error",
            "absolute_forecast_error",
            "forecast_direction",
            "forecast_accuracy",
            "forecast_bias_pct"
        ],
        "formulas": {
            "forecast_error":
                "demand_forecast - units_sold",
            "absolute_forecast_error":
                "abs(forecast_error)",
            "forecast_direction":
                "overforecast / underforecast / accurate",
            "forecast_accuracy":
                "1 - abs(forecast_error) / units_sold",
            "forecast_bias_pct":
                "forecast_error / units_sold"
        }
    }

    return df, report

'''
import numpy as np


def feature_engineer(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Perform feature engineering on the input DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame to be processed.

    Returns:
    pd.DataFrame: DataFrame with engineered features.
    """
    feature_df = df.copy()
    reports = {}

    feature_df, reports["financial"] = (
        _create_financial_features(feature_df)
    )

    feature_df, reports["inventory"] = (
        _create_inventory_features(feature_df)
    )

    feature_df, reports["time"] = (
        _create_time_features(feature_df)
    )

    feature_df, reports["supplier"] = (
        _create_supplier_features(feature_df)
    )

    feature_df, reports["forecast"] = (
        _create_forecast_features(feature_df)
    )

    return feature_df, reports



def _create_financial_features(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:

    financial_report = {}
    
    # Example: Create a new feature 'profit_margin' if 'revenue' and 'cogs' columns exist
    df["revenue"] = df["units_sold"] * df["unit_price"].astype(float)
    df["cogs"] = df["units_sold"] * df["unit_cost"].astype(float)
    df["profit"] = df["revenue"] - df["cogs"]
    df["profit_margin"] = df["profit"] / df["revenue"].replace(0, pd.NA)

    financial_report = {
        "created_features": [
            "revenue", 
            "cogs", 
            "profit", 
            "profit_margin"
        ],

            "formula": {
                "revenue": "units_sold * unit_price",
                "cogs": "units_sold * unit_cost",
                "profit": "revenue - cogs",
                "profit_margin": "profit / revenue"
            }
        }

    return df, financial_report

def _create_inventory_features(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    
    inventory_report = {}
    #df["average_inventory"] =(df["inventory_level"] + df["reorder_point"])/2
    df["forecast_error"] = df["demand_forecast"] - df["units_sold"]
    df["inventory_gap"] = df["inventory_level"]-df["reorder_point"]
    #df["inventory_turnover"] = df["cogs"] / df["average_inventory"].replace(0, pd.NA)
    #df["days_of_inventory"] = df["inventory_level"].astype(float) / df["cogs"].replace(0, pd.NA)
    df["forecasted_error"] = df["demand_forecast"].astype(float)  - df["units_sold"].astype(float)
    df["low_stock_flag"] = (df["inventory_level"]<df["reorder_point"])
    #df["forecast_accuracy"] = (1 -abs(df["forecast_error"]) /df["demand_forecast"].replace(0, pd.NA))

    inventory_report = {
        "created_features":[
        "inventory_gap",
        #"inventory_turnover",
        #"days_of_inventory",
        "forecast_error",
        "low_stock_flag"
        #"forecast_accuracy"
    ],

    "formulas":{

        "inventory_gap":"inventory_level - reorder_point",
        #"inventory_turnover":"cogs / inventory_level",
        #"days_of_inventory":"inventory_level / units_sold",
        "forecast_error":"demand_forecast - units_sold",
        "low_stock_flag":"inventory_level<reorder_point"
        #"forecast_accuracy":"1 -abs(forecast_error) /demand_forecast"

    }

    }

    return df, inventory_report


def _create_time_features(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Create time-related features based on existing columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame to be processed.

    Returns:
    tuple: A tuple containing the modified DataFrame and a report of the created features.
    """
    time_report = {}
    created_features = []
    print(df["date"].head(10))
    print(df["date"].dtype)  
    # Example: Create new features 'year', 'month', 'day' if 'date' column exists
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"],errors="coerce")
        feature_mapping = {
            "year": df["date"].dt.year,
            "month": df["date"].dt.month,
            "day": df["date"].dt.day,
            "quarter": df["date"].dt.quarter
        }

        for feature, values in feature_mapping.items():
            df[feature] = values
            created_features.append(feature)

        time_report = {
            "created_features": created_features
        }
    print(df["date"].head(10))
    print(df["date"].dtype) 

    return df, time_report


def _create_supplier_features(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    feature_mapping = {}
    created_features = []

    # Example: Create a new feature 'lead_time_category' if 'lead_time_days' column exists
    feature_mapping["lead_time_category"] = pd.cut(
        df["supplier_lead_time_days"], bins=[0, 6, 9, 100], labels=["fast", "normal", "slow"]
        )
    feature_mapping["long_lead_time_flag"] = (df["supplier_lead_time_days"] > 9) 
    #feature_mapping["reorder_flag"] = (df["inventory_level"] > df["inventory_level"])
    feature_mapping["lead_time_demand"] = df["supplier_lead_time_days"] * df["demand_forecast"]
    feature_mapping["projected_inventory_after_lead_time"]= df["inventory_level"] -feature_mapping["lead_time_demand"]
    feature_mapping["lead_time_reorder_risk"] = feature_mapping["projected_inventory_after_lead_time"] <df["reorder_point"]
    feature_mapping["projected_stockout_risk"] =  feature_mapping["projected_inventory_after_lead_time"]< 0

    for feature, values in feature_mapping.items():
        df[feature] = values
        created_features.append(feature)



    supplier_report = {
        "created_features": created_features
    }

    return df, supplier_report
    


def _create_forecast_features(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    forecast_mapping = {}
    created_features = []

    # Example: Create a new feature 'forecast_error' if 'demand_forecast' and 'units_sold' columns exist
    
    forecast_mapping["forecast_error"] = (df["demand_forecast"] - df["units_sold"])
    forecast_mapping["forecast_error_absolute"] = forecast_mapping["forecast_error"].abs()
    #forecast_mapping["forecast_accuracy"] = (1 -abs(df["forecast_error"]) /df["demand_forecast"].replace(0, pd.NA))
    forecast_mapping["forecast_bias"] = np.where(
        df["forecast_error"] > 0, "overforecast", "underforecast"
    )

    for feature, values in forecast_mapping.items():
        df[feature] = values
        created_features.append(feature)

    forecast_report = {
        "created_features": created_features
    }

    return df, forecast_report'''