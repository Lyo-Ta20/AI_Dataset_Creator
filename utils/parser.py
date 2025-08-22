# utils/parser.py
import pandas as pd

def clean_messy_text(raw_text):
    """
    Convert messy text into a structured DataFrame.
    Handles commas, spaces, and semicolons as separators.
    """
    try:
        # Split rows by semicolon or space
        rows = [list(filter(None, r.strip().split())) for r in raw_text.replace(",", " ").split(";")]
        # Find max number of columns
        max_len = max(len(r) for r in rows)
        # Generate column names
        columns = [f"Column {i+1}" for i in range(max_len)]
        # Pad shorter rows with empty strings
        padded_rows = [r + [""]*(max_len - len(r)) for r in rows]
        # Create DataFrame
        df = pd.DataFrame(padded_rows, columns=columns)
        return df
    except Exception as e:
        print(f"Error parsing text: {e}")
        return pd.DataFrame()
