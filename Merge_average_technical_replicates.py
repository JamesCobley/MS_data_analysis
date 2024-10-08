import pandas as pd
import numpy as np

# Load the log2-transformed data (replace with your actual file path)
file_path = 'Log2_Transformed_Report_HTT_James_Unnamed_Columns.xlsx'  # Replace with your log2-transformed file path
df = pd.read_excel(file_path)

# Define the column groups for technical replicates
replicate_groups = {
    'HTT1': ['Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6'],
    'HTT2': ['Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'],
    'HTT3': ['Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12'],
    'HTT4': ['Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15'],
    'HTT5': ['Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18'],
    'HTT6': ['Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21'],
    'HTT7': ['Unnamed: 22', 'Unnamed: 23', 'Unnamed: 24'],
    'HTT8': ['Unnamed: 25', 'Unnamed: 26', 'Unnamed: 27'],
    'HTT9': ['Unnamed: 28', 'Unnamed: 29', 'Unnamed: 30'],
    'HTT10': ['Unnamed: 31', 'Unnamed: 32', 'Unnamed: 33'],

    'WT1': ['Unnamed: 34', 'Unnamed: 35', 'Unnamed: 36'],
    'WT2': ['Unnamed: 37', 'Unnamed: 38', 'Unnamed: 39'],
    'WT3': ['Unnamed: 40', 'Unnamed: 41', 'Unnamed: 42'],
    'WT4': ['Unnamed: 43', 'Unnamed: 44', 'Unnamed: 45'],
    'WT5': ['Unnamed: 46', 'Unnamed: 47', 'Unnamed: 48'],
    'WT6': ['Unnamed: 49', 'Unnamed: 50', 'Unnamed: 51'],
    'WT7': ['Unnamed: 52', 'Unnamed: 53', 'Unnamed: 54'],
    'WT8': ['Unnamed: 55', 'Unnamed: 56', 'Unnamed: 57'],
    'WT9': ['Unnamed: 58', 'Unnamed: 59', 'Unnamed: 60'],
    'WT10': ['Unnamed: 61', 'Unnamed: 62', 'Unnamed: 63'],
    # Continue for the remaining WT samples...
}

# Create a new DataFrame to store the averaged values
averaged_df = pd.DataFrame()

# For each sample (HTT1, WT1, etc.), calculate the mean of the technical replicates
for sample, replicates in replicate_groups.items():
    averaged_df[sample] = df[replicates].apply(lambda row: row.mean() if row.count() > 1 else row.dropna().values[0] if row.count() == 1 else np.nan, axis=1)

# Combine the metadata columns (if any) with the averaged values
metadata_columns = df.columns[:4]  # Assuming first 4 columns are metadata (adjust if needed)
final_df = pd.concat([df[metadata_columns], averaged_df], axis=1)

# Display the first few rows of the averaged data
print("Averaged values across technical replicates:")
display(final_df.head())

# Save the averaged data to a new Excel file
output_file_path = 'Averaged_Log2_Transformed_Report.xlsx'
final_df.to_excel(output_file_path, index=False)

print(f"Averaged log2-transformed data saved to: {output_file_path}")
