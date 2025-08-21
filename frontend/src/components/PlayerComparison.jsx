import { useState, useRef, useEffect } from "react";
import Plotly from "plotly.js-dist-min";
import playersWithRawData from "../data/players_with_raw_data.json";

function PlayerComparison() {
    const [player1, setPlayer1] = useState("LeBron James");
    const [player2, setPlayer2] = useState("Nikola Joki\u0107");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const plotRef = useRef(null);

    const playerOptions = playersWithRawData
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((player) => ({
            value: player.name,
            label: `${player.name} (${player.position})`,
        }));

    useEffect(() => {
        if (player1 && player2) {
            generateComparison();
        }
    }, []);

    const getOrdinalSuffix = (num) => {
        const j = num % 10,
            k = num % 100;
        if (j == 1 && k != 11) {
            return num + "st";
        }
        if (j == 2 && k != 12) {
            return num + "nd";
        }
        if (j == 3 && k != 13) {
            return num + "rd";
        }
        return num + "th";
    };

    const createBarChart = (player1Data, player2Data) => {
        const metrics = [
            { key: "ast_tov_ratio", name: "AST/TOV Ratio" },
            { key: "clutch_ast_tov", name: "Clutch AST/TOV" },
            { key: "ast_pct", name: "Assist %" },
            { key: "screen_assists_per_36", name: "Screen Assists" },
            { key: "efg_pct", name: "Effective FG%" },
            { key: "late_clock_efficiency", name: "Late Clock Efficiency" },
            { key: "deflections_per_36", name: "Deflections" },
            { key: "shooting_foul_pct", name: "Shooting Foul Rate" },
            { key: "personal_foul_rate", name: "Personal Fouls" },
            { key: "age", name: "Age" },
        ];

        const player1Percentiles = [];
        const player2Percentiles = [];
        const player1Colors = [];
        const player2Colors = [];
        const player1TextLabels = [];
        const player2TextLabels = [];
        const metricNames = [];

        for (const metric of metrics) {
            const p1Metric = player1Data.metrics[metric.key];
            const p2Metric = player2Data.metrics[metric.key];

            if (p1Metric && p2Metric) {
                player1Percentiles.push(p1Metric.percentile);
                player2Percentiles.push(p2Metric.percentile);
                metricNames.push(metric.name);

                const p1Higher = p1Metric.percentile > p2Metric.percentile;
                const p2Higher = p2Metric.percentile > p1Metric.percentile;

                player1Colors.push(p1Higher ? "#0d6efd" : "#ced4da");
                player2Colors.push(p2Higher ? "#0d6efd" : "#ced4da");

                const p1Text = `${p1Metric.raw_value}${
                    p1Metric.display_unit
                } (${getOrdinalSuffix(Math.round(p1Metric.percentile))})`;
                const p2Text = `${p2Metric.raw_value}${
                    p2Metric.display_unit
                } (${getOrdinalSuffix(Math.round(p2Metric.percentile))})`;

                player1TextLabels.push(p1Text);
                player2TextLabels.push(p2Text);
            }
        }

        // left side negative
        const player1NegativeValues = player1Percentiles.map((val) => -val);

        const data = [
            {
                type: "bar",
                y: metricNames,
                x: player1NegativeValues,
                name: player1Data.name,
                marker: { color: player1Colors },
                text: player1TextLabels,
                textposition: "middle center",
                textfont: {
                    color: "white",
                    size: 12,
                },
                cliponaxis: false,
                hoverinfo: "none",
                orientation: "h",
            },
            {
                type: "bar",
                y: metricNames,
                x: player2Percentiles,
                name: player2Data.name,
                marker: { color: player2Colors },
                text: player2TextLabels,
                textposition: "inside",
                textfont: {
                    color: "white",
                    size: 12,
                },
                cliponaxis: false,
                hoverinfo: "none",
                orientation: "h",
            },
        ];

        const layout = {
            title: `Basketball IQ Comparison<br>${player1Data.name} vs ${player2Data.name}`,
            font: { family: "JetBrains Mono, monospace" },
            annotations: [
                {
                    x: -50,
                    y: 1.11,
                    xref: "x",
                    yref: "paper",
                    text: player1Data.name,
                    showarrow: false,
                    font: {
                        size: 20,
                        color: "#333",
                        family: "JetBrains Mono, monospace",
                    },
                    xanchor: "center",
                },
                {
                    x: 50,
                    y: 1.11,
                    xref: "x",
                    yref: "paper",
                    text: player2Data.name,
                    showarrow: false,
                    font: {
                        size: 20,
                        color: "#333",
                        family: "JetBrains Mono, monospace",
                    },
                    xanchor: "center",
                },
                {
                    x: -50,
                    y: 1.05,
                    xref: "x",
                    yref: "paper",
                    text: `bbIQ: ${player1Data.iq_score}`,
                    showarrow: false,
                    font: {
                        size: 14,
                        color: "#6c757d",
                        family: "JetBrains Mono, monospace",
                    },
                    xanchor: "center",
                },
                {
                    x: 50,
                    y: 1.05,
                    xref: "x",
                    yref: "paper",
                    text: `bbIQ: ${player2Data.iq_score}`,
                    showarrow: false,
                    font: {
                        size: 14,
                        color: "#6c757d",
                        family: "JetBrains Mono, monospace",
                    },
                    xanchor: "center",
                },
                {
                    x: 0,
                    y: -0.1,
                    xref: "x",
                    yref: "paper",
                    text: "Percentile",
                    showarrow: false,
                    font: {
                        size: 16,
                        color: "#333",
                        family: "JetBrains Mono, monospace",
                    },
                    xanchor: "center",
                },
            ],
            xaxis: {
                title: "Percentile",
                range: [-100, 100],
                tickvals: [-100, -75, -50, -25, 0, 25, 50, 75, 100],
                ticktext: [
                    "100%",
                    "75%",
                    "50%",
                    "25%",
                    "0%",
                    "25%",
                    "50%",
                    "75%",
                    "100%",
                ],
                zeroline: true,
                zerolinewidth: 1,
                zerolinecolor: "#333",
            },
            yaxis: {
                automargin: true,
                categoryorder: "array",
                categoryarray: metricNames.slice().reverse(),
                ticklabelstandoff: 20,
            },
            barmode: "overlay",
            showlegend: false,
            margin: { t: 80, b: 80, l: 0, r: 100 },
        };

        const config = { displayModeBar: false, responsive: true };

        Plotly.newPlot(plotRef.current, data, layout, config);
    };

    const generateComparison = () => {
        if (!player1 || !player2) {
            setError("Please select both players");
            return;
        }

        setLoading(true);
        setError("");

        try {
            const player1Data = playersWithRawData.find(
                (p) => p.name.toLowerCase() === player1.toLowerCase()
            );
            const player2Data = playersWithRawData.find(
                (p) => p.name.toLowerCase() === player2.toLowerCase()
            );

            if (!player1Data || !player2Data) {
                throw new Error("One or both players not found");
            }

            createBarChart(player1Data, player2Data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            className="d-flex align-items-start flex-wrap"
            style={{ minHeight: "700px" }}
        >
            {/* control sidebar */}
            <div
                className="align-self-center"
                style={{
                    width: "300px",
                    paddingRight: "2rem",
                }}
            >
                <div className="mb-4">
                    <label className="form-label fw-semibold">Player 1:</label>
                    <select
                        className="form-select"
                        value={player1}
                        onChange={(e) => setPlayer1(e.target.value)}
                    >
                        <option value="">Select a player...</option>
                        {playerOptions.map((option) => (
                            <option key={option.value} value={option.value}>
                                {option.label}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="mb-4">
                    <label className="form-label fw-semibold">Player 2:</label>
                    <select
                        className="form-select"
                        value={player2}
                        onChange={(e) => setPlayer2(e.target.value)}
                    >
                        <option value="">Select a player...</option>
                        {playerOptions.map((option) => (
                            <option key={option.value} value={option.value}>
                                {option.label}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="mb-4">
                    <button
                        className="btn btn-primary btn-lg w-100"
                        onClick={generateComparison}
                        disabled={loading || !player1 || !player2}
                    >
                        {loading ? "Generating..." : "Generate Chart"}
                    </button>
                </div>

                {error && (
                    <div className="alert alert-danger" role="alert">
                        {error}
                    </div>
                )}
            </div>

            {/* graph */}
            <div className="flex-grow-1">
                <div
                    ref={plotRef}
                    style={{
                        width: "100%",
                        height: "70vh",
                    }}
                ></div>
            </div>
        </div>
    );
}

export default PlayerComparison;
