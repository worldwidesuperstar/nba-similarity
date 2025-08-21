function Header() {
    return (
        <header className="text-center" style={{ backgroundColor: "#eeeeee" }}>
            <h1 className="display-1 py-2 fw-bold">nba-iq</h1>
            <p className="lead text-muted">
                composite metric quantifying "basketball IQ" with NBA statistics
            </p>
            <hr></hr>
        </header>
    );
}

export default Header;
