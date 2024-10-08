import pandas as pd

# Load the dataset with molecular weights and log2-transformed intensities
data_file = '/content/dataset_with_estimated_molecular_weights.xlsx'
df = pd.read_excel(data_file)

# Define columns of interest (metadata and sample intensities)
metadata_columns = ['Report_HTT_James.pg_matrix', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3']

# Define sample columns (explicitly include HTT1-HTT10 and WT1-WT10)
sample_columns = [
    'HTT1', 'HTT2', 'HTT3', 'HTT4', 'HTT5', 'HTT6', 'HTT7', 'HTT8', 'HTT9', 'HTT10',
    'WT1', 'WT2', 'WT3', 'WT4', 'WT5', 'WT6', 'WT7', 'WT8', 'WT9', 'WT10'
]

# List of detected histone UniProt IDs (used in previous steps)
detected_histones = [
    'P10922', 'P15864', 'P27661', 'P43274', 'P43247', 'P43275', 'P43276', 
    'P43277', 'P62806', 'Q64478', 'Q64524', 'Q9QZQ8', 'C0HKE1', 'P02301', 'P0C0S6'
]

# Step 1: Filter the dataset to include only the histones detected
histone_df = df[df['Report_HTT_James.pg_matrix'].isin(detected_histones)]

# Step 2: Sum the intensities of histones in each sample
histone_sums = histone_df[sample_columns].sum()

# Step 3: Normalize protein intensities based on histone sums
# For each sample, divide the protein intensity by the histone sum for that sample
normalized_df = df.copy()

for sample in sample_columns:
    normalized_df[sample] = normalized_df[sample] / histone_sums[sample]

# Step 4: Calculate copy numbers for each protein in each sample
# Assuming a total protein mass of 200 picograms (pg) per cell, or approximately 1.2 × 10^10 Daltons
total_protein_mass_daltons = 1.2e10  # Adjust this value based on your experimental setup

# Create new columns for copy numbers in each sample
for sample in sample_columns:
    normalized_df[f'Copy_Number_{sample}'] = (normalized_df[sample] * total_protein_mass_daltons) / normalized_df['Estimated_Molecular_Weight']

# Step 5: Save the updated dataset with individual copy numbers for each sample
output_file = '/content/proteomic_ruler_normalized_copy_numbers_per_sample.xlsx'
normalized_df.to_excel(output_file, index=False)

print(f"Proteomic ruler normalization completed. Results saved to {output_file}")
