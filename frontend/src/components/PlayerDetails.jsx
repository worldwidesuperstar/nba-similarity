import { useState } from "react";
import teamsData from "../data/teams.json";
import PercentileChart from "./PercentileChart.jsx";

function PlayerDetails({ player }) {
    const teamName = teamsData[player.team];
    const [viewMode, setViewMode] = useState("percentiles"); // "percentiles" or "histograms"

    return (
        <div className="card">
            <div className="card-body">
                <div className="d-flex justify-content-between align-items-start mb-4">
                    <div>
                        <h3 className="card-title mb-1">{player.name}</h3>
                        <p className="text-muted mb-0">
                            {player.position}, {teamName}
                        </p>
                    </div>
                    <div className="text-end">
                        <h2 className="text-primary mb-0 fw-bold">
                            {player.iq_score}
                        </h2>
                        <small className="text-muted">basketball IQ</small>
                    </div>
                </div>
                <hr></hr>
                <div className="d-flex justify-content-between align-items-center mb-3">
                    <h5 className="mb-0">IQ Indicators</h5>
                    <div className="btn-group btn-group-sm" role="group">
                        <button
                            type="button"
                            className={`btn ${
                                viewMode === "percentiles"
                                    ? "btn-primary"
                                    : "btn-outline-primary"
                            }`}
                            onClick={() => setViewMode("percentiles")}
                        >
                            Percentiles
                        </button>
                        <button
                            type="button"
                            className={`btn ${
                                viewMode === "histograms"
                                    ? "btn-primary"
                                    : "btn-outline-primary"
                            }`}
                            onClick={() => setViewMode("histograms")}
                        >
                            Distributions
                        </button>
                    </div>
                </div>

                <div className="analytics-content">
                    {viewMode === "percentiles" ? (
                        <PercentileChart player={player} />
                    ) : (
                        <div>Histogram distributions coming soon...</div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default PlayerDetails;
