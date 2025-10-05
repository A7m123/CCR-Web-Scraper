"""
Quick data viewer to check the scraped data
"""
import pandas as pd
import glob

# Find the latest Excel file
excel_files = glob.glob('ccr_data_*.xlsx')
if not excel_files:
    print("No data files found!")
    exit()

latest_file = max(excel_files)
print(f"Reading: {latest_file}\n")

# Read the data
df = pd.read_excel(latest_file)

print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print("\nColumns:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

print("\nFirst few rows:")
print(df.head())

print("\nSample data from first row:")
for col in df.columns:
    print(f"  {col}: {df[col].iloc[0] if len(df) > 0 else 'N/A'}")
