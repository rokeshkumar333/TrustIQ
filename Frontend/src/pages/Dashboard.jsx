import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import Loader from "../components/Loader";
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

    const statCards = [
        { title: "Documents uploaded", value: loading ? "—" : summary.total_documents, icon: "bi-file-earmark-check", tone: "primary" },
        { title: "Average trust score", value: loading ? "—" : `${summary.average_trust_score}%`, icon: "bi-graph-up-arrow", tone: "success" },
        { title: "Suspicious documents", value: loading ? "—" : summary.suspicious_documents, icon: "bi-exclamation-triangle", tone: "warning" },
        { title: "Today’s uploads", value: loading ? "—" : summary.today_uploads, icon: "bi-cloud-arrow-up", tone: "info" },
    ];

    return (
        <Layout>
            <div className="dashboard-title">
                <h2>Executive dashboard</h2>
                <p>Monitor document flow, trust outcomes, and review queues in one place.</p>
            </div>

            <div className="card-grid">
                {statCards.map((card) => (
                    <div className="stat-card" key={card.title}>
                        <div className="d-flex justify-content-between align-items-start">
                            <div>
                                <div className="stat-title">{card.title}</div>
                                <div className="stat-value">{card.value}</div>
                            </div>
                            <div className={`rounded-circle p-2 bg-${card.tone === "warning" ? "warning" : card.tone === "success" ? "success" : card.tone === "info" ? "info" : "primary"} bg-opacity-10 text-${card.tone === "warning" ? "warning" : card.tone === "success" ? "success" : card.tone === "info" ? "info" : "primary"}`}>
                                <i className={`bi ${card.icon}`} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="table-container">
                <div className="d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <h4 className="mb-1">Recent documents</h4>
                        <p className="text-muted mb-0">Latest review activity and trust decisions</p>
                    </div>
                    <span className="badge-soft">Live updates</span>
                </div>

                {loading ? (
                    <Loader />
                ) : (
                    <table>
                        <thead>
                            <tr>
                                <th>Document</th>
                                <th>Trust score</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {documents.length === 0 ? (
                                <tr>
                                    <td colSpan="4" className="text-center py-4 text-muted">
                                        No documents uploaded yet.
                                    </td>
                                </tr>
                            ) : (
                                documents.map((doc) => (
                                    <tr key={doc.id}>
                                        <td>{doc.original_filename}</td>
                                        <td>{doc.trust_score || 0}%</td>
                                        <td>
                                            <span className={doc.status === "Verified" ? "status-good" : "status-review"}>
                                                {doc.status || "Not Processed"}
                                            </span>
                                        </td>
                                        <td>
                                            <button className="btn-primary-custom" onClick={() => navigate(`/report/${doc.id}`)}>
                                                View report
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                )}
            </div>
        </Layout>
    );
}

export default Dashboard;