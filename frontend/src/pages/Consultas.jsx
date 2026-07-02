import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  cita_id: "",
  diagnostico: "",
  observaciones: "",
  fecha_atencion: ""
};

function Consultas() {
  const [consultas, setConsultas] = useState([]);
  const [citas, setCitas] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadConsultas() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/consultas");

      setConsultas(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadCitas() {
    try {
      const data = await apiClient.get("/citas");

      setCitas(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadConsultas();
    loadCitas();
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
      cita_id: Number(form.cita_id),
      diagnostico: form.diagnostico,
      observaciones: form.observaciones || null,
      fecha_atencion: form.fecha_atencion || null
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
        await apiClient.post("/consultas", payload);
        setMessage("Consulta creada correctamente.");
      } else {
        await apiClient.put(`/consultas/${editingId}`, payload);
        setMessage("Consulta actualizada correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadConsultas();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(consulta) {
    setEditingId(consulta.consulta_id);

    setForm({
      cita_id: consulta.cita_id ?? "",
      diagnostico: consulta.diagnostico ?? "",
      observaciones: consulta.observaciones ?? "",
      fecha_atencion: consulta.fecha_atencion
        ? consulta.fecha_atencion.substring(0, 16)
        : ""
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(consultaId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar esta consulta?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/consultas/${consultaId}`);

      setMessage("Consulta eliminada correctamente.");

      await loadConsultas();
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

  function formatCitaLabel(cita) {
    const paciente = cita.paciente_nombre || `Paciente ${cita.paciente_id}`;
    const doctor = cita.doctor_nombre || `Doctor ${cita.doctor_id}`;
    const fecha = cita.fecha_hora_inicio
      ? cita.fecha_hora_inicio.substring(0, 16).replace("T", " ")
      : "Sin fecha";

    return `${fecha} - ${paciente} con ${doctor}`;
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Consultas</h2>
          <p>Registro de atención médica asociada a una cita.</p>
        </div>
      </div>

      <section className="card">
        <h3>{editingId === null ? "Crear consulta" : "Editar consulta"}</h3>

        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Cita
            <select
              name="cita_id"
              value={form.cita_id}
              onChange={handleChange}
              required
            >
              <option value="">Seleccione una cita</option>

              {citas.map((cita) => (
                <option key={cita.cita_id} value={cita.cita_id}>
                  {formatCitaLabel(cita)}
                </option>
              ))}
            </select>
          </label>

          <label>
            Fecha atención
            <input
              type="datetime-local"
              name="fecha_atencion"
              value={form.fecha_atencion}
              onChange={handleChange}
            />
          </label>

          <label>
            Diagnóstico
            <textarea
              name="diagnostico"
              value={form.diagnostico}
              onChange={handleChange}
              rows="4"
              required
            />
          </label>

          <label>
            Observaciones
            <textarea
              name="observaciones"
              value={form.observaciones}
              onChange={handleChange}
              rows="4"
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
        <h3>Lista de consultas</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Cita</th>
                <th>Paciente</th>
                <th>Doctor</th>
                <th>Diagnóstico</th>
                <th>Fecha atención</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {consultas.map((consulta) => (
                <tr key={consulta.consulta_id}>
                  <td>{consulta.consulta_id}</td>
                  <td>{consulta.cita_id}</td>
                  <td>
                    {consulta.paciente_nombre || consulta.paciente_id || ""}
                  </td>
                  <td>
                    {consulta.doctor_nombre || consulta.doctor_id || ""}
                  </td>
                  <td>{consulta.diagnostico}</td>
                  <td>
                    {consulta.fecha_atencion
                      ? consulta.fecha_atencion.substring(0, 16).replace("T", " ")
                      : ""}
                  </td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(consulta)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(consulta.consulta_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {consultas.length === 0 && !loading && (
                <tr>
                  <td colSpan="7">No hay consultas registradas.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default Consultas;