import threading
import time
import requests
from datetime import datetime, timedelta
from .models import Video

API_KEYS = ['']  # Add your API keys
search_query = "cricket"
api_key_index = 0 # To cycle through keys

class FetchVideosThread(threading.Thread):
    def run(self):
        global api_key_index
        exhausted_keys = set()  # Track exhausted API keys

        while True:
            try:
                # Check if all keys are exhausted
                if len(exhausted_keys) == len(API_KEYS):
                    print("All API keys exhausted. Pausing for 1 hour...")
                    time.sleep(3600)  # Pause for 1 hour
                    exhausted_keys.clear()  # Reset the exhausted keys tracker

                print("Fetching videos...")
                key = API_KEYS[api_key_index]
                url = (
                    f"https://www.googleapis.com/youtube/v3/search?part=snippet"
                    f"&q={search_query}&type=video&order=date"
                    f"&key={key}"
                    f"&publishedAfter={(datetime.utcnow() - timedelta(minutes=10)).isoformat()}Z"
                )
                response = requests.get(url)

                # Handle API quota exhausted
                if response.status_code == 403:  # Quota exceeded
                    exhausted_keys.add(key)  # Mark the key as exhausted
                    api_key_index = (api_key_index + 1) % len(API_KEYS)
                    print(f"API key exhausted. Switching to key: {API_KEYS[api_key_index]}")
                    continue

                if response.status_code == 200:
                    data = response.json()
                    for item in data.get("items", []):
                        snippet = item["snippet"]
                        Video.objects.update_or_create(
                            video_id=item["id"]["videoId"],
                            defaults={
                                "title": snippet["title"],
                                "description": snippet["description"],
                                "published_at": snippet["publishedAt"],
                                "thumbnail_url": snippet["thumbnails"]["default"]["url"],
                            },
                        )
                else:
                    print(f"Failed to fetch videos: {response.status_code}")
            except Exception as e:
                print(f"Error in background fetcher: {e}")

            time.sleep(10)  # Wait 10 seconds before the next fetch