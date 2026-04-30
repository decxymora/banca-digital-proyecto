# 🏦 Banca Digital — Proyecto Integrador
**Bootcamp Análisis de Datos | Betek 2026 | Grupo 1**

---

## 📌 Descripción

Diseño e implementación de una base de datos relacional para un banco digital colombiano orientada al análisis financiero, gestión de riesgo crediticio y eficiencia de cobranza.

El proyecto abarca el modelado de datos, generación y limpieza de datos con Python, carga en MySQL y análisis de negocio enfocado en responder tres preguntas clave:

- 💰 **¿Qué tan rentable es el banco?** — análisis de activos, pasivos e ingresos proyectados
- 📉 **¿Cuánto dinero está en riesgo?** — cartera vencida, mora y concentración geográfica
- 📞 **¿Qué tan eficiente es la cobranza?** — tasa de recuperación y efectividad por canal

> Base de datos con **12 tablas** y **475.434 registros** generados con Python y cargados en MySQL.

---

## 📊 Indicadores Financieros del Modelo

| Indicador | Valor |
|---|---|
| Cartera activa (total prestado) | $128.440.200.000 |
| Total depósitos clientes | $136.544.315.000 |
| Ingresos por intereses proyectados/mes | $1.959.337.770 |
| Cartera en riesgo (mora activa) | $2.068.956.605 |
| Tasa de morosidad | 1.20% |
| Tasa de recuperación de cartera | 12.24% |
| Clientes únicos en mora | 250 (25% de la base) |

> Los depósitos superan la cartera prestada — el banco mantiene liquidez positiva. La tasa de morosidad del 1.08% está por debajo del promedio del sector financiero colombiano (3-8%), sin embargo la tasa de recuperación del 12.24% indica una oportunidad crítica de mejora en el proceso de cobranza.

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
| mora | 286 | Registro de cartera vencida |
| gestion_cobranza | 632 | Procesos de recuperación de cartera |

---

## 📈 Análisis de negocio

Las consultas de negocio están organizadas en tres bloques orientados a la toma de decisiones financieras. *(En proceso de validación grupal — próximamente en `sql/consultas_negocio.sql`)*

### 💰 Bloque 1 — Rentabilidad y Salud Financiera

| # | Consulta | Pregunta de negocio |
|---|---|---|
| Q1 | Total activos vs pasivos | ¿Cuánto dinero tiene prestado el banco y cuánto tienen depositado los clientes? |
| Q2 | Ingresos proyectados por intereses | ¿Cuánto genera el banco mensualmente por su cartera activa? |
| Q3 | Rentabilidad por tipo de producto | ¿Qué productos generan más ingresos al banco? |

### 📉 Bloque 2 — Cartera Vencida y Mora

| # | Consulta | Pregunta de negocio |
|---|---|---|
| Q4 | Clientes en mora activa con detalle de deuda | ¿Quiénes deben, cuánto deben y hace cuántos días están en mora? |
| Q5 | Cartera vencida por tipo de producto | ¿Qué productos generan mayor riesgo de impago? |
| Q6 | Cartera vencida por departamento | ¿En qué regiones se concentra el mayor riesgo crediticio? |
| Q7 | Moras sin gestión de cobranza registrada | ¿Qué clientes cayeron en mora sin ser contactados? |
| Q8 | Clientes con saldo disponible y mora activa | ¿Qué clientes tienen dinero en cuenta pero no han pagado su deuda? |

### 📞 Bloque 3 — Eficiencia de Cobranza

| # | Consulta | Pregunta de negocio |
|---|---|---|
| Q9 | Tasa de resolución por canal de contacto | ¿Qué canal de cobranza es más efectivo para recuperar cartera? |
| Q10 | Tiempo promedio de resolución de mora | ¿Cuántos días tarda en promedio cerrar una mora por tipo de producto? |
| Q11 | Casos críticos con múltiples gestiones sin liquidar | ¿Qué clientes requieren escalamiento a proceso jurídico? |
| Q12 | KPIs ejecutivos de cartera | ¿Cuál es el estado global de la cartera del banco? |

### 🔐 Bloque 4 — Seguridad

| # | Consulta | Pregunta de negocio |
|---|---|---|
| Q13 | Intentos fallidos de autenticación | ¿Qué cuentas están bajo riesgo de acceso no autorizado? |
| Q14 | Transacciones por canal | ¿Qué canales concentran mayor volumen y riesgo transaccional? |

---

## 🚧 Estado del proyecto

| Fase | Estado | Descripción |
|---|---|---|
| Fase 1 — Modelado y DDL | ✅ Completado | Diseño de 12 tablas, relaciones y restricciones |
| Fase 2 — Generación de datos | ✅ Completado | 475.434 registros generados y cargados en MySQL |
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
