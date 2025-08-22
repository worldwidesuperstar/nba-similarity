import { useEffect, useState } from "react";
import MarkdownViewer from "../components/MarkdownViewer";

function AboutPage() {
    const [readmeContent, setReadmeContent] = useState("");

    useEffect(() => {
        fetch("/README.md")
            .then((response) => response.text())
            .then((text) => setReadmeContent(text));
    }, []);

    return (
        <main className="container">
            <MarkdownViewer content={readmeContent} />
        </main>
    );
}

export default AboutPage;
