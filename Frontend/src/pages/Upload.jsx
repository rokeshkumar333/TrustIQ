import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import uploadService from "../services/uploadService";

function Upload() {
    const navigate = useNavigate();

    const [selectedFile, setSelectedFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [uploadResult, setUploadResult] = useState(null);
    const [error, setError] = useState("");

    const handleFileChange = (e) => {
        if (e.target.files.length > 0) {
            setSelectedFile(e.target.files[0]);
            setError("");
            setUploadResult(null);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError("Please select a document.");
            return;
        }

        try {
            setLoading(true);
            setError("");
            const response = await uploadService.uploadFile(selectedFile);
            setUploadResult(response);
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.error || err.response?.data?.message || "Upload failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <div className="dashboard-title">
                <h2>Upload document</h2>
                <p>Upload PDF, JPG, JPEG, or PNG documents for instant verification.</p>
            </div>

            <div className="table-container">
                {error && <div className="alert alert-danger">{error}</div>}

                <div className="mb-4">
                    <label className="form-label fw-bold">Select document</label>
                    <input type="file" className="form-control" accept=".pdf,.png,.jpg,.jpeg" onChange={handleFileChange} />
                </div>

                {selectedFile && (
                    <div className="alert alert-info mb-4">
                        <strong>Selected file:</strong> {selectedFile.name}
                    </div>
                )}

                <button className="btn btn-primary" disabled={loading} onClick={handleUpload}>
                    {loading ? "Uploading..." : "Upload document"}
                </button>

                {uploadResult && (
                    <div className="mt-4">
                        <h4 className="mb-3">Upload successful</h4>
                        <div className="panel-card p-3">
                            <div className="row g-3">
                                <div className="col-md-4"><strong>Original file</strong><div>{uploadResult.original_filename}</div></div>
                                <div className="col-md-4"><strong>Trust score</strong><div>{uploadResult.trust_score}</div></div>
                                <div className="col-md-4"><strong>Status</strong><div>{uploadResult.status}</div></div>
                            </div>
                        </div>
                        <button className="btn btn-success mt-3" onClick={() => navigate("/documents")}>Go to documents</button>
                    </div>
                )}
            </div>
        </Layout>
    );
}

export default Upload;