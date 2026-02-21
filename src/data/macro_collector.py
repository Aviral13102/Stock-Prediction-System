# Save this file as: src/data/macro_collector.py

from fredapi import Fred
import yaml
import pandas as pd
import os

def load_config(config_path='config/config.yaml'):
    """Loads the YAML config file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def get_macro_data(api_key, output_path):
    """
    Fetches key macroeconomic series from FRED and saves them to a CSV.
    """
    print("Fetching macroeconomic data from FRED...")
    try:
        fred = Fred(api_key=api_key)
        
        # Series IDs for key indicators
        series_map = {
            'GDP': 'GDP',                       # Gross Domestic Product
            'CPI': 'CPIAUCSL',                  # Consumer Price Index
            'FEDFUNDS': 'FEDFUNDS',             # Federal Funds Rate
            'UNRATE': 'UNRATE',                 # Unemployment Rate
            'T10Y2Y': 'T10Y2Y',                 # 10-Yr Treasury minus 2-Yr Treasury Spread
            'OILPRICE': 'DCOILWTICO'            # WTI Crude Oil Price
        }

        # Fetch all series
        df_list = [fred.get_series(series_id).rename(name) for name, series_id in series_map.items()]
        
        # Combine into a single DataFrame
        macro_df = pd.concat(df_list, axis=1)
        
        # Forward-fill to handle different reporting frequencies
        macro_df.ffill(inplace=True)
        
        # Save to file
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        macro_df.to_csv(output_path)
        
        print(f"Macroeconomic data saved to {output_path}")

    except Exception as e:
        print(f"  > An error occurred while fetching FRED data: {e}")

if __name__ == '__main__':
    config = load_config()
    api_key = config['api_keys']['fred']
    # We save this to 'processed' because we are already combining and filling it
    output_file_path = 'data/processed/macro_data.csv' 
    
    get_macro_data(api_key, output_file_path)