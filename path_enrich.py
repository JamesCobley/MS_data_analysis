import pandas as pd
from scipy.stats import fisher_exact
from gprofiler import GProfiler

# Step 1: Load your dataset containing mouse proteins/genes and their p-values
file_path = '/content/HTT_EXP_OCT_24.xlsx'  # Update this to your actual file path
df = pd.read_excel(file_path)

# Step 2: Filter significant proteins based on the p-value threshold (e.g., p_value < 0.05)
significance_threshold = 0.05
significant_proteins = df[df['p_value'] < significance_threshold]['Gene'].tolist()

# Step 3: Initialize g:Profiler for Mus musculus (mouse) and run enrichment analysis
gp = GProfiler(return_dataframe=False)  # Set return_dataframe to False for detailed output
# Use 'mmusculus' for mouse-specific enrichment
results = gp.profile(organism='mmusculus', query=significant_proteins)

# Step 4: Define the background gene set (all proteins in your dataset)
all_proteins = df['Gene'].tolist()

# Step 5: Loop through each pathway in the enrichment results and perform Fisher's exact test
for result in results:  # 'results' is a list, so iterate over it
    pathway_name = result['name']  # Access pathway name
    pathway_genes = result['intersection']  # Access the intersecting genes
    
    # Print pathway name and intersecting genes for verification
    print(f"Pathway: {pathway_name}")
    print(f"Intersecting genes: {pathway_genes}")

    # Contingency table values for Fisher's Exact Test:
    a = len([gene for gene in significant_proteins if gene in pathway_genes])  # Significant and in pathway
    b = len(significant_proteins) - a  # Significant but not in pathway
    c = len([gene for gene in all_proteins if gene in pathway_genes]) - a  # Not significant and in pathway
    d = len(all_proteins) - (a + b + c)  # Not significant and not in pathway

    # Perform Fisher's Exact Test
    contingency_table = [[a, b], [c, d]]
    odds_ratio, p_value = fisher_exact(contingency_table)

    # Print the results for each pathway
    print(f"Fisher's Exact Test p-value: {p_value:.4f}, Odds ratio: {odds_ratio:.2f}\n")

# Step 6: Optionally, you can save significant pathways (p-value < 0.05) to a CSV
significant_pathways = [result for result in results if result['p_value'] < 0.05]
if significant_pathways:
    significant_df = pd.DataFrame(significant_pathways)
    significant_df.to_csv('/content/significant_pathways_mouse.csv', index=False)
    print("Significant pathways saved to CSV.")
