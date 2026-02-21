const API_BASE = 'http://localhost:8000';

export async function fetchTickers() {
    const res = await fetch(`${API_BASE}/api/tickers`);
    return res.json();
}

export async function fetchPrediction(ticker) {
    const res = await fetch(`${API_BASE}/api/predict/${ticker}`);
    return res.json();
}

export async function fetchAllPredictions() {
    const res = await fetch(`${API_BASE}/api/predictions`);
    return res.json();
}

export async function fetchHistory(ticker, days = 90) {
    const res = await fetch(`${API_BASE}/api/history/${ticker}?days=${days}`);
    return res.json();
}

export async function fetchMetrics() {
    const res = await fetch(`${API_BASE}/api/metrics`);
    return res.json();
}

export async function fetchSentiment(ticker) {
    const res = await fetch(`${API_BASE}/api/sentiment/${ticker}`);
    return res.json();
}
