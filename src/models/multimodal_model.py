# src/models/multimodal_model.py

import torch
import torch.nn as nn


class TabularBranch(nn.Module):
    """Bidirectional LSTM branch for price + technical indicator sequences."""

    def __init__(self, input_size, hidden_size=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers,
            batch_first=True, bidirectional=True, dropout=dropout
        )
        self.output_size = hidden_size * 2  # bidirectional

    def forward(self, x):
        out, _ = self.lstm(x)
        return out[:, -1, :]  # last time-step


class SentimentBranch(nn.Module):
    """Dense branch for news sentiment features (positive, negative, neutral)."""

    def __init__(self, input_size=3, hidden_size=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
        )
        self.output_size = hidden_size

    def forward(self, x):
        # Use last time-step sentiment
        return self.net(x[:, -1, :])


class MultiModalFusionModel(nn.Module):
    """
    Multi-modal stock prediction model.
    Fuses tabular (price/technical) features with news sentiment features
    through separate branches and a shared fusion head.
    """

    def __init__(self, tabular_input_size, sentiment_input_size=3,
                 lstm_hidden=64, lstm_layers=2, sentiment_hidden=32,
                 fusion_hidden=64, output_size=1):
        super().__init__()

        self.tabular_branch = TabularBranch(
            tabular_input_size, lstm_hidden, lstm_layers
        )
        self.sentiment_branch = SentimentBranch(
            sentiment_input_size, sentiment_hidden
        )

        fusion_input = self.tabular_branch.output_size + self.sentiment_branch.output_size

        self.fusion_head = nn.Sequential(
            nn.Linear(fusion_input, fusion_hidden),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(fusion_hidden, fusion_hidden // 2),
            nn.ReLU(),
            nn.Linear(fusion_hidden // 2, output_size),
        )

    def forward(self, tabular_features, news_features):
        tab_out = self.tabular_branch(tabular_features)
        sent_out = self.sentiment_branch(news_features)
        fused = torch.cat([tab_out, sent_out], dim=1)
        return self.fusion_head(fused)
