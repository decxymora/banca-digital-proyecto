# 🏦 Banca Digital — Proyecto Integrador
**Bootcamp Análisis de Datos | Betek 2026 | Grupo 1**

---

## 📌 Descripción

Diseño e implementación de una base de datos relacional para un banco digital colombiano.  
El proyecto abarca el modelado de datos, generación y limpieza de datos con Python, carga en MySQL y análisis de negocio enfocado en tres áreas críticas: **seguridad**, **cartera vencida** y **eficiencia de cobranza**.

> Base de datos con **12 tablas** y **483.411 registros** generados con Python y cargados en MySQL.

---

## 🗂️ Estructura del proyecto

```
banca-digital-proyecto/
│
├── sql/
│   └── DDL_Schema_banca_digital.sql         → Creación de tablas y relaciones
│
├── scripts/
│   ├── data_cleaning_clientes.py            → Limpieza de datos de clientes
│   ├── data_generation_autenticacion.py     → Generación de credenciales de acceso
│   ├── data_generation_extractos.py         → Generación de extractos mensuales
│   ├── data_generation_gestion_cobranza.py  → Generación de gestiones de cobranza
│   ├── data_generation_mora.py              → Generación de registros de mora
│   ├── data_generation_producto_activo.py   → Generación de créditos y tarjetas
│   ├── data_generation_producto_pasivo.py   → Generación de cuentas de ahorro y corriente
│   ├── data_generation_transacciones.py     → Generación de movimientos financieros
│   ├── eda_ciudades.py                      → Análisis exploratorio de ciudades
│   ├── eda_departamentos.py                 → Análisis exploratorio de departamentos
│   ├── eda_productos_banco.py               → Análisis exploratorio de productos
│   ├── eda_tipo_transaccion.py              → Análisis exploratorio de transacciones
│   └── cargar_mysql.py                      → Carga de datos en MySQL
│
├── diagramas/
│   ├── MER_banca_digital.png                → Diagrama Entidad-Relación
│   ├── modelo_relacional_banca_digital.png  → Modelo Relacional
│   └── MER_banca_digital_drawio.xml         → Archivo fuente editable del MER
│
├── docs/
│   └── data_dictionary.md                   → Diccionario de datos
│
├── .gitignore
└── README.md
```

---

## 🛠️ Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| MySQL | Base de datos relacional |
| Python | Generación y limpieza de datos |
| pandas | Manipulación y transformación de datos |
| SQLAlchemy | Conexión Python → MySQL |
| draw.io | Diagramas MER y Relacional |
| VS Code | Entorno de desarrollo |

---

## 📊 Modelo de datos

La base de datos contiene 12 tablas organizadas en cuatro dominios:

| Dominio | Tablas |
|---|---|
| Geografía | `departamentos`, `ciudades` |
| Clientes | `cliente`, `autenticacion_cliente` |
| Productos | `productos_banco`, `tipo_transaccion`, `producto_activo`, `producto_pasivo` |
| Operaciones | `extracto`, `transacciones`, `mora`, `gestion_cobranza` |

### Volumen de datos

| Tabla | Registros | Descripción |
|---|---|---|
| departamentos | 33 | Departamentos de Colombia |
| ciudades | 450 | Ciudades de Colombia |
| cliente | 999 | Clientes del banco |
| autenticacion_cliente | 999 | Credenciales de acceso a la app |
| productos_banco | 12 | Catálogo de productos financieros |
| tipo_transaccion | 14 | Tipos de movimiento financiero |
| producto_activo | 1.887 | Créditos y tarjetas de crédito |
| producto_pasivo | 1.482 | Cuentas de ahorro y corriente |
| extracto | 49.114 | Facturación mensual por producto |
| transacciones | 419.623 | Movimientos financieros |
| mora | 2.997 | Registro de cartera vencida |
| gestion_cobranza | 5.831 | Procesos de recuperación de cartera |

---

## 📈 Análisis de negocio

Las consultas de negocio están organizadas en tres bloques. Cada consulta incluye el contexto de negocio que responde.

### 🔐 Bloque 1 — Seguridad

| # | Consulta | Pregunta de negocio |
|---|---|---|
| Q1 | Intentos fallidos de autenticación | ¿Qué cuentas están bajo ataque o riesgo de acceso no autorizado? |
| Q2 | Cuentas bloqueadas con historial de acceso | ¿Qué usuarios fueron bloqueados y cuándo fue su último ingreso? |
| Q3 | Transacciones por canal | ¿Qué canales concentran mayor volumen y monto transaccional? |
| Q4 | Cuentas activas sin ingreso registrado | ¿Existen cuentas nunca utilizadas que representen riesgo de suplantación? |

### 💳 Bloque 2 — Mora y Cartera Vencida

| # | Consulta | Pregunta de negocio |
|---|---|---|
| Q5 | Clientes en mora activa con detalle de deuda | ¿Quiénes deben, cuánto deben y hace cuántos días están en mora? |
| Q6 | Cartera vencida por tipo de producto | ¿Qué productos generan mayor riesgo de impago? |
| Q7 | Cartera vencida por departamento | ¿En qué regiones se concentra el mayor riesgo crediticio? |
| Q8 | Moras sin gestión de cobranza registrada | ¿Qué clientes cayeron en mora sin ser contactados? |
| Q9 | Clientes con saldo disponible y mora activa | ¿Qué clientes tienen dinero en cuenta pero no han pagado su deuda? |

### 📞 Bloque 3 — Eficiencia de Cobranza

| # | Consulta | Pregunta de negocio |
|---|---|---|
| Q10 | Tasa de resolución por canal de contacto | ¿Qué canal de cobranza es más efectivo para recuperar cartera? |
| Q11 | Tiempo promedio de resolución de mora | ¿Cuántos días tarda en promedio cerrar una mora por tipo de producto? |
| Q12 | Casos críticos con múltiples gestiones sin liquidar | ¿Qué clientes requieren escalamiento a proceso jurídico? |
| Q13 | KPIs ejecutivos de cartera | ¿Cuál es el estado global de la cartera del banco? |

---

## 🚧 Estado del proyecto

| Fase | Estado | Descripción |
|---|---|---|
| Fase 1 — Modelado y DDL | ✅ Completado | Diseño de 12 tablas, relaciones y restricciones |
| Fase 2 — Generación de datos | ✅ Completado | 483.411 registros generados y cargados en MySQL |
| Fase 3 — Consultas de negocio | 🟡 En proceso | 13 consultas desarrolladas, resultados en validación |
| Fase 4 — Visualización | 🔜 Pendiente | Dashboard en Power BI sobre resultados del análisis |

---

## 👥 Equipo

Grupo 1 — Bootcamp Análisis de Datos | Betek 2026

- Gómez, Johana
- Huertas, Johan
- Quiñónez, Decxy

---

## 📄 Licencia

Proyecto académico — uso educativo.
