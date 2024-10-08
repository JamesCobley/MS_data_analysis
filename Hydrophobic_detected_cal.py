import pandas as pd
import numpy as np

# Paths to the input files
hydrophobic_file = '/content/hydrophobic_proteins.xlsx'
dataset_file = '/content/Averaged_Log2_Transformed_Report.xlsx'

# Load the hydrophobic proteins list
hydrophobic_df = pd.read_excel(hydrophobic_file)

# Load the dataset with protein detections
dataset_df = pd.read_excel(dataset_file)

# Display column names for verification
print("Hydrophobic Proteins File Columns:", hydrophobic_df.columns.tolist())
print("Dataset File Columns:", dataset_df.columns.tolist())

# **Assumptions:**
# - Hydrophobic Proteins File has columns: ['UniProt ID', 'Protein Name', 'GRAVY Score']
# - Dataset File has 'UniProt ID' in the first column (column A, which is named 'Report_HTT_James.pg_matrix')
# - Sample columns are from 'Unnamed: 3' and onward for samples.

# Verifying the columns are present
required_hydrophobic_cols = ['UniProt ID', 'Protein Name', 'GRAVY Score']
required_dataset_cols = ['Report_HTT_James.pg_matrix', 'Unnamed: 3']  # Adjusted the columns to match what you mentioned

for col in required_hydrophobic_cols:
    if col not in hydrophobic_df.columns:
        raise ValueError(f"Missing column '{col}' in hydrophobic proteins file.")

# Merge hydrophobic proteins with dataset based on 'Report_HTT_James.pg_matrix' (equivalent to 'UniProt ID')
# Using 'inner' join to keep only hydrophobic proteins present in the dataset
merged_df = pd.merge(hydrophobic_df, dataset_df, left_on='UniProt ID', right_on='Report_HTT_James.pg_matrix', how='inner')

# Define the sample columns (columns starting from 'Unnamed: 3' onwards, representing HTT and WT samples)
sample_columns = ['Unnamed: 3'] + dataset_df.columns[4:].tolist()  # Assuming columns E onward are the sample columns

# Display sample columns for verification
print("Sample Columns:", sample_columns)

# Create binary presence columns: 1 if detected (non-NaN), 0 otherwise
for sample in sample_columns:
    merged_df[sample] = merged_df[sample].notna().astype(int)

# Calculate Detection Frequency (%) as (sum of presence) / 20 * 100
merged_df['Detection Frequency (%)'] = merged_df[sample_columns].sum(axis=1) / len(sample_columns) * 100

# Select the desired columns: 'UniProt ID', 'Protein Name', 'GRAVY Score', sample columns, 'Detection Frequency (%)'
output_columns = ['UniProt ID', 'Protein Name', 'GRAVY Score'] + sample_columns + ['Detection Frequency (%)']
detected_hydrophobic_df = merged_df[output_columns].copy()

# Rename columns for clarity (optional)
detected_hydrophobic_df.rename(columns={'Protein Name': 'Name'}, inplace=True)

# Save to a new Excel file
output_file = '/content/detected_hydrophobic_proteins.xlsx'
detected_hydrophobic_df.to_excel(output_file, index=False)

# Print summary
total_hydrophobic = detected_hydrophobic_df.shape[0]
high_detection = detected_hydrophobic_df[detected_hydrophobic_df['Detection Frequency (%)'] == 100].shape[0]
print(f"Total hydrophobic proteins detected in the dataset: {total_hydrophobic}")
print(f"Proteins detected in all 20 samples: {high_detection}")
print(f"Detected hydrophobic proteins saved to {output_file}")
