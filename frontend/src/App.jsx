import { Route, Routes } from "react-router-dom";

import Navbar from "./components/Navbar.jsx";
import Home from "./pages/Home.jsx";
import Citas from "./pages/Citas.jsx";
import Consultas from "./pages/Consultas.jsx";
import Doctores from "./pages/Doctores.jsx";
import Facturas from "./pages/Facturas.jsx";
import Insumos from "./pages/Insumos.jsx";
import InventarioStock from "./pages/InventarioStock.jsx";
import MetodosPago from "./pages/MetodosPago.jsx";
import Pacientes from "./pages/Pacientes.jsx";
import Pagos from "./pages/Pagos.jsx";
import Proveedores from "./pages/Proveedores.jsx";
import Tratamientos from "./pages/Tratamientos.jsx";
import TratamientosConsulta from "./pages/TratamientosConsulta.jsx";
import Compras from "./pages/Compras.jsx";
import DetalleCompra from "./pages/DetalleCompra.jsx";

function App() {
  return (
    <>
      <Navbar />

      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/pacientes" element={<Pacientes />} />
          <Route path="/doctores" element={<Doctores />} />
          <Route path="/citas" element={<Citas />} />
          <Route path="/consultas" element={<Consultas />} />
          <Route path="/tratamientos" element={<Tratamientos />} />
          <Route path="/tratamientos-consulta" element={<TratamientosConsulta />}/>
          <Route path="/facturas" element={<Facturas />} />
          <Route path="/metodos-pago" element={<MetodosPago />} />
          <Route path="/pagos" element={<Pagos />} />
          <Route path="/proveedores" element={<Proveedores />} />
          <Route path="/insumos" element={<Insumos />} />
          <Route path="/inventario-stock" element={<InventarioStock />} />
          <Route path="/compras" element={<Compras />} />
          <Route path="/detalle-compra" element={<DetalleCompra />} />
        </Routes>
      </main>
    </>
  );
}

export default App;