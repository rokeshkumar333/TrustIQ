import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import documentService from "../services/documentService";

function Documents() {

    const navigate = useNavigate();
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDocuments();
    }, []);

    const loadDocuments = async () => {

        try {

            const response = await documentService.getDocuments();

            setDocuments(response.documents || []);

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }

    };

    const handleDelete = async (id) => {

        if (!window.confirm("Delete this document?")) return;

        try {

            await documentService.deleteDocument(id);

            loadDocuments();

        } catch (error) {

            console.error(error);

            alert("Unable to delete document");

        }

    };

    return (

        <Layout>

            <div className="dashboard-title">

                <h2>Documents</h2>

                <p>Uploaded document history</p>

            </div>

            <div className="table-container">

                {

                    loading ?

                    (

                        <h4>Loading...</h4>

                    ) :

                    (

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