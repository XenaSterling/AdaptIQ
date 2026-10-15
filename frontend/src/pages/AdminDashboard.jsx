/**
 * Módulo: AdminDashboard.jsx
 * Descripción: Muestra el panel de administración con estadísticas
 *              generales de usuarios, cursos y evaluaciones,
 *              así como gráficos de distribución por roles
 *              y estados de las evaluaciones.
 * Autor: Raquel Del Castillo Pérez
 */

import StatCard from "../components/StatCard";
import PieChart from "../components/charts/PieChart";
import { useTranslation } from "react-i18next";


/**
 * Renderiza el panel de control del administrador.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {Object} props.data - Datos estadísticos proporcionados por la API.
 * @returns {JSX.Element} Panel de administración.
 */
export default function AdminDashboard({ data }) {
  const { t } = useTranslation();

  return (
    <div className="container">
      <h1>{t("admin.title", { ns: "dashboard" })}</h1>

      <div className="grid">

        <StatCard
          title={t("admin.totalUsers",{ns:"dashboard"})}
          value={data.total_users}
          tooltip={t("tooltips.totalUsers",{ns:"tooltips"})}
      />

      <StatCard
          title={t("admin.totalCourses",{ns:"dashboard"})}
          value={data.total_courses}
          tooltip={t("tooltips.totalCourses",{ns:"tooltips"})}
      />

      <StatCard
          title={t("admin.totalEvaluations",{ns:"dashboard"})}
          value={data.total_evaluations}
          tooltip={t("tooltips.totalEvaluations",{ns:"tooltips"})}
      />

      <StatCard
          title={t("admin.averageScore",{ns:"dashboard"})}
          value={data.avg_score}
          tooltip={t("tooltips.averageScoreAdmin",{ns:"tooltips"})}
      />

      <StatCard
          title={t("admin.averageTheta",{ns:"dashboard"})}
          value={data.avg_theta}
          tooltip={t("tooltips.averageTheta",{ns:"tooltips"})}
      />

      <StatCard
          title={t("admin.abandonedEvaluations",{ns:"dashboard"})}
          value={data.abandoned}
          tooltip={t("tooltips.abandoned",{ns:"tooltips"})}
      />

      </div>

      <div className="card">
        <h2>{t("charts.usersByRole", { ns: "dashboard" })}
          <span
            className="info-icon"
            title={t("chartTooltips.usersRole",{ns:"tooltips"})}
        >
            ⓘ
        </span>
        </h2>
        <div className="chart-container">
          <PieChart dataMap={data.role_breakdown || {}} />
        </div>
      </div>

      <div className="card">
        <h2>{t("charts.evaluationStatus", { ns: "dashboard" })}
          <span
            className="info-icon"
            title={t("chartTooltips.evaluationStatus",{ns:"tooltips"})}
        >
            ⓘ
        </span>
        </h2>
        <div className="chart-container">
          <PieChart dataMap={data.evaluation_breakdown || {}} />
        </div>
      </div>

    </div>
  );
}