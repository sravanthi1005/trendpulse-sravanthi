
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. Setup ---
# Load the data from Task 3
if os.path.exists("data/trends_analysed.csv"):
    df = pd.read_csv("data/trends_analysed.csv")
    print(f"Successfully loaded data")
else:
    print("Error: file not found!")
    exit()

# Create the outputs folder if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# --- 2. Chart 1: Top 10 Stories by Score ---
plt.figure(figsize=(10, 6))
# Sort by score and take the top 10
top_10_stories = df.sort_values(by='score', ascending=False).head(10)

# Use the story title on the y-axis (shorten titles longer than 50 characters)
short_titles_list = []
for titles in top_10_stories['title']:
     if len(titles) > 50:
        clean_name = titles[:50] 
        short_titles_list.append(clean_name)
        print(f"Shortened: {clean_name}")
     else:
        short_titles_list.append(titles)
        print(f"Unchanged: {titles}")


plt.barh(short_titles_list, top_10_stories['score'], color='skyblue')
plt.gca().invert_yaxis()  
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.show()

# 3. # Chart 2:$-----Stories per Category ---$
plt.figure(figsize=(8, 6))
cat_counts = df['category'].value_counts()
colors = ['blue','pink' 'red', 'green', 'orange', 'purple']

plt.bar(cat_counts.index, cat_counts.values)
plt.title("Number of Stories per Category")
plt.xlabel("Category")
plt.ylabel("Story Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.show()


# --- 4. Chart 3: Create a scatter plot with score on the x-axis and num_comments on the y-axis ---
plt.figure(figsize=(8, 6))
# Filter data for the legend
popular = df[df['is_popular'] == True]
not_popular = df[df['is_popular'] == False]

plt.scatter(popular['score'], popular['num_comments'], color='gold', label='Popular', alpha=0.7)
plt.scatter(not_popular['score'], not_popular['num_comments'], color='gray', label='Not Popular', alpha=0.5)

plt.title("Score vs Number of Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.show()

# Defining popular
popular = df[df['score'] >= 100]
not_popular = df[df['score'] < 100]

# Combine all 3 charts into one figure:
# --- Bonus: Dashboard ---

fig, axs = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle("TrendPulse Dashboard", fontsize=20)
print("Trendpulse Dashboard working")

# Dashboard - Top Stories (Top Left)
axs[0, 0].barh(short_titles_list, top_10_stories['score'], color='blue')
axs[0, 0].invert_yaxis()
axs[0, 0].set_title("Top 10 Stories")
print("Top left stories working")

# Dashboard - Categories (Top Right)
axs[0, 1].bar(cat_counts.index, cat_counts.values, color='teal')
axs[0, 1].set_title("Category Distribution")
print("Top right categories working")

# Dashboard - Scatter (Bottom Left)
axs[1, 0].scatter(popular['score'], popular['num_comments'], color='red', alpha=0.7)
axs[1, 0].scatter(not_popular['score'], not_popular['num_comments'], color='green', alpha=0.5)
axs[1, 0].set_title("Score vs Comments")
print("scatter botton left working")

# Remove the empty 4th subplot (Bottom Right)
# Delete Axis-- removes that specific empty box entirely.
fig.delaxes(axs[1, 1]) 
print("delete axis is working")

# For protecting the overlapping
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("outputs/dashboard.png")
plt.show()

print("Visualization complete! Check the 'outputs' folder .")






     


