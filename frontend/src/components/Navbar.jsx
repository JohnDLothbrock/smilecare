import {
  useState
} from "react";

import {
  Link,
  useNavigate
} from "react-router-dom";

import {
  useAuth
} from "../auth/AuthContext.jsx";


function MenuGroup({
  label,
  menuName,
  items,
  openMenu,
  toggleMenu,
  closeMenus
}) {
  if (items.length === 0) {
    return null;
  }


  return (
    <details
      className="nav-dropdown"
      open={
        openMenu === menuName
      }
    >
      <summary
        onClick={(event) => {
          event.preventDefault();

          toggleMenu(
            menuName
          );
        }}
      >
        {label}
      </summary>


      <div className="nav-dropdown-menu">
        {items.map((item) => (
          <Link
            key={item.to}
            to={item.to}
            onClick={closeMenus}
          >
            {item.label}
          </Link>
        ))}
      </div>
    </details>
  );
}


function Navbar() {
  const [
    openMenu,
    setOpenMenu
  ] = useState(null);


  const {
    user,
    logout,
    hasPermission,
    hasAnyPermission
  } = useAuth();


  const navigate =
    useNavigate();


  function toggleMenu(
    menuName
  ) {
    setOpenMenu(
      (currentMenu) =>
        currentMenu === menuName
          ? null
          : menuName
    );
  }


  function closeMenus() {
    setOpenMenu(null);
  }


  async function handleLogout() {
    closeMenus();

    await logout();

    navigate(
      "/login",
      {
        replace: true
      }
    );
  }


  const clinicalItems = [
    {
      label: "Pacientes",
      to: "/pacientes",
      allowed: hasAnyPermission(
        "PACIENTES_VER",
        "PACIENTES_GESTIONAR"
      )
    },
    {
      label: "Doctores",
      to: "/doctores",
      allowed: hasPermission(
        "DOCTORES_GESTIONAR"
      )
    },
    {
      label: "Agenda Médica",
      to: "/agenda-medica",
      allowed: hasAnyPermission(
        "AGENDA_GESTIONAR",
        "CITAS_GESTIONAR"
      )
    },
    {
      label: "Atención Clínica",
      to: "/atencion-clinica",
      allowed: hasPermission(
        "CONSULTAS_GESTIONAR"
      )
    },
    {
      label: "Expediente Clínico",
      to: "/expediente-clinico",
      allowed: hasPermission(
        "EXPEDIENTE_GESTIONAR"
      )
    }
  ].filter(
    (item) => item.allowed
  );


  const treatmentItems = [
    {
      label: "Tratamientos",
      to: "/tratamientos",
      allowed: hasPermission(
        "TRATAMIENTOS_GESTIONAR"
      )
    }
  ].filter(
    (item) => item.allowed
  );


  const financeItems = [
    {
      label: "Caja",
      to: "/caja",
      allowed: hasPermission(
        "CAJA_USAR"
      )
    },
    {
      label: "Facturas",
      to: "/facturas",
      allowed: hasAnyPermission(
        "FACTURAS_VER",
        "CAJA_USAR"
      )
    },
    {
      label: "Métodos Pago",
      to: "/metodos-pago",
      allowed: hasPermission(
        "METODOS_PAGO_GESTIONAR"
      )
    },
    {
      label: "Pagos",
      to: "/pagos",
      allowed: hasAnyPermission(
        "PAGOS_VER",
        "CAJA_USAR"
      )
    }
  ].filter(
    (item) => item.allowed
  );


  const inventoryItems = [
    {
      label: "Proveedores",
      to: "/proveedores",
      allowed: hasPermission(
        "PROVEEDORES_GESTIONAR"
      )
    },
    {
      label: "Compras e Insumos",
      to: "/compras",
      allowed: hasPermission(
        "COMPRAS_GESTIONAR"
      )
    },
    {
      label: "Stock",
      to: "/inventario-stock",
      allowed: hasAnyPermission(
        "INVENTARIO_VER",
        "INVENTARIO_GESTIONAR"
      )
    }
  ].filter(
    (item) => item.allowed
  );


  const administrationItems =
    hasPermission(
      "ADMIN_GESTIONAR"
    )
      ? [
          {
            label:
              "Usuarios y permisos",

            to:
              "/admin"
          },
          {
            label:
              "Auditoría y accesos",

            to:
              "/admin/auditoria"
          }
        ]
      : [];


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


        <MenuGroup
          label="Clínica"
          menuName="clinica"
          items={clinicalItems}
          openMenu={openMenu}
          toggleMenu={toggleMenu}
          closeMenus={closeMenus}
        />


        <MenuGroup
          label="Tratamientos"
          menuName="tratamientos"
          items={treatmentItems}
          openMenu={openMenu}
          toggleMenu={toggleMenu}
          closeMenus={closeMenus}
        />


        <MenuGroup
          label="Finanzas"
          menuName="finanzas"
          items={financeItems}
          openMenu={openMenu}
          toggleMenu={toggleMenu}
          closeMenus={closeMenus}
        />


        <MenuGroup
          label="Inventario"
          menuName="inventario"
          items={inventoryItems}
          openMenu={openMenu}
          toggleMenu={toggleMenu}
          closeMenus={closeMenus}
        />


        <MenuGroup
          label="Administración"
          menuName="administracion"
          items={
            administrationItems
          }
          openMenu={openMenu}
          toggleMenu={toggleMenu}
          closeMenus={closeMenus}
        />


        <span>
          {user?.nombre_usuario}
          {" · "}
          {user?.nombre_rol}
        </span>


        <button
          type="button"
          className="secondary-button"
          onClick={handleLogout}
        >
          Cerrar sesión
        </button>
      </nav>
    </header>
  );
}


export default Navbar;