/**
 * Módulo: RiskPieChart.jsx
 * Descripción: Proporciona un gráfico circular para representar
 *              la distribución de los datos relacionados con el riesgo.
 *              Reutiliza el componente PieChart para generar
 *              la representación visual.
 * Autor: Raquel Del Castillo Pérez
 */

import PieChart from "./PieChart";


/**
 * Renderiza un gráfico circular de distribución de riesgos.
 *
 * Delega la representación y la traducción de las categorías
 * al componente PieChart.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {Object} [props.dataMap={}] - Datos agrupados por categoría
 *        de riesgo y sus valores correspondientes.
 * @returns {JSX.Element} Gráfico circular de distribución de riesgos.
 */
export default function RiskPieChart({ dataMap = {} }) {
  return <PieChart dataMap={dataMap} />;
}