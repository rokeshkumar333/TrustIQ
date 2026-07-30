import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import api from "../api/api";

function QRVerification() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadVerification = async () => {
            try {
                const response = await api.get("/qr-verification");
                setItems(response.data.verifications || []);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        loadVerification();
    }, []);

    return (
        <Layout>
            <div className="dashboard-title">
                <h2>QR Verification</h2>
                <p>Verification markers detected during document analysis</p>
            </div>

            <div className="table-container">
                <table className="table table-bordered">
                    <thead>
                        <tr>
                            <th>Document</th>
                            <th>Status</th>
                            <th>Method</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        {loading ? (
                            <tr>
                                <td colSpan="4" className="text-center">Loading...</td>
                            </tr>
                        ) : items.length === 0 ? (
                            <tr>
                                <td colSpan="4" className="text-center">No verification results available.</td>
                            </tr>
                        ) : (
                            items.map((item) => (
                                <tr key={item.id || item.original_filename}>
                                    <td>{item.original_filename}</td>
                                    <td>{item.verified ? "Verified" : "Pending"}</td>
                                    <td>{item.method}</td>
                                    <td>{item.message}</td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </Layout>
    );
}

export default QRVerification;
