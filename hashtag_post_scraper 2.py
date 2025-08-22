import os
import requests
import time
import pandas as pd
from datetime import datetime
import re

def extract_location_from_caption(caption):
    if caption:
        match = re.search(r"📍\s*([^\n\r#]+)", caption)
        if match:
            return match.group(1).strip()
    return ""

class InstagramHashtagPostScraper:
    def __init__(self, apify_token, sessionid):
        self.apify_token = apify_token
        self.sessionid = sessionid
        self.base_url = "https://api.apify.com/v2"

    def scrape_posts_by_hashtags(self, hashtags, results_limit=30):
        run_input = {
            "hashtags": hashtags,
            "resultsLimit": results_limit,
            "instagramScraperSessionId": self.sessionid,
            "proxy": {"useApifyProxy": True}
        }

        print(f"Scraping hashtags: {', '.join(hashtags)}")

        try:
            response = requests.post(
                f"{self.base_url}/acts/apify%2Finstagram-hashtag-scraper/runs",
                params={"token": self.apify_token},
                json=run_input,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to start hashtag scraper: {e}")
            return []

        run_id = response.json()["data"]["id"]
        print(f"Hashtag scraper started with run ID: {run_id}")
        return self._wait_for_results(run_id)

    def _wait_for_results(self, run_id):
        while True:
            try:
                status_response = requests.get(
                    f"{self.base_url}/actor-runs/{run_id}",
                    params={"token": self.apify_token}
                )
                status_response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to check status: {e}")
                return []

            status = status_response.json()["data"]["status"]
            if status == "SUCCEEDED":
                break
            elif status in ["FAILED", "ABORTED"]:
                print(f"Run failed with status: {status}")
                return []
            else:
                print(f"Status: {status}... waiting")
                time.sleep(10)

        dataset_id = status_response.json()["data"]["defaultDatasetId"]

        try:
            dataset_response = requests.get(
                f"{self.base_url}/datasets/{dataset_id}/items",
                params={"token": self.apify_token, "format": "json"}
            )
            dataset_response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch dataset: {e}")
            return []

        return dataset_response.json()

    def save_posts_to_csv(self, data, filename=None):
        if not filename:
            filename = f"hashtag_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        if not data:
            print("No data to save.")
            return

        posts = []
        for item in data:
            caption = item.get("caption", "")
            posts.append({
                "username": item.get("ownerUsername"),
                "caption": caption,
                "likes": item.get("likesCount"),
                "comments": item.get("commentsCount"),
                "hashtags": ", ".join(item.get("hashtags", [])),
                "post_url": item.get("url"),
                "timestamp": item.get("timestamp"),
                "location": extract_location_from_caption(caption)
            })

        df = pd.DataFrame(posts)
        df.to_csv(filename, index=False)
        print(f"Post data saved to {filename}")
        print(f"Total posts saved: {len(df)}")

def main():
    APIFY_TOKEN = os.getenv("APIFY_TOKEN")
    SESSION_ID = os.getenv("SESSION_ID")

    if not APIFY_TOKEN or not SESSION_ID:
        print("Error: APIFY_TOKEN and SESSION_ID must be set as environment variables.")
        return

    HASHTAGS = ["hyderabadfoodie", "indianfoodie"]

    scraper = InstagramHashtagPostScraper(APIFY_TOKEN, SESSION_ID)
    post_data = scraper.scrape_posts_by_hashtags(HASHTAGS)

    if post_data:
        print("Sample keys in each item:")
        print(post_data[0].keys())

        print("Sample post data:")
        print(post_data)

        scraper.save_posts_to_csv(post_data)
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()
