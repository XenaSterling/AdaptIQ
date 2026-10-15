/**
 * Módulo: axios.js
 * Descripción: Configura la instancia de Axios para las peticiones
 *              a la API e incorpora el token de autenticación
 *              en las cabeceras de las solicitudes.
 *              OPC 2: baseURL: "http://localhost:8000",
 * Autor: Raquel Del Castillo Pérez
 */

import axios from "axios";


const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

/**
 * Añade el token de autenticación a las solicitudes HTTP.
 */
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default api;