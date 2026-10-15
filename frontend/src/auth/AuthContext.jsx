/**
 * Módulo: AuthContext.jsx
 * Descripción: Proporciona el contexto de autenticación de la
 *              aplicación, gestionando el usuario, el inicio
 *              y cierre de sesión y el estado de carga inicial.
 * Autor: Raquel Del Castillo Pérez
 */

import { createContext, useContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext();


/**
 * Proporciona el estado y las operaciones de autenticación
 * a los componentes descendientes.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {React.ReactNode} props.children - Componentes descendientes.
 * @returns {JSX.Element} Proveedor del contexto de autenticación.
 */
export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("token");

        if (!token) {
            setLoading(false);
            return;
        }

        try {
            const decoded = jwtDecode(token);

            setUser({
                token,
                userId: decoded.sub,
                role: decoded.role,
            });

        } catch (err) {
            localStorage.clear();
            setUser(null);
        }

        setLoading(false);
    }, []);

    const login = ({ token }) => {
        localStorage.setItem("token", token);

        const decoded = jwtDecode(token);

        setUser({
            token,
            userId: decoded.sub,
            role: decoded.role,
        });
    };

    const logout = () => {
        localStorage.clear();
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
}


/**
 * Permite acceder al contexto de autenticación.
 *
 * @returns {Object} Usuario autenticado, operaciones de sesión
 *                   y estado de carga.
 */
export const useAuth = () => useContext(AuthContext);