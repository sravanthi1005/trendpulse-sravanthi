#task3_analysis.py

import pandas as pd
import numpy as np

# --- 1. Load and Explore ---
df = pd.read_csv("data/trends_clean.csv")

# Loaded data

print(f"Loaded data: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())

# Calculate verages (Pandas)
avg_score = df['score'].mean()
avg_comments = df['num_comments'].mean()

# Formatting 
print(f"\nAverage score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

# --- 2. Basic Analysis with NumPy ---
print("\n--- NumPy Stats ---")

scores = df['score'].to_numpy()
comments = df['num_comments'].to_numpy()

print(f"Mean score   : {np.mean(scores):,.0f}")
print(f"Median score : {np.median(scores):,.0f}")
print(f"Std deviation: {np.std(scores):,.0f}")
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Which category has the most stories?
categories, counts = np.unique(df['category'].values, return_counts=True)
top_idx = np.argmax(counts)
print(f"\nMost stories in: {categories[top_idx]} ({counts[top_idx]} stories)")

# Which story has the most comments?
max_comm_idx = np.argmax(comments)
top_title = df.iloc[max_comm_idx]['title']
top_count = comments[max_comm_idx]
print(f"Most commented story: \"{top_title}\" — {top_count} comments")

# --- 3. Add New Columns ---
df['engagement'] = df['num_comments'] / (df['score'] + 1)
df['is_popular'] = df['score'] > avg_score

# --- 4. Save and Final Message ---
output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)
print(f"\nSaved to {output_path}")