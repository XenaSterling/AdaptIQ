/**
 * Módulo: LineChart.jsx
 * Descripción: Representa la evolución del parámetro theta a lo largo
 *              de las evaluaciones mediante un gráfico de líneas.
 * Autor: Raquel Del Castillo Pérez
 */

import {
  Line
} from "react-chartjs-2";
import { useTranslation } from "react-i18next";


import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);


/**
 * Genera un gráfico de líneas con la evolución del parámetro theta.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {Array<Object>} props.dataPoints - Puntos de datos de la evolución.
 *        Cada elemento contiene step y theta.
 * @returns {JSX.Element} Gráfico de líneas con la evolución de theta.
 */
export default function LineChart({
  dataPoints
}) {
  const { t } = useTranslation();
  const data = {
    labels: dataPoints.map((d) => `#${d.step}`),

    datasets: [
      {
        label: t("charts.thetaEvolution", {
          ns: "dashboard"
        }),

        data: dataPoints.map((d) => d.theta),

        borderColor: "#3b82f6",
        backgroundColor: "rgba(59,130,246,0.2)",
        tension: 0.3
      }
    ]
  };

  const options = {
    responsive: true,

    plugins: {
      legend: {
        display: true
      }
    },

    scales: {
      x: {
        title: {
          display: true,
          text: t("charts.evaluation", {
            ns: "dashboard"
          })
        }
      },

      y: {
        title: {
          display: true,
          text: t("student.theta", {
            ns: "dashboard"
          })
        }
      }
    }
  };

  return <Line data={data} options={options} />;
}