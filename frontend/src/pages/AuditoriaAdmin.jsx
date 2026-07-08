import {
  useEffect,
  useState
} from "react";

import {
  apiClient
} from "../api/apiClient.js";


const initialFilters = {
  fecha_desde: "",
  fecha_hasta: "",
  usuario: "",
  modulo: "",
  accion: "",
  resultado: ""
};


const initialData = {
  resumen: {
    login_exitosos: 0,
    login_fallidos: 0,
    logouts: 0,
    cambios_exitosos: 0,
    accesos_denegados: 0,
    eventos_triggers: 0
  },

  auditoria_sistema: [],
  historial_accesos: [],
  auditoria_triggers: []
};


function AuditoriaAdmin() {
  const [filters, setFilters] =
    useState(initialFilters);

  const [data, setData] =
    useState(initialData);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  async function loadDashboard(
    filtersToUse = filters
  ) {
    try {
      setLoading(true);
      setError("");


      const params =
        new URLSearchParams();


      Object.entries(
        filtersToUse
      ).forEach(
        ([key, value]) => {
          if (
            value !== null &&
            value !== undefined &&
            String(value).trim() !== ""
          ) {
            params.set(
              key,
              value
            );
          }
        }
      );


      params.set(
        "limite",
        "500"
      );


      const response =
        await apiClient.get(
          `/admin/auditoria/dashboard?${params.toString()}`
        );


      setData(response);

    } catch (err) {
      setError(err.message);

    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadDashboard(
      initialFilters
    );
  }, []);


  function handleFilterChange(
    event
  ) {
    const {
      name,
      value
    } = event.target;


    setFilters(
      (currentFilters) => ({
        ...currentFilters,
        [name]: value
      })
    );
  }


  async function handleSearch(
    event
  ) {
    event.preventDefault();

    await loadDashboard(
      filters
    );
  }


  async function handleClear() {
    setFilters(
      initialFilters
    );

    await loadDashboard(
      initialFilters
    );
  }


  function formatDateTime(
    value
  ) {
    if (!value) {
      return "";
    }


    const date =
      new Date(value);


    if (
      Number.isNaN(
        date.getTime()
      )
    ) {
      return String(value);
    }


    return date.toLocaleString(
      "es-CR"
    );
  }


  function getResultBadgeClass(
    result
  ) {
    const normalized =
      String(
        result || ""
      ).toUpperCase();


    if (
      normalized === "EXITOSO"
    ) {
      return (
        "badge success-badge"
      );
    }


    if (
      normalized === "DENEGADO"
    ) {
      return (
        "badge warning-badge"
      );
    }


    return "badge danger-badge";
  }


  function escapeCsv(
    value
  ) {
    const text =
      value === null ||
      value === undefined
        ? ""
        : String(value);


    return (
      `"${text.replaceAll(
        '"',
        '""'
      )}"`
    );
  }


  function downloadContent(
    filename,
    content,
    mimeType
  ) {
    const blob =
      new Blob(
        [content],
        {
          type: mimeType
        }
      );


    const url =
      URL.createObjectURL(
        blob
      );


    const link =
      document.createElement(
        "a"
      );


    link.href = url;

    link.download =
      filename;


    document.body.appendChild(
      link
    );

    link.click();

    link.remove();


    URL.revokeObjectURL(
      url
    );
  }


  function exportCsv(
    rows,
    columns,
    filename
  ) {
    if (rows.length === 0) {
      return;
    }


    const header =
      columns
        .map((column) =>
          escapeCsv(column.label)
        )
        .join(",");


    const body =
      rows
        .map((row) =>
          columns
            .map((column) => {
              const value =
                column.format
                  ? column.format(
                      row[column.key]
                    )
                  : row[column.key];

              return escapeCsv(
                value
              );
            })
            .join(",")
        )
        .join("\n");


    downloadContent(
      filename,
      `\uFEFF${header}\n${body}`,
      "text/csv;charset=utf-8"
    );
  }


  function exportTxt(
    rows,
    columns,
    filename,
    title
  ) {
    if (rows.length === 0) {
      return;
    }


    const separator =
      "=".repeat(70);


    const records =
      rows.map(
        (row, index) => {
          const lines = [
            `Registro ${index + 1}`,
            "-".repeat(70)
          ];


          columns.forEach(
            (column) => {
              const value =
                column.format
                  ? column.format(
                      row[column.key]
                    )
                  : row[column.key];


              lines.push(
                `${column.label}: ${
                  value ?? ""
                }`
              );
            }
          );


          return lines.join(
            "\n"
          );
        }
      );


    const content = [
      title,
      separator,
      "",
      ...records.map(
        (record) =>
          `${record}\n${separator}\n`
      )
    ].join("\n");


    downloadContent(
      filename,
      content,
      "text/plain;charset=utf-8"
    );
  }


  const systemColumns = [
    {
      key: "fecha_accion",
      label: "Fecha",
      format: formatDateTime
    },
    {
      key: "nombre_usuario",
      label: "Usuario"
    },
    {
      key: "nombre_rol",
      label: "Rol"
    },
    {
      key: "modulo",
      label: "Módulo"
    },
    {
      key: "entidad",
      label: "Entidad"
    },
    {
      key: "accion",
      label: "Acción"
    },
    {
      key: "metodo_http",
      label: "Método HTTP"
    },
    {
      key: "ruta",
      label: "Ruta"
    },
    {
      key: "valor_llave",
      label: "Registro"
    },
    {
      key: "resultado",
      label: "Resultado"
    },
    {
      key: "status_code",
      label: "HTTP"
    },
    {
      key: "ip_origen",
      label: "IP"
    }
  ];


  const accessColumns = [
    {
      key: "fecha_evento",
      label: "Fecha",
      format: formatDateTime
    },
    {
      key: "nombre_usuario",
      label: "Usuario"
    },
    {
      key: "nombre_rol",
      label: "Rol"
    },
    {
      key: "evento",
      label: "Evento"
    },
    {
      key: "resultado",
      label: "Resultado"
    },
    {
      key: "detalle",
      label: "Detalle"
    },
    {
      key: "ip_origen",
      label: "IP"
    }
  ];


  const triggerColumns = [
    {
      key: "fecha_accion",
      label: "Fecha",
      format: formatDateTime
    },
    {
      key: "nombre_tabla",
      label: "Tabla"
    },
    {
      key: "accion",
      label: "Acción"
    },
    {
      key: "valor_llave",
      label: "Registro"
    },
    {
      key: "usuario_bd",
      label: "Usuario Oracle"
    },
    {
      key: "detalle",
      label: "Detalle"
    }
  ];


  return (
    <section>
      <div className="page-header">
        <div>
          <h2>
            Auditoría y accesos
          </h2>

          <p>
            Historial administrativo de
            accesos, cambios del sistema y
            eventos registrados por triggers
            Oracle.
          </p>
        </div>
      </div>


      <section className="dashboard-grid">
        <article className="dashboard-card">
          <h3>
            Inicios exitosos
          </h3>

          <p>
            {
              data.resumen
                .login_exitosos
            }
          </p>
        </article>


        <article className="dashboard-card">
          <h3>
            Intentos fallidos
          </h3>

          <p>
            {
              data.resumen
                .login_fallidos
            }
          </p>
        </article>


        <article className="dashboard-card">
          <h3>
            Cierres de sesión
          </h3>

          <p>
            {
              data.resumen
                .logouts
            }
          </p>
        </article>


        <article className="dashboard-card">
          <h3>
            Cambios exitosos
          </h3>

          <p>
            {
              data.resumen
                .cambios_exitosos
            }
          </p>
        </article>


        <article className="dashboard-card">
          <h3>
            Accesos denegados
          </h3>

          <p>
            {
              data.resumen
                .accesos_denegados
            }
          </p>
        </article>


        <article className="dashboard-card">
          <h3>
            Eventos de triggers
          </h3>

          <p>
            {
              data.resumen
                .eventos_triggers
            }
          </p>
        </article>
      </section>


      <section className="card">
        <h3>
          Filtros
        </h3>


        <form
          className="form-grid"
          onSubmit={handleSearch}
        >
          <label>
            Fecha desde

            <input
              type="date"
              name="fecha_desde"
              value={
                filters.fecha_desde
              }
              onChange={
                handleFilterChange
              }
            />
          </label>


          <label>
            Fecha hasta

            <input
              type="date"
              name="fecha_hasta"
              value={
                filters.fecha_hasta
              }
              onChange={
                handleFilterChange
              }
            />
          </label>


          <label>
            Usuario

            <input
              type="text"
              name="usuario"
              value={
                filters.usuario
              }
              onChange={
                handleFilterChange
              }
              placeholder="admin, doctor.demo..."
            />
          </label>


          <label>
            Módulo

            <select
              name="modulo"
              value={
                filters.modulo
              }
              onChange={
                handleFilterChange
              }
            >
              <option value="">
                Todos
              </option>

              <option value="CLINICA">
                CLINICA
              </option>

              <option value="TRATAMIENTOS">
                TRATAMIENTOS
              </option>

              <option value="FINANZAS">
                FINANZAS
              </option>

              <option value="INVENTARIO">
                INVENTARIO
              </option>

              <option value="ADMINISTRACION">
                ADMINISTRACION
              </option>

              <option value="SISTEMA">
                SISTEMA
              </option>
            </select>
          </label>


          <label>
            Acción / evento

            <input
              type="text"
              name="accion"
              value={
                filters.accion
              }
              onChange={
                handleFilterChange
              }
              placeholder="ACTUALIZAR, LOGIN_FAILED..."
            />
          </label>


          <label>
            Resultado

            <select
              name="resultado"
              value={
                filters.resultado
              }
              onChange={
                handleFilterChange
              }
            >
              <option value="">
                Todos
              </option>

              <option value="EXITOSO">
                EXITOSO
              </option>

              <option value="FALLIDO">
                FALLIDO
              </option>

              <option value="DENEGADO">
                DENEGADO
              </option>
            </select>
          </label>


          <div className="form-actions">
            <button
              type="submit"
              disabled={loading}
            >
              Buscar
            </button>


            <button
              type="button"
              className="secondary-button"
              onClick={handleClear}
              disabled={loading}
            >
              Limpiar filtros
            </button>
          </div>
        </form>


        {loading && (
          <p>
            Cargando auditoría...
          </p>
        )}


        {error && (
          <p className="error-message">
            {error}
          </p>
        )}
      </section>


      <section className="card">
        <div className="page-header">
          <div>
            <h3>
              Actividad del sistema
            </h3>

            <p className="helper-text">
              Operaciones y accesos
              registrados por la aplicación.
            </p>
          </div>


          <div className="form-actions">
            <button
              type="button"
              className="secondary-button"
              disabled={
                data
                  .auditoria_sistema
                  .length === 0
              }
              onClick={() =>
                exportCsv(
                  data.auditoria_sistema,
                  systemColumns,
                  "auditoria_sistema.csv"
                )
              }
            >
              Exportar CSV
            </button>


            <button
              type="button"
              className="secondary-button"
              disabled={
                data
                  .auditoria_sistema
                  .length === 0
              }
              onClick={() =>
                exportTxt(
                  data.auditoria_sistema,
                  systemColumns,
                  "auditoria_sistema.txt",
                  "AUDITORÍA DEL SISTEMA"
                )
              }
            >
              Exportar TXT
            </button>
          </div>
        </div>


        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Usuario</th>
                <th>Rol</th>
                <th>Módulo</th>
                <th>Entidad</th>
                <th>Acción</th>
                <th>Resultado</th>
                <th>HTTP</th>
                <th>Ruta</th>
                <th>Registro</th>
              </tr>
            </thead>

            <tbody>
              {data.auditoria_sistema.map(
                (item) => (
                  <tr
                    key={
                      item
                        .auditoria_sistema_id
                    }
                  >
                    <td>
                      {formatDateTime(
                        item.fecha_accion
                      )}
                    </td>

                    <td>
                      {item.nombre_usuario ||
                        "Sin identificar"}
                    </td>

                    <td>
                      {item.nombre_rol || ""}
                    </td>

                    <td>
                      {item.modulo}
                    </td>

                    <td>
                      {item.entidad}
                    </td>

                    <td>
                      {item.accion}
                    </td>

                    <td>
                      <span
                        className={
                          getResultBadgeClass(
                            item.resultado
                          )
                        }
                      >
                        {item.resultado}
                      </span>
                    </td>

                    <td>
                      {item.status_code}
                    </td>

                    <td>
                      {item.ruta}
                    </td>

                    <td>
                      {item.valor_llave ||
                        ""}
                    </td>
                  </tr>
                )
              )}


              {data
                .auditoria_sistema
                .length === 0 &&
                !loading && (
                  <tr>
                    <td colSpan="10">
                      No hay registros.
                    </td>
                  </tr>
                )}
            </tbody>
          </table>
        </div>
      </section>


      <section className="card">
        <div className="page-header">
          <div>
            <h3>
              Historial de accesos
            </h3>

            <p className="helper-text">
              Inicios, fallos y cierres
              de sesión.
            </p>
          </div>


          <div className="form-actions">
            <button
              type="button"
              className="secondary-button"
              disabled={
                data
                  .historial_accesos
                  .length === 0
              }
              onClick={() =>
                exportCsv(
                  data.historial_accesos,
                  accessColumns,
                  "historial_accesos.csv"
                )
              }
            >
              Exportar CSV
            </button>


            <button
              type="button"
              className="secondary-button"
              disabled={
                data
                  .historial_accesos
                  .length === 0
              }
              onClick={() =>
                exportTxt(
                  data.historial_accesos,
                  accessColumns,
                  "historial_accesos.txt",
                  "HISTORIAL DE ACCESOS"
                )
              }
            >
              Exportar TXT
            </button>
          </div>
        </div>


        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Usuario</th>
                <th>Rol</th>
                <th>Evento</th>
                <th>Resultado</th>
                <th>IP</th>
                <th>Detalle</th>
              </tr>
            </thead>

            <tbody>
              {data.historial_accesos.map(
                (item) => (
                  <tr
                    key={item.acceso_id}
                  >
                    <td>
                      {formatDateTime(
                        item.fecha_evento
                      )}
                    </td>

                    <td>
                      {item.nombre_usuario ||
                        "No identificado"}
                    </td>

                    <td>
                      {item.nombre_rol || ""}
                    </td>

                    <td>
                      {item.evento}
                    </td>

                    <td>
                      <span
                        className={
                          getResultBadgeClass(
                            item.resultado
                          )
                        }
                      >
                        {item.resultado}
                      </span>
                    </td>

                    <td>
                      {item.ip_origen || ""}
                    </td>

                    <td>
                      {item.detalle || ""}
                    </td>
                  </tr>
                )
              )}


              {data
                .historial_accesos
                .length === 0 &&
                !loading && (
                  <tr>
                    <td colSpan="7">
                      No hay registros.
                    </td>
                  </tr>
                )}
            </tbody>
          </table>
        </div>
      </section>


      <section className="card">
        <div className="page-header">
          <div>
            <h3>
              Eventos de triggers Oracle
            </h3>

            <p className="helper-text">
              Auditoría generada directamente
              por los triggers de la base
              de datos.
            </p>
          </div>


          <div className="form-actions">
            <button
              type="button"
              className="secondary-button"
              disabled={
                data
                  .auditoria_triggers
                  .length === 0
              }
              onClick={() =>
                exportCsv(
                  data.auditoria_triggers,
                  triggerColumns,
                  "auditoria_triggers.csv"
                )
              }
            >
              Exportar CSV
            </button>


            <button
              type="button"
              className="secondary-button"
              disabled={
                data
                  .auditoria_triggers
                  .length === 0
              }
              onClick={() =>
                exportTxt(
                  data.auditoria_triggers,
                  triggerColumns,
                  "auditoria_triggers.txt",
                  "AUDITORÍA DE TRIGGERS ORACLE"
                )
              }
            >
              Exportar TXT
            </button>
          </div>
        </div>


        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Tabla</th>
                <th>Acción</th>
                <th>Registro</th>
                <th>Usuario Oracle</th>
                <th>Detalle</th>
              </tr>
            </thead>

            <tbody>
              {data.auditoria_triggers.map(
                (item) => (
                  <tr
                    key={
                      item.auditoria_id
                    }
                  >
                    <td>
                      {formatDateTime(
                        item.fecha_accion
                      )}
                    </td>

                    <td>
                      {item.nombre_tabla}
                    </td>

                    <td>
                      {item.accion}
                    </td>

                    <td>
                      {item.valor_llave || ""}
                    </td>

                    <td>
                      {item.usuario_bd}
                    </td>

                    <td>
                      {item.detalle || ""}
                    </td>
                  </tr>
                )
              )}


              {data
                .auditoria_triggers
                .length === 0 &&
                !loading && (
                  <tr>
                    <td colSpan="6">
                      No hay registros.
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


export default AuditoriaAdmin;