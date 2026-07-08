import {
  useState
} from "react";

import {
  Link,
  useSearchParams
} from "react-router-dom";

import {
  apiClient
} from "../api/apiClient.js";


function ResetPassword() {
  const [searchParams] =
    useSearchParams();

  const token =
    searchParams.get("token") || "";

  const [
    newPassword,
    setNewPassword
  ] = useState("");

  const [
    confirmPassword,
    setConfirmPassword
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

      if (!token) {
        throw new Error(
          "El enlace no contiene un token de recuperación."
        );
      }

      if (newPassword.length < 8) {
        throw new Error(
          "La nueva contraseña debe tener al menos 8 caracteres."
        );
      }

      if (
        newPassword !==
        confirmPassword
      ) {
        throw new Error(
          "Las contraseñas no coinciden."
        );
      }

      const response =
        await apiClient.post(
          "/auth/reset-password",
          {
            token,

            new_password:
              newPassword
          }
        );

      setMessage(
        response.message
      );

      setNewPassword("");
      setConfirmPassword("");

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
              Restablecer contraseña
            </h2>

            <p>
              Defina una nueva contraseña
              para su cuenta de SmileCare.
            </p>
          </div>
        </div>

        {!token && (
          <p className="error-message">
            El enlace de recuperación
            no contiene un token válido.
          </p>
        )}

        {token && !message && (
          <form
            className="form-grid"
            onSubmit={handleSubmit}
          >
            <label>
              Nueva contraseña

              <input
                type="password"
                value={newPassword}
                onChange={(event) =>
                  setNewPassword(
                    event.target.value
                  )
                }
                minLength="8"
                autoComplete="new-password"
                required
              />
            </label>

            <label>
              Confirmar contraseña

              <input
                type="password"
                value={confirmPassword}
                onChange={(event) =>
                  setConfirmPassword(
                    event.target.value
                  )
                }
                minLength="8"
                autoComplete="new-password"
                required
              />
            </label>

            <div className="form-actions">
              <button
                type="submit"
                disabled={loading}
              >
                {loading
                  ? "Actualizando..."
                  : "Cambiar contraseña"}
              </button>
            </div>
          </form>
        )}

        {message && (
          <>
            <p className="success-message">
              {message}
            </p>

            <div className="form-actions">
              <Link
                to="/login"
                className="secondary-button"
              >
                Ir al inicio de sesión
              </Link>
            </div>
          </>
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


export default ResetPassword;