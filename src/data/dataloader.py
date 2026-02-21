# In src/data/dataloader.py

import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np

class MultimodalStockDataset(Dataset):
    def __init__(self, tickers, data_dir='data/processed', sequence_length=30):
        self.tickers = tickers
        self.sequence_length = sequence_length
        self.sequences = self._create_all_sequences(data_dir)

    def _create_all_sequences(self, data_dir):
        sequences = []
        tabular_cols = ['SMA_50', 'returns', 'Close_Lag_1', 'reportedEPS'] # Example
        news_cols = ['positive', 'negative', 'neutral']
        target_col = 'target'

        for ticker in self.tickers:
            df = pd.read_csv(f'{data_dir}/{ticker}_features.csv', index_col='Date', parse_dates=True)
            valid_tabular_cols = [col for col in tabular_cols if col in df.columns]

            for i in range(len(df) - self.sequence_length):
                tabular_seq = df[valid_tabular_cols].iloc[i:i+self.sequence_length].values
                news_seq = df[news_cols].iloc[i:i+self.sequence_length].values
                target = df[target_col].iloc[i+self.sequence_length-1]
                
                sequences.append({
                    'tabular_features': torch.tensor(tabular_seq, dtype=torch.float32),
                    'news_features': torch.tensor(news_seq, dtype=torch.float32),
                    'target': torch.tensor(target, dtype=torch.float32)
                })
        return sequences

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        return self.sequences[idx]