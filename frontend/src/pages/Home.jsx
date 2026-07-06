import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { apiClient } from "../api/apiClient.js";

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
  const [stats, setStats] = useState(initialStats);

  const [recentFacturas, setRecentFacturas] =
    useState([]);

  const [recentPagos, setRecentPagos] =
    useState([]);

  const [recentCompras, setRecentCompras] =
    useState([]);

  const [lowStockItems, setLowStockItems] =
    useState([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  async function loadDashboardData() {
    try {
      setLoading(true);
      setError("");

      const [
        pacientes,
        doctores,
        consultas,
        facturas,
        pagos,
        compras,
        inventarioStock
      ] = await Promise.all([
        apiClient.get("/pacientes"),
        apiClient.get("/doctores"),
        apiClient.get("/consultas"),
        apiClient.get("/facturas"),
        apiClient.get("/pagos"),
        apiClient.get("/compras"),
        apiClient.get("/inventario-stock")
      ]);

      const lowStock = inventarioStock.filter(
        (item) => {
          if (
            item.stock_minimo === null ||
            item.stock_minimo === undefined
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
        productosStock: inventarioStock.length,
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
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboardData();
  }, []);

  function getStatusBadgeClass(status) {
    const normalizedStatus = String(
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
    if (
      item.codigo &&
      item.insumo_nombre
    ) {
      return (
        `${item.codigo} - ` +
        `${item.insumo_nombre}`
      );
    }

    return (
      item.insumo_nombre ||
      item.nombre ||
      `Insumo ${item.insumo_id}`
    );
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Sistema SmileCare</h2>

          <p>
            Resumen general de la operación clínica,
            financiera y de inventario.
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
        <article className="dashboard-card">
          <h3>Pacientes</h3>

          <p>{stats.pacientes}</p>

          <Link to="/pacientes">
            Ver pacientes
          </Link>
        </article>

        <article className="dashboard-card">
          <h3>Doctores</h3>

          <p>{stats.doctores}</p>

          <Link to="/doctores">
            Ver doctores
          </Link>
        </article>

        <article className="dashboard-card">
          <h3>Atenciones clínicas</h3>

          <p>{stats.atenciones}</p>

          <Link to="/atencion-clinica">
            Registrar atención
          </Link>
        </article>

        <article className="dashboard-card">
          <h3>Facturas</h3>

          <p>{stats.facturas}</p>

          <Link to="/facturas">
            Ver facturas
          </Link>
        </article>

        <article className="dashboard-card">
          <h3>Pagos</h3>

          <p>{stats.pagos}</p>

          <Link to="/pagos">
            Ver pagos
          </Link>
        </article>

        <article className="dashboard-card">
          <h3>Compras recibidas</h3>

          <p>{stats.compras}</p>

          <Link to="/compras">
            Ver compras
          </Link>
        </article>

        <article className="dashboard-card">
          <h3>Productos en stock</h3>

          <p>{stats.productosStock}</p>

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
      </section>

      <section className="card">
        <h3>Acciones rápidas</h3>

        <p className="helper-text">
          Accesos directos a los principales procesos
          del sistema.
        </p>

        <div className="quick-actions">
          <Link to="/atencion-clinica">
            Registrar atención clínica
          </Link>

          <Link to="/caja">
            Cobrar en Caja
          </Link>

          <Link to="/compras">
            Registrar compra e insumos
          </Link>

          <Link to="/inventario-stock">
            Revisar Stock
          </Link>

          <Link to="/expediente-clinico">
            Consultar expediente clínico
          </Link>

          <Link to="/agenda-medica">
            Gestionar agenda médica
          </Link>
        </div>
      </section>

      <section className="card">
        <h3>Flujo clínico principal</h3>

        <p className="helper-text">
          La interfaz integra los procesos relacionados
          para reducir pasos innecesarios para el usuario.
        </p>

        <div className="workflow-grid">
          <div>
            <strong>1. Paciente</strong>

            <p>
              Se registra o selecciona el paciente
              que recibirá atención.
            </p>
          </div>

          <div>
            <strong>2. Agenda médica</strong>

            <p>
              Se revisan los horarios y la disponibilidad
              de los doctores.
            </p>
          </div>

          <div>
            <strong>3. Atención clínica</strong>

            <p>
              En un solo flujo se registra la cita,
              la consulta y los tratamientos aplicados.
            </p>
          </div>

          <div>
            <strong>4. Cirugía opcional</strong>

            <p>
              Cuando corresponde, la cirugía se registra
              como parte de la misma atención clínica.
            </p>
          </div>

          <div>
            <strong>5. Expediente clínico</strong>

            <p>
              Se consulta el historial completo del
              paciente y sus atenciones anteriores.
            </p>
          </div>

          <div>
            <strong>6. Caja</strong>

            <p>
              Se genera la factura, sus detalles,
              el impuesto correspondiente, el pago y
              el comprobante en un solo proceso.
            </p>
          </div>
        </div>
      </section>

      <section className="card">
        <h3>Flujo de compras e inventario</h3>

        <p className="helper-text">
          La recepción de productos y la actualización
          del inventario forman parte de un mismo proceso.
        </p>

        <div className="workflow-grid">
          <div>
            <strong>1. Proveedor</strong>

            <p>
              Se selecciona la empresa que suministra
              los productos a la clínica.
            </p>
          </div>

          <div>
            <strong>2. Compra recibida</strong>

            <p>
              Se registra la fecha y el usuario
              responsable de recibir la compra.
            </p>
          </div>

          <div>
            <strong>3. Productos</strong>

            <p>
              Se seleccionan productos existentes o
              se registran productos nuevos sin salir
              del proceso de compra.
            </p>
          </div>

          <div>
            <strong>4. Cantidad y costo</strong>

            <p>
              Se indica la cantidad recibida y el costo
              según la unidad de medida del producto.
            </p>
          </div>

          <div>
            <strong>5. Entrada automática</strong>

            <p>
              Al guardar la compra, el sistema crea
              los movimientos de entrada y actualiza
              el stock automáticamente.
            </p>
          </div>

          <div>
            <strong>6. Control de stock</strong>

            <p>
              Se revisan existencias, stock mínimo,
              costos recientes y movimientos de
              inventario.
            </p>
          </div>
        </div>
      </section>

      {lowStockItems.length > 0 && (
        <section className="card">
          <h3>Alertas de stock</h3>

          <p className="helper-text">
            Productos que se encuentran en el nivel
            mínimo o por debajo del mínimo definido.
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
                {lowStockItems.map((item) => (
                  <tr key={item.stock_id}>
                    <td>
                      {getStockItemName(item)}
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
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}

      <section className="card">
        <h3>Últimas compras recibidas</h3>

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
    </section>
  );
}

export default Home;