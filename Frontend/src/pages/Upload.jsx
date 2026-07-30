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

            setError(

                err.response?.data?.error ||

                err.response?.data?.message ||

                "Upload Failed"

            );

        } finally {

            setLoading(false);

        }

    };

    return (

        <Layout>

            <div className="dashboard-title">

                <h2>Upload Document</h2>

                <p>

                    Upload PDF, JPG, JPEG or PNG documents.

                </p>

            </div>

            <div className="table-container">

                {error && (

                    <div className="alert alert-danger">

                        {error}

                    </div>

                )}

                <div className="mb-4">

                    <label className="form-label fw-bold">

                        Select Document

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

                    disabled={loading}

                    onClick={handleUpload}

                >

                    {

                        loading ?

                        "Uploading..." :

                        "Upload Document"

                    }

                </button>

                {

                    uploadResult && (

                        <>

                            <hr />

                            <h4>

                                Upload Successful

                            </h4>

                            <br />

                            <table className="table table-bordered">

                                <tbody>

                                    <tr>

                                        <th>

                                            Original File

                                        </th>

                                        <td>

                                            {uploadResult.original_filename}

                                        </td>

                                    </tr>

                                    <tr>

                                        <th>

                                            Trust Score

                                        </th>

                                        <td>

                                            {uploadResult.trust_score}

                                        </td>

                                    </tr>

                                    <tr>

                                        <th>

                                            Status

                                        </th>

                                        <td>

                                            {uploadResult.status}

                                        </td>

                                    </tr>

                                </tbody>

                            </table>

                            <button

                                className="btn btn-success"

                                onClick={() => navigate("/documents")}

                            >

                                Go To Documents

                            </button>

                        </>

                    )

                }

            </div>

        </Layout>

    );

}

export default Upload;