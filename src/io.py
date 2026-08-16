import pandas as pd
from pathlib import Path
def load_csv(file_path: str|Path) -> pd.DataFrame:
    """load_csv loads a CSV file into a pandas DataFrame.
    args:
        file_path (str|Path): The path to the CSV file.
    return:
        pd.DataFrame: The loaded DataFrame.
    raises:
        FileNotFoundError: If the file does not exist.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")


def save_csv(df: pd.DataFrame, file_path: str|Path) -> None: 
    """save_csv saves a pandas DataFrame to a CSV file.
    args:
        df (pd.DataFrame): The DataFrame to save.
        file_path (str|Path): The path to the CSV file.
    """
    df.to_csv(file_path, index=False)