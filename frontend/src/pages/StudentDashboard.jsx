/**
 * Módulo: StudentDashboard.jsx
 * Descripción: Obtiene y muestra el panel de seguimiento académico
 *              del estudiante a partir de los datos proporcionados.
 *              Presenta estadísticas sobre el nivel de conocimiento,
 *              precisión, puntuación, evaluaciones, incertidumbre,
 *              confianza y progreso académico.
 *              Incluye gráficos sobre la evolución del conocimiento,
 *              los temas débiles, el progreso por módulos y la
 *              distribución del nivel de confianza.
 * Autor: Raquel Del Castillo Pérez
 */

import StatCard from "../components/StatCard";
import LineChart from "../components/charts/LineChart";
import BarChart from "../components/charts/BarChart";
import PieChart from "../components/charts/PieChart";
import { useTranslation } from "react-i18next";


/**
 * Renderiza el panel de seguimiento académico del estudiante.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {Object} props.data - Datos estadísticos y de progreso del estudiante.
 * @returns {JSX.Element} Panel con indicadores, gráficos y progreso por módulos.
 */
export default function StudentDashboard({ data }) {
  const { t } = useTranslation();

  const weakTopics = data?.weak_topics ?? {};
  const thetaEvolution = data?.theta_evolution ?? [];
  const moduleProgress = data?.module_progress ?? [];

  const getLevel = (theta) => {
    if (theta < -1) return t("levels.basic", { ns: "dashboard" });
    if (theta < 1) return t("levels.intermediate", { ns: "dashboard" });
    return t("levels.advanced", { ns: "dashboard" });
  };

  const getConfidence = (u) => {
    if (u < 0.30) return "low";
    if (u < 0.60) return "medium";
    return "high";
  };

  const confidence = getConfidence(data?.uncertainty ?? 1);

  const thetaChange =
    thetaEvolution.length > 1
      ? thetaEvolution.at(-1).theta - thetaEvolution[0].theta
      : 0;

  return (
    <div className="container">
      <h1>{t("student.title", { ns: "dashboard" })}</h1>

      <div className="grid">

        <StatCard
          title={t("student.theta", { ns: "dashboard" })}
          value={data?.theta?.toFixed(2) ?? "0.00"}
          tooltip={t("tooltips.theta",{ns:"tooltips"})}
        />

        <StatCard
          title={t("student.level", { ns: "dashboard" })}
          value={getLevel(data?.theta ?? 0)}
          tooltip={t("tooltips.level",{ns:"tooltips"})}
        />

        <StatCard
          title={t("student.accuracy", { ns: "dashboard" })}
          value={`${((data?.accuracy ?? 0) * 100).toFixed(1)}%`}
          tooltip={t("tooltips.accuracy",{ns:"tooltips"})}
        />

        <StatCard
          title={t("student.averageScore", { ns: "dashboard" })}
          value={data?.score ?? 0}
          tooltip={t("tooltips.averageScore",{ns:"tooltips"})}
        />

        <StatCard
          title={t("student.evaluations", { ns: "dashboard" })}
          value={data?.evaluations_completed ?? 0}
          tooltip={t("tooltips.evaluations",{ns:"tooltips"})}
        />

        <StatCard
          title={t("student.uncertainty", { ns: "dashboard" })}
          value={data?.uncertainty?.toFixed(3) ?? "-"}
          tooltip={t("tooltips.uncertainty",{ns:"tooltips"})}
        />

        <StatCard
          title={t("student.confidence", { ns: "dashboard" })}
          value={t(`confidence.${confidence}`, { ns: "dashboard" })}
          tooltip={t("tooltips.confidence",{ns:"tooltips"})}
        />

        <StatCard
          title={t("student.progress", { ns: "dashboard" })}
          value={
            thetaChange >= 0
              ? `+${thetaChange.toFixed(2)}`
              : thetaChange.toFixed(2)
          }
          tooltip={t("tooltips.progress",{ns:"tooltips"})}
        />

        <StatCard
          title={t("student.modulesCompleted", { ns: "dashboard" })}
          value={`${data?.completed_modules ?? 0}/${moduleProgress.length}`}
          tooltip={t("tooltips.modulesCompleted", { ns: "tooltips" })}
        />

        <StatCard
          title={t("student.averageModuleProgress", { ns: "dashboard" })}
          value={`${data?.avg_module_progress?.toFixed(0) ?? 0}%`}
          tooltip={t("tooltips.averageModuleProgress", { ns: "tooltips" })}
        />

      </div>


      <div className="card">
        <h2>{t("charts.thetaEvolution", { ns: "dashboard" })}
          <span
              className="info-icon"
              title={t("chartTooltips.thetaEvolution",{ns:"tooltips"})}
          >
              ⓘ
          </span>
        </h2>
        {thetaEvolution.length > 0 ? (
          <LineChart dataPoints={thetaEvolution} />
        ) : (
          <p>{t("messages.noData", { ns: "common" })}</p>
        )}
      </div>

      <div className="card">
        <h2>{t("charts.weakTopics", { ns: "dashboard" })}
          <span
              className="info-icon"
              title={t("chartTooltips.weakTopics",{ns:"tooltips"})}
          >
              ⓘ
          </span>
        </h2>
        {Object.keys(weakTopics).length > 0 ? (
          <BarChart dataMap={weakTopics} />
        ) : (
          <p>{t("messages.noData", { ns: "common" })}</p>
        )}
      </div>

      <div className="card">
        <h2>
          {t("charts.moduleProgress", { ns: "dashboard" })}
          <span
            className="info-icon"
            title={t("chartTooltips.moduleProgress", { ns: "tooltips" })}
          >
            ⓘ
          </span>
        </h2>

        {moduleProgress.length > 0 ? (

          <div className="module-progress-list">

            {moduleProgress.map((module) => (

              <div
                key={module.module}
                style={{ marginBottom: "1rem" }}
              >

                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginBottom: ".35rem"
                  }}
                >

                  <strong>{module.module}</strong>

                  <span>

                    {module.progress.toFixed(0)}%

                    {module.completed && " ✅"}

                  </span>

                </div>

                <div
                  style={{
                    width: "100%",
                    background: "#e5e7eb",
                    borderRadius: "8px",
                    overflow: "hidden",
                    height: "12px"
                  }}
                >

                  <div
                    style={{
                      width: `${module.progress}%`,
                      height: "100%",
                      background:
                        module.completed
                          ? "linear-gradient(90deg, #16a34a, #22c55e)"
                          : "linear-gradient(90deg, #2563eb, #38bdf8)",
                      transition: ".3s"
                    }}
                  />

                </div>

              </div>

            ))}

          </div>

        ) : (

          <p>{t("messages.noData", { ns: "common" })}</p>

        )}

      </div>

      <div className="card">
        <h2>{t("charts.confidenceDistribution", { ns: "dashboard" })}
          <span
              className="info-icon"
              title={t("chartTooltips.confidenceDistribution",{ns:"tooltips"})}
          >
              ⓘ
          </span>
        </h2>
        <div className="chart-container">
          <PieChart
            dataMap={{
              low: confidence === "low" ? 1 : 0,
              medium: confidence === "medium" ? 1 : 0,
              high: confidence === "high" ? 1 : 0
            }}
          />
        </div>
      </div>
    </div>
  );
}