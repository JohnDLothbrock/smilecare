import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  proveedor_id: "",
  usuario_id: "",
  fecha_compra: "",
  total: "0",
  estado: "REGISTRADA"
};

function Compras() {
  const [compras, setCompras] = useState([]);
  const [proveedores, setProveedores] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadCompras() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/compras");

      setCompras(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadProveedores() {
    try {
      const data = await apiClient.get("/proveedores");

      setProveedores(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadCompras();
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
      proveedor_id: Number(form.proveedor_id),
      usuario_id: Number(form.usuario_id),
      fecha_compra: form.fecha_compra || null,
      total: Number(form.total),
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
        await apiClient.post("/compras", payload);
        setMessage("Compra creada correctamente.");
      } else {
        await apiClient.put(`/compras/${editingId}`, payload);
        setMessage("Compra actualizada correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadCompras();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(compra) {
    setEditingId(compra.compra_id);

    setForm({
      proveedor_id: compra.proveedor_id ?? "",
      usuario_id: compra.usuario_id ?? "",
      fecha_compra: compra.fecha_compra
        ? compra.fecha_compra.substring(0, 10)
        : "",
      total: compra.total ?? "0",
      estado: compra.estado ?? "REGISTRADA"
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(compraId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar esta compra?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/compras/${compraId}`);

      setMessage("Compra eliminada correctamente.");

      await loadCompras();
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
          <h2>Compras</h2>
          <p>Registro de compras realizadas a proveedores.</p>
        </div>
      </div>

      <section className="card">
        <h3>{editingId === null ? "Crear compra" : "Editar compra"}</h3>

        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Proveedor
            <select
              name="proveedor_id"
              value={form.proveedor_id}
              onChange={handleChange}
              required
            >
              <option value="">Seleccione un proveedor</option>

              {proveedores.map((proveedor) => (
                <option
                  key={proveedor.proveedor_id}
                  value={proveedor.proveedor_id}
                >
                  {proveedor.nombre}
                </option>
              ))}
            </select>
          </label>

          <label>
            Usuario ID
            <input
              type="number"
              name="usuario_id"
              value={form.usuario_id}
              onChange={handleChange}
              placeholder="Ejemplo: 1"
              required
            />
          </label>

          <label>
            Fecha de compra
            <input
              type="date"
              name="fecha_compra"
              value={form.fecha_compra}
              onChange={handleChange}
            />
          </label>

          <label>
            Total
            <input
              type="number"
              name="total"
              value={form.total}
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
              <option value="REGISTRADA">REGISTRADA</option>
              <option value="RECIBIDA">RECIBIDA</option>
              <option value="ANULADA">ANULADA</option>
            </select>
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

        <p className="helper-text">
          El Usuario ID corresponde al usuario responsable de registrar la
          compra. Puede consultar el ID en la tabla USUARIOS.
        </p>

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
      </section>

      <section className="card">
        <h3>Lista de compras</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Proveedor</th>
                <th>Usuario</th>
                <th>Fecha</th>
                <th>Total</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {compras.map((compra) => (
                <tr key={compra.compra_id}>
                  <td>{compra.compra_id}</td>
                  <td>{compra.proveedor_nombre || compra.proveedor_id}</td>
                  <td>{compra.usuario_id}</td>
                  <td>
                    {compra.fecha_compra
                      ? compra.fecha_compra.substring(0, 10)
                      : ""}
                  </td>
                  <td>₡{compra.total}</td>
                  <td>{compra.estado}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(compra)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(compra.compra_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {compras.length === 0 && !loading && (
                <tr>
                  <td colSpan="7">No hay compras registradas.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default Compras;