import { NavLink, useNavigate } from "react-router-dom";
import authService from "../services/authService";

function Sidebar() {

    const navigate = useNavigate();

    const handleLogout = () => {

        authService.logout();

        navigate("/login");

    };

    return (

        <div className="sidebar">

            <div className="logo">

                <h2>TrustIQ</h2>

            </div>

            <nav>

                <NavLink
                    to="/dashboard"
                    className={({ isActive }) =>
                        isActive ? "menu active" : "menu"
                    }
                >
                    📊 Dashboard
                </NavLink>

                <NavLink
                    to="/upload"
                    className={({ isActive }) =>
                        isActive ? "menu active" : "menu"
                    }
                >
                    📤 Upload
                </NavLink>

                <NavLink
                    to="/documents"
                    className={({ isActive }) =>
                        isActive ? "menu active" : "menu"
                    }
                >
                    📁 Documents
                </NavLink>

                <NavLink
                    to="/analytics"
                    className={({ isActive }) =>
                        isActive ? "menu active" : "menu"
                    }
                >
                    📈 Analytics
                </NavLink>

                <NavLink
                    to="/classification"
                    className={({ isActive }) =>
                        isActive ? "menu active" : "menu"
                    }
                >
                    🧠 Classification
                </NavLink>

                <NavLink
                    to="/qr-verification"
                    className={({ isActive }) =>
                        isActive ? "menu active" : "menu"
                    }
                >
                    🔍 QR Verification
                </NavLink>

            </nav>

            <button
                className="logout-btn"
                onClick={handleLogout}
            >
                🚪 Logout
            </button>

        </div>

    );

}

export default Sidebar;