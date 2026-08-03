import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import Loader from "../components/Loader";
import documentService from "../services/documentService";

function Documents() {
    const navigate = useNavigate();
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const loadDocuments = async () => {
        try {
            setError("");
            setLoading(true);
            const response = await documentService.getDocuments();
            setDocuments(response.documents || []);
        } catch (error) {
            console.error(error);
            setError("Unable to load documents. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const fetchDocuments = async () => {
            await loadDocuments();
        };

        fetchDocuments();
    }, []);

    const handleDelete = async (id) => {
        if (!window.confirm("Delete this document?")) return;

        try {
            await documentService.deleteDocument(id);
            await loadDocuments();
        } catch (error) {
            console.error(error);
            setError("Unable to delete document. Please try again.");
        }
    };

    return (
        <Layout>
            <div className="dashboard-title">
                <h2>Document repository</h2>
                <p>Review your full review history and manage every submission.</p>
            </div>

            <div className="table-container">
                {error && (
                    <div className="alert alert-danger" role="alert">
                        {error}
                    </div>
                )}

                <div className="mb-3 d-flex justify-content-between align-items-center flex-wrap gap-2">
                    <div>
                        {loading ? (
                            <span className="text-muted">Loading documents…</span>
                        ) : (
                            <span className="badge-soft">{documents.length} documents loaded</span>
                        )}
                    </div>
                    <button className="btn btn-outline-primary btn-sm" onClick={loadDocuments} disabled={loading}>
                        Refresh
                    </button>
                </div>

                {loading ? (
                    <Loader />
                ) : (
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>File name</th>
                                <th>Type</th>
                                <th>Uploaded</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {documents.length === 0 ? (
                                <tr>
                                    <td colSpan="5" className="text-center py-4 text-muted">
                                        No documents found.
                                    </td>
                                </tr>
                            ) : (
                                documents.map((doc) => (
                                    <tr key={doc.id}>
                                        <td>{doc.id}</td>
                                        <td>{doc.original_filename}</td>
                                        <td>{doc.file_type}</td>
                                        <td>{doc.uploaded_at}</td>
                                        <td>
                                            <div className="d-flex gap-2 flex-wrap">
                                                <button className="btn btn-primary btn-sm" onClick={() => navigate(`/report/${doc.id}`)}>
                                                    View report
                                                </button>
                                                <button className="btn btn-outline-danger btn-sm" onClick={() => handleDelete(doc.id)}>
                                                    Delete
                                                </button>
                                            </div>
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

export default Documents;