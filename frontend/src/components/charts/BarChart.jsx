/**
 * Módulo: BarChart.jsx
 * Descripción: Representa mediante un gráfico de barras las tasas
 *              de error asociadas a diferentes temas, utilizando
 *              los datos recibidos y las traducciones disponibles.
 * Autor: Raquel Del Castillo Pérez
 */

import { Bar } from "react-chartjs-2";
import { useTranslation } from "react-i18next";

import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);


/**
 * Genera un gráfico de barras con las tasas de error por tema.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {Object} props.dataMap - Objeto con los datos de cada tema.
 *        Los valores pueden ser numéricos o contener una propiedad
 *        error_rate con la tasa de error correspondiente.
 * @returns {JSX.Element} Gráfico de barras con los datos recibidos.
 */
export default function BarChart({ dataMap }) {

  const { t } = useTranslation();
  const labels = Object.keys(dataMap).map((k) =>
    t(`topics.${k}`, { ns: "dashboard", defaultValue: k })
  );
  const values = labels.map((k) => {

    const v = dataMap[k];
    if (typeof v === "number") return v;
    if (v?.error_rate != null)
      return v.error_rate;
    return 0;
  });

  const data = {
    labels,
    datasets: [
      {
        label: t("charts.errorRate", {
          ns: "dashboard"
        }),
        data: values,
        backgroundColor:
          "rgba(239,68,68,0.6)"
      }
    ]
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        title: {
          display: true,
          text: t("charts.topics", {
            ns: "dashboard"
          })
        }
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: t("charts.errorRate", {
            ns: "dashboard"
          })
        }
      }
    }
  };

  return <Bar data={data} options={options} />;
}