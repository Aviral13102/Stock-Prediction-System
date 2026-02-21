export default function Sidebar({ tickers, selected, onSelect, predictions }) {
    return (
        <nav className="sidebar">
            <div className="sidebar-logo">
                <div className="logo-icon">S</div>
                <h1>StockPredict AI</h1>
            </div>

            <div className="sidebar-section-label">Watchlist</div>

            {tickers.map((ticker) => {
                const pred = predictions?.find((p) => p.ticker === ticker);
                const isUp = pred?.direction === 'up';
                return (
                    <div
                        key={ticker}
                        className={`sidebar-item ${selected === ticker ? 'active' : ''}`}
                        onClick={() => onSelect(ticker)}
                    >
                        <span className="ticker-badge">{ticker}</span>
                        {pred && (
                            <span className={`item-price ${isUp ? 'price-up' : 'price-down'}`}>
                                ${pred.current_price}
                            </span>
                        )}
                    </div>
                );
            })}

            <div className="sidebar-section-label" style={{ marginTop: 'auto' }}>
                System
            </div>
            <div className="sidebar-item" style={{ opacity: 0.5, cursor: 'default' }}>
                <span>⚙️</span>
                <span>Settings</span>
            </div>
        </nav>
    );
}
