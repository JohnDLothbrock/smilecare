import { useEffect, useState } from "react";

import { apiClient } from "../api/apiClient.js";

const DISCRETE_UNITS = [
  "UNIDAD",
  "CAJA",
  "PAQUETE"
];

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

function createInitialPurchaseForm() {
  return {
    proveedor_id: "",
    usuario_id: "",
    fecha_compra: getTodayForInput()
  };
}

const initialItemForm = {
  modo: "EXISTENTE",

  insumo_id: "",

  codigo: "",
  nombre: "",
  descripcion: "",
  unidad_medida: "",

  cantidad: "",
  costo_unitario: ""
};

function Compras() {
  const [compras, setCompras] = useState([]);

  const [proveedores, setProveedores] =
    useState([]);

  const [usuarios, setUsuarios] = useState([]);

  const [insumos, setInsumos] = useState([]);

  const [detallesCompra, setDetallesCompra] =
    useState([]);

  const [purchaseForm, setPurchaseForm] =
    useState(
      () => createInitialPurchaseForm()
    );

  const [itemForm, setItemForm] = useState(
    initialItemForm
  );

  const [purchaseItems, setPurchaseItems] =
    useState([]);

  const [
    editingItemIndex,
    setEditingItemIndex
  ] = useState(null);

  const [
    selectedCompraId,
    setSelectedCompraId
  ] = useState("");

  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState("");

  const [error, setError] = useState("");

  async function loadCompras() {
    const data = await apiClient.get(
      "/compras"
    );

    setCompras(data);
  }

  async function loadProveedores() {
    const data = await apiClient.get(
      "/proveedores"
    );

    setProveedores(data);
  }

  async function loadUsuarios() {
    const data = await apiClient.get(
      "/usuarios"
    );

    setUsuarios(data);
  }

  async function loadInsumos() {
    const data = await apiClient.get(
      "/insumos"
    );

    setInsumos(data);
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
        loadCompras(),
        loadProveedores(),
        loadUsuarios(),
        loadInsumos(),
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

  function handlePurchaseChange(event) {
    const { name, value } = event.target;

    setPurchaseForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function handleItemChange(event) {
    const { name, value } = event.target;

    if (name === "modo") {
      setItemForm({
        ...initialItemForm,
        modo: value
      });

      setEditingItemIndex(null);

      return;
    }

    if (name === "insumo_id") {
      const latestDetail =
        getLatestDetailForInsumo(
          value
        );

      setItemForm((currentForm) => ({
        ...currentForm,
        insumo_id: value,
        costo_unitario:
          latestDetail?.costo_unitario ?? ""
      }));

      return;
    }

    setItemForm((currentForm) => ({
      ...currentForm,
      [name]: value
    }));
  }

  function getInsumoById(insumoId) {
    return insumos.find(
      (insumo) =>
        String(insumo.insumo_id) ===
        String(insumoId)
    );
  }

  function getLatestDetailForInsumo(
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

    return details[0] || null;
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

  function getUnitLabel(unidadMedida) {
    const labels = {
      UNIDAD: "unidad",
      CAJA: "caja",
      PAQUETE: "paquete",
      ML: "ml",
      GRAMOS: "gramo"
    };

    return (
      labels[unidadMedida] ||
      String(
        unidadMedida || "unidad"
      ).toLowerCase()
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

  function getCurrentUnit() {
    if (itemForm.modo === "EXISTENTE") {
      const insumo = getInsumoById(
        itemForm.insumo_id
      );

      return insumo?.unidad_medida || "";
    }

    return itemForm.unidad_medida;
  }

  function getCurrentSubtotal() {
    return (
      Number(itemForm.cantidad || 0) *
      Number(
        itemForm.costo_unitario || 0
      )
    );
  }

  function getPurchaseItemName(item) {
    if (item.modo === "EXISTENTE") {
      const insumo = getInsumoById(
        item.insumo_id
      );

      if (!insumo) {
        return item.insumo_id;
      }

      return (
        `${insumo.codigo} - ` +
        `${insumo.nombre}`
      );
    }

    return (
      `${item.nuevo_insumo.codigo} - ` +
      `${item.nuevo_insumo.nombre}`
    );
  }

  function getPurchaseItemUnit(item) {
    if (item.modo === "EXISTENTE") {
      const insumo = getInsumoById(
        item.insumo_id
      );

      return insumo?.unidad_medida || "";
    }

    return (
      item.nuevo_insumo.unidad_medida
    );
  }

  function getItemSubtotal(item) {
    return (
      Number(item.cantidad || 0) *
      Number(
        item.costo_unitario || 0
      )
    );
  }

  function getPurchaseTotal() {
    return purchaseItems.reduce(
      (total, item) =>
        total + getItemSubtotal(item),
      0
    );
  }

  function validateItem() {
    if (
      itemForm.modo === "EXISTENTE"
    ) {
      if (!itemForm.insumo_id) {
        return (
          "Debe seleccionar un producto existente."
        );
      }
    }

    if (itemForm.modo === "NUEVO") {
      if (!itemForm.codigo.trim()) {
        return (
          "Debe indicar el código del nuevo producto."
        );
      }

      if (!itemForm.nombre.trim()) {
        return (
          "Debe indicar el nombre del nuevo producto."
        );
      }

      if (!itemForm.unidad_medida) {
        return (
          "Debe seleccionar la unidad de medida."
        );
      }

      const codeAlreadyExists =
        insumos.some(
          (insumo) =>
            String(insumo.codigo)
              .toUpperCase() ===
            itemForm.codigo
              .trim()
              .toUpperCase()
        );

      if (codeAlreadyExists) {
        return (
          "Ese código ya existe. " +
          "Seleccione el producto existente."
        );
      }
    }

    const quantity = Number(
      itemForm.cantidad
    );

    if (
      itemForm.cantidad === "" ||
      quantity <= 0
    ) {
      return (
        "La cantidad debe ser mayor a cero."
      );
    }

    const currentUnit =
      getCurrentUnit();

    if (
      isDiscreteUnit(currentUnit) &&
      !Number.isInteger(quantity)
    ) {
      return (
        `La cantidad debe ser un número entero ` +
        `porque la unidad de medida es ${currentUnit}.`
      );
    }

    if (
      itemForm.costo_unitario === "" ||
      Number(
        itemForm.costo_unitario
      ) < 0
    ) {
      return (
        "Debe indicar un costo válido."
      );
    }

    return null;
  }

  function isDuplicateItem(
    candidateItem
  ) {
    return purchaseItems.some(
      (item, index) => {
        if (
          index === editingItemIndex
        ) {
          return false;
        }

        if (
          candidateItem.modo ===
            "EXISTENTE" &&
          item.modo === "EXISTENTE"
        ) {
          return (
            String(
              candidateItem.insumo_id
            ) ===
            String(item.insumo_id)
          );
        }

        if (
          candidateItem.modo ===
            "NUEVO" &&
          item.modo === "NUEVO"
        ) {
          return (
            candidateItem.nuevo_insumo
              .codigo
              .toUpperCase() ===
            item.nuevo_insumo.codigo
              .toUpperCase()
          );
        }

        return false;
      }
    );
  }

  function handleAddItem(event) {
    event.preventDefault();

    setError("");
    setMessage("");

    const validationError =
      validateItem();

    if (validationError) {
      setError(validationError);

      return;
    }

    let newItem;

    if (
      itemForm.modo === "EXISTENTE"
    ) {
      newItem = {
        modo: "EXISTENTE",

        insumo_id: Number(
          itemForm.insumo_id
        ),

        nuevo_insumo: null,

        cantidad: Number(
          itemForm.cantidad
        ),

        costo_unitario: Number(
          itemForm.costo_unitario
        )
      };
    } else {
      newItem = {
        modo: "NUEVO",

        insumo_id: null,

        nuevo_insumo: {
          codigo:
            itemForm.codigo.trim(),

          nombre:
            itemForm.nombre.trim(),

          descripcion:
            itemForm.descripcion
              .trim() || null,

          unidad_medida:
            itemForm.unidad_medida,

          estado: "ACTIVO"
        },

        cantidad: Number(
          itemForm.cantidad
        ),

        costo_unitario: Number(
          itemForm.costo_unitario
        )
      };
    }

    if (isDuplicateItem(newItem)) {
      setError(
        "Ese producto ya fue agregado a la compra."
      );

      return;
    }

    if (
      editingItemIndex === null
    ) {
      setPurchaseItems(
        (currentItems) => [
          ...currentItems,
          newItem
        ]
      );
    } else {
      setPurchaseItems(
        (currentItems) =>
          currentItems.map(
            (item, index) =>
              index === editingItemIndex
                ? newItem
                : item
          )
      );
    }

    setItemForm(initialItemForm);

    setEditingItemIndex(null);
  }

  function handleEditItem(index) {
    const item = purchaseItems[
      index
    ];

    setEditingItemIndex(index);

    if (
      item.modo === "EXISTENTE"
    ) {
      setItemForm({
        ...initialItemForm,

        modo: "EXISTENTE",

        insumo_id: String(
          item.insumo_id
        ),

        cantidad: String(
          item.cantidad
        ),

        costo_unitario: String(
          item.costo_unitario
        )
      });

      return;
    }

    setItemForm({
      modo: "NUEVO",

      insumo_id: "",

      codigo:
        item.nuevo_insumo.codigo,

      nombre:
        item.nuevo_insumo.nombre,

      descripcion:
        item.nuevo_insumo.descripcion ||
        "",

      unidad_medida:
        item.nuevo_insumo.unidad_medida,

      cantidad: String(
        item.cantidad
      ),

      costo_unitario: String(
        item.costo_unitario
      )
    });
  }

  function handleRemoveItem(index) {
    setPurchaseItems(
      (currentItems) =>
        currentItems.filter(
          (_, itemIndex) =>
            itemIndex !== index
        )
    );

    if (
      editingItemIndex === index
    ) {
      setEditingItemIndex(null);

      setItemForm(
        initialItemForm
      );
    }
  }

  function handleCancelItemEdit() {
    setEditingItemIndex(null);

    setItemForm(initialItemForm);

    setError("");
  }

  function resetPurchaseForm() {
    setPurchaseForm(
      createInitialPurchaseForm()
    );

    setItemForm(initialItemForm);

    setPurchaseItems([]);

    setEditingItemIndex(null);
  }

  async function handleSubmitPurchase() {
    try {
      setLoading(true);
      setMessage("");
      setError("");

      if (
        !purchaseForm.proveedor_id
      ) {
        throw new Error(
          "Debe seleccionar un proveedor."
        );
      }

      if (
        !purchaseForm.usuario_id
      ) {
        throw new Error(
          "Debe seleccionar el usuario responsable."
        );
      }

      if (
        purchaseItems.length === 0
      ) {
        throw new Error(
          "Debe agregar al menos un producto."
        );
      }

      const payload = {
        proveedor_id: Number(
          purchaseForm.proveedor_id
        ),

        usuario_id: Number(
          purchaseForm.usuario_id
        ),

        fecha_compra:
          purchaseForm.fecha_compra ||
          null,

        items: purchaseItems.map(
          (item) => ({
            insumo_id:
              item.modo === "EXISTENTE"
                ? Number(
                    item.insumo_id
                  )
                : null,

            nuevo_insumo:
              item.modo === "NUEVO"
                ? item.nuevo_insumo
                : null,

            cantidad: Number(
              item.cantidad
            ),

            costo_unitario: Number(
              item.costo_unitario
            )
          })
        )
      };

      const result =
        await apiClient.post(
          "/compras/completa",
          payload
        );

      const newCompraId =
        result.compra?.compra_id;

      if (newCompraId) {
        setSelectedCompraId(
          String(newCompraId)
        );
      }

      resetPurchaseForm();

      setMessage(
        result.message ||
          "Compra registrada correctamente."
      );

      await loadPageData();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function getDetailsByCompraId(
    compraId
  ) {
    return detallesCompra.filter(
      (detalle) =>
        String(detalle.compra_id) ===
        String(compraId)
    );
  }

  function handleSelectCompra(
    compraId
  ) {
    setSelectedCompraId(
      String(compraId)
    );

    setError("");
  }

  const activeUsers =
    usuarios.filter(
      (usuario) =>
        String(usuario.estado || "")
          .toUpperCase() ===
        "ACTIVO"
    );

  const selectableUsers =
    activeUsers.length > 0
      ? activeUsers
      : usuarios;

  const activeProviders =
    proveedores.filter(
      (proveedor) =>
        String(proveedor.estado || "")
          .toUpperCase() !==
        "INACTIVO"
    );

  const selectableProviders =
    activeProviders.length > 0
      ? activeProviders
      : proveedores;

  const activeInsumos =
    insumos.filter(
      (insumo) =>
        String(insumo.estado || "")
          .toUpperCase() ===
        "ACTIVO"
    );

  const selectableInsumos =
    activeInsumos.length > 0
      ? activeInsumos
      : insumos;

  const selectedInsumo =
    itemForm.modo === "EXISTENTE"
      ? getInsumoById(
          itemForm.insumo_id
        )
      : null;

  const latestDetail =
    itemForm.modo === "EXISTENTE" &&
    itemForm.insumo_id
      ? getLatestDetailForInsumo(
          itemForm.insumo_id
        )
      : null;

  const currentUnit =
    getCurrentUnit();

  const quantityStep =
    isDiscreteUnit(currentUnit)
      ? "1"
      : "0.01";

  const quantityMinimum =
    isDiscreteUnit(currentUnit)
      ? "1"
      : "0.01";

  const selectedCompra =
    compras.find(
      (compra) =>
        String(compra.compra_id) ===
        String(selectedCompraId)
    );

  const selectedCompraDetails =
    selectedCompraId
      ? getDetailsByCompraId(
          selectedCompraId
        )
      : [];

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Registro de Productos/Insumos</h2>

          <p>
            Registro de productos comprados,
            nuevos insumos y entradas al inventario.
          </p>
        </div>
      </div>

      <section className="card">
        <h3>Registrar compra de Producto</h3>

        <p className="helper-text">
          Registre el proveedor y los productos
          recibidos. Puede seleccionar productos
          existentes o registrar productos nuevos
          sin salir de esta pantalla.
        </p>

        <div className="form-grid">
          <label>
            Proveedor

            <select
              name="proveedor_id"
              value={
                purchaseForm.proveedor_id
              }
              onChange={
                handlePurchaseChange
              }
              required
            >
              <option value="">
                Seleccione un proveedor
              </option>

              {selectableProviders.map(
                (proveedor) => (
                  <option
                    key={
                      proveedor.proveedor_id
                    }
                    value={
                      proveedor.proveedor_id
                    }
                  >
                    {proveedor.nombre}
                  </option>
                )
              )}
            </select>
          </label>

          <label>
            Usuario responsable

            <select
              name="usuario_id"
              value={
                purchaseForm.usuario_id
              }
              onChange={
                handlePurchaseChange
              }
              required
            >
              <option value="">
                Seleccione un usuario
              </option>

              {selectableUsers.map(
                (usuario) => (
                  <option
                    key={
                      usuario.usuario_id
                    }
                    value={
                      usuario.usuario_id
                    }
                  >
                    {
                      usuario.nombre_usuario
                    }

                    {usuario.nombre_rol
                      ? ` - ${usuario.nombre_rol}`
                      : ""}

                    {` (ID: ${usuario.usuario_id})`}
                  </option>
                )
              )}
            </select>
          </label>

          <label>
            Fecha de recepción

            <input
              type="date"
              name="fecha_compra"
              value={
                purchaseForm.fecha_compra
              }
              onChange={
                handlePurchaseChange
              }
              required
            />
          </label>
        </div>
      </section>

      <section className="card">
        <h3>
          Agregar producto a la compra
        </h3>

        <form
          className="form-grid"
          onSubmit={handleAddItem}
        >
          <label>
            Tipo de producto

            <select
              name="modo"
              value={itemForm.modo}
              onChange={handleItemChange}
            >
              <option value="EXISTENTE">
                Producto existente
              </option>

              <option value="NUEVO">
                Registrar producto nuevo
              </option>
            </select>
          </label>

          {itemForm.modo ===
            "EXISTENTE" && (
            <>
              <label>
                Producto

                <select
                  name="insumo_id"
                  value={
                    itemForm.insumo_id
                  }
                  onChange={
                    handleItemChange
                  }
                  required
                >
                  <option value="">
                    Seleccione un producto
                  </option>

                  {selectableInsumos.map(
                    (insumo) => (
                      <option
                        key={
                          insumo.insumo_id
                        }
                        value={
                          insumo.insumo_id
                        }
                      >
                        {insumo.codigo} -{" "}
                        {insumo.nombre}
                      </option>
                    )
                  )}
                </select>
              </label>

              <label>
                Unidad de medida

                <input
                  type="text"
                  value={
                    selectedInsumo
                      ?.unidad_medida || ""
                  }
                  placeholder={
                    "Seleccione un producto"
                  }
                  readOnly
                />
              </label>
            </>
          )}

          {itemForm.modo === "NUEVO" && (
            <>
              <label>
                Código

                <input
                  type="text"
                  name="codigo"
                  value={itemForm.codigo}
                  onChange={handleItemChange}
                  placeholder="INS-001"
                  required
                />
              </label>

              <label>
                Nombre

                <input
                  type="text"
                  name="nombre"
                  value={itemForm.nombre}
                  onChange={handleItemChange}
                  required
                />
              </label>

              <label>
                Unidad de medida

                <select
                  name="unidad_medida"
                  value={
                    itemForm.unidad_medida
                  }
                  onChange={handleItemChange}
                  required
                >
                  <option value="">
                    Seleccione unidad
                  </option>

                  <option value="UNIDAD">
                    UNIDAD
                  </option>

                  <option value="CAJA">
                    CAJA
                  </option>

                  <option value="PAQUETE">
                    PAQUETE
                  </option>

                  <option value="ML">
                    ML
                  </option>

                  <option value="GRAMOS">
                    GRAMOS
                  </option>
                </select>
              </label>

              <label>
                Descripción

                <textarea
                  name="descripcion"
                  value={
                    itemForm.descripcion
                  }
                  onChange={
                    handleItemChange
                  }
                  rows="3"
                  placeholder="Opcional"
                />
              </label>
            </>
          )}

          <label>
            {currentUnit
              ? `Cantidad (${currentUnit})`
              : "Cantidad"}

            <input
              type="number"
              name="cantidad"
              value={itemForm.cantidad}
              onChange={handleItemChange}
              min={quantityMinimum}
              step={quantityStep}
              required
            />
          </label>

          <label>
            {currentUnit
              ? `Costo por ${getUnitLabel(
                  currentUnit
                )}`
              : "Costo unitario"}

            <input
              type="number"
              name="costo_unitario"
              value={
                itemForm.costo_unitario
              }
              onChange={handleItemChange}
              min="0"
              step="0.01"
              required
            />
          </label>

          <div className="clinical-summary">
            <p>
              <strong>Unidad:</strong>{" "}
              {currentUnit ||
                "Sin seleccionar"}
            </p>

            <p>
              <strong>
                Regla de cantidad:
              </strong>{" "}
              {currentUnit
                ? isDiscreteUnit(
                    currentUnit
                  )
                  ? "Solo cantidades enteras"
                  : "Se permiten cantidades decimales"
                : "Seleccione una unidad"}
            </p>

            <p>
              <strong>
                Último costo conocido:
              </strong>{" "}
              {latestDetail
                ? formatCurrency(
                    latestDetail
                      .costo_unitario
                  )
                : "Sin compras anteriores"}
            </p>

            <p>
              <strong>Subtotal:</strong>{" "}
              {formatCurrency(
                getCurrentSubtotal()
              )}
            </p>
          </div>

          <div className="form-actions">
            <button type="submit">
              {editingItemIndex === null
                ? "Agregar producto"
                : "Actualizar producto"}
            </button>

            {editingItemIndex !==
              null && (
              <button
                type="button"
                className="secondary-button"
                onClick={
                  handleCancelItemEdit
                }
              >
                Cancelar edición
              </button>
            )}
          </div>
        </form>
      </section>

      <section className="card">
        <h3>Resumen de la compra</h3>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Tipo</th>
                <th>Producto</th>
                <th>Unidad</th>
                <th>Cantidad</th>
                <th>Costo unitario</th>
                <th>Subtotal</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {purchaseItems.map(
                (item, index) => (
                  <tr
                    key={
                      `${item.modo}-${index}`
                    }
                  >
                    <td>
                      {item.modo === "NUEVO"
                        ? "Nuevo"
                        : "Existente"}
                    </td>

                    <td>
                      {
                        getPurchaseItemName(
                          item
                        )
                      }
                    </td>

                    <td>
                      {
                        getPurchaseItemUnit(
                          item
                        )
                      }
                    </td>

                    <td>
                      {item.cantidad}
                    </td>

                    <td>
                      {formatCurrency(
                        item.costo_unitario
                      )}
                    </td>

                    <td>
                      {formatCurrency(
                        getItemSubtotal(item)
                      )}
                    </td>

                    <td>
                      <button
                        type="button"
                        className="small-button"
                        onClick={() =>
                          handleEditItem(index)
                        }
                      >
                        Editar
                      </button>

                      <button
                        type="button"
                        className="danger-button"
                        onClick={() =>
                          handleRemoveItem(
                            index
                          )
                        }
                      >
                        Quitar
                      </button>
                    </td>
                  </tr>
                )
              )}

              {purchaseItems.length ===
                0 && (
                <tr>
                  <td colSpan="7">
                    No hay productos agregados.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="checkout-summary">
          <p>
            <strong>
              Total de la compra:
            </strong>{" "}
            {formatCurrency(
              getPurchaseTotal()
            )}
          </p>
        </div>

        <p className="helper-text">
          El total corresponde al costo real
          recibido del proveedor. Recuerde que el Impuesto
          pertenece al proceso de facturación.
        </p>

        <div className="form-actions">
          <button
            type="button"
            onClick={handleSubmitPurchase}
            disabled={
              loading ||
              purchaseItems.length === 0
            }
          >
            Guardar compra recibida
          </button>

          <button
            type="button"
            className="secondary-button"
            onClick={resetPurchaseForm}
            disabled={loading}
          >
            Limpiar compra
          </button>
        </div>

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
        <h3>Historial de compras</h3>

        {loading && <p>Cargando...</p>}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Proveedor</th>
                <th>Usuario responsable</th>
                <th>Fecha</th>
                <th>Productos</th>
                <th>Total</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {compras.map((compra) => {
                const details =
                  getDetailsByCompraId(
                    compra.compra_id
                  );

                return (
                  <tr key={compra.compra_id}>
                    <td>
                      {compra.compra_id}
                    </td>

                    <td>
                      {compra.proveedor_nombre ||
                        compra.proveedor_id}
                    </td>

                    <td>
                      {compra.nombre_usuario ||
                        getUsuarioLabelById(
                          compra.usuario_id
                        )}
                    </td>

                    <td>
                      {compra.fecha_compra
                        ? compra.fecha_compra.substring(
                            0,
                            10
                          )
                        : ""}
                    </td>

                    <td>
                      {details.length}
                    </td>

                    <td>
                      {formatCurrency(
                        compra.total
                      )}
                    </td>

                    <td>
                      {compra.estado}
                    </td>

                    <td>
                      <button
                        type="button"
                        className="small-button"
                        onClick={() =>
                          handleSelectCompra(
                            compra.compra_id
                          )
                        }
                      >
                        Ver detalle
                      </button>
                    </td>
                  </tr>
                );
              })}

              {compras.length === 0 &&
                !loading && (
                  <tr>
                    <td colSpan="8">
                      No hay compras registradas.
                    </td>
                  </tr>
                )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <h3>
          Detalle de compra seleccionada
        </h3>

        {!selectedCompra && (
          <p className="helper-text">
            Seleccione una compra para revisar
            los productos recibidos.
          </p>
        )}

        {selectedCompra && (
          <>
            <div className="clinical-summary">
              <p>
                <strong>Compra:</strong>{" "}
                {selectedCompra.compra_id}
              </p>

              <p>
                <strong>Proveedor:</strong>{" "}
                {
                  selectedCompra
                    .proveedor_nombre
                }
              </p>

              <p>
                <strong>Fecha:</strong>{" "}
                {selectedCompra.fecha_compra
                  ? selectedCompra
                      .fecha_compra
                      .substring(0, 10)
                  : ""}
              </p>

              <p>
                <strong>Total:</strong>{" "}
                {formatCurrency(
                  selectedCompra.total
                )}
              </p>
            </div>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Producto</th>
                    <th>Unidad</th>
                    <th>Cantidad</th>
                    <th>Costo unitario</th>
                    <th>Subtotal</th>
                  </tr>
                </thead>

                <tbody>
                  {selectedCompraDetails.map(
                    (detalle) => {
                      const insumo =
                        getInsumoById(
                          detalle.insumo_id
                        );

                      return (
                        <tr
                          key={
                            detalle
                              .detalle_compra_id
                          }
                        >
                          <td>
                            {detalle.insumo_codigo
                              ? `${detalle.insumo_codigo} - ${detalle.insumo_nombre}`
                              : detalle.insumo_nombre ||
                                detalle.insumo_id}
                          </td>

                          <td>
                            {insumo
                              ?.unidad_medida ||
                              ""}
                          </td>

                          <td>
                            {detalle.cantidad}
                          </td>

                          <td>
                            {formatCurrency(
                              detalle
                                .costo_unitario
                            )}
                          </td>

                          <td>
                            {formatCurrency(
                              detalle.subtotal
                            )}
                          </td>
                        </tr>
                      );
                    }
                  )}

                  {selectedCompraDetails.length ===
                    0 && (
                    <tr>
                      <td colSpan="5">
                        Esta compra no tiene
                        productos registrados.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </>
        )}
      </section>
    </section>
  );
}

export default Compras;