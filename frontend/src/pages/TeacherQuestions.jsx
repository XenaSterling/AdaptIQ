/**
 * Módulo: TeacherQuestions.jsx
 * Descripción: Gestiona las preguntas del banco de preguntas del profesor.
 *              Permite consultar las preguntas existentes, crear nuevas,
 *              editar sus propiedades y eliminar preguntas.
 *              Incluye la gestión de respuestas, la selección de la
 *              respuesta correcta, el tipo de pregunta, la dificultad,
 *              el nivel de Bloom y las asociaciones con módulos y etiquetas.
 *              Utiliza la API para recuperar y guardar los datos y muestra
 *              mensajes de carga y error durante las operaciones.
 * Autor: Raquel Del Castillo Pérez
 */

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import api from "../api/axios";
import ModuleSelector from "../components/ModuleSelector";
import TagSelector from "../components/TagSelector";

const EMPTY_FORM = {
    content: "",
    type: "single",
    difficulty: null,
    discrimination: null,
    bloom_level: "understand",
    module: null,
    tags: [],
    module_id: null,
    tag_ids: [],
    answers: [
        { content: "", is_correct: true },
        { content: "", is_correct: false }
    ]
};


/**
 * Renderiza la interfaz de gestión de preguntas del profesor.
 *
 * Permite cargar las preguntas existentes, crear y editar preguntas,
 * gestionar sus respuestas y eliminar preguntas previa confirmación.
 *
 * @returns {JSX.Element} Formulario de gestión y listado de preguntas.
 */
export default function TeacherQuestions() {
    const { t } = useTranslation(["teacher", "common"]);

    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [form, setForm] = useState(EMPTY_FORM);
    const [editingId, setEditingId] = useState(null);

    async function loadQuestions() {
        try {
            setLoading(true);
            const res = await api.get("/teacher/questions");
            setQuestions(res.data);
        } catch (err) {
            console.error(err);
            setError(t("errorLoadingQuestions"));
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadQuestions();
    }, []);

    function resetForm() {
        setForm(EMPTY_FORM);
        setEditingId(null);
    }

    function updateAnswer(index, field, value) {
        const updated = [...form.answers];
        updated[index] = { ...updated[index], [field]: value };
        setForm({ ...form, answers: updated });
    }

    function startEdit(question) {
        setEditingId(question.id);

        setForm({
            content: question.content,
            type: question.type,
            difficulty: question.difficulty,
            discrimination: question.discrimination,
            bloom_level: question.bloom_level,
            module_id: question.module_id ?? null,
            tag_ids: question.tags ?? [],
            answers: question.answers.length
                ? question.answers.map(a => ({
                      content: a.content,
                      is_correct: a.is_correct
                  }))
                : [
                      { content: "", is_correct: true },
                      { content: "", is_correct: false }
                  ]
        });
    }

    async function handleSubmit(e) {
        e.preventDefault();

        const isValid =
            form.answers.length >= 2 &&
            form.answers.every(a => a.content.trim() !== "");

        if (!isValid) {
            alert(t("atLeastTwoAnswers"));
            return;
        }

        try {
            if (editingId) {
                await api.put(`/teacher/questions/${editingId}`, form);
            } else {
                await api.post("/teacher/questions", form);
            }

            resetForm();
            loadQuestions();
        } catch (err) {
            console.error(err);
            alert(t("errorSavingQuestion"));
        }
    }

    async function deleteQuestion(id) {
        if (!window.confirm(t("confirmDeleteQuestion"))) return;

        try {
            await api.delete(`/teacher/questions/${id}`);
            loadQuestions();
        } catch (err) {
            console.error(err);
            alert(t("errorDeletingQuestion"));
        }
    }

    if (loading) return <p>{t("loadingQuestions")}</p>;

    return (
        <div className="container">
            <h1>{t("questionManagement")}</h1>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {/* FORM */}
            <form
                onSubmit={handleSubmit}
                style={{
                    border: "1px solid #ddd",
                    padding: "1rem",
                    marginBottom: "2rem"
                }}
            >
                <h2>
                    {editingId
                        ? t("editQuestion")
                        : t("createQuestion")}
                </h2>

                <textarea
                    value={form.content}
                    placeholder={t("questionContent")}
                    onChange={(e) =>
                        setForm({ ...form, content: e.target.value })
                    }
                    rows={2}
                    style={{
                        width: "100%",
                        minHeight: "120px",
                        resize: "vertical",
                        boxSizing: "border-box",
                        padding: "0.75rem",
                        borderRadius: "8px",
                        border: form.content
                            ? "1px solid #ccc"
                            : "2px dashed #aaa"
                    }}
                    required
                />

                <select
                    value={form.type}
                    onChange={(e) =>
                        setForm({ ...form, type: e.target.value })
                    }
                >
                    <option value="single">{t("singleChoice")}</option>
                    <option value="multiple">{t("multipleChoice")}</option>
                </select>

                <input
                    type="number"
                    step="0.1"
                    placeholder={t("difficulty")}
                    value={form.difficulty === null ? "" : form.difficulty}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            difficulty:
                                e.target.value === ""
                                    ? ""
                                    : Number(e.target.value)
                        })
                    }
                />

                <input
                    type="number"
                    step="0.1"
                    placeholder={t("discrimination")}
                    value={
                        form.discrimination === null
                            ? ""
                            : form.discrimination
                    }
                    onChange={(e) =>
                        setForm({
                            ...form,
                            discrimination:
                                e.target.value === ""
                                    ? ""
                                    : Number(e.target.value)
                        })
                    }
                />

                <select
                    value={form.bloom_level}
                    onChange={(e) =>
                        setForm({ ...form, bloom_level: e.target.value })
                    }
                >
                    <option value="remember">{t("remember")}</option>
                    <option value="understand">{t("understand")}</option>
                    <option value="apply">{t("apply")}</option>
                    <option value="analyze">{t("analyze")}</option>
                    <option value="evaluate">{t("evaluate")}</option>
                    <option value="create">{t("create")}</option>
                </select>

                {/* ANSWERS */}
                <h3>{t("answers")}</h3>

                {form.answers.map((ans, i) => (
                    <div key={i} style={{ marginBottom: "0.5rem" }}>
                        <input
                            type="text"
                            placeholder={`${t("answers")} ${i + 1}`}
                            value={ans.content}
                            onChange={(e) =>
                                updateAnswer(i, "content", e.target.value)
                            }
                            required
                            style={{
                                width: "100%",
                                boxSizing: "border-box"
                            }}
                        />

                        <label style={{ marginLeft: "1rem" }}>
                            {t("correct")}
                            <input
                                type="checkbox"
                                checked={ans.is_correct}
                                onChange={(e) =>
                                    updateAnswer(
                                        i,
                                        "is_correct",
                                        e.target.checked
                                    )
                                }
                            />
                        </label>

                        <button
                            type="button"
                            disabled={form.answers.length <= 2}
                            onClick={() =>
                                setForm(prev => ({
                                    ...prev,
                                    answers: prev.answers.filter(
                                        (_, idx) => idx !== i
                                    )
                                }))
                            }
                        >
                            {t("remove")}
                        </button>
                    </div>
                ))}

                <button
                    type="button"
                    onClick={() =>
                        setForm(prev => ({
                            ...prev,
                            answers: [
                                ...prev.answers,
                                { content: "", is_correct: false }
                            ]
                        }))
                    }
                >
                    {t("addAnswer")}
                </button>

                <div
                    style={{
                        marginTop: "20px",
                        display: "flex",
                        flexDirection: "column",
                        gap: "10px"
                    }}
                >
                    <button type="submit">
                        {editingId
                            ? t("updateQuestion")
                            : t("createQuestionButton")}
                    </button>

                    {editingId && (
                        <button type="button" onClick={resetForm}>
                            {t("cancel", { ns: "common" })}
                        </button>
                    )}
                </div>
            </form>

            {/* LIST */}
            <h2>{t("existingQuestions")}</h2>

            {questions.length === 0 ? (
                <p>{t("noQuestions")}</p>
            ) : (
                questions.map((q) => (
                    <div
                        key={q.id}
                        style={{
                            border: "1px solid #ddd",
                            padding: "1rem",
                            marginBottom: "1rem"
                        }}
                    >
                        <h3>{q.content}</h3>

                        <p>
                            <strong>{t("type")}:</strong> 
                                {q.type === "single"
                                    ? t("singleChoice")
                                    : t("multipleChoice")}
                        </p>
                        <p>
                            <strong>{t("difficulty")}:</strong>{" "}
                            {q.difficulty}
                        </p>
                        <p>
                            <strong>{t("bloom")}:</strong>{" "}
                            {t(q.bloom_level)}
                        </p>

                        <div>
                            <strong>{t("answers")}:</strong>
                            <ul>
                                {q.answers.map((a) => (
                                    <li key={a.id}>
                                        {a.content}{" "}
                                        {a.is_correct && "✓"}
                                    </li>
                                ))}
                            </ul>
                        </div>

                        <button onClick={() => startEdit(q)}>
                            {t("edit")}
                        </button>

                        <button
                            onClick={() => deleteQuestion(q.id)}
                            style={{ marginLeft: "0.5rem" }}
                        >
                            {t("delete")}
                        </button>
                    </div>
                ))
            )}
        </div>
    );
}