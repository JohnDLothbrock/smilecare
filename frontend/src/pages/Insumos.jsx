import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  codigo: "",
  nombre: "",
  descripcion: "",
  unidad_medida: "",
  estado: "ACTIVO"
};

function Insumos() {
  const [insumos, setInsumos] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadInsumos() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/insumos");

      setInsumos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadInsumos();
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
      codigo: form.codigo,
      nombre: form.nombre,
      descripcion: form.descripcion || null,
      unidad_medida: form.unidad_medida,
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
        await apiClient.post("/insumos", payload);
        setMessage("Insumo creado correctamente.");
      } else {
        await apiClient.put(`/insumos/${editingId}`, payload);
        setMessage("Insumo actualizado correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadInsumos();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(insumo) {
    setEditingId(insumo.insumo_id);

    setForm({
      codigo: insumo.codigo ?? "",
      nombre: insumo.nombre ?? "",
      descripcion: insumo.descripcion ?? "",
      unidad_medida: insumo.unidad_medida ?? "",
      estado: insumo.estado ?? "ACTIVO"
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(insumoId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este insumo?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/insumos/${insumoId}`);

      setMessage("Insumo eliminado correctamente.");

      await loadInsumos();
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
          <h2>Insumos</h2>
          <p>Administración de insumos usados por la clínica.</p>
        </div>
      </div>

      <section className="card">
        <h3>{editingId === null ? "Crear insumo" : "Editar insumo"}</h3>

        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Código
            <input
              type="text"
              name="codigo"
              value={form.codigo}
              onChange={handleChange}
              placeholder="INS-001"
              required
            />
          </label>

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
            Unidad de medida
            <select
              name="unidad_medida"
              value={form.unidad_medida}
              onChange={handleChange}
              required
            >
              <option value="">Seleccione unidad</option>
              <option value="UNIDAD">UNIDAD</option>
              <option value="CAJA">CAJA</option>
              <option value="PAQUETE">PAQUETE</option>
              <option value="ML">ML</option>
              <option value="GRAMOS">GRAMOS</option>
            </select>
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
        <h3>Lista de insumos</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Código</th>
                <th>Nombre</th>
                <th>Unidad</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {insumos.map((insumo) => (
                <tr key={insumo.insumo_id}>
                  <td>{insumo.insumo_id}</td>
                  <td>{insumo.codigo}</td>
                  <td>{insumo.nombre}</td>
                  <td>{insumo.unidad_medida}</td>
                  <td>{insumo.estado}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(insumo)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(insumo.insumo_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {insumos.length === 0 && !loading && (
                <tr>
                  <td colSpan="6">No hay insumos registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default Insumos;