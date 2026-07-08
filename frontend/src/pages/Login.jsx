import {
  useEffect,
  useState
} from "react";

import {
  Link,
  useLocation,
  useNavigate
} from "react-router-dom";

import {
  useAuth
} from "../auth/AuthContext.jsx";


function Login() {
  const [
    nombreUsuario,
    setNombreUsuario
  ] = useState("");

  const [
    password,
    setPassword
  ] = useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  const {
    user,
    login
  } = useAuth();

  const navigate = useNavigate();

  const location = useLocation();


  const destination =
    location.state?.from?.pathname ||
    "/";


  useEffect(() => {
    if (user) {
      navigate(
        "/",
        {
          replace: true
        }
      );
    }
  }, [
    user,
    navigate
  ]);


  async function handleSubmit(
    event
  ) {
    event.preventDefault();

    if (loading) {
      return;
    }

    try {
      setLoading(true);
      setError("");

      await login(
        nombreUsuario.trim(),
        password
      );

      navigate(
        destination,
        {
          replace: true
        }
      );

    } catch (err) {
      setError(err.message);

    } finally {
      setLoading(false);
    }
  }


  function handleKeyDown(
    event
  ) {
    if (
      event.key === "Enter" &&
      !loading
    ) {
      event.preventDefault();

      event.currentTarget
        .requestSubmit();
    }
  }


  return (
    <main className="container">
      <section className="card">
        <div className="page-header">
          <div>
            <h2>SmileCare</h2>

            <p>
              Ingrese sus credenciales para
              acceder al sistema.
            </p>
          </div>
        </div>

        <form
          className="form-grid"
          onSubmit={handleSubmit}
          onKeyDown={handleKeyDown}
        >
          <label>
            Nombre de usuario

            <input
              type="text"
              value={nombreUsuario}
              onChange={(event) =>
                setNombreUsuario(
                  event.target.value
                )
              }
              autoComplete="username"
              autoFocus
              required
            />
          </label>

          <label>
            Contraseña

            <input
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(
                  event.target.value
                )
              }
              autoComplete="current-password"
              required
            />
          </label>

          <div
            style={{
              display: "flex",
              justifyContent: "flex-end",
              marginTop: "-10px"
            }}
          >
            <Link
              to="/forgot-password"
              style={{
                color: "#0f766e",
                fontSize: "0.95rem",
                fontWeight: "600",
                textDecoration: "none"
              }}
            >
              ¿Olvidó su contraseña?
            </Link>
          </div>

          <div className="form-actions">
            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Iniciando sesión..."
                : "Iniciar sesión"}
            </button>
          </div>
        </form>

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}
      </section>
    </main>
  );
}


export default Login;