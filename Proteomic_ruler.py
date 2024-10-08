import pandas as pd

# Load the dataset with molecular weights and log2-transformed intensities
data_file = '/content/dataset_with_estimated_molecular_weights.xlsx'
df = pd.read_excel(data_file)

# Define columns of interest (metadata and sample intensities)
metadata_columns = ['Report_HTT_James.pg_matrix', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3']
sample_columns = df.columns[4:]  # Assuming the sample intensity columns start after the metadata columns

# List of detected histone UniProt IDs
detected_histones = [
    'P10922', 'P15864', 'P27661', 'P43274', 'P43247', 'P43275', 'P43276', 
    'P43277', 'P62806', 'Q64478', 'Q64524', 'Q9QZQ8', 'C0HKE1', 'P02301', 'P0C0S6'
]

# Step 1: Filter the dataset to include only the histones detected
histone_df = df[df['Report_HTT_James.pg_matrix'].isin(detected_histones)]

# Print the identified histones for verification
print("Histone proteins found in the dataset:", histone_df['Report_HTT_James.pg_matrix'].tolist())

# Step 2: Sum the intensities of histones in each sample
histone_sums = histone_df[sample_columns].sum()

# Step 3: Normalize protein intensities based on histone sums
# For each sample, divide the protein intensity by the histone sum for that sample
normalized_df = df.copy()

for sample in sample_columns:
    normalized_df[sample] = normalized_df[sample] / histone_sums[sample]

# Step 4: Estimate protein copy numbers
# Assuming a total protein mass of 200 picograms (pg) per cell, or approximately 1.2 × 10^10 Daltons
total_protein_mass_daltons = 1.2e10  # Adjust this value based on your experimental setup

# Calculate copy numbers for each protein
normalized_df['Copy_Number'] = (normalized_df[sample_columns].mean(axis=1) * total_protein_mass_daltons) / normalized_df['Estimated_Molecular_Weight']

# Save the normalized data with copy numbers
output_file = '/content/proteomic_ruler_normalized_with_copy_numbers.xlsx'
normalized_df.to_excel(output_file, index=False)

print(f"Proteomic ruler normalization completed. Results saved to {output_file}")
