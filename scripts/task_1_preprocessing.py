import pandas as pd
import glob
import os
from transformers import pipeline

# Path to data folder
data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')

# Pattern to match all review CSV files
file_paths = glob.glob(os.path.join(data_folder, '*_reviews_*.csv'))

# Read and concatenate all dataframes
all_dfs = []
for fp in file_paths:
    df = pd.read_csv(fp)
    all_dfs.append(df)

if not all_dfs:
    print("No review files found. Please run the scraper first.")
    exit()

all_reviews = pd.concat(all_dfs, ignore_index=True)

# Remove duplicates
all_reviews.drop_duplicates(subset=['review_text'], inplace=True)

# Remove missing reviews
all_reviews.dropna(subset=['review_text'], inplace=True)

# Format date
all_reviews['date'] = pd.to_datetime(all_reviews['date'], errors='coerce')
all_reviews['date'] = all_reviews['date'].dt.strftime('%Y-%m-%d')

# Sentiment analysis
sentiment_pipeline = pipeline("sentiment-analysis")

# Get sentiments
sentiments = sentiment_pipeline(all_reviews['review_text'].tolist())

# Add sentiment columns
all_reviews['sentiment_label'] = [s['label'] for s in sentiments]
all_reviews['sentiment_score'] = [s['score'] for s in sentiments]

# Save cleaned data with sentiment
output_path = os.path.join(data_folder, 'reviews_with_sentiment.csv')
all_reviews.to_csv(output_path, index=False)

print(f"Preprocessing and sentiment analysis completed. Saved to {output_path}")