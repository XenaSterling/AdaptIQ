/**
 * Módulo: PieChart.jsx
 * Descripción: Representa mediante un gráfico circular la distribución
 *              de los datos recibidos, traduciendo las etiquetas
 *              conocidas según el idioma de la aplicación.
 * Autor: Raquel Del Castillo Pérez
 */

import { Pie } from "react-chartjs-2";
import { useTranslation } from "react-i18next";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);


/**
 * Genera un gráfico circular a partir de un conjunto de datos.
 *
 * Traduce las etiquetas conocidas relacionadas con niveles de confianza,
 * roles de usuario y estados de evaluación.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {Object} props.dataMap - Objeto con las categorías y sus valores.
 *        Los valores pueden ser numéricos o contener una propiedad count.
 * @returns {JSX.Element} Gráfico circular con la distribución de los datos.
 */
export default function PieChart({ dataMap }) {

  const { t } = useTranslation();

  const labels = Object.keys(dataMap);

  const translatedLabels = labels.map((label) => {

    const normalized = String(label).toLowerCase().replace(/\s+/g, "_");

    const map = {

      low: t("confidence.low", {
        ns: "dashboard"
      }),

      medium: t("confidence.medium", {
        ns: "dashboard"
      }),

      high: t("confidence.high", {
        ns: "dashboard"
      }),

      student: t("roles.student", {
        ns: "common"
      }),

      teacher: t("roles.teacher", {
        ns: "common"
      }),

      admin: t("roles.admin", {
        ns: "common"
      }),

      completed: t("evaluation.completed", {
        ns: "common"
      }),

      abandoned: t("evaluation.abandoned", {
        ns: "common"
      }),

      in_progress: t("evaluation.inProgress", {
        ns: "common"
      })

    };

    return map[normalized] ?? label;

  });

  const values = labels.map((k) =>
    typeof dataMap[k] === "number"
      ? dataMap[k]
      : dataMap[k]?.count ?? 0
  );

  const data = {

    labels: translatedLabels,

    datasets: [
      {
        data: values,

        backgroundColor: [
          "#4caf50",
          "#ff9800",
          "#f44336"
        ]
      }
    ]

  };

  return <Pie data={data} />;

}