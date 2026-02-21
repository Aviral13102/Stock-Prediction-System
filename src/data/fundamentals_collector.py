# In src/data/fundamentals_collector.py

import requests
import yaml
import pandas as pd
import time
import os

def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as file:    
        return yaml.safe_load(file)

def get_fundamental_data(tickers, api_key, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for ticker in tickers:
        output_path = os.path.join(output_dir, f'{ticker}_fundamentals.csv')

        # --- NEW: Check if file already exists ---
        if os.path.exists(output_path):
            print(f"Fundamentals for {ticker} already exist. Skipping.")
            continue
        # -----------------------------------------

        print(f"Fetching fundamental data for {ticker}...")
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={api_key}'

        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()

            if "quarterlyEarnings" in data and data["quarterlyEarnings"]:
                df = pd.DataFrame(data['quarterlyEarnings'])
                df.to_csv(output_path, index=False)
                print(f"  > Saved to {output_path}")
            else:
                print(f"  > No earnings data found for {ticker} or API limit reached. Response: {data}")

            time.sleep(15) 

        except Exception as e:
            print(f"  > An error occurred for {ticker}: {e}")

if __name__ == '__main__':
    config = load_config()
    api_key = config['api_keys']['alpha_vantage']
    tickers_to_fetch = config['settings']['tickers']
    output_directory = 'data/raw'

    get_fundamental_data(tickers_to_fetch, api_key, output_directory)
    print("\nFundamental data collection complete.")