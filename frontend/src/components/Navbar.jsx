import { Link } from "react-router-dom";

function Navbar() {
  return (
    <header className="navbar">
      <h1>SmileCare</h1>

      <nav className="nav-menu">
        <Link to="/">Inicio</Link>

        <details className="nav-dropdown">
          <summary>Clínica</summary>

          <div className="nav-dropdown-menu">
            <Link to="/pacientes">Pacientes</Link>
            <Link to="/doctores">Doctores</Link>
            <Link to="/citas">Citas</Link>
            <Link to="/consultas">Consultas</Link>
          </div>
        </details>

        <details className="nav-dropdown">
          <summary>Tratamientos</summary>

          <div className="nav-dropdown-menu">
            <Link to="/tratamientos">Tratamientos</Link>
            <Link to="/tratamientos-consulta">Tratamientos Consulta</Link>
          </div>
        </details>

        <details className="nav-dropdown">
          <summary>Finanzas</summary>

          <div className="nav-dropdown-menu">
            <Link to="/facturas">Facturas</Link>
            <Link to="/metodos-pago">Métodos Pago</Link>
            <Link to="/pagos">Pagos</Link>
          </div>
        </details>

        <details className="nav-dropdown">
            <summary>Inventario</summary>

            <div className="nav-dropdown-menu">
                <Link to="/proveedores">Proveedores</Link>
                <Link to="/insumos">Insumos</Link>
                <Link to="/inventario-stock">Stock</Link>
            </div>
        </details>
      </nav>
    </header>
  );
}

export default Navbar;