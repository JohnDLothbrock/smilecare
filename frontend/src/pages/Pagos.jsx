import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  factura_id: "",
  metodo_pago_id: "",
  monto: "",
  fecha_pago: "",
  numero_referencia: "",
  estado: "APLICADO"
};

function Pagos() {
  const [pagos, setPagos] = useState([]);
  const [facturas, setFacturas] = useState([]);
  const [metodosPago, setMetodosPago] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
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

  useEffect(() => {
    loadPagos();
    loadFacturas();
    loadMetodosPago();
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;

    if (name === "factura_id") {
      const selectedFactura = facturas.find(
        (factura) => String(factura.factura_id) === value
      );

      setForm((currentForm) => ({
        ...currentForm,
        factura_id: value,
        monto: selectedFactura?.total ?? currentForm.monto
      }));

      return;
    }

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function buildPayload() {
    return {
      factura_id: Number(form.factura_id),
      metodo_pago_id: Number(form.metodo_pago_id),
      monto: Number(form.monto),
      fecha_pago: form.fecha_pago || null,
      numero_referencia: form.numero_referencia || null,
      estado: form.estado
    };
  }

  function generateReference() {
    const randomNumber = Math.floor(Math.random() * 900000) + 100000;

    setForm((currentForm) => ({
      ...currentForm,
      numero_referencia: `REF-${randomNumber}`
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const payload = buildPayload();

      if (editingId === null) {
        await apiClient.post("/pagos", payload);
        setMessage("Pago registrado correctamente.");
      } else {
        await apiClient.put(`/pagos/${editingId}`, payload);
        setMessage("Pago actualizado correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadPagos();
      await loadFacturas();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(pago) {
    setEditingId(pago.pago_id);

    setForm({
      factura_id: pago.factura_id ?? "",
      metodo_pago_id: pago.metodo_pago_id ?? "",
      monto: pago.monto ?? "",
      fecha_pago: pago.fecha_pago ? pago.fecha_pago.substring(0, 10) : "",
      numero_referencia: pago.numero_referencia ?? "",
      estado: pago.estado ?? "APLICADO"
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(pagoId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este pago?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/pagos/${pagoId}`);

      setMessage("Pago eliminado correctamente.");

      await loadPagos();
      await loadFacturas();
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

  function formatFacturaLabel(factura) {
    const paciente = factura.paciente_nombre || `Paciente ${factura.paciente_id}`;

    return `${factura.numero_factura} - ${paciente} - ₡${factura.total}`;
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Pagos</h2>
          <p>Registro de pagos realizados sobre facturas.</p>
        </div>
      </div>

      <section className="card">
        <h3>{editingId === null ? "Registrar pago" : "Editar pago"}</h3>

        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Factura
            <select
              name="factura_id"
              value={form.factura_id}
              onChange={handleChange}
              required
            >
              <option value="">Seleccione una factura</option>

              {facturas.map((factura) => (
                <option key={factura.factura_id} value={factura.factura_id}>
                  {formatFacturaLabel(factura)}
                </option>
              ))}
            </select>
          </label>

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
                  {metodo.nombre}
                </option>
              ))}
            </select>
          </label>

          <label>
            Monto
            <input
              type="number"
              name="monto"
              value={form.monto}
              onChange={handleChange}
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
              value={form.fecha_pago}
              onChange={handleChange}
            />
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
              />

              <button type="button" onClick={generateReference}>
                Generar
              </button>
            </div>
          </label>

          <label>
            Estado
            <select
              name="estado"
              value={form.estado}
              onChange={handleChange}
              required
            >
              <option value="APLICADO">APLICADO</option>
              <option value="PENDIENTE">PENDIENTE</option>
              <option value="ANULADO">ANULADO</option>
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

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
      </section>

      <section className="card">
        <h3>Lista de pagos</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Factura</th>
                <th>Método</th>
                <th>Monto</th>
                <th>Fecha</th>
                <th>Referencia</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {pagos.map((pago) => (
                <tr key={pago.pago_id}>
                  <td>{pago.pago_id}</td>
                  <td>{pago.numero_factura || pago.factura_id}</td>
                  <td>
                    {pago.metodo_pago_nombre ||
                      pago.nombre_metodo_pago ||
                      pago.metodo_pago_id}
                  </td>
                  <td>₡{pago.monto}</td>
                  <td>
                    {pago.fecha_pago
                      ? pago.fecha_pago.substring(0, 10)
                      : ""}
                  </td>
                  <td>{pago.numero_referencia}</td>
                  <td>{pago.estado}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(pago)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(pago.pago_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {pagos.length === 0 && !loading && (
                <tr>
                  <td colSpan="8">No hay pagos registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default Pagos;