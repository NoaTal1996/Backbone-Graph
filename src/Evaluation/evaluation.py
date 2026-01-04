import random
import pandas as pd

# List of directories to check for top posts dataframes
directories = [
    "results/Labeled_Datasets/Ecuador/Ecuador_part_10/2025_12_23/topics_top_posts.parquet",
    "results/Labeled_Datasets/Ecuador/Ecuador_part_all/2025_12_23/topics_top_posts.parquet",
    "results/Labeled_Datasets/Ecuador/Ecuador_part_7/2025_12_23/topics_top_posts.parquet",
    "results/Labeled_Datasets/Ecuador/Ecuador_part_3/2025_12_23/topics_top_posts.parquet"
]

# List to hold the top posts dataframes

path_number  = 0 # Change this index to load different directories
df_path = directories[path_number]

top_post_df = pd.read_parquet(df_path)


top_post_df.head() 

top_post = []
topic = random.randint(0, len(top_post_df)-1)
print(f"Selected topic index: {topic}")
top_post_lst = top_post_df.iloc[topic].to_list()
print(f"Top posts for topic {topic}:")
for i, post in enumerate(top_post_lst, 1):
    print(f"{i}. {post}")