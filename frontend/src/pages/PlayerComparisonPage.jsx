import PlayerComparison from "../components/PlayerComparison.jsx";

function PlayerComparisonPage() {
    return (
        <main className="d-flex justify-content-center flex-wrap">
            <div
                style={{
                    minheight: "700px",
                    justifyContent: "flex-start",
                }}
            >
                <PlayerComparison />
            </div>
        </main>
    );
}

export default PlayerComparisonPage;
