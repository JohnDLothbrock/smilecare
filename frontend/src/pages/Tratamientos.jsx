import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  nombre: "",
  descripcion: "",
  costo_base: "",
  estado: "ACTIVO"
};

function Tratamientos() {
  const [tratamientos, setTratamientos] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadTratamientos() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/tratamientos");

      setTratamientos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTratamientos();
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
      descripcion: form.descripcion || null,
      costo_base: Number(form.costo_base),
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
        await apiClient.post("/tratamientos", payload);
        setMessage("Tratamiento creado correctamente.");
      } else {
        await apiClient.put(`/tratamientos/${editingId}`, payload);
        setMessage("Tratamiento actualizado correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadTratamientos();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(tratamiento) {
    setEditingId(tratamiento.tratamiento_id);

    setForm({
      nombre: tratamiento.nombre ?? "",
      descripcion: tratamiento.descripcion ?? "",
      costo_base: tratamiento.costo_base ?? "",
      estado: tratamiento.estado ?? "ACTIVO"
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(tratamientoId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este tratamiento?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/tratamientos/${tratamientoId}`);

      setMessage("Tratamiento eliminado correctamente.");

      await loadTratamientos();
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
          <h2>Tratamientos</h2>
          <p>Administración de tratamientos ofrecidos por la clínica.</p>
        </div>
      </div>

      <section className="card">
        <h3>
          {editingId === null ? "Crear tratamiento" : "Editar tratamiento"}
        </h3>

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
            Costo base
            <input
              type="number"
              name="costo_base"
              value={form.costo_base}
              onChange={handleChange}
              min="0"
              step="0.01"
              required
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
            Descripción
            <textarea
              name="descripcion"
              value={form.descripcion}
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
        <h3>Lista de tratamientos</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Descripción</th>
                <th>Costo base</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {tratamientos.map((tratamiento) => (
                <tr key={tratamiento.tratamiento_id}>
                  <td>{tratamiento.tratamiento_id}</td>
                  <td>{tratamiento.nombre}</td>
                  <td>{tratamiento.descripcion}</td>
                  <td>{tratamiento.costo_base}</td>
                  <td>{tratamiento.estado}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(tratamiento)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() =>
                        handleDelete(tratamiento.tratamiento_id)
                      }
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {tratamientos.length === 0 && !loading && (
                <tr>
                  <td colSpan="6">No hay tratamientos registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default Tratamientos;