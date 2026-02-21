# src/models/train.py

import os
import sys
import json
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
import yaml
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.data.dataloader import MultimodalStockDataset
from src.models.multimodal_model import MultiModalFusionModel


def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def train_model(config_path='config/config.yaml'):
    config = load_config(config_path)
    tickers = config['settings']['tickers']

    # --- Hyperparameters ---
    model_cfg = config.get('model', {})
    sequence_length = model_cfg.get('sequence_length', 30)
    batch_size = model_cfg.get('batch_size', 32)
    epochs = model_cfg.get('epochs', 50)
    learning_rate = model_cfg.get('learning_rate', 0.001)
    lstm_hidden = model_cfg.get('lstm_hidden', 64)
    lstm_layers = model_cfg.get('lstm_layers', 2)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # --- Data ---
    print("Loading dataset...")
    dataset = MultimodalStockDataset(tickers, sequence_length=sequence_length)
    print(f"Total sequences: {len(dataset)}")

    if len(dataset) == 0:
        print("ERROR: Dataset is empty. Ensure feature CSVs exist in data/processed/")
        return

    # Determine feature dimensions from first sample
    sample = dataset[0]
    tabular_input_size = sample['tabular_features'].shape[1]
    sentiment_input_size = sample['news_features'].shape[1]

    # Train/val split (80/20)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    print(f"Train: {train_size}, Val: {val_size}")

    # --- Model ---
    model = MultiModalFusionModel(
        tabular_input_size=tabular_input_size,
        sentiment_input_size=sentiment_input_size,
        lstm_hidden=lstm_hidden,
        lstm_layers=lstm_layers,
    ).to(device)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5
    )

    # --- Training Loop ---
    best_val_loss = float('inf')
    train_losses = []
    val_losses = []

    os.makedirs('models', exist_ok=True)

    print(f"\nTraining for {epochs} epochs...")
    for epoch in range(1, epochs + 1):
        # Train
        model.train()
        epoch_train_loss = 0.0
        for batch in train_loader:
            tab = batch['tabular_features'].to(device)
            news = batch['news_features'].to(device)
            target = batch['target'].to(device).unsqueeze(1)

            optimizer.zero_grad()
            pred = model(tab, news)
            loss = criterion(pred, target)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            epoch_train_loss += loss.item()

        avg_train_loss = epoch_train_loss / len(train_loader)
        train_losses.append(avg_train_loss)

        # Validate
        model.eval()
        epoch_val_loss = 0.0
        all_preds = []
        all_targets = []
        with torch.no_grad():
            for batch in val_loader:
                tab = batch['tabular_features'].to(device)
                news = batch['news_features'].to(device)
                target = batch['target'].to(device).unsqueeze(1)

                pred = model(tab, news)
                loss = criterion(pred, target)
                epoch_val_loss += loss.item()
                all_preds.extend(pred.cpu().numpy().flatten())
                all_targets.extend(target.cpu().numpy().flatten())

        avg_val_loss = epoch_val_loss / len(val_loader)
        val_losses.append(avg_val_loss)
        scheduler.step(avg_val_loss)

        if epoch % 5 == 0 or epoch == 1:
            print(f"  Epoch {epoch:3d}/{epochs} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")

        # Save best model
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save({
                'model_state_dict': model.state_dict(),
                'tabular_input_size': tabular_input_size,
                'sentiment_input_size': sentiment_input_size,
                'lstm_hidden': lstm_hidden,
                'lstm_layers': lstm_layers,
                'epoch': epoch,
            }, 'models/best_model.pth')

    # --- Final Metrics ---
    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)

    mse = float(np.mean((all_preds - all_targets) ** 2))
    mae = float(np.mean(np.abs(all_preds - all_targets)))
    ss_res = np.sum((all_targets - all_preds) ** 2)
    ss_tot = np.sum((all_targets - np.mean(all_targets)) ** 2)
    r2 = float(1 - (ss_res / ss_tot)) if ss_tot > 0 else 0.0

    metrics = {
        'mse': round(mse, 4),
        'mae': round(mae, 4),
        'r2': round(r2, 4),
        'best_val_loss': round(best_val_loss, 4),
        'epochs_trained': epochs,
        'train_samples': train_size,
        'val_samples': val_size,
    }

    with open('models/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"\n--- Training Complete ---")
    print(f"  MSE:  {metrics['mse']}")
    print(f"  MAE:  {metrics['mae']}")
    print(f"  R²:   {metrics['r2']}")
    print(f"  Best model saved to models/best_model.pth")
    print(f"  Metrics saved to models/metrics.json")

    return model, metrics


if __name__ == '__main__':
    train_model()
