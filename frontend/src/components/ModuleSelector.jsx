/**
 * Módulo: ModuleSelector.jsx
 * Descripción: Permite buscar y seleccionar módulos mediante
 *              consultas a la API del profesor.
 * Autor: Raquel Del Castillo Pérez
 */

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import api from "../api/axios";


/**
 * Permite buscar módulos y seleccionar uno de los resultados.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {Object|null} props.value - Módulo seleccionado.
 * @param {Function} props.onSelect - Función que recibe el módulo seleccionado.
 * @returns {JSX.Element} Buscador y selector de módulos.
 */
export default function ModuleSelector({
    value,
    onSelect
}) {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const { t } = useTranslation(["teacher"]);

    /**
     * Busca módulos en la API cuando cambia la consulta.
     * Retrasa la petición 300 milisegundos para evitar solicitudes
     * innecesarias durante la escritura.
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
                    `/teacher/modules/search?q=${query}`
                );

                setResults(res.data);

            } catch (err) {
                console.error(err);
            }

        }, 300);

        return () => clearTimeout(timeout);

    }, [query]);

    return (
        <div>
            <div
                style={{
                    marginBottom: "0.5rem"
                }}
            ></div>
            <label>{t("module")}</label>

            <div
                style={{
                    marginBottom: "0.5rem"
                }}
            >
                {value && (
                    <span>{value.title}</span>
                )}
            </div>

            <input
                type="text"
                value={query}
                placeholder={t("searchModule")}
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
                    {results.map(module => (
                        <div
                            key={module.id}
                            style={{
                                cursor: "pointer",
                                padding: "0.5rem"
                            }}
                            onClick={() => {

                                onSelect(module);

                                setQuery(module.title);

                                setResults([]);
                            }}
                        >
                            {module.title}
                        </div>
                    ))}
                </div>
            )}

            {value && (
                <p
                    style={{
                        marginTop: "0.5rem"
                    }}
                >
                    {t("selected")}: {value.title}
                </p>
            )}
        </div>
    );
}