import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

function getTodayDate() {
  return new Date().toISOString().substring(0, 10);
}

const initialHistorialForm = {
  paciente_id: "",
  doctor_id: "",
  alergias: "",
  enfermedades: "",
  medicamentos: "",
  antecedentes_quirurgicos: "",
  observaciones: "",
  fecha_registro: getTodayDate()
};

const initialCirugiaForm = {
  tratamiento_consulta_id: "",
  doctor_id: "",
  fecha_cirugia: "",
  descripcion_quirurgica: "",
  anestesia: "",
  observaciones: "",
  estado: "PROGRAMADA"
};

function ExpedienteClinico() {
  const [historiales, setHistoriales] = useState([]);
  const [cirugias, setCirugias] = useState([]);
  const [pacientes, setPacientes] = useState([]);
  const [doctores, setDoctores] = useState([]);
  const [consultas, setConsultas] = useState([]);
  const [tratamientosConsulta, setTratamientosConsulta] = useState([]);

  const [selectedPacienteId, setSelectedPacienteId] = useState("");
  const [historialForm, setHistorialForm] = useState(initialHistorialForm);
  const [cirugiaForm, setCirugiaForm] = useState(initialCirugiaForm);

  const [editingHistorialId, setEditingHistorialId] = useState(null);
  const [editingCirugiaId, setEditingCirugiaId] = useState(null);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadHistoriales() {
    const data = await apiClient.get("/historial-medico");
    setHistoriales(data);
  }

  async function loadCirugias() {
    const data = await apiClient.get("/cirugias");
    setCirugias(data);
  }

  async function loadPacientes() {
    const data = await apiClient.get("/pacientes");
    setPacientes(data);
  }

  async function loadDoctores() {
    const data = await apiClient.get("/doctores");
    setDoctores(data);
  }

  async function loadConsultas() {
    const data = await apiClient.get("/consultas");
    setConsultas(data);
  }

  async function loadTratamientosConsulta() {
    const data = await apiClient.get("/tratamientos-consulta");
    setTratamientosConsulta(data);
  }

  async function loadPageData() {
    try {
      setLoading(true);
      setError("");

      await Promise.all([
        loadHistoriales(),
        loadCirugias(),
        loadPacientes(),
        loadDoctores(),
        loadConsultas(),
        loadTratamientosConsulta()
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

  function getPacienteById(pacienteId) {
    return pacientes.find(
      (paciente) => String(paciente.paciente_id) === String(pacienteId)
    );
  }

  function getPacienteLabel(pacienteId) {
    const paciente = getPacienteById(pacienteId);

    if (!paciente) {
      return pacienteId || "";
    }

    return `${paciente.nombre} ${paciente.apellido}`;
  }

  function getDoctorLabel(doctorId) {
    const doctor = doctores.find(
      (item) => String(item.doctor_id) === String(doctorId)
    );

    if (!doctor) {
      return doctorId || "";
    }

    return `${doctor.nombre} ${doctor.apellido}`;
  }

  function getConsultaById(consultaId) {
    return consultas.find(
      (consulta) => String(consulta.consulta_id) === String(consultaId)
    );
  }

  function getTratamientoConsultaById(tratamientoConsultaId) {
    return tratamientosConsulta.find(
      (item) =>
        String(item.tratamiento_consulta_id) === String(tratamientoConsultaId)
    );
  }

  function getHistorialByPacienteId(pacienteId) {
    const patientHistories = historiales.filter(
      (historial) => String(historial.paciente_id) === String(pacienteId)
    );

    if (patientHistories.length === 0) {
      return null;
    }

    return patientHistories[patientHistories.length - 1];
  }

  function getTratamientoConsultaPacienteId(item) {
    if (item?.paciente_id) {
      return item.paciente_id;
    }

    const consulta = getConsultaById(item?.consulta_id);

    return consulta?.paciente_id || "";
  }

  function getCirugiaPacienteId(cirugia) {
    if (cirugia?.paciente_id) {
      return cirugia.paciente_id;
    }

    const tratamientoConsulta = getTratamientoConsultaById(
      cirugia.tratamiento_consulta_id
    );

    return getTratamientoConsultaPacienteId(tratamientoConsulta);
  }

  function getCirugiasByPacienteId(pacienteId) {
    return cirugias.filter(
      (cirugia) => String(getCirugiaPacienteId(cirugia)) === String(pacienteId)
    );
  }

  function getAvailableTratamientosConsulta() {
    if (selectedPacienteId === "") {
      return [];
    }

    return tratamientosConsulta.filter(
      (item) =>
        String(getTratamientoConsultaPacienteId(item)) ===
        String(selectedPacienteId)
    );
  }

  function getTreatmentName(item) {
    return (
      item?.tratamiento_nombre ||
      item?.nombre_tratamiento ||
      item?.nombre ||
      `Tratamiento ${item?.tratamiento_id || ""}`
    );
  }

  function formatTratamientoConsultaLabel(item) {
    const treatmentName = getTreatmentName(item);
    const consulta = getConsultaById(item.consulta_id);

    const doctor =
      item.doctor_nombre ||
      consulta?.doctor_nombre ||
      (consulta?.doctor_id ? getDoctorLabel(consulta.doctor_id) : "Doctor");

    return `Consulta ${item.consulta_id} - ${treatmentName} - ${doctor}`;
  }

  function getProcedureLabel(cirugia) {
    const tratamientoConsulta = getTratamientoConsultaById(
      cirugia.tratamiento_consulta_id
    );

    if (!tratamientoConsulta) {
      return `Procedimiento ${cirugia.tratamiento_consulta_id}`;
    }

    return getTreatmentName(tratamientoConsulta);
  }

  function getStatusBadgeClass(status) {
    if (status === "REALIZADA") {
      return "badge success-badge";
    }

    if (status === "CANCELADA") {
      return "badge danger-badge";
    }

    return "badge warning-badge";
  }

  function loadPatientRecord(pacienteId) {
    const existingHistorial = getHistorialByPacienteId(pacienteId);

    setSelectedPacienteId(pacienteId);

    if (existingHistorial) {
      setEditingHistorialId(existingHistorial.historial_id);

      setHistorialForm({
        paciente_id: existingHistorial.paciente_id ?? pacienteId,
        doctor_id: existingHistorial.doctor_id ?? "",
        alergias: existingHistorial.alergias ?? "",
        enfermedades: existingHistorial.enfermedades ?? "",
        medicamentos: existingHistorial.medicamentos ?? "",
        antecedentes_quirurgicos:
          existingHistorial.antecedentes_quirurgicos ?? "",
        observaciones: existingHistorial.observaciones ?? "",
        fecha_registro: existingHistorial.fecha_registro
          ? existingHistorial.fecha_registro.substring(0, 10)
          : getTodayDate()
      });
    } else {
      setEditingHistorialId(null);

      setHistorialForm({
        ...initialHistorialForm,
        paciente_id: pacienteId,
        fecha_registro: getTodayDate()
      });
    }

    setCirugiaForm(initialCirugiaForm);
    setEditingCirugiaId(null);
    setMessage("");
    setError("");
  }

  function handlePatientSelect(event) {
    const pacienteId = event.target.value;

    if (pacienteId === "") {
      setSelectedPacienteId("");
      setHistorialForm(initialHistorialForm);
      setCirugiaForm(initialCirugiaForm);
      setEditingHistorialId(null);
      setEditingCirugiaId(null);
      return;
    }

    loadPatientRecord(pacienteId);
  }

  function handleHistorialChange(event) {
    const { name, value } = event.target;

    setHistorialForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function handleCirugiaChange(event) {
    const { name, value } = event.target;

    if (name === "tratamiento_consulta_id") {
      const selectedTreatment = getTratamientoConsultaById(value);

      setCirugiaForm((currentForm) => ({
        ...currentForm,
        tratamiento_consulta_id: value,
        descripcion_quirurgica:
          currentForm.descripcion_quirurgica ||
          (selectedTreatment ? getTreatmentName(selectedTreatment) : "")
      }));

      return;
    }

    setCirugiaForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function buildHistorialPayload() {
    return {
      paciente_id: Number(selectedPacienteId || historialForm.paciente_id),
      doctor_id: Number(historialForm.doctor_id),
      alergias: historialForm.alergias || null,
      enfermedades: historialForm.enfermedades || null,
      medicamentos: historialForm.medicamentos || null,
      antecedentes_quirurgicos:
        historialForm.antecedentes_quirurgicos || null,
      observaciones: historialForm.observaciones || null,
      fecha_registro: historialForm.fecha_registro || null
    };
  }

  function buildCirugiaPayload() {
    return {
      tratamiento_consulta_id: Number(cirugiaForm.tratamiento_consulta_id),
      doctor_id: Number(cirugiaForm.doctor_id),
      fecha_cirugia: cirugiaForm.fecha_cirugia || null,
      descripcion_quirurgica: cirugiaForm.descripcion_quirurgica || null,
      anestesia: cirugiaForm.anestesia || null,
      observaciones: cirugiaForm.observaciones || null,
      estado: cirugiaForm.estado
    };
  }

  async function handleHistorialSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      if (selectedPacienteId === "") {
        setError("Debe seleccionar un paciente antes de guardar.");
        return;
      }

      const payload = buildHistorialPayload();

      if (editingHistorialId === null) {
        await apiClient.post("/historial-medico", payload);
        setMessage("Expediente clínico creado correctamente.");
      } else {
        await apiClient.put(`/historial-medico/${editingHistorialId}`, payload);
        setMessage("Expediente clínico actualizado correctamente.");
      }

      await loadHistoriales();

      const updatedHistoriales = await apiClient.get("/historial-medico");
      setHistoriales(updatedHistoriales);

      const updatedRecord = updatedHistoriales.find(
        (historial) =>
          String(historial.paciente_id) === String(selectedPacienteId)
      );

      if (updatedRecord) {
        setEditingHistorialId(updatedRecord.historial_id);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleCirugiaSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      if (selectedPacienteId === "") {
        setError("Debe seleccionar un paciente antes de registrar un procedimiento.");
        return;
      }

      const payload = buildCirugiaPayload();

      if (editingCirugiaId === null) {
        await apiClient.post("/cirugias", payload);
        setMessage("Procedimiento registrado correctamente.");
      } else {
        await apiClient.put(`/cirugias/${editingCirugiaId}`, payload);
        setMessage("Procedimiento actualizado correctamente.");
      }

      setCirugiaForm(initialCirugiaForm);
      setEditingCirugiaId(null);

      await loadCirugias();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEditHistorial(historial) {
    loadPatientRecord(historial.paciente_id);
  }

  function handleEditCirugia(cirugia) {
    const pacienteId = getCirugiaPacienteId(cirugia);

    if (pacienteId) {
      loadPatientRecord(pacienteId);
    }

    setEditingCirugiaId(cirugia.cirugia_id);

    setCirugiaForm({
      tratamiento_consulta_id: cirugia.tratamiento_consulta_id ?? "",
      doctor_id: cirugia.doctor_id ?? "",
      fecha_cirugia: cirugia.fecha_cirugia
        ? cirugia.fecha_cirugia.substring(0, 16)
        : "",
      descripcion_quirurgica: cirugia.descripcion_quirurgica ?? "",
      anestesia: cirugia.anestesia ?? "",
      observaciones: cirugia.observaciones ?? "",
      estado: cirugia.estado ?? "PROGRAMADA"
    });

    setMessage("Procedimiento seleccionado para edición.");
    setError("");
  }

  async function handleDeleteHistorial(historialId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este expediente clínico?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/historial-medico/${historialId}`);

      setMessage("Expediente clínico eliminado correctamente.");

      if (editingHistorialId === historialId) {
        setEditingHistorialId(null);
        setHistorialForm({
          ...initialHistorialForm,
          paciente_id: selectedPacienteId,
          fecha_registro: getTodayDate()
        });
      }

      await loadHistoriales();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDeleteCirugia(cirugiaId) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar este procedimiento?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(`/cirugias/${cirugiaId}`);

      setMessage("Procedimiento eliminado correctamente.");

      if (editingCirugiaId === cirugiaId) {
        setEditingCirugiaId(null);
        setCirugiaForm(initialCirugiaForm);
      }

      await loadCirugias();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleCancelCirugiaEdit() {
    setEditingCirugiaId(null);
    setCirugiaForm(initialCirugiaForm);
    setMessage("");
    setError("");
  }

  const selectedPaciente = selectedPacienteId
    ? getPacienteById(selectedPacienteId)
    : null;

  const selectedHistorial = selectedPacienteId
    ? getHistorialByPacienteId(selectedPacienteId)
    : null;

  const selectedCirugias = selectedPacienteId
    ? getCirugiasByPacienteId(selectedPacienteId)
    : [];

  const sortedHistoriales = [...historiales].sort(
    (a, b) => Number(b.historial_id) - Number(a.historial_id)
  );

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Expediente Clínico</h2>
          <p>
            Consulta y mantenimiento del expediente médico del paciente.
          </p>
        </div>
      </div>

      <section className="card">
        <h3>Seleccionar paciente</h3>

        <p className="helper-text">
          Seleccione un paciente para revisar sus datos médicos, antecedentes y
          procedimientos realizados.
        </p>

        <div className="form-grid">
          <label>
            Paciente
            <select
              value={selectedPacienteId}
              onChange={handlePatientSelect}
            >
              <option value="">Seleccione un paciente</option>

              {pacientes.map((paciente) => (
                <option key={paciente.paciente_id} value={paciente.paciente_id}>
                  {paciente.nombre} {paciente.apellido}
                </option>
              ))}
            </select>
          </label>
        </div>

        {selectedPaciente && (
          <div className="clinical-summary">
            <p>
              <strong>Paciente:</strong> {selectedPaciente.nombre}{" "}
              {selectedPaciente.apellido}
            </p>

            <p>
              <strong>Teléfono:</strong>{" "}
              {selectedPaciente.telefono || "No registrado"}
            </p>

            <p>
              <strong>Correo:</strong>{" "}
              {selectedPaciente.correo || "No registrado"}
            </p>

            <p>
              <strong>Estado del expediente:</strong>{" "}
              {selectedHistorial ? "Expediente existente" : "Sin expediente previo"}
            </p>
          </div>
        )}

        {loading && <p>Cargando...</p>}
        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
      </section>

      {selectedPaciente && (
        <>
          <section className="card">
            <form onSubmit={handleHistorialSubmit}>
              <h3>
                {editingHistorialId === null
                  ? "Datos médicos del paciente"
                  : "Actualizar datos médicos"}
              </h3>

              <p className="helper-text">
                Registre la información clínica general del paciente. Estos
                datos forman la base del expediente.
              </p>

              <div className="form-grid">
                <label>
                  Doctor responsable
                  <select
                    name="doctor_id"
                    value={historialForm.doctor_id}
                    onChange={handleHistorialChange}
                    required
                  >
                    <option value="">Seleccione un doctor</option>

                    {doctores.map((doctor) => (
                      <option key={doctor.doctor_id} value={doctor.doctor_id}>
                        {doctor.nombre} {doctor.apellido}
                      </option>
                    ))}
                  </select>
                </label>

                <label>
                  Fecha de actualización
                  <input
                    type="date"
                    name="fecha_registro"
                    value={historialForm.fecha_registro}
                    onChange={handleHistorialChange}
                  />
                </label>

                <label>
                  Alergias conocidas
                  <textarea
                    name="alergias"
                    value={historialForm.alergias}
                    onChange={handleHistorialChange}
                    rows="3"
                    placeholder="Ejemplo: Penicilina, anestesia, látex..."
                  />
                </label>

                <label>
                  Condiciones médicas
                  <textarea
                    name="enfermedades"
                    value={historialForm.enfermedades}
                    onChange={handleHistorialChange}
                    rows="3"
                    placeholder="Ejemplo: Diabetes, hipertensión, asma..."
                  />
                </label>

                <label>
                  Medicamentos actuales
                  <textarea
                    name="medicamentos"
                    value={historialForm.medicamentos}
                    onChange={handleHistorialChange}
                    rows="3"
                    placeholder="Medicamentos que el paciente utiliza actualmente"
                  />
                </label>

                <label>
                  Antecedentes quirúrgicos
                  <textarea
                    name="antecedentes_quirurgicos"
                    value={historialForm.antecedentes_quirurgicos}
                    onChange={handleHistorialChange}
                    rows="3"
                    placeholder="Cirugías o procedimientos previos relevantes"
                  />
                </label>

                <label>
                  Notas clínicas generales
                  <textarea
                    name="observaciones"
                    value={historialForm.observaciones}
                    onChange={handleHistorialChange}
                    rows="3"
                    placeholder="Notas importantes para la atención del paciente"
                  />
                </label>
              </div>

              <div className="form-actions">
                <button type="submit" disabled={loading}>
                  {editingHistorialId === null
                    ? "Guardar expediente"
                    : "Actualizar expediente"}
                </button>
              </div>
            </form>
          </section>

          <section className="card">
            <form onSubmit={handleCirugiaSubmit}>
              <h3>
                {editingCirugiaId === null
                  ? "Registrar procedimiento"
                  : "Editar procedimiento"}
              </h3>

              <p className="helper-text">
                Registre cirugías o procedimientos relevantes asociados al
                tratamiento del paciente seleccionado.
              </p>

              <div className="form-grid">
                <label>
                  Tratamiento realizado
                  <select
                    name="tratamiento_consulta_id"
                    value={cirugiaForm.tratamiento_consulta_id}
                    onChange={handleCirugiaChange}
                    required
                  >
                    <option value="">Seleccione tratamiento aplicado</option>

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
                  Doctor responsable
                  <select
                    name="doctor_id"
                    value={cirugiaForm.doctor_id}
                    onChange={handleCirugiaChange}
                    required
                  >
                    <option value="">Seleccione un doctor</option>

                    {doctores.map((doctor) => (
                      <option key={doctor.doctor_id} value={doctor.doctor_id}>
                        {doctor.nombre} {doctor.apellido}
                      </option>
                    ))}
                  </select>
                </label>

                <label>
                  Fecha y hora
                  <input
                    type="datetime-local"
                    name="fecha_cirugia"
                    value={cirugiaForm.fecha_cirugia}
                    onChange={handleCirugiaChange}
                  />
                </label>

                <label>
                  Estado
                  <select
                    name="estado"
                    value={cirugiaForm.estado}
                    onChange={handleCirugiaChange}
                  >
                    <option value="PROGRAMADA">PROGRAMADA</option>
                    <option value="REALIZADA">REALIZADA</option>
                    <option value="CANCELADA">CANCELADA</option>
                    <option value="EN SEGUIMIENTO">EN SEGUIMIENTO</option>
                  </select>
                </label>

                <label>
                  Anestesia
                  <input
                    type="text"
                    name="anestesia"
                    value={cirugiaForm.anestesia}
                    onChange={handleCirugiaChange}
                    placeholder="Local, general, sedación..."
                  />
                </label>

                <label>
                  Procedimiento realizado
                  <textarea
                    name="descripcion_quirurgica"
                    value={cirugiaForm.descripcion_quirurgica}
                    onChange={handleCirugiaChange}
                    rows="3"
                    placeholder="Describa el procedimiento realizado"
                  />
                </label>

                <label>
                  Observaciones y seguimiento
                  <textarea
                    name="observaciones"
                    value={cirugiaForm.observaciones}
                    onChange={handleCirugiaChange}
                    rows="3"
                    placeholder="Indicaciones, evolución o notas posteriores"
                  />
                </label>
              </div>

              <div className="form-actions">
                <button type="submit" disabled={loading}>
                  {editingCirugiaId === null
                    ? "Guardar procedimiento"
                    : "Actualizar procedimiento"}
                </button>

                {editingCirugiaId !== null && (
                  <button
                    type="button"
                    className="secondary-button"
                    onClick={handleCancelCirugiaEdit}
                  >
                    Cancelar
                  </button>
                )}
              </div>
            </form>
          </section>

          <section className="card">
            <h3>Resumen del expediente</h3>

            <div className="clinical-summary">
              <p>
                <strong>Alergias:</strong>{" "}
                {historialForm.alergias || "No registradas"}
              </p>

              <p>
                <strong>Condiciones médicas:</strong>{" "}
                {historialForm.enfermedades || "No registradas"}
              </p>

              <p>
                <strong>Medicamentos actuales:</strong>{" "}
                {historialForm.medicamentos || "No registrados"}
              </p>

              <p>
                <strong>Antecedentes quirúrgicos:</strong>{" "}
                {historialForm.antecedentes_quirurgicos || "No registrados"}
              </p>

              <p>
                <strong>Notas clínicas:</strong>{" "}
                {historialForm.observaciones || "No registradas"}
              </p>
            </div>
          </section>

          <section className="card">
            <h3>Procedimientos del paciente</h3>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Procedimiento</th>
                    <th>Doctor</th>
                    <th>Fecha</th>
                    <th>Anestesia</th>
                    <th>Estado</th>
                    <th>Observaciones</th>
                    <th>Acciones</th>
                  </tr>
                </thead>

                <tbody>
                  {selectedCirugias.map((cirugia) => (
                    <tr key={cirugia.cirugia_id}>
                      <td>{getProcedureLabel(cirugia)}</td>
                      <td>
                        {cirugia.doctor_nombre ||
                          getDoctorLabel(cirugia.doctor_id)}
                      </td>
                      <td>
                        {cirugia.fecha_cirugia
                          ? cirugia.fecha_cirugia
                              .substring(0, 16)
                              .replace("T", " ")
                          : ""}
                      </td>
                      <td>{cirugia.anestesia}</td>
                      <td>
                        <span className={getStatusBadgeClass(cirugia.estado)}>
                          {cirugia.estado}
                        </span>
                      </td>
                      <td>{cirugia.observaciones}</td>
                      <td>
                        <button
                          type="button"
                          className="small-button"
                          onClick={() => handleEditCirugia(cirugia)}
                        >
                          Editar
                        </button>

                        <button
                          type="button"
                          className="danger-button"
                          onClick={() => handleDeleteCirugia(cirugia.cirugia_id)}
                        >
                          Eliminar
                        </button>
                      </td>
                    </tr>
                  ))}

                  {selectedCirugias.length === 0 && (
                    <tr>
                      <td colSpan="7">
                        Este paciente no tiene procedimientos registrados.
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
        <h3>Expedientes registrados</h3>

        <p className="helper-text">
          Use esta lista para abrir rápidamente el expediente de un paciente.
        </p>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Paciente</th>
                <th>Doctor responsable</th>
                <th>Fecha actualización</th>
                <th>Alergias</th>
                <th>Condiciones médicas</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {sortedHistoriales.map((historial) => (
                <tr key={historial.historial_id}>
                  <td>
                    {historial.paciente_nombre ||
                      getPacienteLabel(historial.paciente_id)}
                  </td>
                  <td>
                    {historial.doctor_nombre ||
                      getDoctorLabel(historial.doctor_id)}
                  </td>
                  <td>
                    {historial.fecha_registro
                      ? historial.fecha_registro.substring(0, 10)
                      : ""}
                  </td>
                  <td>{historial.alergias}</td>
                  <td>{historial.enfermedades}</td>
                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() => handleEditHistorial(historial)}
                    >
                      Abrir
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() =>
                        handleDeleteHistorial(historial.historial_id)
                      }
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {historiales.length === 0 && !loading && (
                <tr>
                  <td colSpan="6">No hay expedientes registrados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default ExpedienteClinico;