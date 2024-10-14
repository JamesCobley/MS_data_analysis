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
results = gp.profile(organism='mmusculus', query=significant_proteins)

# Step 4: Define the background gene set (all proteins in your dataset)
all_proteins = df['Gene'].tolist()

# Step 5: Print the first result to inspect the structure
print("Sample result structure:", results[0])  # Inspect the structure of the first result

# Step 6: Print all available keys in the first result to find where the intersecting genes are stored
print("Available keys in the first result:", results[0].keys())

# Step 7: Loop through each pathway in the enrichment results and perform Fisher's exact test
for result in results:
    pathway_name = result['name']  # Access pathway name
    
    # Print result to see available fields (including possibly the list of intersecting genes)
    print(f"Full pathway result: {result}")
