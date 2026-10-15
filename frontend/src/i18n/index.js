/**
 * Módulo: index.js
 * Descripción: Configura e inicializa el sistema de internacionalización
 *              de la aplicación mediante las librerías i18next y
 *              react-i18next.
 *              Importa los archivos de traducción en español e inglés
 *              y los organiza en espacios de nombres para las distintas
 *              secciones de la aplicación.
 *              Determina el idioma inicial a partir de la preferencia
 *              guardada en el almacenamiento local del navegador o,
 *              en su defecto, del idioma configurado en el navegador.
 *              Establece el español como idioma de reserva y configura
 *              la interpolación de textos.
 * Autor: Raquel Del Castillo Pérez
 */

import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import esCommon from "./es/common.json";
import enCommon from "./en/common.json";
import esDashboard from "./es/dashboard.json";
import enDashboard from "./en/dashboard.json";
import esTooltips from "./es/tooltips.json";
import enTooltips from "./en/tooltips.json";
import esLogin from "./es/login.json";
import enLogin from "./en/login.json";
import esTeacher from "./es/teacher.json";
import enTeacher from "./en/teacher.json";
import esAdmin from "./es/admin.json";
import enAdmin from "./en/admin.json";
import esEvaluation from "./es/evaluation.json";
import enEvaluation from "./en/evaluation.json";
import esRecommendation from "./es/recommendations.json";
import enRecommendation from "./en/recommendations.json";
import esNavBar from "./es/navbar.json";
import enNavBar from "./en/navbar.json";


const resources = {
  es: {
    common: esCommon,
    dashboard: esDashboard,
    tooltips: esTooltips,
    login: esLogin,
    teacher: esTeacher,
    admin: esAdmin,
    evaluation: esEvaluation,
    recommendations: esRecommendation,
    navbar: esNavBar
  },
  en: {
    common: enCommon,
    dashboard: enDashboard,
    tooltips: enTooltips,
    login: enLogin,
    teacher: enTeacher,
    admin: enAdmin,
    evaluation: enEvaluation,
    recommendations: enRecommendation,
    navbar: enNavBar
  },
};


/**
 * Obtiene el idioma inicial de la aplicación.
 *
 * Comprueba si existe un idioma guardado en localStorage.
 * Si no existe, utiliza el idioma del navegador cuando es español
 * o inglés y establece el español como idioma predeterminado
 * para los demás idiomas.
 *
 * @returns {string} Código del idioma inicial: "es" o "en".
 */
const getInitialLanguage = () => {
  const saved = localStorage.getItem("lang");

  if (saved) return saved;

  const browserLang = navigator.language.toLowerCase();

  if (browserLang.startsWith("en")) return "en";
  if (browserLang.startsWith("es")) return "es";

  return "es";
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: getInitialLanguage(),

    fallbackLng: "es",

    ns: ["common", "dashboard", "tooltips", "login", "teacher", "admin", "evaluation", "recommendations", "navbar"],
    defaultNS: "common",

    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;