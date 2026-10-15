/**
 * Módulo: FailedQuestionsBar.js
 * Descripción: Representa mediante un gráfico de barras las preguntas
 *              que presentan errores, mostrando el número de errores
 *              registrados para cada pregunta.
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
 * Genera un gráfico con el número de errores por pregunta.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {Array<Object>} props.dataList - Lista de preguntas.
 *        Cada elemento contiene question_text y errors.
 * @returns {JSX.Element} Gráfico de barras con las preguntas
 *          y sus respectivos números de errores.
 */
export default function FailedQuestionsBar({ dataList }) {

  const { t } = useTranslation();

  const data = {
    labels: dataList.map(
      q => q.question_text
    ),
    datasets: [
      {
        label: t("charts.errors", {
          ns: "dashboard"
        }),
        data: dataList.map(
          q => q.errors
        ),
        backgroundColor: "#2196f3"
      }
    ]
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        ticks: {
          display: false
        },
        title: {
          display: true,
          text: t("charts.questions", {
            ns: "dashboard"
          })
        }
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: t("charts.errors", {
            ns: "dashboard"
          })
        }
      }
    }
  };

  return <Bar data={data} options={options} />;

}