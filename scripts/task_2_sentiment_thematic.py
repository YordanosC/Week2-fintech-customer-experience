# task_2_sentiment_thematic.py

import pandas as pd
import os
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Path to data folder
data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')

# Load cleaned reviews
file_paths = glob.glob(os.path.join(data_folder, 'clean_reviews.csv'))
if not file_paths:
    print("Clean reviews file not found.")
    exit()

df = pd.read_csv(file_paths[0])

# Extract review texts
texts = df['review_text'].astype(str).tolist()

# Vectorize text data
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.95, min_df=2)
tfidf = tfidf_vectorizer.fit_transform(texts)

# Apply LDA for topic modeling
n_topics = 5
lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
lda.fit(tfidf)

# Function to display top words per topic
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print(f"Topic {topic_idx + 1}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
        print()

# Display top words for each topic
no_top_words = 10
feature_names = tfidf_vectorizer.get_feature_names_out()
display_topics(lda, feature_names, no_top_words)

# Save topics and keywords to CSV
topics_df = pd.DataFrame()
for idx in range(n_topics):
    top_words = [feature_names[i] for i in lda.components_[idx].argsort()[:-no_top_words - 1:-1]]
    topics_df[f"Topic {idx+1}"] = top_words

topics_df.to_csv(os.path.join(data_folder, 'topics_keywords.csv'), index=False)
print("Saved topic keywords to topics_keywords.csv")