/**
 * Módulo: Login.jsx
 * Descripción: Gestiona el inicio de sesión de los usuarios mediante
 *              la API de autenticación y redirige al dashboard
 *              cuando las credenciales son válidas.
 * Autor: Raquel Del Castillo Pérez
 */

import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import api from "../api/axios";
import { useAuth } from "../auth/AuthContext";


/**
 * Renderiza el formulario de inicio de sesión.
 *
 * @returns {JSX.Element} Formulario de autenticación.
 */
export default function Login() {
    const navigate = useNavigate();
    const { login, user } = useAuth();
    const { t } = useTranslation(["login", "common"]);

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    if (user) {
        return <Navigate to="/dashboard" />;
    }


    /**
   * Valida las credenciales mediante la API e inicia la sesión.
   *
   * @param {Event} e - Evento de envío del formulario.
   * @returns {Promise<void>}
   */
    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const res = await api.post("/auth/login", {
                email,
                password,
            });

            login({
                token: res.data.access_token,
            });

            navigate("/dashboard");

        } catch (err) {
            setError(t("invalidCredentials", { ns: "common" }));
        }
    };

    return (
        <div className="page-center">
            <form className="card login-card" onSubmit={handleLogin}>
                <h1>{t("adaptivePlatformTitle")}</h1>

                <input
                    type="email"
                    placeholder={t("email")}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />

                <input
                    type="password"
                    placeholder={t("password")}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />

                <button type="submit">{t("login")}</button>

                {error && <p className="error">{error}</p>}
            </form>
        </div>
    );
}