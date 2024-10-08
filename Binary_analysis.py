import pandas as pd

# Load the log2-transformed data with metadata
file_path = '/content/Averaged_Log2_Transformed_Report.xlsx'
df = pd.read_excel(file_path)

# Define the sample groups
htt_samples = ['HTT1', 'HTT2', 'HTT3', 'HTT4', 'HTT5', 'HTT6', 'HTT7', 'HTT8', 'HTT9', 'HTT10']
wt_samples = ['WT1', 'WT2', 'WT3', 'WT4', 'WT5', 'WT6', 'WT7', 'WT8', 'WT9', 'WT10']

# Define male and female groups for WT and HTT
wt_male_samples = ['WT1', 'WT2', 'WT3', 'WT4', 'WT5']
wt_female_samples = ['WT6', 'WT7', 'WT8', 'WT9', 'WT10']
htt_male_samples = ['HTT1', 'HTT2', 'HTT3', 'HTT4', 'HTT5']
htt_female_samples = ['HTT6', 'HTT7', 'HTT8', 'HTT9', 'HTT10']

# Metadata columns (assuming first 4 columns are metadata)
metadata_columns = df.columns[:4]

# Step 1: Identify proteins only present in HTT or WT (at least 8 out of 10 samples)
df['HTT_presence'] = (df[htt_samples].notna().sum(axis=1) >= 8)  # Protein present in at least 8 HTT samples
df['WT_presence'] = (df[wt_samples].notna().sum(axis=1) >= 8)    # Protein present in at least 8 WT samples

# Proteins only in HTT or only in WT
only_htt = df[(df['HTT_presence']) & (~df['WT_presence'])].copy()
only_wt = df[(~df['HTT_presence']) & (df['WT_presence'])].copy()

# Include metadata columns in the output
only_htt = only_htt[metadata_columns.tolist() + htt_samples]
only_wt = only_wt[metadata_columns.tolist() + wt_samples]

# Step 2: Identify proteins only in male vs. female for WT and HTT (at least 3 out of 5 samples)
# WT: Proteins only in males or only in females
wt_male_only = df[(df[wt_male_samples].notna().sum(axis=1) >= 3) & (df[wt_female_samples].notna().sum(axis=1) == 0)].copy()
wt_female_only = df[(df[wt_female_samples].notna().sum(axis=1) >= 3) & (df[wt_male_samples].notna().sum(axis=1) == 0)].copy()

# HTT: Proteins only in males or only in females
htt_male_only = df[(df[htt_male_samples].notna().sum(axis=1) >= 3) & (df[htt_female_samples].notna().sum(axis=1) == 0)].copy()
htt_female_only = df[(df[htt_female_samples].notna().sum(axis=1) >= 3) & (df[htt_male_samples].notna().sum(axis=1) == 0)].copy()

# Include metadata columns in male/female outputs
wt_male_only = wt_male_only[metadata_columns.tolist() + wt_male_samples]
wt_female_only = wt_female_only[metadata_columns.tolist() + wt_female_samples]
htt_male_only = htt_male_only[metadata_columns.tolist() + htt_male_samples]
htt_female_only = htt_female_only[metadata_columns.tolist() + htt_female_samples]

# Step 3: Save the results to an Excel file
output_file = '/content/Proteins_Exclusive_HTT_WT_Male_Female.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    # Write HTT only and WT only proteins
    only_htt.to_excel(writer, sheet_name='HTT_Only', index=False)
    only_wt.to_excel(writer, sheet_name='WT_Only', index=False)
    
    # Write male vs female specific proteins for WT
    wt_male_only.to_excel(writer, sheet_name='WT_Male_Only', index=False)
    wt_female_only.to_excel(writer, sheet_name='WT_Female_Only', index=False)
    
    # Write male vs female specific proteins for HTT
    htt_male_only.to_excel(writer, sheet_name='HTT_Male_Only', index=False)
    htt_female_only.to_excel(writer, sheet_name='HTT_Female_Only', index=False)

print(f"Results saved to {output_file}")
