import ReactMarkdown from 'react-markdown';

function MarkdownViewer({ content }) {
    return (
        <div className="markdown-content" style={{
            lineHeight: '1.8',
            maxWidth: '800px',
            margin: '0 auto'
        }}>
            <ReactMarkdown 
                components={{
                    h1: ({node, ...props}) => <h1 style={{marginTop: '2rem', marginBottom: '1.5rem'}} {...props} />,
                    h2: ({node, ...props}) => <h2 style={{marginTop: '2.5rem', marginBottom: '1.2rem'}} {...props} />,
                    h3: ({node, ...props}) => <h3 style={{marginTop: '2rem', marginBottom: '1rem'}} {...props} />,
                    p: ({node, ...props}) => <p style={{marginBottom: '1.2rem'}} {...props} />,
                    ul: ({node, ...props}) => <ul style={{marginBottom: '1.5rem', paddingLeft: '1.5rem'}} {...props} />,
                    ol: ({node, ...props}) => <ol style={{marginBottom: '1.5rem', paddingLeft: '1.5rem'}} {...props} />,
                    li: ({node, ...props}) => <li style={{marginBottom: '0.5rem'}} {...props} />,
                }}
            >
                {content}
            </ReactMarkdown>
        </div>
    );
}

export default MarkdownViewer;