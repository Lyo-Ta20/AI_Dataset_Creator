import pandas as pd
import re
from datetime import datetime

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize column names
    df.columns = [col.strip().title() for col in df.columns]

    # Clean Name (capitalize properly, strip spaces)
    if "Name" in df.columns:
        df["Name"] = df["Name"].fillna("").str.strip().str.title()
        df["Name"] = df["Name"].replace("", None)

    # Clean Age (convert to int, fill missing with NaN)
    if "Age" in df.columns:
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

    # Clean Dept (capitalize first letter, remove blanks)
    if "Dept" in df.columns:
        df["Dept"] = df["Dept"].fillna("").str.strip().str.title()
        df["Dept"] = df["Dept"].replace("", None)

    # Clean Salary (extract numbers only)
    if "Salary" in df.columns:
        df["Salary"] = df["Salary"].astype(str)
        df["Salary"] = df["Salary"].apply(lambda x: re.sub(r"[^\d.]", "", x))
        df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

    # Clean Join Date (convert to YYYY-MM-DD)
    if "Join Date" in df.columns:
        def normalize_date(x):
            if pd.isna(x):
                return None
            for fmt in ("%d/%m/%y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
                try:
                    return datetime.strptime(str(x).strip(), fmt).strftime("%Y-%m-%d")
                except:
                    continue
            return None
        df["Join Date"] = df["Join Date"].apply(normalize_date)

    return df
