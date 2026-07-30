import { useEffect, useMemo, useState } from "react";
import { useParams, Link } from "react-router-dom";
import Layout from "../components/Layout";
import documentService from "../services/documentService";

function Report() {
    const { id } = useParams();
    const [document, setDocument] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadReport = async () => {
            try {
                setLoading(true);
                const response = await documentService.getDocument(id);
                setDocument(response.document);
            } catch (err) {
                console.error(err);
                setError("Unable to load the document report.");
            } finally {
                setLoading(false);
            }
        };

        loadReport();
    }, [id]);

    const scoreClass = useMemo(() => {
        if (!document) return "";

        if (document.status === "Verified") return "status-good";
        if (document.status === "Needs Manual Review") return "status-review";
        return "text-danger";
    }, [document]);

    if (loading) {
        return (
            <Layout>
                <div className="dashboard-title">
                    <h2>Document Report</h2>
                    <p>Loading report details...</p>
                </div>
            </Layout>
        );
    }

    if (error || !document) {
        return (
            <Layout>
                <div className="dashboard-title">
                    <h2>Document Report</h2>
                    <p className="text-danger">{error || "No document found."}</p>
                    <Link to="/documents" className="btn btn-outline-primary mt-3">
                        Back to Documents
                    </Link>
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="dashboard-title">
                <h2>Document Report</h2>
                <p>Verification summary for {document.original_filename}</p>
            </div>

            <div className="table-container">
                <div className="row g-4">
                    <div className="col-md-6">
                        <div className="card shadow-sm">
                            <div className="card-body">
                                <h5 className="card-title">Document Summary</h5>
                                <table className="table table-borderless mb-0">
                                    <tbody>
                                        <tr>
                                            <th>File Name</th>
                                            <td>{document.original_filename}</td>
                                        </tr>
                                        <tr>
                                            <th>Type</th>
                                            <td>{document.file_type}</td>
                                        </tr>
                                        <tr>
                                            <th>Uploaded</th>
                                            <td>{document.uploaded_at}</td>
                                        </tr>
                                        <tr>
                                            <th>Trust Score</th>
                                            <td className={scoreClass}>{document.trust_score}%</td>
                                        </tr>
                                        <tr>
                                            <th>Status</th>
                                            <td className={scoreClass}>{document.status}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-6">
                        <div className="card shadow-sm">
                            <div className="card-body">
                                <h5 className="card-title">Extracted Fields</h5>
                                <pre className="mb-0" style={{ whiteSpace: "pre-wrap" }}>
                                    {JSON.stringify(document.fields || {}, null, 2)}
                                </pre>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="card shadow-sm mt-4">
                    <div className="card-body">
                        <h5 className="card-title">OCR Preview</h5>
                        <p className="mb-0" style={{ whiteSpace: "pre-wrap" }}>
                            {document.ocr_text || "No OCR text available for this document."}
                        </p>
                    </div>
                </div>

                <Link to="/documents" className="btn btn-outline-primary mt-4">
                    Back to Documents
                </Link>
            </div>
        </Layout>
    );
}

export default Report;