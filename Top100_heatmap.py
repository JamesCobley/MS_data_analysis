import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load the results with metadata, means, and differences
mean_diff_file = '/content/HTT_vs_WT_TTest_Results_with_Metadata_And_Significance.xlsx'
mean_diff_df = pd.read_excel(mean_diff_file)

# Load the log2-transformed data
log2_file = '/content/Averaged_Log2_Transformed_Report.xlsx'
log2_df = pd.read_excel(log2_file)

# UniProt accession is in column A (df.iloc[:, 0]) and protein group name is in column C (df.iloc[:, 2])
uniprot_accession_col = mean_diff_df.columns[0]  # Column A (first column)
protein_group_col = mean_diff_df.columns[2]  # Column C (third column)

# Sort the proteins by absolute mean difference and select the top 100
top_100_proteins = mean_diff_df.nlargest(100, 'Mean_Difference', keep='all')

# Combine UniProt accession and protein group name into a single label
top_100_proteins['Protein_Label'] = top_100_proteins.apply(
    lambda row: f"{row[protein_group_col]} ({row[uniprot_accession_col]})", axis=1)

# Now map these top 100 proteins back to the log2-transformed data by matching UniProt accession
log2_data = log2_df[log2_df.iloc[:, 0].isin(top_100_proteins[uniprot_accession_col])].copy()

# Set the index to the combined labels (protein group name + UniProt accession)
log2_data['Protein_Label'] = log2_data.apply(
    lambda row: f"{row[log2_df.columns[2]]} ({row[log2_df.columns[0]]})", axis=1)

# Now subset the log2 values for the samples from columns E to X (columns 4 to 23 in zero-based indexing)
log2_values = log2_data.iloc[:, 4:24]  # Subset columns E to X (index 4 to 23)
log2_values.index = log2_data['Protein_Label']  # Set the index to the protein labels

# Replace NaN values with 0
log2_values = log2_values.fillna(0)

# Define sample groups and create a color map for them (HTT: red, WT: blue)
sample_groups = ['HTT'] * 10 + ['WT'] * 10  # Assuming 10 HTT and 10 WT samples
group_colors = ['red'] * 10 + ['blue'] * 10  # Assign colors to the sample groups

# Create a color map for the samples (annotation)
col_colors = pd.DataFrame(group_colors, index=log2_values.columns, columns=['Sample Group'])

# Create the clustermap with sample group color annotations
g = sns.clustermap(log2_values, cmap='viridis', col_colors=col_colors, figsize=(12, 10))

# Step 1: Mark missing or incomplete values (<10 valid values) with a cross
for i in range(log2_values.shape[0]):  # Iterate through each row (protein)
    for j in range(log2_values.shape[1]):  # Iterate through each column (sample)
        if log2_values.iloc[i, j] == 0:  # Mark the 0-filled NaN values with a cross
            g.ax_heatmap.scatter(j + 0.5, i + 0.5, marker='x', s=100, c='black', lw=2)

# Add a legend for sample groups
legend_labels = [mpatches.Patch(color='red', label='HTT'), mpatches.Patch(color='blue', label='WT')]
plt.legend(handles=legend_labels, title='Sample Groups', bbox_to_anchor=(1.05, 1), loc='upper left')

# Save the heatmap as a PNG file
plt.savefig('/content/Top_100_Proteins_Clustermap_with_Sample_Groups.png', dpi=300)

# Show the plot
plt.show()
