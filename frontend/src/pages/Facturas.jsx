import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  paciente_id: "",
  consulta_id: "",
  numero_factura: "",
  fecha_emision: "",
  subtotal: "",
  impuesto: "0",
  estado: "PENDIENTE"
};

function Facturas() {
  const [facturas, setFacturas] = useState([]);
  const [pacientes, setPacientes] = useState([]);
  const [consultas, setConsultas] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
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

  useEffect(() => {
    loadFacturas();
    loadPacientes();
    loadConsultas();
  }, []);

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

      return;
    }

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function buildPayload() {
    return {
      paciente_id: Number(form.paciente_id),
      consulta_id: Number(form.consulta_id),
      numero_factura: form.numero_factura,
      fecha_emision: form.fecha_emision || null,
      subtotal: Number(form.subtotal),
      impuesto: Number(form.impuesto),
      estado: form.estado
    };
  }

  function getTotalPreview() {
    const subtotal = Number(form.subtotal || 0);
    const impuesto = Number(form.impuesto || 0);

    return subtotal + impuesto;
  }

  function generateFacturaNumber() {
    const currentYear = new Date().getFullYear();
    const randomNumber = Math.floor(Math.random() * 900000) + 100000;

    setForm((currentForm) => ({
      ...currentForm,
      numero_factura: `FAC-${currentYear}-${randomNumber}`
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
        await apiClient.post("/facturas", payload);
        setMessage("Factura creada correctamente.");
      } else {
        await apiClient.put(`/facturas/${editingId}`, payload);
        setMessage("Factura actualizada correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadFacturas();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(factura) {
    setEditingId(factura.factura_id);

    setForm({
      paciente_id: factura.paciente_id ?? "",
      consulta_id: factura.consulta_id ?? "",
      numero_factura: factura.numero_factura ?? "",
      fecha_emision: factura.fecha_emision
        ? factura.fecha_emision.substring(0, 10)
        : "",
      subtotal: factura.subtotal ?? "",
      impuesto: factura.impuesto ?? "0",
      estado: factura.estado ?? "PENDIENTE"
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(facturaId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar esta factura?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/facturas/${facturaId}`);

      setMessage("Factura eliminada correctamente.");

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

  function formatConsultaLabel(consulta) {
    const paciente = consulta.paciente_nombre || `Paciente ${consulta.paciente_id}`;
    const doctor = consulta.doctor_nombre || `Doctor ${consulta.doctor_id}`;

    return `Consulta ${consulta.consulta_id} - ${paciente} con ${doctor}`;
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Facturas</h2>
          <p>Administración de facturación asociada a pacientes y consultas.</p>
        </div>
      </div>

      <section className="card">
        <h3>{editingId === null ? "Crear factura" : "Editar factura"}</h3>

        <form className="form-grid" onSubmit={handleSubmit}>
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
                <option key={consulta.consulta_id} value={consulta.consulta_id}>
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
                <option key={paciente.paciente_id} value={paciente.paciente_id}>
                  {paciente.nombre} {paciente.apellido}
                </option>
              ))}
            </select>
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

          <label>
            Fecha emisión
            <input
              type="date"
              name="fecha_emision"
              value={form.fecha_emision}
              onChange={handleChange}
            />
          </label>

          <label>
            Subtotal
            <input
              type="number"
              name="subtotal"
              value={form.subtotal}
              onChange={handleChange}
              min="0"
              step="0.01"
              required
            />
          </label>

          <label>
            Impuesto
            <input
              type="number"
              name="impuesto"
              value={form.impuesto}
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
              <option value="PENDIENTE">PENDIENTE</option>
              <option value="PAGADA">PAGADA</option>
              <option value="ANULADA">ANULADA</option>
            </select>
          </label>

          <div className="total-preview">
            <strong>Total:</strong> ₡{getTotalPreview()}
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
        <h3>Lista de facturas</h3>

        {loading && <p>Cargando...</p>}

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
              {facturas.map((factura) => (
                <tr key={factura.factura_id}>
                  <td>{factura.factura_id}</td>
                  <td>{factura.numero_factura}</td>
                  <td>{factura.paciente_nombre || factura.paciente_id}</td>
                  <td>{factura.consulta_id}</td>
                  <td>
                    {factura.fecha_emision
                      ? factura.fecha_emision.substring(0, 10)
                      : ""}
                  </td>
                  <td>₡{factura.subtotal}</td>
                  <td>₡{factura.impuesto}</td>
                  <td>₡{factura.total}</td>
                  <td>{factura.estado}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(factura)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(factura.factura_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {facturas.length === 0 && !loading && (
                <tr>
                  <td colSpan="10">No hay facturas registradas.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default Facturas;