import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
import numpy as np

# Load the log2-transformed and averaged data (replace with your actual file path)
file_path = '/content/Averaged_Log2_Transformed_Report.xlsx'  # Replace with your file path
df = pd.read_excel(file_path)

# Define your HTT and WT sample groups
htt_samples = ['HTT1', 'HTT2', 'HTT3', 'HTT4', 'HTT5', 'HTT6', 'HTT7', 'HTT8', 'HTT9', 'HTT10']  # Adjust if needed
wt_samples = ['WT1', 'WT2', 'WT3', 'WT4', 'WT5', 'WT6', 'WT7', 'WT8', 'WT9', 'WT10']  # Adjust if needed

# Step 1: Ensure all values in HTT and WT groups are numeric, coercing non-numeric to NaN
df[htt_samples + wt_samples] = df[htt_samples + wt_samples].apply(pd.to_numeric, errors='coerce')

# Step 2: Filter rows where there are at least 8 non-NaN values per group
df['HTT_non_NaN'] = df[htt_samples].notna().sum(axis=1)
df['WT_non_NaN'] = df[wt_samples].notna().sum(axis=1)

# Only keep rows with at least 8 valid values in both HTT and WT groups
filtered_df = df[(df['HTT_non_NaN'] >= 8) & (df['WT_non_NaN'] >= 8)].copy()

# Step 3: Calculate the mean for each condition
filtered_df['HTT_mean'] = filtered_df[htt_samples].mean(axis=1)
filtered_df['WT_mean'] = filtered_df[wt_samples].mean(axis=1)

# Step 4: Calculate the difference between the two means
filtered_df['Mean_Difference'] = filtered_df['HTT_mean'] - filtered_df['WT_mean']

# Step 5: Perform unpaired t-test between HTT and WT for each row
def perform_ttest(row):
    # Ensure the values passed to t-test are numeric and non-NaN
    htt_values = row[htt_samples].dropna().astype(float)
    wt_values = row[wt_samples].dropna().astype(float)
    return ttest_ind(htt_values, wt_values, nan_policy='omit').pvalue

# Apply t-test row-wise and store p-values in a new column
filtered_df['p_value'] = filtered_df.apply(perform_ttest, axis=1)

# Step 6: Apply Benjamini-Hochberg FDR correction for multiple comparisons
filtered_df['p_value_adj'] = multipletests(filtered_df['p_value'], method='fdr_bh')[1]

# Step 7: Add a "significance" column based on the adjusted p-value
alpha = 0.05  # Significance level
filtered_df['significance'] = np.where(filtered_df['p_value_adj'] < alpha, 'yes', 'no')

# Step 8: Combine metadata with results
# Assuming the first 3 columns of the source file are metadata columns
metadata_columns = df.columns[:3]
final_df = pd.concat([df[metadata_columns], 
                      filtered_df[['HTT_mean', 'WT_mean', 'Mean_Difference', 'p_value', 'p_value_adj', 'significance']]], axis=1)

# Step 9: Save the results to a new Excel file
output_file_path = '/content/HTT_vs_WT_TTest_Results_with_Metadata_And_Significance.xlsx'
final_df.to_excel(output_file_path, index=False)

print(f"Results with metadata, t-tests, and significance saved to: {output_file_path}")
