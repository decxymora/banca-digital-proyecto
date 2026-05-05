
-- BANCA DIGITAL — Consultas de Negocio
-- Proyecto Integrador — Bootcamp Análisis de Datos

USE BANCA_DIGITAL;

-- BLOQUE 1 — RENTABILIDAD Y SALUD FINANCIERA

-- Q1: Activos totales vs pasivos
-- ¿Cuánto dinero tiene prestado el banco y cuánto tienen depositado los clientes?
SELECT 
    ROUND(SUM(monto_aprobado), 0) AS cartera_activa
FROM producto_activo
WHERE estado = 'Vigente';

SELECT 
    ROUND(SUM(saldo_actual), 0) AS total_depositos
FROM producto_pasivo;

-- Q2: Ingresos proyectados por intereses
-- ¿Cuánto genera el banco mensualmente por su cartera activa?
SELECT 
    ROUND(SUM(monto_aprobado * tasa_interes_mensual / 100), 0) AS ingresos_intereses_mes
FROM producto_activo
WHERE estado = 'Vigente';

-- Q3: Rentabilidad por tipo de producto
-- ¿Qué productos generan más ingresos al banco?
SELECT 
    pb.nombre_producto,
    COUNT(pa.id_producto_activo) AS total_contratos,
    ROUND(AVG(pa.monto_aprobado), 0) AS monto_promedio,
    SUM(pa.monto_aprobado) AS cartera_total,
    ROUND(SUM(pa.monto_aprobado * pa.tasa_interes_mensual / 100), 0) AS ingreso_mensual_proyectado
FROM producto_activo pa
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
WHERE pa.estado = 'Vigente'
GROUP BY pb.nombre_producto
ORDER BY ingreso_mensual_proyectado DESC;

-- BLOQUE 2 — CARTERA VENCIDA Y MORA
-- Q4: Clientes en mora activa con detalle de deuda
-- ¿Quiénes deben, cuánto deben y hace cuántos días están en mora?
SELECT 
    c.id_cliente,
    c.nombre,
    c.apellido,
    ci.nombre_ciudad,
    d.nombre_departamento,
    pa.estado AS estado_producto,
    pb.nombre_producto,
    m.dias_mora,
    m.capital_vencido,
    m.interes_mora,
    m.capital_vencido + m.interes_mora AS deuda_total,
    m.estado_mora
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN cliente c ON pa.id_cliente = c.id_cliente
JOIN ciudades ci ON c.id_ciudad = ci.id_ciudad
JOIN departamentos d ON ci.id_departamento = d.id_departamento
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
WHERE m.estado_mora IN ('Activa', 'En Gestión')
ORDER BY m.capital_vencido DESC
LIMIT 20;

-- Q5: Cartera vencida por tipo de producto
-- ¿Qué productos generan mayor riesgo de impago?
SELECT 
    pb.nombre_producto,
    COUNT(m.id_mora) AS total_moras,
    ROUND(AVG(m.dias_mora), 0) AS dias_mora_promedio,
    SUM(m.capital_vencido) AS capital_vencido,
    SUM(m.interes_mora) AS intereses_mora,
    SUM(m.capital_vencido + m.interes_mora) AS deuda_total
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
GROUP BY pb.nombre_producto
ORDER BY deuda_total DESC;

-- Q6: Cartera vencida por departamento
-- ¿En qué regiones se concentra el mayor riesgo crediticio?
SELECT 
    d.nombre_departamento,
    COUNT(DISTINCT pa.id_cliente) AS clientes_en_mora,
    SUM(m.capital_vencido) AS capital_vencido_total,
    ROUND(AVG(m.dias_mora), 0) AS dias_mora_promedio,
    SUM(m.capital_vencido + m.interes_mora) AS deuda_total
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN cliente c ON pa.id_cliente = c.id_cliente
JOIN ciudades ci ON c.id_ciudad = ci.id_ciudad
JOIN departamentos d ON ci.id_departamento = d.id_departamento
GROUP BY d.nombre_departamento
ORDER BY capital_vencido_total DESC
LIMIT 10;

-- Q7: Moras sin gestión de cobranza registrada
-- ¿Qué clientes cayeron en mora sin ser contactados?
SELECT 
    c.nombre,
    c.apellido,
    ci.nombre_ciudad,
    d.nombre_departamento,
    pb.nombre_producto,
    m.dias_mora,
    m.capital_vencido,
    m.estado_mora
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN cliente c ON pa.id_cliente = c.id_cliente
JOIN ciudades ci ON c.id_ciudad = ci.id_ciudad
JOIN departamentos d ON ci.id_departamento = d.id_departamento
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
WHERE m.id_mora NOT IN (
    SELECT DISTINCT id_mora FROM gestion_cobranza
)
ORDER BY m.dias_mora DESC;

-- Q8: Clientes con saldo disponible y mora activa
-- ¿Qué clientes tienen dinero en cuenta pero no han pagado su deuda?
SELECT 
    c.id_cliente,
    c.nombre,
    c.apellido,
    ci.nombre_ciudad,
    SUM(pp.saldo_actual) AS saldo_disponible,
    m.capital_vencido,
    m.capital_vencido + m.interes_mora AS deuda_total,
    m.dias_mora,
    SUM(pp.saldo_actual) - (m.capital_vencido + m.interes_mora) AS diferencia
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN cliente c ON pa.id_cliente = c.id_cliente
JOIN ciudades ci ON c.id_ciudad = ci.id_ciudad
JOIN producto_pasivo pp ON c.id_cliente = pp.id_cliente
GROUP BY c.id_cliente, c.nombre, c.apellido, ci.nombre_ciudad,
         m.capital_vencido, m.interes_mora, m.dias_mora
HAVING saldo_disponible > deuda_total
ORDER BY saldo_disponible DESC
LIMIT 15;

-- BLOQUE 3 — EFICIENCIA DE COBRANZA

-- Q9: Tasa de resolución por canal de contacto
-- ¿Qué canal de cobranza es más efectivo para recuperar cartera?
SELECT 
    gc.tipo_contacto,
    COUNT(gc.id_gestion) AS total_gestiones,
    SUM(CASE WHEN m.estado_mora = 'Liquidada' THEN 1 ELSE 0 END) AS moras_liquidadas,
    ROUND(SUM(CASE WHEN m.estado_mora = 'Liquidada' THEN 1 ELSE 0 END) * 100.0 / COUNT(gc.id_gestion), 2) AS tasa_efectividad
FROM gestion_cobranza gc
JOIN mora m ON gc.id_mora = m.id_mora
GROUP BY gc.tipo_contacto
ORDER BY tasa_efectividad DESC;

-- Q10: Tiempo promedio de resolución de mora por producto
-- ¿Cuántos días tarda en promedio cerrar una mora por tipo de producto?
SELECT 
    pb.nombre_producto,
    COUNT(m.id_mora) AS total_moras,
    ROUND(AVG(m.dias_mora), 0) AS dias_mora_promedio,
    MIN(m.dias_mora) AS dias_minimo,
    MAX(m.dias_mora) AS dias_maximo,
    SUM(CASE WHEN m.estado_mora = 'Liquidada' THEN 1 ELSE 0 END) AS moras_liquidadas
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
GROUP BY pb.nombre_producto
ORDER BY dias_mora_promedio DESC;

-- Q11: Casos críticos con múltiples gestiones sin liquidar
-- ¿Qué clientes requieren escalamiento a proceso jurídico?
SELECT 
    c.nombre,
    c.apellido,
    ci.nombre_ciudad,
    d.nombre_departamento,
    pb.nombre_producto,
    m.dias_mora,
    m.capital_vencido,
    m.estado_mora,
    COUNT(gc.id_gestion) AS total_gestiones,
    MAX(gc.fecha_gestion) AS ultima_gestion
FROM mora m
JOIN gestion_cobranza gc ON m.id_mora = gc.id_mora
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN cliente c ON pa.id_cliente = c.id_cliente
JOIN ciudades ci ON c.id_ciudad = ci.id_ciudad
JOIN departamentos d ON ci.id_departamento = d.id_departamento
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
WHERE m.estado_mora IN ('Activa', 'En Gestión')
GROUP BY c.nombre, c.apellido, ci.nombre_ciudad, d.nombre_departamento,
         pb.nombre_producto, m.dias_mora, m.capital_vencido, m.estado_mora
HAVING total_gestiones >= 3
ORDER BY m.dias_mora DESC
LIMIT 15;

-- Q12: KPI ejecutivos de cartera
-- ¿Cuál es el estado global de la cartera del banco?
SELECT 
    ROUND(SUM(pa.monto_aprobado), 0) AS cartera_total,
    ROUND(SUM(CASE WHEN pa.estado = 'Vigente' THEN pa.monto_aprobado ELSE 0 END), 0) AS cartera_vigente,
    ROUND(SUM(CASE WHEN pa.estado = 'En_Mora' THEN pa.monto_aprobado ELSE 0 END), 0) AS cartera_en_mora,
    ROUND(SUM(CASE WHEN pa.estado = 'Castigada' THEN pa.monto_aprobado ELSE 0 END), 0) AS cartera_castigada,
    ROUND(SUM(CASE WHEN pa.estado = 'Cancelada' THEN pa.monto_aprobado ELSE 0 END), 0) AS cartera_cancelada,
    ROUND(SUM(CASE WHEN pa.estado IN ('En_Mora', 'Castigada') THEN pa.monto_aprobado ELSE 0 END) * 100.0 / SUM(pa.monto_aprobado), 2) AS tasa_morosidad_exposicion,
    ROUND(SUM(m.capital_vencido) * 100.0 / SUM(CASE WHEN pa.estado = 'Vigente' THEN pa.monto_aprobado ELSE 0 END), 2) AS tasa_morosidad_real
FROM producto_activo pa
LEFT JOIN mora m ON pa.id_producto_activo = m.id_producto_activo;


-- BLOQUE 4 — SEGURIDAD

-- Q13: Intentos fallidos de autenticación
-- ¿Qué cuentas están bajo riesgo de acceso no autorizado?
SELECT 
    c.id_cliente,
    c.nombre,
    c.apellido,
    ci.nombre_ciudad,
    d.nombre_departamento,
    ac.nombre_usuario,
    ac.intentos_fallidos,
    ac.estado,
    ac.ultimo_ingreso
FROM autenticacion_cliente ac
JOIN cliente c ON ac.id_cliente = c.id_cliente
JOIN ciudades ci ON c.id_ciudad = ci.id_ciudad
JOIN departamentos d ON ci.id_departamento = d.id_departamento
WHERE ac.intentos_fallidos > 0
ORDER BY ac.intentos_fallidos DESC
LIMIT 20;

-- Q14: Transacciones por canal
-- ¿Qué canales concentran mayor volumen y riesgo transaccional?
SELECT 
    canal,
    COUNT(*) AS total_transacciones,
    ROUND(SUM(monto), 0) AS dinero_total,
    ROUND(AVG(monto), 0) AS monto_promedio,
    ROUND(COUNT(*) * 100.0 / 419623, 2) AS porcentaje_transacciones
FROM transacciones
GROUP BY canal
ORDER BY total_transacciones DESC;

