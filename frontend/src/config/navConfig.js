/**
 * Módulo: navConfig.js
 * Descripción: Define los elementos de navegación de la aplicación
 *              y los roles autorizados para acceder a cada sección.
 * Autor: Raquel Del Castillo Pérez
 */


export const NAV_ITEMS = [
  {
    label: "dashboard",
    to: "/dashboard",
    roles: ["student", "teacher", "admin"]
  },

  {
    label: "evaluation",
    to: "/evaluation",
    roles: ["student"]
  },

  {
    label: "recommendations",
    to: "/recommendations",
    roles: ["student"]
  },

  {
    label: "questions",
    to: "/teacher/questions",
    roles: ["teacher"]
  },

  {
    label: "resources",
    to: "/teacher/resources",
    roles: ["teacher"]
  },

  {
    label: "users",
    to: "/users",
    roles: ["admin"]
  }
];