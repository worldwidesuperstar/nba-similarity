import { useState } from "react";
import Header from "./components/Header.jsx";
import Navigation from "./components/Navigation.jsx";
import DataPage from "./pages/DataPage.jsx";
import PlayerComparisonPage from "./pages/PlayerComparisonPage.jsx";
import AboutPage from "./pages/AboutPage.jsx";

function App() {
    const [currentPage, setCurrentPage] = useState("data");

    const renderPage = () => {
        switch (currentPage) {
            case "data":
                return <DataPage />;
            case "comparison":
                return <PlayerComparisonPage />;
            case "about":
                return <AboutPage />;
            default:
                return <DataPage />;
        }
    };

    return (
        <div className="container-fluid px-0">
            <Header />
            <Navigation currentPage={currentPage} setCurrentPage={setCurrentPage} />
            {renderPage()}
        </div>
    );
}

export default App;
