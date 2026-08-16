import pandas as pd
EXPECTED_SCHEMA = {
            "date": {"dtype": "datetime", "nullable": False},
            "region": {"dtype": "string", "nullable": False},
            "units_sold": {"dtype": "numeric", "nullable": False, "min": 0},
            "inventory_level": {"dtype": "numeric", "nullable": False},
            "supplier_lead_time_days": {"dtype": "numeric", "nullable": False},
            "reorder_point": {"dtype": "numeric", "nullable": False},
            "order_quantity": {"dtype": "numeric", "nullable": False},
            "unit_cost": {"dtype": "numeric", "nullable": False},
            "unit_price": {"dtype": "numeric", "nullable": False},
            "promotion_flag": {"dtype": "boolean"},
            "stockout_flag": {"dtype": "boolean"},
            "demand_forecast": {"dtype": "numeric"},
            "demand_forecast_outlier_flag": {"dtype": "boolean"}
        }
TYPE_CHECKER = {
        "numeric": pd.api.types.is_numeric_dtype,
        "datetime": pd.api.types.is_datetime64_any_dtype,
        "string": pd.api.types.is_string_dtype,
        "category": pd.api.types.is_categorical_dtype,
        'boolean': pd.api.types.is_bool_dtype,
        }