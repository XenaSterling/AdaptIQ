/**
 * Módulo: Dashboard.jsx
 * Descripción: Obtiene los datos del panel de control del usuario
 *              autenticado y muestra el dashboard correspondiente
 *              según su rol: estudiante, profesor o administrador.
 * Autor: Raquel Del Castillo Pérez
 */

import { useEffect, useState } from "react";
import api from "../api/axios";
import Loader from "../components/Loader";

import StudentDashboard from "./StudentDashboard";
import TeacherDashboard from "./TeacherDashboard";
import AdminDashboard from "./AdminDashboard";

import { useAuth } from "../auth/AuthContext";
import { useTranslation } from "react-i18next";


/**
 * Gestiona la carga y visualización del dashboard del usuario.
 *
 * @returns {JSX.Element} Panel de control correspondiente al rol.
 */
export default function Dashboard() {
    const { user } = useAuth();
    const { t } = useTranslation();
    const [data, setData] = useState(null);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!user) return;
        loadDashboard();
    }, [user]);

    const loadDashboard = async () => {
        try {
            let url = "";

            switch (user.role) {
                case "student":
                    url = `/dashboard/student/${user.userId}`;
                    break;

                case "teacher":
                    url = "/dashboard/teacher";
                    break;

                case "admin":
                    url = "/dashboard/admin";
                    break;

                default:
                    setError("Unknown role");
                    return;
            }

            const res = await api.get(url);
            setData(res.data);

        } catch (err) {
            setError(err?.response?.data?.detail || "Failed to load dashboard");
        }
    };

    if (error) {
        return (
            <div className="container">
                <div className="card">
                    <h2>Error</h2>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    if (!data) {
        return <Loader
            text={t("loadingDashboard", { ns: "common" })}
        />;
    }

    switch (user.role) {
        case "student":
            return <StudentDashboard data={data} />;
        case "teacher":
            return <TeacherDashboard data={data} />;
        case "admin":
            return <AdminDashboard data={data} />;
        default:
            return <div>Unknown role</div>;
    }
}