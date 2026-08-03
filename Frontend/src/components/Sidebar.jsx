import { NavLink, useNavigate } from "react-router-dom";
import authService from "../services/authService";

function Sidebar() {
    const navigate = useNavigate();

    const handleLogout = () => {
        authService.logout();
        navigate("/login");
    };

    const navItems = [
        { to: "/dashboard", label: "Dashboard", icon: "bi-speedometer2" },
        { to: "/upload", label: "Upload", icon: "bi-cloud-arrow-up" },
        { to: "/documents", label: "Documents", icon: "bi-files" },
        { to: "/analytics", label: "Analytics", icon: "bi-bar-chart-line" },
        { to: "/classification", label: "Classification", icon: "bi-diagram-3" },
        { to: "/qr-verification", label: "QR Verification", icon: "bi-qr-code-scan" },
    ];

    return (
        <aside className="sidebar">
            <div>
                <div className="logo">
                    <div className="brand-mark">T</div>
                    <div>
                        <h2>TrustIQ</h2>
                        <p>Enterprise trust engine</p>
                    </div>
                </div>

                <nav className="nav-links">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.to}
                            to={item.to}
                            className={({ isActive }) => (isActive ? "menu active" : "menu")}
                        >
                            <i className={`bi ${item.icon}`} />
                            <span>{item.label}</span>
                        </NavLink>
                    ))}
                </nav>
            </div>

            <button className="logout-btn" onClick={handleLogout}>
                <i className="bi bi-box-arrow-right" />
                <span>Logout</span>
            </button>
        </aside>
    );
}

export default Sidebar;