# src/models/predict.py

import os
import torch
import pandas as pd
import numpy as np

from src.models.multimodal_model import MultiModalFusionModel


def load_model(model_path='models/best_model.pth'):
    """Load trained model from checkpoint."""
    if not os.path.exists(model_path):
        return None, None

    checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)

    model = MultiModalFusionModel(
        tabular_input_size=checkpoint['tabular_input_size'],
        sentiment_input_size=checkpoint['sentiment_input_size'],
        lstm_hidden=checkpoint['lstm_hidden'],
        lstm_layers=checkpoint['lstm_layers'],
    )
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model, checkpoint


def predict_ticker(ticker, model=None, checkpoint=None,
                   data_dir='data/processed', sequence_length=30):
    """Generate prediction for a single ticker."""
    if model is None:
        model, checkpoint = load_model()
        if model is None:
            return None

    feature_path = os.path.join(data_dir, f'{ticker}_features.csv')
    if not os.path.exists(feature_path):
        return None

    df = pd.read_csv(feature_path, index_col='Date', parse_dates=True)

    tabular_cols = [c for c in ['SMA_50', 'returns', 'Close_Lag_1', 'reportedEPS']
                    if c in df.columns]
    news_cols = ['positive', 'negative', 'neutral']

    # Take the last `sequence_length` rows
    if len(df) < sequence_length:
        return None

    recent = df.iloc[-sequence_length:]
    tabular_seq = torch.tensor(
        recent[tabular_cols].values, dtype=torch.float32
    ).unsqueeze(0)
    news_seq = torch.tensor(
        recent[news_cols].values, dtype=torch.float32
    ).unsqueeze(0)

    with torch.no_grad():
        predicted_price = model(tabular_seq, news_seq).item()

    current_price = float(df['Close'].iloc[-1])
    change_pct = ((predicted_price - current_price) / current_price) * 100

    return {
        'ticker': ticker,
        'current_price': round(current_price, 2),
        'predicted_price': round(predicted_price, 2),
        'change_percent': round(change_pct, 2),
        'direction': 'up' if change_pct > 0 else 'down',
        'date': str(df.index[-1].date()),
    }


def predict_all_tickers(tickers, data_dir='data/processed', sequence_length=30):
    """Generate predictions for all tickers."""
    model, checkpoint = load_model()
    if model is None:
        # Return mock predictions if no trained model exists
        return _mock_predictions(tickers, data_dir)

    results = []
    for ticker in tickers:
        pred = predict_ticker(ticker, model, checkpoint, data_dir, sequence_length)
        if pred:
            results.append(pred)
    return results


def _mock_predictions(tickers, data_dir='data/processed'):
    """Generate reasonable mock predictions from last known prices when no model is trained."""
    results = []
    for ticker in tickers:
        feature_path = os.path.join(data_dir, f'{ticker}_features.csv')
        if not os.path.exists(feature_path):
            continue
        df = pd.read_csv(feature_path, index_col='Date', parse_dates=True)
        if len(df) < 2:
            continue

        current = float(df['Close'].iloc[-1])
        # Use average recent return to project
        avg_return = float(df['returns'].iloc[-5:].mean()) if 'returns' in df.columns else 0.001
        predicted = current * (1 + avg_return)
        change_pct = avg_return * 100

        results.append({
            'ticker': ticker,
            'current_price': round(current, 2),
            'predicted_price': round(predicted, 2),
            'change_percent': round(change_pct, 2),
            'direction': 'up' if change_pct > 0 else 'down',
            'date': str(df.index[-1].date()),
        })
    return results
