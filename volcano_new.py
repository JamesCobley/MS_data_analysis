import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew

# Step 1: Load the results from the Excel file with t-test and Benjamini-Hochberg correction
file_path = '/content/HTT_vs_WT_TTest_Results_with_Metadata_And_Significance.xlsx'
df = pd.read_excel(file_path)

# Step 2: Calculate -log10(p_value) for the y-axis (use unadjusted p-values)
df['log10_p_value'] = -np.log10(df['p_value'])

# Step 3: Set up the figure for the volcano plot
plt.figure(figsize=(10, 7), dpi=300)

# Step 4: Plot non-significant points in grey
plt.scatter(df['Mean_Difference'], df['log10_p_value'], c='grey', alpha=0.7, label='Not significant')

# Step 5: Highlight upregulated and downregulated points with different colors
# Upregulated: Positive mean difference and significant (e.g., blue)
upregulated = (df['p_value'] < 0.05) & (df['Mean_Difference'] > 0)
plt.scatter(df.loc[upregulated, 'Mean_Difference'], 
            df.loc[upregulated, 'log10_p_value'], 
            c='blue', alpha=0.8, label='Upregulated (p < 0.05)')

# Downregulated: Negative mean difference and significant (e.g., green)
downregulated = (df['p_value'] < 0.05) & (df['Mean_Difference'] < 0)
plt.scatter(df.loc[downregulated, 'Mean_Difference'], 
            df.loc[downregulated, 'log10_p_value'], 
            c='red', alpha=0.8, label='Downregulated (p < 0.05)')

# Step 6: Add labels, formatting, and gridlines to the volcano plot
plt.title('Volcano Plot of HTT vs. WT (Unadjusted p-values)', fontsize=16)
plt.xlabel('Mean Difference (HTT - WT)', fontsize=12)
plt.ylabel('-log10(p-value)', fontsize=12)
plt.axhline(y=-np.log10(0.05), color='blue', linestyle='--', linewidth=1, label='p = 0.05')  # Significance threshold
plt.axvline(x=0, color='black', linestyle='-', linewidth=1)  # Mean difference = 0 line
plt.grid(True, linestyle='--', linewidth=0.5)  # Add gridlines for better readability
plt.legend(loc='upper right')

# Step 7: Save the volcano plot with 300 DPI
volcano_output_path = '/content/Volcano_Plot_HTT_vs_WT_Unadjusted.png'
plt.savefig(volcano_output_path, dpi=300)
print(f"Volcano plot saved to: {volcano_output_path}")

# Step 8: Show the volcano plot
plt.show()

# Step 9: Symmetry analysis of the volcano plot
# Count the number of proteins with positive and negative mean differences
positive_side = df[df['Mean_Difference'] > 0].shape[0]  # Proteins with positive mean differences
negative_side = df[df['Mean_Difference'] < 0].shape[0]  # Proteins with negative mean differences

# Calculate the ratio of positive to negative mean differences
ratio_pos_neg = positive_side / negative_side if negative_side != 0 else np.inf

# Calculate the mean and median of the mean differences
mean_diff_mean = df['Mean_Difference'].mean()
mean_diff_median = df['Mean_Difference'].median()

# Calculate the skewness of the mean differences
mean_diff_skewness = skew(df['Mean_Difference'].dropna())

# Step 10: Display the symmetry analysis results
print(f"Number of proteins with positive mean differences: {positive_side}")
print(f"Number of proteins with negative mean differences: {negative_side}")
print(f"Ratio of positive to negative mean differences: {ratio_pos_neg:.2f}")
print(f"Mean of Mean Differences: {mean_diff_mean:.4f}")
print(f"Median of Mean Differences: {mean_diff_median:.4f}")
print(f"Skewness of Mean Differences: {mean_diff_skewness:.4f}")

# Step 11: Visualize the distribution of Mean Differences using a histogram with KDE
plt.figure(figsize=(8, 6), dpi=300)
sns.histplot(df['Mean_Difference'], kde=True, bins=50, color='purple', alpha=0.7)
plt.axvline(x=0, color='black', linestyle='--', label='Mean Difference = 0')
plt.title('Distribution of Mean Differences (HTT vs. WT)', fontsize=14)
plt.xlabel('Mean Difference (HTT - WT)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, linestyle='--', linewidth=0.5)  # Add gridlines to the distribution plot
plt.legend()
distribution_output_path = '/content/Mean_Difference_Distribution.png'
plt.savefig(distribution_output_path, dpi=300)
print(f"Distribution plot saved to: {distribution_output_path}")

# Step 12: Show the distribution plot
plt.show()
