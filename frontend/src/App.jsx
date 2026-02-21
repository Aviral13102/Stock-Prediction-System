import { useState, useEffect } from 'react';
import './index.css';
import Sidebar from './components/Sidebar';
import StockChart from './components/StockChart';
import PredictionCard from './components/PredictionCard';
import SentimentPanel from './components/SentimentPanel';
import MetricsPanel from './components/MetricsPanel';
import { fetchTickers, fetchPrediction, fetchHistory, fetchMetrics, fetchSentiment, fetchAllPredictions } from './api';

function App() {
  const [tickers, setTickers] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [allPredictions, setAllPredictions] = useState([]);
  const [history, setHistory] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load tickers on mount
  useEffect(() => {
    async function init() {
      try {
        const data = await fetchTickers();
        setTickers(data.tickers || []);
        const predData = await fetchAllPredictions();
        setAllPredictions(predData.predictions || []);
        const metricsData = await fetchMetrics();
        setMetrics(metricsData);
        if (data.tickers?.length > 0) {
          setSelectedTicker(data.tickers[0]);
        }
      } catch (e) {
        console.error('Failed to load initial data:', e);
        // Use fallback tickers
        const fallback = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'NVDA', 'V', 'JPM'];
        setTickers(fallback);
        setSelectedTicker(fallback[0]);
      }
      setLoading(false);
    }
    init();
  }, []);

  // Load ticker-specific data
  useEffect(() => {
    if (!selectedTicker) return;

    async function loadTickerData() {
      try {
        const [predData, histData, sentData] = await Promise.all([
          fetchPrediction(selectedTicker),
          fetchHistory(selectedTicker),
          fetchSentiment(selectedTicker),
        ]);
        setPrediction(predData);
        setHistory(histData);
        setSentiment(sentData);
      } catch (e) {
        console.error(`Failed to load data for ${selectedTicker}:`, e);
      }
    }
    loadTickerData();
  }, [selectedTicker]);

  const getPredictionForTicker = (t) =>
    allPredictions.find((p) => p.ticker === t);

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
        <div className="spinner" />
      </div>
    );
  }

  return (
    <>
      <Sidebar
        tickers={tickers}
        selected={selectedTicker}
        onSelect={setSelectedTicker}
        predictions={allPredictions}
      />
      <main className="main-content">
        <div className="page-header">
          <h2>{selectedTicker} Dashboard</h2>
          <span className="ticker-tag">Multi-Modal Prediction</span>
        </div>

        <div className="prediction-row">
          <PredictionCard
            label="Current Price"
            value={prediction ? `$${prediction.current_price}` : '—'}
            color="blue"
          />
          <PredictionCard
            label="Predicted Price"
            value={prediction ? `$${prediction.predicted_price}` : '—'}
            change={prediction?.change_percent}
            direction={prediction?.direction}
            color={prediction?.direction === 'up' ? 'green' : 'red'}
          />
          <PredictionCard
            label="R² Score"
            value={metrics ? metrics.r2.toFixed(2) : '—'}
            color="purple"
          />
          <PredictionCard
            label="Model MAE"
            value={metrics ? metrics.mae.toFixed(2) : '—'}
            color="blue"
          />
        </div>

        <div className="grid-3">
          <StockChart history={history} prediction={prediction} ticker={selectedTicker} />
          <SentimentPanel sentiment={sentiment} ticker={selectedTicker} />
        </div>

        <MetricsPanel metrics={metrics} />
      </main>
    </>
  );
}

export default App;
