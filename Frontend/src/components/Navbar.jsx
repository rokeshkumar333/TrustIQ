import { useLocation } from "react-router-dom";

function Navbar() {

    const location = useLocation();

    const getTitle = () => {

        switch (location.pathname) {

            case "/dashboard":
                return "Dashboard";

            case "/upload":
                return "Upload Document";

            case "/documents":
                return "Documents";

            default:
                if (location.pathname.startsWith("/report")) {
                    return "Document Report";
                }

                return "TrustIQ";
        }

    };

    return (

        <div className="navbar">

            <div>

                <h3>{getTitle()}</h3>

            </div>

            <div className="navbar-right">

                <span className="welcome">

                    Welcome

                </span>

                <div className="avatar">

                    RK

                </div>

            </div>

        </div>

    );

}

export default Navbar;