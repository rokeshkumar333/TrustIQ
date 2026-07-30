import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import api from "../api/api";

function Analytics() {
    const [summary, setSummary] = useState({
        total_documents: 0,
        average_score: 0,
        max_score: 0,
        min_score: 0,
        status_breakdown: {},
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadAnalytics = async () => {
            try {
                const response = await api.get("/analytics");
                setSummary(response.data.summary || {});
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        loadAnalytics();
    }, []);

    return (
        <Layout>
            <div className="dashboard-title">
                <h2>Analytics</h2>
                <p>Operational insights for document verification performance</p>
            </div>

            <div className="card-grid">
                <div className="stat-card">
                    <div className="stat-title">Total Documents</div>
                    <div className="stat-value">{loading ? "..." : summary.total_documents}</div>
                </div>
                <div className="stat-card">
                    <div className="stat-title">Average Score</div>
                    <div className="stat-value">{loading ? "..." : `${summary.average_score}%`}</div>
                </div>
                <div className="stat-card">
                    <div className="stat-title">Highest Score</div>
                    <div className="stat-value">{loading ? "..." : `${summary.max_score}%`}</div>
                </div>
                <div className="stat-card">
                    <div className="stat-title">Lowest Score</div>
                    <div className="stat-value">{loading ? "..." : `${summary.min_score}%`}</div>
                </div>
            </div>

            <div className="table-container">
                <h4 className="mb-3">Status Breakdown</h4>
                <table className="table table-bordered">
                    <thead>
                        <tr>
                            <th>Status</th>
                            <th>Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(summary.status_breakdown || {}).map(([status, count]) => (
                            <tr key={status}>
                                <td>{status}</td>
                                <td>{count}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Layout>
    );
}

export default Analytics;
