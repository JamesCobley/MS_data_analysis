import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the results from the Excel file with t-test and Benjamini-Hochberg correction
file_path = '/content/HTT_vs_WT_TTest_Results_with_Metadata_And_Significance.xlsx'
df = pd.read_excel(file_path)

# Step 1: Calculate -log10(p_value_adj) for the y-axis
df['log10_p_value_adj'] = -np.log10(df['p_value_adj'])

# Step 2: Set up the figure for the volcano plot
plt.figure(figsize=(10, 7), dpi=300)

# Step 3: Plot all points (non-significant in grey)
plt.scatter(df['Mean_Difference'], df['log10_p_value_adj'], c='grey', alpha=0.7, label='Not significant')

# Step 4: Highlight significant points (p-value < 0.05) in red
significant = df['significance'] == 'yes'
plt.scatter(df.loc[significant, 'Mean_Difference'], 
            df.loc[significant, 'log10_p_value_adj'], 
            c='red', alpha=0.8, label='Significant (p_adj < 0.05)')

# Step 5: Add labels and formatting
plt.title('Volcano Plot of HTT vs. WT', fontsize=16)
plt.xlabel('Mean Difference (HTT - WT)', fontsize=12)
plt.ylabel('-log10(Adjusted p-value)', fontsize=12)
plt.axhline(y=-np.log10(0.05), color='blue', linestyle='--', linewidth=1)  # Mark significance threshold line
plt.axvline(x=0, color='black', linestyle='-', linewidth=1)  # Add line at mean difference = 0
plt.legend(loc='upper right')

# Step 6: Save the volcano plot with 300 DPI
plt.savefig('/content/Volcano_Plot_HTT_vs_WT.png', dpi=300)

# Step 7: Show the plot
plt.show()
