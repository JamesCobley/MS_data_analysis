import pandas as pd
import re

# Function to clean and extract core UniProt ID from the predicted data
def extract_uniprot_id(protein_id):
    # This regex captures the part of the UniProt ID after tr| or sp|, or uses the whole if no prefix
    match = re.match(r"(?:tr|sp)\|([^|]+)\|", protein_id)
    if match:
        return match.group(1)  # Return the part after tr| or sp|
    else:
        return protein_id  # Return as is if no prefix

# Load the predicted phase data from refined_protein_phase_estimation.xlsx
predicted_phase_file = '/content/refined_protein_phase_estimation.xlsx'
predicted_df = pd.read_excel(predicted_phase_file)

# Apply the function to clean up the UniProt ID in the predicted data
predicted_df['Clean UniProt ID'] = predicted_df['UniProt ID'].apply(extract_uniprot_id)

# Load the mass spectrometry output data (assuming a column 'Protein.Names' with multiple IDs separated by ;)
# Replace 'ms_output_file.xlsx' with the actual path to your MS output file
ms_output_file = '/content/ms_output_file.xlsx'
ms_df = pd.read_excel(ms_output_file)

# Function to check if any of the UniProt IDs in the MS entry matches the predicted IDs
def match_uniprot(ms_protein_names, predicted_uniprot_set):
    # Check if the entry is a string, if not (e.g., NaN), return False
    if isinstance(ms_protein_names, str):
        # Split the MS Protein.Names by semicolon (;) and check if any match the predicted IDs
        ms_ids = [entry.strip() for entry in ms_protein_names.split(';')]
        return any(ms_id in predicted_uniprot_set for ms_id in ms_ids)
    else:
        return False  # If not a valid string, no match

# Create a set of all Clean UniProt IDs from the predicted data for fast lookup
predicted_uniprot_set = set(predicted_df['Clean UniProt ID'])

# Add a 'Detected' column to the predicted_df indicating if the protein was detected in MS
predicted_df['Detected'] = predicted_df['Clean UniProt ID'].apply(lambda x: x in predicted_uniprot_set)

# Now check each MS entry and see if it contains a matching UniProt ID
ms_df['Matched'] = ms_df['Protein.Names'].apply(lambda names: match_uniprot(names, predicted_uniprot_set))

# Calculate the total number of predicted proteins per phase
total_phase_counts = predicted_df.groupby('Phase Classification').size()

# Calculate the number of proteins detected in MS per phase
detected_phase_counts = predicted_df[predicted_df['Detected'] == True].groupby('Phase Classification').size()

# Calculate the coverage for each phase
coverage = (detected_phase_counts / total_phase_counts) * 100

# Fill missing phases (where no proteins were detected) with 0% coverage
coverage = coverage.reindex(total_phase_counts.index, fill_value=0)

# Print the coverage for each phase
print("Protein coverage by phase (as detected in MS):")
for phase, cov in coverage.items():
    print(f"{phase}: {cov:.2f}% coverage ({detected_phase_counts.get(phase, 0)} out of {total_phase_counts[phase]} proteins detected)")

# Optionally, save the results to a new file
output_file = '/content/protein_phase_coverage.xlsx'
coverage_df = pd.DataFrame({
    'Phase Classification': total_phase_counts.index,
    'Total Predicted': total_phase_counts.values,
    'Detected in MS': detected_phase_counts.reindex(total_phase_counts.index, fill_value=0).values,
    'Coverage (%)': coverage.values
})
coverage_df.to_excel(output_file, index=False)

print(f"\nCoverage data saved to {output_file}")
