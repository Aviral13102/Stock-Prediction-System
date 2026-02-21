export default function PredictionCard({ label, value, change, direction, color = 'blue' }) {
    return (
        <div className={`stat-card ${color}`}>
            <div className="stat-label">{label}</div>
            <div className="stat-value">{value}</div>
            {change !== undefined && change !== null && (
                <div className={`stat-change ${direction || (change >= 0 ? 'up' : 'down')}`}>
                    {change >= 0 ? '▲' : '▼'} {Math.abs(change).toFixed(2)}%
                </div>
            )}
        </div>
    );
}
