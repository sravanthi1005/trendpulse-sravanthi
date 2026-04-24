
import requests
import time
import json
import os
from datetime import datetime

# headers
headers = {"User-Agent": "TrendPulse/1.0"}

# CATEGORIES for story Fetching
CATEGORIES = {
    "technology": ['AI', 'software', 'tech', 'code', 'computer', 'data', 'cloud', 'API', 'GPU', 'LLM', 'app', 'linux', 'programming'],
    "worldnews" : ['war', 'government', 'country', 'president', 'election', 'climate', 'attack', 'global', 'news', 'law', 'policy'],
    "sports": ['NFL', 'NBA', 'FIFA', 'sport', 'game', 'team', 'player', 'league', 'championship', 'football', 'soccer', 'olympics', 'racing'],
    "science" : ['research', 'study', 'space', 'physics', 'biology', 'discovery', 'NASA', 'genome', 'medical', 'health', 'nature', 'planet'],
    "entertainment" :['movie', 'film', 'music', 'Netflix', 'game', 'book', 'show', 'award', 'streaming', 'video', 'tv', 'art', 'culture']
}

def fetch_data():
    print("Fetching top stories list...")
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    try:
        ids = requests.get(url, headers=headers).json()[:500]
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return []
    
    collected = []
    # track of IDs we already added to avoid duplicates
    seen_ids = set()
    
    # --- PHASE 1: 
    for category, keywords in CATEGORIES.items():
        print(f"Scanning for {category}")
        count_for_this_cat = 0
        
        for story_id in ids:
            if count_for_this_cat >= 25 or len(collected) >= 122:
                break
            
            if story_id in seen_ids:
                continue
                
            try:
                res = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", headers=headers, timeout=10)
                data = res.json()

                if not data or "title" not in data or data.get("type") != "story":
                    continue

                title = data["title"].lower()
                
                # Keyword matching 
                match = any(word.lower() in title for word in keywords)
                
                if match:
                    story = {
                        "post_id": data.get("id"),
                        "title": data.get("title"),
                        "category": category,
                        "score" : data.get("score", 0),
                        "num_comments": data.get("descendants", 0),
                        "author" : data.get("by"),
                        "collected_at": datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                    }
                    collected.append(story)
                    seen_ids.add(story_id)
                    count_for_this_cat += 1
                    print(f" Added stories: {len(collected)}/122")

            except Exception:
                continue
        
        print(f"Completed {category}. Waiting 2 seconds...")
        time.sleep(2)

    # --- PHASE 2: Final Sweep (The "Emergency" fix to reach 122) ---
    if len(collected) < 122:
        print(f"Stories collecting: {len(collected)}. Starting fetching...")
        for story_id in ids:
            if len(collected) >= 122:
                break
            if story_id in seen_ids:
                continue
                
            try:
                res = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", headers=headers)
                data = res.json()
                
                if data and "title" in data and data.get("type") == "story":
                    story = {
                        "post_id": data.get("id"),
                        "title": data.get("title"),
                        "category": "technology", 
                        "score" : data.get("score", 0),
                        "num_comments": data.get("descendants", 0),
                        "author" : data.get("by"),
                        "collected_at": datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                    }
                    collected.append(story)
                    seen_ids.add(story_id)
                    print(f" Added stories (fetching): {len(collected)}/122")
            except:
                continue
            
    return collected

def save_json(data):
    os.makedirs("data", exist_ok=True)
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f"data/trends_{date_str}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Collected {len(data)} stories. Saved to {filename}")

if __name__ == "__main__":
    result = fetch_data()
    save_json(result)
    print("Fetching process is successful.")