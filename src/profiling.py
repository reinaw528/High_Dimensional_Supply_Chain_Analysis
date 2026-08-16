import pandas as pd
from src.config.outlier_rules import OUTLIER_RULES
import src.config.schema as schema


def generate_profile(profile_df: pd.DataFrame) -> dict:
    df = profile_df.copy()
    df.columns=(
        profile_df.columns.str.lower()
        .str.strip()
    )
    profile = {
            "basic_info": _get_basic_info(df),
            "data_quality": _get_data_quality(df),   
            "schema_validation": _validate_schema(df),         
            "column_summary": _get_column_summary(df),
            "descriptive_statistics": _get_descriptive_statistics(df)
    }
    
    return profile

def _get_basic_info(df):
    """
    _get_basic_info generates basic information of the given DataFrame.
    parameters:
        df (pd.DataFrame): input Dataset.
        return:
            dict: A structured basic information result.
    """
    basic_info = {
        "sample_data": df.head(),
        "shape": df.shape,
        "column_names": df.columns.tolist(),
        "data_types": df.dtypes,
        "memory_usage": df.memory_usage(deep=True).sum()
    }
    return basic_info

def _get_data_quality(df):
    """
    _get_data_quality generates data quality information of the given DataFrame.
    parameters:
        df (pd.DataFrame): input Dataset.
        return:
            dict: A structured data quality result.
    """
    data_quality = {
        "missing_values": df.isnull().sum(),
        "missing_rate": df.isnull().mean(),
        "duplicate_rows": df.duplicated().sum(),
        "outliers": _check_outliers(df)
    }

    return data_quality

def _validate_schema(df):
    report = {}
    for col in df.columns:
        
        if col not in schema.EXPECTED_SCHEMA:
            report[col] = {
                "current_dtype": str(df[col].dtype),
                "status": "UKNOWN_COLUMN"
            }
            continue
        excepted = schema.EXPECTED_SCHEMA[col]
        dtype_checker = schema.TYPE_CHECKER[excepted["dtype"]]
        passed = dtype_checker(df[col])

        report[col] = {
                "status": "PASS" if passed else "WARNING",
                "current_dtype": str(df[col].dtype),
                "expected_dtype": excepted["dtype"],
                }
    return report

def _check_outliers(df):
    
    report = {}
    for col, rule in OUTLIER_RULES.items():
        method = rule['method']
        if method == "iqr":
            report[col] = _check_outliers_iqr(df, col, rule)
        elif method == "zscore":
            report[col] = _check_outliers_zscore(df, col, rule)
    return report

def _check_outliers_iqr(df, col, rule):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    factor = rule["parameter"]["multiplier"]
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    mask = (df[col] < lower) | (df[col] > upper)
    print("=" * 40)
    print(col)
    print("Q1 =", q1)
    print("Q3 =", q3)
    print("IQR =", iqr)
    print("Lower =", lower)
    print("Upper =", upper)
    return {
            "method": "iqr",
            "status": "pass" if mask.sum() == 0 else "warning",
            "count": int(mask.sum()),
            "rate":float(mask.mean()),
            "parameter": {
                "lower_bound": lower,
                "upper_bound": upper
            },
            "mask": mask
        }

def _check_outliers_zscore(df, col, rule):
    threshold = rule["parameter"]["threshold"]
    mean = df[col].mean()
    std = df[col].std()
    z_scores = (df[col] - mean) / std
    mask = z_scores.abs() > threshold

    return {
            "method": "zscore",
            "status": "pass" if mask.sum() == 0 else "warning",
            "count": int(mask.sum()),
            "rate":float(mask.mean()),
            "parameter": {
                "threshold": threshold
            },
            "mask": mask
        }

'''Private helper functions for generating column summary and descriptive statistics.'''
def _get_column_summary(df):
    """
    _get_column_summary generates column summary information of the given DataFrame.
    parameters:
        df (pd.DataFrame): input Dataset.
        return:
            dict: A structured column summary result.
    """
    
    column_summary = {
        "numeric_columns": df.select_dtypes(include='number').columns.tolist(),
        "categorical_columns": df.select_dtypes(include='object').columns.tolist(),
        "datetime_columns": df.select_dtypes(include='datetime').columns.tolist(),
        "unique_counts": df.nunique()

    }
    return column_summary

def _get_descriptive_statistics(df):
    """
    _get_descriptive_statistics generates descriptive statistics of the given DataFrame.
    parameters:
        df (pd.DataFrame): input Dataset.
        return:
            dict: A structured descriptive statistics result.
    """
    descriptive_statistics = {
        "data_description": df.describe(include='all')
    }
    return descriptive_statistics