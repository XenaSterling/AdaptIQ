/**
 * Módulo: eslint.config.js
 * Descripción: Configura ESLint para analizar el código JavaScript
 *              y JSX del proyecto, aplicando las reglas recomendadas
 *              de JavaScript, React Hooks y React Refresh.
 */


import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'


/**
 * Configuración principal de ESLint.
 *
 * Ignora los archivos generados en dist y aplica las reglas
 * recomendadas a los ficheros JavaScript y JSX del proyecto.
 */
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
  },
])
