import pandas as pd

# Load your protein report HTT file into colab
file_path = '/content/Report_HTT_James.xlsx'
xls = pd.ExcelFile(file_path)

# Load the first sheet into a DataFrame
df = pd.read_excel(xls, sheet_name='Sheet 1')

# Print the column names
print(df.columns)
