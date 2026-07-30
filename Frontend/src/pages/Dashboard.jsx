import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import api from "../api/api";

function Dashboard() {
    const navigate = useNavigate();
    const [summary, setSummary] = useState({
        total_documents: 0,
        average_trust_score: 0,
        suspicious_documents: 0,
        today_uploads: 0,
    });
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadDashboard = async () => {
            try {
                const response = await api.get("/dashboard");
                setSummary(response.data.summary || {});
                setDocuments(response.data.documents || []);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        loadDashboard();
    }, []);

    return (
        <Layout>

            <div className="dashboard-title">
                <h2>Dashboard</h2>
                <p>Welcome to TrustIQ Document Verification System</p>
            </div>

            {/* Statistics Cards */}

            <div className="card-grid">

                <div className="stat-card">
                    <div className="stat-title">
                        Documents Uploaded
                    </div>

                    <div className="stat-value">
                        {loading ? "..." : summary.total_documents}
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-title">
                        Average Trust Score
                    </div>

                    <div className="stat-value">
                        {loading ? "..." : `${summary.average_trust_score}%`}
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-title">
                        Suspicious Documents
                    </div>

                    <div className="stat-value">
                        {loading ? "..." : summary.suspicious_documents}
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-title">
                        Today's Uploads
                    </div>

                    <div className="stat-value">
                        {loading ? "..." : summary.today_uploads}
                    </div>
                </div>

            </div>

            {/* Recent Documents */}

            <div className="table-container">

                <h4 style={{ marginBottom: "20px" }}>
                    Recent Documents
                </h4>

                <table>

                    <thead>

                        <tr>

                            <th>Document</th>

                            <th>Trust Score</th>

                            <th>Status</th>

                            <th>Action</th>

                        </tr>

                    </thead>

                    <tbody>

                        {documents.length === 0 ? (
                            <tr>
                                <td colSpan="4" className="text-center">
                                    {loading ? "Loading recent documents..." : "No documents uploaded yet."}
                                </td>
                            </tr>
                        ) : (
                            documents.map((doc) => (
                                <tr key={doc.id}>
                                    <td>{doc.original_filename}</td>
                                    <td>{doc.trust_score || 0}%</td>
                                    <td>
                                        <span
                                            className={
                                                doc.status === "Verified"
                                                    ? "status-good"
                                                    : "status-review"
                                            }
                                        >
                                            {doc.status || "Not Processed"}
                                        </span>
                                    </td>
                                    <td>
                                        <button
                                            className="btn-primary-custom"
                                            onClick={() => navigate(`/report/${doc.id}`)}
                                        >
                                            View Report
                                        </button>
                                    </td>
                                </tr>
                            ))
                        )}

                    </tbody>

                </table>

            </div>

        </Layout>
    );
}

export default Dashboard;