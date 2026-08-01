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

    const renderBadge = (value, variant = "secondary") => (
        <span className={`badge bg-${variant}`}>{value}</span>
    );

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
                                <h5 className="card-title mb-0">Trust Score Overview</h5>
                                <span className={`badge bg-${scoreTone} fs-6`}>{summary?.score ?? report.trust_score}/100</span>
                            </div>
                            <div className="progress" style={{ height: "12px" }}>
                                <div
                                    className={`progress-bar bg-${scoreTone}`}
                                    role="progressbar"
                                    style={{ width: `${summary?.score ?? report.trust_score}%` }}
                                />
                            </div>
                            <div className="mt-2 text-muted">Risk level: {summary?.risk_level || "Unknown"}</div>
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

                    <div className="card shadow-sm border-0 mt-4 mb-4">
                        <div className="card-body">
                            <h5 className="card-title">Fraud Detection Summary</h5>
                            <div className="row gy-3">
                                <div className="col-md-6">
                                    <strong>Tampering indicators</strong>
                                    <div>{verificationReport?.fraud_detection_summary?.tampering_indicators?.join(", ") || "None"}</div>
                                </div>
                                <div className="col-md-6">
                                    <strong>Missing metadata</strong>
                                    <div>{verificationReport?.fraud_detection_summary?.missing_metadata?.join(", ") || "None"}</div>
                                </div>
                                <div className="col-md-6">
                                    <strong>OCR inconsistencies</strong>
                                    <div>{verificationReport?.fraud_detection_summary?.ocr_inconsistencies?.join(", ") || "None"}</div>
                                </div>
                                <div className="col-md-6">
                                    <strong>Invalid QR</strong>
                                    <div>{verificationReport?.fraud_detection_summary?.invalid_qr?.join(", ") || "None"}</div>
                                </div>
                                <div className="col-md-12">
                                    <strong>Suspicious patterns</strong>
                                    <div>{verificationReport?.fraud_detection_summary?.suspicious_patterns?.join(", ") || "None"}</div>
                                </div>
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
