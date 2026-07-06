import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const TAX_RATE = 0.13;

function getTodayDate() {
  return new Date().toISOString().substring(0, 10);
}

function getInitialForm() {
  return {
    consulta_id: "",
    paciente_id: "",
    numero_factura: "",
    fecha_operacion: getTodayDate(),
    metodo_pago_id: "",
    numero_referencia: ""
  };
}

const initialLineForm = {
  tratamiento_consulta_id: "",
  descripcion: "",
  cantidad: "1",
  precio_unitario: ""
};

function Caja() {
  const [consultas, setConsultas] = useState([]);
  const [pacientes, setPacientes] = useState([]);
  const [tratamientosConsulta, setTratamientosConsulta] = useState([]);
  const [metodosPago, setMetodosPago] = useState([]);
  const [facturas, setFacturas] = useState([]);
  const [pagos, setPagos] = useState([]);

  const [form, setForm] = useState(getInitialForm());
  const [lineForm, setLineForm] = useState(initialLineForm);
  const [lineItems, setLineItems] = useState([]);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadConsultas() {
    try {
      const data = await apiClient.get("/consultas");
      setConsultas(data);
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

  async function loadTratamientosConsulta() {
    try {
      const data = await apiClient.get("/tratamientos-consulta");
      setTratamientosConsulta(data);
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

  async function loadFacturas() {
    try {
      const data = await apiClient.get("/facturas");
      setFacturas(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadPagos() {
    try {
      const data = await apiClient.get("/pagos");
      setPagos(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadPageData() {
    setLoading(true);
    setError("");

    try {
      await Promise.all([
        loadConsultas(),
        loadPacientes(),
        loadTratamientosConsulta(),
        loadMetodosPago(),
        loadFacturas(),
        loadPagos()
      ]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadPageData();
  }, []);

  function roundMoney(value) {
    return Math.round((Number(value) + Number.EPSILON) * 100) / 100;
  }

  function handleChange(event) {
    const { name, value } = event.target;

    if (name === "consulta_id") {
      const selectedConsulta = consultas.find(
        (consulta) => String(consulta.consulta_id) === value
      );

      setForm((currentForm) => ({
        ...currentForm,
        consulta_id: value,
        paciente_id: selectedConsulta?.paciente_id ?? currentForm.paciente_id
      }));

      setLineItems([]);
      setLineForm(initialLineForm);
      setMessage("");
      setError("");

      return;
    }

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function handleLineChange(event) {
    const { name, value } = event.target;

    if (name === "tratamiento_consulta_id") {
      const selectedTreatment = tratamientosConsulta.find(
        (item) => String(item.tratamiento_consulta_id) === value
      );

      const treatmentName =
        selectedTreatment?.tratamiento_nombre ||
        selectedTreatment?.nombre_tratamiento ||
        selectedTreatment?.nombre ||
        `Tratamiento ${selectedTreatment?.tratamiento_id || ""}`;

      const unitPrice =
        selectedTreatment?.precio_unitario ??
        selectedTreatment?.precio ??
        selectedTreatment?.precio_final ??
        selectedTreatment?.costo ??
        selectedTreatment?.costo_base ??
        "";

      setLineForm((currentForm) => ({
        ...currentForm,
        tratamiento_consulta_id: value,
        descripcion: treatmentName,
        precio_unitario: unitPrice
      }));

      return;
    }

    setLineForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function getAvailableTratamientosConsulta() {
    if (form.consulta_id === "") {
      return tratamientosConsulta;
    }

    return tratamientosConsulta.filter(
      (item) => String(item.consulta_id) === String(form.consulta_id)
    );
  }

  function getLineSubtotal(line) {
    const cantidad = Number(line.cantidad || 0);
    const precioUnitario = Number(line.precio_unitario || 0);

    return roundMoney(cantidad * precioUnitario);
  }

  function getSubtotal() {
    return roundMoney(
      lineItems.reduce((total, line) => total + getLineSubtotal(line), 0)
    );
  }

  function getImpuesto() {
    return roundMoney(getSubtotal() * TAX_RATE);
  }

  function getTotal() {
    return roundMoney(getSubtotal() + getImpuesto());
  }

  function generateFacturaNumber() {
    const currentYear = new Date().getFullYear();
    const randomNumber = Math.floor(Math.random() * 900000) + 100000;

    setForm((currentForm) => ({
      ...currentForm,
      numero_factura: `FAC-${currentYear}-${randomNumber}`
    }));
  }

  function generateReference() {
    const randomNumber = Math.floor(Math.random() * 900000) + 100000;

    setForm((currentForm) => ({
      ...currentForm,
      numero_referencia: `REF-${randomNumber}`
    }));
  }

  function generateCheckoutNumbers() {
    const currentYear = new Date().getFullYear();
    const facturaNumber = Math.floor(Math.random() * 900000) + 100000;
    const referenceNumber = Math.floor(Math.random() * 900000) + 100000;

    setForm((currentForm) => ({
      ...currentForm,
      numero_factura: `FAC-${currentYear}-${facturaNumber}`,
      numero_referencia: `REF-${referenceNumber}`
    }));
  }

  function addLineItem() {
    setMessage("");
    setError("");

    if (lineForm.descripcion.trim() === "") {
      setError("Debe indicar una descripción para el servicio.");
      return;
    }

    if (Number(lineForm.cantidad) <= 0) {
      setError("La cantidad debe ser mayor a 0.");
      return;
    }

    if (Number(lineForm.precio_unitario) < 0) {
      setError("El precio unitario no puede ser negativo.");
      return;
    }

    const newLine = {
      local_id: Date.now(),
      tratamiento_consulta_id: lineForm.tratamiento_consulta_id || null,
      descripcion: lineForm.descripcion,
      cantidad: Number(lineForm.cantidad),
      precio_unitario: Number(lineForm.precio_unitario)
    };

    setLineItems((currentLines) => [...currentLines, newLine]);
    setLineForm(initialLineForm);
  }

  function removeLineItem(localId) {
    setLineItems((currentLines) =>
      currentLines.filter((line) => line.local_id !== localId)
    );
  }

  function buildFacturaPayload() {
    return {
      paciente_id: Number(form.paciente_id),
      consulta_id: Number(form.consulta_id),
      numero_factura: form.numero_factura,
      fecha_emision: form.fecha_operacion || null,
      subtotal: getSubtotal(),
      impuesto: getImpuesto(),
      estado: "PAGADA"
    };
  }

  function buildDetallePayload(facturaId, line) {
    return {
      factura_id: Number(facturaId),
      tratamiento_consulta_id:
        line.tratamiento_consulta_id === null ||
        line.tratamiento_consulta_id === ""
          ? null
          : Number(line.tratamiento_consulta_id),
      descripcion: line.descripcion,
      cantidad: Number(line.cantidad),
      precio_unitario: Number(line.precio_unitario),
      subtotal: getLineSubtotal(line)
    };
  }

  function buildPagoPayload(facturaId) {
    return {
      factura_id: Number(facturaId),
      metodo_pago_id: Number(form.metodo_pago_id),
      monto: getTotal(),
      fecha_pago: form.fecha_operacion || null,
      numero_referencia: form.numero_referencia,
      estado: "APLICADO"
    };
  }

  function buildComprobantePayload(pagoId) {
    return {
      pago_id: Number(pagoId),
      numero_comprobante: form.numero_factura,
      tipo_comprobante: "FACTURA",
      fecha_emision: form.fecha_operacion || null,
      detalle: `Factura ${form.numero_factura} pagada con referencia ${form.numero_referencia}`
    };
  }

  async function resolveCreatedFacturaId(createdFactura, numeroFactura) {
    if (createdFactura?.factura_id) {
      return createdFactura.factura_id;
    }

    if (createdFactura?.id) {
      return createdFactura.id;
    }

    const allFacturas = await apiClient.get("/facturas");

    const foundFactura = allFacturas.find(
      (factura) => factura.numero_factura === numeroFactura
    );

    if (foundFactura?.factura_id) {
      return foundFactura.factura_id;
    }

    throw new Error(
      "La factura fue creada, pero no se pudo obtener el ID para continuar."
    );
  }

  async function resolveCreatedPagoId(createdPago, numeroReferencia) {
    if (createdPago?.pago_id) {
      return createdPago.pago_id;
    }

    if (createdPago?.id) {
      return createdPago.id;
    }

    const allPagos = await apiClient.get("/pagos");

    const foundPago = allPagos.find(
      (pago) => pago.numero_referencia === numeroReferencia
    );

    if (foundPago?.pago_id) {
      return foundPago.pago_id;
    }

    throw new Error(
      "El pago fue creado, pero no se pudo obtener el ID para crear el comprobante."
    );
  }

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setMessage("");
      setError("");

      if (lineItems.length === 0) {
        setError("Debe agregar al menos un servicio antes de guardar.");
        return;
      }

      if (form.numero_factura.trim() === "") {
        setError("Debe generar o escribir un número de factura.");
        return;
      }

      if (form.numero_referencia.trim() === "") {
        setError("Debe generar o escribir un número de referencia de pago.");
        return;
      }

      const facturaPayload = buildFacturaPayload();

      const createdFactura = await apiClient.post("/facturas", facturaPayload);

      const facturaId = await resolveCreatedFacturaId(
        createdFactura,
        facturaPayload.numero_factura
      );

      for (const line of lineItems) {
        const detallePayload = buildDetallePayload(facturaId, line);

        await apiClient.post("/detalle-factura", detallePayload);
      }

      const pagoPayload = buildPagoPayload(facturaId);

      const createdPago = await apiClient.post("/pagos", pagoPayload);

      const pagoId = await resolveCreatedPagoId(
        createdPago,
        pagoPayload.numero_referencia
      );

      const comprobantePayload = buildComprobantePayload(pagoId);

      await apiClient.post("/comprobantes", comprobantePayload);

      setForm(getInitialForm());
      setLineForm(initialLineForm);
      setLineItems([]);

      setMessage(
        "Operación guardada correctamente. Se creó la factura, sus detalles, el pago y el comprobante."
      );

      await loadPageData();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function formatConsultaLabel(consulta) {
    const paciente =
      consulta.paciente_nombre || `Paciente ${consulta.paciente_id}`;
    const doctor = consulta.doctor_nombre || `Doctor ${consulta.doctor_id}`;

    return `Consulta ${consulta.consulta_id} - ${paciente} con ${doctor}`;
  }

  function formatTratamientoConsultaLabel(item) {
    const treatmentName =
      item.tratamiento_nombre ||
      item.nombre_tratamiento ||
      item.nombre ||
      `Tratamiento ${item.tratamiento_id}`;

    return `Consulta ${item.consulta_id} - ${treatmentName}`;
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

  function getMetodoPagoName(metodoPagoId) {
    const metodo = metodosPago.find(
      (item) => String(item.metodo_pago_id) === String(metodoPagoId)
    );

    if (!metodo) {
      return metodoPagoId || "";
    }

    return metodo.nombre || metodo.nombre_metodo || metodo.descripcion;
  }

  function getPagoByFacturaId(facturaId) {
    return pagos.find(
      (pago) => String(pago.factura_id) === String(facturaId)
    );
  }

  const recentFacturas = [...facturas]
    .sort((a, b) => Number(b.factura_id) - Number(a.factura_id))
    .slice(0, 5);

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Caja</h2>
          <p>
            Cobro de consultas en un solo lugar: factura, servicios, pago y
            comprobante.
          </p>
        </div>
      </div>

      <section className="card">
        <form onSubmit={handleSubmit}>
          <h3>Cobrar consulta</h3>

          <p className="helper-text">
            Seleccione la consulta, agregue los servicios realizados y registre
            el pago, buen dia.
          </p>

          <div className="form-actions">
            <button type="button" onClick={generateCheckoutNumbers}>
              Generar factura y referencia
            </button>
          </div>

          <h4>Datos de la consulta</h4>

          <div className="form-grid">
            <label>
              Consulta
              <select
                name="consulta_id"
                value={form.consulta_id}
                onChange={handleChange}
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
              Paciente
              <select
                name="paciente_id"
                value={form.paciente_id}
                onChange={handleChange}
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
              Fecha
              <input
                type="date"
                name="fecha_operacion"
                value={form.fecha_operacion}
                onChange={handleChange}
                required
              />
            </label>

            <label>
              Número de factura
              <div className="inline-input">
                <input
                  type="text"
                  name="numero_factura"
                  value={form.numero_factura}
                  onChange={handleChange}
                  placeholder="FAC-2026-000001"
                  required
                />

                <button type="button" onClick={generateFacturaNumber}>
                  Generar
                </button>
              </div>
            </label>
          </div>

          <hr />

          <h4>Servicios facturados</h4>

          <div className="form-grid">
            <label>
              Tratamiento aplicado
              <select
                name="tratamiento_consulta_id"
                value={lineForm.tratamiento_consulta_id}
                onChange={handleLineChange}
              >
                <option value="">Servicio manual</option>

                {getAvailableTratamientosConsulta().map((item) => (
                  <option
                    key={item.tratamiento_consulta_id}
                    value={item.tratamiento_consulta_id}
                  >
                    {formatTratamientoConsultaLabel(item)}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Descripción
              <input
                type="text"
                name="descripcion"
                value={lineForm.descripcion}
                onChange={handleLineChange}
                placeholder="Ejemplo: Limpieza dental"
              />
            </label>

            <label>
              Cantidad
              <input
                type="number"
                name="cantidad"
                value={lineForm.cantidad}
                onChange={handleLineChange}
                min="1"
                step="1"
              />
            </label>

            <label>
              Precio unitario
              <input
                type="number"
                name="precio_unitario"
                value={lineForm.precio_unitario}
                onChange={handleLineChange}
                min="0"
                step="0.01"
              />
            </label>

            <div className="total-preview">
              <strong>Subtotal línea:</strong> ₡{getLineSubtotal(lineForm)}
            </div>

            <div className="form-actions">
              <button type="button" onClick={addLineItem}>
                Agregar servicio
              </button>
            </div>
          </div>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Servicio</th>
                  <th>Cantidad</th>
                  <th>Precio unitario</th>
                  <th>Subtotal</th>
                  <th>Acciones</th>
                </tr>
              </thead>

              <tbody>
                {lineItems.map((line) => (
                  <tr key={line.local_id}>
                    <td>{line.descripcion}</td>
                    <td>{line.cantidad}</td>
                    <td>₡{line.precio_unitario}</td>
                    <td>₡{getLineSubtotal(line)}</td>
                    <td>
                      <button
                        type="button"
                        className="danger-button"
                        onClick={() => removeLineItem(line.local_id)}
                      >
                        Quitar
                      </button>
                    </td>
                  </tr>
                ))}

                {lineItems.length === 0 && (
                  <tr>
                    <td colSpan="5">
                      Aún no se han agregado servicios a esta operación.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          <hr />

          <h4>Pago</h4>

          <div className="form-grid">
            <label>
              Método de pago
              <select
                name="metodo_pago_id"
                value={form.metodo_pago_id}
                onChange={handleChange}
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
              Número de referencia
              <div className="inline-input">
                <input
                  type="text"
                  name="numero_referencia"
                  value={form.numero_referencia}
                  onChange={handleChange}
                  placeholder="REF-123456"
                  required
                />

                <button type="button" onClick={generateReference}>
                  Generar
                </button>
              </div>
            </label>
          </div>

          <div className="checkout-summary">
            <p>
              <strong>Paciente:</strong>{" "}
              {form.paciente_id
                ? getPacienteName(form.paciente_id)
                : "Pendiente"}
            </p>

            <p>
              <strong>Factura / Comprobante:</strong>{" "}
              {form.numero_factura || "Pendiente"}
            </p>

            <p>
              <strong>Referencia de pago:</strong>{" "}
              {form.numero_referencia || "Pendiente"}
            </p>

            <p>
              <strong>Subtotal:</strong> ₡{getSubtotal()}
            </p>

            <p>
              <strong>Impuesto 13%:</strong> ₡{getImpuesto()}
            </p>

            <p>
              <strong>Total a pagar:</strong> ₡{getTotal()}
            </p>
          </div>

          <div className="form-actions">
            <button type="submit" disabled={loading}>
              Guardar operación
            </button>
          </div>
        </form>

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
      </section>

      <section className="card">
        <h3>Últimas operaciones de caja</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Factura</th>
                <th>Paciente</th>
                <th>Fecha</th>
                <th>Total</th>
                <th>Método de pago</th>
                <th>Referencia</th>
                <th>Estado</th>
              </tr>
            </thead>

            <tbody>
              {recentFacturas.map((factura) => {
                const pago = getPagoByFacturaId(factura.factura_id);

                return (
                  <tr key={factura.factura_id}>
                    <td>{factura.numero_factura}</td>
                    <td>
                      {factura.paciente_nombre ||
                        getPacienteName(factura.paciente_id)}
                    </td>
                    <td>
                      {factura.fecha_emision
                        ? factura.fecha_emision.substring(0, 10)
                        : ""}
                    </td>
                    <td>₡{factura.total}</td>
                    <td>
                      {pago
                        ? pago.metodo_pago_nombre ||
                          pago.nombre_metodo_pago ||
                          getMetodoPagoName(pago.metodo_pago_id)
                        : "Sin pago"}
                    </td>
                    <td>{pago?.numero_referencia || "Sin referencia"}</td>
                    <td>{factura.estado}</td>
                  </tr>
                );
              })}

              {recentFacturas.length === 0 && !loading && (
                <tr>
                  <td colSpan="7">No hay operaciones registradas.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default Caja;