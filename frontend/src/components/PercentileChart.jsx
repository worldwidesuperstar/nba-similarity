function PercentileChart({ player }) {
    const getMetricData = (metricKey, name) => {
        const metric = player.metrics?.[metricKey];
        return {
            name: name,
            value: metric ? parseFloat(metric.percentile || 0) : 0,
            rawValue: metric ? metric.raw_value : 0,
            unit: metric ? metric.display_unit : "",
            key: metricKey,
        };
    };

    const metrics = [
        getMetricData("ast_tov_ratio", "AST/TOV Ratio"),
        getMetricData("clutch_ast_tov", "Clutch AST/TOV Ratio"),
        getMetricData("ast_pct", "Assist Percentage"),
        getMetricData("late_clock_efficiency", "Late Clock Efficiency"),
        getMetricData("efg_pct", "Effective FG Percentage"),
        getMetricData("deflections_per_36", "Deflections per 36"),
        getMetricData(
            "screen_assists_per_36",
            "Screen Assists per 36 (position-relative)"
        ),
        getMetricData(
            "shooting_foul_pct",
            "Shooting Foul on Contest Rate (position-relative)"
        ),
        getMetricData("personal_foul_rate", "Personal Fouls per 36"),
        getMetricData("age", "Age"),
    ];

    const getBarColor = (value) => {
        if (value >= 75) return "success";
        if (value >= 50) return "warning";
        if (value >= 25) return { backgroundColor: "#fd7e14" };
        return "danger";
    };

    const getOrdinalSuffix = (num) => {
        const j = num % 10;
        const k = num % 100;
        if (j === 1 && k !== 11) return "st";
        if (j === 2 && k !== 12) return "nd";
        if (j === 3 && k !== 13) return "rd";
        return "th";
    };

    return (
        <div className="percentile-charts">
            {metrics.map((metric) => (
                <div key={metric.key} className="mb-3">
                    <div className="d-flex justify-content-between align-items-center mb-1">
                        <small className="text-muted fw-semibold">
                            {metric.name}
                        </small>
                        <small className="text-muted">
                            {metric.rawValue}
                            {metric.unit} ({metric.value.toFixed(0)}
                            {getOrdinalSuffix(metric.value.toFixed(0))}{" "}
                            percentile)
                        </small>
                    </div>
                    <div className="progress" style={{ height: "8px" }}>
                        <div
                            className={
                                typeof getBarColor(metric.value) === "string"
                                    ? `progress-bar bg-${getBarColor(
                                          metric.value
                                      )}`
                                    : "progress-bar"
                            }
                            role="progressbar"
                            style={{
                                width: `${metric.value}%`,
                                ...(typeof getBarColor(metric.value) ===
                                "object"
                                    ? getBarColor(metric.value)
                                    : {}),
                            }}
                            aria-valuenow={metric.value}
                            aria-valuemin="0"
                            aria-valuemax="100"
                        />
                    </div>
                </div>
            ))}
        </div>
    );
}

export default PercentileChart;
