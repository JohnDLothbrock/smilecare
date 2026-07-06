import { useState } from "react";
import { Link } from "react-router-dom";

function Navbar() {
  const [openMenu, setOpenMenu] = useState(null);

  function toggleMenu(menuName) {
    setOpenMenu((currentMenu) =>
      currentMenu === menuName
        ? null
        : menuName
    );
  }

  function closeMenus() {
    setOpenMenu(null);
  }

  return (
    <header className="navbar">
      <Link
        to="/"
        className="navbar-logo"
        onClick={closeMenus}
      >
        SmileCare
      </Link>

      <nav className="nav-menu">
        <Link
          to="/"
          onClick={closeMenus}
        >
          Inicio
        </Link>

        <details
          className="nav-dropdown"
          open={openMenu === "clinica"}
        >
          <summary
            onClick={(event) => {
              event.preventDefault();
              toggleMenu("clinica");
            }}
          >
            Clínica
          </summary>

          <div className="nav-dropdown-menu">
            <Link
              to="/pacientes"
              onClick={closeMenus}
            >
              Pacientes
            </Link>

            <Link
              to="/doctores"
              onClick={closeMenus}
            >
              Doctores
            </Link>

            <Link
              to="/agenda-medica"
              onClick={closeMenus}
            >
              Agenda Médica
            </Link>

            <Link
              to="/atencion-clinica"
              onClick={closeMenus}
            >
              Atención Clínica
            </Link>

            <Link
              to="/expediente-clinico"
              onClick={closeMenus}
            >
              Expediente Clínico
            </Link>
          </div>
        </details>

        <details
          className="nav-dropdown"
          open={openMenu === "tratamientos"}
        >
          <summary
            onClick={(event) => {
              event.preventDefault();
              toggleMenu("tratamientos");
            }}
          >
            Tratamientos
          </summary>

          <div className="nav-dropdown-menu">
            <Link
              to="/tratamientos"
              onClick={closeMenus}
            >
              Tratamientos
            </Link>
          </div>
        </details>

        <details
          className="nav-dropdown"
          open={openMenu === "finanzas"}
        >
          <summary
            onClick={(event) => {
              event.preventDefault();
              toggleMenu("finanzas");
            }}
          >
            Finanzas
          </summary>

          <div className="nav-dropdown-menu">
            <Link
              to="/caja"
              onClick={closeMenus}
            >
              Caja
            </Link>

            <Link
              to="/facturas"
              onClick={closeMenus}
            >
              Facturas
            </Link>

            <Link
              to="/metodos-pago"
              onClick={closeMenus}
            >
              Métodos Pago
            </Link>

            <Link
              to="/pagos"
              onClick={closeMenus}
            >
              Pagos
            </Link>
          </div>
        </details>

        <details
          className="nav-dropdown"
          open={openMenu === "inventario"}
        >
          <summary
            onClick={(event) => {
              event.preventDefault();
              toggleMenu("inventario");
            }}
          >
            Inventario
          </summary>

          <div className="nav-dropdown-menu">
            <Link
              to="/proveedores"
              onClick={closeMenus}
            >
              Proveedores
            </Link>

            <Link
              to="/compras"
              onClick={closeMenus}
            >
              Compras e Insumos
            </Link>

            <Link
              to="/inventario-stock"
              onClick={closeMenus}
            >
              Stock
            </Link>
          </div>
        </details>

        <Link
          to="/admin"
          onClick={closeMenus}
        >
          Administración
        </Link>
      </nav>
    </header>
  );
}

export default Navbar;