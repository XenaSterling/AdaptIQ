/**
 * Módulo: main.jsx
 * Descripción: Punto de entrada de la aplicación React.
 *              Inicializa el árbol de componentes, configura el enrutamiento,
 *              proporciona el contexto de autenticación e importa
 *              los estilos globales y la configuración de internacionalización.
 * Autor: Raquel Del Castillo Pérez
 */

import React from "react";
import ReactDOM from "react-dom/client";

import { HashRouter } from "react-router-dom";
import App from "./App";
import { AuthProvider } from "./auth/AuthContext";

import "./styles/app.css";
import "./i18n";


/**
 * Inicializa y renderiza la aplicación React.
 *
 * Configura HashRouter para gestionar la navegación mediante fragmentos
 * de URL y AuthProvider para compartir el estado de autenticación
 * con los componentes descendientes.
 *
 * @returns {void}
 */
ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <HashRouter>
            <AuthProvider>
                <App />
            </AuthProvider>
        </HashRouter>
    </React.StrictMode>
);