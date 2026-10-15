/**
 * Módulo: useLanguage.js
 * Descripción: Proporciona un hook para consultar y modificar el idioma
 *              actual de la aplicación.
 *              Utiliza la instancia de i18next para cambiar el idioma
 *              activo y guarda la preferencia seleccionada en localStorage,
 *              permitiendo conservarla durante futuras visitas.
 * Autor: Raquel Del Castillo Pérez
 */

import i18n from "./index";


/**
 * Hook para gestionar el idioma de la aplicación.
 *
 * Proporciona el idioma actual y una función para cambiarlo.
 * La preferencia seleccionada se guarda en el almacenamiento local
 * del navegador.
 *
 * @returns {Object} Objeto con el idioma actual y la función de cambio.
 * @returns {string} returns.currentLanguage - Idioma activo.
 * @returns {Function} returns.changeLanguage - Cambia y guarda el idioma.
 */
export const useLanguage = () => {
  const changeLanguage = (lang) => {
    i18n.changeLanguage(lang);
    localStorage.setItem("lang", lang);
  };

  return {
    currentLanguage: i18n.language,
    changeLanguage,
  };
};