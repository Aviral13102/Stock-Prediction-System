import yfinance as yf
import pandas as pd

def get_price_data(tickers, start_date, end_date, output_path):
    """Downloads OHLCV data for a list of tickers and saves to CSV."""
    df = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
    for ticker in tickers:
        ticker_df = df[ticker].copy()
        ticker_df.dropna(inplace=True) # yfinance can have missing rows
        ticker_df.to_csv(f"{output_path}/{ticker}_prices.csv")
    print(f"Price data saved for {tickers}.")

# In src/data/price_collector.py

if __name__ == '__main__':
    import yaml

    # Function to load the config file
    def load_config(config_path='config/config.yaml'):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    # Load the one true ticker list from your config
    config = load_config()
    TICKERS = config['settings']['tickers']

    # Run the download for all tickers in your config
    get_price_data(TICKERS, '2020-01-01', '2023-12-31', 'data/raw')