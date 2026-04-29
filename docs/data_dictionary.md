## Descripción general

Este diccionario de datos documenta la estructura del modelo de banca digital, incluyendo tablas de clientes, productos financieros, transacciones y gestión de mora.


## Tabla: cliente

| Campo | Tipo | Descripción |
|------|------|------------|
| id_cliente | INT | Identificador único del cliente |
| id_ciudad | INT | Ciudad de residencia |
| nombre | VARCHAR | Nombre del cliente |
| apellido | VARCHAR | Apellido del cliente |
| tipo_documento | ENUM | Tipo de identificación (CC, TI, CE, Pasaporte) |
| numero_documento | VARCHAR | Número único de identificación |
| fecha_nacimiento | DATE | Fecha de nacimiento |
| direccion | VARCHAR | Dirección de residencia |
| email | VARCHAR | Correo electrónico |
| telefono | VARCHAR | Teléfono de contacto |
| estado | ENUM | Estado del cliente |

---

## Tabla: productos_banco

| Campo | Tipo | Descripción |
|------|------|------------|
| id_producto_banco | INT | ID del producto |
| codigo_producto | VARCHAR | Código único |
| tipo_producto | ENUM | Activo (crédito) o Pasivo (depósito) |
| nombre_producto | VARCHAR | Nombre del producto |

---

## Tabla: producto_activo

| Campo | Tipo | Descripción |
|------|------|------------|
| id_producto_activo | INT | ID del producto |
| id_cliente | INT | Cliente asociado |
| monto_aprobado | DECIMAL | Valor aprobado |
| tasa_interes_mensual | DECIMAL | Tasa de interés |
| estado | ENUM | Vigente, En Mora, Cancelada, Castigada |
| numero_cuotas | INT | Número de cuotas |
| valor_cuota_fija | DECIMAL | Valor de cuota |

---

## Tabla: producto_pasivo

| Campo | Tipo | Descripción |
|------|------|------------|
| id_producto_pasivo | INT | ID de la cuenta |
| id_cliente | INT | Cliente asociado |
| numero_cuenta | VARCHAR | Número de cuenta |
| saldo_actual | DECIMAL | Saldo disponible |
| cuota_manejo | DECIMAL | Costo de mantenimiento |

---

## Tabla: transacciones

| Campo | Tipo | Descripción |
|------|------|------------|
| id_transaccion | INT | ID de la transacción |
| id_tipo_transaccion | INT | Tipo de movimiento |
| monto | DECIMAL | Valor de la transacción |
| fecha_transaccion | DATETIME | Fecha |
| canal | VARCHAR | Canal (App, Web, etc.) |

---

## Tabla: extracto

| Campo | Tipo | Descripción |
|------|------|------------|
| id_extracto | INT | ID del extracto |
| fecha_corte | DATE | Fecha de corte |
| fecha_limite_pago | DATE | Fecha límite |
| pago_total_mes | DECIMAL | Total a pagar |
| estado_pago | ENUM | Pendiente, Pagado, Mora |

---

## Tabla: mora

| Campo | Tipo | Descripción |
|------|------|------------|
| id_mora | INT | ID de la mora |
| fecha_inicio_mora | DATE | Inicio |
| dias_mora | INT | Días en mora |
| capital_vencido | DECIMAL | Deuda |
| estado_mora | ENUM | Estado de la mora |
