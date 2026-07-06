import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const TAX_RATE = 0.13;

const initialEditForm = {
  paciente_id: "",
  consulta_id: "",
  numero_factura: "",
  fecha_emision: "",
  estado: "PENDIENTE"
};

function Facturas() {
  const [facturas, setFacturas] = useState([]);
  const [detallesFactura, setDetallesFactura] = useState([]);
  const [pacientes, setPacientes] = useState([]);
  const [consultas, setConsultas] = useState([]);

  const [editForm, setEditForm] = useState(initialEditForm);
  const [editingFacturaId, setEditingFacturaId] = useState(null);
  const [selectedFacturaId, setSelectedFacturaId] = useState(null);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadFacturas() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/facturas");

      setFacturas(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadDetallesFactura() {
    try {
      const data = await apiClient.get("/detalle-factura");

      setDetallesFactura(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadPacientes() {
    try {
      const data = await apiClient.get("/pacientes");

      setPacientes(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadConsultas() {
    try {
      const data = await apiClient.get("/consultas");

      setConsultas(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadPageData() {
    await Promise.all([
      loadFacturas(),
      loadDetallesFactura(),
      loadPacientes(),
      loadConsultas()
    ]);
  }

  useEffect(() => {
    loadPageData();
  }, []);

  function roundMoney(value) {
    return Math.round((Number(value) + Number.EPSILON) * 100) / 100;
  }

  function handleEditChange(event) {
    const { name, value } = event.target;

    setEditForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function getFacturaById(facturaId) {
    return facturas.find(
      (factura) => String(factura.factura_id) === String(facturaId)
    );
  }

  function getDetallesByFacturaId(facturaId) {
    return detallesFactura.filter(
      (detalle) => String(detalle.factura_id) === String(facturaId)
    );
  }

  function getFacturaSubtotal(factura) {
    const detalles = getDetallesByFacturaId(factura.factura_id);

    if (detalles.length > 0) {
      return roundMoney(
        detalles.reduce(
          (total, detalle) => total + Number(detalle.subtotal || 0),
          0
        )
      );
    }

    return roundMoney(factura.subtotal || 0);
  }

  function getFacturaImpuesto(factura) {
    return roundMoney(getFacturaSubtotal(factura) * TAX_RATE);
  }

  function getFacturaTotal(factura) {
    if (factura.total !== undefined && factura.total !== null) {
      return factura.total;
    }

    return roundMoney(getFacturaSubtotal(factura) + getFacturaImpuesto(factura));
  }

  function getPacienteName(pacienteId) {
    const paciente = pacientes.find(
      (item) => String(item.paciente_id) === String(pacienteId)
    );

    if (!paciente) {
      return pacienteId || "";
    }

    return `${paciente.nombre} ${paciente.apellido}`;
  }

  function formatConsultaLabel(consulta) {
    const paciente =
      consulta.paciente_nombre || `Paciente ${consulta.paciente_id}`;

    const doctor =
      consulta.doctor_nombre || `Doctor ${consulta.doctor_id}`;

    return `Consulta ${consulta.consulta_id} - ${paciente} con ${doctor}`;
  }

  function getConsultaLabel(consultaId) {
    const consulta = consultas.find(
      (item) => String(item.consulta_id) === String(consultaId)
    );

    if (!consulta) {
      return consultaId || "";
    }

    return formatConsultaLabel(consulta);
  }

  function getStatusBadgeClass(status) {
    if (status === "PAGADA") {
      return "badge success-badge";
    }

    if (status === "ANULADA") {
      return "badge danger-badge";
    }

    return "badge warning-badge";
  }

  function handleViewDetails(facturaId) {
    setSelectedFacturaId(facturaId);
    setMessage("");
    setError("");
  }

  function handleEditFactura(factura) {
    setEditingFacturaId(factura.factura_id);
    setSelectedFacturaId(factura.factura_id);

    setEditForm({
      paciente_id: factura.paciente_id ?? "",
      consulta_id: factura.consulta_id ?? "",
      numero_factura: factura.numero_factura ?? "",
      fecha_emision: factura.fecha_emision
        ? factura.fecha_emision.substring(0, 10)
        : "",
      estado: factura.estado ?? "PENDIENTE"
    });

    setMessage("Factura seleccionada para edición.");
    setError("");
  }

  function handleCancelEdit() {
    setEditingFacturaId(null);
    setEditForm(initialEditForm);
    setMessage("");
    setError("");
  }

  function buildFacturaUpdatePayload() {
    const factura = getFacturaById(editingFacturaId);

    if (!factura) {
      throw new Error("No se encontró la factura seleccionada.");
    }

    const subtotal = getFacturaSubtotal(factura);
    const impuesto = roundMoney(subtotal * TAX_RATE);

    return {
      paciente_id: Number(editForm.paciente_id),
      consulta_id: Number(editForm.consulta_id),
      numero_factura: editForm.numero_factura,
      fecha_emision: editForm.fecha_emision || null,
      subtotal,
      impuesto,
      estado: editForm.estado
    };
  }

  async function handleSubmitEdit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setMessage("");
      setError("");

      const payload = buildFacturaUpdatePayload();

      await apiClient.put(`/facturas/${editingFacturaId}`, payload);

      setEditingFacturaId(null);
      setEditForm(initialEditForm);

      setMessage("Factura actualizada correctamente.");

      await loadFacturas();
      await loadDetallesFactura();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function syncFacturaTotals(facturaId, updatedDetails) {
    const factura = getFacturaById(facturaId);

    if (!factura) {
      return;
    }

    const relatedDetails = updatedDetails.filter(
      (detalle) => String(detalle.factura_id) === String(facturaId)
    );

    const subtotal = roundMoney(
      relatedDetails.reduce(
        (total, detalle) => total + Number(detalle.subtotal || 0),
        0
      )
    );

    const impuesto = roundMoney(subtotal * TAX_RATE);

    await apiClient.put(`/facturas/${facturaId}`, {
      paciente_id: Number(factura.paciente_id),
      consulta_id: Number(factura.consulta_id),
      numero_factura: factura.numero_factura,
      fecha_emision: factura.fecha_emision
        ? factura.fecha_emision.substring(0, 10)
        : null,
      subtotal,
      impuesto,
      estado: factura.estado
    });
  }

  async function handleDeleteDetalle(detalleFacturaId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este servicio de la factura?"
    );

    if (!confirmed) {
      return;
    }

    const detalle = detallesFactura.find(
      (item) => String(item.detalle_factura_id) === String(detalleFacturaId)
    );

    try {
      setLoading(true);
      setMessage("");
      setError("");

      await apiClient.delete(`/detalle-factura/${detalleFacturaId}`);

      const updatedDetails = detallesFactura.filter(
        (item) => String(item.detalle_factura_id) !== String(detalleFacturaId)
      );

      if (detalle?.factura_id) {
        await syncFacturaTotals(detalle.factura_id, updatedDetails);
      }

      setMessage("Servicio eliminado correctamente.");

      await loadFacturas();
      await loadDetallesFactura();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDeleteFactura(facturaId) {
    const factura = getFacturaById(facturaId);

    if (!factura) {
      setError("No se encontró la factura seleccionada.");
      return;
    }

    const confirmed = window.confirm(
      `¿Seguro que desea anular esta factura?\n\n` +
        `Factura: ${factura.numero_factura}\n\n` +
        `No se eliminarán los servicios, pagos ni comprobantes relacionados.\n` +
        `La factura se moverá a la sección de facturas anuladas y podrá restaurarse después.`
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setMessage("");
      setError("");

      await apiClient.delete(`/facturas/${facturaId}`);

      if (String(selectedFacturaId) === String(facturaId)) {
        setSelectedFacturaId(null);
      }

      if (String(editingFacturaId) === String(facturaId)) {
        setEditingFacturaId(null);
        setEditForm(initialEditForm);
      }

      setMessage("Factura anulada correctamente.");

      await loadFacturas();
      await loadDetallesFactura();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleRestoreFactura(facturaId) {
    const factura = getFacturaById(facturaId);

    if (!factura) {
      setError("No se encontró la factura seleccionada.");
      return;
    }

    const confirmed = window.confirm(
      `¿Desea restaurar esta factura?\n\n` +
        `Factura: ${factura.numero_factura}\n\n` +
        `El sistema la devolverá a PAGADA si tiene pagos aplicados, o a PENDIENTE si no tiene pagos.`
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setMessage("");
      setError("");

      await apiClient.put(`/facturas/${facturaId}/restaurar`, {});

      setMessage("Factura restaurada correctamente.");

      await loadFacturas();
      await loadDetallesFactura();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const activeFacturas = facturas.filter(
    (factura) => factura.estado !== "ANULADA"
  );

  const deletedFacturas = facturas.filter(
    (factura) => factura.estado === "ANULADA"
  );

  const selectedFactura = selectedFacturaId
    ? getFacturaById(selectedFacturaId)
    : null;

  const selectedFacturaDetails = selectedFacturaId
    ? getDetallesByFacturaId(selectedFacturaId)
    : [];

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Facturas</h2>
          <p>
            Revisión, anulación y restauración de facturas generadas desde Caja.
          </p>
        </div>
      </div>

      <section className="card">
        <h3>Facturas activas</h3>

        <p className="helper-text">
          Para crear una nueva factura use la página Caja. Esta sección es para
          revisar, corregir o anular facturas existentes.
        </p>

        {loading && <p>Cargando...</p>}

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Número</th>
                <th>Paciente</th>
                <th>Consulta</th>
                <th>Fecha</th>
                <th>Subtotal</th>
                <th>Impuesto</th>
                <th>Total</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {activeFacturas.map((factura) => (
                <tr key={factura.factura_id}>
                  <td>{factura.factura_id}</td>
                  <td>{factura.numero_factura}</td>
                  <td>
                    {factura.paciente_nombre ||
                      getPacienteName(factura.paciente_id)}
                  </td>
                  <td>{factura.consulta_id}</td>
                  <td>
                    {factura.fecha_emision
                      ? factura.fecha_emision.substring(0, 10)
                      : ""}
                  </td>
                  <td>₡{getFacturaSubtotal(factura)}</td>
                  <td>₡{getFacturaImpuesto(factura)}</td>
                  <td>₡{getFacturaTotal(factura)}</td>
                  <td>
                    <span className={getStatusBadgeClass(factura.estado)}>
                      {factura.estado}
                    </span>
                  </td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleViewDetails(factura.factura_id)}
                    >
                      Ver servicios
                    </button>

                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEditFactura(factura)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDeleteFactura(factura.factura_id)}
                    >
                      Anular
                    </button>
                  </td>
                </tr>
              ))}

              {activeFacturas.length === 0 && !loading && (
                <tr>
                  <td colSpan="10">No hay facturas activas registradas.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <h3>Facturas anuladas / eliminadas</h3>

        <p className="helper-text">
          Estas facturas no se muestran como activas, pero se conservan con sus
          servicios, pagos y comprobantes relacionados. Puede restaurarlas si es
          necesario.
        </p>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Número</th>
                <th>Paciente</th>
                <th>Consulta</th>
                <th>Fecha</th>
                <th>Total</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {deletedFacturas.map((factura) => (
                <tr key={factura.factura_id}>
                  <td>{factura.factura_id}</td>
                  <td>{factura.numero_factura}</td>
                  <td>
                    {factura.paciente_nombre ||
                      getPacienteName(factura.paciente_id)}
                  </td>
                  <td>{factura.consulta_id}</td>
                  <td>
                    {factura.fecha_emision
                      ? factura.fecha_emision.substring(0, 10)
                      : ""}
                  </td>
                  <td>₡{getFacturaTotal(factura)}</td>
                  <td>
                    <span className={getStatusBadgeClass(factura.estado)}>
                      {factura.estado}
                    </span>
                  </td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleRestoreFactura(factura.factura_id)}
                    >
                      Restaurar
                    </button>

                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleViewDetails(factura.factura_id)}
                    >
                      Ver servicios
                    </button>
                  </td>
                </tr>
              ))}

              {deletedFacturas.length === 0 && !loading && (
                <tr>
                  <td colSpan="8">No hay facturas anuladas.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      {editingFacturaId !== null && (
        <section className="card">
          <h3>Editar factura</h3>

          <p className="helper-text">
            Modifique solamente datos administrativos de la factura. Los
            servicios y montos provienen del detalle facturado.
          </p>

          <form className="form-grid" onSubmit={handleSubmitEdit}>
            <label>
              Paciente
              <select
                name="paciente_id"
                value={editForm.paciente_id}
                onChange={handleEditChange}
                required
              >
                <option value="">Seleccione un paciente</option>

                {pacientes.map((paciente) => (
                  <option
                    key={paciente.paciente_id}
                    value={paciente.paciente_id}
                  >
                    {paciente.nombre} {paciente.apellido}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Consulta
              <select
                name="consulta_id"
                value={editForm.consulta_id}
                onChange={handleEditChange}
                required
              >
                <option value="">Seleccione una consulta</option>

                {consultas.map((consulta) => (
                  <option
                    key={consulta.consulta_id}
                    value={consulta.consulta_id}
                  >
                    {formatConsultaLabel(consulta)}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Número de factura
              <input
                type="text"
                name="numero_factura"
                value={editForm.numero_factura}
                onChange={handleEditChange}
                required
              />
            </label>

            <label>
              Fecha emisión
              <input
                type="date"
                name="fecha_emision"
                value={editForm.fecha_emision}
                onChange={handleEditChange}
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
                <option value="PENDIENTE">PENDIENTE</option>
                <option value="PAGADA">PAGADA</option>
                <option value="ANULADA">ANULADA</option>
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
        <h3>Servicios de la factura</h3>

        {!selectedFactura && (
          <p className="helper-text">
            Seleccione una factura con el botón Ver servicios para revisar su
            detalle.
          </p>
        )}

        {selectedFactura && (
          <>
            <div className="invoice-summary">
              <p>
                <strong>Factura:</strong> {selectedFactura.numero_factura}
              </p>

              <p>
                <strong>Estado:</strong>{" "}
                <span className={getStatusBadgeClass(selectedFactura.estado)}>
                  {selectedFactura.estado}
                </span>
              </p>

              <p>
                <strong>Paciente:</strong>{" "}
                {selectedFactura.paciente_nombre ||
                  getPacienteName(selectedFactura.paciente_id)}
              </p>

              <p>
                <strong>Consulta:</strong>{" "}
                {getConsultaLabel(selectedFactura.consulta_id)}
              </p>

              <p>
                <strong>Subtotal:</strong> ₡
                {getFacturaSubtotal(selectedFactura)}
              </p>

              <p>
                <strong>Impuesto 13%:</strong> ₡
                {getFacturaImpuesto(selectedFactura)}
              </p>

              <p>
                <strong>Total:</strong> ₡{getFacturaTotal(selectedFactura)}
              </p>
            </div>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Servicio</th>
                    <th>Cantidad</th>
                    <th>Precio unitario</th>
                    <th>Subtotal</th>
                    <th>Acciones</th>
                  </tr>
                </thead>

                <tbody>
                  {selectedFacturaDetails.map((detalle) => (
                    <tr key={detalle.detalle_factura_id}>
                      <td>{detalle.detalle_factura_id}</td>
                      <td>{detalle.descripcion}</td>
                      <td>{detalle.cantidad}</td>
                      <td>₡{detalle.precio_unitario}</td>
                      <td>₡{detalle.subtotal}</td>
                      <td>
                        {selectedFactura.estado === "ANULADA" ? (
                          <span className="helper-text">
                            No editable
                          </span>
                        ) : (
                          <button
                            type="button"
                            className="danger-button"
                            onClick={() =>
                              handleDeleteDetalle(detalle.detalle_factura_id)
                            }
                          >
                            Eliminar servicio
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}

                  {selectedFacturaDetails.length === 0 && (
                    <tr>
                      <td colSpan="6">
                        Esta factura no tiene servicios registrados.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </>
        )}
      </section>
    </section>
  );
}

export default Facturas;