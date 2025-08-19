import { useState, useEffect } from "react";
import PlayerTable from "./components/PlayerTable.jsx";
import playersData from "./data/players.json";

function App() {
    const [players, setPlayers] = useState([]);
    const [selectedPlayer, setSelectedPlayer] = useState(null);
    const [minutesFilter, setMinutesFilter] = useState(0);
    const [sortOrder, setSortOrder] = useState("asc");

    useEffect(() => {
        setPlayers(playersData);
    }, []);

    const filteredPlayers = players
        .filter((player) => player.minutes >= minutesFilter)
        .sort((a, b) => {
            if (sortOrder === "asc") {
                return a.rank - b.rank;
            } else {
                return b.rank - a.rank;
            }
        });

    const handleSortToggle = () => {
        setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    };

    return (
        <div className="container-fluid py-4">
            <header className="text-center mb-4">
                <h1 className="display-1 fw-bold">nba-iq</h1>
                <p className="lead text-muted">
                    composite metric quantifying "basketball IQ" with NBA
                    statistics
                </p>
            </header>

            <main>
                <div
                    className="d-flex flex-wrap justify-content-center"
                    style={{ gap: "10px", minWidth: "100vw" }}
                >
                    <div>
                        <PlayerTable
                            players={filteredPlayers}
                            selectedPlayer={selectedPlayer}
                            onPlayerSelect={setSelectedPlayer}
                            sortOrder={sortOrder}
                            onSortToggle={handleSortToggle}
                        />
                        <div className="text-center text-muted mt-1">
                            <small>
                                all stats from 2024-25 Regular Season, collected
                                from nba-api and Basketball Reference
                            </small>
                        </div>
                    </div>

                    <div>
                        <div className="card m-0">
                            <div className="card-body">
                                <div className="mb-3">
                                    <label className="form-label fw-semibold">
                                        minimum MPG:
                                    </label>
                                    <input
                                        type="number"
                                        className="form-control"
                                        min="0"
                                        placeholder="0"
                                        value={
                                            minutesFilter === 0
                                                ? ""
                                                : minutesFilter
                                        }
                                        onChange={(e) => {
                                            const value = e.target.value;
                                            if (value === "") {
                                                setMinutesFilter(0);
                                            } else {
                                                setMinutesFilter(
                                                    Number(value) || 0
                                                );
                                            }
                                        }}
                                    />
                                </div>
                            </div>
                        </div>
                        <div className="text text-muted ms-1 mt-1">
                            <small>
                                showing {filteredPlayers.length} players
                            </small>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;
