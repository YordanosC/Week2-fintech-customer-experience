from google_play_scraper import reviews, Sort
import csv
import os
from datetime import datetime

# App IDs for each bank
app_ids = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.cr2.amolelight'
}

# Bank full names for display
bank_full_names = {
    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia',
    'Dashen': 'Dashen Bank'
}

# Directory to save data
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(data_dir, exist_ok=True)

def scrape_reviews(app_id, bank_name, filename):
    print(f"Scraping reviews for {bank_name}...")
    try:
        result, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=500
        )
        print(f"Fetched {len(result)} reviews for {bank_name}")

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['review_text', 'rating', 'date', 'bank_name', 'source'])
            writer.writeheader()
            for r in result:
                writer.writerow({
                    'review_text': r['content'],
                    'rating': r['score'],
                    'date': r['at'].strftime('%Y-%m-%d'),
                    'bank_name': bank_name,
                    'source': 'Google Play'
                })
        print(f"Saved reviews to {filename}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    for bank_key, app_id in app_ids.items():
        filename = os.path.join(data_dir, f"{bank_key}_reviews_{date_str}.csv")
        bank_name = bank_full_names[bank_key]
        scrape_reviews(app_id, bank_name, filename)