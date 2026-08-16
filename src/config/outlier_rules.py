from numpy import clip


OUTLIER_RULES = {
    "units_sold": {
        "method": "iqr",
        "parameter":{
        "multiplier": 1.5
        }
        ,
        "action": "clip"
    },
    "inventory_level": {
        "method": "iqr",
        "parameter": {
            "multiplier": 1.5
        },
        "action": "ignore"
    },
    "supplier_lead_time_days": {
        "method": "zscore",
        "parameter": {
            "threshold": 3
        },
        "action": "drop"
    },
    "reorder_point": {
        "method": "iqr",
        "parameter": {
            "multiplier": 1.5
        },
        "action": "clip"
    },
    "order_quantity": {
        "method": "iqr",
        "parameter": {
            "multiplier": 1.5
        },
        "action": "ignore"
    },
    "unit_cost": {
        "method": "iqr",
        "parameter": {
            "multiplier": 1.5
        },
        "action": "clip"
    },
    "unit_price": {
        "method": "iqr",
        "parameter": {
            "multiplier": 1.5
        },
        "action": "clip"
    },
    "demand_forecast": {
        "method": "zscore",
        "parameter": {
            "threshold": 3
        },
        "action": "flag"
    }
}