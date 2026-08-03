import { useLocation } from "react-router-dom";

function Navbar() {
    const location = useLocation();

    const pageMeta = {
        "/dashboard": { title: "Dashboard", subtitle: "Operational overview for the verification workflow" },
        "/upload": { title: "Upload Document", subtitle: "Securely ingest new evidence for review" },
        "/documents": { title: "Documents", subtitle: "Track document history and lifecycle" },
        "/analytics": { title: "Analytics", subtitle: "Performance insights across trust signals" },
        "/classification": { title: "Document Classification", subtitle: "AI-generated document categories" },
        "/qr-verification": { title: "QR Verification", subtitle: "Inspect tag integrity and decoded data" },
    };

    const current = location.pathname.startsWith("/report")
        ? { title: "Document Report", subtitle: "Complete review package for this document" }
        : pageMeta[location.pathname] || { title: "TrustIQ", subtitle: "Enterprise trust intelligence" };

    return (
        <header className="navbar">
            <div>
                <p className="navbar-kicker">TrustIQ workspace</p>
                <h3>{current.title}</h3>
                <p className="navbar-subtitle">{current.subtitle}</p>
            </div>

            <div className="navbar-right">
                <div className="navbar-pill">
                    <i className="bi bi-shield-check" />
                    <span>Secure review</span>
                </div>
                <div className="avatar">RK</div>
            </div>
        </header>
    );
}

export default Navbar;