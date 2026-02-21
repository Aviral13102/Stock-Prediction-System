export default function SentimentPanel({ sentiment, ticker }) {
    if (!sentiment) {
        return (
            <div className="glass-card">
                <div className="card-header">
                    <h3>Sentiment — {ticker}</h3>
                </div>
                <div className="loading-container">
                    <div className="spinner" />
                </div>
            </div>
        );
    }

    const bars = [
        { label: 'Positive', value: sentiment.positive, cls: 'positive', color: 'var(--accent-green)' },
        { label: 'Negative', value: sentiment.negative, cls: 'negative', color: 'var(--accent-red)' },
        { label: 'Neutral', value: sentiment.neutral, cls: 'neutral', color: 'var(--accent-blue)' },
    ];

    return (
        <div className="glass-card">
            <div className="card-header">
                <h3>🧠 News Sentiment</h3>
            </div>

            <div className="sentiment-bars">
                {bars.map((b) => (
                    <div className="sentiment-row" key={b.label}>
                        <span className="sentiment-label">{b.label}</span>
                        <div className="sentiment-bar-track">
                            <div
                                className={`sentiment-bar-fill ${b.cls}`}
                                style={{ width: `${(b.value * 100).toFixed(0)}%` }}
                            />
                        </div>
                        <span className="sentiment-value" style={{ color: b.color }}>
                            {(b.value * 100).toFixed(1)}%
                        </span>
                    </div>
                ))}
            </div>

            {sentiment.headline && (
                <div className="sentiment-headline">
                    <p>"{sentiment.headline}"</p>
                </div>
            )}
        </div>
    );
}
