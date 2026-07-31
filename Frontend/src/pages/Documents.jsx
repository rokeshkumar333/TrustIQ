import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
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

                <h2>Documents</h2>

                <p>Uploaded document history</p>

            </div>

            <div className="table-container">

                {error && (
                    <div className="alert alert-danger" role="alert">
                        {error}
                    </div>
                )}

                <div className="mb-3 d-flex justify-content-between align-items-center">
                    <div>
                        {loading ? (
                            <span>Loading documents...</span>
                        ) : (
                            <span>{documents.length} documents loaded</span>
                        )}
                    </div>
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={loadDocuments}
                        disabled={loading}
                    >
                        Refresh
                    </button>
                </div>

                {loading ? (
                    <h4>Loading...</h4>
                ) : (
                    <table className="table table-striped table-bordered">

                            <thead>

                                <tr>

                                    <th>ID</th>
                                    <th>File Name</th>
                                    <th>Type</th>
                                    <th>Uploaded</th>
                                    <th>Actions</th>

                                </tr>

                            </thead>

                            <tbody>

                                {

                                    documents.length === 0 ?

                                    (

                                        <tr>

                                            <td colSpan="5" className="text-center">

                                                No Documents Found

                                            </td>

                                        </tr>

                                    ) :

                                    (

                                        documents.map((doc) => (

                                            <tr key={doc.id}>

                                                <td>{doc.id}</td>

                                                <td>{doc.original_filename}</td>

                                                <td>{doc.file_type}</td>

                                                <td>{doc.uploaded_at}</td>

                                                <td>

                                                    <button
                                                        className="btn btn-primary btn-sm me-2"
                                                        onClick={() => navigate(`/report/${doc.id}`)}
                                                    >
                                                        View Report
                                                    </button>

                                                    <button
                                                        className="btn btn-danger btn-sm"
                                                        onClick={() => handleDelete(doc.id)}
                                                    >
                                                        Delete
                                                    </button>

                                                </td>

                                            </tr>

                                        ))

                                    )

                                }

                            </tbody>

                        </table>

                    )

                }

            </div>

        </Layout>

    );

}

export default Documents;