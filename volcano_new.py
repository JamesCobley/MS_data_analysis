import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew

# Function to select the sheet and load the Excel file
def load_excel(file_path):
    xl = pd.ExcelFile(file_path)
    print("Available sheets:", xl.sheet_names)
    selected_sheet = input("Enter the sheet name you want to select: ")
    if selected_sheet not in xl.sheet_names:
        raise ValueError(f"Sheet '{selected_sheet}' not found.")
    return xl.parse(selected_sheet)

# Step 1: Load the results from the selected sheet of the Excel file
file_path = '/content/HTT_EXP_OCT_24.xlsx'  # Update this to your actual file path
df = load_excel(file_path)

# Step 2: Calculate -log10(p_value) for the y-axis (use unadjusted p-values)
df['log10_p_value'] = -np.log10(df['p_value'])

# Step 3: Sort by differential expression (assume it's in column C) and get the top 100 proteins
top_100_proteins = df.nlargest(100, 'Differential Expression')['Gene Name']

# Step 4: Set up the figure for the volcano plot
plt.figure(figsize=(10, 7), dpi=300)

# Step 5: Plot non-significant points in grey
plt.scatter(df['Mean_Difference'], df['log10_p_value'], c='grey', alpha=0.7, label='Not significant')

# Step 6: Highlight upregulated and downregulated points with different colors
# Upregulated: Positive mean difference and significant (e.g., blue)
upregulated = (df['p_value'] < 0.05) & (df['Mean_Difference'] > 0)
plt.scatter(df.loc[upregulated, 'Mean_Difference'], 
            df.loc[upregulated, 'log10_p_value'], 
            c='blue', alpha=0.8, label='Upregulated (p < 0.05)')

# Downregulated: Negative mean difference and significant (e.g., red)
downregulated = (df['p_value'] < 0.05) & (df['Mean_Difference'] < 0)
plt.scatter(df.loc[downregulated, 'Mean_Difference'], 
            df.loc[downregulated, 'log10_p_value'], 
            c='red', alpha=0.8, label='Downregulated (p < 0.05)')

# Step 7: Annotate the top 100 proteins with their gene names
for i, gene_name in enumerate(top_100_proteins):
    row = df[df['Gene Name'] == gene_name]
    plt.text(row['Mean_Difference'].values[0], row['log10_p_value'].values[0], gene_name, fontsize=8)

# Step 8: Add labels, formatting, and gridlines to the volcano plot
plt.title('Volcano Plot of HTT vs. WT (Top 100 Differentially Expressed Genes)', fontsize=16)
plt.xlabel('Mean Difference (HTT - WT)', fontsize=12)
plt.ylabel('-log10(p-value)', fontsize=12)
plt.axhline(y=-np.log10(0.05), color='blue', linestyle='--', linewidth=1, label='p = 0.05')  # Significance threshold
plt.axvline(x=0, color='black', linestyle='-', linewidth=1)  # Mean difference = 0 line
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend(loc='upper right')

# Step 9: Save the volcano plot with 300 DPI
volcano_output_path = '/content/Volcano_Plot_Top_100_Genes.png'
plt.savefig(volcano_output_path, dpi=300)
print(f"Volcano plot saved to: {volcano_output_path}")

# Step 10: Show the volcano plot
plt.show()
