export default function Header({ onClear, hasMessages }) {
    return (
        <header className="header">
            <div className="header-brand">
                <div className="header-logo">IIIT Kota</div>
                <div className="header-tagline">Placement Help Cell</div>
                <div className="header-divider" />
            </div>
            {hasMessages && (
                <div className="header-actions">
                    <button className="btn-clear" onClick={onClear}>New Chat</button>
                </div>
            )}
        </header>
    )
}
