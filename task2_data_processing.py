
import pandas as pd
import os
from datetime import datetime

# 1. Define the filename (Task 1 file date)
filename = "data/trends_20260422.json"

# Task 1:.....#### Loading the JSON file ###......
if os.path.exists(filename):
    df = pd.read_json(filename)
    
    print(f"Loaded {len(df)} stories from {filename}") 
else:
    print(f"Error: {filename} not found. Check your task1 file.")
    exit() 

# Task 2:...... Cleaning the Data.......!

# 1. Removing Duplicates 
df = df.drop_duplicates(subset=['post_id'])
print(f"After removing duplicates: {len(df)}")

# 2. Removing Null values

df = df.dropna(subset=['post_id', 'title', 'score'])
print(f"After removing nulls: {len(df)}")

# 3. Removing Low quality stories

df = df[df['score'] >= 5]
print(f"After removing low scores: {len(df)}")

# 4. Removing Whitespace 

df['title'] = df['title'].str.strip()

# Convert types to integer
df['score'] = df['score'].astype(int)
df['num_comments'] = df['num_comments'].astype(int)

# Task 3: ..........Saving data.......!

# # saving data
clean_df = 'data/trends_clean.csv'
df.to_csv(clean_df, index=False)

# Saving Confirmation 
print(f"Saved {len(df)} rows to {clean_df}")

# Quick summary: stories per category
print("\nStories per category:")
print(df['category'].value_counts().to_string())

