function PercentileChart({ player }) {
    const metrics = [
        {
            name: "AST/TOV Ratio",
            value: parseFloat(player.ast_tov_ratio_percentile || 0),
            key: "ast_tov_ratio_percentile",
        },
        {
            name: "Clutch AST/TOV Ratio",
            value: parseFloat(player.clutch_ast_tov_percentile || 0),
            key: "clutch_ast_tov_percentile",
        },
        {
            name: "Assist Percentage",
            value: parseFloat(player.ast_pct_percentile || 0),
            key: "ast_pct_percentile",
        },
        {
            name: "Late Clock Efficiency",
            value: parseFloat(player.late_clock_efficiency_percentile || 0),
            key: "late_clock_efficiency_percentile",
        },
        {
            name: "Effective FG Percentage",
            value: parseFloat(player.efg_pct_percentile || 0),
            key: "efg_pct_percentile",
        },
        {
            name: "Deflections per 36",
            value: parseFloat(player.deflections_per_36_percentile || 0),
            key: "deflections_per_36_percentile",
        },
        {
            name: "Screen Assists per 36 (position-relative)",
            value: parseFloat(player.screen_assists_per_36_percentile || 0),
            key: "screen_assists_per_36_percentile",
        },
        {
            name: "Shooting Foul Rate (position-relative)",
            value: parseFloat(player.shooting_foul_pct_percentile || 0),
            key: "shooting_foul_pct_percentile",
        },
        {
            name: "Personal Foul Rate",
            value: parseFloat(player.personal_foul_rate_percentile || 0),
            key: "personal_foul_rate_percentile",
        },
        {
            name: "Age",
            value: parseFloat(player.age_percentile || 0),
            key: "age_percentile",
        },
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
            {metrics.map((metric, index) => (
                <div key={metric.key} className="mb-3">
                    <div className="d-flex justify-content-between align-items-center mb-1">
                        <small className="text-muted fw-semibold">
                            {metric.name}
                        </small>
                        <small className="text-muted">
                            {metric.value.toFixed(0)}
                            {getOrdinalSuffix(metric.value.toFixed(0))}{" "}
                            percentile
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
