import os
import pandas as pd

dataset_path = r"d:\nanohack new proj\required\dataset"
csv_path = os.path.join(dataset_path, "updated_data.csv")
tn_csv_path = os.path.join(dataset_path, "tamilnadu_data.csv")
tn_dir = os.path.join(dataset_path, "tamilnadu")

# Read main dataset
try:
    df = pd.read_csv(csv_path)
    
    # Filter rows mentioning 'tamil nadu' or 'tamilnadu'
    # We can check several text columns
    text_cols = ['scheme_name', 'details', 'eligibility', 'application', 'tags']
    mask = pd.Series([False] * len(df))
    
    for col in text_cols:
        if col in df.columns:
            # fillna first, then use str.contains
            mask = mask | df[col].fillna('').str.contains('Tamil Nadu|Tamilnadu|TamilNadu', case=False)
            
    tn_df = df[mask]
    tn_df.to_csv(tn_csv_path, index=False)
    
    print(f"Extracted {len(tn_df)} records for Tamil Nadu to {tn_csv_path}")
    
    if 'schemeCategory' in tn_df.columns:
        print("\nTop Tamil Nadu Scheme Categories:")
        print(tn_df['schemeCategory'].value_counts().head(5))
except Exception as e:
    print("Error processing CSV:", e)

# Count txt files in tamilnadu dir
if os.path.isdir(tn_dir):
    txt_files = [f for f in os.listdir(tn_dir) if f.endswith('.txt')]
    print(f"\nFound {len(txt_files)} text document(s) in the 'tamilnadu' folder.")
else:
    print(f"Directory {tn_dir} not found.")
