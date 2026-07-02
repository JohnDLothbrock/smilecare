import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  nombre: "",
  descripcion: "",
  estado: "ACTIVO"
};

function MetodosPago() {
  const [metodosPago, setMetodosPago] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadMetodosPago() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/metodos-pago");

      setMetodosPago(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadMetodosPago();
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
        await apiClient.post("/metodos-pago", payload);
        setMessage("Método de pago creado correctamente.");
      } else {
        await apiClient.put(`/metodos-pago/${editingId}`, payload);
        setMessage("Método de pago actualizado correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadMetodosPago();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(metodo) {
    setEditingId(metodo.metodo_pago_id);

    setForm({
      nombre: metodo.nombre ?? "",
      descripcion: metodo.descripcion ?? "",
      estado: metodo.estado ?? "ACTIVO"
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(metodoPagoId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este método de pago?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/metodos-pago/${metodoPagoId}`);

      setMessage("Método de pago eliminado correctamente.");

      await loadMetodosPago();
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
          <h2>Métodos de Pago</h2>
          <p>Administración de formas de pago disponibles.</p>
        </div>
      </div>

      <section className="card">
        <h3>
          {editingId === null
            ? "Crear método de pago"
            : "Editar método de pago"}
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
        <h3>Lista de métodos de pago</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {metodosPago.map((metodo) => (
                <tr key={metodo.metodo_pago_id}>
                  <td>{metodo.metodo_pago_id}</td>
                  <td>{metodo.nombre}</td>
                  <td>{metodo.descripcion}</td>
                  <td>{metodo.estado}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(metodo)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(metodo.metodo_pago_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {metodosPago.length === 0 && !loading && (
                <tr>
                  <td colSpan="5">No hay métodos de pago registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default MetodosPago;