-- BANCA DIGITAL — 
-- Proyecto Integrador — Bootcamp Analisis de Datos

CREATE DATABASE BANCA_DIGITAL CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE BANCA_DIGITAL;

-- TABLA 1
-- 1. DEPARTAMENTOS
-- Base geográfica Colombiana

CREATE TABLE departamentos (
    id_departamento     INT AUTO_INCREMENT PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- TABLA 2 
-- 2. CIUDADES
-- Normalización geográfica (igual que Sakila)

CREATE TABLE ciudades (
    id_ciudad       INT AUTO_INCREMENT PRIMARY KEY,
    id_departamento INT NOT NULL,
    nombre_ciudad   VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
) ENGINE=InnoDB;

-- TABLA 3 
-- 3. PRODUCTOS_BANCO
-- Cataalogo maestro de productos que ofrece el banco
-- tipo_producto: Activo = el banco presta (créditos, tarjetas)
--               Pasivo = el cliente deposita (cuentas de ahorro, corriente)

CREATE TABLE productos_banco (
    id_producto_banco INT AUTO_INCREMENT PRIMARY KEY,
    codigo_producto   VARCHAR(50) UNIQUE NOT NULL,
    tipo_producto     ENUM('Activo', 'Pasivo') NOT NULL,
    nombre_producto   VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- TABLA 4 
-- 4. TIPO_TRANSACCION
-- Catalogo de movimientos financieros posibles
-- naturaleza: Entrada = suma al saldo, Salida = resta, Neutro = no afecta saldo

CREATE TABLE tipo_transaccion (
    id_tipo_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo         VARCHAR(100) NOT NULL,
    naturaleza          ENUM('Entrada', 'Salida', 'Neutro') NOT NULL -- (se agrego)
) ENGINE=InnoDB;

-- TABLA 5 
-- 5. CLIENTE
-- Información personal del cliente
-- El proyecto exige: nombre, dirección, contacto, número de identificación

CREATE TABLE cliente (
    id_cliente       INT AUTO_INCREMENT PRIMARY KEY,
    id_ciudad        INT NOT NULL,
    nombre           VARCHAR(100) NOT NULL,
    apellido         VARCHAR(100) NOT NULL,
    tipo_documento   ENUM('CC', 'CE', 'Pasaporte') NOT NULL,
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion        VARCHAR(150) NOT NULL,
    email            VARCHAR(100) UNIQUE NOT NULL,
    telefono         VARCHAR(20),
    estado           ENUM('Activo', 'Inactivo', 'Bloqueado') DEFAULT 'Activo',
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad)
) ENGINE=InnoDB;

-- TABLA 6 
-- 6. AUTENTICACION_CLIENTE
-- El proyecto exige explícitamente "datos de autenticación"
-- Almacena credenciales de acceso a la app bancaria

CREATE TABLE autenticacion_cliente (
    id_usuario        INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente        INT NOT NULL UNIQUE,       -- un cliente, un usuario
    nombre_usuario    VARCHAR(50) UNIQUE NOT NULL,
    clave_hash        VARCHAR(255) NOT NULL,      -- NUNCA se guarda la clave en texto plano
    tipo_mfa          ENUM('SMS', 'App', 'Correo') DEFAULT 'SMS',
    estado            ENUM('Activo', 'Bloqueado', 'Suspendido') DEFAULT 'Activo',
    intentos_fallidos INT DEFAULT 0,
    ultimo_ingreso    DATETIME NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
) ENGINE=InnoDB;

-- TABLA 7 
-- 7. PRODUCTO_ACTIVO
-- Créditos y tarjetas de crédito (el banco le presta al cliente)
-- numero_cuotas y valor_cuota_fija: obligatorios para créditos, NULL para tarjetas
-- cupo_disponible: exclusivo para tarjetas de crédito

CREATE TABLE producto_activo (
    id_producto_activo   INT AUTO_INCREMENT PRIMARY KEY,
    id_producto_banco    INT NOT NULL,
    id_cliente           INT NOT NULL,
    numero_contrato      VARCHAR(50) UNIQUE NOT NULL,
    monto_aprobado       DECIMAL(18,2) NOT NULL,
    tasa_interes_mensual DECIMAL(5,2) NOT NULL,   -- % mensual, máx legal Colombia ~2.80%
    tasa_interes_mora    DECIMAL(5,2) NOT NULL,   -- % mora, máx legal ~3.93% mensual
    fecha_inicio         DATE NOT NULL,
    fecha_vencimiento    DATE NULL,               -- obligatoria para créditos, NULL para tarjetas sin plazo
    estado               ENUM('Vigente', 'En_Mora', 'Cancelada', 'Castigada') DEFAULT 'Vigente',
    numero_cuotas        INT NULL,
    valor_cuota_fija     DECIMAL(18,2) NULL,
    cupo_disponible      DECIMAL(18,2) NULL,      -- solo tarjetas de crédito
    dia_corte            INT NULL CHECK (dia_corte BETWEEN 1 AND 31),
    FOREIGN KEY (id_producto_banco) REFERENCES productos_banco(id_producto_banco),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
) ENGINE=InnoDB;

-- TABLA 8 
-- 8. PRODUCTO_PASIVO
-- Cuentas de ahorro y corriente (el cliente deposita en el banco)

CREATE TABLE producto_pasivo (
    id_producto_pasivo INT AUTO_INCREMENT PRIMARY KEY,
    id_producto_banco  INT NOT NULL,
    id_cliente         INT NOT NULL,
    numero_cuenta      VARCHAR(50) UNIQUE NOT NULL,
    saldo_actual       DECIMAL(18,2) DEFAULT 0.00,
    cuota_manejo       DECIMAL(12,2) DEFAULT 0.00,
    fecha_apertura     DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_producto_banco) REFERENCES productos_banco(id_producto_banco),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
) ENGINE=InnoDB;

-- TABLA 9 
-- 9. EXTRACTO
-- Facturación mensual de productos activos (tarjetas y créditos)
-- El proyecto pide "pagos realizados", "saldos pendientes", "fechas de vencimiento"
-- La tabla es fundamental para la cartera

CREATE TABLE extracto (
    id_extracto              INT AUTO_INCREMENT PRIMARY KEY,
    id_producto_activo       INT NOT NULL,
    numero_extracto          VARCHAR(50) UNIQUE NOT NULL,
    fecha_corte              DATE NOT NULL,
    fecha_limite_pago        DATE NOT NULL,
    saldo_capital_pendiente  DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    intereses_mes            DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    cuota_manejo             DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    pago_total_mes           DECIMAL(18,2) NOT NULL,  -- valor total que debe pagar
    pago_minimo              DECIMAL(18,2) NULL,       -- aplica para tarjetas de crédito
    estado_pago              ENUM('Pendiente', 'Pagado', 'Parcial', 'Mora') DEFAULT 'Pendiente',
    FOREIGN KEY (id_producto_activo) REFERENCES producto_activo(id_producto_activo)
) ENGINE=InnoDB;

-- TABLA 10
-- 10. TRANSACCIONES
-- Tabla más importante: registra TODOS los movimientos financieros
-- El proyecto pide: depósitos, retiros, transferencias, pagos, compras
-- id_extracto: opcional, permite saber a qué extracto aplica un pago

CREATE TABLE transacciones (
    id_transaccion      INT AUTO_INCREMENT PRIMARY KEY,
    id_producto_pasivo  INT NULL,           -- origen o destino en cuentas
    id_producto_activo  INT NULL,           -- origen o destino en créditos/tarjetas
    id_tipo_transaccion INT NOT NULL,
    id_extracto         INT NULL,           -- si es pago de cuota, referencia el extracto (se agrego)
    monto               DECIMAL(18,2) NOT NULL CHECK (monto > 0),
    fecha_transaccion   DATETIME DEFAULT CURRENT_TIMESTAMP, -- (se agrego)
    canal               VARCHAR(50) NULL,   -- App, Web, Cajero, Corresponsal
    ip_origen           VARCHAR(45) NULL,   -- trazabilidad de seguridad
    FOREIGN KEY (id_producto_pasivo)  REFERENCES producto_pasivo(id_producto_pasivo),
    FOREIGN KEY (id_producto_activo)  REFERENCES producto_activo(id_producto_activo),
    FOREIGN KEY (id_tipo_transaccion) REFERENCES tipo_transaccion(id_tipo_transaccion),
    FOREIGN KEY (id_extracto)         REFERENCES extracto(id_extracto)
) ENGINE=InnoDB;

-- TABLA 11
-- 11. MORA
-- Seguimiento de clientes en situación de morosidad
-- El proyecto pide: clientes en mora, monto deuda, fechas vencimiento
-- Regla de negocio: solo puede existir mora si hay un extracto impago

CREATE TABLE mora (
    id_mora            INT AUTO_INCREMENT PRIMARY KEY,
    id_producto_activo INT NOT NULL,
    id_extracto        INT NOT NULL,        -- el extracto que no se pagó genera la mora (se agrego)
    fecha_inicio_mora  DATE NOT NULL,
    dias_mora          INT DEFAULT 0,
    capital_vencido    DECIMAL(18,2) NOT NULL,
    interes_mora       DECIMAL(18,2) DEFAULT 0.00,
    estado_mora        ENUM('Activa', 'En Gestion', 'Liquidada') DEFAULT 'Activa',
    FOREIGN KEY (id_producto_activo) REFERENCES producto_activo(id_producto_activo),
    FOREIGN KEY (id_extracto)        REFERENCES extracto(id_extracto)
) ENGINE=InnoDB;

-- TABLA 12 
-- 12. GESTION_COBRANZA
-- Procesos de recuperacion de cartera en mora
-- El proyecto pide: "procesos de recuperacion"
-- resultado_gestion es fundamental — sin el no sabemos que paso

CREATE TABLE gestion_cobranza (
    id_gestion        INT AUTO_INCREMENT PRIMARY KEY,
    id_mora           INT NOT NULL,
    fecha_gestion     DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_contacto     ENUM('Llamada', 'Correo', 'SMS', 'Visita Domiciliaria') NOT NULL,
    resultado_gestion TEXT NOT NULL,        -- ejemplo: "Cliente promete pagar el viernes" (se agrego)
    FOREIGN KEY (id_mora) REFERENCES mora(id_mora)
) ENGINE=InnoDB;

