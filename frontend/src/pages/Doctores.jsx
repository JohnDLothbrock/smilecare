import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  usuario_id: "",
  especialidad_id: "",
  nombre: "",
  apellido: "",
  telefono: "",
  correo: ""
};

function Doctores() {
  const [doctores, setDoctores] = useState([]);
  const [especialidades, setEspecialidades] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadDoctores() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/doctores");

      setDoctores(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadEspecialidades() {
    try {
      const data = await apiClient.get("/especialidades");

      setEspecialidades(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadDoctores();
    loadEspecialidades();
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
      usuario_id: form.usuario_id === "" ? null : Number(form.usuario_id),
      especialidad_id: Number(form.especialidad_id),
      nombre: form.nombre,
      apellido: form.apellido,
      telefono: form.telefono || null,
      correo: form.correo || null
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
        await apiClient.post("/doctores", payload);
        setMessage("Doctor creado correctamente.");
      } else {
        await apiClient.put(`/doctores/${editingId}`, payload);
        setMessage("Doctor actualizado correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadDoctores();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(doctor) {
    setEditingId(doctor.doctor_id);

    setForm({
      usuario_id: doctor.usuario_id ?? "",
      especialidad_id: doctor.especialidad_id ?? "",
      nombre: doctor.nombre ?? "",
      apellido: doctor.apellido ?? "",
      telefono: doctor.telefono ?? "",
      correo: doctor.correo ?? ""
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(doctorId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este doctor?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/doctores/${doctorId}`);

      setMessage("Doctor eliminado correctamente.");

      await loadDoctores();
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
          <h2>Doctores</h2>
          <p>Administración de doctores y especialidades médicas.</p>
        </div>
      </div>

      <section className="card">
        <h3>{editingId === null ? "Crear doctor" : "Editar doctor"}</h3>

        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Usuario ID
            <input
              type="number"
              name="usuario_id"
              value={form.usuario_id}
              onChange={handleChange}
              placeholder="Opcional"
            />
          </label>

          <label>
            Especialidad
            <select
              name="especialidad_id"
              value={form.especialidad_id}
              onChange={handleChange}
              required
            >
              <option value="">Seleccione una especialidad</option>

              {especialidades.map((especialidad) => (
                <option
                  key={especialidad.especialidad_id}
                  value={especialidad.especialidad_id}
                >
                  {especialidad.nombre}
                </option>
              ))}
            </select>
          </label>

          <label>
            Nombre
            <input
              type="text"
              name="nombre"
              value={form.nombre}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Apellido
            <input
              type="text"
              name="apellido"
              value={form.apellido}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Teléfono
            <input
              type="text"
              name="telefono"
              value={form.telefono}
              onChange={handleChange}
              placeholder="8888-9999"
            />
          </label>

          <label>
            Correo
            <input
              type="email"
              name="correo"
              value={form.correo}
              onChange={handleChange}
              placeholder="doctor@ejemplo.com"
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
        <h3>Lista de doctores</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre completo</th>
                <th>Especialidad</th>
                <th>Teléfono</th>
                <th>Correo</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {doctores.map((doctor) => (
                <tr key={doctor.doctor_id}>
                  <td>{doctor.doctor_id}</td>
                  <td>
                    {doctor.nombre} {doctor.apellido}
                  </td>
                  <td>
                    {doctor.especialidad_nombre ||
                      doctor.nombre_especialidad ||
                      doctor.especialidad_id}
                  </td>
                  <td>{doctor.telefono}</td>
                  <td>{doctor.correo}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(doctor)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(doctor.doctor_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {doctores.length === 0 && !loading && (
                <tr>
                  <td colSpan="6">No hay doctores registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default Doctores;