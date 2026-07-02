import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialStockForm = {
  insumo_id: "",
  stock_actual: "",
  stock_minimo: "",
  ubicacion: ""
};

const initialMovementForm = {
  insumo_id: "",
  usuario_id: "",
  detalle_compra_id: "",
  consulta_id: "",
  tipo_movimiento: "ENTRADA",
  cantidad: "",
  fecha_movimiento: "",
  motivo: ""
};

function InventarioStock() {
  const [stock, setStock] = useState([]);
  const [movimientos, setMovimientos] = useState([]);
  const [insumos, setInsumos] = useState([]);

  const [stockForm, setStockForm] = useState(initialStockForm);
  const [movementForm, setMovementForm] = useState(initialMovementForm);

  const [editingStockId, setEditingStockId] = useState(null);

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

  async function loadMovimientos() {
    try {
      const data = await apiClient.get("/movimientos-inventario");

      setMovimientos(data);
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
    loadStock();
    loadMovimientos();
    loadInsumos();
  }, []);

  function handleStockChange(event) {
    const { name, value } = event.target;

    setStockForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function handleMovementChange(event) {
    const { name, value } = event.target;

    setMovementForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function buildStockPayload() {
    return {
      insumo_id: Number(stockForm.insumo_id),
      stock_actual: Number(stockForm.stock_actual),
      stock_minimo:
        stockForm.stock_minimo === "" ? null : Number(stockForm.stock_minimo),
      ubicacion: stockForm.ubicacion || null
    };
  }

  function buildMovementPayload() {
    return {
      insumo_id: Number(movementForm.insumo_id),
      usuario_id: Number(movementForm.usuario_id),
      detalle_compra_id:
        movementForm.detalle_compra_id === ""
          ? null
          : Number(movementForm.detalle_compra_id),
      consulta_id:
        movementForm.consulta_id === "" ? null : Number(movementForm.consulta_id),
      tipo_movimiento: movementForm.tipo_movimiento,
      cantidad: Number(movementForm.cantidad),
      fecha_movimiento: movementForm.fecha_movimiento || null,
      motivo: movementForm.motivo || null
    };
  }

  async function handleStockSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const payload = buildStockPayload();

      if (editingStockId === null) {
        await apiClient.post("/inventario-stock", payload);
        setMessage("Registro de stock creado correctamente.");
      } else {
        await apiClient.put(`/inventario-stock/${editingStockId}`, payload);
        setMessage("Registro de stock actualizado correctamente.");
      }

      setStockForm(initialStockForm);
      setEditingStockId(null);

      await loadStock();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleMovementSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const payload = buildMovementPayload();

      await apiClient.post("/movimientos-inventario", payload);

      setMovementForm(initialMovementForm);
      setMessage("Movimiento de inventario registrado correctamente.");

      await loadStock();
      await loadMovimientos();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEditStock(item) {
    setEditingStockId(item.stock_id);

    setStockForm({
      insumo_id: item.insumo_id ?? "",
      stock_actual: item.stock_actual ?? "",
      stock_minimo: item.stock_minimo ?? "",
      ubicacion: item.ubicacion ?? ""
    });

    setMessage("");
    setError("");
  }

  async function handleDeleteStock(stockId) {
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

  async function handleReverseMovement(movimiento) {
    const confirmed = window.confirm(
      "¿Seguro que desea revertir este movimiento? Esto puede modificar el stock actual."
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(
        `/movimientos-inventario/${movimiento.movimiento_id}`
      );

      setMessage("Movimiento revertido correctamente.");

      await loadStock();
      await loadMovimientos();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleCancelStockEdit() {
    setEditingStockId(null);
    setStockForm(initialStockForm);
    setMessage("");
    setError("");
  }

  function handlePrepareMovement(item) {
    setMovementForm((currentForm) => ({
      ...currentForm,
      insumo_id: item.insumo_id ?? ""
    }));

    setMessage("Insumo seleccionado para registrar movimiento.");
    setError("");
  }

  function isLowStock(item) {
    if (item.stock_minimo === null || item.stock_minimo === undefined) {
      return false;
    }

    return Number(item.stock_actual) <= Number(item.stock_minimo);
  }

  function getInsumoLabelById(insumoId) {
    const insumo = insumos.find(
      (item) => String(item.insumo_id) === String(insumoId)
    );

    if (!insumo) {
      return insumoId;
    }

    return `${insumo.codigo} - ${insumo.nombre}`;
  }

  function getMovementBadgeClass(tipoMovimiento) {
    if (tipoMovimiento === "ENTRADA") {
      return "badge success-badge";
    }

    if (tipoMovimiento === "SALIDA") {
      return "badge danger-badge";
    }

    return "badge warning-badge";
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Stock e Inventario</h2>
          <p>
            Control de existencias actuales, stock mínimo y movimientos de
            inventario.
          </p>
        </div>
      </div>

      <section className="card">
        <h3>
          {editingStockId === null
            ? "Crear registro de stock"
            : "Editar registro de stock"}
        </h3>

        <p className="helper-text">
          Use esta sección para crear el stock inicial, definir stock mínimo o
          cambiar la ubicación. Para entradas, salidas o ajustes diarios, use
          la sección de movimientos.
        </p>

        <form className="form-grid" onSubmit={handleStockSubmit}>
          <label>
            Insumo
            <select
              name="insumo_id"
              value={stockForm.insumo_id}
              onChange={handleStockChange}
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
              value={stockForm.stock_actual}
              onChange={handleStockChange}
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
              value={stockForm.stock_minimo}
              onChange={handleStockChange}
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
              value={stockForm.ubicacion}
              onChange={handleStockChange}
              placeholder="Bodega principal"
            />
          </label>

          <div className="form-actions">
            <button type="submit" disabled={loading}>
              {editingStockId === null ? "Guardar" : "Actualizar"}
            </button>

            {editingStockId !== null && (
              <button
                type="button"
                className="secondary-button"
                onClick={handleCancelStockEdit}
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
        <h3>Registrar movimiento</h3>

        <p className="helper-text">
          Una entrada aumenta el stock, una salida disminuye el stock y un
          ajuste establece una nueva cantidad de stock.
        </p>

        <form className="form-grid" onSubmit={handleMovementSubmit}>
          <label>
            Insumo
            <select
              name="insumo_id"
              value={movementForm.insumo_id}
              onChange={handleMovementChange}
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
            Tipo de movimiento
            <select
              name="tipo_movimiento"
              value={movementForm.tipo_movimiento}
              onChange={handleMovementChange}
              required
            >
              <option value="ENTRADA">ENTRADA</option>
              <option value="SALIDA">SALIDA</option>
              <option value="AJUSTE">AJUSTE</option>
            </select>
          </label>

          <label>
            Cantidad
            <input
              type="number"
              name="cantidad"
              value={movementForm.cantidad}
              onChange={handleMovementChange}
              min="0.01"
              step="0.01"
              required
            />
          </label>

          <label>
            Usuario ID
            <input
              type="number"
              name="usuario_id"
              value={movementForm.usuario_id}
              onChange={handleMovementChange}
              placeholder="Ejemplo: 1"
              required
            />
          </label>

          <label>
            Fecha movimiento
            <input
              type="datetime-local"
              name="fecha_movimiento"
              value={movementForm.fecha_movimiento}
              onChange={handleMovementChange}
            />
          </label>

          <label>
            Detalle compra ID
            <input
              type="number"
              name="detalle_compra_id"
              value={movementForm.detalle_compra_id}
              onChange={handleMovementChange}
              placeholder="Opcional"
            />
          </label>

          <label>
            Consulta ID
            <input
              type="number"
              name="consulta_id"
              value={movementForm.consulta_id}
              onChange={handleMovementChange}
              placeholder="Opcional"
            />
          </label>

          <label>
            Motivo
            <textarea
              name="motivo"
              value={movementForm.motivo}
              onChange={handleMovementChange}
              rows="3"
              placeholder="Ejemplo: Compra recibida, uso en consulta, ajuste manual..."
            />
          </label>

          <div className="form-actions">
            <button type="submit" disabled={loading}>
              Registrar movimiento
            </button>
          </div>
        </form>
      </section>

      <section className="card">
        <h3>Stock actual</h3>

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
                      onClick={() => handlePrepareMovement(item)}
                    >
                      Mover
                    </button>

                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEditStock(item)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDeleteStock(item.stock_id)}
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

      <section className="card">
        <h3>Historial de movimientos</h3>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Insumo</th>
                <th>Tipo</th>
                <th>Cantidad</th>
                <th>Usuario</th>
                <th>Fecha</th>
                <th>Motivo</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {movimientos.map((movimiento) => (
                <tr key={movimiento.movimiento_id}>
                  <td>{movimiento.movimiento_id}</td>
                  <td>
                    {movimiento.codigo
                      ? `${movimiento.codigo} - ${
                          movimiento.insumo_nombre || movimiento.nombre
                        }`
                      : movimiento.insumo_nombre ||
                        getInsumoLabelById(movimiento.insumo_id)}
                  </td>
                  <td>
                    <span
                      className={getMovementBadgeClass(
                        movimiento.tipo_movimiento
                      )}
                    >
                      {movimiento.tipo_movimiento}
                    </span>
                  </td>
                  <td>{movimiento.cantidad}</td>
                  <td>{movimiento.usuario_id}</td>
                  <td>
                    {movimiento.fecha_movimiento
                      ? movimiento.fecha_movimiento
                          .substring(0, 16)
                          .replace("T", " ")
                      : ""}
                  </td>
                  <td>{movimiento.motivo}</td>
                  <td>
                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleReverseMovement(movimiento)}
                    >
                      Revertir
                    </button>
                  </td>
                </tr>
              ))}

              {movimientos.length === 0 && (
                <tr>
                  <td colSpan="8">No hay movimientos registrados.</td>
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