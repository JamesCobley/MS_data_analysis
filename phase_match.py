import pandas as pd
import re

# Function to clean and extract core UniProt ID from the predicted data
def extract_uniprot_id(protein_id):
    # This regex captures the part of the UniProt ID after tr| or sp|, or uses the whole if no prefix
    match = re.match(r"(?:tr|sp)\|([^|]+)\|", protein_id)
    if match:
        return match.group(1).lower()  # Return the part after tr| or sp|, converted to lowercase
    else:
        return protein_id.lower()  # Return as is if no prefix, converted to lowercase

# Load the predicted phase data from refined_protein_phase_estimation.xlsx
predicted_phase_file = '/content/refined_protein_phase_estimation.xlsx'
predicted_df = pd.read_excel(predicted_phase_file)

# Apply the function to clean up and lowercase the UniProt ID in the predicted data
predicted_df['Clean UniProt ID'] = predicted_df['UniProt ID'].apply(extract_uniprot_id)

# Load the mass spectrometry output data (assuming a column 'Protein.Names' with multiple IDs separated by ;)
# Replace 'ms_output_file.xlsx' with the actual path to your MS output file
ms_output_file = '/content/Report_HTT_James.xlsx'
ms_df = pd.read_excel(ms_output_file)

# Extract unique UniProt IDs from the MS output (handling multiple IDs separated by semicolons)
ms_detected_uniprot_ids = set()
for names in ms_df['Unnamed: 2'].dropna():  # Drop NaN values to avoid errors
    ms_ids = [entry.strip().lower() for entry in names.split(';')]  # Split multiple IDs and convert to lowercase
    ms_detected_uniprot_ids.update(ms_ids)  # Add to the set of unique detected IDs

# Function to check if a protein in the predicted data was detected in MS
def is_detected_in_ms(predicted_id):
    return predicted_id in ms_detected_uniprot_ids

# Add a 'Detected' column to the predicted_df indicating if the protein was detected in MS
predicted_df['Detected'] = predicted_df['Clean UniProt ID'].apply(is_detected_in_ms)

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
