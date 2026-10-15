/**
 * Módulo: Evaluation.jsx
 * Descripción: Gestiona las evaluaciones adaptativas de los estudiantes.
 *              Obtiene las preguntas de la API, registra las respuestas
 *              y muestra los resultados, las áreas de mejora y los
 *              recursos educativos recomendados al finalizar.
 * Autor: Raquel Del Castillo Pérez
 */

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import api from "../api/axios";
import { useAuth } from "../auth/AuthContext";


/**
 * Renderiza y gestiona una evaluación adaptativa.
 *
 * @returns {JSX.Element} Interfaz de evaluación o resultados finales.
 */
export default function Evaluation() {
  const { user } = useAuth();
  const { t } = useTranslation(["evaluation", "common"]);

  const userId = user?.userId;

  const [question, setQuestion] = useState(null);
  const [selected, setSelected] = useState([]);
  const [theta, setTheta] = useState(0);

  const [finished, setFinished] = useState(false);

  const [score, setScore] = useState(null);
  const [finalTheta, setFinalTheta] = useState(null);

  const [feedback, setFeedback] = useState(null);
  const [weakTopics, setWeakTopics] = useState([]);
  const [resources, setResources] = useState([]);

  useEffect(() => {
    if (!userId) return;
    startEvaluation();
  }, [userId]);


  /**
   * Inicia una evaluación y obtiene la primera pregunta.
   *
   * @returns {Promise<void>}
   */
  const startEvaluation = async () => {
    try {
      const res = await api.get(
        `/evaluation/start/${userId}`
      );

      setQuestion(res.data.question);
      setTheta(res.data.theta);

      setFinished(false);
      setFeedback(null);
      setWeakTopics([]);
      setResources([]);
    } catch (err) {
      console.error(
        "Error starting evaluation:",
        err
      );
    }
  };


  /**
   * Añade o elimina una respuesta seleccionada.
   * En preguntas de respuesta única, solo permite una opción.
   *
   * @param {number|string} id - Identificador de la respuesta.
   */
  const toggleAnswer = (id) => {
    if (selected.includes(id)) {
      setSelected(
        selected.filter((x) => x !== id)
      );
      return;
    }
    if (question.type === "single") {
      setSelected([id]);
      return;
    }
    setSelected([
      ...selected,
      id
    ]);
  };


  /**
   * Envía las respuestas seleccionadas a la API.
   * Actualiza la habilidad estimada y carga la siguiente pregunta
   * o los resultados finales de la evaluación.
   *
   * @returns {Promise<void>}
   */
  const submitAnswer = async () => {
    if (selected.length === 0) {
      alert(
        t("selectAtLeastOne")
      );
      return;
    }
    try {
      const res = await api.post(
        `/evaluation/answer/${userId}?question_id=${question.id}`,
        {
          selected_answer_ids: selected,
          response_time: 10,
        }
      );

      setTheta(res.data.theta);

      if (res.data.finished) {
        setFinished(true);
        setScore(
          res.data.score
        );
        setFinalTheta(
          res.data.final_theta
        );
        setFeedback(
          res.data.feedback || ""
        );
        setWeakTopics(
          res.data.weak_topics || []
        );
        setResources(
          res.data.recommended_resources || []
        );
        return;
      }

      setQuestion(
        res.data.question
      );

      setSelected([]);

    } catch (err) {
      console.error(
        "Error submitting answer:",
        err
      );
    }
  };

  if (!userId) {
    return (
      <div className="loading">
        {t("loadingUserSession", { ns: "common" })}
      </div>
    );
  }

  if (finished) {
    return (
      <div className="container">
        <div className="card">

          <h1>
            {t("completed")}
          </h1>

          <h2>
            {t("finalScore")}: {score}
          </h2>

          <p>
            {t("finalTheta")}: {finalTheta?.toFixed(2)}
          </p>

          <hr />

          {feedback && (
            <>
              <h3>{t("summary")}</h3>

              <p>{feedback.summary}</p>

              <p>
                <strong>{t("performance")}:</strong>{" "}
                {t(`performanceLevels.${feedback.performance}`)}
              </p>

              <p>
                <strong>{t("level")}:</strong>{" "}
                {t(`levels.${feedback.level}`)}
              </p>

              <p>
                <strong>{t("accuracy")}:</strong>{" "}
                {(feedback.accuracy * 100).toFixed(1)}%
              </p>

              <p>
                <strong>{t("theta")}:</strong>{" "}
                {feedback.theta}
              </p>

              <p>
                <strong>{t("thetaChange")}:</strong>{" "}
                {feedback.theta_change > 0
                  ? `+${feedback.theta_change}`
                  : feedback.theta_change}
              </p>

              <p>
                <strong>{t("uncertainty")}:</strong>{" "}
                {feedback.uncertainty}
              </p>

              <p>
                {feedback.improvement}
              </p>
            </>
          )}

          {weakTopics.length > 0 && (
            <>
              <h3>
                {t("areasToImprove")}
              </h3>

              <ul>
                {weakTopics.map(
                  (topic) => (
                    <li key={topic.id}>
                      {topic.name}
                      {" "}
                      (
                      {topic.weakness}
                      )
                    </li>
                  )
                )}
              </ul>
            </>
          )}

          {resources.length > 0 && (
            <>
              <h3>
                {t("recommendedResources")}
              </h3>

              <ul>
                {resources.map(
                  (resource) => (
                    <li
                      key={resource.id}
                    >
                      <a
                        href={
                          resource.url
                        }
                        target="_blank"
                        rel="noreferrer"
                      >
                        {resource.title}
                      </a>
                    </li>
                  )
                )}
              </ul>
            </>
          )}

        </div>
      </div>
    );
  }

  if (!question) {
    return (
      <div className="loading">
        {t("loadingEvaluation", { ns: "common" })}
      </div>
    );
  }

  return (
    <div className="container">
      <div className="card">

        <h1>
          {question.content}
        </h1>

        <div className="answers">
          {question.answers.map(
            (answer) => (
              <label
                key={answer.id}
                className="answer"
              >
                <input
                  type={
                    question.type ===
                    "multiple"
                      ? "checkbox"
                      : "radio"
                  }
                  checked={selected.includes(
                    answer.id
                  )}
                  onChange={() =>
                    toggleAnswer(
                      answer.id
                    )
                  }
                />

                {answer.content}
              </label>
            )
          )}
        </div>

        <button
          onClick={submitAnswer}
          disabled={selected.length === 0}
        >
          {t("submitAnswer")}
        </button>

      </div>
    </div>
  );
}