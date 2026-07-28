import Layout from "../components/Layout";

function Dashboard() {
    const recentDocuments = [
        {
            id: 1,
            name: "Passport.pdf",
            score: 97,
            status: "Verified",
        },
        {
            id: 2,
            name: "Aadhaar.pdf",
            score: 91,
            status: "Verified",
        },
        {
            id: 3,
            name: "PAN_Card.pdf",
            score: 82,
            status: "Review",
        },
        {
            id: 4,
            name: "Driving_License.pdf",
            score: 95,
            status: "Verified",
        },
    ];

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
                        24
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-title">
                        Average Trust Score
                    </div>

                    <div className="stat-value">
                        94%
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-title">
                        Suspicious Documents
                    </div>

                    <div className="stat-value">
                        2
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-title">
                        Today's Uploads
                    </div>

                    <div className="stat-value">
                        5
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

                        {recentDocuments.map((doc) => (

                            <tr key={doc.id}>

                                <td>{doc.name}</td>

                                <td>{doc.score}%</td>

                                <td>

                                    <span
                                        className={
                                            doc.status === "Verified"
                                                ? "status-good"
                                                : "status-review"
                                        }
                                    >
                                        {doc.status}
                                    </span>

                                </td>

                                <td>

                                    <button
                                        className="btn-primary-custom"
                                    >
                                        View Report
                                    </button>

                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </Layout>
    );
}

export default Dashboard;