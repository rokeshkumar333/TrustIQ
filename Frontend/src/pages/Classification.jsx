import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import Loader from "../components/Loader";
import api from "../api/api";

function Classification() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadClassification = async () => {
            try {
                const response = await api.get("/classification");
                setItems(response.data.classifications || []);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        loadClassification();
    }, []);

    return (
        <Layout>
            <div className="dashboard-title">
                <h2>Document classification</h2>
                <p>AI-assisted categorization of uploaded documents</p>
            </div>

            <div className="table-container">
                <div className="d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <h4 className="mb-1">Classification results</h4>
                        <p className="text-muted mb-0">Confidence scores for each predicted category</p>
                    </div>
                    <span className="badge-soft">AI-assisted</span>
                </div>
                {loading ? (
                    <Loader />
                ) : (
                    <table>
                        <thead>
                            <tr>
                                <th>Document</th>
                                <th>Category</th>
                                <th>Confidence</th>
                            </tr>
                        </thead>
                        <tbody>
                            {items.length === 0 ? (
                                <tr>
                                    <td colSpan="3" className="text-center py-4 text-muted">No classifications available.</td>
                                </tr>
                            ) : (
                                items.map((item) => (
                                    <tr key={item.id || item.original_filename}>
                                        <td>{item.original_filename}</td>
                                        <td>{item.category}</td>
                                        <td>{item.confidence}</td>
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

export default Classification;
