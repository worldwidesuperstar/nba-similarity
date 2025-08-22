import { useState, useRef, useEffect } from "react";
import Plotly from "plotly.js-dist-min";
import playersWithRawData from "../data/players_with_raw_data.json";

function PlayerComparison() {
    const [player1, setPlayer1] = useState("LeBron James");
    const [player2, setPlayer2] = useState("Nikola Joki\u0107");
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

    const wrapPlayerName = (name) => {
        // If name is longer than 15 characters, try to break it at a space
        if (name.length > 15) {
            const words = name.split(" ");
            if (words.length > 1) {
                const midpoint = Math.ceil(words.length / 2);
                const firstLine = words.slice(0, midpoint).join(" ");
                const secondLine = words.slice(midpoint).join(" ");
                return `${firstLine}<br>${secondLine}`;
            }
        }
        return name;
    };

    const createBarChart = (player1Data, player2Data) => {
        const metrics = [
            { key: "ast_tov_ratio", name: "AST/TOV Ratio" },
            { key: "clutch_ast_tov", name: "Clutch AST/TOV" },
            { key: "ast_pct", name: "Assist %" },
            { key: "screen_assists_per_36", name: "Screen Assists per 36" },
            { key: "efg_pct", name: "Effective FG%" },
            { key: "late_clock_efficiency", name: "Late Clock Efficiency" },
            { key: "deflections_per_36", name: "Deflections per 36" },
            { key: "shooting_foul_pct", name: "Shooting Foul Rate" },
            { key: "personal_foul_rate", name: "Personal Fouls per 36" },
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
                } (${getOrdinalSuffix(Math.round(p1Metric.percentile))} %)`;
                const p2Text = `${p2Metric.raw_value}${
                    p2Metric.display_unit
                } (${getOrdinalSuffix(Math.round(p2Metric.percentile))} %)`;

                player1TextLabels.push(p1Text);
                player2TextLabels.push(p2Text);
            }
        }

        // left side negative
        const player1NegativeValues = player1Percentiles.map((val) => -val);

        // position outside if bar is too small
        const player1TextPositions = player1Percentiles.map((val) =>
            val < 30 ? "outside" : "inside"
        );
        const player2TextPositions = player2Percentiles.map((val) =>
            val < 30 ? "outside" : "inside"
        );

        const player1TextColors = player1Percentiles.map((val) =>
            val < 30 ? "black" : "white"
        );
        const player2TextColors = player2Percentiles.map((val) =>
            val < 30 ? "black" : "white"
        );

        const data = [
            {
                type: "bar",
                y: metricNames,
                x: player1NegativeValues,
                name: player1Data.name,
                marker: { color: player1Colors },
                text: player1TextLabels,
                textposition: player1TextPositions,
                textfont: {
                    color: player1TextColors,
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
                textposition: player2TextPositions,
                textfont: {
                    color: player2TextColors,
                    size: 12,
                },
                cliponaxis: false,
                hoverinfo: "none",
                orientation: "h",
            },
        ];

        const layout = {
            title: `nba-iq<br>${player1Data.name} vs ${player2Data.name}`,
            font: { family: "JetBrains Mono, monospace" },
            annotations: [
                {
                    x: -10,
                    y: 1.04,
                    xref: "x",
                    yref: "paper",
                    text: wrapPlayerName(player1Data.name),
                    showarrow: false,
                    font: {
                        size: 20,
                        color: "#333",
                        family: "JetBrains Mono, monospace",
                    },
                    xanchor: "right",
                    yanchor: "bottom",
                    align: "right",
                },
                {
                    x: 10,
                    y: 1.04,
                    xref: "x",
                    yref: "paper",
                    text: wrapPlayerName(player2Data.name),
                    showarrow: false,
                    font: {
                        size: 20,
                        color: "#333",
                        family: "JetBrains Mono, monospace",
                    },
                    xanchor: "left",
                    yanchor: "bottom",
                    align: "left",
                },
                {
                    x: -10,
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
                    xanchor: "right",
                },
                {
                    x: 10,
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
                    xanchor: "left",
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
            margin: { t: 80, b: 60, l: 30, r: 30 },
        };

        const config = { displayModeBar: false, responsive: true };

        Plotly.newPlot(plotRef.current, data, layout, config);
    };

    const downloadChart = () => {
        if (plotRef.current) {
            Plotly.downloadImage(plotRef.current, {
                format: "png",
                width: 1200,
                height: 800,
                filename: `nba-iq ${player1} vs ${player2}`,
            });
        }
    };

    const generateComparison = () => {
        if (!player1 || !player2) {
            setError("Please select both players");
            return;
        }

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
        }
    };

    return (
        <div
            className="d-flex align-items-start flex-wrap justify-content-lg-start justify-content-center"
            style={{ minHeight: "700px", gap: "5vw" }}
        >
            {/* control sidebar */}
            <div className="card m-0 align-self-center">
                <div className="card-body">
                    <div className="mb-3">
                        <label className="form-label fw-semibold">
                            player 1:
                        </label>
                        <select
                            className="form-control"
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

                    <div className="mb-3">
                        <label className="form-label fw-semibold">
                            player 2:
                        </label>
                        <select
                            className="form-control"
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

                    <div className="mb-3">
                        <button
                            className="btn btn-primary btn-lg w-100 mb-2"
                            onClick={generateComparison}
                            disabled={!player1 || !player2}
                        >
                            generate chart
                        </button>
                        <button
                            className="btn btn-outline-secondary w-100"
                            onClick={downloadChart}
                            disabled={!plotRef.current || !player1 || !player2}
                        >
                            export as PNG
                        </button>
                    </div>

                    {error && (
                        <div className="alert alert-danger" role="alert">
                            {error}
                        </div>
                    )}
                </div>
            </div>

            {/* graph */}
            <div
                className="card flex-grow-1"
                style={{
                    padding: "8px",
                    marginTop: "8px",
                    marginBottom: "0px",
                    borderRadius: "8px",
                    maxWidth: "95vw",
                }}
            >
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
