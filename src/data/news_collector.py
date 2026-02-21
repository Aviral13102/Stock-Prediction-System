import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# NOTE: For a real system, you'd use a news API (e.g., NewsAPI, Refinitiv).
# Here, we'll simulate with a sample CSV of headlines.
# Create a file `data/raw/sample_news.csv` with columns: date, ticker, headline

# Initialize model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

def analyze_sentiment(news_df):
    """Analyzes sentiment of headlines in a DataFrame."""
    sentiments = []
    for headline in news_df['headline']:
        inputs = tokenizer(headline, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits
        
        scores = {k: v for k, v in zip(model.config.id2label.values(), torch.softmax(logits, dim=1).tolist()[0])}
        sentiments.append(scores)
    
    sentiment_df = pd.DataFrame(sentiments)
    result_df = pd.concat([news_df.reset_index(), sentiment_df], axis=1)
    return result_df

if __name__ == '__main__':
    # Load your news data
    news_data = pd.read_csv('data/raw/sample_news.csv', parse_dates=['date'])
    
    # Analyze and save
    sentiment_results = analyze_sentiment(news_data)
    sentiment_results.to_csv('data/processed/news_sentiment.csv', index=False)
    print("Sentiment analysis complete.")