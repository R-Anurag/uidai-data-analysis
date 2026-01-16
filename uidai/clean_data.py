import pandas as pd
import os

# List of CSV files to clean
csv_files = [
    'Merged_Aadhar_demographic.csv',
    'merged_aadhar_biometric.csv',
    'merged_enrollement.csv'
]

def clean_column_names(df):
    """
    Convert column names to lowercase and remove spaces
    """
    df.columns = df.columns.str.lower().str.replace(' ', '_', regex=False)
    return df

# Process each file
for file in csv_files:
    if os.path.exists(file):
        print(f"\nProcessing {file}...")
        
        # Read the CSV file
        df = pd.read_csv(file)
        
        # Show original column names
        print(f"Original columns ({len(df.columns)}): {df.columns.tolist()[:10]}...")
        
        # Clean column names
        df = clean_column_names(df)
        
        # Show cleaned column names
        print(f"Cleaned columns: {df.columns.tolist()[:10]}...")
        
        # Save the cleaned data (overwrite original or create new file)
        output_file = f"cleaned_{file}"
        df.to_csv(output_file, index=False)
        
        print(f"✓ Saved cleaned data to {output_file}")
        print(f"  Rows: {len(df):,}, Columns: {len(df.columns)}")
    else:
        print(f"⚠ File not found: {file}")

print("\n✓ Data cleaning completed!")
