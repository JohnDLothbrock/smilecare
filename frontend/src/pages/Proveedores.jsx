import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  nombre: "",
  telefono: "",
  correo: "",
  direccion: "",
  estado: "ACTIVO"
};

function Proveedores() {
  const [proveedores, setProveedores] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadProveedores() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/proveedores");

      setProveedores(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProveedores();
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function buildPayload() {
    return {
      nombre: form.nombre,
      telefono: form.telefono || null,
      correo: form.correo || null,
      direccion: form.direccion || null,
      estado: form.estado
    };
  }

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const payload = buildPayload();

      if (editingId === null) {
        await apiClient.post("/proveedores", payload);
        setMessage("Proveedor creado correctamente.");
      } else {
        await apiClient.put(`/proveedores/${editingId}`, payload);
        setMessage("Proveedor actualizado correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadProveedores();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(proveedor) {
    setEditingId(proveedor.proveedor_id);

    setForm({
      nombre: proveedor.nombre ?? "",
      telefono: proveedor.telefono ?? "",
      correo: proveedor.correo ?? "",
      direccion: proveedor.direccion ?? "",
      estado: proveedor.estado ?? "ACTIVO"
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(proveedorId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este proveedor?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/proveedores/${proveedorId}`);

      setMessage("Proveedor eliminado correctamente.");

      await loadProveedores();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleCancelEdit() {
    setEditingId(null);
    setForm(initialForm);
    setMessage("");
    setError("");
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Proveedores</h2>
          <p>Administración de proveedores de insumos.</p>
        </div>
      </div>

      <section className="card">
        <h3>{editingId === null ? "Crear proveedor" : "Editar proveedor"}</h3>

        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Nombre
            <input
              type="text"
              name="nombre"
              value={form.nombre}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Teléfono
            <input
              type="text"
              name="telefono"
              value={form.telefono}
              onChange={handleChange}
              placeholder="2222-3333"
            />
          </label>

          <label>
            Correo
            <input
              type="email"
              name="correo"
              value={form.correo}
              onChange={handleChange}
              placeholder="proveedor@ejemplo.com"
            />
          </label>

          <label>
            Estado
            <select
              name="estado"
              value={form.estado}
              onChange={handleChange}
              required
            >
              <option value="ACTIVO">ACTIVO</option>
              <option value="INACTIVO">INACTIVO</option>
            </select>
          </label>

          <label>
            Dirección
            <textarea
              name="direccion"
              value={form.direccion}
              onChange={handleChange}
              rows="3"
            />
          </label>

          <div className="form-actions">
            <button type="submit" disabled={loading}>
              {editingId === null ? "Guardar" : "Actualizar"}
            </button>

            {editingId !== null && (
              <button
                type="button"
                className="secondary-button"
                onClick={handleCancelEdit}
              >
                Cancelar
              </button>
            )}
          </div>
        </form>

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
      </section>

      <section className="card">
        <h3>Lista de proveedores</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Teléfono</th>
                <th>Correo</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {proveedores.map((proveedor) => (
                <tr key={proveedor.proveedor_id}>
                  <td>{proveedor.proveedor_id}</td>
                  <td>{proveedor.nombre}</td>
                  <td>{proveedor.telefono}</td>
                  <td>{proveedor.correo}</td>
                  <td>{proveedor.estado}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(proveedor)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(proveedor.proveedor_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {proveedores.length === 0 && !loading && (
                <tr>
                  <td colSpan="6">No hay proveedores registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default Proveedores;