import {
  useState
} from "react";

import {
  Link
} from "react-router-dom";

import {
  apiClient
} from "../api/apiClient.js";


function ForgotPassword() {
  const [
    identifier,
    setIdentifier
  ] = useState("");

  const [loading, setLoading] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [error, setError] =
    useState("");


  async function handleSubmit(
    event
  ) {
    event.preventDefault();

    try {
      setLoading(true);
      setMessage("");
      setError("");

      const response =
        await apiClient.post(
          "/auth/forgot-password",
          {
            identificador:
              identifier.trim()
          }
        );

      setMessage(
        response.message
      );

    } catch (err) {
      setError(err.message);

    } finally {
      setLoading(false);
    }
  }


  return (
    <main className="container">
      <section className="card">
        <div className="page-header">
          <div>
            <h2>
              Recuperar contraseña
            </h2>

            <p>
              Ingrese su nombre de usuario
              o correo de recuperación.
            </p>
          </div>
        </div>

        <form
          className="form-grid"
          onSubmit={handleSubmit}
        >
          <label>
            Usuario o correo

            <input
              type="text"
              value={identifier}
              onChange={(event) =>
                setIdentifier(
                  event.target.value
                )
              }
              autoComplete="username"
              autoFocus
              required
            />
          </label>

          <div className="form-actions">
            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Enviando..."
                : "Enviar enlace"}
            </button>

            <Link
              to="/login"
              className="secondary-button"
            >
              Volver al inicio de sesión
            </Link>
          </div>
        </form>

        {message && (
          <p className="success-message">
            {message}
          </p>
        )}

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}
      </section>
    </main>
  );
}


export default ForgotPassword;