import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load data from Excel file into a DataFrame
dfRawData = pd.read_excel(r"C:\Users\wiktor.daszynski\Downloads\Python\Cluster Forecasting Project\Data Cluster Forecasting.xlsx")

#Rename columns heders to english
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

# Prepare the final list to collect metrics
metrics = []

# Set the last date for expansion
last_date = pd.to_datetime("2025-05-01")

# Process each product separately
for code, min_date in min_dates.items():
    # Filter only this product
    df_code = dfRawData[dfRawData['Product Code'] == code][['Date of Sale', 'Quantity']].copy()
    # Create full date range for this product
    date_range = pd.date_range(start=min_date, end=last_date, freq='D')
    # Merge with full date range, fill missing Quantity with 0
    df_full = pd.DataFrame({'Date of Sale': date_range})
    df_full = df_full.merge(df_code, on='Date of Sale', how='left').fillna({'Quantity': 0})
    # Calculate metrics
    avg = df_full['Quantity'].mean()
    std = df_full['Quantity'].std(ddof=0)
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

