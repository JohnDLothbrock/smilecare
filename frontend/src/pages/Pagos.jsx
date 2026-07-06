import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialEditForm = {
  factura_id: "",
  metodo_pago_id: "",
  monto: "",
  fecha_pago: "",
  numero_referencia: "",
  estado: "APLICADO"
};

function Pagos() {
  const [pagos, setPagos] = useState([]);
  const [comprobantes, setComprobantes] = useState([]);
  const [facturas, setFacturas] = useState([]);
  const [metodosPago, setMetodosPago] = useState([]);

  const [editForm, setEditForm] = useState(initialEditForm);
  const [editingPagoId, setEditingPagoId] = useState(null);
  const [selectedPagoId, setSelectedPagoId] = useState(null);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadPagos() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/pagos");

      setPagos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadComprobantes() {
    try {
      const data = await apiClient.get("/comprobantes");

      setComprobantes(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadFacturas() {
    try {
      const data = await apiClient.get("/facturas");

      setFacturas(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadMetodosPago() {
    try {
      const data = await apiClient.get("/metodos-pago");

      setMetodosPago(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadPageData() {
    await Promise.all([
      loadPagos(),
      loadComprobantes(),
      loadFacturas(),
      loadMetodosPago()
    ]);
  }

  useEffect(() => {
    loadPageData();
  }, []);

  function handleEditChange(event) {
    const { name, value } = event.target;

    if (name === "factura_id") {
      const selectedFactura = facturas.find(
        (factura) => String(factura.factura_id) === value
      );

      setEditForm((currentForm) => ({
        ...currentForm,
        factura_id: value,
        monto: selectedFactura?.total ?? currentForm.monto
      }));

      return;
    }

    setEditForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function getPagoById(pagoId) {
    return pagos.find((pago) => String(pago.pago_id) === String(pagoId));
  }

  function getFacturaById(facturaId) {
    return facturas.find(
      (factura) => String(factura.factura_id) === String(facturaId)
    );
  }

  function getComprobanteByPagoId(pagoId) {
    return comprobantes.find(
      (comprobante) => String(comprobante.pago_id) === String(pagoId)
    );
  }

  function getMetodoPagoName(metodoPagoId) {
    const metodo = metodosPago.find(
      (item) => String(item.metodo_pago_id) === String(metodoPagoId)
    );

    if (!metodo) {
      return metodoPagoId || "";
    }

    return metodo.nombre || metodo.nombre_metodo || metodo.descripcion;
  }

  function getFacturaLabel(facturaId) {
    const factura = getFacturaById(facturaId);

    if (!factura) {
      return facturaId || "";
    }

    const paciente = factura.paciente_nombre || `Paciente ${factura.paciente_id}`;

    return `${factura.numero_factura} - ${paciente} - ₡${factura.total}`;
  }

  function getFacturaNumber(facturaId) {
    const factura = getFacturaById(facturaId);

    if (!factura) {
      return facturaId || "";
    }

    return factura.numero_factura;
  }

  function getFacturaPatient(facturaId) {
    const factura = getFacturaById(facturaId);

    if (!factura) {
      return "";
    }

    return factura.paciente_nombre || `Paciente ${factura.paciente_id}`;
  }

  function getStatusBadgeClass(status) {
    if (status === "APLICADO") {
      return "badge success-badge";
    }

    if (status === "ANULADO") {
      return "badge danger-badge";
    }

    return "badge warning-badge";
  }

  function handleViewDetails(pagoId) {
    setSelectedPagoId(pagoId);
    setMessage("");
    setError("");
  }

  function handleEditPago(pago) {
    setEditingPagoId(pago.pago_id);
    setSelectedPagoId(pago.pago_id);

    setEditForm({
      factura_id: pago.factura_id ?? "",
      metodo_pago_id: pago.metodo_pago_id ?? "",
      monto: pago.monto ?? "",
      fecha_pago: pago.fecha_pago ? pago.fecha_pago.substring(0, 10) : "",
      numero_referencia: pago.numero_referencia ?? "",
      estado: pago.estado ?? "APLICADO"
    });

    setMessage("Pago seleccionado para edición.");
    setError("");
  }

  function handleCancelEdit() {
    setEditingPagoId(null);
    setEditForm(initialEditForm);
    setMessage("");
    setError("");
  }

  function buildPagoUpdatePayload() {
    return {
      factura_id: Number(editForm.factura_id),
      metodo_pago_id: Number(editForm.metodo_pago_id),
      monto: Number(editForm.monto),
      fecha_pago: editForm.fecha_pago || null,
      numero_referencia: editForm.numero_referencia || null,
      estado: editForm.estado
    };
  }

  function buildComprobantePayload(pagoId) {
    const factura = getFacturaById(editForm.factura_id);
    const numeroFactura = factura?.numero_factura || `FACTURA-${editForm.factura_id}`;

    return {
      pago_id: Number(pagoId),
      numero_comprobante: numeroFactura,
      tipo_comprobante: "FACTURA",
      fecha_emision: editForm.fecha_pago || null,
      detalle: `Factura ${numeroFactura} pagada con referencia ${editForm.numero_referencia}`
    };
  }

  async function handleSubmitEdit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setMessage("");
      setError("");

      const pagoPayload = buildPagoUpdatePayload();

      await apiClient.put(`/pagos/${editingPagoId}`, pagoPayload);

      const comprobante = getComprobanteByPagoId(editingPagoId);
      const comprobantePayload = buildComprobantePayload(editingPagoId);

      if (comprobante) {
        await apiClient.put(
          `/comprobantes/${comprobante.comprobante_id}`,
          comprobantePayload
        );
      } else {
        await apiClient.post("/comprobantes", comprobantePayload);
      }

      setEditingPagoId(null);
      setEditForm(initialEditForm);

      setMessage("Pago actualizado correctamente.");

      await loadPageData();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDeletePago(pagoId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este pago? También se eliminará su comprobante."
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setMessage("");
      setError("");

      const comprobante = getComprobanteByPagoId(pagoId);

      if (comprobante) {
        await apiClient.delete(`/comprobantes/${comprobante.comprobante_id}`);
      }

      await apiClient.delete(`/pagos/${pagoId}`);

      if (String(selectedPagoId) === String(pagoId)) {
        setSelectedPagoId(null);
      }

      if (String(editingPagoId) === String(pagoId)) {
        setEditingPagoId(null);
        setEditForm(initialEditForm);
      }

      setMessage("Pago eliminado correctamente.");

      await loadPageData();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const selectedPago = selectedPagoId ? getPagoById(selectedPagoId) : null;

  const selectedComprobante = selectedPago
    ? getComprobanteByPagoId(selectedPago.pago_id)
    : null;

  const sortedPagos = [...pagos].sort(
    (a, b) => Number(b.pago_id) - Number(a.pago_id)
  );

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Pagos</h2>
          <p>
            Revisión y mantenimiento de pagos generados desde Caja.
          </p>
        </div>
      </div>

      <section className="card">
        <h3>Pagos registrados</h3>

        <p className="helper-text">
          Para registrar un nuevo pago use la página Caja. Esta sección es para
          revisar, corregir o anular pagos existentes.
        </p>

        {loading && <p>Cargando...</p>}

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Factura</th>
                <th>Paciente</th>
                <th>Método</th>
                <th>Monto</th>
                <th>Fecha</th>
                <th>Referencia</th>
                <th>Comprobante</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {sortedPagos.map((pago) => {
                const comprobante = getComprobanteByPagoId(pago.pago_id);

                return (
                  <tr key={pago.pago_id}>
                    <td>{pago.pago_id}</td>
                    <td>{pago.numero_factura || getFacturaNumber(pago.factura_id)}</td>
                    <td>{pago.paciente_nombre || getFacturaPatient(pago.factura_id)}</td>
                    <td>
                      {pago.metodo_pago_nombre ||
                        pago.nombre_metodo_pago ||
                        getMetodoPagoName(pago.metodo_pago_id)}
                    </td>
                    <td>₡{pago.monto}</td>
                    <td>
                      {pago.fecha_pago
                        ? pago.fecha_pago.substring(0, 10)
                        : ""}
                    </td>
                    <td>{pago.numero_referencia}</td>
                    <td>
                      {comprobante
                        ? comprobante.numero_comprobante
                        : "Sin comprobante"}
                    </td>
                    <td>
                      <span className={getStatusBadgeClass(pago.estado)}>
                        {pago.estado}
                      </span>
                    </td>
                    <td>
                      <button
                        type="button"
                        className="small-button"
                        onClick={() => handleViewDetails(pago.pago_id)}
                      >
                        Ver detalle
                      </button>

                      <button
                        type="button"
                        className="small-button"
                        onClick={() => handleEditPago(pago)}
                      >
                        Editar
                      </button>

                      <button
                        type="button"
                        className="danger-button"
                        onClick={() => handleDeletePago(pago.pago_id)}
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                );
              })}

              {pagos.length === 0 && !loading && (
                <tr>
                  <td colSpan="10">No hay pagos registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      {editingPagoId !== null && (
        <section className="card">
          <h3>Editar pago</h3>

          <p className="helper-text">
            Modifique solamente datos administrativos del pago. La factura y el
            comprobante se mantienen relacionados automáticamente.
          </p>

          <form className="form-grid" onSubmit={handleSubmitEdit}>
            <label>
              Factura
              <select
                name="factura_id"
                value={editForm.factura_id}
                onChange={handleEditChange}
                required
              >
                <option value="">Seleccione una factura</option>

                {facturas.map((factura) => (
                  <option key={factura.factura_id} value={factura.factura_id}>
                    {getFacturaLabel(factura.factura_id)}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Método de pago
              <select
                name="metodo_pago_id"
                value={editForm.metodo_pago_id}
                onChange={handleEditChange}
                required
              >
                <option value="">Seleccione un método de pago</option>

                {metodosPago.map((metodo) => (
                  <option
                    key={metodo.metodo_pago_id}
                    value={metodo.metodo_pago_id}
                  >
                    {metodo.nombre || metodo.nombre_metodo || metodo.descripcion}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Monto
              <input
                type="number"
                name="monto"
                value={editForm.monto}
                onChange={handleEditChange}
                min="0"
                step="0.01"
                required
              />
            </label>

            <label>
              Fecha de pago
              <input
                type="date"
                name="fecha_pago"
                value={editForm.fecha_pago}
                onChange={handleEditChange}
              />
            </label>

            <label>
              Número de referencia
              <input
                type="text"
                name="numero_referencia"
                value={editForm.numero_referencia}
                onChange={handleEditChange}
                required
              />
            </label>

            <label>
              Estado
              <select
                name="estado"
                value={editForm.estado}
                onChange={handleEditChange}
                required
              >
                <option value="APLICADO">APLICADO</option>
                <option value="PENDIENTE">PENDIENTE</option>
                <option value="ANULADO">ANULADO</option>
              </select>
            </label>

            <div className="form-actions">
              <button type="submit" disabled={loading}>
                Guardar cambios
              </button>

              <button
                type="button"
                className="secondary-button"
                onClick={handleCancelEdit}
              >
                Cancelar
              </button>
            </div>
          </form>
        </section>
      )}

      <section className="card">
        <h3>Detalle del pago</h3>

        {!selectedPago && (
          <p className="helper-text">
            Seleccione un pago con el botón Ver detalle para revisar la
            información relacionada.
          </p>
        )}

        {selectedPago && (
          <div className="payment-summary">
            <p>
              <strong>Pago ID:</strong> {selectedPago.pago_id}
            </p>

            <p>
              <strong>Factura:</strong>{" "}
              {selectedPago.numero_factura ||
                getFacturaNumber(selectedPago.factura_id)}
            </p>

            <p>
              <strong>Paciente:</strong>{" "}
              {selectedPago.paciente_nombre ||
                getFacturaPatient(selectedPago.factura_id)}
            </p>

            <p>
              <strong>Método de pago:</strong>{" "}
              {selectedPago.metodo_pago_nombre ||
                selectedPago.nombre_metodo_pago ||
                getMetodoPagoName(selectedPago.metodo_pago_id)}
            </p>

            <p>
              <strong>Monto:</strong> ₡{selectedPago.monto}
            </p>

            <p>
              <strong>Fecha:</strong>{" "}
              {selectedPago.fecha_pago
                ? selectedPago.fecha_pago.substring(0, 10)
                : ""}
            </p>

            <p>
              <strong>Referencia:</strong> {selectedPago.numero_referencia}
            </p>

            <p>
              <strong>Estado:</strong>{" "}
              <span className={getStatusBadgeClass(selectedPago.estado)}>
                {selectedPago.estado}
              </span>
            </p>

            <p>
              <strong>Comprobante:</strong>{" "}
              {selectedComprobante
                ? selectedComprobante.numero_comprobante
                : "Sin comprobante registrado"}
            </p>

            <p>
              <strong>Tipo de comprobante:</strong>{" "}
              {selectedComprobante
                ? selectedComprobante.tipo_comprobante
                : "No disponible"}
            </p>

            <p>
              <strong>Detalle:</strong>{" "}
              {selectedComprobante
                ? selectedComprobante.detalle
                : "No disponible"}
            </p>
          </div>
        )}
      </section>
    </section>
  );
}

export default Pagos;