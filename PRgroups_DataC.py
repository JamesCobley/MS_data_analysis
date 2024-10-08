import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the log2-transformed and averaged data (replace with your actual file path)
file_path = '/content/Averaged_Log2_Transformed_Report.xlsx'  # Path to your merged and processed data
df = pd.read_excel(file_path)

# Step 1: Count unique protein groups (column 1) for each sample and output to sheet 1
# Split the UniProt IDs by ';' and count unique IDs per row, ignoring NaN values
df['Unique_Protein_Count'] = df.iloc[:, 0].apply(lambda x: len(set(str(x).split(';'))) if pd.notna(x) else 0)

# Step 2: Now, calculate the total number of protein groups identified in each sample
# Assuming the first 4 columns are metadata, the actual sample data starts from column 5 onward
sample_columns = df.columns[4:]

# Create a DataFrame to store the number of identified protein groups per sample
sheet1_df = pd.DataFrame({
    'Sample': sample_columns,
    'Unique_Protein_Groups': [df[col].notna().sum() for col in sample_columns]  # Count non-NaN values per sample
})

# Step 3: Calculate data completeness (the proportion of non-NaN values for each row) for sheet 2
# Completeness for each row is calculated as the proportion of non-NaN values across all samples
completeness = df[sample_columns].notna().mean(axis=1) * 100  # Convert to percentage

# Include metadata columns (first 4 columns) in sheet 2 alongside completeness data
sheet2_df = pd.concat([df.iloc[:, :4], pd.DataFrame({'Completeness (%)': completeness})], axis=1)

# Step 4: Plot the data completeness as a histogram
plt.figure(figsize=(8, 6), dpi=300)
plt.hist(completeness, bins=20, edgecolor='black')
plt.title('Data Completeness Histogram')
plt.xlabel('Completeness (%)')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('/content/Data_Completeness_Histogram.png')  # Save the histogram as a PNG file

# Step 5: Save everything to a new Excel file with two sheets
output_file_path = '/content/Protein_Groups_And_Completeness_with_Metadata.xlsx'
with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    # Write sheet 1: Unique protein groups identified in each sample
    sheet1_df.to_excel(writer, sheet_name='Protein Groups Identified', index=False)
    
    # Write sheet 2: Data completeness for each row with metadata
    sheet2_df.to_excel(writer, sheet_name='Data Completeness', index=False)

print(f"Protein group counts and data completeness (with metadata) saved to: {output_file_path}")
