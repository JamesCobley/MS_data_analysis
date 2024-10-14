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

# Function to process and print pathway results
def display_pathway_results(results):
    for result in results:
        print(f"Pathway Name: {result.get('name')}")
        print(f"  Description: {result.get('description')}")
        print(f"  Source: {result.get('source')} ({result.get('native')})")
        print(f"  Effective Domain Size: {result.get('effective_domain_size')}")
        print(f"  Term Size: {result.get('term_size')}")
        print(f"  Query Size: {result.get('query_size')}")
        print(f"  Intersection Size: {result.get('intersection_size')}")
        print(f"  P-Value: {result.get('p_value'):.2e}")
        print(f"  Precision: {result.get('precision'):.2f}")
        print(f"  Recall: {result.get('recall'):.2f}")
        print(f"  Significant: {result.get('significant')}")
        print(f"  Parent Pathways: {', '.join(result.get('parents', []))}")
        print("-" * 50)  # Just to separate the entries for readability

# Display all the results
display_pathway_results(results)

# Create a DataFrame from the results for output to Excel
def create_dataframe_from_results(results):
    # Flatten the results to prepare for DataFrame
    data = []
    for result in results:
        data.append({
            'Pathway Name': result.get('name'),
            'Description': result.get('description'),
            'Source': result.get('source'),
            'Native': result.get('native'),
            'Effective Domain Size': result.get('effective_domain_size'),
            'Term Size': result.get('term_size'),
            'Query Size': result.get('query_size'),
            'Intersection Size': result.get('intersection_size'),
            'P-Value': result.get('p_value'),
            'Precision': result.get('precision'),
            'Recall': result.get('recall'),
            'Significant': result.get('significant'),
            'Parent Pathways': ', '.join(result.get('parents', []))
        })

    # Create the DataFrame
    df = pd.DataFrame(data)
    return df

# Create the DataFrame
df_results = create_dataframe_from_results(results)

# Output DataFrame to an Excel file
output_file = "pathway_results.xlsx"
df_results.to_excel(output_file, index=False)

print(f"Results successfully written to {output_file}")
