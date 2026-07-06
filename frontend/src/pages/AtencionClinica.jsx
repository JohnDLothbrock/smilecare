import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const initialForm = {
  paciente_id: "",
  doctor_id: "",
  fecha_hora_inicio: "",
  duracion_minutos: "30",
  estado_cita: "FINALIZADA",
  motivo: "",

  diagnostico: "",
  observaciones_consulta: "",
  fecha_atencion: "",

  tratamiento_id: "",
  cantidad: "1",
  precio_unitario: "",

  incluye_cirugia: false,
  fecha_cirugia: "",
  descripcion_quirurgica: "",
  anestesia: "",
  observaciones_cirugia: "",
  estado_cirugia: "PROGRAMADA"
};

function AtencionClinica() {
  const [form, setForm] = useState(initialForm);

  const [pacientes, setPacientes] = useState([]);
  const [doctores, setDoctores] = useState([]);
  const [tratamientos, setTratamientos] = useState([]);
  const [citas, setCitas] = useState([]);
  const [consultas, setConsultas] = useState([]);
  const [tratamientosConsulta, setTratamientosConsulta] = useState([]);
  const [cirugias, setCirugias] = useState([]);

  const [selectedConsultaId, setSelectedConsultaId] = useState("");

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadPacientes() {
    const data = await apiClient.get("/pacientes");
    setPacientes(data);
  }

  async function loadDoctores() {
    const data = await apiClient.get("/doctores");
    setDoctores(data);
  }

  async function loadTratamientos() {
    const data = await apiClient.get("/tratamientos");
    setTratamientos(data);
  }

  async function loadCitas() {
    const data = await apiClient.get("/citas");
    setCitas(data);
  }

  async function loadConsultas() {
    const data = await apiClient.get("/consultas");
    setConsultas(data);
  }

  async function loadTratamientosConsulta() {
    const data = await apiClient.get("/tratamientos-consulta");
    setTratamientosConsulta(data);
  }

  async function loadCirugias() {
    const data = await apiClient.get("/cirugias");
    setCirugias(data);
  }

  async function loadPageData() {
    try {
      setLoading(true);
      setError("");

      await Promise.all([
        loadPacientes(),
        loadDoctores(),
        loadTratamientos(),
        loadCitas(),
        loadConsultas(),
        loadTratamientosConsulta(),
        loadCirugias()
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

  function handleChange(event) {
    const { name, value, type, checked } = event.target;

    if (type === "checkbox") {
      setForm((currentForm) => ({
        ...currentForm,
        [name]: checked
      }));

      return;
    }

    if (name === "tratamiento_id") {
      const selectedTratamiento = tratamientos.find(
        (tratamiento) => String(tratamiento.tratamiento_id) === value
      );

      setForm((currentForm) => ({
        ...currentForm,
        tratamiento_id: value,
        precio_unitario: selectedTratamiento?.costo_base ?? ""
      }));

      return;
    }

    setForm((currentForm) => {
      const updatedForm = {
        ...currentForm,
        [name]: value
      };

      if (name === "fecha_hora_inicio" && !currentForm.fecha_atencion) {
        updatedForm.fecha_atencion = value;
      }

      if (name === "fecha_hora_inicio" && !currentForm.fecha_cirugia) {
        updatedForm.fecha_cirugia = value;
      }

      return updatedForm;
    });
  }

  function resetForm() {
    setForm(initialForm);
  }

  function formatDateTime(value) {
    if (!value) {
      return "";
    }

    return value.substring(0, 16).replace("T", " ");
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

  function getDoctorName(doctorId) {
    const doctor = doctores.find(
      (item) => String(item.doctor_id) === String(doctorId)
    );

    if (!doctor) {
      return doctorId || "";
    }

    return `${doctor.nombre} ${doctor.apellido}`;
  }

  function getTratamientoName(tratamientoId) {
    const tratamiento = tratamientos.find(
      (item) => String(item.tratamiento_id) === String(tratamientoId)
    );

    if (!tratamiento) {
      return tratamientoId || "";
    }

    return tratamiento.nombre;
  }

  function getCitaById(citaId) {
    return citas.find(
      (cita) => String(cita.cita_id) === String(citaId)
    );
  }

  function getConsultaById(consultaId) {
    return consultas.find(
      (consulta) => String(consulta.consulta_id) === String(consultaId)
    );
  }

  function getTratamientosByConsultaId(consultaId) {
    return tratamientosConsulta.filter(
      (item) => String(item.consulta_id) === String(consultaId)
    );
  }

  function getCirugiaByTratamientoConsultaId(tratamientoConsultaId) {
    return cirugias.find(
      (cirugia) =>
        String(cirugia.tratamiento_consulta_id) ===
        String(tratamientoConsultaId)
    );
  }

  function getCirugiasByConsultaId(consultaId) {
    const relatedTreatments = getTratamientosByConsultaId(consultaId);

    return relatedTreatments
      .map((tratamientoConsulta) =>
        getCirugiaByTratamientoConsultaId(
          tratamientoConsulta.tratamiento_consulta_id
        )
      )
      .filter(Boolean);
  }

  function getSelectedConsulta() {
    if (!selectedConsultaId) {
      return null;
    }

    return getConsultaById(selectedConsultaId);
  }

  function getSelectedCita() {
    const selectedConsulta = getSelectedConsulta();

    if (!selectedConsulta) {
      return null;
    }

    return getCitaById(selectedConsulta.cita_id);
  }

  function buildCitaPayload() {
    return {
      paciente_id: Number(form.paciente_id),
      doctor_id: Number(form.doctor_id),
      fecha_hora_inicio: form.fecha_hora_inicio,
      duracion_minutos: Number(form.duracion_minutos),
      estado: form.estado_cita,
      motivo: form.motivo || null
    };
  }

  function buildConsultaPayload(citaId) {
    return {
      cita_id: Number(citaId),
      diagnostico: form.diagnostico,
      observaciones: form.observaciones_consulta || null,
      fecha_atencion: form.fecha_atencion || null
    };
  }

  function buildTratamientoConsultaPayload(consultaId) {
    return {
      consulta_id: Number(consultaId),
      tratamiento_id: Number(form.tratamiento_id),
      cantidad: Number(form.cantidad),
      precio_unitario: Number(form.precio_unitario)
    };
  }

  function buildCirugiaPayload(tratamientoConsultaId) {
    return {
      tratamiento_consulta_id: Number(tratamientoConsultaId),
      doctor_id: Number(form.doctor_id),
      fecha_cirugia: form.fecha_cirugia || null,
      descripcion_quirurgica: form.descripcion_quirurgica || null,
      anestesia: form.anestesia || null,
      observaciones: form.observaciones_cirugia || null,
      estado: form.estado_cirugia || null
    };
  }

  function validateForm() {
    if (!form.paciente_id) {
      throw new Error("Debe seleccionar un paciente.");
    }

    if (!form.doctor_id) {
      throw new Error("Debe seleccionar un doctor.");
    }

    if (!form.fecha_hora_inicio) {
      throw new Error("Debe indicar la fecha y hora de la cita.");
    }

    if (!form.diagnostico.trim()) {
      throw new Error("Debe indicar el diagnóstico de la atención clínica.");
    }

    if (!form.tratamiento_id) {
      throw new Error("Debe seleccionar un tratamiento aplicado.");
    }

    if (!form.cantidad || Number(form.cantidad) <= 0) {
      throw new Error("La cantidad del tratamiento debe ser mayor a cero.");
    }

    if (form.precio_unitario === "" || Number(form.precio_unitario) < 0) {
      throw new Error("Debe indicar un precio unitario válido.");
    }

    if (form.incluye_cirugia) {
      if (!form.descripcion_quirurgica.trim()) {
        throw new Error(
          "Debe indicar la descripción quirúrgica si incluye cirugía."
        );
      }

      if (!form.anestesia.trim()) {
        throw new Error(
          "Debe indicar el tipo de anestesia si incluye cirugía."
        );
      }
    }
  }

  async function cleanupCreatedRecords(createdRecords) {
    try {
      if (createdRecords.cirugiaId) {
        await apiClient.delete(`/cirugias/${createdRecords.cirugiaId}`);
      }

      if (createdRecords.tratamientoConsultaId) {
        await apiClient.delete(
          `/tratamientos-consulta/${createdRecords.tratamientoConsultaId}`
        );
      }

      if (createdRecords.consultaId) {
        await apiClient.delete(`/consultas/${createdRecords.consultaId}`);
      }

      if (createdRecords.citaId) {
        await apiClient.delete(`/citas/${createdRecords.citaId}`);
      }
    } catch {
      // If cleanup fails, the original error is more important for the user.
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const createdRecords = {
      citaId: null,
      consultaId: null,
      tratamientoConsultaId: null,
      cirugiaId: null
    };

    try {
      setLoading(true);
      setMessage("");
      setError("");

      validateForm();

      const createdCita = await apiClient.post("/citas", buildCitaPayload());
      const citaId = createdCita.cita_id || createdCita.id;

      if (!citaId) {
        throw new Error(
          "La cita fue creada, pero el backend no devolvió el ID."
        );
      }

      createdRecords.citaId = citaId;

      const createdConsulta = await apiClient.post(
        "/consultas",
        buildConsultaPayload(citaId)
      );

      const consultaId = createdConsulta.consulta_id || createdConsulta.id;

      if (!consultaId) {
        throw new Error(
          "La consulta fue creada, pero el backend no devolvió el ID."
        );
      }

      createdRecords.consultaId = consultaId;

      const createdTratamientoConsulta = await apiClient.post(
        "/tratamientos-consulta",
        buildTratamientoConsultaPayload(consultaId)
      );

      const tratamientoConsultaId =
        createdTratamientoConsulta.tratamiento_consulta_id ||
        createdTratamientoConsulta.id;

      if (!tratamientoConsultaId) {
        throw new Error(
          "El tratamiento aplicado fue creado, pero el backend no devolvió el ID."
        );
      }

      createdRecords.tratamientoConsultaId = tratamientoConsultaId;

      if (form.incluye_cirugia) {
        const createdCirugia = await apiClient.post(
          "/cirugias",
          buildCirugiaPayload(tratamientoConsultaId)
        );

        const cirugiaId = createdCirugia.cirugia_id || createdCirugia.id;

        if (!cirugiaId) {
          throw new Error(
            "La cirugía fue creada, pero el backend no devolvió el ID."
          );
        }

        createdRecords.cirugiaId = cirugiaId;
      }

      setSelectedConsultaId(String(consultaId));

      resetForm();

      setMessage(
        "Atención clínica creada correctamente con cita, consulta y tratamiento aplicado."
      );

      await loadPageData();
    } catch (err) {
      await cleanupCreatedRecords(createdRecords);

      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDeleteFullAttention(consulta) {
    const confirmed = window.confirm(
      "¿Seguro que desea eliminar esta atención clínica?\n\n" +
        "Se eliminarán en este orden: cirugía, tratamientos aplicados, consulta y cita.\n" +
        "Si ya fue facturada, Oracle puede impedir la eliminación."
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setMessage("");
      setError("");

      const relatedTreatments = getTratamientosByConsultaId(
        consulta.consulta_id
      );

      for (const treatment of relatedTreatments) {
        const relatedSurgery = getCirugiaByTratamientoConsultaId(
          treatment.tratamiento_consulta_id
        );

        if (relatedSurgery) {
          await apiClient.delete(`/cirugias/${relatedSurgery.cirugia_id}`);
        }
      }

      for (const treatment of relatedTreatments) {
        await apiClient.delete(
          `/tratamientos-consulta/${treatment.tratamiento_consulta_id}`
        );
      }

      await apiClient.delete(`/consultas/${consulta.consulta_id}`);

      const cita = getCitaById(consulta.cita_id);

      if (cita) {
        await apiClient.delete(`/citas/${cita.cita_id}`);
      }

      if (String(selectedConsultaId) === String(consulta.consulta_id)) {
        setSelectedConsultaId("");
      }

      setMessage("Atención clínica eliminada correctamente.");

      await loadPageData();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleSelectConsulta(consultaId) {
    setSelectedConsultaId(String(consultaId));
    setMessage("Atención clínica seleccionada.");
    setError("");
  }

  const selectedConsulta = getSelectedConsulta();
  const selectedCita = getSelectedCita();

  const selectedTreatments = selectedConsultaId
    ? getTratamientosByConsultaId(selectedConsultaId)
    : [];

  const selectedSurgeries = selectedConsultaId
    ? getCirugiasByConsultaId(selectedConsultaId)
    : [];

  const selectedTreatmentsTotal = selectedTreatments.reduce(
    (total, item) => total + Number(item.subtotal || 0),
    0
  );

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Atención Clínica</h2>
          <p>
            Registro completo de cita, consulta, tratamiento aplicado y cirugía
            opcional.
          </p>
        </div>
      </div>

      <section className="card">
        <h3>Registrar atención clínica</h3>

        <p className="helper-text">
          Complete todo el proceso clínico en un solo lugar.
        </p>

        {loading && <p>Cargando...</p>}

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}

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
                <option key={doctor.doctor_id} value={doctor.doctor_id}>
                  {doctor.nombre} {doctor.apellido}
                </option>
              ))}
            </select>
          </label>

          <label>
            Fecha y hora de la cita
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
            Estado de la cita
            <select
              name="estado_cita"
              value={form.estado_cita}
              onChange={handleChange}
              required
            >
              <option value="PROGRAMADA">PROGRAMADA</option>
              <option value="CONFIRMADA">CONFIRMADA</option>
              <option value="FINALIZADA">FINALIZADA</option>
              <option value="CANCELADA">CANCELADA</option>
            </select>
          </label>

          <label>
            Fecha de atención
            <input
              type="datetime-local"
              name="fecha_atencion"
              value={form.fecha_atencion}
              onChange={handleChange}
            />
          </label>

          <label>
            Motivo de la cita
            <textarea
              name="motivo"
              value={form.motivo}
              onChange={handleChange}
              rows="3"
              placeholder="Motivo por el cual el paciente solicita atención"
            />
          </label>

          <label>
            Diagnóstico
            <textarea
              name="diagnostico"
              value={form.diagnostico}
              onChange={handleChange}
              rows="3"
              placeholder="Diagnóstico clínico"
              required
            />
          </label>

          <label>
            Observaciones de la consulta
            <textarea
              name="observaciones_consulta"
              value={form.observaciones_consulta}
              onChange={handleChange}
              rows="3"
              placeholder="Observaciones generales"
            />
          </label>

          <label>
            Tratamiento aplicado
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

          <label>
            Incluye cirugía
            <div className="inline-input">
              <input
                type="checkbox"
                name="incluye_cirugia"
                checked={form.incluye_cirugia}
                onChange={handleChange}
              />
              <span>Sí, esta atención incluye cirugía</span>
            </div>
          </label>

          {form.incluye_cirugia && (
            <>
              <label>
                Fecha cirugía
                <input
                  type="datetime-local"
                  name="fecha_cirugia"
                  value={form.fecha_cirugia}
                  onChange={handleChange}
                />
              </label>

              <label>
                Descripción quirúrgica
                <textarea
                  name="descripcion_quirurgica"
                  value={form.descripcion_quirurgica}
                  onChange={handleChange}
                  rows="3"
                  placeholder="Detalle del procedimiento quirúrgico"
                  required={form.incluye_cirugia}
                />
              </label>

              <label>
                Anestesia
                <input
                  type="text"
                  name="anestesia"
                  value={form.anestesia}
                  onChange={handleChange}
                  placeholder="Local, general, sedación, etc."
                  required={form.incluye_cirugia}
                />
              </label>

              <label>
                Estado cirugía
                <select
                  name="estado_cirugia"
                  value={form.estado_cirugia}
                  onChange={handleChange}
                >
                  <option value="PROGRAMADA">PROGRAMADA</option>
                  <option value="REALIZADA">REALIZADA</option>
                  <option value="CANCELADA">CANCELADA</option>
                  <option value="EN_SEGUIMIENTO">EN_SEGUIMIENTO</option>
                </select>
              </label>

              <label>
                Observaciones cirugía
                <textarea
                  name="observaciones_cirugia"
                  value={form.observaciones_cirugia}
                  onChange={handleChange}
                  rows="3"
                  placeholder="Observaciones específicas de la cirugía"
                />
              </label>
            </>
          )}

          <div className="form-actions">
            <button type="submit" disabled={loading}>
              Guardar atención clínica
            </button>

            <button
              type="button"
              className="secondary-button"
              onClick={resetForm}
              disabled={loading}
            >
              Limpiar
            </button>
          </div>
        </form>
      </section>

      <section className="card">
        <h3>Atenciones clínicas registradas</h3>

        <p className="helper-text">
          Cada registro muestra la cita, la consulta, sus tratamientos aplicados
          y si incluye cirugía.
        </p>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Consulta</th>
                <th>Cita</th>
                <th>Paciente</th>
                <th>Doctor</th>
                <th>Fecha cita</th>
                <th>Estado</th>
                <th>Diagnóstico</th>
                <th>Tratamientos</th>
                <th>Cirugías</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {consultas.map((consulta) => {
                const cita = getCitaById(consulta.cita_id);
                const relatedTreatments = getTratamientosByConsultaId(
                  consulta.consulta_id
                );
                const relatedSurgeries = getCirugiasByConsultaId(
                  consulta.consulta_id
                );

                return (
                  <tr key={consulta.consulta_id}>
                    <td>{consulta.consulta_id}</td>
                    <td>{consulta.cita_id}</td>
                    <td>
                      {consulta.paciente_nombre ||
                        cita?.paciente_nombre ||
                        getPacienteName(cita?.paciente_id)}
                    </td>
                    <td>
                      {consulta.doctor_nombre ||
                        cita?.doctor_nombre ||
                        getDoctorName(cita?.doctor_id)}
                    </td>
                    <td>{formatDateTime(cita?.fecha_hora_inicio)}</td>
                    <td>{cita?.estado || ""}</td>
                    <td>{consulta.diagnostico}</td>
                    <td>{relatedTreatments.length}</td>
                    <td>{relatedSurgeries.length}</td>
                    <td>
                      <button
                        type="button"
                        className="small-button"
                        onClick={() =>
                          handleSelectConsulta(consulta.consulta_id)
                        }
                      >
                        Ver detalle
                      </button>

                      <button
                        type="button"
                        className="danger-button"
                        onClick={() => handleDeleteFullAttention(consulta)}
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                );
              })}

              {consultas.length === 0 && !loading && (
                <tr>
                  <td colSpan="10">
                    No hay atenciones clínicas registradas.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <h3>Detalle de atención seleccionada</h3>

        {!selectedConsulta && (
          <p className="helper-text">
            Seleccione una atención clínica para revisar sus tratamientos y
            cirugías.
          </p>
        )}

        {selectedConsulta && (
          <>
            <div className="clinical-summary">
              <p>
                <strong>Consulta:</strong> {selectedConsulta.consulta_id}
              </p>

              <p>
                <strong>Cita:</strong> {selectedConsulta.cita_id}
              </p>

              <p>
                <strong>Paciente:</strong>{" "}
                {selectedConsulta.paciente_nombre ||
                  selectedCita?.paciente_nombre ||
                  getPacienteName(selectedCita?.paciente_id)}
              </p>

              <p>
                <strong>Doctor:</strong>{" "}
                {selectedConsulta.doctor_nombre ||
                  selectedCita?.doctor_nombre ||
                  getDoctorName(selectedCita?.doctor_id)}
              </p>

              <p>
                <strong>Fecha cita:</strong>{" "}
                {formatDateTime(selectedCita?.fecha_hora_inicio)}
              </p>

              <p>
                <strong>Diagnóstico:</strong> {selectedConsulta.diagnostico}
              </p>

              <p>
                <strong>Total tratamientos:</strong> ₡
                {selectedTreatmentsTotal.toFixed(2)}
              </p>
            </div>

            <h4>Tratamientos aplicados</h4>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Tratamiento</th>
                    <th>Cantidad</th>
                    <th>Precio unitario</th>
                    <th>Subtotal</th>
                  </tr>
                </thead>

                <tbody>
                  {selectedTreatments.map((item) => (
                    <tr key={item.tratamiento_consulta_id}>
                      <td>{item.tratamiento_consulta_id}</td>
                      <td>
                        {item.tratamiento_nombre ||
                          item.nombre_tratamiento ||
                          getTratamientoName(item.tratamiento_id)}
                      </td>
                      <td>{item.cantidad}</td>
                      <td>₡{item.precio_unitario}</td>
                      <td>₡{item.subtotal}</td>
                    </tr>
                  ))}

                  {selectedTreatments.length === 0 && (
                    <tr>
                      <td colSpan="5">
                        Esta atención no tiene tratamientos aplicados.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            <h4>Cirugías</h4>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Tratamiento</th>
                    <th>Fecha</th>
                    <th>Anestesia</th>
                    <th>Estado</th>
                    <th>Descripción</th>
                  </tr>
                </thead>

                <tbody>
                  {selectedSurgeries.map((cirugia) => (
                    <tr key={cirugia.cirugia_id}>
                      <td>{cirugia.cirugia_id}</td>
                      <td>{cirugia.tratamiento_nombre}</td>
                      <td>{formatDateTime(cirugia.fecha_cirugia)}</td>
                      <td>{cirugia.anestesia}</td>
                      <td>{cirugia.estado}</td>
                      <td>{cirugia.descripcion_quirurgica}</td>
                    </tr>
                  ))}

                  {selectedSurgeries.length === 0 && (
                    <tr>
                      <td colSpan="6">
                        Esta atención no tiene cirugía registrada.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </>
        )}
      </section>
    </section>
  );
}

export default AtencionClinica;