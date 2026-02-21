import torch
# In src/models/baseline_lstm.py

import torch.nn as nn

# In src/models/baseline_lstm.py

class BaselineLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(BaselineLSTM, self).__init__()
        # --- MODIFICATION ---
        # 1. Add bidirectional=True
        # 2. Add dropout for regularization
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                            batch_first=True, bidirectional=True, dropout=0.2)
        
        # 3. The input to the final layer is now hidden_size * 2
        self.fc = nn.Linear(hidden_size * 2, output_size)
        # --------------------

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out