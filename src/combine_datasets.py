import pandas as pd
import glob
from pathlib import Path

# The main folder where all your country datasets live
base_dir = Path("/home/idanmu/Backbone-Graph/data/Labeled_Datasets")

# The exact names of the folders you want to process
# (I used "Ghana_Nigeria" based on the zip file you uploaded earlier)
countries = ["Armenia", "Bangladesh", "Catalonia", "Ghana_Nigeria"]

for country in countries:
    folder_path = base_dir / country
    
    # Check if the folder exists
    if not folder_path.exists():
        print(f"⚠️ Folder not found: {folder_path}")
        continue
        
    # Find all parquet files in this folder (ignoring any existing combined files)
    # Adjust the "*part*.parquet" if your files are named differently!
    file_pattern = str(folder_path / "*part*.parquet")
    parquet_files = glob.glob(file_pattern)
    
    if not parquet_files:
        print(f"⚠️ No 'part' files found in {country}")
        continue
        
    print(f"⏳ Combining {len(parquet_files)} files for {country}...")
    
    # Read and combine all files into one DataFrame
    df_list = [pd.read_parquet(file) for file in parquet_files]
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Define the output path
    output_name = f"{country}_combined.gzip.parquet"
    output_path = folder_path / output_name
    
    # Save the combined file with gzip compression
    combined_df.to_parquet(output_path, compression='gzip')
    
    print(f"✅ Saved! -> {output_path}")
    print(f"📊 Total rows in {country}: {len(combined_df)}\n")

print("🎉 All done! Ready for sbatch.")