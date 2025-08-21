import { useState, useEffect, useRef } from "react";
import PlayerTable from "../components/PlayerTable.jsx";
import PlayerDetails from "../components/PlayerDetails.jsx";
import playersWithRawData from "../data/players_with_raw_data.json";

function DataPage() {
    const [players, setPlayers] = useState([]);
    const [selectedPlayer, setSelectedPlayer] = useState(null);
    const [minutesFilter, setMinutesFilter] = useState(0);
    const [gpFilter, setGpFilter] = useState(0);
    const [sortOrder, setSortOrder] = useState("asc");
    const playerDetailsRef = useRef(null);

    useEffect(() => {
        setPlayers(playersWithRawData);
    }, []);

    const filteredPlayers = players
        .filter((player) => player.minutes >= minutesFilter)
        .filter((player) => player.games >= gpFilter)
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

    const handlePlayerSelect = (player) => {
        setSelectedPlayer(player);
        if (player) {
            setTimeout(() => {
                playerDetailsRef.current.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                });
            }, 100);
        }
    };

    return (
        <main>
            <div
                className="d-flex flex-wrap justify-content-center"
                style={{ gap: "10px", minWidth: "100vw" }}
            >
                <div>
                    <PlayerTable
                        players={filteredPlayers}
                        selectedPlayer={selectedPlayer}
                        onPlayerSelect={handlePlayerSelect}
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
                                    max="48"
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
                            <div className="mb-3">
                                <label className="form-label fw-semibold">
                                    minimum GP:
                                </label>
                                <input
                                    type="number"
                                    className="form-control"
                                    min="0"
                                    max="82"
                                    placeholder="0"
                                    value={gpFilter === 0 ? "" : gpFilter}
                                    onChange={(e) => {
                                        const value = e.target.value;
                                        if (value === "") {
                                            setGpFilter(0);
                                        } else {
                                            setGpFilter(Number(value) || 0);
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

            {selectedPlayer && (
                <div className="mt-5 px-5" ref={playerDetailsRef}>
                    <PlayerDetails player={selectedPlayer} />
                </div>
            )}
        </main>
    );
}

export default DataPage;