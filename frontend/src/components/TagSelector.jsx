/**
 * Módulo: TagSelector.jsx
 * Descripción: Permite buscar, crear, seleccionar y eliminar
 *              etiquetas mediante la API de la aplicación.
 * Autor: Raquel Del Castillo Pérez
 */

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import api from "../api/axios";


/**
 * Gestiona la selección de etiquetas.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {Array<Object>} [props.selectedTags=[]] - Etiquetas seleccionadas.
 * @param {Function} props.onChange - Función que recibe la nueva selección.
 * @returns {JSX.Element} Selector de etiquetas.
 */
export default function TagSelector({
    selectedTags = [],
    onChange
}) {

    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const { t } = useTranslation(["teacher"]);


    /**
     * Busca etiquetas en la API al cambiar el texto de búsqueda.
     * Retrasa la petición 300 milisegundos para reducir las solicitudes.
     *
     * @returns {Function|undefined} Función para cancelar el temporizador.
     */
    useEffect(() => {

        if (!query.trim()) {
            setResults([]);
            return;
        }

        const timeout = setTimeout(async () => {

            try {

                const res = await api.get(
                    `/teacher/tags/search?q=${query}`
                );

                setResults(res.data);

            } catch (err) {
                console.error(err);
            }

        }, 300);

        return () => clearTimeout(timeout);

    }, [query]);


    /**
     * Crea una etiqueta nueva mediante la API y la añade a la selección.
     *
     * @returns {Promise<void>} Finaliza cuando termina la petición.
     */
    async function createTag() {

        if (!query.trim()) return;

        try {

            const res = await api.post(
                "/teacher/tags",
                {
                    name: query
                }
            );

            onChange([
                ...selectedTags,
                res.data
            ]);

            setQuery("");
            setResults([]);

        } catch (err) {
            console.error(err);
        }
    }


    /**
     * Añade una etiqueta si no está seleccionada previamente.
     *
     * @param {Object} tag - Etiqueta que se desea añadir.
     * @param {number|string} tag.id - Identificador de la etiqueta.
     * @returns {void}
     */
    function addTag(tag) {

        const exists = selectedTags.some(
            t => t.id === tag.id
        );

        if (exists) return;

        onChange([
            ...selectedTags,
            tag
        ]);

        setQuery("");
        setResults([]);
    }


    /**
     * Elimina una etiqueta de la selección actual.
     *
     * @param {number|string} id - Identificador de la etiqueta.
     * @returns {void}
     */
    function removeTag(id) {

        onChange(
            selectedTags.filter(
                t => t.id !== id
            )
        );
    }

    return (
        <div>

            <label>{t("tags")}</label>

            <div
                style={{
                    display: "flex",
                    gap: "0.5rem",
                    flexWrap: "wrap",
                    marginBottom: "0.5rem"
                }}
            >
                {selectedTags.map(tag => (
                    <span
                        key={tag.id}
                        style={{
                            background: "#eee",
                            padding: "0.3rem 0.6rem",
                            borderRadius: "999px"
                        }}
                    >
                        {tag.name}

                        <button
                            type="button"
                            onClick={() => removeTag(tag.id)}
                            style={{
                                marginLeft: "0.5rem"
                            }}
                        >
                            x
                        </button>
                    </span>
                ))}
            </div>

            <input
                type="text"
                value={query}
                placeholder={t("searchTag")}
                onChange={(e) => setQuery(e.target.value)}
                style={{
                    boxSizing: "border-box"
                }}
            />

            {results.length > 0 && (
                <div
                    style={{
                        border: "1px solid #ccc",
                        marginTop: "0.5rem"
                    }}
                >
                    {results.map(tag => (
                        <div
                            key={tag.id}
                            style={{
                                cursor: "pointer",
                                padding: "0.5rem"
                            }}
                            onClick={() => addTag(tag)}
                        >
                            {tag.name}
                        </div>
                    ))}
                </div>
            )}

            {query &&
                results.length === 0 && (
                    <button
                        type="button"
                        onClick={createTag}
                    >
                        {t("createTag", { tag: query })}
                    </button>
                )}
        </div>
    );
}