/**
 * Módulo: LanguageSelector.jsx
 * Descripción: Permite cambiar el idioma de la aplicación entre
 *              español e inglés.
 * Autor: Raquel Del Castillo Pérez
 */

import { useLanguage } from "../i18n/useLanguage";


/**
 * Muestra los botones para seleccionar el idioma.
 *
 * @returns {JSX.Element} Selector de idioma.
 */
export default function LanguageSelector() {
  const { currentLanguage, changeLanguage } = useLanguage();

  return (
    <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
      <button
        onClick={() => changeLanguage("es")}
        style={{
          fontWeight: currentLanguage === "es" ? "bold" : "normal",
          cursor: "pointer",
        }}
      >
        🇪🇸 ES
      </button>

      <button
        onClick={() => changeLanguage("en")}
        style={{
          fontWeight: currentLanguage === "en" ? "bold" : "normal",
          cursor: "pointer",
        }}
      >
        🇬🇧 EN
      </button>
    </div>
  );
}