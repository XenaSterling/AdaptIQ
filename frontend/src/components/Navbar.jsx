/**
 * Módulo: Navbar.jsx
 * Descripción: Muestra la barra de navegación de la aplicación
 *              según el rol del usuario autenticado. Permite cambiar
 *              el idioma y cerrar la sesión.
 * Autor: Raquel Del Castillo Pérez
 */

import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { NAV_ITEMS } from "../config/navConfig";
import { useTranslation } from "react-i18next";
import i18n from "../i18n";


/**
 * Renderiza la barra de navegación principal.
 *
 * Filtra los enlaces según el rol del usuario y proporciona
 * opciones para cambiar el idioma y cerrar la sesión.
 *
 * @returns {JSX.Element|null} Barra de navegación o null si no hay usuario.
 */
export default function Navbar() {
    const navigate = useNavigate();
    const { user, logout } = useAuth();
    const { t } = useTranslation("navbar");
    const currentLanguage = i18n.language.startsWith("es") ? "es" : "en";

    if (!user) return null;

    const role = user.role;


    /**
     * Obtiene los elementos de navegación permitidos para el rol actual.
     *
     * @type {Array<Object>}
     */
    const filteredItems = NAV_ITEMS.filter(
        (item) => item.roles.includes(role)
    );

    return (
        <nav className="navbar">
            <div className="nav-left">

                <Link to="/home">
                    {t("home")}
                </Link>

                {filteredItems.map((item) => (
                    <Link key={item.to} to={item.to}>
                        {t(item.label)}
                    </Link>
                ))}

            </div>

            <div
                style={{
                    display: "flex",
                    gap: "0.5rem",
                    alignItems: "center"
                }}
            >
                <button
                    style={{
                        minWidth: "70px"
                    }}
                    onClick={() =>
                        i18n.changeLanguage(currentLanguage === "es" ? "en" : "es")
                    }
                    title={currentLanguage === "es" ? "Switch to English" : "Cambiar a español"}
                >
                    {currentLanguage === "es" ? "EN" : "ES"}
                </button>

                <button
                    style={{
                        minWidth: "120px"
                    }}
                    onClick={() => {
                        logout();
                        navigate("/login");
                    }}
                >
                    {t("logout")}
                </button>
            </div>
        </nav>
    );
}