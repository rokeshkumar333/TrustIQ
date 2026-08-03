import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

function Layout({ children }) {
    return (
        <div className="app-shell">
            <Sidebar />

            <div className="main-section">
                <Navbar />
                <main className="content">{children}</main>
            </div>
        </div>
    );
}

export default Layout;