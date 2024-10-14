from gprofiler import GProfiler
import pandas as pd

# Step 1: Load your dataset containing genes or proteins
file_path = '/content/your_dataset.xlsx'  # Adjust this to your actual file
df = pd.read_excel(file_path)

# Assume 'Gene' is the column with the gene symbols
genes_of_interest = df['Gene'].tolist()

# Step 2: Initialize g:Profiler and query pathways
gp = GProfiler(return_dataframe=True)

# Step 3: Run g:Profiler for pathway enrichment (KEGG, Reactome, etc.)
results = gp.profile(organism='hsapiens', query=genes_of_interest)

# Step 4: Filter results for specific pathway of interest (e.g., 'KEGG')
specific_pathway = results[results['source'] == 'KEGG']

# You can also search for specific pathways by name:
pathway_of_interest = specific_pathway[specific_pathway['name'].str.contains('MAPK signaling pathway')]

# Step 5: Determine representation
pathway_gene_count = pathway_of_interest['intersection_size'].values[0]
total_genes_in_pathway = pathway_of_interest['effective_domain_size'].values[0]

# Calculate relative representation
representation = pathway_gene_count / total_genes_in_pathway
print(f"Representation of the pathway: {representation:.2%}")

# Optional: Save the results to a CSV for further inspection
results.to_csv('/content/pathway_enrichment_results.csv', index=False)
