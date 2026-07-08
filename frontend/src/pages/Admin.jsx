import {
  useEffect,
  useState
} from "react";

import {
  apiClient
} from "../api/apiClient.js";


const initialUsuarioForm = {
  rol_id: "",
  nombre_usuario: "",
  correo: "",
  password: "",
  estado: "ACTIVO"
};


const initialRolForm = {
  nombre_rol: "",
  descripcion: "",
  estado: "ACTIVO"
};


const initialPermisoForm = {
  codigo_permiso: "",
  descripcion: "",
  modulo: ""
};


const initialRolPermisoForm = {
  rol_id: "",
  permiso_id: ""
};


function Admin() {
  const [usuarios, setUsuarios] =
    useState([]);

  const [roles, setRoles] =
    useState([]);

  const [permisos, setPermisos] =
    useState([]);

  const [rolPermisos, setRolPermisos] =
    useState([]);


  const [
    usuarioForm,
    setUsuarioForm
  ] = useState(
    initialUsuarioForm
  );

  const [
    rolForm,
    setRolForm
  ] = useState(
    initialRolForm
  );

  const [
    permisoForm,
    setPermisoForm
  ] = useState(
    initialPermisoForm
  );

  const [
    rolPermisoForm,
    setRolPermisoForm
  ] = useState(
    initialRolPermisoForm
  );


  const [
    editingUsuarioId,
    setEditingUsuarioId
  ] = useState(null);

  const [
    editingRolId,
    setEditingRolId
  ] = useState(null);

  const [
    editingPermisoId,
    setEditingPermisoId
  ] = useState(null);

  const [
    selectedRoleId,
    setSelectedRoleId
  ] = useState("");


  const [loading, setLoading] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [error, setError] =
    useState("");


  async function loadUsuarios() {
    const data =
      await apiClient.get(
        "/usuarios"
      );

    setUsuarios(data);
  }


  async function loadRoles() {
    const data =
      await apiClient.get(
        "/roles"
      );

    setRoles(data);
  }


  async function loadPermisos() {
    const data =
      await apiClient.get(
        "/permisos"
      );

    setPermisos(data);
  }


  async function loadRolPermisos() {
    const data =
      await apiClient.get(
        "/rol-permisos"
      );

    setRolPermisos(data);
  }


  async function loadPageData() {
    try {
      setLoading(true);
      setError("");

      await Promise.all([
        loadUsuarios(),
        loadRoles(),
        loadPermisos(),
        loadRolPermisos()
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadPageData();
  }, []);


  function handleUsuarioChange(
    event
  ) {
    const {
      name,
      value
    } = event.target;

    setUsuarioForm(
      (currentForm) => ({
        ...currentForm,
        [name]: value
      })
    );
  }


  function handleRolChange(
    event
  ) {
    const {
      name,
      value
    } = event.target;

    setRolForm(
      (currentForm) => ({
        ...currentForm,
        [name]: value
      })
    );
  }


  function handlePermisoChange(
    event
  ) {
    const {
      name,
      value
    } = event.target;

    setPermisoForm(
      (currentForm) => ({
        ...currentForm,
        [name]: value
      })
    );
  }


  function handleRolPermisoChange(
    event
  ) {
    const {
      name,
      value
    } = event.target;

    setRolPermisoForm(
      (currentForm) => ({
        ...currentForm,
        [name]: value
      })
    );
  }


  function buildUsuarioPayload() {
    const payload = {
      rol_id: Number(
        usuarioForm.rol_id
      ),

      nombre_usuario:
        usuarioForm
          .nombre_usuario
          .trim(),

      correo:
        usuarioForm
          .correo
          .trim()
          .toLowerCase(),

      estado:
        usuarioForm.estado
    };

    if (
      editingUsuarioId === null ||
      usuarioForm.password
    ) {
      payload.password =
        usuarioForm.password;
    }

    return payload;
  }


  function buildRolPayload() {
    return {
      nombre_rol:
        rolForm.nombre_rol.trim(),

      descripcion:
        rolForm.descripcion.trim() ||
        null,

      estado:
        rolForm.estado
    };
  }


  function buildPermisoPayload() {
    return {
      codigo_permiso:
        permisoForm
          .codigo_permiso
          .trim(),

      descripcion:
        permisoForm
          .descripcion
          .trim() || null,

      modulo:
        permisoForm.modulo.trim() ||
        null
    };
  }


  function buildRolPermisoPayload() {
    return {
      rol_id: Number(
        rolPermisoForm.rol_id
      ),

      permiso_id: Number(
        rolPermisoForm.permiso_id
      )
    };
  }


  async function handleUsuarioSubmit(
    event
  ) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      if (
        editingUsuarioId === null &&
        usuarioForm.password.length < 8
      ) {
        throw new Error(
          "La contraseña inicial debe tener al menos 8 caracteres."
        );
      }

      if (
        editingUsuarioId !== null &&
        usuarioForm.password &&
        usuarioForm.password.length < 8
      ) {
        throw new Error(
          "La nueva contraseña debe tener al menos 8 caracteres."
        );
      }

      const payload =
        buildUsuarioPayload();

      if (
        editingUsuarioId === null
      ) {
        await apiClient.post(
          "/usuarios",
          payload
        );

        setMessage(
          "Usuario creado correctamente."
        );
      } else {
        await apiClient.put(
          `/usuarios/${editingUsuarioId}`,
          payload
        );

        setMessage(
          "Usuario actualizado correctamente."
        );
      }

      setUsuarioForm(
        initialUsuarioForm
      );

      setEditingUsuarioId(null);

      await loadUsuarios();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  async function handleRolSubmit(
    event
  ) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const payload =
        buildRolPayload();

      if (editingRolId === null) {
        await apiClient.post(
          "/roles",
          payload
        );

        setMessage(
          "Rol creado correctamente."
        );
      } else {
        await apiClient.put(
          `/roles/${editingRolId}`,
          payload
        );

        setMessage(
          "Rol actualizado correctamente."
        );
      }

      setRolForm(
        initialRolForm
      );

      setEditingRolId(null);

      await loadRoles();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  async function handlePermisoSubmit(
    event
  ) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const payload =
        buildPermisoPayload();

      if (
        editingPermisoId === null
      ) {
        await apiClient.post(
          "/permisos",
          payload
        );

        setMessage(
          "Permiso creado correctamente."
        );
      } else {
        await apiClient.put(
          `/permisos/${editingPermisoId}`,
          payload
        );

        setMessage(
          "Permiso actualizado correctamente."
        );
      }

      setPermisoForm(
        initialPermisoForm
      );

      setEditingPermisoId(null);

      await loadPermisos();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  async function handleRolPermisoSubmit(
    event
  ) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.post(
        "/rol-permisos",
        buildRolPermisoPayload()
      );

      setRolPermisoForm(
        initialRolPermisoForm
      );

      setMessage(
        "Permiso asignado al rol correctamente."
      );

      await loadRolPermisos();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  function handleEditUsuario(
    usuario
  ) {
    setEditingUsuarioId(
      usuario.usuario_id
    );

    setUsuarioForm({
      rol_id:
        usuario.rol_id ?? "",

      nombre_usuario:
        usuario.nombre_usuario ?? "",

      correo:
        usuario.correo ?? "",

      password: "",

      estado:
        usuario.estado ?? "ACTIVO"
    });

    setMessage(
      "Usuario seleccionado para edición."
    );

    setError("");
  }


  function handleEditRol(rol) {
    setEditingRolId(
      rol.rol_id
    );

    setRolForm({
      nombre_rol:
        rol.nombre_rol ?? "",

      descripcion:
        rol.descripcion ?? "",

      estado:
        rol.estado ?? "ACTIVO"
    });

    setMessage(
      "Rol seleccionado para edición."
    );

    setError("");
  }


  function handleEditPermiso(
    permiso
  ) {
    setEditingPermisoId(
      permiso.permiso_id
    );

    setPermisoForm({
      codigo_permiso:
        permiso.codigo_permiso ??
        "",

      descripcion:
        permiso.descripcion ?? "",

      modulo:
        permiso.modulo ?? ""
    });

    setMessage(
      "Permiso seleccionado para edición."
    );

    setError("");
  }


  async function handleDeleteUsuario(
    usuarioId
  ) {
    const confirmed =
      window.confirm(
        "¿Seguro que desea eliminar este usuario?"
      );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(
        `/usuarios/${usuarioId}`
      );

      setMessage(
        "Usuario eliminado correctamente."
      );

      await loadUsuarios();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  async function handleDeleteRol(
    rolId
  ) {
    const confirmed =
      window.confirm(
        "¿Seguro que desea eliminar este rol?"
      );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(
        `/roles/${rolId}`
      );

      setMessage(
        "Rol eliminado correctamente."
      );

      await Promise.all([
        loadRoles(),
        loadRolPermisos()
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  async function handleDeletePermiso(
    permisoId
  ) {
    const confirmed =
      window.confirm(
        "¿Seguro que desea eliminar este permiso?"
      );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(
        `/permisos/${permisoId}`
      );

      setMessage(
        "Permiso eliminado correctamente."
      );

      await Promise.all([
        loadPermisos(),
        loadRolPermisos()
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  async function handleDeleteRolPermiso(
    rolId,
    permisoId
  ) {
    const confirmed =
      window.confirm(
        "¿Seguro que desea quitar este permiso del rol?"
      );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(
        `/rol-permisos/${rolId}/${permisoId}`
      );

      setMessage(
        "Permiso removido del rol correctamente."
      );

      await loadRolPermisos();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  function handleCancelUsuarioEdit() {
    setEditingUsuarioId(null);

    setUsuarioForm(
      initialUsuarioForm
    );

    setMessage("");
    setError("");
  }


  function handleCancelRolEdit() {
    setEditingRolId(null);

    setRolForm(
      initialRolForm
    );

    setMessage("");
    setError("");
  }


  function handleCancelPermisoEdit() {
    setEditingPermisoId(null);

    setPermisoForm(
      initialPermisoForm
    );

    setMessage("");
    setError("");
  }


  function getRolLabel(rolId) {
    const rol = roles.find(
      (item) =>
        String(item.rol_id) ===
        String(rolId)
    );

    return (
      rol?.nombre_rol ||
      rolId ||
      ""
    );
  }


  function getPermisoLabel(
    permisoId
  ) {
    const permiso =
      permisos.find(
        (item) =>
          String(
            item.permiso_id
          ) ===
          String(permisoId)
      );

    return (
      permiso?.codigo_permiso ||
      permisoId ||
      ""
    );
  }


  function getStatusBadgeClass(
    currentStatus
  ) {
    if (currentStatus === "ACTIVO") {
      return (
        "badge success-badge"
      );
    }

    if (
      currentStatus === "INACTIVO"
    ) {
      return (
        "badge warning-badge"
      );
    }

    return "badge danger-badge";
  }


  function getRolPermisosByRolId(
    rolId
  ) {
    return rolPermisos.filter(
      (item) =>
        String(item.rol_id) ===
        String(rolId)
    );
  }


  function handleSelectRoleForPermissions(
    event
  ) {
    const rolId =
      event.target.value;

    setSelectedRoleId(rolId);

    setRolPermisoForm(
      (currentForm) => ({
        ...currentForm,
        rol_id: rolId
      })
    );
  }


  const selectedRolePermissions =
    selectedRoleId
      ? getRolPermisosByRolId(
          selectedRoleId
        )
      : [];


  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Administración</h2>

          <p>
            Gestión de usuarios, roles y
            permisos del sistema.
          </p>
        </div>
      </div>

      <section className="card">
        <h3>Resumen de seguridad</h3>

        <div className="admin-summary">
          <p>
            <strong>
              Usuarios:
            </strong>{" "}
            {usuarios.length}
          </p>

          <p>
            <strong>
              Roles:
            </strong>{" "}
            {roles.length}
          </p>

          <p>
            <strong>
              Permisos:
            </strong>{" "}
            {permisos.length}
          </p>

          <p>
            <strong>
              Asignaciones:
            </strong>{" "}
            {rolPermisos.length}
          </p>
        </div>

        {loading && (
          <p>Cargando...</p>
        )}

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

      <section className="card">
        <h3>
          {editingUsuarioId === null
            ? "Crear usuario"
            : "Editar usuario"}
        </h3>

        <form
          className="form-grid"
          onSubmit={handleUsuarioSubmit}
        >
          <label>
            Rol

            <select
              name="rol_id"
              value={
                usuarioForm.rol_id
              }
              onChange={
                handleUsuarioChange
              }
              required
            >
              <option value="">
                Seleccione un rol
              </option>

              {roles.map((rol) => (
                <option
                  key={rol.rol_id}
                  value={rol.rol_id}
                >
                  {rol.nombre_rol}
                </option>
              ))}
            </select>
          </label>

          <label>
            Nombre de usuario

            <input
              type="text"
              name="nombre_usuario"
              value={
                usuarioForm
                  .nombre_usuario
              }
              onChange={
                handleUsuarioChange
              }
              required
            />
          </label>

          <label>
            Correo de recuperación

            <input
              type="email"
              name="correo"
              value={
                usuarioForm.correo
              }
              onChange={
                handleUsuarioChange
              }
              placeholder="usuario@correo.com"
              autoComplete="email"
              required
            />
          </label>

          <label>
            {editingUsuarioId === null
              ? "Contraseña inicial"
              : "Nueva contraseña"}

            <input
              type="password"
              name="password"
              value={
                usuarioForm.password
              }
              onChange={
                handleUsuarioChange
              }
              minLength="8"
              required={
                editingUsuarioId === null
              }
              placeholder={
                editingUsuarioId === null
                  ? "Mínimo 8 caracteres"
                  : "Dejar vacío para conservar la actual"
              }
              autoComplete="new-password"
            />
          </label>

          <label>
            Estado

            <select
              name="estado"
              value={
                usuarioForm.estado
              }
              onChange={
                handleUsuarioChange
              }
              required
            >
              <option value="ACTIVO">
                ACTIVO
              </option>

              <option value="INACTIVO">
                INACTIVO
              </option>

              <option value="BLOQUEADO">
                BLOQUEADO
              </option>
            </select>
          </label>

          <div className="form-actions">
            <button
              type="submit"
              disabled={loading}
            >
              {editingUsuarioId === null
                ? "Guardar usuario"
                : "Actualizar"}
            </button>

            {editingUsuarioId !==
              null && (
              <button
                type="button"
                className="secondary-button"
                onClick={
                  handleCancelUsuarioEdit
                }
              >
                Cancelar
              </button>
            )}
          </div>
        </form>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Usuario</th>
                <th>Correo</th>
                <th>Rol</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {usuarios.map(
                (usuario) => (
                  <tr
                    key={
                      usuario.usuario_id
                    }
                  >
                    <td>
                      {
                        usuario.usuario_id
                      }
                    </td>

                    <td>
                      {
                        usuario.nombre_usuario
                      }
                    </td>

                    <td>
                      {usuario.correo ||
                        "Sin correo"}
                    </td>

                    <td>
                      {usuario.nombre_rol ||
                        getRolLabel(
                          usuario.rol_id
                        )}
                    </td>

                    <td>
                      <span
                        className={
                          getStatusBadgeClass(
                            usuario.estado
                          )
                        }
                      >
                        {usuario.estado}
                      </span>
                    </td>

                    <td>
                      <button
                        type="button"
                        className="small-button"
                        onClick={() =>
                          handleEditUsuario(
                            usuario
                          )
                        }
                      >
                        Editar
                      </button>

                      <button
                        type="button"
                        className="danger-button"
                        onClick={() =>
                          handleDeleteUsuario(
                            usuario.usuario_id
                          )
                        }
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                )
              )}

              {usuarios.length === 0 &&
                !loading && (
                  <tr>
                    <td colSpan="6">
                      No hay usuarios registrados.
                    </td>
                  </tr>
                )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <h3>
          {editingRolId === null
            ? "Crear rol"
            : "Editar rol"}
        </h3>

        <form
          className="form-grid"
          onSubmit={handleRolSubmit}
        >
          <label>
            Nombre del rol

            <input
              type="text"
              name="nombre_rol"
              value={
                rolForm.nombre_rol
              }
              onChange={
                handleRolChange
              }
              required
            />
          </label>

          <label>
            Descripción

            <textarea
              name="descripcion"
              value={
                rolForm.descripcion
              }
              onChange={
                handleRolChange
              }
              rows="3"
            />
          </label>

          <label>
            Estado

            <select
              name="estado"
              value={
                rolForm.estado
              }
              onChange={
                handleRolChange
              }
              required
            >
              <option value="ACTIVO">
                ACTIVO
              </option>

              <option value="INACTIVO">
                INACTIVO
              </option>
            </select>
          </label>

          <div className="form-actions">
            <button
              type="submit"
              disabled={loading}
            >
              {editingRolId === null
                ? "Guardar rol"
                : "Actualizar"}
            </button>

            {editingRolId !== null && (
              <button
                type="button"
                className="secondary-button"
                onClick={
                  handleCancelRolEdit
                }
              >
                Cancelar
              </button>
            )}
          </div>
        </form>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Rol</th>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {roles.map((rol) => (
                <tr key={rol.rol_id}>
                  <td>{rol.rol_id}</td>

                  <td>
                    {rol.nombre_rol}
                  </td>

                  <td>
                    {rol.descripcion}
                  </td>

                  <td>
                    <span
                      className={
                        getStatusBadgeClass(
                          rol.estado
                        )
                      }
                    >
                      {rol.estado}
                    </span>
                  </td>

                  <td>
                    <button
                      type="button"
                      className="small-button"
                      onClick={() =>
                        handleEditRol(rol)
                      }
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      className="danger-button"
                      onClick={() =>
                        handleDeleteRol(
                          rol.rol_id
                        )
                      }
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {roles.length === 0 &&
                !loading && (
                  <tr>
                    <td colSpan="5">
                      No hay roles registrados.
                    </td>
                  </tr>
                )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <h3>
          {editingPermisoId === null
            ? "Crear permiso"
            : "Editar permiso"}
        </h3>

        <form
          className="form-grid"
          onSubmit={
            handlePermisoSubmit
          }
        >
          <label>
            Código del permiso

            <input
              type="text"
              name="codigo_permiso"
              value={
                permisoForm
                  .codigo_permiso
              }
              onChange={
                handlePermisoChange
              }
              required
            />
          </label>

          <label>
            Módulo

            <input
              type="text"
              name="modulo"
              value={
                permisoForm.modulo
              }
              onChange={
                handlePermisoChange
              }
            />
          </label>

          <label>
            Descripción

            <textarea
              name="descripcion"
              value={
                permisoForm.descripcion
              }
              onChange={
                handlePermisoChange
              }
              rows="3"
            />
          </label>

          <div className="form-actions">
            <button
              type="submit"
              disabled={loading}
            >
              {editingPermisoId === null
                ? "Guardar permiso"
                : "Actualizar"}
            </button>

            {editingPermisoId !==
              null && (
              <button
                type="button"
                className="secondary-button"
                onClick={
                  handleCancelPermisoEdit
                }
              >
                Cancelar
              </button>
            )}
          </div>
        </form>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Código</th>
                <th>Módulo</th>
                <th>Descripción</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {permisos.map(
                (permiso) => (
                  <tr
                    key={
                      permiso.permiso_id
                    }
                  >
                    <td>
                      {
                        permiso.permiso_id
                      }
                    </td>

                    <td>
                      {
                        permiso.codigo_permiso
                      }
                    </td>

                    <td>
                      {permiso.modulo}
                    </td>

                    <td>
                      {permiso.descripcion}
                    </td>

                    <td>
                      <button
                        type="button"
                        className="small-button"
                        onClick={() =>
                          handleEditPermiso(
                            permiso
                          )
                        }
                      >
                        Editar
                      </button>

                      <button
                        type="button"
                        className="danger-button"
                        onClick={() =>
                          handleDeletePermiso(
                            permiso.permiso_id
                          )
                        }
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <h3>Permisos por rol</h3>

        <form
          className="form-grid"
          onSubmit={
            handleRolPermisoSubmit
          }
        >
          <label>
            Rol

            <select
              name="rol_id"
              value={
                rolPermisoForm.rol_id
              }
              onChange={
                handleRolPermisoChange
              }
              required
            >
              <option value="">
                Seleccione un rol
              </option>

              {roles.map((rol) => (
                <option
                  key={rol.rol_id}
                  value={rol.rol_id}
                >
                  {rol.nombre_rol}
                </option>
              ))}
            </select>
          </label>

          <label>
            Permiso

            <select
              name="permiso_id"
              value={
                rolPermisoForm.permiso_id
              }
              onChange={
                handleRolPermisoChange
              }
              required
            >
              <option value="">
                Seleccione un permiso
              </option>

              {permisos.map(
                (permiso) => (
                  <option
                    key={
                      permiso.permiso_id
                    }
                    value={
                      permiso.permiso_id
                    }
                  >
                    {
                      permiso.codigo_permiso
                    }
                  </option>
                )
              )}
            </select>
          </label>

          <div className="form-actions">
            <button
              type="submit"
              disabled={loading}
            >
              Asignar permiso
            </button>
          </div>
        </form>

        <div className="form-grid">
          <label>
            Revisar permisos de un rol

            <select
              value={selectedRoleId}
              onChange={
                handleSelectRoleForPermissions
              }
            >
              <option value="">
                Seleccione un rol
              </option>

              {roles.map((rol) => (
                <option
                  key={rol.rol_id}
                  value={rol.rol_id}
                >
                  {rol.nombre_rol}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Rol</th>
                <th>Permiso</th>
                <th>Módulo</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {(selectedRoleId
                ? selectedRolePermissions
                : rolPermisos
              ).map((item) => (
                <tr
                  key={
                    `${item.rol_id}-${item.permiso_id}`
                  }
                >
                  <td>
                    {item.nombre_rol ||
                      getRolLabel(
                        item.rol_id
                      )}
                  </td>

                  <td>
                    {item.codigo_permiso ||
                      getPermisoLabel(
                        item.permiso_id
                      )}
                  </td>

                  <td>
                    {item.modulo}
                  </td>

                  <td>
                    <button
                      type="button"
                      className="danger-button"
                      onClick={() =>
                        handleDeleteRolPermiso(
                          item.rol_id,
                          item.permiso_id
                        )
                      }
                    >
                      Quitar permiso
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}


export default Admin;