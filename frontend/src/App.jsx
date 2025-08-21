import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header.jsx";
import Navigation from "./components/Navigation.jsx";
import DataPage from "./pages/DataPage.jsx";
import PlayerComparisonPage from "./pages/PlayerComparisonPage.jsx";
import AboutPage from "./pages/AboutPage.jsx";

function App() {
    return (
        <Router>
            <div className="container-fluid px-0">
                <Header />
                <Navigation />
                <Routes>
                    <Route path="/" element={<DataPage />} />
                    <Route
                        path="/comparison"
                        element={<PlayerComparisonPage />}
                    />
                    <Route path="/about" element={<AboutPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
