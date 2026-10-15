/**
 * Módulo: App.jsx
 * Descripción: Define el componente principal de la aplicación,
 *              gestiona las rutas, comprueba el estado de autenticación
 *              y aplica las restricciones de acceso según el rol.
 * Autor: Raquel Del Castillo Pérez
 */

import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./auth/AuthContext";
import { useTranslation } from "react-i18next";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Evaluation from "./pages/Evaluation";
import Recommendations from "./pages/Recommendations";
import TeacherQuestions from "./pages/TeacherQuestions";
import TeacherResources from "./pages/TeacherResources";
import UserManagement from "./pages/UserManagement";

import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import Loader from "./components/Loader";


/**
 * Componente raíz de la aplicación.
 *
 * Muestra un indicador de carga mientras se comprueba la sesión.
 * Cuando finaliza la comprobación, renderiza la barra de navegación
 * y configura las rutas públicas y protegidas de la aplicación.
 *
 * @returns {JSX.Element} Estructura principal y sistema de rutas.
 */
export default function App() {
    const { loading } = useAuth();
    const { t } = useTranslation();

    if (loading) {
        return (
            <Loader
                text={t("loadingSession", { ns: "common" })}
            />
        );
    }

    return (
        <>
            <Navbar />

            <Routes>

                 <Route
                    path="/"
                    element={
                        <Navigate
                            to={
                                localStorage.getItem("token")
                                    ? "/dashboard"
                                    : "/login"
                            }
                        />
                    }
                />

                <Route path="/login" element={<Login />} />

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/evaluation"
                    element={
                        <ProtectedRoute>
                            <Evaluation />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/recommendations"
                    element={
                        <ProtectedRoute>
                            <Recommendations />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/teacher/questions"
                    element={
                        <ProtectedRoute roles={["teacher", "admin"]}>
                            <TeacherQuestions />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/teacher/resources"
                    element={
                        <ProtectedRoute roles={["teacher", "admin"]}>
                            <TeacherResources />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/users"
                    element={
                        <ProtectedRoute roles={["admin"]}>
                            <UserManagement />
                        </ProtectedRoute>
                    }
                />

                <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
        </>
    );
}