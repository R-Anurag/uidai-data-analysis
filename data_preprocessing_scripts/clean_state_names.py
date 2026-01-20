"""
State Name Cleaning and Standardization Script for UIDAI Data

This script standardizes state names across all UIDAI datasets by:
1. Converting to lowercase and removing extra spaces
2. Handling common typos and variations
3. Mapping old/legacy state names to current official names
4. Ensuring consistency across enrollment, demographic, and biometric data

Author: Data Preprocessing Team
Date: 2026-01-20
"""

import pandas as pd
import sys

# ============================================================================
# OFFICIAL STATE NAME MAPPING
# ============================================================================
# Maps variations, typos, and old names to the current official state names
# All names are in lowercase for case-insensitive matching

STATE_NAME_MAP = {
    # ----- Current Official Names (normalized) -----
    "andaman and nicobar islands": "andaman and nicobar islands",
    "andhra pradesh": "andhra pradesh",
    "arunachal pradesh": "arunachal pradesh",
    "assam": "assam",
    "bihar": "bihar",
    "chandigarh": "chandigarh",
    "chhattisgarh": "chhattisgarh",
    "dadra and nagar haveli and daman and diu": "dadra and nagar haveli and daman and diu",
    "delhi": "delhi",
    "goa": "goa",
    "gujarat": "gujarat",
    "haryana": "haryana",
    "himachal pradesh": "himachal pradesh",
    "jammu and kashmir": "jammu and kashmir",
    "jharkhand": "jharkhand",
    "karnataka": "karnataka",
    "kerala": "kerala",
    "ladakh": "ladakh",
    "lakshadweep": "lakshadweep",
    "madhya pradesh": "madhya pradesh",
    "maharashtra": "maharashtra",
    "manipur": "manipur",
    "meghalaya": "meghalaya",
    "mizoram": "mizoram",
    "nagaland": "nagaland",
    "odisha": "odisha",
    "puducherry": "puducherry",
    "punjab": "punjab",
    "rajasthan": "rajasthan",
    "sikkim": "sikkim",
    "tamil nadu": "tamil nadu",
    "telangana": "telangana",
    "tripura": "tripura",
    "uttar pradesh": "uttar pradesh",
    "uttarakhand": "uttarakhand",
    "west bengal": "west bengal",
    
    # ----- Common Variations & Typos -----
    
    # Andaman & Nicobar Islands
    "andaman & nicobar islands": "andaman and nicobar islands",
    "andaman & nicobar": "andaman and nicobar islands",
    "andaman and nicobar": "andaman and nicobar islands",
    "a & n islands": "andaman and nicobar islands",
    "a&n islands": "andaman and nicobar islands",
    
    # Delhi variations
    "nct of delhi": "delhi",
    "new delhi": "delhi",
    "national capital territory of delhi": "delhi",
    
    # Chhattisgarh variations
    "chattisgarh": "chhattisgarh",
    "chhatisgarh": "chhattisgarh",
    
    # Dadra & Nagar Haveli and Daman & Diu (merged UTs)
    "dadra and nagar haveli": "dadra and nagar haveli and daman and diu",
    "dadra & nagar haveli": "dadra and nagar haveli and daman and diu",
    "dnh": "dadra and nagar haveli and daman and diu",
    "daman and diu": "dadra and nagar haveli and daman and diu",
    "daman & diu": "dadra and nagar haveli and daman and diu",
    "diu": "dadra and nagar haveli and daman and diu",
    "daman": "dadra and nagar haveli and daman and diu",
    
    # Jammu & Kashmir
    "jammu & kashmir": "jammu and kashmir",
    "j&k": "jammu and kashmir",
    "j & k": "jammu and kashmir",
    
    # Odisha (formerly Orissa)
    "orissa": "odisha",
    
    # Puducherry (formerly Pondicherry)
    "pondicherry": "puducherry",
    "pondy": "puducherry",
    
    # Tamil Nadu
    "tamilnadu": "tamil nadu",
    "tn": "tamil nadu",
    
    # Uttar Pradesh
    "uttarpradesh": "uttar pradesh",
    "up": "uttar pradesh",
    "u.p.": "uttar pradesh",
    
    # Uttarakhand (formerly Uttaranchal)
    "uttaranchal": "uttarakhand",
    
    # West Bengal
    "westbengal": "west bengal",
    "w.b.": "west bengal",
    "wb": "west bengal",
    
    # Madhya Pradesh
    "madhyapradesh": "madhya pradesh",
    "mp": "madhya pradesh",
    "m.p.": "madhya pradesh",
    
    # Himachal Pradesh
    "himachalpradesh": "himachal pradesh",
    "hp": "himachal pradesh",
    "h.p.": "himachal pradesh",
    
    # Arunachal Pradesh
    "arunachalpradesh": "arunachal pradesh",
    
    # Andhra Pradesh
    "andhrapradesh": "andhra pradesh",
    "ap": "andhra pradesh",
    
    # Lakshadweep
    "laccadive": "lakshadweep",
    "lakshadweep islands": "lakshadweep",
}


def clean_state_name(state_value):
    """
    Clean and standardize a single state name.
    
    Args:
        state_value: String or any value representing a state name
        
    Returns:
        Standardized state name in lowercase, or 'INVALID_STATE' if not recognized
    """
    if pd.isna(state_value):
        return "INVALID_STATE"
    
    # Convert to string and lowercase
    state_clean = str(state_value).strip().lower()
    
    # Remove extra whitespace
    state_clean = ' '.join(state_clean.split())
    
    # Remove special characters except & and -
    state_clean = state_clean.replace('&', 'and')
    
    # Look up in mapping
    if state_clean in STATE_NAME_MAP:
        return STATE_NAME_MAP[state_clean]
    
    # If not found, return as invalid
    print(f" Warning: Unrecognized state name: '{state_value}' (cleaned: '{state_clean}')")
    return "INVALID_STATE"


def clean_state_column(df, column_name='state'):
    """
    Clean the state column in a DataFrame.
    
    Args:
        df: pandas DataFrame
        column_name: Name of the state column (default: 'state')
        
    Returns:
        DataFrame with cleaned state column
    """
    print(f"\n{'='*80}")
    print(f"Cleaning state names in column: '{column_name}'")
    print(f"{'='*80}")
    
    # Get original state counts
    original_states = df[column_name].value_counts()
    print(f"\nOriginal: {len(original_states)} unique states")
    print(f"Total rows: {len(df):,}")
    
    # Apply cleaning
    df[column_name] = df[column_name].apply(clean_state_name)
    
    # Get cleaned state counts
    cleaned_states = df[column_name].value_counts()
    print(f"\nAfter cleaning: {len(cleaned_states)} unique states")
    
    # Check for invalid states
    invalid_count = (df[column_name] == 'INVALID_STATE').sum()
    if invalid_count > 0:
        print(f"\n⚠ WARNING: {invalid_count:,} rows have INVALID_STATE")
        print("\nInvalid state examples:")
        invalid_samples = df[df[column_name] == 'INVALID_STATE'][column_name].head(10)
        for sample in invalid_samples:
            print(f"  - {sample}")
    else:
        print("\n✓ All states successfully standardized!")
    
    # Show cleaned state distribution
    print(f"\n{'='*80}")
    print("Cleaned State Distribution:")
    print(f"{'='*80}")
    for state, count in cleaned_states.items():
        print(f"  {state:45} : {count:>10,} rows")
    
    return df


def process_csv_file(input_file, output_file=None, state_column='state'):
    """
    Process a CSV file to clean state names.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file (if None, will overwrite input)
        state_column: Name of the state column
    """
    print(f"\n{'#'*80}")
    print(f"Processing file: {input_file}")
    print(f"{'#'*80}")
    
    # Load data
    print("\nLoading data...")
    df = pd.read_csv(input_file)
    print(f"✓ Loaded {len(df):,} rows, {len(df.columns)} columns")
    
    # Clean state column
    df = clean_state_column(df, state_column)
    
    # Determine output file
    if output_file is None:
        # Create backup
        backup_file = input_file.replace('.csv', '_BACKUP.csv')
        print(f"\n Creating backup: {backup_file}")
        df_original = pd.read_csv(input_file)
        df_original.to_csv(backup_file, index=False)
        output_file = input_file
    
    # Save cleaned data
    print(f"\n Saving cleaned data to: {output_file}")
    df.to_csv(output_file, index=False)
    print(f"✓ Successfully saved {len(df):,} rows")
    
    return df


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print(f"\n{'#'*80}")
    print("UIDAI STATE NAME CLEANING SCRIPT")
    print(f"{'#'*80}\n")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        # Process specific file
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        process_csv_file(input_file, output_file)
    else:
        # Process all three main datasets
        files_to_process = [
            ('data/enrollment.csv', 'data/enrollment_cleaned_states.csv'),
            ('data/demographic.csv', 'data/demographic_cleaned_states.csv'),
            ('data/biometric.csv', 'data/biometric_cleaned_states.csv'),
        ]
        
        print("Processing all UIDAI datasets...\n")
        
        for input_file, output_file in files_to_process:
            try:
                process_csv_file(input_file, output_file)
            except FileNotFoundError:
                print(f"\nWarning: File not found: {input_file}")
            except Exception as e:
                print(f"\n Error processing {input_file}: {str(e)}")
        
        print(f"\n{'#'*80}")
        print("✓ ALL PROCESSING COMPLETE!")
        print(f"{'#'*80}\n")
        print("\nCleaned files created:")
        for _, output_file in files_to_process:
            print(f"  - {output_file}")
        
        print("\n Next steps:")
        print("  1. Review the cleaned files")
        print("  2. Check for any INVALID_STATE entries")
        print("  3. Replace original files if satisfied with cleaning")
