# 📊 Consultas de Negocio — Banca Digital

> Proyecto Integrador | Bootcamp Análisis de Datos | Grupo 1 | Betek 2026

Las consultas están organizadas en **4 bloques** orientados a la toma de decisiones financieras. Cada consulta responde una pregunta de negocio concreta con datos reales de la base de datos.

---

## 💰 Bloque 1 — Rentabilidad y Salud Financiera

### Q1 — Activos totales vs Pasivos
**Pregunta:** ¿Cuánto dinero tiene prestado el banco y cuánto tienen depositado los clientes?

```sql
SELECT ROUND(SUM(monto_aprobado), 0) AS cartera_activa
FROM producto_activo WHERE estado = 'Vigente';

SELECT ROUND(SUM(saldo_actual), 0) AS total_depositos
FROM producto_pasivo;
```

**Resultado:**
| Indicador | Valor |
|-----------|-------|
| Cartera activa (prestado) | $128.440.200.000 |
| Total depósitos clientes | $136.544.315.000 |

**Insight:** Los depósitos superan la cartera prestada en $8.144.115.000 — el banco mantiene **liquidez positiva**. Por cada peso que presta tiene más de un peso depositado.

---

### Q2 — Ingresos proyectados por intereses
**Pregunta:** ¿Cuánto genera el banco mensualmente por su cartera activa?

```sql
SELECT ROUND(SUM(monto_aprobado * tasa_interes_mensual / 100), 0) AS ingresos_intereses_mes
FROM producto_activo WHERE estado = 'Vigente';
```

**Resultado:** **$1.959.337.770 mensuales** en ingresos proyectados por intereses.

**Insight:** El banco genera aproximadamente $1.959 millones al mes solo por intereses de su cartera vigente — sin contar cuotas de manejo ni comisiones.

---

### Q3 — Rentabilidad por tipo de producto
**Pregunta:** ¿Qué productos generan más ingresos al banco?

```sql
SELECT pb.nombre_producto,
    COUNT(pa.id_producto_activo) AS total_contratos,
    ROUND(SUM(pa.monto_aprobado * pa.tasa_interes_mensual / 100), 0) AS ingreso_mensual_proyectado
FROM producto_activo pa
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
WHERE pa.estado = 'Vigente'
GROUP BY pb.nombre_producto
ORDER BY ingreso_mensual_proyectado DESC;
```

**Resultado:**
| Producto | Contratos | Ingreso mensual proyectado |
|----------|-----------|---------------------------|
| Crédito Automotriz | 148 | Mayor ingreso |
| Tarjeta de Crédito Black | 209 | Segundo lugar |
| Tarjeta de Crédito Platinum | 203 | Tercer lugar |

**Insight:** El Crédito Automotriz es el producto más rentable por su alto monto promedio ($687M) aunque tiene menos contratos que las tarjetas.

---

## 📉 Bloque 2 — Cartera Vencida y Mora

### Q4 — Clientes en mora activa con detalle de deuda
**Pregunta:** ¿Quiénes deben, cuánto deben y hace cuántos días están en mora?

```sql
SELECT c.nombre, c.apellido, ci.nombre_ciudad, d.nombre_departamento,
    pb.nombre_producto, m.dias_mora, m.capital_vencido,
    m.capital_vencido + m.interes_mora AS deuda_total, m.estado_mora
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN cliente c ON pa.id_cliente = c.id_cliente
JOIN ciudades ci ON c.id_ciudad = ci.id_ciudad
JOIN departamentos d ON ci.id_departamento = d.id_departamento
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
WHERE m.estado_mora IN ('Activa', 'En Gestión')
ORDER BY m.capital_vencido DESC LIMIT 20;
```

**Top 3 clientes con mayor deuda:**
| Cliente | Ciudad | Producto | Días mora | Deuda total |
|---------|--------|----------|-----------|-------------|
| Luis Miguel Gutiérrez | Puerto Nariño, Amazonas | Crédito Automotriz | 1.048 | $75.359.402 |
| Valerio Valentín | Carmen del Darién, Chocó | Crédito Automotriz | 959 | $68.007.997 |
| Nidia Pardo | Pitalito, Huila | Crédito Automotriz | 348 | $51.235.933 |

**Insight:** El Crédito Automotriz concentra los mayores montos de deuda vencida. Los departamentos de Amazonas y Chocó aparecen en los primeros lugares — coherente con la concentración de riesgo en zonas de menor desarrollo económico.

---

### Q5 — Cartera vencida por tipo de producto
**Pregunta:** ¿Qué productos generan mayor riesgo de impago?

```sql
SELECT pb.nombre_producto, COUNT(m.id_mora) AS total_moras,
    ROUND(AVG(m.dias_mora), 0) AS dias_mora_promedio,
    SUM(m.capital_vencido + m.interes_mora) AS deuda_total
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
GROUP BY pb.nombre_producto ORDER BY deuda_total DESC;
```

**Resultado:**
| Producto | Moras | Días promedio | Deuda total |
|----------|-------|---------------|-------------|
| Crédito Automotriz | 25 | 635 | $804.894.058 |
| Tarjeta de Crédito Black | 43 | 642 | $647.224.415 |
| Tarjeta de Crédito Platinum | 50 | 720 | $433.406.010 |
| Tarjeta de Crédito Oro | 52 | 658 | $199.237.349 |
| Crédito Libre Inversión | 59 | 662 | $107.235.670 |
| Crédito Estudios | 47 | 712 | $60.923.483 |
| Crédito Hipotecario | 10 | 660 | $40.883.144 |

**Insight:** El Crédito Automotriz tiene la mayor deuda total con solo 25 casos — alto monto por mora. El Hipotecario tiene la menor deuda total — los clientes priorizan pagar su vivienda.

---

### Q6 — Cartera vencida por departamento
**Pregunta:** ¿En qué regiones se concentra el mayor riesgo crediticio?

```sql
SELECT d.nombre_departamento, COUNT(DISTINCT pa.id_cliente) AS clientes_en_mora,
    SUM(m.capital_vencido) AS capital_vencido_total,
    ROUND(AVG(m.dias_mora), 0) AS dias_mora_promedio,
    SUM(m.capital_vencido + m.interes_mora) AS deuda_total
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN cliente c ON pa.id_cliente = c.id_cliente
JOIN ciudades ci ON c.id_ciudad = ci.id_ciudad
JOIN departamentos d ON ci.id_departamento = d.id_departamento
GROUP BY d.nombre_departamento ORDER BY capital_vencido_total DESC LIMIT 10;
```

**Top 5 departamentos con mayor mora:**
| Departamento | Clientes | Capital vencido | Días mora prom | Deuda total |
|--------------|----------|-----------------|----------------|-------------|
| Antioquia | 34 | $270.608.436 | 624 | $402.854.757 |
| Santander | 36 | $191.268.845 | 687 | $301.435.108 |
| Chocó | 17 | $180.283.789 | 706 | $275.712.049 |
| Huila | 6 | $91.367.907 | 597 | $116.932.991 |
| Boyacá | 16 | $73.234.141 | 716 | $108.814.224 |

**Insight:** Chocó tiene solo 17 clientes pero $275M en deuda — deuda promedio por cliente muy alta. Amazonas tiene los días de mora más altos (915 días) — casi 3 años sin pagar.

---

### Q7 — Moras sin gestión de cobranza registrada
**Pregunta:** ¿Qué clientes cayeron en mora sin ser contactados?

```sql
SELECT c.nombre, c.apellido, pb.nombre_producto, m.dias_mora, m.estado_mora
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN cliente c ON pa.id_cliente = c.id_cliente
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
WHERE m.id_mora NOT IN (SELECT DISTINCT id_mora FROM gestion_cobranza)
ORDER BY m.dias_mora DESC;
```

**Resultado:** Sin resultados — 0 clientes en mora sin contactar.

**Insight:** El banco tiene **trazabilidad completa** — el 100% de los clientes en mora han sido contactados al menos una vez. Esto es una fortaleza del proceso de cobranza.

---

### Q8 — Clientes con saldo disponible y mora activa
**Pregunta:** ¿Qué clientes tienen dinero en cuenta pero no han pagado su deuda?

```sql
SELECT c.nombre, c.apellido, ci.nombre_ciudad,
    SUM(pp.saldo_actual) AS saldo_disponible,
    m.capital_vencido + m.interes_mora AS deuda_total,
    m.dias_mora
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN cliente c ON pa.id_cliente = c.id_cliente
JOIN ciudades ci ON c.id_ciudad = ci.id_ciudad
JOIN producto_pasivo pp ON c.id_cliente = pp.id_cliente
GROUP BY c.id_cliente, c.nombre, c.apellido, ci.nombre_ciudad,
         m.capital_vencido, m.interes_mora, m.dias_mora
HAVING saldo_disponible > deuda_total
ORDER BY saldo_disponible DESC LIMIT 15;
```

**Casos más críticos:**
| Cliente | Ciudad | Saldo disponible | Deuda total | Días mora |
|---------|--------|------------------|-------------|-----------|
| Zoraida Rovira | Carcasí | $1.335.899.000 | $579.709 | 745 |
| Nadia Tormo | Cisneros | $1.270.907.000 | $5.633.444 | 379 |
| Amada Falco | Candelaria | $1.198.102.000 | $6.912.101 | 959 |

**Insight:** Estos clientes tienen suficiente dinero en cuenta para pagar su deuda varias veces. **Recomendación:** implementar débito automático con autorización previa para recuperar esta cartera sin gestión de cobranza adicional.

---

## 📞 Bloque 3 — Eficiencia de Cobranza

### Q9 — Tasa de resolución por canal de contacto
**Pregunta:** ¿Qué canal de cobranza es más efectivo para recuperar cartera?

```sql
SELECT gc.tipo_contacto, COUNT(gc.id_gestion) AS total_gestiones,
    SUM(CASE WHEN m.estado_mora = 'Liquidada' THEN 1 ELSE 0 END) AS moras_liquidadas,
    ROUND(SUM(CASE WHEN m.estado_mora = 'Liquidada' THEN 1 ELSE 0 END) * 100.0 / COUNT(gc.id_gestion), 2) AS tasa_efectividad
FROM gestion_cobranza gc
JOIN mora m ON gc.id_mora = m.id_mora
GROUP BY gc.tipo_contacto ORDER BY tasa_efectividad DESC;
```

**Resultado:**
| Canal | Gestiones | Moras liquidadas | Tasa efectividad |
|-------|-----------|------------------|------------------|
| Correo | 139 | 23 | 16.55% |
| Llamada | 249 | 35 | 14.06% |
| Visita Domiciliaria | 244 | 25 | 10.25% |

**Insight:** El Correo es el canal más efectivo con 16.55% — y el menos costoso operativamente. La Visita Domiciliaria es la más costosa y la menos efectiva. **Recomendación:** redirigir recursos de visitas domiciliarias hacia gestión por correo electrónico.

---

### Q10 — Tiempo promedio de resolución de mora por producto
**Pregunta:** ¿Cuántos días tarda en promedio cerrar una mora por tipo de producto?

```sql
SELECT pb.nombre_producto, COUNT(m.id_mora) AS total_moras,
    ROUND(AVG(m.dias_mora), 0) AS dias_mora_promedio,
    MIN(m.dias_mora) AS dias_minimo, MAX(m.dias_mora) AS dias_maximo,
    SUM(CASE WHEN m.estado_mora = 'Liquidada' THEN 1 ELSE 0 END) AS moras_liquidadas
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
GROUP BY pb.nombre_producto ORDER BY dias_mora_promedio DESC;
```

**Resultado:**
| Producto | Moras | Días promedio | Liquidadas |
|----------|-------|---------------|------------|
| Tarjeta Platinum | 50 | 720 | 12 |
| Crédito Estudios | 47 | 712 | 5 |
| Crédito Libre Inversión | 59 | 662 | 4 |
| Crédito Hipotecario | 10 | 660 | 0 |
| Tarjeta Oro | 52 | 658 | 8 |
| Tarjeta Black | 43 | 642 | 4 |
| Crédito Automotriz | 25 | 635 | 2 |

**Insight:** El Crédito Hipotecario tiene 0 moras liquidadas — ninguna se ha resuelto. La Tarjeta Platinum tiene el mayor promedio de días pero también la mayor cantidad de liquidaciones (12).

---

### Q11 — Casos críticos con múltiples gestiones sin liquidar
**Pregunta:** ¿Qué clientes requieren escalamiento a proceso jurídico?

```sql
SELECT c.nombre, c.apellido, ci.nombre_ciudad, d.nombre_departamento,
    pb.nombre_producto, m.dias_mora, m.capital_vencido, m.estado_mora,
    COUNT(gc.id_gestion) AS total_gestiones, MAX(gc.fecha_gestion) AS ultima_gestion
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
ORDER BY m.dias_mora DESC LIMIT 15;
```

**Insight:** Clientes con más de 3 gestiones sin resolver y más de 900 días de mora son candidatos directos a proceso jurídico. Destacan casos en Chocó, Santander y Tolima.

---

### Q12 — KPI ejecutivos de cartera
**Pregunta:** ¿Cuál es el estado global de la cartera del banco?

```sql
SELECT 
    ROUND(SUM(pa.monto_aprobado), 0) AS cartera_total,
    ROUND(SUM(CASE WHEN pa.estado = 'Vigente' THEN pa.monto_aprobado ELSE 0 END), 0) AS cartera_vigente,
    ROUND(SUM(CASE WHEN pa.estado = 'En_Mora' THEN pa.monto_aprobado ELSE 0 END), 0) AS cartera_en_mora,
    ROUND(SUM(CASE WHEN pa.estado = 'Castigada' THEN pa.monto_aprobado ELSE 0 END), 0) AS cartera_castigada,
    ROUND(SUM(m.capital_vencido) * 100.0 / SUM(CASE WHEN pa.estado = 'Vigente' THEN pa.monto_aprobado ELSE 0 END), 2) AS tasa_morosidad_real
FROM producto_activo pa
LEFT JOIN mora m ON pa.id_producto_activo = m.id_producto_activo;
```

**Resultado:**
| KPI | Valor |
|-----|-------|
| Cartera total | $191.709.400.000 |
| Cartera vigente | $128.440.200.000 |
| Cartera en mora | $18.072.100.000 |
| Cartera castigada | $3.947.000.000 |
| Tasa morosidad real | 1.20% |
| Promedio sector Colombia | 3% - 8% |

**Insight:** La tasa de morosidad real del 1.20% está muy por debajo del promedio del sector financiero colombiano (3-8%) — el banco tiene una cartera sana y bien gestionada.

---

## 🔐 Bloque 4 — Seguridad

### Q13 — Intentos fallidos de autenticación
**Pregunta:** ¿Qué cuentas están bajo riesgo de acceso no autorizado?

```sql
SELECT c.nombre, c.apellido, ci.nombre_ciudad, d.nombre_departamento,
    ac.nombre_usuario, ac.intentos_fallidos, ac.estado, ac.ultimo_ingreso
FROM autenticacion_cliente ac
JOIN cliente c ON ac.id_cliente = c.id_cliente
JOIN ciudades ci ON c.id_ciudad = ci.id_ciudad
JOIN departamentos d ON ci.id_departamento = d.id_departamento
WHERE ac.intentos_fallidos > 0
ORDER BY ac.intentos_fallidos DESC LIMIT 20;
```

**Insight:** Los usuarios con 3 intentos fallidos están bloqueados o suspendidos — el sistema de seguridad funciona correctamente. Se identifican cuentas que requieren verificación de identidad adicional antes de desbloquear.

---

### Q14 — Transacciones por canal
**Pregunta:** ¿Qué canales concentran mayor volumen y riesgo transaccional?

```sql
SELECT canal, COUNT(*) AS total_transacciones,
    ROUND(SUM(monto), 0) AS dinero_total,
    ROUND(AVG(monto), 0) AS monto_promedio,
    ROUND(COUNT(*) * 100.0 / 419623, 2) AS porcentaje_transacciones
FROM transacciones
GROUP BY canal ORDER BY total_transacciones DESC;
```

**Insight:** La App Móvil concentra el 45% de las transacciones — confirma que el banco es verdaderamente digital. El Corresponsal Bancario tiene el menor volumen pero es crítico en departamentos pobres donde la penetración digital es baja.

---

### Q15 — Transacciones en horario nocturno con montos altos
**Pregunta:** ¿Hay transacciones sospechosas fuera del horario habitual?

```sql
SELECT c.nombre, c.apellido, ci.nombre_ciudad, t.canal, t.ip_origen,
    t.monto, t.fecha_transaccion, tt.nombre_tipo
FROM transacciones t
JOIN producto_pasivo pp ON t.id_producto_pasivo = pp.id_producto_pasivo
JOIN cliente c ON pp.id_cliente = c.id_cliente
JOIN ciudades ci ON c.id_ciudad = ci.id_ciudad
JOIN tipo_transaccion tt ON t.id_tipo_transaccion = tt.id_tipo_transaccion
WHERE HOUR(t.fecha_transaccion) BETWEEN 0 AND 5
AND t.monto > 5000000
ORDER BY t.monto DESC LIMIT 20;
```

**Insight:** Transacciones de alto monto entre las 12am y 5am son señales de alerta. El banco debe implementar verificación adicional (OTP o llamada de confirmación) para transacciones nocturnas superiores a $5.000.000.

---

## 📌 Resumen de Hallazgos

| # | Hallazgo | Recomendación |
|---|----------|---------------|
| 1 | Depósitos superan cartera — liquidez positiva | Mantener política de crédito conservadora |
| 2 | Crédito Automotriz: mayor riesgo y mayor ingreso | Fortalecer análisis de crédito para este producto |
| 3 | Tasa de morosidad 1.20% — por debajo del sector | Mantener criterios de originación actuales |
| 4 | Correo es el canal más efectivo de cobranza | Redirigir recursos de visitas a gestión digital |
| 5 | Clientes con saldo > deuda sin pagar | Implementar débito automático con autorización |
| 6 | 100% de moras tienen gestión registrada | Trazabilidad completa — proceso bien estructurado |
| 7 | Hipotecario: 0 moras liquidadas | Revisar estrategia de cobranza para este producto |
| 8 | Chocó y Amazonas: mayor mora per cápita | Ajustar política de originación en estas regiones |
