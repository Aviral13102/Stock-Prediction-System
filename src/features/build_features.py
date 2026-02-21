# In src/features/build_features.py

import pandas as pd
import os

# In src/features/build_features.py

import pandas as pd
import os

def create_features(ticker, data_dir='data'):
    """
    Loads all raw data for a ticker, merges it, and creates a feature DataFrame.
    """
    raw_dir = os.path.join(data_dir, 'raw')
    processed_dir = os.path.join(data_dir, 'processed')
    
    # Load daily prices
    price_df = pd.read_csv(f'{raw_dir}/{ticker}_prices.csv', index_col='Date', parse_dates=True)
    
    # Load daily aggregated news sentiment
    try:
        sentiment_df = pd.read_csv(f'{processed_dir}/news_sentiment.csv', index_col='date', parse_dates=True)
        ticker_sentiment = sentiment_df[sentiment_df['ticker'] == ticker]
        daily_sentiment = ticker_sentiment[['positive', 'negative', 'neutral']]
    except FileNotFoundError:
        daily_sentiment = pd.DataFrame(index=price_df.index)

    # Load Macro Data
    try:
        macro_df = pd.read_csv(f'{processed_dir}/macro_data.csv', index_col=0, parse_dates=True)
    except FileNotFoundError:
        macro_df = pd.DataFrame(index=price_df.index)

    # Load and Forward-Fill Fundamentals
    try:
        fundamentals_df = pd.read_csv(f'{raw_dir}/{ticker}_fundamentals.csv')
        fundamentals_df['fiscalDateEnding'] = pd.to_datetime(fundamentals_df['fiscalDateEnding'])
        fundamentals_df.set_index('fiscalDateEnding', inplace=True)
        daily_fundamentals = fundamentals_df.reindex(price_df.index, method='ffill')
    except FileNotFoundError:
        print(f"Fundamentals file for {ticker} not found. Skipping.")
        daily_fundamentals = pd.DataFrame(index=price_df.index)

    # --- UPDATED SECTION ---
    # Start with the daily price data and join other sources
    feat_df = price_df.copy()
    feat_df = feat_df.join(daily_sentiment)
    feat_df = feat_df.join(macro_df)
    
    # Conditionally join fundamentals only if the dataframe is not empty
    if not daily_fundamentals.empty and 'reportedEPS' in daily_fundamentals.columns:
        feat_df = feat_df.join(daily_fundamentals[['reportedEPS']])
    # -----------------------
    
    # Fill any remaining NaNs after joins
    feat_df.fillna(0, inplace=True)
    
    # Create technical indicators
    feat_df['SMA_50'] = feat_df['Close'].rolling(window=50).mean()
    feat_df['returns'] = feat_df['Close'].pct_change()
    feat_df['Close_Lag_1'] = feat_df['Close'].shift(1)
    
    for lag in range(1, 6):
        feat_df[f'returns_lag_{lag}'] = feat_df['returns'].shift(lag)
        
    feat_df['target'] = feat_df['Close'].shift(-1)
    
    feat_df.dropna(inplace=True)
    
    return feat_df

# This is the new, correct block
if __name__ == '__main__':
    import yaml

    # Function to load the config file
    def load_config(config_path='config/config.yaml'):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    # Load the one true ticker list from your config
    config = load_config()
    TICKERS = config['settings']['tickers']

    # Now the script will loop through all tickers from your config
    for ticker in TICKERS:
        print(f"Building features for {ticker}...")
        features = create_features(ticker)

        processed_dir = 'data/processed'
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)

        features.to_csv(f'{processed_dir}/{ticker}_features.csv')
        print(f"Feature DataFrame for {ticker} created and saved.")