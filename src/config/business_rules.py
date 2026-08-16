BUSINESS_RULES = {
    "units_sold": {
        "rule": ">= 0",
        "validator": lambda x: x >= 0,
        "severity": "high",
        "action": "drop"
    },
    "inventory_level": {
        "rule": ">= 0",
        "validator": lambda x: x >= 0,
        "severity": "medium",
        "action": "impute"
    },
    "supplier_lead_time_days": {
        "rule": "> 0",
        "validator": lambda x: x > 0,
        "severity": "high",
        "action": "drop"
    },
    "reorder_point": {
        "rule": ">= 0",
        "validator": lambda x: x >= 0,
        "severity": "medium",
        "action": "impute"
    },
    "order_quantity": {
        "rule": ">= 0",
        "validator": lambda x: x >= 0,
        "severity": "high",
        "action": "drop"
    },
    "unit_cost": {
        "rule": "> 0",
        "validator": lambda x: x > 0,
        "severity": "high",
        "action": "drop"
    },
    "demand_forecast": {
        "rule": ">= 0",
        "validator": lambda x: x >= 0,
        "severity": "medium",
        "action": "impute"
    }
}