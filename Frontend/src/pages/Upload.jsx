import { useState } from "react";
import Layout from "../components/Layout";

function Upload() {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (e) => {
        if (e.target.files.length > 0) {
            setSelectedFile(e.target.files[0]);
        }
    };

    const handleUpload = () => {
        if (!selectedFile) {
            alert("Please select a document.");
            return;
        }

        // Backend API integration will be added next
        alert(`Uploading: ${selectedFile.name}`);
    };

    return (
        <Layout>
            <div className="dashboard-title">
                <h2>Upload Document</h2>
                <p>Upload a document for TrustIQ verification.</p>
            </div>

            <div className="table-container">

                <div className="mb-4">

                    <label className="form-label fw-bold">
                        Choose Document
                    </label>

                    <input
                        type="file"
                        className="form-control"
                        accept=".pdf,.png,.jpg,.jpeg"
                        onChange={handleFileChange}
                    />

                </div>

                {selectedFile && (
                    <div className="alert alert-info">

                        <strong>Selected File:</strong>

                        <br />

                        {selectedFile.name}

                    </div>
                )}

                <button
                    className="btn btn-primary"
                    onClick={handleUpload}
                >
                    Upload Document
                </button>

            </div>
        </Layout>
    );
}

export default Upload;