import gzip
import pandas as pd
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# Define Kyte-Doolittle hydrophobicity scale
hydrophobic_threshold = 0.5  # You can adjust this threshold based on the hydrophobicity definition
valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")  # Standard 20 amino acids

# Function to compute the average hydrophobicity of a protein sequence
def compute_hydrophobicity(sequence):
    # Filter out non-standard amino acids (optional: you can replace them with neutral values instead)
    clean_sequence = ''.join([aa for aa in str(sequence) if aa in valid_amino_acids])
    if len(clean_sequence) == 0:
        return None  # Skip if no valid amino acids remain
    analysis = ProteinAnalysis(clean_sequence)
    return analysis.gravy()  # GRAVY = Grand Average of Hydropathy

# Initialize an empty list to store hydrophobic proteins
hydrophobic_protein_list = []

# Open and parse the gzipped FASTA file
fasta_file = '/content/UP000000589_10090.fasta.gz'
hydrophobic_proteins = 0
total_proteins = 0
skipped_proteins = 0

with gzip.open(fasta_file, 'rt') as handle:
    for record in SeqIO.parse(handle, "fasta"):
        sequence = record.seq
        hydrophobicity = compute_hydrophobicity(sequence)
        
        if hydrophobicity is None:
            skipped_proteins += 1
            continue  # Skip this protein
        
        total_proteins += 1
        
        # Check if the protein is classified as hydrophobic based on the average hydrophobicity
        if hydrophobicity > hydrophobic_threshold:
            hydrophobic_proteins += 1
            # Append the UniProt ID, protein name (description), and GRAVY score to the list
            hydrophobic_protein_list.append([record.id, record.description.split()[1], hydrophobicity])

# Create a DataFrame from the hydrophobic protein list
hydrophobic_df = pd.DataFrame(hydrophobic_protein_list, columns=['UniProt ID', 'Protein Name', 'GRAVY Score'])

# Save the DataFrame to an Excel file
output_file = '/content/hydrophobic_proteins.xlsx'
hydrophobic_df.to_excel(output_file, index=False)

# Print the results and summary
print(f"Total number of proteins detected: {total_proteins}")
print(f"Number of hydrophobic proteins (GRAVY > {hydrophobic_threshold}): {hydrophobic_proteins}")
print(f"Skipped proteins due to non-standard amino acids: {skipped_proteins}")
print(f"Hydrophobic proteins saved to {output_file}")
