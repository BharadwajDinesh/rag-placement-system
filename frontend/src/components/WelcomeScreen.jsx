export default function WelcomeScreen({ suggestions, onSuggest }) {
    return (
        <div className="welcome">
            <div className="welcome-icon">💬</div>
            <h2>How can I help you today?</h2>
            <p>
                Ask me anything about placement policies, eligibility, rules,
                and procedures at IIIT Kota.
            </p>
            <div className="suggestions-label">Try asking</div>
            <div className="suggestions-grid">
                {suggestions.map((q, i) => (
                    <button
                        key={i}
                        className="suggestion-card"
                        onClick={() => onSuggest(q)}
                    >
                        {q}
                    </button>
                ))}
            </div>
        </div>
    )
}
