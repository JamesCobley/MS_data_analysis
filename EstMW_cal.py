import gzip
from Bio import SeqIO
import pandas as pd

# Function to estimate molecular weight from sequence length
def estimate_molecular_weight(sequence):
    avg_mass_per_residue = 110.0  # Average mass of an amino acid residue in Daltons
    return len(sequence) * avg_mass_per_residue

# Path to the FASTA file
fasta_file = '/content/UP000000589_10090.fasta.gz'

# Dictionary to store UniProt ID -> Estimated Molecular Weight
protein_mw = {}

# Parse the FASTA file and estimate molecular weights based on sequence length
with gzip.open(fasta_file, 'rt') as handle:
    for record in SeqIO.parse(handle, "fasta"):
        # Extract UniProt ID from FASTA header (assuming UniProt format)
        header_parts = record.id.split('|')
        if len(header_parts) >= 2:
            uniprot_id = header_parts[1]  # UniProt ID format
        else:
            uniprot_id = record.id  # Fallback if format differs

        sequence = record.seq
        estimated_weight = estimate_molecular_weight(sequence)
        protein_mw[uniprot_id] = estimated_weight

# Print summary
print(f"Estimated molecular weights for {len(protein_mw)} proteins.")

# Load the dataset with protein intensities
data_file = '/content/Averaged_Log2_Transformed_Report.xlsx'
df = pd.read_excel(data_file)

# Function to handle protein groups (X;X format)
def handle_protein_group(protein_ids, protein_mw_dict, strategy='average'):
    """
    Given a string of protein IDs separated by semicolons, look up the molecular weight for each,
    and return a single molecular weight based on the selected strategy (average, min, max).
    """
    ids = protein_ids.split(';')
    weights = [protein_mw_dict.get(pid.strip(), None) for pid in ids]
    weights = [w for w in weights if w is not None]  # Remove None values (unmatched IDs)

    if len(weights) == 0:
        return None  # No molecular weights found for this group

    if strategy == 'average':
        return sum(weights) / len(weights)
    elif strategy == 'max':
        return max(weights)
    elif strategy == 'min':
        return min(weights)
    else:
        return None

# Apply the handle_protein_group function to handle multiple protein IDs
# Assuming 'Report_HTT_James.pg_matrix' contains the protein IDs (potentially in X;X format)
df['Estimated_Molecular_Weight'] = df['Report_HTT_James.pg_matrix'].apply(
    lambda x: handle_protein_group(x, protein_mw, strategy='average')  # Use 'average', 'min', or 'max'
)

# Check for proteins without molecular weight (NaN) and handle if necessary
missing_mw = df['Estimated_Molecular_Weight'].isna().sum()
if missing_mw > 0:
    print(f"Warning: {missing_mw} proteins in the dataset do not have an estimated molecular weight.")
# Save the updated dataset with estimated molecular weights
output_file = '/content/dataset_with_estimated_molecular_weights.xlsx'
df.to_excel(output_file, index=False)

print(f"Dataset with estimated molecular weights saved to {output_file}")
