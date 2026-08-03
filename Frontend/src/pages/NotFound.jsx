import { Link } from "react-router-dom";

function NotFound() {
    return (
        <div className="auth-hero">
            <div className="auth-card text-center">
                <div className="brand-mark mx-auto mb-3"><i className="bi bi-signpost-split" /></div>
                <h1 className="display-5 fw-bold">404</h1>
                <h3 className="mb-3">Page not found</h3>
                <p className="text-muted mb-4">The route you requested is unavailable. Return to the dashboard to continue.</p>
                <Link to="/dashboard" className="btn btn-primary">Back to dashboard</Link>
            </div>
        </div>
    );
}

export default NotFound;