import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const DISCRETE_UNITS = [
  "UNIDAD",
  "CAJA",
  "PAQUETE"
];

const initialProductForm = {
  codigo: "",
  nombre: "",
  descripcion: "",
  stock_minimo: "",
  ubicacion: ""
};

function getTodayForInput() {
  const today = new Date();

  const year = today.getFullYear();

  const month = String(
    today.getMonth() + 1
  ).padStart(2, "0");

  const day = String(
    today.getDate()
  ).padStart(2, "0");

  return `${year}-${month}-${day}`;
}

function createInitialMovementForm() {
  return {
    insumo_id: "",
    usuario_id: "",
    tipo_movimiento: "SALIDA",
    cantidad: "",
    fecha_movimiento: getTodayForInput(),
    motivo: ""
  };
}

function InventarioStock() {
  const [stock, setStock] = useState([]);

  const [movimientos, setMovimientos] =
    useState([]);

  const [usuarios, setUsuarios] =
    useState([]);

  const [detallesCompra, setDetallesCompra] =
    useState([]);

  const [productForm, setProductForm] =
    useState(initialProductForm);

  const [movementForm, setMovementForm] =
    useState(
      () => createInitialMovementForm()
    );

  const [editingStock, setEditingStock] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [error, setError] =
    useState("");

  async function loadStock() {
    const data = await apiClient.get(
      "/inventario-stock"
    );

    setStock(data);
  }

  async function loadMovimientos() {
    const data = await apiClient.get(
      "/movimientos-inventario"
    );

    setMovimientos(data);
  }

  async function loadUsuarios() {
    const data = await apiClient.get(
      "/usuarios"
    );

    setUsuarios(data);
  }

  async function loadDetallesCompra() {
    const data = await apiClient.get(
      "/detalle-compra"
    );

    setDetallesCompra(data);
  }

  async function loadPageData() {
    try {
      setLoading(true);
      setError("");

      await Promise.all([
        loadStock(),
        loadMovimientos(),
        loadUsuarios(),
        loadDetallesCompra()
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

  function handleProductChange(event) {
    const { name, value } = event.target;

    setProductForm(
      (currentForm) => ({
        ...currentForm,
        [name]: value
      })
    );
  }

  function handleMovementChange(event) {
    const { name, value } = event.target;

    if (name === "insumo_id") {
      setMovementForm(
        (currentForm) => ({
          ...currentForm,
          insumo_id: value,
          cantidad: ""
        })
      );

      return;
    }

    if (name === "tipo_movimiento") {
      setMovementForm(
        (currentForm) => ({
          ...currentForm,
          tipo_movimiento: value,
          cantidad: ""
        })
      );

      return;
    }

    setMovementForm(
      (currentForm) => ({
        ...currentForm,
        [name]: value
      })
    );
  }

  function getStockByInsumoId(insumoId) {
    return stock.find(
      (item) =>
        String(item.insumo_id) ===
        String(insumoId)
    );
  }

  function getProductLabel(item) {
    if (!item) {
      return "";
    }

    return (
      `${item.insumo_codigo} - ` +
      `${item.insumo_nombre}`
    );
  }

  function getMovementProductLabel(
    movimiento
  ) {
    if (
      movimiento.insumo_codigo &&
      movimiento.insumo_nombre
    ) {
      return (
        `${movimiento.insumo_codigo} - ` +
        `${movimiento.insumo_nombre}`
      );
    }

    const stockItem =
      getStockByInsumoId(
        movimiento.insumo_id
      );

    if (stockItem) {
      return getProductLabel(
        stockItem
      );
    }

    return (
      `Producto ${movimiento.insumo_id}`
    );
  }

  function getUsuarioLabelById(usuarioId) {
    const usuario = usuarios.find(
      (item) =>
        String(item.usuario_id) ===
        String(usuarioId)
    );

    if (!usuario) {
      return usuarioId;
    }

    if (usuario.nombre_rol) {
      return (
        `${usuario.nombre_usuario} - ` +
        `${usuario.nombre_rol}`
      );
    }

    return usuario.nombre_usuario;
  }

  function isDiscreteUnit(unidadMedida) {
    return DISCRETE_UNITS.includes(
      String(
        unidadMedida || ""
      ).toUpperCase()
    );
  }

  function getQuantityStep(unidadMedida) {
    return isDiscreteUnit(
      unidadMedida
    )
      ? "1"
      : "0.01";
  }

  function getQuantityMinimum(
    unidadMedida
  ) {
    return isDiscreteUnit(
      unidadMedida
    )
      ? "1"
      : "0.01";
  }

  function validateQuantityForUnit(
    value,
    unidadMedida,
    fieldLabel
  ) {
    const quantity = Number(
      value
    );

    if (
      value === "" ||
      Number.isNaN(quantity)
    ) {
      return (
        `Debe indicar ${fieldLabel.toLowerCase()}.`
      );
    }

    if (quantity < 0) {
      return (
        `${fieldLabel} no puede ser negativo.`
      );
    }

    if (
      isDiscreteUnit(unidadMedida) &&
      !Number.isInteger(quantity)
    ) {
      return (
        `${fieldLabel} debe ser un número entero ` +
        `porque la unidad es ${unidadMedida}.`
      );
    }

    return null;
  }

  function getLatestCostByInsumoId(
    insumoId
  ) {
    const details = detallesCompra
      .filter(
        (detalle) =>
          String(detalle.insumo_id) ===
          String(insumoId)
      )
      .sort(
        (first, second) =>
          Number(
            second.detalle_compra_id
          ) -
          Number(
            first.detalle_compra_id
          )
      );

    if (details.length === 0) {
      return null;
    }

    return Number(
      details[0].costo_unitario
    );
  }

  function getInventoryValue(item) {
    const latestCost =
      getLatestCostByInsumoId(
        item.insumo_id
      );

    if (latestCost === null) {
      return null;
    }

    return (
      Number(item.stock_actual || 0) *
      latestCost
    );
  }

  function formatCurrency(value) {
    return new Intl.NumberFormat(
      "es-CR",
      {
        style: "currency",
        currency: "CRC",
        maximumFractionDigits: 2
      }
    ).format(
      Number(value || 0)
    );
  }

  function isLowStock(item) {
    if (
      item.stock_minimo === null ||
      item.stock_minimo === undefined
    ) {
      return false;
    }

    return (
      Number(item.stock_actual) <=
      Number(item.stock_minimo)
    );
  }

  function handleEditProduct(item) {
    setEditingStock(item);

    setProductForm({
      codigo:
        item.insumo_codigo || "",

      nombre:
        item.insumo_nombre || "",

      descripcion:
        item.insumo_descripcion || "",

      stock_minimo:
        item.stock_minimo ?? "",

      ubicacion:
        item.ubicacion || ""
    });

    setMessage("");
    setError("");

    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }

  function handleCancelProductEdit() {
    setEditingStock(null);

    setProductForm(
      initialProductForm
    );

    setMessage("");
    setError("");
  }

  async function handleProductSubmit(
    event
  ) {
    event.preventDefault();

    if (!editingStock) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      if (!productForm.codigo.trim()) {
        throw new Error(
          "El código del producto es obligatorio."
        );
      }

      if (!productForm.nombre.trim()) {
        throw new Error(
          "El nombre del producto es obligatorio."
        );
      }

      if (
        productForm.stock_minimo !== ""
      ) {
        const validationError =
          validateQuantityForUnit(
            productForm.stock_minimo,
            editingStock.unidad_medida,
            "El stock mínimo"
          );

        if (validationError) {
          throw new Error(
            validationError
          );
        }
      }

      const payload = {
        codigo:
          productForm.codigo.trim(),

        nombre:
          productForm.nombre.trim(),

        descripcion:
          productForm.descripcion
            .trim() || null,

        stock_minimo:
          productForm.stock_minimo === ""
            ? null
            : Number(
                productForm.stock_minimo
              ),

        ubicacion:
          productForm.ubicacion
            .trim() || null
      };

      const result = await apiClient.put(
        `/inventario-stock/${editingStock.stock_id}/producto`,
        payload
      );

      setMessage(
        result.message ||
          "Producto actualizado correctamente."
      );

      setEditingStock(null);

      setProductForm(
        initialProductForm
      );

      await loadStock();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleToggleProductStatus(
    item
  ) {
    const currentStatus = String(
      item.insumo_estado || "ACTIVO"
    ).toUpperCase();

    const newStatus =
      currentStatus === "ACTIVO"
        ? "INACTIVO"
        : "ACTIVO";

    const action =
      newStatus === "INACTIVO"
        ? "desactivar"
        : "reactivar";

    const confirmed = window.confirm(
      `¿Seguro que desea ${action} ` +
        `${getProductLabel(item)}?\n\n` +
        (
          newStatus === "INACTIVO"
            ? "El producto conservará toda su información histórica."
            : "El producto volverá a estar disponible para operaciones normales."
        )
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const result = await apiClient.put(
        `/inventario-stock/${item.stock_id}/estado`,
        {
          estado: newStatus
        }
      );

      setMessage(
        result.message ||
          "Estado actualizado correctamente."
      );

      if (
        editingStock?.stock_id ===
        item.stock_id
      ) {
        setEditingStock(null);

        setProductForm(
          initialProductForm
        );
      }

      await loadStock();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function getProjectedStock() {
    const selectedStock =
      getStockByInsumoId(
        movementForm.insumo_id
      );

    if (!selectedStock) {
      return null;
    }

    const currentStock = Number(
      selectedStock.stock_actual || 0
    );

    const quantity = Number(
      movementForm.cantidad || 0
    );

    if (
      movementForm.tipo_movimiento ===
      "ENTRADA"
    ) {
      return (
        currentStock + quantity
      );
    }

    if (
      movementForm.tipo_movimiento ===
      "SALIDA"
    ) {
      return (
        currentStock - quantity
      );
    }

    if (
      movementForm.tipo_movimiento ===
      "AJUSTE"
    ) {
      return quantity;
    }

    return null;
  }

  function getMovementHelperText() {
    if (
      movementForm.tipo_movimiento ===
      "ENTRADA"
    ) {
      return (
        "Use ENTRADA manual solo para casos excepcionales, " +
        "como devoluciones o inventario recibido fuera del " +
        "proceso normal de compras."
      );
    }

    if (
      movementForm.tipo_movimiento ===
      "SALIDA"
    ) {
      return (
        "Use SALIDA para consumo interno, pérdida, daño, " +
        "vencimiento u otra reducción de existencias."
      );
    }

    return (
      "AJUSTE reemplaza el stock actual por la cantidad " +
      "indicada después de un conteo físico."
    );
  }

  function getReasonPlaceholder() {
    if (
      movementForm.tipo_movimiento ===
      "ENTRADA"
    ) {
      return (
        "Ejemplo: Devolución al inventario"
      );
    }

    if (
      movementForm.tipo_movimiento ===
      "SALIDA"
    ) {
      return (
        "Ejemplo: Material vencido o consumo interno"
      );
    }

    return (
      "Ejemplo: Resultado del conteo físico mensual"
    );
  }

  function validateMovementForm() {
    if (!movementForm.insumo_id) {
      return (
        "Debe seleccionar un producto."
      );
    }

    if (!movementForm.usuario_id) {
      return (
        "Debe seleccionar el usuario responsable."
      );
    }

    const selectedStock =
      getStockByInsumoId(
        movementForm.insumo_id
      );

    if (!selectedStock) {
      return (
        "No se encontró el producto seleccionado."
      );
    }

    const quantity = Number(
      movementForm.cantidad
    );

    if (
      movementForm.cantidad === "" ||
      quantity <= 0
    ) {
      return (
        "La cantidad debe ser mayor a cero."
      );
    }

    if (
      isDiscreteUnit(
        selectedStock.unidad_medida
      ) &&
      !Number.isInteger(quantity)
    ) {
      return (
        "La cantidad debe ser un número entero " +
        `porque la unidad es ${selectedStock.unidad_medida}.`
      );
    }

    if (
      movementForm.tipo_movimiento ===
      "SALIDA" &&
      quantity >
        Number(
          selectedStock.stock_actual
        )
    ) {
      return (
        "No hay suficiente stock para registrar esta salida."
      );
    }

    if (
      !movementForm.motivo.trim()
    ) {
      return (
        "Debe indicar el motivo del movimiento manual."
      );
    }

    return null;
  }

  async function handleMovementSubmit(
    event
  ) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const validationError =
        validateMovementForm();

      if (validationError) {
        throw new Error(
          validationError
        );
      }

      const payload = {
        insumo_id: Number(
          movementForm.insumo_id
        ),

        usuario_id: Number(
          movementForm.usuario_id
        ),

        detalle_compra_id: null,

        consulta_id: null,

        tipo_movimiento:
          movementForm.tipo_movimiento,

        cantidad: Number(
          movementForm.cantidad
        ),

        fecha_movimiento:
          movementForm.fecha_movimiento ||
          null,

        motivo:
          movementForm.motivo.trim()
      };

      await apiClient.post(
        "/movimientos-inventario",
        payload
      );

      setMovementForm(
        createInitialMovementForm()
      );

      setMessage(
        "Movimiento de inventario registrado correctamente."
      );

      await Promise.all([
        loadStock(),
        loadMovimientos()
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function getMovementBadgeClass(
    tipoMovimiento
  ) {
    if (tipoMovimiento === "ENTRADA") {
      return "badge success-badge";
    }

    if (tipoMovimiento === "SALIDA") {
      return "badge danger-badge";
    }

    return "badge warning-badge";
  }

  function getMovementOrigin(
    movimiento
  ) {
    if (
      movimiento.detalle_compra_id !==
        null &&
      movimiento.detalle_compra_id !==
        undefined
    ) {
      return "Compra automática";
    }

    return "Manual";
  }

  function canReverseMovement(
    movimiento
  ) {
    const isAutomaticPurchase =
      movimiento.detalle_compra_id !==
        null &&
      movimiento.detalle_compra_id !==
        undefined;

    const isAdjustment =
      movimiento.tipo_movimiento ===
      "AJUSTE";

    return (
      !isAutomaticPurchase &&
      !isAdjustment
    );
  }

  async function handleReverseMovement(
    movimiento
  ) {
    if (
      !canReverseMovement(movimiento)
    ) {
      return;
    }

    const confirmed = window.confirm(
      "¿Seguro que desea revertir este movimiento?\n\n" +
        "Esta acción modificará el stock actual."
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      await apiClient.delete(
        `/movimientos-inventario/${movimiento.movimiento_id}`
      );

      setMessage(
        "Movimiento revertido correctamente."
      );

      await Promise.all([
        loadStock(),
        loadMovimientos()
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const activeUsers = usuarios.filter(
    (usuario) =>
      String(usuario.estado || "")
        .toUpperCase() === "ACTIVO"
  );

  const selectableUsers =
    activeUsers.length > 0
      ? activeUsers
      : usuarios;

  const selectedMovementStock =
    getStockByInsumoId(
      movementForm.insumo_id
    );

  const movementUnit =
    selectedMovementStock
      ?.unidad_medida || "";

  const projectedStock =
    getProjectedStock();

  const quantityLabel =
    movementForm.tipo_movimiento ===
    "AJUSTE"
      ? movementUnit
        ? `Nuevo stock resultante (${movementUnit})`
        : "Nuevo stock resultante"
      : movementUnit
        ? `Cantidad (${movementUnit})`
        : "Cantidad";

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Stock e Inventario</h2>

          <p>
            Administración de productos, existencias,
            costos y movimientos de inventario.
          </p>
        </div>
      </div>

      {message && (
        <section className="card">
          <p className="success-message">
            {message}
          </p>
        </section>
      )}

      {error && (
        <section className="card">
          <p className="error-message">
            {error}
          </p>
        </section>
      )}

      {editingStock && (
        <section className="card">
          <h3>Editar producto</h3>

          <p className="helper-text">
            Modifique la información general del producto
            y su configuración de inventario. El stock
            actual solo cambia mediante compras o
            movimientos.
          </p>

          <form
            className="form-grid"
            onSubmit={handleProductSubmit}
          >
            <label>
              Código

              <input
                type="text"
                name="codigo"
                value={productForm.codigo}
                onChange={
                  handleProductChange
                }
                required
              />
            </label>

            <label>
              Nombre

              <input
                type="text"
                name="nombre"
                value={productForm.nombre}
                onChange={
                  handleProductChange
                }
                required
              />
            </label>

            <label>
              Descripción

              <textarea
                name="descripcion"
                value={
                  productForm.descripcion
                }
                onChange={
                  handleProductChange
                }
                rows="3"
                placeholder="Opcional"
              />
            </label>

            <label>
              Unidad de medida

              <input
                type="text"
                value={
                  editingStock.unidad_medida
                }
                readOnly
              />
            </label>

            <label>
              Stock actual

              <input
                type="text"
                value={
                  `${editingStock.stock_actual} ${editingStock.unidad_medida}`
                }
                readOnly
              />
            </label>

            <label>
              Stock mínimo

              <input
                type="number"
                name="stock_minimo"
                value={
                  productForm.stock_minimo
                }
                onChange={
                  handleProductChange
                }
                min="0"
                step={getQuantityStep(
                  editingStock.unidad_medida
                )}
                placeholder="Opcional"
              />
            </label>

            <label>
              Ubicación

              <input
                type="text"
                name="ubicacion"
                value={
                  productForm.ubicacion
                }
                onChange={
                  handleProductChange
                }
                placeholder="Ejemplo: Bodega principal"
              />
            </label>

            <div className="clinical-summary">
              <p>
                <strong>
                  Estado actual:
                </strong>{" "}
                {editingStock.insumo_estado}
              </p>

              <p>
                <strong>
                  Unidad:
                </strong>{" "}
                {editingStock.unidad_medida}
              </p>

              <p>
                <strong>
                  Nota:
                </strong>{" "}
                La unidad de medida se conserva para
                mantener consistentes las compras y
                movimientos históricos.
              </p>
            </div>

            <div className="form-actions">
              <button
                type="submit"
                disabled={loading}
              >
                Guardar cambios
              </button>

              <button
                type="button"
                className="secondary-button"
                onClick={
                  handleCancelProductEdit
                }
              >
                Cancelar
              </button>
            </div>
          </form>
        </section>
      )}

      <section className="card">
        <h3>Registrar movimiento manual</h3>

        <p className="helper-text">
          Las compras generan entradas automáticamente.
          Use esta sección para salidas, entradas
          excepcionales o ajustes derivados de un
          conteo físico.
        </p>

        <form
          className="form-grid"
          onSubmit={handleMovementSubmit}
        >
          <label>
            Producto

            <select
              name="insumo_id"
              value={
                movementForm.insumo_id
              }
              onChange={
                handleMovementChange
              }
              required
            >
              <option value="">
                Seleccione un producto
              </option>

              {stock.map((item) => (
                <option
                  key={item.stock_id}
                  value={item.insumo_id}
                >
                  {getProductLabel(item)}

                  {item.insumo_estado ===
                  "INACTIVO"
                    ? " (INACTIVO)"
                    : ""}
                </option>
              ))}
            </select>
          </label>

          <label>
            Unidad de medida

            <input
              type="text"
              value={movementUnit}
              placeholder="Seleccione un producto"
              readOnly
            />
          </label>

          <label>
            Tipo de movimiento

            <select
              name="tipo_movimiento"
              value={
                movementForm.tipo_movimiento
              }
              onChange={
                handleMovementChange
              }
              required
            >
              <option value="SALIDA">
                SALIDA
              </option>

              <option value="ENTRADA">
                ENTRADA MANUAL
              </option>

              <option value="AJUSTE">
                AJUSTE POR CONTEO
              </option>
            </select>
          </label>

          <label>
            {quantityLabel}

            <input
              type="number"
              name="cantidad"
              value={
                movementForm.cantidad
              }
              onChange={
                handleMovementChange
              }
              min={getQuantityMinimum(
                movementUnit
              )}
              step={getQuantityStep(
                movementUnit
              )}
              required
            />
          </label>

          <label>
            Usuario responsable

            <select
              name="usuario_id"
              value={
                movementForm.usuario_id
              }
              onChange={
                handleMovementChange
              }
              required
            >
              <option value="">
                Seleccione un usuario
              </option>

              {selectableUsers.map(
                (usuario) => (
                  <option
                    key={usuario.usuario_id}
                    value={usuario.usuario_id}
                  >
                    {usuario.nombre_usuario}

                    {usuario.nombre_rol
                      ? ` - ${usuario.nombre_rol}`
                      : ""}
                  </option>
                )
              )}
            </select>
          </label>

          <label>
            Fecha

            <input
              type="date"
              name="fecha_movimiento"
              value={
                movementForm.fecha_movimiento
              }
              onChange={
                handleMovementChange
              }
              required
            />
          </label>

          <label>
            Motivo

            <textarea
              name="motivo"
              value={movementForm.motivo}
              onChange={
                handleMovementChange
              }
              rows="3"
              placeholder={
                getReasonPlaceholder()
              }
              required
            />
          </label>

          <div className="clinical-summary">
            <p>
              <strong>
                Stock actual:
              </strong>{" "}
              {selectedMovementStock
                ? selectedMovementStock
                    .stock_actual
                : "Seleccione un producto"}
            </p>

            <p>
              <strong>
                Stock resultante:
              </strong>{" "}
              {projectedStock === null
                ? "Sin calcular"
                : projectedStock}
            </p>

            <p>
              <strong>
                Regla de cantidad:
              </strong>{" "}
              {movementUnit
                ? isDiscreteUnit(
                    movementUnit
                  )
                  ? "Solo números enteros"
                  : "Se permiten decimales"
                : "Seleccione un producto"}
            </p>

            {selectedMovementStock
              ?.insumo_estado ===
              "INACTIVO" && (
              <p>
                <strong>
                  Producto inactivo:
                </strong>{" "}
                utilice movimientos solamente para
                gestionar existencias remanentes o
                correcciones.
              </p>
            )}
          </div>

          <p className="helper-text">
            {getMovementHelperText()}
          </p>

          <div className="form-actions">
            <button
              type="submit"
              disabled={loading}
            >
              Registrar movimiento
            </button>
          </div>
        </form>
      </section>

      <section className="card">
        <h3>Stock actual</h3>

        {loading && (
          <p>Cargando...</p>
        )}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Producto</th>
                <th>Estado producto</th>
                <th>Unidad</th>
                <th>Stock actual</th>
                <th>Stock mínimo</th>
                <th>Último costo</th>
                <th>Valor aproximado</th>
                <th>Ubicación</th>
                <th>Nivel</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {stock.map((item) => {
                const latestCost =
                  getLatestCostByInsumoId(
                    item.insumo_id
                  );

                const inventoryValue =
                  getInventoryValue(item);

                const isActive =
                  item.insumo_estado ===
                  "ACTIVO";

                return (
                  <tr key={item.stock_id}>
                    <td>
                      {item.stock_id}
                    </td>

                    <td>
                      {getProductLabel(item)}
                    </td>

                    <td>
                      <span
                        className={
                          isActive
                            ? "badge success-badge"
                            : "badge danger-badge"
                        }
                      >
                        {item.insumo_estado}
                      </span>
                    </td>

                    <td>
                      {item.unidad_medida}
                    </td>

                    <td>
                      {item.stock_actual}
                    </td>

                    <td>
                      {item.stock_minimo ??
                        "No definido"}
                    </td>

                    <td>
                      {latestCost === null
                        ? "Sin compras"
                        : formatCurrency(
                            latestCost
                          )}
                    </td>

                    <td>
                      {inventoryValue === null
                        ? "Sin costo disponible"
                        : formatCurrency(
                            inventoryValue
                          )}
                    </td>

                    <td>
                      {item.ubicacion ||
                        "No definida"}
                    </td>

                    <td>
                      {isLowStock(item) ? (
                        <span className="badge danger-badge">
                          Bajo mínimo
                        </span>
                      ) : (
                        <span className="badge success-badge">
                          Disponible
                        </span>
                      )}
                    </td>

                    <td>
                      <button
                        type="button"
                        className="small-button"
                        onClick={() =>
                          handleEditProduct(item)
                        }
                      >
                        Editar producto
                      </button>

                      <button
                        type="button"
                        className={
                          isActive
                            ? "danger-button"
                            : "small-button"
                        }
                        onClick={() =>
                          handleToggleProductStatus(
                            item
                          )
                        }
                      >
                        {isActive
                          ? "Desactivar"
                          : "Reactivar"}
                      </button>
                    </td>
                  </tr>
                );
              })}

              {stock.length === 0 &&
                !loading && (
                  <tr>
                    <td colSpan="11">
                      No hay registros de stock.
                    </td>
                  </tr>
                )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <h3>Historial de movimientos</h3>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Producto</th>
                <th>Origen</th>
                <th>Tipo</th>
                <th>Cantidad</th>
                <th>Usuario responsable</th>
                <th>Fecha</th>
                <th>Motivo</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {movimientos.map(
                (movimiento) => (
                  <tr
                    key={
                      movimiento.movimiento_id
                    }
                  >
                    <td>
                      {
                        movimiento.movimiento_id
                      }
                    </td>

                    <td>
                      {getMovementProductLabel(
                        movimiento
                      )}
                    </td>

                    <td>
                      {getMovementOrigin(
                        movimiento
                      )}
                    </td>

                    <td>
                      <span
                        className={
                          getMovementBadgeClass(
                            movimiento
                              .tipo_movimiento
                          )
                        }
                      >
                        {
                          movimiento
                            .tipo_movimiento
                        }
                      </span>
                    </td>

                    <td>
                      {movimiento.cantidad}
                    </td>

                    <td>
                      {movimiento.nombre_usuario ||
                        getUsuarioLabelById(
                          movimiento.usuario_id
                        )}
                    </td>

                    <td>
                      {movimiento.fecha_movimiento
                        ? movimiento
                            .fecha_movimiento
                            .substring(0, 10)
                        : ""}
                    </td>

                    <td>
                      {movimiento.motivo ||
                        "Sin motivo"}
                    </td>

                    <td>
                      {canReverseMovement(
                        movimiento
                      ) ? (
                        <button
                          type="button"
                          className="danger-button"
                          onClick={() =>
                            handleReverseMovement(
                              movimiento
                            )
                          }
                        >
                          Revertir
                        </button>
                      ) : movimiento
                          .detalle_compra_id !==
                          null &&
                        movimiento
                          .detalle_compra_id !==
                          undefined ? (
                        <span className="helper-text">
                          Automático
                        </span>
                      ) : (
                        <span className="helper-text">
                          No reversible
                        </span>
                      )}
                    </td>
                  </tr>
                )
              )}

              {movimientos.length === 0 && (
                <tr>
                  <td colSpan="9">
                    No hay movimientos registrados.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}

export default InventarioStock;