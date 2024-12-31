import threading
import time
import requests
from datetime import datetime, timedelta
from .models import Video, APIKey
from django.utils.timezone import now

search_query = "cricket"

class FetchVideosThread(threading.Thread):
    def run(self):
        while True:
            try:
                print("Fetching videos...")
                # Fetch active keys from the database
                api_keys = APIKey.objects.filter(is_active=True).order_by('last_used')
                if not api_keys.exists():
                    print("No active API keys available. Retrying after 1 hour.")
                    time.sleep(3600)  # Wait 1 hour before retrying
                    continue

                for api_key in api_keys:
                    key = api_key.key
                    url = (
                        f"https://www.googleapis.com/youtube/v3/search?part=snippet"
                        f"&q={search_query}&type=video&order=date"
                        f"&key={key}"
                        f"&publishedAfter={(datetime.utcnow() - timedelta(minutes=10)).isoformat()}Z"
                    )
                    response = requests.get(url)

                    if response.status_code == 403:  # Quota exceeded
                        print(f"Quota exceeded for API key: {key}")
                        api_key.is_active = False
                        api_key.save()
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
                        api_key.last_used = now()
                        api_key.save()
                        break  # Break after successful fetch with a valid key
                    else:
                        print(f"Failed to fetch videos: {response.status_code}")

                # Reactivate all keys if it's a new day
                self.reactivate_keys_if_new_day()
            except Exception as e:
                print(f"Error in background fetcher: {e}")

            time.sleep(10)  # Wait 10 seconds before the next fetch

    def reactivate_keys_if_new_day(self):
        """Reactivate all keys if it's a new day."""
        if now().hour == 0:  # Check if it's midnight
            APIKey.objects.filter(is_active=False).update(is_active=True)
            print("Reactivated all API keys for the new day.")
