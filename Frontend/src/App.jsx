import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Documents from "./pages/Documents";
import Report from "./pages/Report";
import Analytics from "./pages/Analytics";
import Classification from "./pages/Classification";
import QRVerification from "./pages/QRVerification";
import NotFound from "./pages/NotFound";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
    return (
        <Routes>

            <Route path="/" element={<Navigate to="/login" />} />

            <Route path="/login" element={<Login />} />

            <Route path="/register" element={<Register />} />

            <Route
                path="/dashboard"
                element={
                    <ProtectedRoute>
                        <Dashboard />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/upload"
                element={
                    <ProtectedRoute>
                        <Upload />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/documents"
                element={
                    <ProtectedRoute>
                        <Documents />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/report/:id"
                element={
                    <ProtectedRoute>
                        <Report />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/analytics"
                element={
                    <ProtectedRoute>
                        <Analytics />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/classification"
                element={
                    <ProtectedRoute>
                        <Classification />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/qr-verification"
                element={
                    <ProtectedRoute>
                        <QRVerification />
                    </ProtectedRoute>
                }
            />

            <Route path="*" element={<NotFound />} />

        </Routes>
    );
}

export default App;