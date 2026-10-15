/**
 * Módulo: CohortsBarChart.jsx
 * Descripción: Representa mediante un gráfico de barras la distribución
 *              de estudiantes según los grupos de rendimiento
 *              obtenidos en el análisis de cohortes.
 * Autor: Raquel Del Castillo Pérez
 */

import { Bar } from "react-chartjs-2";
import { useTranslation } from "react-i18next";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);


/**
 * Genera un gráfico con el número de estudiantes por cohorte.
 *
 * Agrupa los estudiantes según su identificador de cluster y asigna
 * etiquetas y colores según el nivel de rendimiento.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {Array<Object>} [props.cohorts=[]] - Lista de estudiantes
 *        con su correspondiente identificador de cluster.
 * @returns {JSX.Element} Gráfico de barras con la distribución
 *          de estudiantes por grupo de rendimiento.
 */
export default function CohortsBarChart({ cohorts = [] }) {

  const { t } = useTranslation();
  const grouped = {};

  cohorts.forEach((c) => {
    const cluster = c.cluster ?? "unknown";
    grouped[cluster] =
      (grouped[cluster] || 0) + 1;
  });

  const clusterLabels = {
    0: t("charts.lowPerformance", {
      ns: "dashboard"
    }),
    1: t("charts.mediumPerformance", {
      ns: "dashboard"
    }),
    2: t("charts.highPerformance", {
      ns: "dashboard"
    })
  };

  const clusterColors = {
    0: "#ef5350",
    1: "#ffca28",
    2: "#66bb6a"
  };

  const data = {
    labels: Object.keys(grouped).map(
      (k) =>
        clusterLabels[k] ??
        `${t("charts.cluster", {
          ns: "dashboard"
        })} ${k}`
    ),
    datasets: [
      {
        label: t("charts.studentsPerCohort", {
          ns: "dashboard"
        }),
        data: Object.values(grouped),
        backgroundColor:
          Object.keys(grouped).map(
            (k) =>
              clusterColors[k] ??
              "#42a5f5"
          )
      }
    ]
  };

  const options = {
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: t("charts.cohorts", {
            ns: "dashboard"
          })
        }
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: t("charts.students", {
            ns: "dashboard"
          })
        }
      }
    }
  };

  return <Bar data={data} options={options} />;
}