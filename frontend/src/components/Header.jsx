import { FaGithub } from "react-icons/fa";

function Header() {
    return (
        <header
            className="text-center position-relative"
            style={{ backgroundColor: "#eeeeee" }}
        >
            <a
                href="https://github.com/worldwidesuperstar/nba-iq"
                target="_blank"
                rel="noopener noreferrer"
                className="position-absolute top-0 start-0 mt-0 ms-3 text-muted"
                style={{ fontSize: "3rem" }}
            >
                <FaGithub />
            </a>
            <h1 className="display-1 py-2 fw-bold">nba-iq</h1>
            <p className="lead text-muted">
                composite metric quantifying "basketball IQ" with NBA statistics
            </p>
            <hr></hr>
        </header>
    );
}

export default Header;
