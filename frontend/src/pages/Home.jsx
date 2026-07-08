import {
  useEffect,
  useState
} from "react";

import {
  Link
} from "react-router-dom";

import {
  apiClient
} from "../api/apiClient.js";

import {
  useAuth
} from "../auth/AuthContext.jsx";


const initialStats = {
  pacientes: 0,
  doctores: 0,
  atenciones: 0,
  facturas: 0,
  pagos: 0,
  compras: 0,
  productosStock: 0,
  stockBajo: 0
};


function Home() {
  const {
    user,
    hasPermission,
    hasAnyPermission
  } = useAuth();


  const [stats, setStats] =
    useState(initialStats);

  const [
    recentFacturas,
    setRecentFacturas
  ] = useState([]);

  const [
    recentPagos,
    setRecentPagos
  ] = useState([]);

  const [
    recentCompras,
    setRecentCompras
  ] = useState([]);

  const [
    lowStockItems,
    setLowStockItems
  ] = useState([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  const canViewPatients =
    hasAnyPermission(
      "PACIENTES_VER",
      "PACIENTES_GESTIONAR"
    );

  const canManageDoctors =
    hasPermission(
      "DOCTORES_GESTIONAR"
    );

  const canUseAgenda =
    hasAnyPermission(
      "AGENDA_GESTIONAR",
      "CITAS_GESTIONAR"
    );

  const canRegisterClinicalAttention =
    hasPermission(
      "CONSULTAS_GESTIONAR"
    );

  const canUseClinicalRecord =
    hasPermission(
      "EXPEDIENTE_GESTIONAR"
    );

  const canManageTreatments =
    hasPermission(
      "TRATAMIENTOS_GESTIONAR"
    );

  const canUseCashier =
    hasPermission(
      "CAJA_USAR"
    );

  const canViewInvoices =
    hasAnyPermission(
      "FACTURAS_VER",
      "CAJA_USAR"
    );

  const canManagePaymentMethods =
    hasPermission(
      "METODOS_PAGO_GESTIONAR"
    );

  const canViewPayments =
    hasAnyPermission(
      "PAGOS_VER",
      "CAJA_USAR"
    );

  const canManageSuppliers =
    hasPermission(
      "PROVEEDORES_GESTIONAR"
    );

  const canManagePurchases =
    hasPermission(
      "COMPRAS_GESTIONAR"
    );

  const canViewInventory =
    hasAnyPermission(
      "INVENTARIO_VER",
      "INVENTARIO_GESTIONAR"
    );


  const canViewClinicalWorkflow =
    canViewPatients ||
    canUseAgenda ||
    canRegisterClinicalAttention ||
    canUseClinicalRecord ||
    canUseCashier;


  const canViewInventoryWorkflow =
    canManageSuppliers ||
    canManagePurchases ||
    canViewInventory;


  async function loadDashboardData() {
    try {
      setLoading(true);
      setError("");


      const requestDefinitions = [
        {
          key: "pacientes",
          endpoint: "/pacientes",
          enabled: canViewPatients
        },
        {
          key: "doctores",
          endpoint: "/doctores",
          enabled: canManageDoctors
        },
        {
          key: "consultas",
          endpoint: "/consultas",
          enabled:
            canRegisterClinicalAttention
        },
        {
          key: "facturas",
          endpoint: "/facturas",
          enabled: canViewInvoices
        },
        {
          key: "pagos",
          endpoint: "/pagos",
          enabled: canViewPayments
        },
        {
          key: "compras",
          endpoint: "/compras",
          enabled: canManagePurchases
        },
        {
          key: "inventarioStock",
          endpoint: "/inventario-stock",
          enabled: canViewInventory
        }
      ].filter(
        (requestDefinition) =>
          requestDefinition.enabled
      );


      const results =
        await Promise.allSettled(
          requestDefinitions.map(
            (requestDefinition) =>
              apiClient.get(
                requestDefinition.endpoint
              )
          )
        );


      const dashboardData = {};

      const errors = [];


      results.forEach(
        (result, index) => {
          const requestDefinition =
            requestDefinitions[index];

          if (
            result.status ===
            "fulfilled"
          ) {
            dashboardData[
              requestDefinition.key
            ] = result.value;
          } else {
            errors.push(
              result.reason?.message ||
              "No se pudo cargar una sección."
            );
          }
        }
      );


      const pacientes =
        dashboardData.pacientes || [];

      const doctores =
        dashboardData.doctores || [];

      const consultas =
        dashboardData.consultas || [];

      const facturas =
        dashboardData.facturas || [];

      const pagos =
        dashboardData.pagos || [];

      const compras =
        dashboardData.compras || [];

      const inventarioStock =
        dashboardData.inventarioStock ||
        [];


      const lowStock =
        inventarioStock.filter(
          (item) => {
            if (
              item.stock_minimo === null ||
              item.stock_minimo ===
                undefined
            ) {
              return false;
            }

            return (
              Number(item.stock_actual) <=
              Number(item.stock_minimo)
            );
          }
        );


      setStats({
        pacientes: pacientes.length,
        doctores: doctores.length,
        atenciones: consultas.length,
        facturas: facturas.length,
        pagos: pagos.length,
        compras: compras.length,
        productosStock:
          inventarioStock.length,
        stockBajo: lowStock.length
      });


      setRecentFacturas(
        [...facturas]
          .sort(
            (first, second) =>
              Number(second.factura_id) -
              Number(first.factura_id)
          )
          .slice(0, 5)
      );


      setRecentPagos(
        [...pagos]
          .sort(
            (first, second) =>
              Number(second.pago_id) -
              Number(first.pago_id)
          )
          .slice(0, 5)
      );


      setRecentCompras(
        [...compras]
          .sort(
            (first, second) =>
              Number(second.compra_id) -
              Number(first.compra_id)
          )
          .slice(0, 5)
      );


      setLowStockItems(
        [...lowStock].slice(0, 5)
      );


      if (errors.length > 0) {
        const uniqueErrors = [
          ...new Set(errors)
        ];

        setError(
          "Algunos datos del panel no se pudieron cargar: " +
          uniqueErrors.join(" ")
        );
      }

    } catch (err) {
      setError(err.message);

    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadDashboardData();
  }, [user]);


  function getStatusBadgeClass(
    status
  ) {
    const normalizedStatus =
      String(
        status || ""
      ).toUpperCase();


    if (
      normalizedStatus === "PAGADA" ||
      normalizedStatus === "APLICADO" ||
      normalizedStatus === "ACTIVO" ||
      normalizedStatus === "RECIBIDA" ||
      normalizedStatus === "COMPLETADA"
    ) {
      return "badge success-badge";
    }


    if (
      normalizedStatus === "ANULADA" ||
      normalizedStatus === "ANULADO" ||
      normalizedStatus === "CANCELADA" ||
      normalizedStatus === "INACTIVO"
    ) {
      return "badge danger-badge";
    }


    return "badge warning-badge";
  }


  function formatCurrency(value) {
    return new Intl.NumberFormat(
      "es-CR",
      {
        style: "currency",
        currency: "CRC",
        maximumFractionDigits: 2
      }
    ).format(
      Number(value || 0)
    );
  }


  function formatDate(value) {
    if (!value) {
      return "";
    }

    return String(value).substring(
      0,
      10
    );
  }


  function getStockItemName(item) {
    const code =
      item.insumo_codigo ||
      item.codigo;

    const name =
      item.insumo_nombre ||
      item.nombre;


    if (code && name) {
      return `${code} - ${name}`;
    }


    return (
      name ||
      `Insumo ${item.insumo_id}`
    );
  }


  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Sistema SmileCare</h2>

          <p>
            Bienvenido,{" "}
            <strong>
              {user?.nombre_usuario}
            </strong>
            {" · "}
            {user?.nombre_rol}
          </p>
        </div>
      </div>


      {loading && (
        <section className="card">
          <p>
            Cargando información del sistema...
          </p>
        </section>
      )}


      {error && (
        <section className="card">
          <p className="error-message">
            {error}
          </p>
        </section>
      )}


      <section className="dashboard-grid">
        {canViewPatients && (
          <article className="dashboard-card">
            <h3>Pacientes</h3>

            <p>{stats.pacientes}</p>

            <Link to="/pacientes">
              Ver pacientes
            </Link>
          </article>
        )}


        {canManageDoctors && (
          <article className="dashboard-card">
            <h3>Doctores</h3>

            <p>{stats.doctores}</p>

            <Link to="/doctores">
              Ver doctores
            </Link>
          </article>
        )}


        {canRegisterClinicalAttention && (
          <article className="dashboard-card">
            <h3>
              Atenciones clínicas
            </h3>

            <p>{stats.atenciones}</p>

            <Link to="/atencion-clinica">
              Registrar atención
            </Link>
          </article>
        )}


        {canViewInvoices && (
          <article className="dashboard-card">
            <h3>Facturas</h3>

            <p>{stats.facturas}</p>

            <Link to="/facturas">
              Ver facturas
            </Link>
          </article>
        )}


        {canViewPayments && (
          <article className="dashboard-card">
            <h3>Pagos</h3>

            <p>{stats.pagos}</p>

            <Link to="/pagos">
              Ver pagos
            </Link>
          </article>
        )}


        {canManagePurchases && (
          <article className="dashboard-card">
            <h3>
              Compras recibidas
            </h3>

            <p>{stats.compras}</p>

            <Link to="/compras">
              Ver compras
            </Link>
          </article>
        )}


        {canViewInventory && (
          <>
            <article className="dashboard-card">
              <h3>
                Productos en stock
              </h3>

              <p>
                {stats.productosStock}
              </p>

              <Link to="/inventario-stock">
                Ver inventario
              </Link>
            </article>

            <article className="dashboard-card">
              <h3>Stock bajo</h3>

              <p>{stats.stockBajo}</p>

              <Link to="/inventario-stock">
                Revisar existencias
              </Link>
            </article>
          </>
        )}
      </section>


      <section className="card">
        <h3>Acciones rápidas</h3>

        <p className="helper-text">
          Accesos directos disponibles
          para su perfil.
        </p>

        <div className="quick-actions">
          {canRegisterClinicalAttention && (
            <Link to="/atencion-clinica">
              Registrar atención clínica
            </Link>
          )}

          {canUseCashier && (
            <Link to="/caja">
              Cobrar en Caja
            </Link>
          )}

          {canManagePurchases && (
            <Link to="/compras">
              Registrar compra e insumos
            </Link>
          )}

          {canViewInventory && (
            <Link to="/inventario-stock">
              Revisar Stock
            </Link>
          )}

          {canUseClinicalRecord && (
            <Link to="/expediente-clinico">
              Consultar expediente clínico
            </Link>
          )}

          {canUseAgenda && (
            <Link to="/agenda-medica">
              Gestionar agenda médica
            </Link>
          )}

          {canViewPatients && (
            <Link to="/pacientes">
              Gestionar pacientes
            </Link>
          )}

          {canManageSuppliers && (
            <Link to="/proveedores">
              Gestionar proveedores
            </Link>
          )}
        </div>
      </section>


      {canViewClinicalWorkflow && (
        <section className="card">
          <h3>Flujo clínico principal</h3>

          <p className="helper-text">
            Procesos disponibles según los
            permisos del usuario.
          </p>

          <div className="workflow-grid">
            {canViewPatients && (
              <div>
                <strong>
                  Pacientes
                </strong>

                <p>
                  Registro y consulta de los
                  pacientes de la clínica.
                </p>
              </div>
            )}

            {canUseAgenda && (
              <div>
                <strong>
                  Agenda médica
                </strong>

                <p>
                  Gestión de horarios,
                  disponibilidad y citas.
                </p>
              </div>
            )}

            {canRegisterClinicalAttention && (
              <div>
                <strong>
                  Atención clínica
                </strong>

                <p>
                  Registro de cita, consulta
                  y tratamientos aplicados.
                </p>
              </div>
            )}

            {canRegisterClinicalAttention && (
              <div>
                <strong>
                  Cirugía opcional
                </strong>

                <p>
                  Registro de cirugías cuando
                  corresponden a la atención.
                </p>
              </div>
            )}

            {canUseClinicalRecord && (
              <div>
                <strong>
                  Expediente clínico
                </strong>

                <p>
                  Consulta del historial
                  completo del paciente.
                </p>
              </div>
            )}

            {canUseCashier && (
              <div>
                <strong>Caja</strong>

                <p>
                  Facturación, pagos y
                  comprobantes.
                </p>
              </div>
            )}
          </div>
        </section>
      )}


      {canViewInventoryWorkflow && (
        <section className="card">
          <h3>
            Flujo de compras e inventario
          </h3>

          <p className="helper-text">
            Procesos de abastecimiento y
            control de existencias.
          </p>

          <div className="workflow-grid">
            {canManageSuppliers && (
              <div>
                <strong>
                  Proveedores
                </strong>

                <p>
                  Gestión de las empresas
                  proveedoras.
                </p>
              </div>
            )}

            {canManagePurchases && (
              <>
                <div>
                  <strong>
                    Compra recibida
                  </strong>

                  <p>
                    Registro de la recepción
                    de productos.
                  </p>
                </div>

                <div>
                  <strong>
                    Productos
                  </strong>

                  <p>
                    Selección de productos
                    existentes o creación
                    de nuevos insumos.
                  </p>
                </div>

                <div>
                  <strong>
                    Cantidad y costo
                  </strong>

                  <p>
                    Registro de cantidades
                    y costos de compra.
                  </p>
                </div>

                <div>
                  <strong>
                    Entrada automática
                  </strong>

                  <p>
                    Actualización automática
                    del stock al recibir
                    una compra.
                  </p>
                </div>
              </>
            )}

            {canViewInventory && (
              <div>
                <strong>
                  Control de stock
                </strong>

                <p>
                  Consulta de existencias,
                  mínimos y movimientos.
                </p>
              </div>
            )}
          </div>
        </section>
      )}


      {canViewInventory &&
        lowStockItems.length > 0 && (
        <section className="card">
          <h3>Alertas de stock</h3>

          <p className="helper-text">
            Productos en el nivel mínimo
            o por debajo del mínimo.
          </p>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Producto</th>
                  <th>Stock actual</th>
                  <th>Stock mínimo</th>
                  <th>Estado</th>
                </tr>
              </thead>

              <tbody>
                {lowStockItems.map(
                  (item) => (
                    <tr key={item.stock_id}>
                      <td>
                        {getStockItemName(
                          item
                        )}
                      </td>

                      <td>
                        {item.stock_actual}
                      </td>

                      <td>
                        {item.stock_minimo}
                      </td>

                      <td>
                        <span className="badge danger-badge">
                          Reabastecer
                        </span>
                      </td>
                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>
        </section>
      )}


      {canManagePurchases && (
        <section className="card">
          <h3>
            Últimas compras recibidas
          </h3>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Proveedor</th>
                  <th>Responsable</th>
                  <th>Fecha</th>
                  <th>Total</th>
                  <th>Estado</th>
                </tr>
              </thead>

              <tbody>
                {recentCompras.map(
                  (compra) => (
                    <tr
                      key={compra.compra_id}
                    >
                      <td>
                        {compra.compra_id}
                      </td>

                      <td>
                        {compra.proveedor_nombre ||
                          compra.proveedor_id}
                      </td>

                      <td>
                        {compra.nombre_usuario ||
                          compra.usuario_id}
                      </td>

                      <td>
                        {formatDate(
                          compra.fecha_compra
                        )}
                      </td>

                      <td>
                        {formatCurrency(
                          compra.total
                        )}
                      </td>

                      <td>
                        <span
                          className={
                            getStatusBadgeClass(
                              compra.estado
                            )
                          }
                        >
                          {compra.estado}
                        </span>
                      </td>
                    </tr>
                  )
                )}

                {recentCompras.length === 0 &&
                  !loading && (
                    <tr>
                      <td colSpan="6">
                        No hay compras registradas.
                      </td>
                    </tr>
                  )}
              </tbody>
            </table>
          </div>
        </section>
      )}


      {canViewInvoices && (
        <section className="card">
          <h3>Últimas facturas</h3>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Número</th>
                  <th>Paciente</th>
                  <th>Fecha</th>
                  <th>Total</th>
                  <th>Estado</th>
                </tr>
              </thead>

              <tbody>
                {recentFacturas.map(
                  (factura) => (
                    <tr
                      key={factura.factura_id}
                    >
                      <td>
                        {factura.numero_factura}
                      </td>

                      <td>
                        {factura.paciente_nombre ||
                          factura.paciente_id}
                      </td>

                      <td>
                        {formatDate(
                          factura.fecha_emision
                        )}
                      </td>

                      <td>
                        {formatCurrency(
                          factura.total
                        )}
                      </td>

                      <td>
                        <span
                          className={
                            getStatusBadgeClass(
                              factura.estado
                            )
                          }
                        >
                          {factura.estado}
                        </span>
                      </td>
                    </tr>
                  )
                )}

                {recentFacturas.length === 0 &&
                  !loading && (
                    <tr>
                      <td colSpan="5">
                        No hay facturas registradas.
                      </td>
                    </tr>
                  )}
              </tbody>
            </table>
          </div>
        </section>
      )}


      {canViewPayments && (
        <section className="card">
          <h3>Últimos pagos</h3>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Factura</th>
                  <th>Método</th>
                  <th>Monto</th>
                  <th>Fecha</th>
                  <th>Referencia</th>
                  <th>Estado</th>
                </tr>
              </thead>

              <tbody>
                {recentPagos.map(
                  (pago) => (
                    <tr key={pago.pago_id}>
                      <td>
                        {pago.numero_factura ||
                          pago.factura_id}
                      </td>

                      <td>
                        {pago.metodo_pago_nombre ||
                          pago.nombre_metodo_pago ||
                          pago.metodo_pago_id}
                      </td>

                      <td>
                        {formatCurrency(
                          pago.monto
                        )}
                      </td>

                      <td>
                        {formatDate(
                          pago.fecha_pago
                        )}
                      </td>

                      <td>
                        {pago.numero_referencia ||
                          "Sin referencia"}
                      </td>

                      <td>
                        <span
                          className={
                            getStatusBadgeClass(
                              pago.estado
                            )
                          }
                        >
                          {pago.estado}
                        </span>
                      </td>
                    </tr>
                  )
                )}

                {recentPagos.length === 0 &&
                  !loading && (
                    <tr>
                      <td colSpan="6">
                        No hay pagos registrados.
                      </td>
                    </tr>
                  )}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </section>
  );
}


export default Home;