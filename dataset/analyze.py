import os
import pandas as pd

dataset_path = r"d:\nanohack new proj\required\dataset"
csv_path = os.path.join(dataset_path, "updated_data.csv")

# 1. Directory-based counts (txt files)
dir_counts = {}
for root, dirs, files in os.walk(dataset_path):
    if root == dataset_path:
        continue
    folder_name = os.path.basename(root)
    txt_files = [f for f in files if f.endswith('.txt')]
    dir_counts[folder_name] = len(txt_files)

print("--- Statewise and Central Schemes (from directories) ---")
for k, v in sorted(dir_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{k.capitalize().replace('-', ' ')}: {v} schemes")

# 2. DataFrame analysis
print("\n--- CSV Analysis ---")
try:
    df = pd.read_csv(csv_path)
    print("Total records in CSV:", len(df))
    if 'level' in df.columns:
        print("\nBreakdown by Level:")
        print(df['level'].value_counts())
    if 'schemeCategory' in df.columns:
        print("\nTop 10 Categories:")
        print(df['schemeCategory'].value_counts().head(10))
except Exception as e:
    print("Could not read CSV:", e)
