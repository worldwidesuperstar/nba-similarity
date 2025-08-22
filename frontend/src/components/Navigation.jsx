import { Link, useLocation } from "react-router-dom";

function Navigation() {
    const location = useLocation();

    const getLinkClass = (path) => {
        const baseClass = "me-3 text-decoration-none";
        const isActive = location.pathname === path;
        return isActive 
            ? `${baseClass} text-primary fw-bold`
            : `${baseClass} text-secondary`;
    };

    const getLastLinkClass = (path) => {
        const baseClass = "text-decoration-none";
        const isActive = location.pathname === path;
        return isActive 
            ? `${baseClass} text-primary fw-bold`
            : `${baseClass} text-secondary`;
    };

    return (
        <div className="text-center mb-3">
            <Link to="/" className={getLinkClass("/")}>
                data
            </Link>
            <Link to="/comparison" className={getLinkClass("/comparison")}>
                player IQ comparison
            </Link>
            <Link to="/about" className={getLastLinkClass("/about")}>
                about
            </Link>
        </div>
    );
}

export default Navigation;
