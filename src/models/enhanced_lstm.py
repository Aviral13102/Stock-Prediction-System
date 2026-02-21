# In src/models/enhanced_lstm.py

import torch.nn as nn

class EnhancedLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(EnhancedLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # --- MODIFICATIONS ---
        # 1. bidirectional=True: Processes data forwards and backwards.
        # 2. dropout=0.25: Adds dropout between LSTM layers for regularization.
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                            batch_first=True, bidirectional=True, dropout=0.25)
        
        # 3. Extra dense layer with a ReLU activation function for more complex patterns.
        self.fc1 = nn.Linear(hidden_size * 2, hidden_size) # Input is *2 because it's bidirectional
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        # --------------------

    def forward(self, x):
        # Forward propagate LSTM
        out, _ = self.lstm(x)
        
        # Get the output from the last time step
        out = out[:, -1, :]
        
        # Pass through the new dense layers
        out = self.fc1(out)
        out = self.relu(out)
        out = self.fc2(out)
        
        return out