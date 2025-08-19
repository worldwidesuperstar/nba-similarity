function PlayerRow({ player, isSelected, onClick }) {
    return (
        <tr
            className={`${isSelected ? "table-primary" : ""}`}
            onClick={onClick}
            style={{ cursor: "pointer" }}
        >
            <td className="fw-bold">{player.rank}</td>
            <td className="fw-semibold">{player.name}</td>
            <td className="text-muted">{player.position}</td>
            <td className="text">{player.minutes}</td>
            <td className="text">{player.games}</td>
            <td className="fw-bold text-primary">{player.iq_score}</td>
        </tr>
    );
}

export default PlayerRow;
