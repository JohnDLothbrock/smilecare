import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  insumo_id: "",
  stock_actual: "",
  stock_minimo: "",
  ubicacion: ""
};

function InventarioStock() {
  const [stock, setStock] = useState([]);
  const [insumos, setInsumos] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadStock() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/inventario-stock");

      setStock(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadInsumos() {
    try {
      const data = await apiClient.get("/insumos");

      setInsumos(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadStock();
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
      insumo_id: Number(form.insumo_id),
      stock_actual: Number(form.stock_actual),
      stock_minimo: form.stock_minimo === "" ? null : Number(form.stock_minimo),
      ubicacion: form.ubicacion || null
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
        await apiClient.post("/inventario-stock", payload);
        setMessage("Registro de stock creado correctamente.");
      } else {
        await apiClient.put(`/inventario-stock/${editingId}`, payload);
        setMessage("Registro de stock actualizado correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadStock();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(item) {
    setEditingId(item.stock_id);

    setForm({
      insumo_id: item.insumo_id ?? "",
      stock_actual: item.stock_actual ?? "",
      stock_minimo: item.stock_minimo ?? "",
      ubicacion: item.ubicacion ?? ""
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(stockId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este registro de stock?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/inventario-stock/${stockId}`);

      setMessage("Registro de stock eliminado correctamente.");

      await loadStock();
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

  function isLowStock(item) {
    if (item.stock_minimo === null || item.stock_minimo === undefined) {
      return false;
    }

    return Number(item.stock_actual) <= Number(item.stock_minimo);
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Inventario Stock</h2>
          <p>Control de existencias actuales y stock mínimo de insumos.</p>
        </div>
      </div>

      <section className="card">
        <h3>
          {editingId === null
            ? "Crear registro de stock"
            : "Editar registro de stock"}
        </h3>

        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Insumo
            <select
              name="insumo_id"
              value={form.insumo_id}
              onChange={handleChange}
              required
            >
              <option value="">Seleccione un insumo</option>

              {insumos.map((insumo) => (
                <option key={insumo.insumo_id} value={insumo.insumo_id}>
                  {insumo.codigo} - {insumo.nombre}
                </option>
              ))}
            </select>
          </label>

          <label>
            Stock actual
            <input
              type="number"
              name="stock_actual"
              value={form.stock_actual}
              onChange={handleChange}
              min="0"
              step="0.01"
              required
            />
          </label>

          <label>
            Stock mínimo
            <input
              type="number"
              name="stock_minimo"
              value={form.stock_minimo}
              onChange={handleChange}
              min="0"
              step="0.01"
              placeholder="Opcional"
            />
          </label>

          <label>
            Ubicación
            <input
              type="text"
              name="ubicacion"
              value={form.ubicacion}
              onChange={handleChange}
              placeholder="Bodega principal"
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
        <h3>Lista de stock</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Insumo</th>
                <th>Stock actual</th>
                <th>Stock mínimo</th>
                <th>Ubicación</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {stock.map((item) => (
                <tr key={item.stock_id}>
                  <td>{item.stock_id}</td>
                  <td>
                    {item.codigo
                      ? `${item.codigo} - ${item.insumo_nombre || item.nombre}`
                      : item.insumo_nombre || item.insumo_id}
                  </td>
                  <td>{item.stock_actual}</td>
                  <td>{item.stock_minimo}</td>
                  <td>{item.ubicacion}</td>
                  <td>
                    {isLowStock(item) ? (
                      <span className="badge danger-badge">Bajo mínimo</span>
                    ) : (
                      <span className="badge success-badge">Disponible</span>
                    )}
                  </td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(item)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(item.stock_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {stock.length === 0 && !loading && (
                <tr>
                  <td colSpan="7">No hay registros de stock.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default InventarioStock;