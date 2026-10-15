/**
 * Módulo: UserManagement.jsx
 * Descripción: Gestiona los usuarios de la aplicación desde el panel
 *              de administración.
 *              Permite consultar, buscar, crear y editar usuarios,
 *              así como modificar su rol y estado de actividad.
 *              Gestiona los datos personales, las credenciales y los
 *              permisos asociados a los roles de estudiante, profesor
 *              y administrador.
 *              Utiliza la API para recuperar y actualizar los datos,
 *              ordena los usuarios alfabéticamente y permite filtrar
 *              el listado por nombre.
 * Autor: Raquel Del Castillo Pérez
 */

import { useEffect, useState } from "react";
import api from "../api/axios";
import { useTranslation } from "react-i18next";


/**
 * Renderiza la interfaz de administración de usuarios.
 *
 * Permite cargar y filtrar usuarios, crear nuevas cuentas, editar
 * sus datos y activar o desactivar cuentas existentes.
 *
 * @returns {JSX.Element} Formulario de gestión y listado de usuarios.
 */
export default function UserManagement() {
    const { t } = useTranslation("admin");

    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [search, setSearch] = useState("");

    const [editingId, setEditingId] = useState(null);

    const [form, setForm] = useState({
        name: "",
        email: "",
        password: "",
        role: "student",
        is_active: true,
    });

    async function loadUsers() {
        try {
            setLoading(true);
            const res = await api.get("/admin/users");
            const ordered = [...res.data].sort((a, b) =>
                a.name.localeCompare(b.name)
            );
            setUsers(ordered);
        } catch (err) {
            console.error(err);
            setError(t("errorLoadingUsers"));
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadUsers();
    }, []);

    function resetForm() {
        setForm({
            name: "",
            email: "",
            password: "",
            role: "student",
            is_active: true,
        });
        setEditingId(null);
    }

    function startEdit(user) {
        setEditingId(user.id);

        setForm({
            name: user.name,
            email: user.email,
            password: "",
            role: user.role,
            is_active: user.is_active,
        });
    }

    async function handleSubmit() {
        try {
            if (editingId) {
                await api.put(`/admin/users/${editingId}`, form);
            } else {
                await api.post("/admin/users", form);
            }

            resetForm();
            loadUsers();
        } catch (err) {
            console.error(err);
            alert(t("errorSavingUser"));
        }
    }

    async function toggleUserStatus(id, currentState) {
        try {
            await api.put(`/admin/users/${id}`, {
                is_active: !currentState,
            });

            loadUsers();
        } catch (err) {
            console.error(err);
            alert(t("errorUpdatingUser"));
        }
    }

    const filteredUsers = users.filter(u =>
        u.name.toLowerCase().includes(search.toLowerCase())
    );
    if (loading) return <p>{t("loadingUsers")}</p>;

    return (
        <div className="container">
            <h1>{t("title")}</h1>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {/* ================= FORM ================= */}
            <div
                style={{
                    border: "1px solid #ddd",
                    padding: "1rem",
                    marginBottom: "2rem",
                }}
            >
                <h3>
                    {editingId ? t("editUser") : t("createUser")}
                </h3>

                <input
                    placeholder={t("name")}
                    type="text"
                    value={form.name}
                    onChange={(e) =>
                        setForm({ ...form, name: e.target.value })
                    }
                    style={{
                        width: "100%",
                        boxSizing: "border-box",
                        marginBottom: "0.75rem"
                    }}
                />

                <input
                    placeholder={t("email")}
                    type="email"
                    value={form.email}
                    onChange={(e) =>
                        setForm({ ...form, email: e.target.value })
                    }
                    style={{
                        width: "100%",
                        boxSizing: "border-box",
                        marginBottom: "0.75rem"
                    }}
                />

                <input
                    placeholder={
                        editingId
                            ? t("passwordKeep")
                            : t("password")
                    }
                    type="password"
                    value={form.password}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            password: e.target.value,
                        })
                    }
                    style={{
                        width: "100%",
                        boxSizing: "border-box",
                        marginBottom: "0.75rem"
                    }}
                />

                <select
                    value={form.role}
                    onChange={(e) =>
                        setForm({ ...form, role: e.target.value })
                    }
                >
                    <option value="student">{t("student")}</option>
                    <option value="teacher">{t("teacher")}</option>
                    <option value="admin">{t("admin")}</option>
                </select>

                <select
                    value={form.is_active}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            is_active: e.target.value === "true",
                        })
                    }
                    style={{ marginLeft: "0.5rem" }}
                >
                    <option value="true">{t("active")}</option>
                    <option value="false">{t("inactive")}</option>
                </select>

                <div style={{ marginTop: "1rem" }}>
                    <button onClick={handleSubmit}>
                        {editingId ? t("updateUser") : t("createUser")}
                    </button>

                    {editingId && (
                        <button
                            onClick={resetForm}
                            style={{ marginLeft: "1rem" }}
                        >
                            {t("cancel", { ns: "common" })}
                        </button>
                    )}
                </div>
            </div>

            {/* ================= LIST ================= */}
            <h2>{t("users")}</h2>

            <input
                type="text"
                placeholder={t("searchUser")}
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={{
                    width: "100%",
                    boxSizing: "border-box",
                    marginBottom: "1rem"
                }}
            />

            {users.length === 0 ? (
                <p>{t("noUsers")}</p>
            ) : (
                filteredUsers.map((u) => (
                    <div
                        key={u.id}
                        style={{
                            border: "1px solid #ddd",
                            padding: "1rem",
                            marginBottom: "1rem",
                            opacity: u.is_active ? 1 : 0.5,
                        }}
                    >
                        <h3>{u.name}</h3>
                        <p>{u.email}</p>
                        <p>
                            {t("role")}: {t(u.role)}
                        </p>

                        <div>
                            <button onClick={() => startEdit(u)}>
                                {t("editUser")}
                            </button>

                            <button
                                onClick={() =>
                                    toggleUserStatus(u.id, u.is_active)
                                }
                                style={{ marginLeft: "0.5rem" }}
                            >
                                {u.is_active
                                    ? t("deactivate")
                                    : t("reactivate")}
                            </button>
                        </div>
                    </div>
                ))
            )}
        </div>
    );
}