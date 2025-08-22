# Instagram Hashtag Post Scraper

This Python project scrapes Instagram posts based on specified hashtags using the Apify Instagram Hashtag Scraper API. It collects post details such as username, caption, likes, comments, hashtags, post URL, timestamp, and location, saving the data to a CSV file.

## Features

- Scrape Instagram posts by hashtags.
- Extract useful metadata including location from post captions.
- Save results into a timestamped CSV file for easy reference.

## Requirements

- Python 3.x
- `requests` library
- `pandas` library

Install the required packages using pip:

pip install requests pandas

## Setup

1. Obtain your `APIFY_TOKEN` and `SESSION_ID` from your Apify account.
2. For security, set your credentials as environment variables instead of hardcoding them:

### On Windows Command Prompt:

setx APIFY_TOKEN "your_apify_token_here"
setx SESSION_ID "your_session_id_here"

### On Linux/macOS Terminal:

export APIFY_TOKEN="your_apify_token_here"
export SESSION_ID="your_session_id_here"

3. Modify the script to read from environment variables (recommended) or insert your tokens directly (not recommended for security reasons).

## Usage

Run the scraper script:

python hashtag_post_scraper.py

The script scrapes posts for hashtags defined in the script (`hyderabadfoodie`, `indianfoodie` by default) and saves the output to a CSV file named like `hashtag_posts_YYYYMMDD_HHMMSS.csv`.

## Notes

- Make sure to have an active Apify account with access to the Instagram Hashtag Scraper actor.
- Usage of environment variables enhances security by keeping sensitive tokens out of your codebase.
- You can update the `HASHTAGS` list in the script to scrape posts from different hashtags.

## License

This project is open-source and free to use.

---
