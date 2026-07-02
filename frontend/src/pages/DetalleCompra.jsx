import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  compra_id: "",
  insumo_id: "",
  cantidad: "",
  costo_unitario: ""
};

function DetalleCompra() {
  const [detalles, setDetalles] = useState([]);
  const [compras, setCompras] = useState([]);
  const [insumos, setInsumos] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadDetalles() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/detalle-compra");

      setDetalles(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadCompras() {
    try {
      const data = await apiClient.get("/compras");

      setCompras(data);
    } catch (err) {
      setError(err.message);
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
    loadDetalles();
    loadCompras();
    loadInsumos();
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function getSubtotalPreview() {
    const cantidad = Number(form.cantidad || 0);
    const costoUnitario = Number(form.costo_unitario || 0);

    return cantidad * costoUnitario;
  }

  function buildPayload() {
    return {
      compra_id: Number(form.compra_id),
      insumo_id: Number(form.insumo_id),
      cantidad: Number(form.cantidad),
      costo_unitario: Number(form.costo_unitario),
      subtotal: getSubtotalPreview()
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
        await apiClient.post("/detalle-compra", payload);
        setMessage("Detalle de compra creado correctamente.");
      } else {
        await apiClient.put(`/detalle-compra/${editingId}`, payload);
        setMessage("Detalle de compra actualizado correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadDetalles();
      await loadCompras();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(detalle) {
    setEditingId(detalle.detalle_compra_id);

    setForm({
      compra_id: detalle.compra_id ?? "",
      insumo_id: detalle.insumo_id ?? "",
      cantidad: detalle.cantidad ?? "",
      costo_unitario: detalle.costo_unitario ?? ""
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(detalleCompraId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este detalle de compra?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/detalle-compra/${detalleCompraId}`);

      setMessage("Detalle de compra eliminado correctamente.");

      await loadDetalles();
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

  function formatCompraLabel(compra) {
    const proveedor = compra.proveedor_nombre || `Proveedor ${compra.proveedor_id}`;
    const fecha = compra.fecha_compra
      ? compra.fecha_compra.substring(0, 10)
      : "Sin fecha";

    return `Compra ${compra.compra_id} - ${proveedor} - ${fecha}`;
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Detalle Compra</h2>
          <p>Registro de insumos comprados en cada compra.</p>
        </div>
      </div>

      <section className="card">
        <h3>
          {editingId === null
            ? "Crear detalle de compra"
            : "Editar detalle de compra"}
        </h3>

        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Compra
            <select
              name="compra_id"
              value={form.compra_id}
              onChange={handleChange}
              required
            >
              <option value="">Seleccione una compra</option>

              {compras.map((compra) => (
                <option key={compra.compra_id} value={compra.compra_id}>
                  {formatCompraLabel(compra)}
                </option>
              ))}
            </select>
          </label>

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
            Cantidad
            <input
              type="number"
              name="cantidad"
              value={form.cantidad}
              onChange={handleChange}
              min="1"
              step="0.01"
              required
            />
          </label>

          <label>
            Costo unitario
            <input
              type="number"
              name="costo_unitario"
              value={form.costo_unitario}
              onChange={handleChange}
              min="0"
              step="0.01"
              required
            />
          </label>

          <div className="total-preview">
            <strong>Subtotal:</strong> ₡{getSubtotalPreview()}
          </div>

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
        <h3>Lista de detalles de compra</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Compra</th>
                <th>Insumo</th>
                <th>Cantidad</th>
                <th>Costo unitario</th>
                <th>Subtotal</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {detalles.map((detalle) => (
                <tr key={detalle.detalle_compra_id}>
                  <td>{detalle.detalle_compra_id}</td>
                  <td>{detalle.compra_id}</td>
                  <td>
                    {detalle.insumo_nombre ||
                      detalle.nombre_insumo ||
                      detalle.insumo_id}
                  </td>
                  <td>{detalle.cantidad}</td>
                  <td>₡{detalle.costo_unitario}</td>
                  <td>₡{detalle.subtotal}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(detalle)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() =>
                        handleDelete(detalle.detalle_compra_id)
                      }
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {detalles.length === 0 && !loading && (
                <tr>
                  <td colSpan="7">No hay detalles de compra registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default DetalleCompra;