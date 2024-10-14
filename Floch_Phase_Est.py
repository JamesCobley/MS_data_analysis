import gzip
import pandas as pd
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# Define Kyte-Doolittle hydrophobicity scale and solubility thresholds
valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")  # Standard 20 amino acids

# Function to compute the GRAVY score of a protein sequence
def compute_hydrophobicity(sequence):
    clean_sequence = ''.join([aa for aa in str(sequence) if aa in valid_amino_acids])
    if len(clean_sequence) == 0:
        return None  # Skip if no valid amino acids remain
    analysis = ProteinAnalysis(clean_sequence)
    return analysis.gravy()

# Function to classify the likely phase after centrifugation
def classify_phase(gravy_score):
    if gravy_score is None:
        return "Unknown"
    elif gravy_score < -0.5:
        return "Water Phase (Hydrophilic)"
    elif -0.5 <= gravy_score <= 0.5:
        return "Protein Disc (Amphipathic)"
    else:
        return "Lipid Phase (Hydrophobic)"

# Initialize lists to store protein details and phase classification
protein_list = []

# Open and parse the gzipped FASTA file
fasta_file = '/content/UP000000589_10090.fasta.gz'
total_proteins = 0
skipped_proteins = 0

with gzip.open(fasta_file, 'rt') as handle:
    for record in SeqIO.parse(handle, "fasta"):
        sequence = record.seq
        hydrophobicity = compute_hydrophobicity(sequence)
        
        if hydrophobicity is None:
            skipped_proteins += 1
            continue
        
        total_proteins += 1
        phase_class = classify_phase(hydrophobicity)
        
        # Append UniProt ID, protein name, GRAVY score, and phase classification
        protein_list.append([record.id, record.description.split()[1], hydrophobicity, phase_class])

# Create a DataFrame from the protein list
protein_df = pd.DataFrame(protein_list, columns=['UniProt ID', 'Protein Name', 'GRAVY Score', 'Phase Classification'])

# Save the DataFrame to an Excel file
output_file = '/content/protein_phase_estimation.xlsx'
protein_df.to_excel(output_file, index=False)

# Print summary
print(f"Total number of proteins detected: {total_proteins}")
print(f"Skipped proteins due to non-standard amino acids: {skipped_proteins}")
print(f"Phase classification saved to {output_file}")
