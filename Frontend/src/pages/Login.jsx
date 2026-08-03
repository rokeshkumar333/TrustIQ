import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import authService from "../services/authService";

function Login() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        setLoading(true);
        setError("");

        try {
            await authService.login(formData);
            navigate("/dashboard");
        } catch (err) {
            setError(err.response?.data?.message || "Invalid email or password.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-hero">
            <div className="auth-card">
                <div className="text-center mb-4">
                    <div className="brand-mark mx-auto mb-3"><i className="bi bi-shield-check" /></div>
                    <h2 className="mb-2">Welcome back</h2>
                    <p className="text-muted">Sign in to continue your trust verification workflow.</p>
                </div>

                {error && <div className="alert alert-danger">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Email</label>
                        <input type="email" className="form-control" name="email" value={formData.email} onChange={handleChange} required />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Password</label>
                        <input type="password" className="form-control" name="password" value={formData.password} onChange={handleChange} required />
                    </div>

                    <button className="btn btn-primary w-100" disabled={loading}>
                        {loading ? "Signing in..." : "Login"}
                    </button>
                </form>

                <div className="text-center mt-3">
                    Don&apos;t have an account? <Link to="/register">Register</Link>
                </div>
            </div>
        </div>
    );
}

export default Login;