import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import authService from "../services/authService";

function Register() {

    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: ""
    });

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    const [success, setSuccess] = useState("");

    const handleChange = (e) => {

        setFormData({

            ...formData,

            [e.target.name]: e.target.value

        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        setLoading(true);

        setError("");

        setSuccess("");

        try {

            await authService.register(formData);

            setSuccess("Registration Successful");

            setTimeout(() => {

                navigate("/login");

            }, 1000);

        } catch (err) {

            setError(

                err.response?.data?.message ||

                "Registration Failed"

            );

        } finally {

            setLoading(false);

        }

    };

    return (

        <div className="container mt-5">

            <div className="row justify-content-center">

                <div className="col-md-6">

                    <div className="card shadow">

                        <div className="card-body">

                            <h2 className="text-center mb-4">

                                Create Account

                            </h2>

                            {error &&

                                <div className="alert alert-danger">

                                    {error}

                                </div>

                            }

                            {success &&

                                <div className="alert alert-success">

                                    {success}

                                </div>

                            }

                            <form onSubmit={handleSubmit}>

                                <div className="mb-3">

                                    <label>Name</label>

                                    <input

                                        type="text"

                                        className="form-control"

                                        name="username"

                                        value={formData.username}

                                        onChange={handleChange}

                                        required

                                    />

                                </div>

                                <div className="mb-3">

                                    <label>Email</label>

                                    <input

                                        type="email"

                                        className="form-control"

                                        name="email"

                                        value={formData.email}

                                        onChange={handleChange}

                                        required

                                    />

                                </div>

                                <div className="mb-3">

                                    <label>Password</label>

                                    <input

                                        type="password"

                                        className="form-control"

                                        name="password"

                                        value={formData.password}

                                        onChange={handleChange}

                                        required

                                    />

                                </div>

                                <button

                                    className="btn btn-success w-100"

                                    disabled={loading}

                                >

                                    {loading ? "Creating..." : "Register"}

                                </button>

                            </form>

                            <div className="text-center mt-3">

                                Already have an account?

                                <Link to="/login">

                                    {" "}Login

                                </Link>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default Register;