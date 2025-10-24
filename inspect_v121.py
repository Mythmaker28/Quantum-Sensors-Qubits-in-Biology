import pandas as pd
df = pd.read_csv('data/processed/atlas_fp_optical.csv')
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)[:15]}")
if 'contrast_ratio' in df.columns:
    print(f"Rows with contrast_ratio: {df['contrast_ratio'].notna().sum()}")
if 'contrast_value' in df.columns:
    print(f"Rows with contrast_value: {df['contrast_value'].notna().sum()}")

