# 🏦 Banca Digital — Proyecto Integrador

> Bootcamp Análisis de Datos | Grupo 1

## 📌 Descripción
Diseño e implementación de una base de datos relacional para un banco digital colombiano. El proyecto incluye modelado de datos, generación y limpieza de datos con Python, carga en MySQL y análisis de seguridad y cartera.

## 🗂️ Estructura del proyecto
banca-digital-proyecto/
│
├── sql/               → Script DDL completo de la base de datos
├── scripts/           → Scripts Python de limpieza y generación de datos
├── docs/              → Documentación del proyecto
└── diagramas/         → Modelo Entidad-Relación y Modelo Relacional

## 🛠️ Tecnologías utilizadas
- **MySQL** — Base de datos relacional
- **Python** — Limpieza y generación de datos
- **pandas** — Manipulación de datos
- **SQLAlchemy** — Conexión Python-MySQL
- **draw.io** — Diagramas MER y Relacional
- **VS Code** — Entorno de desarrollo

## 📊 Base de datos
La BD contiene 12 tablas y 483.411 registros:

| Tabla | Registros | Descripción |
|-------|-----------|-------------|
| departamentos | 33 | Departamentos de Colombia |
| ciudades | 450 | Ciudades de Colombia |
| cliente | 999 | Clientes del banco |
| autenticacion_cliente | 999 | Acceso a la app bancaria |
| productos_banco | 12 | Catálogo de productos |
| tipo_transaccion | 14 | Tipos de movimiento financiero |
| producto_activo | 1.887 | Créditos y tarjetas |
| producto_pasivo | 1.482 | Cuentas de ahorro y corriente |
| extracto | 49.114 | Facturación mensual |
| transacciones | 419.623 | Movimientos financieros |
| mora | 2.997 | Cartera vencida |
| gestion_cobranza | 5.831 | Procesos de recuperación |

## 🔐 Análisis de seguridad
- Detección de transacciones sospechosas por IP
- Identificación de intentos fallidos de acceso
- Monitoreo de transacciones en horarios inusuales

## 📈 Análisis de cartera
- Perfil de clientes con mayor riesgo de mora
- Concentración geográfica de cartera vencida
- Relación entre edad, producto y probabilidad de mora

## 👥 Equipo
Grupo 1 — Bootcamp Análisis de Datos

## 📅 Estado del proyecto
🟡 En desarrollo — Fase 3: Consultas de negocio y visualización
