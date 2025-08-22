function Navigation({ currentPage, setCurrentPage }) {
    const getLinkClass = (page) => {
        const baseClass = "me-3 text-decoration-none";
        const isActive = currentPage === page;
        return isActive 
            ? `${baseClass} text-primary fw-bold`
            : `${baseClass} text-secondary`;
    };

    const getLastLinkClass = (page) => {
        const baseClass = "text-decoration-none";
        const isActive = currentPage === page;
        return isActive 
            ? `${baseClass} text-primary fw-bold`
            : `${baseClass} text-secondary`;
    };

    return (
        <div className="text-center mb-3">
            <button 
                className={getLinkClass("data")}
                style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                onClick={() => setCurrentPage("data")}
            >
                data
            </button>
            <button 
                className={getLinkClass("comparison")}
                style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                onClick={() => setCurrentPage("comparison")}
            >
                player IQ comparison
            </button>
            <button 
                className={getLastLinkClass("about")}
                style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                onClick={() => setCurrentPage("about")}
            >
                about
            </button>
        </div>
    );
}

export default Navigation;
