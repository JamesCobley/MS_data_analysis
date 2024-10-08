import pandas as pd
import numpy as np

# Load the protein group report file (replace with the correct path to your file)
file_path = '/content/Report_HTT_James.xlsx'  
df = pd.read_excel(file_path)

# Select the unnamed columns from 4 to 63 (index 4 to 63 refers to actual columns 5 to 64)
unnamed_columns = df.columns[4:64]  # Select columns Unnamed: 4 to Unnamed: 63

# Convert the columns to numeric, coercing non-numeric values to NaN
df[unnamed_columns] = df[unnamed_columns].apply(pd.to_numeric, errors='coerce')

# Log2 transform the selected unnamed columns, adding a small constant (1) to avoid log2(0) issues
df[unnamed_columns] = df[unnamed_columns].apply(lambda x: np.log2(x + 1))

# Display the first few rows of the log2-transformed data
print("First 5 rows after log2 transformation:")
display(df.head())

# Save the log2-transformed data to a new Excel file
output_file_path = '/content/Log2_Transformed_Report_HTT_James_Unnamed_Columns.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Log2-transformed data (Unnamed columns) saved to: {output_file_path}")
