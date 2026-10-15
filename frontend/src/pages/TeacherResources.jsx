/**
 * Módulo: TeacherResources.jsx
 * Descripción: Gestiona los recursos educativos del profesor.
 *              Permite consultar los recursos existentes, crear nuevos,
 *              editar sus propiedades y eliminar recursos.
 *              Gestiona el título, la descripción, la URL, el tipo,
 *              la dificultad, el tiempo estimado y las asociaciones
 *              con módulos y etiquetas.
 *              Utiliza selectores específicos para asignar módulos
 *              y etiquetas, y se comunica con la API para recuperar
 *              y guardar los datos.
 * Autor: Raquel Del Castillo Pérez
 */

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import api from "../api/axios";
import ModuleSelector from "../components/ModuleSelector";
import TagSelector from "../components/TagSelector";

const EMPTY_FORM = {
    title: "",
    description: "",
    url: "",
    type: "video",
    difficulty: null,
    estimated_time: null,
    module: null,
    tags: [],
    module_id: null,
    tag_ids: []
};


/**
 * Renderiza la interfaz de gestión de recursos educativos.
 *
 * Permite cargar los recursos existentes, crear y editar recursos,
 * asignarlos a módulos y etiquetas, y eliminarlos previa confirmación.
 *
 * @returns {JSX.Element} Formulario de gestión y listado de recursos.
 */
export default function TeacherResources() {
    const { t } = useTranslation(["teacher"]);

    const [resources, setResources] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [form, setForm] = useState(EMPTY_FORM);
    const [editingId, setEditingId] = useState(null);

    async function loadResources() {
        try {
            setLoading(true);
            const res = await api.get("/teacher/resources");
            setResources(res.data);
        } catch (err) {
            console.error(err);
            setError(t("errorLoadingResources"));
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadResources();
    }, []);

    function resetForm() {
        setForm(EMPTY_FORM);
        setEditingId(null);
    }

    function startEdit(resource) {
        setEditingId(resource.id);

        setForm({
            title: resource.title,
            description: resource.description ?? "",
            url: resource.url,
            type: resource.type,
            difficulty: resource.difficulty,
            estimated_time: resource.estimated_time ?? null,
            module: resource.module ?? null,
            module_id: resource.module_id ?? null,
            tag_ids: (resource.tags ?? []).map(t => t.id),
            tags: resource.tags ?? []
        });
    }

    function handleChange(field, value) {
        setForm(prev => ({
            ...prev,
            [field]: value
        }));
    }

    async function handleSubmit(e) {
        e.preventDefault();

        try {
            if (editingId) {
                await api.put(`/teacher/resources/${editingId}`, form);
            } else {
                await api.post(`/teacher/resources`, form);
            }

            resetForm();
            loadResources();
        } catch (err) {
            console.error(err);
            alert(t("errorSavingResource"));
        }
    }

    async function deleteResource(id) {
        if (!window.confirm(t("confirmDeleteResource"))) return;

        try {
            await api.delete(`/teacher/resources/${id}`);
            loadResources();
        } catch (err) {
            console.error(err);
            alert(t("errorDeletingResource"));
        }
    }

    if (loading) return <p>{t("loadingResources")}</p>;

    return (
        <div className="container">
            <h1>{t("resourceManagement")}</h1>

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
                        ? t("editResource")
                        : t("createResource")}
                </h2>

                <input
                    type="text"
                    placeholder={t("title")}
                    value={form.title}
                    onChange={(e) => handleChange("title", e.target.value)}
                    required
                    style={{
                        width: "100%",
                        boxSizing: "border-box"
                    }}
                />

                <textarea
                    placeholder={t("resourceDescription")}
                    value={form.description}
                    onChange={(e) =>
                        handleChange("description", e.target.value)
                    }
                    rows={5}
                    style={{
                        width: "100%",
                        minHeight: "120px",
                        resize: "vertical",
                        boxSizing: "border-box",
                        padding: "0.75rem",
                        borderRadius: "8px",
                        border: form.description
                            ? "1px solid #ccc"
                            : "2px dashed #aaa"
                    }}
                />

                <input
                    type="text"
                    placeholder={t("url")}
                    value={form.url}
                    onChange={(e) => handleChange("url", e.target.value)}
                    required
                    style={{
                        width: "100%",
                        boxSizing: "border-box"
                    }}
                />

                <select
                    value={form.type}
                    onChange={(e) => handleChange("type", e.target.value)}
                >
                    <option value="video">{t("video")}</option>
                    <option value="article">{t("article")}</option>
                    <option value="pdf">{t("pdf")}</option>
                    <option value="exercise">{t("exercise")}</option>
                </select>

                <input
                    type="number"
                    step="0.1"
                    placeholder={t("difficulty")}
                    value={form.difficulty ?? ""}
                    onChange={(e) =>
                        handleChange(
                            "difficulty",
                            e.target.value === ""
                                ? null
                                : Number(e.target.value)
                        )
                    }
                />

                <input
                    type="number"
                    step="1"
                    placeholder={t("estimatedTime")}
                    value={form.estimated_time ?? ""}
                    onChange={(e) =>
                        handleChange(
                            "estimated_time",
                            e.target.value === ""
                                ? null
                                : Number(e.target.value)
                        )
                    }
                />



                <div style={{ width: "100%" }}>
                    <ModuleSelector
                        value={form.module}
                        onSelect={(module) =>
                            setForm(prev => ({
                                ...prev,
                                module,
                                module_id: module.id
                            }))
                        }
                    />
                </div>

                <div style={{ width: "100%" }}>
                    <TagSelector
                        selectedTags={form.tags}
                        onChange={(tags) =>
                            setForm(prev => ({
                                ...prev,
                                tags,
                                tag_ids: tags.map(t => t.id)
                            }))
                        }
                    />
                </div>

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
                            ? t("updateResource")
                            : t("createResourceButton")}
                    </button>

                    {editingId && (
                        <button type="button" onClick={resetForm}>
                            {t("cancel", { ns: "common" })}
                        </button>
                    )}
                </div>
            </form>

            {/* LIST */}
            <h2>{t("existingResources")}</h2>

            {resources.length === 0 ? (
                <p>{t("noResources")}</p>
            ) : (
                resources.map((r) => (
                    <div
                        key={r.id}
                        style={{
                            border: "1px solid #ddd",
                            padding: "1rem",
                            marginBottom: "1rem"
                        }}
                    >
                        <h3>{r.title}</h3>

                        <p>
                            <strong>{t("type")}:</strong> {r.type}
                        </p>

                        <p>
                            <strong>{t("difficulty")}:</strong>{" "}
                            {r.difficulty}
                        </p>

                        <p>
                            <a href={r.url} target="_blank" rel="noreferrer">
                                {t("openResource")}
                            </a>
                        </p>

                        <div>
                            <strong>{t("tags")}:</strong>{" "}
                            {(r.tags || [])
                                .map(t =>
                                    typeof t === "object" ? t.name : t
                                )
                                .join(", ")}
                        </div>

                        <div
                            style={{
                                marginTop: "20px",
                                display: "flex",
                                flexDirection: "column",
                                gap: "10px"
                            }}
                        ></div>                    

                        <button onClick={() => startEdit(r)}>
                            {t("edit")}
                        </button>

                        <button
                            onClick={() => deleteResource(r.id)}
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