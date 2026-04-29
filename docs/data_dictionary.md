# 📖 Diccionario de Datos — Banca Digital
**Proyecto Integrador | Bootcamp Análisis de Datos | Betek 2026**

---

## Índice

1. [Tablas de Catálogo](#1-tablas-de-catálogo)
   - [departamentos](#11-departamentos)
   - [ciudades](#12-ciudades)
   - [productos_banco](#13-productos_banco)
   - [tipo_transaccion](#14-tipo_transaccion)
2. [Tablas de Clientes](#2-tablas-de-clientes)
   - [cliente](#21-cliente)
   - [autenticacion_cliente](#22-autenticacion_cliente)
3. [Tablas de Productos](#3-tablas-de-productos)
   - [producto_activo](#31-producto_activo)
   - [producto_pasivo](#32-producto_pasivo)
4. [Tablas Operativas](#4-tablas-operativas)
   - [extracto](#41-extracto)
   - [transacciones](#42-transacciones)
   - [mora](#43-mora)
   - [gestion_cobranza](#44-gestion_cobranza)

---

## 1. Tablas de Catálogo

### 1.1 `departamentos`
Base geográfica de Colombia. Tabla de referencia usada para normalizar la ubicación de clientes.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_departamento` | INT | Identificador único del departamento (PK) |
| `nombre_departamento` | VARCHAR(100) | Nombre oficial del departamento |

> **Registros:** 33 — corresponden a los 32 departamentos de Colombia más el Distrito Capital.

---

### 1.2 `ciudades`
Normalización geográfica a nivel municipal. Cada ciudad pertenece a un departamento.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_ciudad` | INT | Identificador único de la ciudad (PK) |
| `id_departamento` | INT | Departamento al que pertenece (FK → departamentos) |
| `nombre_ciudad` | VARCHAR(100) | Nombre del municipio o ciudad |

> **Registros:** 450 ciudades distribuidas en los 33 departamentos.

---

### 1.3 `productos_banco`
Catálogo maestro de los productos financieros que ofrece el banco. Define si el banco presta dinero al cliente (Activo) o el cliente deposita en el banco (Pasivo).

| Campo | Tipo | Descripción |
|---|---|---|
| `id_producto_banco` | INT | Identificador único del producto (PK) |
| `codigo_producto` | VARCHAR(50) | Código interno único del producto |
| `tipo_producto` | ENUM | `Activo` = banco presta al cliente / `Pasivo` = cliente deposita en el banco |
| `nombre_producto` | VARCHAR(100) | Nombre comercial del producto |

> **Registros:** 12 productos — incluye créditos de consumo, tarjetas de crédito, cuentas de ahorro y cuentas corrientes.

---

### 1.4 `tipo_transaccion`
Catálogo de todos los movimientos financieros posibles en el sistema. El campo `naturaleza` determina cómo afecta el saldo de una cuenta.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_tipo_transaccion` | INT | Identificador único del tipo (PK) |
| `nombre_tipo` | VARCHAR(100) | Nombre del movimiento (ej: Depósito, Retiro, Pago de cuota) |
| `naturaleza` | ENUM | `Entrada` = suma al saldo / `Salida` = resta al saldo / `Neutro` = no afecta saldo |

> **Registros:** 14 tipos de transacción.

---

## 2. Tablas de Clientes

### 2.1 `cliente`
Información personal y de contacto de cada cliente del banco. El campo `estado` permite gestionar clientes activos, inactivos o bloqueados sin eliminar registros.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_cliente` | INT | Identificador único del cliente (PK) |
| `id_ciudad` | INT | Ciudad de residencia (FK → ciudades) |
| `nombre` | VARCHAR(100) | Nombre del cliente |
| `apellido` | VARCHAR(100) | Apellido del cliente |
| `tipo_documento` | ENUM | `CC` Cédula de Ciudadanía  / `CE` Cédula de Extranjería / `Pasaporte` |
| `numero_documento` | VARCHAR(20) | Número de identificación — único por cliente |
| `fecha_nacimiento` | DATE | Fecha de nacimiento — usada para calcular edad y validar mayoría de edad |
| `direccion` | VARCHAR(150) | Dirección de residencia |
| `email` | VARCHAR(100) | Correo electrónico — único por cliente |
| `telefono` | VARCHAR(20) | Teléfono de contacto |
| `estado` | ENUM | `Activo` / `Inactivo` / `Bloqueado` — por defecto `Activo` |

> **Registros:** 999 clientes.

---

### 2.2 `autenticacion_cliente`
Gestión de credenciales de acceso a la aplicación bancaria. Tabla crítica para el análisis de seguridad.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_usuario` | INT | Identificador único del usuario (PK) |
| `id_cliente` | INT | Cliente al que pertenece — relación 1 a 1 (FK → cliente) |
| `nombre_usuario` | VARCHAR(50) | Usuario de acceso a la app — único |
| `clave_hash` | VARCHAR(255) | Contraseña almacenada con hash — nunca en texto plano |
| `tipo_mfa` | ENUM | Método de autenticación de doble factor: `SMS` / `App` / `Correo` |
| `estado` | ENUM | `Activo` / `Bloqueado` / `Suspendido` — por defecto `Activo` |
| `intentos_fallidos` | INT | Contador de intentos de acceso fallidos — se usa para detección de ataques |
| `ultimo_ingreso` | DATETIME | Fecha y hora del último acceso exitoso — NULL si nunca ha ingresado |

> **Registros:** 999 — un registro por cliente.  
> **Uso analítico:** `intentos_fallidos` y `ultimo_ingreso` son los campos clave para el análisis de seguridad y detección de accesos sospechosos.

---

## 3. Tablas de Productos

### 3.1 `producto_activo`
Registra los créditos y tarjetas de crédito asignados a cada cliente. Es una tabla dual: algunos campos aplican solo a créditos y otros solo a tarjetas de crédito.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_producto_activo` | INT | Identificador único (PK) |
| `id_producto_banco` | INT | Tipo de producto (FK → productos_banco) |
| `id_cliente` | INT | Cliente titular (FK → cliente) |
| `numero_contrato` | VARCHAR(50) | Número de contrato — único |
| `monto_aprobado` | DECIMAL(18,2) | Monto total aprobado del crédito o cupo de la tarjeta |
| `tasa_interes_mensual` | DECIMAL(5,2) | Tasa de interés mensual en % — máximo legal Colombia ~2.80% |
| `tasa_interes_mora` | DECIMAL(5,2) | Tasa de interés por mora en % — máximo legal Colombia ~3.93% mensual |
| `fecha_inicio` | DATE | Fecha de desembolso o apertura |
| `fecha_vencimiento` | DATE | Fecha de vencimiento — obligatoria para créditos, NULL para tarjetas sin plazo |
| `estado` | ENUM | `Vigente` / `En_Mora` / `Cancelada` / `Castigada` |
| `numero_cuotas` | INT | Total de cuotas pactadas — solo créditos, NULL para tarjetas |
| `valor_cuota_fija` | DECIMAL(18,2) | Valor de cuota mensual fija — solo créditos, NULL para tarjetas |
| `cupo_disponible` | DECIMAL(18,2) | Cupo disponible actual — solo tarjetas de crédito, NULL para créditos |
| `dia_corte` | INT | Día del mes en que se genera el extracto — solo tarjetas (1-31) |

> **Registros:** 1.887  
> **Regla de negocio clave:** `numero_cuotas` y `valor_cuota_fija` son obligatorios para créditos y NULL para tarjetas. `cupo_disponible` y `dia_corte` son exclusivos de tarjetas de crédito.

---

### 3.2 `producto_pasivo`
Cuentas de ahorro y corriente donde el cliente deposita dinero en el banco.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_producto_pasivo` | INT | Identificador único (PK) |
| `id_producto_banco` | INT | Tipo de producto (FK → productos_banco) |
| `id_cliente` | INT | Cliente titular (FK → cliente) |
| `numero_cuenta` | VARCHAR(50) | Número de cuenta bancaria — único |
| `saldo_actual` | DECIMAL(18,2) | Saldo disponible en la cuenta — por defecto 0.00 |
| `cuota_manejo` | DECIMAL(12,2) | Cobro mensual por administración de la cuenta |
| `fecha_apertura` | DATETIME | Fecha y hora de apertura de la cuenta |

> **Registros:** 1.482

---

## 4. Tablas Operativas

### 4.1 `extracto`
Facturación mensual de productos activos. Consolida lo que el cliente debe pagar cada mes por sus créditos o tarjetas. Es la tabla que origina la mora cuando no se paga.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_extracto` | INT | Identificador único (PK) |
| `id_producto_activo` | INT | Producto al que corresponde el extracto (FK → producto_activo) |
| `numero_extracto` | VARCHAR(50) | Número de extracto — único |
| `fecha_corte` | DATE | Fecha en que se cierra el período de facturación |
| `fecha_limite_pago` | DATE | Fecha máxima de pago antes de entrar en mora |
| `saldo_capital_pendiente` | DECIMAL(18,2) | Capital que aún no ha sido pagado |
| `intereses_mes` | DECIMAL(18,2) | Intereses generados en el período |
| `cuota_manejo` | DECIMAL(12,2) | Cargo fijo por administración del producto |
| `pago_total_mes` | DECIMAL(18,2) | Valor total que debe pagar el cliente en el mes |
| `pago_minimo` | DECIMAL(18,2) | Pago mínimo requerido — aplica solo para tarjetas de crédito |
| `estado_pago` | ENUM | `Pendiente` / `Pagado` / `Parcial` / `Mora` |

> **Registros:** 49.114  
> **Regla de negocio clave:** cuando `fecha_limite_pago` vence y `estado_pago` es `Pendiente` o `Parcial`, se genera un registro en la tabla `mora`.

---

### 4.2 `transacciones`
Tabla central del sistema. Registra absolutamente todos los movimientos financieros. Puede estar asociada a un producto pasivo (cuentas), un producto activo (créditos/tarjetas) o ambos en el caso de transferencias.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_transaccion` | INT | Identificador único (PK) |
| `id_producto_pasivo` | INT | Cuenta origen o destino — NULL si no aplica (FK → producto_pasivo) |
| `id_producto_activo` | INT | Crédito o tarjeta involucrado — NULL si no aplica (FK → producto_activo) |
| `id_tipo_transaccion` | INT | Tipo de movimiento (FK → tipo_transaccion) |
| `id_extracto` | INT | Extracto al que aplica el pago — NULL si no es pago de cuota (FK → extracto) |
| `monto` | DECIMAL(18,2) | Valor del movimiento — siempre positivo |
| `fecha_transaccion` | DATETIME | Fecha y hora exacta del movimiento |
| `canal` | VARCHAR(50) | Canal usado: `App` / `Web` / `Cajero` / `Corresponsal` |
| `ip_origen` | VARCHAR(45) | Dirección IP desde donde se originó — usado para trazabilidad y seguridad |

> **Registros:** 419.623 — es la tabla más grande del sistema.  
> **Uso analítico:** `canal` e `ip_origen` son los campos clave para el análisis de seguridad transaccional. `id_extracto` permite relacionar pagos con obligaciones específicas.

---

### 4.3 `mora`
Seguimiento de clientes en situación de morosidad. Solo puede existir un registro de mora si hay un extracto impago que lo origina.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_mora` | INT | Identificador único (PK) |
| `id_producto_activo` | INT | Producto en mora (FK → producto_activo) |
| `id_extracto` | INT | Extracto impago que origina la mora (FK → extracto) |
| `fecha_inicio_mora` | DATE | Fecha en que inició la situación de mora |
| `dias_mora` | INT | Número de días transcurridos en mora — por defecto 0 |
| `capital_vencido` | DECIMAL(18,2) | Monto de capital que no fue pagado |
| `interes_mora` | DECIMAL(18,2) | Intereses generados por el incumplimiento de pago |
| `estado_mora` | ENUM | `Activa` / `En Gestion` / `Liquidada` — por defecto `Activa` |

> **Registros:** 2.997  
> **Regla de negocio clave:** `capital_vencido + interes_mora` = deuda total del cliente en mora. El campo `dias_mora` es el principal indicador de severidad para priorizar la gestión de cobranza.

---

### 4.4 `gestion_cobranza`
Registro de todas las acciones realizadas para recuperar cartera en mora. Cada contacto con el cliente genera un registro independiente.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_gestion` | INT | Identificador único (PK) |
| `id_mora` | INT | Mora a la que corresponde la gestión (FK → mora) |
| `fecha_gestion` | DATETIME | Fecha y hora en que se realizó el contacto |
| `tipo_contacto` | ENUM | Canal usado: `Llamada` / `Correo` / `SMS` / `Visita Domiciliaria` |
| `resultado_gestion` | TEXT | Descripción del resultado del contacto — ej: "Cliente promete pagar el viernes" |

> **Registros:** 5.831  
> **Uso analítico:** la relación entre `tipo_contacto` y el `estado_mora` resultante permite medir qué canal de cobranza es más efectivo para recuperar cartera.

---

*Última actualización: 2026 | Proyecto académico — uso educativo*