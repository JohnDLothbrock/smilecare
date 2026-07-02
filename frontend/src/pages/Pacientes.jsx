import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  usuario_id: "",
  nombre: "",
  apellido: "",
  telefono: "",
  correo: "",
  direccion: "",
  fecha_nacimiento: ""
};

function Pacientes() {
  const [pacientes, setPacientes] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadPacientes() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/pacientes");

      setPacientes(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadPacientes();
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
      nombre: form.nombre,
      apellido: form.apellido,
      telefono: form.telefono || null,
      correo: form.correo || null,
      direccion: form.direccion || null,
      fecha_nacimiento: form.fecha_nacimiento || null
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
        await apiClient.post("/pacientes", payload);
        setMessage("Paciente creado correctamente.");
      } else {
        await apiClient.put(`/pacientes/${editingId}`, payload);
        setMessage("Paciente actualizado correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadPacientes();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(paciente) {
    setEditingId(paciente.paciente_id);

    setForm({
      usuario_id: paciente.usuario_id ?? "",
      nombre: paciente.nombre ?? "",
      apellido: paciente.apellido ?? "",
      telefono: paciente.telefono ?? "",
      correo: paciente.correo ?? "",
      direccion: paciente.direccion ?? "",
      fecha_nacimiento: paciente.fecha_nacimiento
        ? paciente.fecha_nacimiento.substring(0, 10)
        : ""
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(pacienteId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este paciente?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/pacientes/${pacienteId}`);

      setMessage("Paciente eliminado correctamente.");

      await loadPacientes();
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
          <h2>Pacientes</h2>
          <p>Administración de pacientes registrados en SmileCare.</p>
        </div>
      </div>

      <section className="card">
        <h3>{editingId === null ? "Crear paciente" : "Editar paciente"}</h3>

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
              placeholder="correo@ejemplo.com"
            />
          </label>

          <label>
            Dirección
            <input
              type="text"
              name="direccion"
              value={form.direccion}
              onChange={handleChange}
            />
          </label>

          <label>
            Fecha nacimiento
            <input
              type="date"
              name="fecha_nacimiento"
              value={form.fecha_nacimiento}
              onChange={handleChange}
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
        <h3>Lista de pacientes</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre completo</th>
                <th>Teléfono</th>
                <th>Correo</th>
                <th>Fecha nacimiento</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {pacientes.map((paciente) => (
                <tr key={paciente.paciente_id}>
                  <td>{paciente.paciente_id}</td>
                  <td>
                    {paciente.nombre} {paciente.apellido}
                  </td>
                  <td>{paciente.telefono}</td>
                  <td>{paciente.correo}</td>
                  <td>
                    {paciente.fecha_nacimiento
                      ? paciente.fecha_nacimiento.substring(0, 10)
                      : ""}
                  </td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(paciente)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => handleDelete(paciente.paciente_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {pacientes.length === 0 && !loading && (
                <tr>
                  <td colSpan="6">No hay pacientes registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default Pacientes;