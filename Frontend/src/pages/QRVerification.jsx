import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import Loader from "../components/Loader";
import api from "../api/api";

function QRVerification() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadVerification = async () => {
            try {
                const response = await api.get("/qr-verification");
                setItems(response.data.verifications || []);
            } catch (fetchError) {
                console.error(fetchError);
                setError("Unable to load QR verification results.");
            } finally {
                setLoading(false);
            }
        };

        loadVerification();
    }, []);

    return (
        <Layout>
            <div className="dashboard-title">
                <h2>QR verification</h2>
                <p>Review uploaded documents for QR detection and validation details.</p>
            </div>

            <div className="table-container">
                {error ? (
                    <div className="alert alert-danger" role="alert">
                        {error}
                    </div>
                ) : null}

                <div className="d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <h4 className="mb-1">Verification results</h4>
                        <p className="text-muted mb-0">Each record shows the current QR state and confidence rating</p>
                    </div>
                    <span className="badge-soft">Scan-ready</span>
                </div>

                {loading ? (
                    <Loader />
                ) : (
                    <>
                        <table>
                            <thead>
                                <tr>
                                    <th>Document</th>
                                    <th>Type</th>
                                    <th>Uploaded</th>
                                    <th>QR found</th>
                                    <th>Validation</th>
                                    <th>Confidence</th>
                                </tr>
                            </thead>
                            <tbody>
                                {items.length === 0 ? (
                                    <tr>
                                        <td colSpan="6" className="text-center py-4 text-muted">
                                            No QR verification results available.
                                        </td>
                                    </tr>
                                ) : (
                                    items.map((item) => (
                                        <tr key={item.id || item.original_filename}>
                                            <td>{item.original_filename}</td>
                                            <td>{item.file_type || "Unknown"}</td>
                                            <td>{item.uploaded_at || "Unknown"}</td>
                                            <td>{item.qr_found ? "Yes" : "No"}</td>
                                            <td>
                                                <span className={item.verified ? "text-success" : "text-danger"}>
                                                    {item.validation_result || (item.verified ? "Verified" : "Invalid")}
                                                </span>
                                                <div className="small text-muted">{item.method}</div>
                                            </td>
                                            <td>{item.confidence ? `${Math.round(item.confidence * 100)}%` : "N/A"}</td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>

                        {!loading && items.length > 0 ? (
                            <div className="mt-4">
                                <h5 className="mb-3">QR data summary</h5>
                                {items.map((item) => (
                                    <div key={`summary-${item.id || item.original_filename}`} className="panel-card p-3 mb-3">
                                        <div className="d-flex justify-content-between align-items-center mb-2">
                                            <div>
                                                <h6 className="mb-1">{item.original_filename}</h6>
                                                <small className="text-muted">{item.file_type || "Unknown file type"}</small>
                                            </div>
                                            <span className={item.qr_found ? "badge bg-success" : "badge bg-secondary"}>
                                                {item.qr_found ? "QR found" : "QR missing"}
                                            </span>
                                        </div>
                                        <p className="mb-2">{item.message}</p>
                                        <p className="mb-1 fw-semibold">QR content</p>
                                        <pre className="bg-light p-2 rounded mb-0">
                                            {item.qr_content && item.qr_content.length > 0 ? item.qr_content.join("\n") : "No QR data extracted."}
                                        </pre>
                                    </div>
                                ))}
                            </div>
                        ) : null}
                    </>
                )}
            </div>
        </Layout>
    );
}

export default QRVerification;
