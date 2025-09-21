import camelot
import pandas as pd
import re

pdf_path = "nevadareportcard_2024.pdf"

# --- Cleaning helpers ---

def clean_cell(cell):
    """Normalize whitespace and add space between lowercase-uppercase"""
    if cell is None:
        return ""
    text = " ".join(cell.split())
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    return text.strip()

def merge_split_rows(df):
    """Merge rows where the first cell is blank into the previous row"""
    merged_rows = []
    buffer_row = None

    for _, row in df.iterrows():
        first_cell = row[0].strip()
        if first_cell == "" and buffer_row is not None:
            # Merge this row into buffer_row
            buffer_row = [
                buffer_row[i] + " " + row[i].strip()
                if row[i].strip() != "" else buffer_row[i]
                for i in range(len(row))
            ]
        else:
            if buffer_row is not None:
                merged_rows.append(buffer_row)
            buffer_row = list(row)
    if buffer_row is not None:
        merged_rows.append(buffer_row)

    return pd.DataFrame(merged_rows)

def strip_empty_columns(df):
    """Remove trailing empty columns"""
    df = df.replace(r'^\s*$', pd.NA, regex=True)
    return df.dropna(axis=1, how="all")

# --- Extract + clean ---

tables = camelot.read_pdf(
    pdf_path,
    pages="all",
    flavor="lattice",
    line_scale=30
)

cleaned_dfs = []
for t in tables:
    df = t.df.applymap(clean_cell)
    df = merge_split_rows(df)
    df = strip_empty_columns(df)
    cleaned_dfs.append(df)

big_df = pd.concat(cleaned_dfs, ignore_index=True)

# --- Save clean CSV ---
big_df.to_csv("nevada_report_clean.csv", index=False)
print("Saved nevada_report_clean.csv with shape:", big_df.shape)