import { useEffect, useMemo, useState } from "react";
import { useParams, Link } from "react-router-dom";
import Layout from "../components/Layout";
import reportService from "../services/reportService";

function Report() {
    const { id } = useParams();
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadReport = async () => {
            try {
                setLoading(true);
                setError("");
                const response = await reportService.getReport(id);
                setReport(response.report);
            } catch (err) {
                console.error(err);
                setError(
                    err?.response?.data?.message ||
                    "Unable to load the document report."
                );
            } finally {
                setLoading(false);
            }
        };

        loadReport();
    }, [id]);

    const scoreClass = useMemo(() => {
        if (!report) return "";

        if (report.status === "Verified") return "status-good";
        if (report.status === "Needs Manual Review") return "status-review";
        return "text-danger";
    }, [report]);

    const renderLoading = () => (
        <div className="text-center py-5">
            <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-3">Loading report details...</p>
        </div>
    );

    const renderError = () => (
        <div className="text-center py-5">
            <p className="text-danger fs-5">{error || "No report found."}</p>
            <Link to="/documents" className="btn btn-outline-primary mt-3">
                Back to Documents
            </Link>
        </div>
    );

    const renderReport = () => (
        <>
            <div className="row g-4">
                <div className="col-lg-8">
                    <div className="card shadow-sm">
                        <div className="card-body">
                            <div className="d-flex justify-content-between align-items-start mb-3">
                                <div>
                                    <h5 className="card-title">Document Information</h5>
                                    <p className="text-muted mb-0">{report.original_filename}</p>
                                </div>
                                <button
                                    type="button"
                                    className="btn btn-outline-secondary"
                                    onClick={() => window.alert("Download report placeholder")}
                                >
                                    Download Report
                                </button>
                            </div>

                            <div className="row gy-3">
                                <div className="col-sm-6">
                                    <div className="fw-semibold">Upload Date</div>
                                    <div>{report.uploaded_at}</div>
                                </div>
                                <div className="col-sm-6">
                                    <div className="fw-semibold">File Type</div>
                                    <div>{report.file_type}</div>
                                </div>
                                <div className="col-sm-6">
                                    <div className="fw-semibold">Trust Score</div>
                                    <div className={scoreClass}>{report.trust_score}%</div>
                                </div>
                                <div className="col-sm-6">
                                    <div className="fw-semibold">Verification Status</div>
                                    <div className={scoreClass}>{report.status}</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="card shadow-sm mt-4">
                        <div className="card-body">
                            <h5 className="card-title">OCR Extracted Text</h5>
                            <div className="text-muted" style={{ whiteSpace: "pre-wrap" }}>
                                {report.ocr_text || "No OCR text available for this document."}
                            </div>
                        </div>
                    </div>

                    <div className="card shadow-sm mt-4 mb-4">
                        <div className="card-body">
                            <h5 className="card-title">Extracted Fields</h5>
                            <pre className="bg-light p-3 rounded" style={{ whiteSpace: "pre-wrap" }}>
                                {Object.keys(report.fields || {}).length > 0
                                    ? JSON.stringify(report.fields, null, 2)
                                    : "No extracted fields available."}
                            </pre>
                        </div>
                    </div>
                </div>
                <div className="col-lg-4">
                    <div className="card shadow-sm">
                        <div className="card-body">
                            <h5 className="card-title">Verification Summary</h5>
                            <div className="mb-3">
                                <div className="fw-semibold">Status</div>
                                <div className={scoreClass}>{report.status}</div>
                            </div>
                            <div className="mb-3">
                                <div className="fw-semibold">QR Verified</div>
                                <div>{report.qr_verification?.verified ? "Yes" : "No"}</div>
                            </div>
                            <div className="mb-3">
                                <div className="fw-semibold">Verification Method</div>
                                <div>{report.qr_verification?.method || "Unknown"}</div>
                            </div>
                            <div>
                                <div className="fw-semibold">Verification Notes</div>
                                <div className="text-muted">
                                    {report.qr_verification?.message || "No verification details available."}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="d-flex gap-3 mt-4">
                <Link to="/documents" className="btn btn-outline-primary">
                    Back to Documents
                </Link>
                <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => window.alert("Download report placeholder")}
                >
                    Download Report
                </button>
            </div>
        </>
    );

    return (
        <Layout>
            <div className="dashboard-title">
                <h2>Document Report</h2>
                <p>Review the full verification summary for your document.</p>
            </div>
            <div className="table-container">
                {loading ? renderLoading() : error || !report ? renderError() : renderReport()}
            </div>
        </Layout>
    );
}

export default Report;
