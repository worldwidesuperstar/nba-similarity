import PlayerRow from "./PlayerRow";

function PlayerTable({ players, selectedPlayer, onPlayerSelect }) {
    return (
        <div className="card m-0" style={{ maxWidth: "800px" }}>
            <div
                className="table-responsive"
                style={{
                    height: "60vh",
                    minHeight: "60vh",
                    overflowY: "auto",
                    overflowX: "hidden",
                }}
            >
                <table
                    className="table table-hover table-striped mb-0 table-sm"
                    style={{ fontSize: "max(1rem, min(1rem, 2vw))" }}
                >
                    <thead className="table-dark sticky-top">
                        <tr>
                            <th scope="col">rank</th>
                            <th scope="col">player</th>
                            <th scope="col">pos</th>
                            <th scope="col">mpg</th>
                            <th scope="col">gp</th>
                            <th
                                scope="col"
                                className="user-select-none"
                                style={{ cursor: "pointer" }}
                                onClick={() => onSort("iq")}
                            >
                                iq
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {players.map((player) => (
                            <PlayerRow
                                key={player.rank}
                                player={player}
                                isSelected={
                                    selectedPlayer?.rank === player.rank
                                }
                                onClick={() => onPlayerSelect(player)}
                            />
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default PlayerTable;
