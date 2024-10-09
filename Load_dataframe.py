from google.colab import files
import pandas as pd

# Use the upload widget in colab to upload a file
uploaded = files.upload()

# Get the uploaded file path
file_path = next(iter(uploaded))

# Load the Excel file
xls = pd.ExcelFile(file_path)

# Load the first sheet into a DataFrame
df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

# Print the column names
print("Column names in the selected file")
print(df.columns)
