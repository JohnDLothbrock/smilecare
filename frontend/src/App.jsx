import {
  Navigate,
  Outlet,
  Route,
  Routes
} from "react-router-dom";

import Navbar from "./components/Navbar.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";

import Admin from "./pages/Admin.jsx";
import AgendaMedica from "./pages/AgendaMedica.jsx";
import AtencionClinica from "./pages/AtencionClinica.jsx";
import AuditoriaAdmin from "./pages/AuditoriaAdmin.jsx";
import Caja from "./pages/Caja.jsx";
import Compras from "./pages/Compras.jsx";
import Doctores from "./pages/Doctores.jsx";
import ExpedienteClinico from "./pages/ExpedienteClinico.jsx";
import Facturas from "./pages/Facturas.jsx";
import ForgotPassword from "./pages/ForgotPassword.jsx";
import Home from "./pages/Home.jsx";
import InventarioStock from "./pages/InventarioStock.jsx";
import Login from "./pages/Login.jsx";
import MetodosPago from "./pages/MetodosPago.jsx";
import Pacientes from "./pages/Pacientes.jsx";
import Pagos from "./pages/Pagos.jsx";
import Proveedores from "./pages/Proveedores.jsx";
import ResetPassword from "./pages/ResetPassword.jsx";
import Tratamientos from "./pages/Tratamientos.jsx";


function AppLayout() {
  return (
    <>
      <Navbar />

      <main className="container">
        <Outlet />
      </main>
    </>
  );
}


function App() {
  return (
    <Routes>
      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/forgot-password"
        element={<ForgotPassword />}
      />

      <Route
        path="/reset-password"
        element={<ResetPassword />}
      />

      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/pacientes"
          element={
            <ProtectedRoute
              requiredPermissions={[
                "PACIENTES_VER",
                "PACIENTES_GESTIONAR"
              ]}
            >
              <Pacientes />
            </ProtectedRoute>
          }
        />

        <Route
          path="/doctores"
          element={
            <ProtectedRoute
              requiredPermission={
                "DOCTORES_GESTIONAR"
              }
            >
              <Doctores />
            </ProtectedRoute>
          }
        />

        <Route
          path="/agenda-medica"
          element={
            <ProtectedRoute
              requiredPermissions={[
                "AGENDA_GESTIONAR",
                "CITAS_GESTIONAR"
              ]}
            >
              <AgendaMedica />
            </ProtectedRoute>
          }
        />

        <Route
          path="/atencion-clinica"
          element={
            <ProtectedRoute
              requiredPermission={
                "CONSULTAS_GESTIONAR"
              }
            >
              <AtencionClinica />
            </ProtectedRoute>
          }
        />

        <Route
          path="/expediente-clinico"
          element={
            <ProtectedRoute
              requiredPermission={
                "EXPEDIENTE_GESTIONAR"
              }
            >
              <ExpedienteClinico />
            </ProtectedRoute>
          }
        />

        <Route
          path="/tratamientos"
          element={
            <ProtectedRoute
              requiredPermission={
                "TRATAMIENTOS_GESTIONAR"
              }
            >
              <Tratamientos />
            </ProtectedRoute>
          }
        />

        <Route
          path="/caja"
          element={
            <ProtectedRoute
              requiredPermission={
                "CAJA_USAR"
              }
            >
              <Caja />
            </ProtectedRoute>
          }
        />

        <Route
          path="/facturas"
          element={
            <ProtectedRoute
              requiredPermissions={[
                "FACTURAS_VER",
                "CAJA_USAR"
              ]}
            >
              <Facturas />
            </ProtectedRoute>
          }
        />

        <Route
          path="/metodos-pago"
          element={
            <ProtectedRoute
              requiredPermission={
                "METODOS_PAGO_GESTIONAR"
              }
            >
              <MetodosPago />
            </ProtectedRoute>
          }
        />

        <Route
          path="/pagos"
          element={
            <ProtectedRoute
              requiredPermissions={[
                "PAGOS_VER",
                "CAJA_USAR"
              ]}
            >
              <Pagos />
            </ProtectedRoute>
          }
        />

        <Route
          path="/proveedores"
          element={
            <ProtectedRoute
              requiredPermission={
                "PROVEEDORES_GESTIONAR"
              }
            >
              <Proveedores />
            </ProtectedRoute>
          }
        />

        <Route
          path="/inventario-stock"
          element={
            <ProtectedRoute
              requiredPermissions={[
                "INVENTARIO_VER",
                "INVENTARIO_GESTIONAR"
              ]}
            >
              <InventarioStock />
            </ProtectedRoute>
          }
        />

        <Route
          path="/compras"
          element={
            <ProtectedRoute
              requiredPermission={
                "COMPRAS_GESTIONAR"
              }
            >
              <Compras />
            </ProtectedRoute>
          }
        />

        <Route
          path="/admin"
          element={
            <ProtectedRoute
              requiredPermission={
                "ADMIN_GESTIONAR"
              }
            >
              <Admin />
            </ProtectedRoute>
          }
        />

        <Route
          path="/admin/auditoria"
          element={
            <ProtectedRoute
              requiredPermission={
                "ADMIN_GESTIONAR"
              }
            >
              <AuditoriaAdmin />
            </ProtectedRoute>
          }
        />
      </Route>

      <Route
        path="*"
        element={
          <Navigate
            to="/"
            replace
          />
        }
      />
    </Routes>
  );
}


export default App;