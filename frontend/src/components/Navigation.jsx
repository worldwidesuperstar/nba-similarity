import { Link } from "react-router-dom";

function Navigation() {
    return (
        <div className="text-center mb-3">
            <Link to="/" className="me-3">
                data
            </Link>
            <Link to="/comparison" className="me-3">
                player IQ comparison
            </Link>
            <Link to="/about">about</Link>
        </div>
    );
}

export default Navigation;
