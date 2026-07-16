import pandas as pd
import glob
import re
from pathlib import Path

base_dir = Path("/home/idanmu/Backbone-Graph/data/Labeled_Datasets")
output_dir = Path("/home/idanmu/Backbone-Graph/results/labeled_datasets")

countries = sorted([
    p.name for p in base_dir.iterdir()
    if p.is_dir() and p.name != "to_insert"
])
print(f"Found {len(countries)} datasets: {countries}\n")

FILES_PER_CHUNK = 30

def part_number(filepath):
    m = re.search(r'(\d+)(?=\.gzip\.parquet)', Path(filepath).name)
    return int(m.group(1)) if m else 0

for country in countries:
    folder_path = base_dir / country
    out_folder = output_dir / country
    out_folder.mkdir(parents=True, exist_ok=True)

    all_parquets = glob.glob(str(folder_path / "*.parquet"))
    parquet_files = sorted(
        [f for f in all_parquets if "combined" not in Path(f).name and "part_all" not in Path(f).name],
        key=part_number
    )

    if not parquet_files:
        print(f"⚠️  No source parquet files found in {country}, skipping.")
        continue

    n_files = len(parquet_files)
    n_chunks = max(1, -(-n_files // FILES_PER_CHUNK))  # ceil division
    print(f"⏳ [{country}] Reading {n_files} files...")

    frames = []
    skipped = 0
    for f in parquet_files:
        try:
            frames.append(pd.read_parquet(f))
        except Exception as e:
            print(f"  ⚠️  Skipping corrupted file: {Path(f).name} ({e})")
            skipped += 1

    if not frames:
        print(f"  ❌ All files corrupted in {country}, skipping.\n")
        continue
    if skipped:
        print(f"  ℹ️  {skipped}/{n_files} files skipped.")

    df = pd.concat(frames, ignore_index=True)

    if "post_time" in df.columns:
        df = df.sort_values("post_time").reset_index(drop=True)

    print(f"  Sorted. Saving {n_chunks} combined output(s)...")

    chunk_size = -(-len(df) // n_chunks)  # ceil division
    for chunk_idx in range(n_chunks):
        chunk = df.iloc[chunk_idx * chunk_size:(chunk_idx + 1) * chunk_size]

        if n_chunks == 1:
            out_path = out_folder / f"{country}_combined.gzip.parquet"
        else:
            out_path = out_folder / f"{country}_combined_part_{chunk_idx + 1}.gzip.parquet"

        chunk.to_parquet(out_path, compression="gzip")
        print(f"  ✅ Part {chunk_idx + 1}/{n_chunks} -> {out_path.name}  ({len(chunk):,} rows)")

    print()

print("🎉 All done!")
