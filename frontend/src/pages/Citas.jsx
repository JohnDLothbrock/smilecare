import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  paciente_id: "",
  doctor_id: "",
  fecha_hora_inicio: "",
  duracion_minutos: "30",
  estado: "PROGRAMADA",
  motivo: ""
};

function Citas() {
  const [citas, setCitas] = useState([]);
  const [pacientes, setPacientes] = useState([]);
  const [doctores, setDoctores] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadCitas() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/citas");

      setCitas(data);
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

  async function loadDoctores() {
    try {
      const data = await apiClient.get("/doctores");

      setDoctores(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadCitas();
    loadPacientes();
    loadDoctores();
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
      paciente_id: Number(form.paciente_id),
      doctor_id: Number(form.doctor_id),
      fecha_hora_inicio: form.fecha_hora_inicio,
      duracion_minutos: Number(form.duracion_minutos),
      estado: form.estado,
      motivo: form.motivo || null
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
        await apiClient.post("/citas", payload);
        setMessage("Cita creada correctamente.");
      } else {
        await apiClient.put(`/citas/${editingId}`, payload);
        setMessage("Cita actualizada correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadCitas();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(cita) {
    setEditingId(cita.cita_id);

    setForm({
      paciente_id: cita.paciente_id ?? "",
      doctor_id: cita.doctor_id ?? "",
      fecha_hora_inicio: cita.fecha_hora_inicio
        ? cita.fecha_hora_inicio.substring(0, 16)
        : "",
      duracion_minutos: cita.duracion_minutos ?? "30",
      estado: cita.estado ?? "PROGRAMADA",
      motivo: cita.motivo ?? ""
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(citaId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar esta cita?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/citas/${citaId}`);

      setMessage("Cita eliminada correctamente.");

      await loadCitas();
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
          <h2>Citas</h2>
          <p>Administración de citas entre pacientes y doctores.</p>
        </div>
      </div>

      <section className="card">
        <h3>{editingId === null ? "Crear cita" : "Editar cita"}</h3>

        <form className="form-grid" onSubmit={handleSubmit}>
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
            Doctor
            <select
              name="doctor_id"
              value={form.doctor_id}
              onChange={handleChange}
              required
            >
              <option value="">Seleccione un doctor</option>

              {doctores.map((doctor) => (
                <option
                  key={doctor.doctor_id}
                  value={doctor.doctor_id}
                >
                  {doctor.nombre} {doctor.apellido}
                </option>
              ))}
            </select>
          </label>

          <label>
            Fecha y hora
            <input
              type="datetime-local"
              name="fecha_hora_inicio"
              value={form.fecha_hora_inicio}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Duración en minutos
            <input
              type="number"
              name="duracion_minutos"
              value={form.duracion_minutos}
              onChange={handleChange}
              min="1"
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
              <option value="PROGRAMADA">PROGRAMADA</option>
              <option value="CONFIRMADA">CONFIRMADA</option>
              <option value="CANCELADA">CANCELADA</option>
              <option value="FINALIZADA">FINALIZADA</option>
            </select>
          </label>

          <label>
            Motivo
            <textarea
              name="motivo"
              value={form.motivo}
              onChange={handleChange}
              rows="3"
              placeholder="Motivo de la cita"
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
        <h3>Lista de citas</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Paciente</th>
                <th>Doctor</th>
                <th>Fecha y hora</th>
                <th>Duración</th>
                <th>Estado</th>
                <th>Motivo</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {citas.map((cita) => (
                <tr key={cita.cita_id}>
                  <td>{cita.cita_id}</td>
                  <td>
                    {cita.paciente_nombre ||
                      `${cita.paciente_id}`}
                  </td>
                  <td>
                    {cita.doctor_nombre ||
                      `${cita.doctor_id}`}
                  </td>
                  <td>
                    {cita.fecha_hora_inicio
                      ? cita.fecha_hora_inicio.substring(0, 16).replace("T", " ")
                      : ""}
                  </td>
                  <td>{cita.duracion_minutos} min</td>
                  <td>{cita.estado}</td>
                  <td>{cita.motivo}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(cita)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(cita.cita_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {citas.length === 0 && !loading && (
                <tr>
                  <td colSpan="8">No hay citas registradas.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default Citas;