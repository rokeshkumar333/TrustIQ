import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import authService from "../services/authService";

function Register() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        full_name: "",
        email: "",
        password: "",
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

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
        setSuccess("");

        try {
            const response = await authService.register(formData);

            if (response.success) {
                setSuccess(response.message);
                setTimeout(() => {
                    navigate("/login");
                }, 1500);
            } else {
                setError(response.message);
            }
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.error || err.response?.data?.message || "Registration failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-hero">
            <div className="auth-card">
                <div className="text-center mb-4">
                    <div className="brand-mark mx-auto mb-3"><i className="bi bi-person-plus" /></div>
                    <h2 className="mb-2">Create your workspace</h2>
                    <p className="text-muted">Begin securing your document review process with TrustIQ.</p>
                </div>

                {error && <div className="alert alert-danger">{error}</div>}
                {success && <div className="alert alert-success">{success}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Full name</label>
                        <input type="text" className="form-control" name="full_name" value={formData.full_name} onChange={handleChange} placeholder="Enter your full name" required />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Email</label>
                        <input type="email" className="form-control" name="email" value={formData.email} onChange={handleChange} placeholder="Enter your email" required />
                    </div>

                    <div className="mb-3">
                        <label className="form-label">Password</label>
                        <input type="password" className="form-control" name="password" value={formData.password} onChange={handleChange} placeholder="Enter your password" required />
                    </div>

                    <button type="submit" className="btn btn-success w-100" disabled={loading}>
                        {loading ? "Creating account..." : "Register"}
                    </button>
                </form>

                <div className="text-center mt-3">
                    Already have an account? <Link to="/login">Login</Link>
                </div>
            </div>
        </div>
    );
}

export default Register;