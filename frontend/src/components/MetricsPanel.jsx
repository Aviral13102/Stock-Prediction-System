export default function MetricsPanel({ metrics }) {
    if (!metrics) {
        return (
            <div className="glass-card">
                <div className="card-header">
                    <h3>Model Performance</h3>
                </div>
                <div className="loading-container">
                    <div className="spinner" />
                </div>
            </div>
        );
    }

    const items = [
        { label: 'R² Score', value: metrics.r2?.toFixed(4) ?? '—', cls: 'metric-r2' },
        { label: 'MSE', value: metrics.mse?.toFixed(4) ?? '—', cls: 'metric-mse' },
        { label: 'MAE', value: metrics.mae?.toFixed(4) ?? '—', cls: 'metric-mae' },
        { label: 'Best Val Loss', value: metrics.best_val_loss?.toFixed(4) ?? '—', cls: 'metric-loss' },
    ];

    return (
        <div className="glass-card">
            <div className="card-header">
                <h3>📊 Model Performance</h3>
                <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                    {metrics.epochs_trained > 0 ? `${metrics.epochs_trained} epochs` : 'Default metrics'}
                </span>
            </div>

            <div className="metrics-grid">
                {items.map((item) => (
                    <div className="metric-item" key={item.label}>
                        <div className={`metric-val ${item.cls}`}>{item.value}</div>
                        <div className="metric-name">{item.label}</div>
                    </div>
                ))}
            </div>

            {metrics.train_samples > 0 && (
                <div style={{
                    marginTop: '16px',
                    padding: '12px',
                    background: 'rgba(255,255,255,0.03)',
                    borderRadius: '10px',
                    fontSize: '12px',
                    color: 'var(--text-muted)',
                    display: 'flex',
                    justifyContent: 'space-around'
                }}>
                    <span>Train: {metrics.train_samples} samples</span>
                    <span>Val: {metrics.val_samples} samples</span>
                </div>
            )}
        </div>
    );
}
