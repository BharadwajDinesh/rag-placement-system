import { useState, useRef } from 'react'

export default function InputBox({ onSend, loading }) {
    const [value, setValue] = useState('')
    const textareaRef = useRef(null)

    const handleSend = () => {
        if (!value.trim() || loading) return
        onSend(value)
        setValue('')
        // Reset textarea height
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto'
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    const handleInput = (e) => {
        setValue(e.target.value)
        // Auto-resize textarea
        e.target.style.height = 'auto'
        e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px'
    }

    return (
        <div className="input-area">
            <div className="input-wrap">
                <textarea
                    ref={textareaRef}
                    className="chat-input"
                    rows={1}
                    value={value}
                    onChange={handleInput}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask about placement policies..."
                    disabled={loading}
                    id="chat-input"
                />
                <button
                    className="send-btn"
                    onClick={handleSend}
                    disabled={loading || !value.trim()}
                    title="Send (Enter)"
                    id="send-button"
                >
                    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                    </svg>
                </button>
            </div>
            <p className="input-hint">Press Enter to send · Shift+Enter for new line</p>
        </div>
    )
}
