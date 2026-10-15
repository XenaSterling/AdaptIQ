/**
 * Módulo: auth.js
 * Descripción: Gestiona la autenticación de los usuarios mediante
 *              la API y almacena los datos de la sesión recibidos.
 * Autor: Raquel Del Castillo Pérez
 */

import api from "../api/axios";

/**
 * Inicia sesión y almacena los datos de autenticación.
 *
 * @param {string} email - Correo electrónico del usuario.
 * @param {string} password - Contraseña del usuario.
 * @returns {Promise<Object>} Datos devueltos por la API.
 */
export async function login(email, password) {
  const res = await api.post("/auth/login", {
    email,
    password,
  });

  const { access_token, user_id, role } = res.data;

  localStorage.setItem("token", access_token);
  localStorage.setItem("user_id", user_id);
  localStorage.setItem("role", role);

  return res.data;
}