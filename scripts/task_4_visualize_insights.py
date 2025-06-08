import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

# Load data
df = pd.read_csv('analysis.csv')

# Plot 1: Sentiment Distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='sentiment_label', hue='bank')
plt.title('Sentiment Distribution by Bank')
plt.savefig('sentiment_distribution.png')
plt.close()

# Plot 2: Rating Distribution
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='rating', hue='bank', multiple='stack')
plt.title('Rating Distribution by Bank')
plt.savefig('rating_distribution.png')
plt.close()

# Plot 3: Word Cloud per Bank
for bank in df['bank'].unique():
    bank_reviews = df[df['bank'] == bank]['processed_text'].str.cat(sep=' ')
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(bank_reviews)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Word Cloud for {bank}')
    plt.savefig(f'wordcloud_{bank.lower()}.png')
    plt.close()

print("Visualizations saved")