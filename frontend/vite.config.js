/**
 * Módulo: vite.config.js
 * Descripción: Configura Vite como herramienta de desarrollo
 *              y compilación de la aplicación React.
 *              Define el complemento de React y la ruta base
 *              para la generación de los recursos.
 *              Para dev: https://vite.dev/config/
 * Autor: Raquel Del Castillo Pérez
 */

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'


/**
 * Configuración de Vite.
 *
 * Registra el complemento de React y establece una ruta base relativa,
 * lo que facilita servir la aplicación desde distintas ubicaciones.
 */
export default defineConfig({
  plugins: [react()],
  base: './',
})
