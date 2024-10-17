import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the Excel file
file_path = '/content/report_pg_matrix_log2.xlsx'  # Adjust with the actual path
df = pd.read_excel(file_path)

# Step 1: Print column names for clarity
print("Column names in the dataset:")
print(df.columns.tolist())

# Step 2: Ask the user for the number of sample columns
sample_size = int(input("\nPlease enter the number of sample columns (integer): "))

# Function to calculate allowed percentages based on sample size
def calculate_allowed_percentages(n):
    return [(i / n) * 100 for i in range(n + 1)]

# Calculate allowed percentages based on the sample size
allowed_percentages = calculate_allowed_percentages(sample_size)
print(f"\nAllowed percentages for a sample size of {sample_size}: {allowed_percentages}")

# Step 3: Identify sample columns (we assume metadata columns are the first 4)
sample_columns = df.columns[4:]  # Adjust if your metadata columns are different

# Step 4: Calculate data completeness based on the number of blank cells
def calculate_completeness_by_blank_cells(row, total_columns):
    blank_cells = row.isna().sum()  # Count the number of blank cells
    completeness_percentage = ((total_columns - blank_cells) / total_columns) * 100  # Map to completeness
    return completeness_percentage

# Calculate completeness for each row
completeness = df[sample_columns].apply(lambda row: calculate_completeness_by_blank_cells(row, sample_size), axis=1)

# Step 5: Verify if the completeness percentage matches allowed values
def enforce_allowed_percentage(completeness_value, allowed):
    # If the completeness value is not in the allowed list, return False
    if completeness_value not in allowed:
        return False
    return True

# Step 6: Check and print invalid rows
def print_if_completeness_invalid(row, completeness_percentage, allowed_percentages):
    if not enforce_allowed_percentage(completeness_percentage, allowed_percentages):
        blank_cells = row.isna().sum()  # Count blank cells
        print(f"\n--- Invalid Row Detected ---")
        print(f"Row data (blank cells: {blank_cells}, completeness: {completeness_percentage}%):")
        print(row.values)

# Apply the check and print only invalid rows
df[sample_columns].apply(lambda row: print_if_completeness_invalid(row, calculate_completeness_by_blank_cells(row, sample_size), allowed_percentages), axis=1)

# Step 7: Plot the data completeness as a histogram
plt.figure(figsize=(8, 6), dpi=300)
plt.hist(completeness, bins=len(allowed_percentages), edgecolor='black')

# Adjust the x-axis to match allowed percentages
plt.xticks(allowed_percentages)  # Set x-ticks to allowed percentages
plt.xlim(0, 100)  # Set the x-axis limits to go from 0% to 100%

plt.title('Data Completeness Histogram')
plt.xlabel('Completeness (%)')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('/content/Data_Completeness_Histogram.png')  # Save the histogram as a PNG file

# Step 8: Save the adjusted completeness and results to Excel
output_file_path = '/content/Protein_Groups_Completeness.xlsx'
with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    # Save sheet 1: Unique protein groups identified in each sample
    sheet1_df = pd.DataFrame({'Sample': sample_columns, 'Unique Protein Groups': df[sample_columns].notna().sum()})
    sheet1_df.to_excel(writer, sheet_name='Protein Groups Identified', index=False)
    
    # Add completeness to metadata columns
    sheet2_df = pd.concat([df.iloc[:, :4], pd.DataFrame({'Completeness (%)': completeness})], axis=1)
    sheet2_df.to_excel(writer, sheet_name='Data Completeness', index=False)

print(f"Protein group counts and data completeness (with metadata) saved to: {output_file_path}")
