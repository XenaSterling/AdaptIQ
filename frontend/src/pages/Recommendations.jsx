/**
 * Módulo: Recommendations.jsx
 * Descripción: Obtiene y muestra las recomendaciones personalizadas
 *              de preguntas y recursos educativos del usuario.
 *              Presenta información sobre dificultad, etiquetas,
 *              confianza y motivos de cada recomendación.
 * Autor: Raquel Del Castillo Pérez
 */

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import api from "../api/axios";


/**
 * Renderiza las recomendaciones personalizadas.
 *
 * @returns {JSX.Element} Listado de preguntas y recursos recomendados.
 */
export default function Recommendations() {
  const [questions, setQuestions] = useState(null);
  const [resources, setResources] = useState(null);
  const { t } = useTranslation("recommendations");

  useEffect(() => {
    api.get("/recommendations/questions/me")
      .then((res) => setQuestions(res.data));

    api.get("/recommendations/resources/me")
      .then((res) => setResources(res.data));
  }, []);

  if (!questions || !resources) {
    return <div>{t("loading")}</div>;
  }

  return (
    <div className="container">

      <h1>{t("title")}</h1>

      {/* ================= RESOURCES ================= */}
      <div className="card">
        <h2>{t("recommendedResources")}</h2>

        {resources.resources.map((r) => (
          <div key={r.id} className="recommendation">

            <h3>{r.title}</h3>

            <p>{r.description}</p>

            <a href={r.url} target="_blank" rel="noreferrer">
              {t("openResource")}
            </a>

            <p>
              {t("type")}:{" "}
              {t(`resourceTypes.${r.type}`, {
                defaultValue: r.type,
              })}
            </p>

            <p>
              {t("difficulty")}: {r.difficulty}
            </p>

            {r.tags && r.tags.length > 0 && (
              <p>
                {t("tags")}:{" "}
                {r.tags.join(", ")}
              </p>
            )}

            <p>
              {t("reason")}:{" "}
              {r.reason?.reason_type
                ? t(`reasonTypes.${r.reason.reason_type}`)
                : t("adaptive")}
            </p>

            <p>
              {t("confidence")}:{" "}
              {r.reason?.confidence != null
                ? `${(r.reason.confidence * 100).toFixed(0)}%`
                : t("na")}
            </p>

            {r.reason?.explanation && (
              <p>
                {t(r.reason.explanation)}
              </p>
            )}

          </div>
        ))}
      </div>

      {/* ================= QUESTIONS ================= */}
      <div className="card">
        <h2>{t("recommendedQuestions")}</h2>

        {questions.recommendations.map((q) => (
          <div key={q.id} className="recommendation">

            <h3>{q.content}</h3>

            <p>
              {t("difficulty")}: {q.difficulty}
            </p>

            <p>
              {q.reason?.explanation
                ? t(q.reason.explanation)
                : t("noExplanation")}
            </p>

            <p>
              {t("reason")}:{" "}
              {q.reason?.reason_type
                ? t(`reasonTypes.${q.reason.reason_type}`)
                : t("adaptive")}
            </p>

            <p>
              {t("confidence")}:{" "}
              {q.reason?.confidence != null
                ? `${(q.reason.confidence * 100).toFixed(0)}%`
                : t("na")}
            </p>

            {q.reason?.peer_context && (
              <p>
                {t("similarStudents")}{" "}
                {q.reason.peer_context.avg_improvement_after_resource}
              </p>
            )}

          </div>
        ))}
      </div>

    </div>
  );
}