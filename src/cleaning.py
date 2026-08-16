import pandas as pd
from src.config.business_rules import BUSINESS_RULES
from src.config.outlier_rules import OUTLIER_RULES 

def clean_data(profile_df: pd.DataFrame,profile: dict) -> pd.DataFrame:  
    report = {}
    clean_df = profile_df.copy()
    clean_df.columns=(
        profile_df.columns.str.lower()
        .str.strip()
    )

    clean_df, report["missing_values"] = _clean_missing_values(clean_df, profile)
    clean_df, report["duplicate_rows"] = _remove_duplicate_rows(clean_df)
    clean_df, report["column_names"] = _standardize_column_names(clean_df)
    clean_df, report["column_values"] = _standardize_column_values(clean_df)
    clean_df, report["data_types"] = _convert_data_types(clean_df)
    clean_df, report["validate_business_rules"] = _validate_business_rules(clean_df)
    clean_df, report["outliers"] = _handle_outliers(clean_df, profile)
    
    return clean_df,report



def _clean_missing_values(clean_df: pd.DataFrame,profile: dict) -> tuple[pd.DataFrame, dict]:
    missing_report = {
        "filled_cells": 0,
        "dropped_rows": 0,
        "strategy": {}
    }

    for col in profile["column_summary"]["numeric_columns"]:

        missing_count = clean_df[col].isnull().sum()

        if missing_count > 0:
            clean_df[col] = clean_df[col].fillna(
                clean_df[col].mean()
            )
            missing_report["filled_cells"] += missing_count
            missing_report["strategy"][col] = "mean"

    for col in profile["column_summary"]["categorical_columns"]:
        missing_count = clean_df[col].isnull().sum()

        if missing_count > 0:
            clean_df[col] = clean_df[col].fillna(
                clean_df[col].mode()[0]
            )
            missing_report["filled_cells"] += missing_count
            missing_report["strategy"][col] = "mode"
    print("Before convert:")
    print(clean_df["date"].head())
    return clean_df, missing_report


def _remove_duplicate_rows(clean_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    initial_row_count = len(clean_df)
    clean_df = clean_df.drop_duplicates()
    final_row_count = len(clean_df)

    duplicate_report = {
        "initial_row_count": initial_row_count,
        "final_row_count": final_row_count,
        "removed_duplicates": initial_row_count - final_row_count
    }
 
    return clean_df, duplicate_report



def _standardize_column_names(clean_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    _standardize_columns standardizes column names in the DataFrame.
    parameters:
        clean_df (pd.DataFrame): input Dataset.
        return:
            cleaned DataFrame and a report of the standardization.
    """
    original_columns = clean_df.columns.tolist()
    clean_df.columns = (
        clean_df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_',regex=True)
        .str.replace(r'[^\w\s]', '', regex=True)
    )
    standardized_columns = clean_df.columns.tolist()

    standardization_names_report = {
        "renaming_columns": dict(zip(original_columns, standardized_columns)),
    }

    return clean_df, standardization_names_report

def _standardize_column_values(clean_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    _standardize_column_values standardizes values in categorical columns of the DataFrame.
    parameters:
        clean_df (pd.DataFrame): input Dataset.
        return:
            cleaned DataFrame and a report of the standardization.
    """
    standardization_values_report = {}

    for col in clean_df.select_dtypes(include='object').columns:
        if col == "date":
            continue

        original_series = clean_df[col].copy()
        
        clean_df[col] = (
            clean_df[col]
            .str.strip()
            .str.lower()
            .str.replace(' ', '_', regex=True)
            .str.replace(r'[^\w\s]', '', regex=True)
        )
        mapping = {}

        for before, after in zip(original_series, clean_df[col]):
            if before != after:
                mapping[before] = after

        
        standardization_values_report[col] = {
            "standardization_mapping": mapping
        }


    return clean_df, standardization_values_report


def _convert_data_types(clean_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    conversion_report = {}

    for col in clean_df.columns:
        original_dtype = str(clean_df[col].dtype)
        if original_dtype != 'object':
                conversion_report[col] = {
                    "from": original_dtype,
                    "to": original_dtype
                }
                continue
        try:
            clean_df[col] = pd.to_numeric(clean_df[col], errors='raise')
            conversion_report[col] = {
                "from": original_dtype,
                "to": str(clean_df[col].dtype)
            }
            continue
        except:
            pass

        try:
            clean_df[col] = pd.to_datetime(clean_df[col], errors='raise')
            conversion_report[col] = {
                "from": original_dtype,
                "to": str(clean_df[col].dtype)
            }   
            continue
        except:
            pass

        conversion_report[col] = {
            "from": original_dtype,
            "to": original_dtype
        }


    return clean_df, conversion_report

def _validate_business_rules(clean_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    _validate_business_rules validates the DataFrame against predefined business rules.
    parameters:
        clean_df (pd.DataFrame): input Dataset.
        profile (dict): A structured profiling result.
        return:
            cleaned DataFrame and a report of the validation.
    """
    validation_report = {}

    # Example business rule: No negative values in numeric columns
    for col,config in BUSINESS_RULES.items():
        if col not in clean_df.columns:
            continue

        invalid_rows = clean_df[~config['validator'](clean_df[col])]
        invalid_count = invalid_rows.shape[0]

        valid_mask = config['validator'](clean_df[col])
        invalid_mask = ~valid_mask
        invalid_rows = clean_df[invalid_mask]
        invalid_count = len(invalid_rows)
        action = config['action']

        if action == "drop":
            clean_df = clean_df.loc[valid_mask]
        elif action == "impute":
            clean_df.loc[invalid_mask, col] = clean_df[col].median()
  

        result = {
            "rule": config['rule'],
            "severity": config['severity'],
            "action": config['action'],
            "invalid_count": invalid_count,
            "invalid_index": invalid_rows.index.tolist(),
            "invalid_values": invalid_rows[col].tolist()
        }
        validation_report[col] = result

 
    return clean_df, validation_report

def _handle_outliers(clean_df: pd.DataFrame,profile: dict) -> tuple[pd.DataFrame, dict]:
    
    outlier_report = {}
    profiling_result = profile["data_quality"]["outliers"]
    for col,rule in OUTLIER_RULES.items():
        print("=" * 40)
        print("Processing:", col)
        print(clean_df["order_quantity"].value_counts().head())
        if col not in clean_df.columns:
            continue
        if col not in profiling_result:
            continue
        result = profiling_result[col]
        mask = result['mask']
        action = rule['action']

        affected_rows =int(result['count'])
        if action == "ignore":
            pass
        elif action =="drop":
            clean_df = clean_df.loc[~mask]
        elif action in ["clip", "winsorize"]:
            params =result['parameter']
            print("Column:", col)
            lower_bound = params.get('lower_bound')
            upper_bound = params.get('upper_bound')
            print("Lower Bound:", lower_bound)
            print("Upper Bound:", upper_bound)

            clean_df[col] = clean_df[col].clip(lower=lower_bound, upper=upper_bound)

        elif action == "flag":
            clean_df[f"{col}_is_outlier"] = mask
            affected_rows = int(mask.sum())

        else:
            raise ValueError(f"Unsupported outlier action: {action}")
        outlier_report[col] = {
            "method": result['method'],
            "action": action,
            "status": result['status'],
            "affected_rows": affected_rows

        }

    return clean_df, outlier_report