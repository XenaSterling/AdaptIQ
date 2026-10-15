/**
 * Módulo: TeacherDashboard.jsx
 * Descripción: Obtiene y muestra el panel de seguimiento académico
 *              del profesor a partir de las estadísticas proporcionadas.
 *              Presenta indicadores generales sobre estudiantes,
 *              precisión, evaluaciones, respuestas, puntuación media,
 *              nivel de conocimiento y estudiantes con dificultades.
 *              Incluye gráficos sobre el riesgo de abandono,
 *              las preguntas más falladas y el rendimiento por grupos,
 *              además de un listado de estudiantes con mayor riesgo.
 * Autor: Raquel Del Castillo Pérez
 */

import StatCard from "../components/StatCard";
import { useTranslation } from "react-i18next";
import RiskPieChart from "../components/charts/RiskPieChart";
import FailedQuestionsBar from "../components/charts/FailedQuestionsBar";
import CohortsBarChart from "../components/charts/CohortsBarChart";


/**
 * Renderiza el panel de seguimiento académico del profesor.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {Object} props.data - Estadísticas generales, datos de gráficos
 *                              y listado de estudiantes con riesgo elevado.
 * @returns {JSX.Element} Panel con indicadores, gráficos y tabla de riesgos.
 */
export default function TeacherDashboard({ data }) {
  const { t } = useTranslation();

  return (
    <div className="container">
      <h1>{t("teacher.title", { ns: "dashboard" })}</h1>

      <div className="grid">
        <StatCard
          title={t("teacher.totalStudents",{ns:"dashboard"})}
          value={data.total_students}
          tooltip={t("tooltips.totalStudents",{ns:"tooltips"})}
        />

        <StatCard
            title={t("teacher.accuracy",{ns:"dashboard"})}
            value={`${(data.accuracy*100).toFixed(1)}%`}
            tooltip={t("tooltips.accuracyTeacher",{ns:"tooltips"})}
        />

        <StatCard
            title={t("teacher.totalEvaluations",{ns:"dashboard"})}
            value={data.total_evaluations}
            tooltip={t("tooltips.totalEvaluations",{ns:"tooltips"})}
        />

        <StatCard
            title={t("teacher.totalAnswers",{ns:"dashboard"})}
            value={data.total_answers}
            tooltip={t("tooltips.totalAnswers",{ns:"tooltips"})}
        />

        <StatCard
            title={t("teacher.averageScore",{ns:"dashboard"})}
            value={data.avg_score}
            tooltip={t("tooltips.averageScoreTeacher",{ns:"tooltips"})}
        />

        <StatCard
            title={t("teacher.averageTheta",{ns:"dashboard"})}
            value={data.avg_theta}
            tooltip={t("tooltips.averageTheta",{ns:"tooltips"})}
        />

        <StatCard
            title={t("teacher.strugglingStudents",{ns:"dashboard"})}
            value={data.struggling_students}
            tooltip={t("tooltips.strugglingStudents",{ns:"tooltips"})}
        />
      </div>

      <div className="card">
        <h2>{t("charts.dropoutRisk", { ns: "dashboard" })}
          <span
              className="info-icon"
              title={t("chartTooltips.dropout",{ns:"tooltips"})}
          >
              ⓘ
          </span>
        </h2>
        <div className="chart-container">
          <RiskPieChart dataMap={data.risk_breakdown} />
        </div>
      </div>

      <div className="card">
        <h2>{t("charts.failedQuestions", { ns: "dashboard" })}
          <span
              className="info-icon"
              title={t("chartTooltips.failedQuestions",{ns:"tooltips"})}
          >
              ⓘ
          </span>    
        </h2>
        <FailedQuestionsBar dataList={data.most_failed_questions} />
      </div>

      <div className="card">
        <h2>{t("charts.cohorts", { ns: "dashboard" })}
          <span
              className="info-icon"
              title={t("chartTooltips.cohorts",{ns:"tooltips"})}
          >
              ⓘ
          </span> 
        </h2>
        <CohortsBarChart cohorts={data.cohorts} />
      </div>

      {/* ================= LIST ================= */}

      <div className="card">
        <h2>{t("charts.highRiskStudents", { ns: "dashboard" })}
          <span
              className="info-icon"
              title={t("chartTooltips.highRisk", { ns: "tooltips" })}
          >
              ⓘ
          </span>
        </h2>
        {data.high_risk_students?.length === 0 ? (
          <p>{t("messages.noHighRiskStudents", { ns: "common" })}</p>
        ) : (
          <table className="risk-table">
            <thead>
              <tr>
                <th>{t("table.student", { ns: "common" })}</th>
                <th>{t("table.risk", { ns: "common" })}</th>
              </tr>
            </thead>

            <tbody>
              {[...(data.high_risk_students ?? [])]
                .sort((a, b) => b.risk_score - a.risk_score)
                .map((student) => (
                  <tr key={student.id}>
                    <td>{student.name}</td>
                    <td>
                      {(student.risk_score * 100).toFixed(0)}%
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}