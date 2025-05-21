import pandas as pd

# Load data from Excel file into a DataFrame
dfRawData = pd.read_excel(r"C:\Users\wiktor.daszynski\Downloads\Python\Claster Forecasting Project\Data Claster Forecasting.xlsx")
# Display the first few rows of the DataFrame
print(dfRawData.head(5))

