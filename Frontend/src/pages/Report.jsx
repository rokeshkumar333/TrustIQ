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

    const verificationReport = useMemo(() => report?.verification_report || null, [report]);
    const summary = useMemo(() => report?.report_summary || null, [report]);
    const trustEngine = useMemo(() => report?.trust_score_engine || null, [report]);
    const fraudEngine = useMemo(() => report?.fraud_detection_engine || null, [report]);

    const scoreClass = useMemo(() => {
        if (!summary) return "";

        if (summary.score >= 80) return "status-good";
        if (summary.score >= 60) return "status-review";
        return "text-danger";
    }, [summary]);

    const scoreTone = useMemo(() => {
        if (!summary) return "secondary";
        if (summary.score >= 80) return "success";
        if (summary.score >= 60) return "warning";
        return "danger";
    }, [summary]);

    const scoreTextColor = useMemo(() => {
        if (!summary) return "text-secondary";
        if (summary.score >= 80) return "text-success";
        if (summary.score >= 60) return "text-warning";
        return "text-danger";
    }, [summary]);

    const renderBadge = (value, variant = "secondary") => (
        <span className={`badge bg-${variant}`}>{value}</span>
    );

    const renderGauge = (value) => {
        const percentage = Math.max(0, Math.min(100, value));
        const radius = 46;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (percentage / 100) * circumference;

        return (
            <svg width="140" height="140" viewBox="0 0 120 120" aria-label="trust score gauge">
                <circle cx="60" cy="60" r={radius} fill="none" stroke="#e9ecef" strokeWidth="12" />
                <circle
                    cx="60"
                    cy="60"
                    r={radius}
                    fill="none"
                    stroke={scoreTone === "success" ? "#198754" : scoreTone === "warning" ? "#f59e0b" : "#dc3545"}
                    strokeWidth="12"
                    strokeLinecap="round"
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    transform="rotate(-90 60 60)"
                />
            </svg>
        );
    };

    const handlePrint = () => window.print();

    const handleDownload = () => {
        const content = JSON.stringify(verificationReport || report, null, 2);
        const blob = new Blob([content], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `${report?.original_filename || "report"}.json`;
        link.click();
        URL.revokeObjectURL(url);
    };

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
                    <div className="card shadow-sm border-0">
                        <div className="card-body">
                            <div className="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
                                <div>
                                    <h5 className="card-title mb-1">AI Verification Report</h5>
                                    <p className="text-muted mb-0">{report.original_filename}</p>
                                </div>
                                <div className="d-flex gap-2">
                                    <button type="button" className="btn btn-outline-secondary" onClick={handlePrint}>
                                        Print Report
                                    </button>
                                    <button type="button" className="btn btn-primary" onClick={handleDownload}>
                                        Download Report
                                    </button>
                                </div>
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
                                    <div className={scoreClass}>{summary?.score ?? report.trust_score}%</div>
                                </div>
                                <div className="col-sm-6">
                                    <div className="fw-semibold">Decision</div>
                                    <div>{summary?.status || report.status}</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="card shadow-sm border-0 mt-4">
                        <div className="card-body">
                            <div className="d-flex justify-content-between align-items-center mb-3">
                                <h5 className="card-title mb-0">AI Trust Score Engine</h5>
                                <span className={`badge bg-${scoreTone} fs-6`}>{summary?.score ?? report.trust_score}/100</span>
                            </div>
                            <div className="row align-items-center">
                                <div className="col-md-4 text-center py-3">
                                    <div className="position-relative d-inline-flex align-items-center justify-content-center">
                                        {renderGauge(summary?.score ?? report.trust_score)}
                                        <div className="position-absolute text-center">
                                            <div className={`display-6 fw-bold ${scoreTextColor}`}>{Math.round(summary?.score ?? report.trust_score)}</div>
                                            <div className="text-muted small">/100</div>
                                        </div>
                                    </div>
                                    <div className="text-muted mt-2">Overall Trust Score</div>
                                </div>
                                <div className="col-md-8">
                                    <div className="progress mb-3" style={{ height: "12px" }}>
                                        <div className={`progress-bar bg-${scoreTone}`} role="progressbar" style={{ width: `${summary?.score ?? report.trust_score}%` }} />
                                    </div>
                                    <div className="d-flex align-items-center gap-2 mb-2">
                                        <strong>Risk Level</strong>
                                        <span className={`badge bg-${scoreTone}`}>{summary?.risk_level || "Unknown"}</span>
                                    </div>
                                    <div className="text-muted">Recommended action: {trustEngine?.recommended_action || "No recommendation available"}</div>
                                </div>
                            </div>
                            <div className="mt-4">
                                <h6 className="fw-semibold">Explanation panel</h6>
                                <ul className="mb-0">
                                    {trustEngine?.reasons_affecting_score?.length ? trustEngine.reasons_affecting_score.map((item) => <li key={item}>{item}</li>) : <li>No reasons available.</li>}
                                </ul>
                            </div>
                            <div className="row mt-4 g-3">
                                <div className="col-md-6">
                                    <h6 className="fw-semibold">Positive indicators</h6>
                                    <ul className="mb-0">
                                        {trustEngine?.positive_indicators?.length ? trustEngine.positive_indicators.map((item) => <li key={item}>{item}</li>) : <li>None</li>}
                                    </ul>
                                </div>
                                <div className="col-md-6">
                                    <h6 className="fw-semibold">Negative indicators</h6>
                                    <ul className="mb-0">
                                        {trustEngine?.negative_indicators?.length ? trustEngine.negative_indicators.map((item) => <li key={item}>{item}</li>) : <li>None</li>}
                                    </ul>
                                </div>
                            </div>
                            <div className="mt-4">
                                <h6 className="fw-semibold">Score breakdown</h6>
                                <div className="row g-3">
                                    {(trustEngine?.score_breakdown || []).map((item) => (
                                        <div className="col-md-6" key={item.module}>
                                            <div className="border rounded p-3 h-100">
                                                <div className="d-flex justify-content-between align-items-center">
                                                    <strong>{item.module}</strong>
                                                    <span className="fw-semibold">{item.score}/{item.max_score}</span>
                                                </div>
                                                <div className="progress mt-2" style={{ height: "8px" }}>
                                                    <div className={`progress-bar ${item.impact === "positive" ? "bg-success" : item.impact === "negative" ? "bg-danger" : "bg-warning"}`} style={{ width: `${(item.score / item.max_score) * 100}%` }} />
                                                </div>
                                                <div className="text-muted small mt-2">{item.reason}</div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                            <div className="mt-4">
                                <h6 className="fw-semibold">Confidence breakdown</h6>
                                <div className="row g-3">
                                    <div className="col-md-6">
                                        <div className="border rounded p-3">
                                            <div className="d-flex justify-content-between">
                                                <span>OCR confidence</span>
                                                <strong>{trustEngine?.confidence_breakdown?.ocr_confidence ?? "-"}</strong>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="col-md-6">
                                        <div className="border rounded p-3">
                                            <div className="d-flex justify-content-between">
                                                <span>Classification confidence</span>
                                                <strong>{trustEngine?.confidence_breakdown?.classification_confidence ?? "-"}</strong>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="col-md-6">
                                        <div className="border rounded p-3">
                                            <div className="d-flex justify-content-between">
                                                <span>QR confidence</span>
                                                <strong>{trustEngine?.confidence_breakdown?.qr_confidence ?? "-"}</strong>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="col-md-6">
                                        <div className="border rounded p-3">
                                            <div className="d-flex justify-content-between">
                                                <span>Metadata completeness</span>
                                                <strong>{trustEngine?.confidence_breakdown?.metadata_completeness ?? "-"}</strong>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="card shadow-sm border-0 mt-4">
                        <div className="card-body">
                            <h5 className="card-title">Document Information</h5>
                            <div className="row gy-3">
                                <div className="col-md-6"><strong>File name</strong><div>{verificationReport?.document_information?.file_name}</div></div>
                                <div className="col-md-6"><strong>File type</strong><div>{verificationReport?.document_information?.file_type}</div></div>
                                <div className="col-md-6"><strong>Upload date</strong><div>{verificationReport?.document_information?.upload_date}</div></div>
                                <div className="col-md-6"><strong>File size</strong><div>{verificationReport?.document_information?.file_size}</div></div>
                                <div className="col-md-6"><strong>Processing time</strong><div>{trustEngine?.confidence_breakdown?.processing_time_ms || 0} ms</div></div>
                            </div>
                        </div>
                    </div>

                    <div className="card shadow-sm border-0 mt-4">
                        <div className="card-body">
                            <h5 className="card-title">OCR Results</h5>
                            <div className="mb-3">
                                <div className="fw-semibold">Extracted Text</div>
                                <div className="text-muted" style={{ whiteSpace: "pre-wrap" }}>
                                    {verificationReport?.ocr_results?.extracted_text || "No OCR text available for this document."}
                                </div>
                            </div>
                            <div className="row gy-3">
                                <div className="col-md-6"><strong>OCR confidence</strong><div>{verificationReport?.ocr_results?.ocr_confidence}</div></div>
                                <div className="col-md-6"><strong>Detected language</strong><div>{verificationReport?.ocr_results?.detected_language}</div></div>
                            </div>
                        </div>
                    </div>

                    <div className="card shadow-sm border-0 mt-4">
                        <div className="card-body">
                            <h5 className="card-title">Metadata Analysis</h5>
                            <div className="row gy-3">
                                <div className="col-md-6"><strong>Creation date</strong><div>{verificationReport?.metadata_analysis?.creation_date}</div></div>
                                <div className="col-md-6"><strong>Modification date</strong><div>{verificationReport?.metadata_analysis?.modification_date}</div></div>
                                <div className="col-md-6"><strong>Author</strong><div>{verificationReport?.metadata_analysis?.author}</div></div>
                                <div className="col-md-6"><strong>Producer</strong><div>{verificationReport?.metadata_analysis?.producer}</div></div>
                            </div>
                            <div className="mt-3">
                                <strong>Metadata anomalies</strong>
                                <div>{verificationReport?.metadata_analysis?.metadata_anomalies?.length ? verificationReport.metadata_analysis.metadata_anomalies.join(", ") : "None detected"}</div>
                            </div>
                        </div>
                    </div>

                    <div className="card shadow-sm border-0 mt-4">
                        <div className="card-body">
                            <h5 className="card-title">Classification & QR Verification</h5>
                            <div className="row gy-3">
                                <div className="col-md-6">
                                    <strong>Predicted document type</strong>
                                    <div>{verificationReport?.document_classification?.predicted_document_type}</div>
                                </div>
                                <div className="col-md-6">
                                    <strong>Confidence score</strong>
                                    <div>{verificationReport?.document_classification?.confidence_score}</div>
                                </div>
                                <div className="col-md-6">
                                    <strong>QR detected</strong>
                                    <div>{verificationReport?.qr_verification?.qr_detected ? "Yes" : "No"}</div>
                                </div>
                                <div className="col-md-6">
                                    <strong>Validation result</strong>
                                    <div>{verificationReport?.qr_verification?.validation_result}</div>
                                </div>
                                <div className="col-md-6">
                                    <strong>Confidence</strong>
                                    <div>{verificationReport?.qr_verification?.confidence}</div>
                                </div>
                                <div className="col-md-6">
                                    <strong>Detection method</strong>
                                    <div>{verificationReport?.qr_verification?.detection_method}</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="card shadow-sm border-0 mt-4">
                        <div className="card-body">
                            <div className="d-flex justify-content-between align-items-center mb-3">
                                <h5 className="card-title mb-0">Digital Signature Verification</h5>
                                <span className={`badge bg-${report?.signature_verification?.signed ? (report.signature_verification.verification_status === "Valid" ? "success" : "warning") : "secondary"}`}>
                                    {report?.signature_verification?.signed ? (report.signature_verification.verification_status || "Unknown") : "Not Signed"}
                                </span>
                            </div>
                            <div className="row gy-3">
                                <div className="col-md-6"><strong>Signed</strong><div>{report?.signature_verification?.signed ? "Yes" : "No"}</div></div>
                                <div className="col-md-6"><strong>Verification Status</strong><div>{report?.signature_verification?.verification_status || "Unknown"}</div></div>
                                <div className="col-md-6"><strong>Certificate Validity</strong><div>{report?.signature_verification?.certificate_valid === true ? "Valid" : report?.signature_verification?.certificate_valid === false ? "Expired" : "Unknown"}</div></div>
                                <div className="col-md-6"><strong>Signer Name</strong><div>{report?.signature_verification?.signer_name || "Not available"}</div></div>
                                <div className="col-md-6"><strong>Issuer</strong><div>{report?.signature_verification?.issuer || "Not available"}</div></div>
                                <div className="col-md-6"><strong>Signing Time</strong><div>{report?.signature_verification?.signing_time || "Not available"}</div></div>
                                <div className="col-md-6"><strong>Signature Algorithm</strong><div>{report?.signature_verification?.signature_algorithm || "Not available"}</div></div>
                                <div className="col-md-6"><strong>Hash Algorithm</strong><div>{report?.signature_verification?.hash_algorithm || "Not available"}</div></div>
                                <div className="col-md-6"><strong>Number of Signatures</strong><div>{report?.signature_verification?.signature_count ?? 0}</div></div>
                                <div className="col-md-12"><strong>Verification Message</strong><div>{report?.signature_verification?.verification_message || "No message available."}</div></div>
                            </div>
                        </div>
                    </div>

                    <div className="card shadow-sm border-0 mt-4 mb-4">
                        <div className="card-body">
                            <div className="d-flex justify-content-between align-items-center mb-3">
                                <h5 className="card-title mb-0">Document Fraud Analysis</h5>
                                <span className={`badge bg-${fraudEngine?.fraud_score >= 60 ? "danger" : fraudEngine?.fraud_score >= 35 ? "warning" : "success"}`}>
                                    {fraudEngine?.risk_level || "Pending"}
                                </span>
                            </div>
                            <div className="row align-items-center">
                                <div className="col-md-4 text-center py-3">
                                    <div className={`display-6 fw-bold ${fraudEngine?.fraud_score >= 60 ? "text-danger" : fraudEngine?.fraud_score >= 35 ? "text-warning" : "text-success"}`}>
                                        {Math.round(fraudEngine?.fraud_score || 0)}
                                    </div>
                                    <div className="text-muted">Fraud Score</div>
                                </div>
                                <div className="col-md-8">
                                    <div className="progress" style={{ height: "10px" }}>
                                        <div className={`progress-bar ${fraudEngine?.fraud_score >= 60 ? "bg-danger" : fraudEngine?.fraud_score >= 35 ? "bg-warning" : "bg-success"}`} style={{ width: `${fraudEngine?.fraud_score || 0}%` }} />
                                    </div>
                                    <div className="mt-2 text-muted">Confidence: {fraudEngine?.confidence ?? "-"}</div>
                                </div>
                            </div>
                            <div className="mt-4">
                                <h6 className="fw-semibold">Passed checks</h6>
                                <ul className="mb-0">
                                    {(fraudEngine?.passed_checks || []).length ? fraudEngine.passed_checks.map((item) => <li key={item}><span className="text-success">✓</span> {item}</li>) : <li>No passed checks recorded.</li>}
                                </ul>
                            </div>
                            <div className="row mt-4 g-3">
                                <div className="col-md-6">
                                    <h6 className="fw-semibold">Warnings</h6>
                                    <ul className="mb-0">
                                        {(fraudEngine?.warnings || []).length ? fraudEngine.warnings.map((item) => <li key={item}><span className="text-warning">⚠</span> {item}</li>) : <li>No warnings.</li>}
                                    </ul>
                                </div>
                                <div className="col-md-6">
                                    <h6 className="fw-semibold">Failed checks</h6>
                                    <ul className="mb-0">
                                        {(fraudEngine?.failed_checks || []).length ? fraudEngine.failed_checks.map((item) => <li key={item}><span className="text-danger">✕</span> {item}</li>) : <li>No failed checks.</li>}
                                    </ul>
                                </div>
                            </div>
                            <div className="mt-4">
                                <h6 className="fw-semibold">Recommended action</h6>
                                <div>{fraudEngine?.recommended_action || "No action available."}</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-lg-4">
                    <div className="card shadow-sm border-0">
                        <div className="card-body">
                            <h5 className="card-title">Final Decision</h5>
                            <div className="mb-3">
                                {renderBadge(verificationReport?.final_decision || "Pending", scoreTone === "success" ? "success" : scoreTone === "warning" ? "warning" : "danger")}
                            </div>
                            <div className="mb-3">
                                <div className="fw-semibold">AI Trust Score</div>
                                <div className={scoreClass}>{verificationReport?.ai_trust_score?.overall_score ?? summary?.score ?? report.trust_score}/100</div>
                            </div>
                            <div className="mb-3">
                                <div className="fw-semibold">Risk Level</div>
                                <div>{verificationReport?.ai_trust_score?.risk_level}</div>
                            </div>
                            <div className="mb-3">
                                <div className="fw-semibold">Suspicious Indicators</div>
                                <div>{verificationReport?.ai_trust_score?.suspicious_indicators?.join(", ") || "None"}</div>
                            </div>
                            <div>
                                <div className="fw-semibold">Confidence</div>
                                <div>{verificationReport?.ai_trust_score?.confidence}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="d-flex gap-3 mt-4 flex-wrap">
                <Link to="/documents" className="btn btn-outline-primary">
                    Back to Documents
                </Link>
                <button type="button" className="btn btn-outline-secondary" onClick={handlePrint}>
                    Print Report
                </button>
                <button type="button" className="btn btn-primary" onClick={handleDownload}>
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
