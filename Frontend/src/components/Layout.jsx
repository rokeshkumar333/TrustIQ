import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

function Layout({ children }) {
    return (
        <div className="layout">

            <Sidebar />

            <div className="main-section">

                <Navbar />

                <div className="content">

                    {children}

                </div>

            </div>

        </div>
    );
}

export default Layout;