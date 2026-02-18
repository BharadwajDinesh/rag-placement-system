import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

function SourcesPanel({ sources }) {
    const [open, setOpen] = useState(false)
    if (!sources || sources.length === 0) return null

    return (
        <div className="sources-section">
            <button className="sources-toggle" onClick={() => setOpen(o => !o)}>
                {open ? '▾' : '▸'} {sources.length} source{sources.length > 1 ? 's' : ''} used
            </button>
            {open && (
                <div className="sources-list">
                    {sources.map((src, i) => (
                        <div key={i} className="source-chip">
                            <span className="source-score">{(src.score * 100).toFixed(0)}%</span>
                            {src.text_preview}
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

function TypingIndicator() {
    return (
        <div className="message-row">
            <div className="avatar bot">🤖</div>
            <div className="typing-indicator">
                <div className="typing-dot" />
                <div className="typing-dot" />
                <div className="typing-dot" />
            </div>
        </div>
    )
}

export default function MessageList({ messages, loading, messagesEndRef }) {
    return (
        <div className="messages-list">
            {messages.map(msg => (
                <div key={msg.id} className={`message-row ${msg.role}`}>
                    <div className={`avatar ${msg.role === 'user' ? 'user' : 'bot'}`}>
                        {msg.role === 'user' ? '👤' : 'TP'}
                    </div>
                    <div className="bubble-wrap">
                        <div className={`bubble ${msg.role === 'user' ? 'user' : 'bot'} ${msg.error ? 'error' : ''}`}>
                            {msg.role === 'user' ? (
                                msg.content
                            ) : (
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                    {msg.content}
                                </ReactMarkdown>
                            )}
                        </div>
                        {msg.role === 'assistant' && !msg.error && (
                            <SourcesPanel sources={msg.sources} />
                        )}
                    </div>
                </div>
            ))}
            {loading && <TypingIndicator />}
            <div ref={messagesEndRef} />
        </div>
    )
}
