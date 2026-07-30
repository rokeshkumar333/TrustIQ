import { useEffect, useState } from "react";
import Layout from "../components/Layout";
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
                <h2>Document Classification</h2>
                <p>AI-assisted categorization of uploaded documents</p>
            </div>

            <div className="table-container">
                <table className="table table-bordered">
                    <thead>
                        <tr>
                            <th>Document</th>
                            <th>Category</th>
                            <th>Confidence</th>
                        </tr>
                    </thead>
                    <tbody>
                        {loading ? (
                            <tr>
                                <td colSpan="3" className="text-center">Loading...</td>
                            </tr>
                        ) : items.length === 0 ? (
                            <tr>
                                <td colSpan="3" className="text-center">No classifications available.</td>
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
            </div>
        </Layout>
    );
}

export default Classification;
