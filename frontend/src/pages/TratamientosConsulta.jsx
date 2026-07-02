import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  consulta_id: "",
  tratamiento_id: "",
  cantidad: "1",
  precio_unitario: ""
};

function TratamientosConsulta() {
  const [tratamientosConsulta, setTratamientosConsulta] = useState([]);
  const [consultas, setConsultas] = useState([]);
  const [tratamientos, setTratamientos] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadTratamientosConsulta() {
    try {
      setLoading(true);
      setError("");

      const data = await apiClient.get("/tratamientos-consulta");

      setTratamientosConsulta(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
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

  async function loadTratamientos() {
    try {
      const data = await apiClient.get("/tratamientos");

      setTratamientos(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadTratamientosConsulta();
    loadConsultas();
    loadTratamientos();
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));

    if (name === "tratamiento_id") {
      const selectedTratamiento = tratamientos.find(
        (tratamiento) => String(tratamiento.tratamiento_id) === value
      );

      if (selectedTratamiento) {
        setForm((currentForm) => ({
          ...currentForm,
          tratamiento_id: value,
          precio_unitario: selectedTratamiento.costo_base ?? ""
        }));
      }
    }
  }

  function buildPayload() {
    return {
      consulta_id: Number(form.consulta_id),
      tratamiento_id: Number(form.tratamiento_id),
      cantidad: Number(form.cantidad),
      precio_unitario: Number(form.precio_unitario)
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
        await apiClient.post("/tratamientos-consulta", payload);
        setMessage("Tratamiento agregado a la consulta correctamente.");
      } else {
        await apiClient.put(`/tratamientos-consulta/${editingId}`, payload);
        setMessage("Tratamiento de consulta actualizado correctamente.");
      }

      setForm(initialForm);
      setEditingId(null);

      await loadTratamientosConsulta();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(item) {
    setEditingId(item.tratamiento_consulta_id);

    setForm({
      consulta_id: item.consulta_id ?? "",
      tratamiento_id: item.tratamiento_id ?? "",
      cantidad: item.cantidad ?? "1",
      precio_unitario: item.precio_unitario ?? ""
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(tratamientoConsultaId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este tratamiento de la consulta?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(
        `/tratamientos-consulta/${tratamientoConsultaId}`
      );

      setMessage("Tratamiento eliminado de la consulta correctamente.");

      await loadTratamientosConsulta();
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
          <h2>Tratamientos por Consulta</h2>
          <p>Asignación de tratamientos realizados durante una consulta.</p>
        </div>
      </div>

      <section className="card">
        <h3>
          {editingId === null
            ? "Agregar tratamiento a consulta"
            : "Editar tratamiento de consulta"}
        </h3>

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
            Tratamiento
            <select
              name="tratamiento_id"
              value={form.tratamiento_id}
              onChange={handleChange}
              required
            >
              <option value="">Seleccione un tratamiento</option>

              {tratamientos.map((tratamiento) => (
                <option
                  key={tratamiento.tratamiento_id}
                  value={tratamiento.tratamiento_id}
                >
                  {tratamiento.nombre} - ₡{tratamiento.costo_base}
                </option>
              ))}
            </select>
          </label>

          <label>
            Cantidad
            <input
              type="number"
              name="cantidad"
              value={form.cantidad}
              onChange={handleChange}
              min="1"
              step="1"
              required
            />
          </label>

          <label>
            Precio unitario
            <input
              type="number"
              name="precio_unitario"
              value={form.precio_unitario}
              onChange={handleChange}
              min="0"
              step="0.01"
              required
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
        <h3>Tratamientos asignados</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Consulta</th>
                <th>Tratamiento</th>
                <th>Cantidad</th>
                <th>Precio unitario</th>
                <th>Subtotal</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {tratamientosConsulta.map((item) => (
                <tr key={item.tratamiento_consulta_id}>
                  <td>{item.tratamiento_consulta_id}</td>
                  <td>{item.consulta_id}</td>
                  <td>
                    {item.tratamiento_nombre ||
                      item.nombre_tratamiento ||
                      item.tratamiento_id}
                  </td>
                  <td>{item.cantidad}</td>
                  <td>₡{item.precio_unitario}</td>
                  <td>₡{item.subtotal}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEdit(item)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() =>
                        handleDelete(item.tratamiento_consulta_id)
                      }
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {tratamientosConsulta.length === 0 && !loading && (
                <tr>
                  <td colSpan="7">
                    No hay tratamientos asignados a consultas.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default TratamientosConsulta;