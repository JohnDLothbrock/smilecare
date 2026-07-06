import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const DAYS = [
  { value: "LUNES", label: "LUNES", order: 1 },
  { value: "MARTES", label: "MARTES", order: 2 },
  { value: "MIERCOLES", label: "MIÉRCOLES", order: 3 },
  { value: "JUEVES", label: "JUEVES", order: 4 },
  { value: "VIERNES", label: "VIERNES", order: 5 },
  { value: "SABADO", label: "SÁBADO", order: 6 },
  { value: "DOMINGO", label: "DOMINGO", order: 7 }
];

const DAYS_ORDER = {
  LUNES: 1,
  MARTES: 2,
  MIERCOLES: 3,
  JUEVES: 4,
  VIERNES: 5,
  SABADO: 6,
  DOMINGO: 7
};

const initialHorarioForm = {
  doctor_id: "",
  tipo_horario: "DIA",
  dia_inicio: "LUNES",
  dia_fin: "VIERNES",
  hora_inicio: "",
  hora_fin: "",
  estado: "ACTIVO"
};

const initialDisponibilidadForm = {
  doctor_id: "",
  fecha: "",
  hora_inicio: "",
  hora_fin: "",
  estado: "NO DISPONIBLE"
};

function AgendaMedica() {
  const [horarios, setHorarios] = useState([]);
  const [disponibilidades, setDisponibilidades] = useState([]);
  const [doctores, setDoctores] = useState([]);

  const [selectedDoctorId, setSelectedDoctorId] = useState("");
  const [horarioForm, setHorarioForm] = useState(initialHorarioForm);
  const [disponibilidadForm, setDisponibilidadForm] = useState(
    initialDisponibilidadForm
  );

  const [editingHorarioId, setEditingHorarioId] = useState(null);
  const [editingDisponibilidadId, setEditingDisponibilidadId] = useState(null);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadHorarios() {
    const data = await apiClient.get("/horarios-doctores");
    setHorarios(data);
  }

  async function loadDisponibilidades() {
    const data = await apiClient.get("/disponibilidad-doctores");
    setDisponibilidades(data);
  }

  async function loadDoctores() {
    const data = await apiClient.get("/doctores");
    setDoctores(data);
  }

  async function loadPageData() {
    try {
      setLoading(true);
      setError("");

      await Promise.all([
        loadHorarios(),
        loadDisponibilidades(),
        loadDoctores()
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadPageData();
  }, []);

  function normalizeTimeForInput(value) {
    if (!value) {
      return "";
    }

    return value.substring(0, 5);
  }

  function getDayLabel(dayValue) {
    const day = DAYS.find((item) => item.value === dayValue);

    if (!day) {
      return dayValue;
    }

    return day.label;
  }

  function getDaysInRange(startDay, endDay) {
    const start = DAYS.find((day) => day.value === startDay);
    const end = DAYS.find((day) => day.value === endDay);

    if (!start || !end) {
      return [];
    }

    if (start.order > end.order) {
      return [];
    }

    return DAYS.filter(
      (day) => day.order >= start.order && day.order <= end.order
    ).map((day) => day.value);
  }

  function handleDoctorSelect(event) {
    const doctorId = event.target.value;

    setSelectedDoctorId(doctorId);

    setHorarioForm({
      ...initialHorarioForm,
      doctor_id: doctorId
    });

    setDisponibilidadForm({
      ...initialDisponibilidadForm,
      doctor_id: doctorId
    });

    setEditingHorarioId(null);
    setEditingDisponibilidadId(null);
    setMessage("");
    setError("");
  }

  function handleHorarioChange(event) {
    const { name, value } = event.target;

    setHorarioForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function handleDisponibilidadChange(event) {
    const { name, value } = event.target;

    setDisponibilidadForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function buildHorarioPayload(day) {
    return {
      doctor_id: Number(selectedDoctorId || horarioForm.doctor_id),
      dia_semana: day,
      hora_inicio: horarioForm.hora_inicio,
      hora_fin: horarioForm.hora_fin,
      estado: horarioForm.estado
    };
  }

  function buildDisponibilidadPayload() {
    return {
      doctor_id: Number(selectedDoctorId || disponibilidadForm.doctor_id),
      fecha: disponibilidadForm.fecha,
      hora_inicio: disponibilidadForm.hora_inicio,
      hora_fin: disponibilidadForm.hora_fin,
      estado: disponibilidadForm.estado
    };
  }

  async function handleHorarioSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      if (selectedDoctorId === "") {
        setError("Debe seleccionar un doctor antes de guardar un horario.");
        return;
      }

      if (horarioForm.hora_inicio >= horarioForm.hora_fin) {
        setError("La hora de inicio debe ser menor que la hora de fin.");
        return;
      }

      if (editingHorarioId !== null) {
        const payload = buildHorarioPayload(horarioForm.dia_inicio);

        await apiClient.put(`/horarios-doctores/${editingHorarioId}`, payload);

        setMessage("Horario de atención actualizado correctamente.");
      } else {
        let selectedDays = [];

        if (horarioForm.tipo_horario === "DIA") {
          selectedDays = [horarioForm.dia_inicio];
        } else {
          selectedDays = getDaysInRange(
            horarioForm.dia_inicio,
            horarioForm.dia_fin
          );
        }

        if (selectedDays.length === 0) {
          setError(
            "El rango de días no es válido. El día inicial debe ser anterior o igual al día final."
          );
          return;
        }

        for (const day of selectedDays) {
          const payload = buildHorarioPayload(day);

          await apiClient.post("/horarios-doctores", payload);
        }

        if (selectedDays.length === 1) {
          setMessage("Horario de atención guardado correctamente.");
        } else {
          setMessage("Rango de horarios guardado correctamente.");
        }
      }

      setHorarioForm({
        ...initialHorarioForm,
        doctor_id: selectedDoctorId
      });

      setEditingHorarioId(null);

      await loadHorarios();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDisponibilidadSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      if (selectedDoctorId === "") {
        setError(
          "Debe seleccionar un doctor antes de registrar una fecha especial."
        );
        return;
      }

      if (disponibilidadForm.hora_inicio >= disponibilidadForm.hora_fin) {
        setError("La hora de inicio debe ser menor que la hora de fin.");
        return;
      }

      const payload = buildDisponibilidadPayload();

      if (editingDisponibilidadId === null) {
        await apiClient.post("/disponibilidad-doctores", payload);
        setMessage("Fecha especial guardada correctamente.");
      } else {
        await apiClient.put(
          `/disponibilidad-doctores/${editingDisponibilidadId}`,
          payload
        );
        setMessage("Fecha especial actualizada correctamente.");
      }

      setDisponibilidadForm({
        ...initialDisponibilidadForm,
        doctor_id: selectedDoctorId
      });

      setEditingDisponibilidadId(null);

      await loadDisponibilidades();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEditHorario(horario) {
    setSelectedDoctorId(String(horario.doctor_id));
    setEditingHorarioId(horario.horario_id);

    setHorarioForm({
      doctor_id: horario.doctor_id ?? "",
      tipo_horario: "DIA",
      dia_inicio: horario.dia_semana ?? "LUNES",
      dia_fin: horario.dia_semana ?? "LUNES",
      hora_inicio: normalizeTimeForInput(horario.hora_inicio),
      hora_fin: normalizeTimeForInput(horario.hora_fin),
      estado: horario.estado ?? "ACTIVO"
    });

    setMessage("Horario seleccionado para edición.");
    setError("");
  }

  function handleEditDisponibilidad(disponibilidad) {
    setSelectedDoctorId(String(disponibilidad.doctor_id));
    setEditingDisponibilidadId(disponibilidad.disponibilidad_id);

    setDisponibilidadForm({
      doctor_id: disponibilidad.doctor_id ?? "",
      fecha: disponibilidad.fecha
        ? disponibilidad.fecha.substring(0, 10)
        : "",
      hora_inicio: normalizeTimeForInput(disponibilidad.hora_inicio),
      hora_fin: normalizeTimeForInput(disponibilidad.hora_fin),
      estado: disponibilidad.estado ?? "NO DISPONIBLE"
    });

    setMessage("Fecha especial seleccionada para edición.");
    setError("");
  }

  async function handleDeleteHorario(horarioId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este horario de atención?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/horarios-doctores/${horarioId}`);

      setMessage("Horario eliminado correctamente.");

      if (editingHorarioId === horarioId) {
        setEditingHorarioId(null);
        setHorarioForm({
          ...initialHorarioForm,
          doctor_id: selectedDoctorId
        });
      }

      await loadHorarios();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDeleteDisponibilidad(disponibilidadId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar esta fecha especial?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(
        `/disponibilidad-doctores/${disponibilidadId}`
      );

      setMessage("Fecha especial eliminada correctamente.");

      if (editingDisponibilidadId === disponibilidadId) {
        setEditingDisponibilidadId(null);
        setDisponibilidadForm({
          ...initialDisponibilidadForm,
          doctor_id: selectedDoctorId
        });
      }

      await loadDisponibilidades();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleCancelHorarioEdit() {
    setEditingHorarioId(null);

    setHorarioForm({
      ...initialHorarioForm,
      doctor_id: selectedDoctorId
    });

    setMessage("");
    setError("");
  }

  function handleCancelDisponibilidadEdit() {
    setEditingDisponibilidadId(null);

    setDisponibilidadForm({
      ...initialDisponibilidadForm,
      doctor_id: selectedDoctorId
    });

    setMessage("");
    setError("");
  }

  function getDoctorById(doctorId) {
    return doctores.find(
      (item) => String(item.doctor_id) === String(doctorId)
    );
  }

  function getDoctorLabel(doctorId) {
    const doctor = getDoctorById(doctorId);

    if (!doctor) {
      return doctorId || "";
    }

    return `${doctor.nombre} ${doctor.apellido}`;
  }

  function getHorarioBadgeClass(estado) {
    if (estado === "ACTIVO") {
      return "badge success-badge";
    }

    return "badge warning-badge";
  }

  function getDisponibilidadBadgeClass(estado) {
    if (estado === "DISPONIBLE") {
      return "badge success-badge";
    }

    if (
      estado === "OCUPADO" ||
      estado === "NO DISPONIBLE" ||
      estado === "BLOQUEADO"
    ) {
      return "badge danger-badge";
    }

    return "badge warning-badge";
  }

  function getHorariosByDoctorId(doctorId) {
    return horarios
      .filter((horario) => String(horario.doctor_id) === String(doctorId))
      .sort(
        (a, b) =>
          (DAYS_ORDER[a.dia_semana] || 99) -
          (DAYS_ORDER[b.dia_semana] || 99)
      );
  }

  function getDisponibilidadesByDoctorId(doctorId) {
    return disponibilidades
      .filter(
        (disponibilidad) =>
          String(disponibilidad.doctor_id) === String(doctorId)
      )
      .sort((a, b) => {
        const firstDate = a.fecha || "";
        const secondDate = b.fecha || "";

        return secondDate.localeCompare(firstDate);
      });
  }

  const selectedDoctor = selectedDoctorId
    ? getDoctorById(selectedDoctorId)
    : null;

  const selectedDoctorHorarios = selectedDoctorId
    ? getHorariosByDoctorId(selectedDoctorId)
    : [];

  const selectedDoctorDisponibilidades = selectedDoctorId
    ? getDisponibilidadesByDoctorId(selectedDoctorId)
    : [];

  const allHorariosSorted = [...horarios].sort((a, b) => {
    const doctorCompare = String(a.doctor_id).localeCompare(String(b.doctor_id));

    if (doctorCompare !== 0) {
      return doctorCompare;
    }

    return (
      (DAYS_ORDER[a.dia_semana] || 99) -
      (DAYS_ORDER[b.dia_semana] || 99)
    );
  });

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Agenda Médica</h2>
          <p>
            Gestión de horarios de atención y fechas especiales por doctor.
          </p>
        </div>
      </div>

      <section className="card">
        <h3>Seleccionar doctor</h3>

        <p className="helper-text">
          Seleccione un doctor para revisar o modificar su agenda.
        </p>

        <div className="form-grid">
          <label>
            Doctor
            <select value={selectedDoctorId} onChange={handleDoctorSelect}>
              <option value="">Seleccione un doctor</option>

              {doctores.map((doctor) => (
                <option key={doctor.doctor_id} value={doctor.doctor_id}>
                  {doctor.nombre} {doctor.apellido}
                </option>
              ))}
            </select>
          </label>
        </div>

        {selectedDoctor && (
          <div className="agenda-summary">
            <p>
              <strong>Doctor:</strong> {selectedDoctor.nombre}{" "}
              {selectedDoctor.apellido}
            </p>

            <p>
              <strong>Horarios activos:</strong>{" "}
              {
                selectedDoctorHorarios.filter(
                  (horario) => horario.estado === "ACTIVO"
                ).length
              }
            </p>

            <p>
              <strong>Fechas especiales registradas:</strong>{" "}
              {selectedDoctorDisponibilidades.length}
            </p>
          </div>
        )}

        {loading && <p>Cargando...</p>}
        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
      </section>

      {selectedDoctor && (
        <>
          <section className="card">
            <form onSubmit={handleHorarioSubmit}>
              <h3>
                {editingHorarioId === null
                  ? "Horario regular de atención"
                  : "Editar horario regular"}
              </h3>

              <p className="helper-text">
                Puede registrar un horario para un solo día o para un rango de
                días, por ejemplo de lunes a viernes.
              </p>

              <div className="form-grid">
                <label>
                  Tipo de horario
                  <select
                    name="tipo_horario"
                    value={horarioForm.tipo_horario}
                    onChange={handleHorarioChange}
                    disabled={editingHorarioId !== null}
                    required
                  >
                    <option value="DIA">Un solo día</option>
                    <option value="RANGO">Rango de días</option>
                  </select>
                </label>

                <label>
                  {horarioForm.tipo_horario === "DIA" ||
                  editingHorarioId !== null
                    ? "Día de atención"
                    : "Desde"}
                  <select
                    name="dia_inicio"
                    value={horarioForm.dia_inicio}
                    onChange={handleHorarioChange}
                    required
                  >
                    {DAYS.map((day) => (
                      <option key={day.value} value={day.value}>
                        {day.label}
                      </option>
                    ))}
                  </select>
                </label>

                {horarioForm.tipo_horario === "RANGO" &&
                  editingHorarioId === null && (
                    <label>
                      Hasta
                      <select
                        name="dia_fin"
                        value={horarioForm.dia_fin}
                        onChange={handleHorarioChange}
                        required
                      >
                        {DAYS.map((day) => (
                          <option key={day.value} value={day.value}>
                            {day.label}
                          </option>
                        ))}
                      </select>
                    </label>
                  )}

                <label>
                  Hora de inicio
                  <input
                    type="time"
                    name="hora_inicio"
                    value={horarioForm.hora_inicio}
                    onChange={handleHorarioChange}
                    required
                  />
                </label>

                <label>
                  Hora de fin
                  <input
                    type="time"
                    name="hora_fin"
                    value={horarioForm.hora_fin}
                    onChange={handleHorarioChange}
                    required
                  />
                </label>

                <label>
                  Estado del horario
                  <select
                    name="estado"
                    value={horarioForm.estado}
                    onChange={handleHorarioChange}
                    required
                  >
                    <option value="ACTIVO">ACTIVO</option>
                    <option value="INACTIVO">INACTIVO</option>
                  </select>
                </label>
              </div>

              <div className="form-actions">
                <button type="submit" disabled={loading}>
                  {editingHorarioId === null
                    ? "Guardar horario"
                    : "Actualizar horario"}
                </button>

                {editingHorarioId !== null && (
                  <button
                    type="button"
                    className="secondary-button"
                    onClick={handleCancelHorarioEdit}
                  >
                    Cancelar
                  </button>
                )}
              </div>
            </form>
          </section>

          <section className="card">
            <form onSubmit={handleDisponibilidadSubmit}>
              <h3>
                {editingDisponibilidadId === null
                  ? "Fecha especial o bloqueo"
                  : "Editar fecha especial"}
              </h3>

              <p className="helper-text">
                Registre ausencias, espacios ocupados, bloqueos o disponibilidad
                específica para una fecha concreta.
              </p>

              <div className="form-grid">
                <label>
                  Fecha
                  <input
                    type="date"
                    name="fecha"
                    value={disponibilidadForm.fecha}
                    onChange={handleDisponibilidadChange}
                    required
                  />
                </label>

                <label>
                  Hora de inicio
                  <input
                    type="time"
                    name="hora_inicio"
                    value={disponibilidadForm.hora_inicio}
                    onChange={handleDisponibilidadChange}
                    required
                  />
                </label>

                <label>
                  Hora de fin
                  <input
                    type="time"
                    name="hora_fin"
                    value={disponibilidadForm.hora_fin}
                    onChange={handleDisponibilidadChange}
                    required
                  />
                </label>

                <label>
                  Estado
                  <select
                    name="estado"
                    value={disponibilidadForm.estado}
                    onChange={handleDisponibilidadChange}
                    required
                  >
                    <option value="DISPONIBLE">DISPONIBLE</option>
                    <option value="OCUPADO">OCUPADO</option>
                    <option value="NO DISPONIBLE">NO DISPONIBLE</option>
                    <option value="BLOQUEADO">BLOQUEADO</option>
                  </select>
                </label>
              </div>

              <div className="form-actions">
                <button type="submit" disabled={loading}>
                  {editingDisponibilidadId === null
                    ? "Guardar fecha especial"
                    : "Actualizar fecha especial"}
                </button>

                {editingDisponibilidadId !== null && (
                  <button
                    type="button"
                    className="secondary-button"
                    onClick={handleCancelDisponibilidadEdit}
                  >
                    Cancelar
                  </button>
                )}
              </div>
            </form>
          </section>

          <section className="card">
            <h3>Agenda del doctor seleccionado</h3>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Día</th>
                    <th>Hora inicio</th>
                    <th>Hora fin</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>

                <tbody>
                  {selectedDoctorHorarios.map((horario) => (
                    <tr key={horario.horario_id}>
                      <td>{getDayLabel(horario.dia_semana)}</td>
                      <td>{horario.hora_inicio}</td>
                      <td>{horario.hora_fin}</td>
                      <td>
                        <span className={getHorarioBadgeClass(horario.estado)}>
                          {horario.estado}
                        </span>
                      </td>
                      <td>
                        <button
                          type="button"
                          className="small-button"
                          onClick={() => handleEditHorario(horario)}
                        >
                          Editar
                        </button>

                        <button
                          type="button"
                          className="danger-button"
                          onClick={() => handleDeleteHorario(horario.horario_id)}
                        >
                          Eliminar
                        </button>
                      </td>
                    </tr>
                  ))}

                  {selectedDoctorHorarios.length === 0 && (
                    <tr>
                      <td colSpan="5">
                        Este doctor no tiene horario regular registrado.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>

          <section className="card">
            <h3>Fechas especiales del doctor</h3>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Hora inicio</th>
                    <th>Hora fin</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>

                <tbody>
                  {selectedDoctorDisponibilidades.map((disponibilidad) => (
                    <tr key={disponibilidad.disponibilidad_id}>
                      <td>
                        {disponibilidad.fecha
                          ? disponibilidad.fecha.substring(0, 10)
                          : ""}
                      </td>
                      <td>{disponibilidad.hora_inicio}</td>
                      <td>{disponibilidad.hora_fin}</td>
                      <td>
                        <span
                          className={getDisponibilidadBadgeClass(
                            disponibilidad.estado
                          )}
                        >
                          {disponibilidad.estado}
                        </span>
                      </td>
                      <td>
                        <button
                          type="button"
                          className="small-button"
                          onClick={() =>
                            handleEditDisponibilidad(disponibilidad)
                          }
                        >
                          Editar
                        </button>

                        <button
                          type="button"
                          className="danger-button"
                          onClick={() =>
                            handleDeleteDisponibilidad(
                              disponibilidad.disponibilidad_id
                            )
                          }
                        >
                          Eliminar
                        </button>
                      </td>
                    </tr>
                  ))}

                  {selectedDoctorDisponibilidades.length === 0 && (
                    <tr>
                      <td colSpan="5">
                        Este doctor no tiene fechas especiales registradas.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}

      <section className="card">
        <h3>Resumen general de horarios</h3>

        <p className="helper-text">
          Vista general para revisar rápidamente los horarios registrados de
          todos los doctores.
        </p>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Doctor</th>
                <th>Día</th>
                <th>Hora inicio</th>
                <th>Hora fin</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {allHorariosSorted.map((horario) => (
                <tr key={horario.horario_id}>
                  <td>
                    {horario.doctor_nombre ||
                      getDoctorLabel(horario.doctor_id)}
                  </td>
                  <td>{getDayLabel(horario.dia_semana)}</td>
                  <td>{horario.hora_inicio}</td>
                  <td>{horario.hora_fin}</td>
                  <td>
                    <span className={getHorarioBadgeClass(horario.estado)}>
                      {horario.estado}
                    </span>
                  </td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEditHorario(horario)}
                    >
                      Abrir
                    </button>
                  </td>
                </tr>
              ))}

              {horarios.length === 0 && !loading && (
                <tr>
                  <td colSpan="6">No hay horarios registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default AgendaMedica;