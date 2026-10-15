/**
 * Módulo: ProtectedRoute.jsx
 * Descripción: Protege las rutas comprobando la autenticación
 *              del usuario y los roles autorizados para acceder.
 * Autor: Raquel Del Castillo Pérez
 */

import { Navigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";


/**
 * Controla el acceso a las rutas protegidas.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {JSX.Element} props.children - Contenido de la ruta protegida.
 * @param {Array<string>} [props.roles] - Roles autorizados para acceder.
 * @returns {JSX.Element} Contenido protegido o redirección.
 */
export default function ProtectedRoute({ children, roles }) {
    const { user } = useAuth();

    if (!user?.token) {
        return <Navigate to="/login" />;
    }

    if (roles && roles.length > 0) {
        if (!user?.role || !roles.includes(user.role)) {
            return <Navigate to="/dashboard" />;
        }
    }

    return children;
}