import { useMemo } from 'react';

export default function StockChart({ history, prediction, ticker }) {
    const chartData = useMemo(() => {
        if (!history?.data?.length) return null;

        const data = history.data;
        const closes = data.map((d) => d.close);
        const min = Math.min(...closes) * 0.995;
        const max = Math.max(...closes) * 1.005;
        const range = max - min || 1;

        return { data, closes, min, max, range };
    }, [history]);

    if (!chartData) {
        return (
            <div className="glass-card chart-container">
                <div className="card-header">
                    <h3>Price Chart — {ticker}</h3>
                </div>
                <div className="loading-container">
                    <div className="spinner" />
                </div>
            </div>
        );
    }

    const { data, closes, min, max, range } = chartData;
    const width = 800;
    const height = 300;
    const paddingX = 20;
    const paddingY = 20;
    const chartW = width - paddingX * 2;
    const chartH = height - paddingY * 2;

    // Build SVG line path
    const points = closes.map((c, i) => {
        const x = paddingX + (i / (closes.length - 1)) * chartW;
        const y = paddingY + chartH - ((c - min) / range) * chartH;
        return [x, y];
    });

    const linePath = points.map((p, i) => (i === 0 ? `M ${p[0]},${p[1]}` : `L ${p[0]},${p[1]}`)).join(' ');

    // Area fill path
    const areaPath = linePath + ` L ${points[points.length - 1][0]},${paddingY + chartH} L ${points[0][0]},${paddingY + chartH} Z`;

    // Prediction point
    let predPoint = null;
    if (prediction?.predicted_price) {
        const predY = paddingY + chartH - ((prediction.predicted_price - min) / range) * chartH;
        const predX = paddingX + chartW + 10;
        predPoint = { x: Math.min(predX, width - 10), y: Math.max(paddingY, Math.min(predY, paddingY + chartH)) };
    }

    // Y-axis labels
    const yLabels = [];
    const steps = 5;
    for (let i = 0; i <= steps; i++) {
        const val = min + (i / steps) * range;
        const y = paddingY + chartH - (i / steps) * chartH;
        yLabels.push({ val: val.toFixed(0), y });
    }

    // X-axis labels (pick ~6 dates)
    const xLabels = [];
    const step = Math.floor(data.length / 6);
    for (let i = 0; i < data.length; i += step) {
        const x = paddingX + (i / (data.length - 1)) * chartW;
        const label = data[i].date.slice(5); // MM-DD
        xLabels.push({ label, x });
    }

    return (
        <div className="glass-card chart-container">
            <div className="card-header">
                <h3>📈 Price Chart — {ticker}</h3>
                <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                    Last {data.length} days
                </span>
            </div>

            <svg viewBox={`0 0 ${width} ${height + 30}`} style={{ width: '100%', height: 'auto' }}>
                <defs>
                    <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.3" />
                        <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.02" />
                    </linearGradient>
                    <linearGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0%" stopColor="#3b82f6" />
                        <stop offset="100%" stopColor="#8b5cf6" />
                    </linearGradient>
                </defs>

                {/* Grid lines */}
                {yLabels.map((yl, i) => (
                    <g key={i}>
                        <line x1={paddingX} y1={yl.y} x2={paddingX + chartW} y2={yl.y}
                            stroke="rgba(255,255,255,0.04)" strokeWidth="1" />
                        <text x={paddingX - 4} y={yl.y + 4} textAnchor="end"
                            fill="#64748b" fontSize="10">${yl.val}</text>
                    </g>
                ))}

                {/* X labels */}
                {xLabels.map((xl, i) => (
                    <text key={i} x={xl.x} y={height + 16} textAnchor="middle"
                        fill="#64748b" fontSize="10">{xl.label}</text>
                ))}

                {/* Area fill */}
                <path d={areaPath} className="chart-area-fill" />

                {/* Line */}
                <path d={linePath} fill="none" stroke="url(#lineGrad)" strokeWidth="2.5"
                    strokeLinecap="round" strokeLinejoin="round" />

                {/* Current price dot */}
                {points.length > 0 && (
                    <circle cx={points[points.length - 1][0]} cy={points[points.length - 1][1]}
                        r="4" fill="#3b82f6" stroke="white" strokeWidth="2" />
                )}

                {/* Prediction dot */}
                {predPoint && (
                    <>
                        <line x1={points[points.length - 1][0]} y1={points[points.length - 1][1]}
                            x2={predPoint.x} y2={predPoint.y}
                            stroke="#8b5cf6" strokeWidth="2" strokeDasharray="6,4" />
                        <circle cx={predPoint.x} cy={predPoint.y} r="6"
                            className="chart-prediction-dot" />
                        <text x={predPoint.x} y={predPoint.y - 12} textAnchor="middle"
                            fill="#a78bfa" fontSize="11" fontWeight="600">
                            ${prediction.predicted_price}
                        </text>
                    </>
                )}
            </svg>
        </div>
    );
}
