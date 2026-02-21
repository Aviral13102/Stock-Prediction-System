# Multi-Modal Stock Prediction System

An AI-powered stock prediction system that fuses financial price data, macroeconomic indicators, and news sentiment using a Multi-Modal Deep Learning architecture (LSTM + Dense Fusion).

## Features

- **Multi-Modal Architecture**: Combines bidirectional LSTM for technical/macro data with a dense neural network for news sentiment.
- **Data Collection**: Integrated collectors for Yahoo Finance prices, FRED macroeconomic data, Alpha Vantage fundamentals, and news sentiment using FinBERT.
- **FastAPI Backend**: High-performance API serving real-time predictions, historical data, and model performance metrics.
- **React + Vite Dashboard**: Modern, dark-themed dashboard with glassmorphism design, interactive SVG charts, sentiment analysis panels, and model performance gauges.
- **Training Pipeline**: Comprehensive training script with validation loss tracking, R²/MAE/MSE metrics, and model persistence.

## Project Structure

```text
stock_prediction_system/
├── src/
│   ├── api/            # FastAPI server
│   ├── data/           # Data ingestion & collection scripts
│   ├── features/       # Feature engineering & preprocessing
│   └── models/         # PyTorch model definitions & training
├── config/             # Configuration files
├── data/               # Raw and processed data (ignored in git)
├── frontend/           # React + Vite dashboard
├── models/             # Trained model checkpoints (ignored in git)
└── notebooks/          # Exploratory Data Analysis
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Node.js (for frontend)
- API Keys: Alpha Vantage, FRED

### 2. Backend Setup
```bash
# Clone the repository
git clone <repository-url>
cd stock_prediction_system

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Configuration
Create `config/config.yaml` (copy from template if available) and add your API keys:
```yaml
api_keys:
  alpha_vantage: "YOUR_KEY"
  fred: "YOUR_KEY"
```

## Usage

### Start the System
You can use the provided workflow if you have an agentic IDE, or run manually:

**Start Backend:**
```bash
python -m uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
```

**Start Frontend:**
```bash
cd frontend
npm run dev
```

### Training the Model
To retrain the model on the latest data:
```bash
python -m src.models.train
```

## Architecture
The system uses a **Multi-Modal Fusion Model**:
1. **Tabular Branch**: Processes 30-day sequences of price, technical indicators, and macro data through a Bidirectional LSTM.
2. **Sentiment Branch**: Processes FinBERT-derived news sentiment scores (positive, negative, neutral).
3. **Fusion Head**: Concatenates outputs from both branches and passes them through dense layers to predict the next-day closing price.

## Documentation
- [Implementation Plan](implementation_plan.md)
- [Walkthrough](walkthrough.md)
