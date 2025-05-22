import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load data from Excel file into a DataFrame
dfRawData = pd.read_excel(r"C:\Users\wiktor.daszynski\Downloads\Python\Cluster Forecasting Project\Data Cluster Forecasting.xlsx")

# Rename columns headers to English
dfRawData.rename(columns={
    "Kod towaru": "Product Code",
    'Opis towaru': 'Product Name',
    'Data wystawienia': 'Date of Sale',
    'Wartość towaru': 'Value',
    "Cena jednostkowa": "Unit price",
    "Ilość": "Quantity"
    }, inplace=True)

dfRawData['Date of Sale'] = pd.to_datetime(dfRawData['Date of Sale'], format='%Y-%m-%d')

# Find minimum sale date for each product
min_dates = dfRawData.groupby('Product Code')['Date of Sale'].min()

metrics = []
last_date = pd.to_datetime("2025-05-01")

for code, min_date in min_dates.items():
    # Filter only this product
    df_code = dfRawData[dfRawData['Product Code'] == code][['Date of Sale', 'Quantity']].copy()
    # Create full date range for this product (daily)
    date_range = pd.date_range(start=min_date, end=last_date, freq='D')
    df_full = pd.DataFrame({'Date of Sale': date_range})
    df_full = df_full.merge(df_code, on='Date of Sale', how='left').fillna({'Quantity': 0})
    # Set date as index for resampling
    df_full.set_index('Date of Sale', inplace=True)
    # Resample to weekly (sum quantities per week, week starts on Monday)
    df_weekly = df_full.resample('W').sum()
    # Calculate metrics on weekly data
    avg = df_weekly['Quantity'].mean()
    std = df_weekly['Quantity'].std(ddof=0)
    cv = round((std / avg * 100), 2) if avg != 0 else np.nan
    metrics.append({'Product Code': code, 'Average': avg, 'StdDev': std, 'CV (%)': cv})

# Combine all metrics into a DataFrame
dfMetrics = pd.DataFrame(metrics)

# Assign XYZ classes based on CV (%) thresholds
def xyz_class(cv):
    if cv <= 50:
        return 'X'
    elif 50 < cv <= 100:
        return 'Y'
    else:
        return 'Z'

dfMetrics['XYZ'] = dfMetrics['CV (%)'].apply(xyz_class)
print(dfMetrics[['Product Code', 'CV (%)', 'XYZ']])

