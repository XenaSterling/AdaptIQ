/**
 * Módulo: jwt.js
 * Descripción: Proporciona utilidades para obtener y decodificar
 *              el contenido del token JWT almacenado en la sesión.
 * Autor: Raquel Del Castillo Pérez
 */

import { jwtDecode } from "jwt-decode";


/**
 * Obtiene el contenido del token JWT almacenado.
 *
 * @returns {Object|null} Contenido decodificado del token o null
 *                        si no existe o no se puede decodificar.
 */
export function getTokenPayload() {
  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    return jwtDecode(token);
  } catch {
    return null;
  }
}