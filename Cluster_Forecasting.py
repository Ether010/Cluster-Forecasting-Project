import pandas as pd
import sys

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

### TODO: check price standard deviation per Product code

## ⬇️ To check and rewiew
# Population standard deviation of Unit price per Product Code
unit_price_std = dfRawData.groupby('Product Code')['Unit price'].agg(
    std_pop = lambda x: x.std(ddof=0)
).reset_index()

print(unit_price_std)

# ⬆️

### TODO: Check date of first code sell (min. date when sale >0)

sys.exit()

dfRawData['Date of Sale'] = pd.to_datetime(dfRawData['Date of Sale'], format='%Y-%m-%d')

sale_date_range = pd.date_range(
    start = "2024.01.01",
    end = "2025.01.05",
    freq = "D")
workdays = sale_date_range[sale_date_range.weekday < 6]
products = dfRawData['Product Code'].unique()

# full date and unique product code df
dfFDP = pd.MultiIndex.from_product(
    [workdays, products],
    names=['Date of Sale', 'Product Code']
).to_frame(index=False)

dfMerged = pd.merge(
    dfFDP,
    dfRawData,
    how='left',
    on=['Date of Sale', 'Product Code'])
dfMerged["Quantity"] = dfMerged["Quantity"].fillna(0)

### TODO: fill empty cuolumns Name, Unit price, with previous table data -> then calculate Value Q*Price = value

print(dfMerged.head(10))
