import { Route, Routes } from "react-router-dom";

import Navbar from "./components/Navbar.jsx";
import Home from "./pages/Home.jsx";
import Doctores from "./pages/Doctores.jsx";
import Facturas from "./pages/Facturas.jsx";
import InventarioStock from "./pages/InventarioStock.jsx";
import MetodosPago from "./pages/MetodosPago.jsx";
import Pacientes from "./pages/Pacientes.jsx";
import Pagos from "./pages/Pagos.jsx";
import Proveedores from "./pages/Proveedores.jsx";
import Tratamientos from "./pages/Tratamientos.jsx";
import Compras from "./pages/Compras.jsx";
import ExpedienteClinico from "./pages/ExpedienteClinico.jsx";
import AgendaMedica from "./pages/AgendaMedica.jsx";
import Caja from "./pages/Caja.jsx";
import Admin from "./pages/Admin.jsx";
import AtencionClinica from "./pages/AtencionClinica.jsx";

function App() {
  return (
    <>
      <Navbar />

      <main className="container">
        <Routes>
          <Route
            path="/"
            element={<Home />}
          />

          <Route
            path="/pacientes"
            element={<Pacientes />}
          />

          <Route
            path="/doctores"
            element={<Doctores />}
          />

          <Route
            path="/agenda-medica"
            element={<AgendaMedica />}
          />

          <Route
            path="/atencion-clinica"
            element={<AtencionClinica />}
          />

          <Route
            path="/expediente-clinico"
            element={<ExpedienteClinico />}
          />

          <Route
            path="/tratamientos"
            element={<Tratamientos />}
          />

          <Route
            path="/caja"
            element={<Caja />}
          />

          <Route
            path="/facturas"
            element={<Facturas />}
          />

          <Route
            path="/metodos-pago"
            element={<MetodosPago />}
          />

          <Route
            path="/pagos"
            element={<Pagos />}
          />

          <Route
            path="/proveedores"
            element={<Proveedores />}
          />

          <Route
            path="/inventario-stock"
            element={<InventarioStock />}
          />

          <Route
            path="/compras"
            element={<Compras />}
          />

          <Route
            path="/admin"
            element={<Admin />}
          />
        </Routes>
      </main>
    </>
  );
}

export default App;