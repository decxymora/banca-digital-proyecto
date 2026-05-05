# Consultas de Negocio — Banca Digital

> Proyecto Integrador | Bootcamp Análisis de Datos | Grupo 1 | Betek 2026

Las consultas están organizadas en **4 bloques** orientados a la toma de decisiones financieras. Cada consulta responde una pregunta de negocio concreta con datos reales de la base de datos.

---

## Bloque 1 — Rentabilidad y Salud Financiera

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

**Hallazgo:** Los depósitos superan la cartera prestada en $8.144.115.000 — el banco mantiene **liquidez positiva**. Por cada peso que presta tiene más de un peso depositado. Señal de solidez financiera.

---

### Q2 — Ingresos proyectados por intereses
**Pregunta:** ¿Cuánto genera el banco mensualmente por su cartera activa?

```sql
SELECT ROUND(SUM(monto_aprobado * tasa_interes_mensual / 100), 0) AS ingresos_intereses_mes
FROM producto_activo WHERE estado = 'Vigente';
```

**Resultado:** **$1.959.337.770 mensuales** en ingresos proyectados por intereses.

**Hallazgo:** El banco genera aproximadamente $1.959 millones al mes solo por intereses de su cartera vigente — sin contar cuotas de manejo ni comisiones. Proyectado anualmente representa más de $23.512 millones.

---

### Q3 — Rentabilidad por tipo de producto
**Pregunta:** ¿Qué productos generan más ingresos al banco?

```sql
SELECT pb.nombre_producto,
    COUNT(pa.id_producto_activo) AS total_contratos,
    ROUND(AVG(pa.monto_aprobado), 0) AS monto_promedio,
    SUM(pa.monto_aprobado) AS cartera_total,
    ROUND(SUM(pa.monto_aprobado * pa.tasa_interes_mensual / 100), 0) AS ingreso_mensual_proyectado
FROM producto_activo pa
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
WHERE pa.estado = 'Vigente'
GROUP BY pb.nombre_producto
ORDER BY ingreso_mensual_proyectado DESC;
```

**Resultado:**
| Producto | Contratos | Monto promedio | Cartera total | Ingreso mensual proyectado |
|----------|-----------|----------------|---------------|---------------------------|
| Crédito Automotriz | 148 | $699.989.189 | $103.598.400.000 | $1.553.240.030 |
| Crédito Libre Inversión | 233 | $41.453.648 | $9.658.700.000 | $160.067.940 |
| Tarjeta de Crédito Black | 209 | $19.660.287 | $4.109.000.000 | $73.940.350 |
| Crédito Hipotecario | 22 | $234.063.636 | $5.149.400.000 | $64.837.110 |
| Crédito Estudios | 144 | $19.552.778 | $2.815.600.000 | $42.724.680 |
| Tarjeta de Crédito Platinum | 203 | $9.946.305 | $2.019.100.000 | $41.202.940 |
| Tarjeta de Crédito Oro | 251 | $4.342.629 | $1.090.000.000 | $23.324.720 |

**Hallazgo:** El Crédito Automotriz genera el **79% de los ingresos mensuales del banco** con solo 148 contratos — es el producto más rentable por su alto monto promedio ($699M). Sin embargo es también el producto con mayor concentración de riesgo. El Crédito Hipotecario tiene el segundo monto promedio más alto ($234M) pero muy pocos contratos (22).

---

## 📉 Bloque 2 — Cartera Vencida y Mora

### Q4 — Clientes en mora activa con detalle de deuda
**Pregunta:** ¿Quiénes deben, cuánto deben y hace cuántos días están en mora?

```sql
SELECT c.nombre, c.apellido, ci.nombre_ciudad, d.nombre_departamento,
    pa.estado AS estado_producto, pb.nombre_producto, m.dias_mora,
    m.capital_vencido, m.interes_mora,
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

**Top 5 clientes con mayor deuda:**
| Cliente | Ciudad | Producto | Días mora | Capital vencido | Deuda total |
|---------|--------|----------|-----------|-----------------|-------------|
| Luis Miguel Gutiérrez | Puerto Nariño, Amazonas | Crédito Automotriz | 1.048 | $47.804.746 | $75.359.402 |
| Valerio Valentín | Carmen del Darién, Chocó | Crédito Automotriz | 959 | $42.994.237 | $68.007.997 |
| Nidia Pardo | Pitalito, Huila | Crédito Automotriz | 348 | $42.385.782 | $51.235.933 |
| Febe Amaya | Puerto Wilches, Santander | Crédito Automotriz | 836 | $40.112.674 | $65.375.101 |
| Benito Aramburu | Cácota, Norte de Santander | Crédito Automotriz | 683 | $38.560.728 | $49.973.418 |

**Hallazgo:** El Crédito Automotriz domina los primeros lugares de mora. Los departamentos de Amazonas, Chocó y Santander concentran los casos más críticos. Los dos primeros clientes tienen estado **Castigada** — el banco ya asumió la pérdida contablemente pero los intereses siguen corriendo, lo que eleva la deuda total significativamente.

---

### Q5 — Cartera vencida por tipo de producto
**Pregunta:** ¿Qué productos generan mayor riesgo de impago?

```sql
SELECT pb.nombre_producto, COUNT(m.id_mora) AS total_moras,
    ROUND(AVG(m.dias_mora), 0) AS dias_mora_promedio,
    SUM(m.capital_vencido) AS capital_vencido,
    SUM(m.interes_mora) AS intereses_mora,
    SUM(m.capital_vencido + m.interes_mora) AS deuda_total
FROM mora m
JOIN producto_activo pa ON m.id_producto_activo = pa.id_producto_activo
JOIN productos_banco pb ON pa.id_producto_banco = pb.id_producto_banco
GROUP BY pb.nombre_producto ORDER BY deuda_total DESC;
```

**Resultado:**
| Producto | Moras | Días promedio | Capital vencido | Intereses mora | Deuda total |
|----------|-------|---------------|-----------------|----------------|-------------|
| Crédito Automotriz | 25 | 635 | $572.582.385 | $232.311.673 | $804.894.058 |
| Tarjeta de Crédito Black | 43 | 642 | $433.858.937 | $213.365.478 | $647.224.415 |
| Tarjeta de Crédito Platinum | 50 | 720 | $266.476.813 | $166.929.197 | $433.406.010 |
| Tarjeta de Crédito Oro | 52 | 658 | $124.598.467 | $74.638.882 | $199.237.349 |
| Crédito Libre Inversión | 59 | 662 | $71.387.202 | $35.848.468 | $107.235.670 |
| Crédito Estudios | 47 | 712 | $41.301.131 | $19.622.352 | $60.923.483 |
| Crédito Hipotecario | 10 | 660 | $30.123.646 | $10.759.498 | $40.883.144 |

**Hallazgo:** El Crédito Automotriz tiene la mayor deuda total con solo 25 casos — un monto promedio de $32M por mora. Las Tarjetas de Crédito Black y Platinum representan juntas más de $1.080M en deuda vencida. El Crédito Hipotecario tiene la menor deuda total — los clientes priorizan pagar su vivienda sobre cualquier otro producto.

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

**Resultado:**
| Departamento | Clientes | Capital vencido | Días mora prom | Deuda total |
|--------------|----------|-----------------|----------------|-------------|
| Antioquia | 34 | $270.608.436 | 624 | $402.854.757 |
| Santander | 36 | $191.268.845 | 687 | $301.435.108 |
| Chocó | 17 | $180.283.789 | 706 | $275.712.049 |
| Huila | 6 | $91.367.907 | 597 | $116.932.991 |
| Boyacá | 16 | $73.234.141 | 716 | $108.814.224 |
| Bolívar | 9 | $70.077.630 | 623 | $98.028.559 |
| Valle del Cauca | 15 | $69.615.003 | 682 | $95.020.779 |
| Norte de Santander | 5 | $69.582.410 | 501 | $89.264.261 |
| Amazonas | 4 | $57.626.001 | 915 | $91.397.760 |
| Cundinamarca | 10 | $54.244.318 | 773 | $87.612.893 |

**Hallazgo:** Chocó tiene solo 17 clientes pero $275M en deuda — deuda promedio por cliente de $16M, la más alta del país. Amazonas tiene los días de mora más altos con 915 días  casi 3 años sin pagar. Norte de Santander con solo 5 clientes tiene $69M en capital vencido — perfil de alto riesgo individual.

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

**Resultado:** Sin resultados — 0 clientes en mora sin gestión registrada.

**Hallazgo:** El banco tiene **trazabilidad completa** — el 100% de los clientes en mora han sido contactados al menos una vez. Esto demuestra un proceso de cobranza bien estructurado donde ningún caso se pierde sin seguimiento.

---

### Q8 — Clientes con saldo disponible y mora activa
**Pregunta:** ¿Qué clientes tienen dinero en cuenta pero no han pagado su deuda?

```sql
SELECT c.nombre, c.apellido, ci.nombre_ciudad,
    SUM(pp.saldo_actual) AS saldo_disponible,
    m.capital_vencido, m.capital_vencido + m.interes_mora AS deuda_total,
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
ORDER BY saldo_disponible DESC LIMIT 15;
```

**Casos más críticos:**
| Cliente | Ciudad | Saldo disponible | Deuda total | Días mora | Diferencia |
|---------|--------|------------------|-------------|-----------|------------|
| Zoraida Rovira | Carcasí | $1.335.899.000 | $579.709 | 745 | $1.335.319.291 |
| Nadia Tormo | Cisneros | $1.270.907.000 | $5.633.444 | 379 | $1.265.273.556 |
| Amada Falco | Candelaria | $1.198.102.000 | $6.912.101 | 959 | $1.191.189.899 |
| Calisto Menéndez | Bogotá DC | $1.152.795.000 | $961.198 | 867 | $1.151.833.802 |
| Emiliano Galván | Salgar | $1.141.495.000 | $1.544.847 | 683 | $1.139.950.153 |

**Hallazgo:** Este es el hallazgo más impactante — hay clientes con más de $1.000 millones en cuenta que llevan años sin pagar deudas menores a $7 millones. Zoraida Rovira tiene 745 días de mora con una deuda de solo $579.709 teniendo $1.335 millones disponibles. **Recomendación:** implementar débito automático con autorización previa — estos casos se resuelven sin gestión de cobranza adicional.

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

**Hallazgo:** El Correo es el canal más efectivo con 16.55% de tasa de resolución — y el menos costoso operativamente. La Llamada es el canal más usado (249 gestiones) pero no el más efectivo. La Visita Domiciliaria es la más costosa logísticamente y tiene la menor efectividad (10.25%). **Recomendación:** redirigir recursos de visitas domiciliarias hacia gestión digital por correo electrónico — mismo resultado a menor costo.

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
| Producto | Moras | Días promedio | Días min | Días max | Liquidadas |
|----------|-------|---------------|----------|----------|------------|
| Tarjeta Platinum | 50 | 720 | 317 | 1.079 | 12 |
| Crédito Estudios | 47 | 712 | 105 | 1.079 | 5 |
| Crédito Libre Inversión | 59 | 662 | 75 | 1.079 | 4 |
| Crédito Hipotecario | 10 | 660 | 379 | 1.079 | 0 |
| Tarjeta Oro | 52 | 658 | 228 | 1.048 | 8 |
| Tarjeta Black | 43 | 642 | 105 | 1.020 | 4 |
| Crédito Automotriz | 25 | 635 | 75 | 1.079 | 2 |

**Hallazgo:** El Crédito Hipotecario tiene 0 moras liquidadas — ninguna se ha resuelto y su promedio de días es de 660. La Tarjeta Platinum tiene el mayor promedio de días (720) pero también la mayor cantidad de liquidaciones (12) — es el producto donde más se recupera cartera eventualmente. El Crédito Automotriz tiene solo 2 liquidaciones a pesar de ser el de mayor deuda total.

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

**Casos más críticos:**
| Cliente | Ciudad | Producto | Días mora | Capital vencido | Gestiones |
|---------|--------|----------|-----------|-----------------|-----------|
| Ximena Jurado | Ortega, Tolima | Libre Inversión | 1.079 | $432.816 | 3 |
| Isidora de Crespi | El Guacamayo, Santander | Hipotecario | 1.079 | $4.071.499 | 3 |
| Socorro Sans | Fonseca, La Guajira | Libre Inversión | 1.079 | $1.344.258 | 4 |
| Luis Miguel Gutiérrez | Puerto Nariño, Amazonas | Automotriz | 1.048 | $47.804.746 | 3 |
| Valerio Valentín | Carmen del Darién, Chocó | Automotriz | 959 | $42.994.237 | 3 |

**Hallazgo:** Clientes con más de 1.000 días de mora y 3 o más gestiones sin resultado son candidatos directos a proceso jurídico. Luis Miguel Gutiérrez y Valerio Valentín concentran los montos más altos — $47M y $42M respectivamente — con múltiples gestiones fallidas. **Recomendación:** escalar estos casos a cobro jurídico inmediatamente.

---

### Q12 — KPI ejecutivos de cartera
**Pregunta:** ¿Cuál es el estado global de la cartera del banco?

```sql
SELECT 
    ROUND(SUM(pa.monto_aprobado), 0) AS cartera_total,
    ROUND(SUM(CASE WHEN pa.estado = 'Vigente' THEN pa.monto_aprobado ELSE 0 END), 0) AS cartera_vigente,
    ROUND(SUM(CASE WHEN pa.estado = 'En_Mora' THEN pa.monto_aprobado ELSE 0 END), 0) AS cartera_en_mora,
    ROUND(SUM(CASE WHEN pa.estado = 'Castigada' THEN pa.monto_aprobado ELSE 0 END), 0) AS cartera_castigada,
    ROUND(SUM(CASE WHEN pa.estado = 'Cancelada' THEN pa.monto_aprobado ELSE 0 END), 0) AS cartera_cancelada,
    ROUND(SUM(CASE WHEN pa.estado IN ('En_Mora','Castigada') THEN pa.monto_aprobado ELSE 0 END) * 100.0 / SUM(pa.monto_aprobado), 2) AS tasa_morosidad_exposicion,
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
| Cartera cancelada | $41.250.100.000 |
| Tasa morosidad por exposición | 11.49% |
| Tasa morosidad real | 1.20% |
| Promedio sector Colombia | 3% - 8% |

**Hallazgo:** La tasa de morosidad real del 1.20% — calculada sobre capital vencido real vs cartera vigente — está muy por debajo del promedio del sector financiero colombiano (3-8%). La tasa de exposición del 11.49% indica cuánto del portafolio está comprometido en productos problemáticos — útil para el análisis de riesgo estructural del banco.

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

**Muestra de resultados:**
| Cliente | Ciudad | Usuario | Intentos fallidos | Estado |
|---------|--------|---------|-------------------|--------|
| Carmelita Tejedor | Cúcuta, Norte de Santander | user_1156 | 5 | Bloqueado |
| Mónica Colom | Aratoca, Santander | user_1282 | 5 | Suspendido |
| Pía Huertas | Majagual, Sucre | user_1875 | 5 | Bloqueado |
| Clemente Nevado | Gachantivá, Boyacá | user_1941 | 5 | Bloqueado |
| Luis Miguel Cuadrado | Floridablanca, Santander | user_2129 | 5 | Bloqueado |

**Hallazgo:** Todos los usuarios con intentos fallidos tienen estado Bloqueado o Suspendido — el sistema de seguridad funciona correctamente bloqueando accesos tras múltiples intentos fallidos. **Recomendación:** implementar notificación automática por SMS o correo al cliente cuando su cuenta sea bloqueada para facilitar el proceso de recuperación de acceso.

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

**Resultado:**
| Canal | Transacciones | Dinero total | Monto promedio | % del total |
|-------|---------------|--------------|----------------|-------------|
| App Móvil | 182.700 | $1.816.076.745.816 | $9.940.212 | 43.54% |
| Web | 102.702 | $1.029.236.047.478 | $10.021.577 | 24.47% |
| Cajero Automático | 63.917 | $625.658.271.891 | $9.788.605 | 15.23% |
| Corresponsal Bancario | 49.231 | $488.258.487.610 | $9.917.704 | 11.73% |
| Oficina | 21.073 | $209.582.950.938 | $9.945.568 | 5.02% |

**Hallazgo:** La App Móvil concentra el 43.54% de las transacciones — confirma que el banco es verdaderamente digital. Los canales digitales (App + Web) representan el 68% del total de transacciones. El monto promedio es similar en todos los canales (~$9.9M) lo que indica que el comportamiento de transacción no varía por canal. El Corresponsal Bancario es crítico en departamentos de baja penetración digital — representa $488M en movimientos.



---

## 📌 Resumen de Hallazgos y Recomendaciones

| # | Hallazgo | Recomendación |
|---|----------|---------------|
| 1 | Depósitos superan cartera — liquidez positiva | Mantener política de crédito conservadora |
| 2 | Crédito Automotriz genera el 79% de ingresos mensuales | Fortalecer análisis de crédito — es el producto más rentable y más riesgoso |
| 3 | Tasa de morosidad real 1.20% — por debajo del sector | Mantener criterios de originación actuales |
| 4 | Correo es el canal más efectivo de cobranza (16.55%) | Redirigir recursos de visitas domiciliarias a gestión digital |
| 5 | Clientes con saldo > $1.000M y mora sin pagar | Implementar débito automático con autorización previa |
| 6 | 100% de moras tienen gestión registrada | Trazabilidad completa — proceso bien estructurado |
| 7 | Hipotecario: 0 moras liquidadas | Revisar estrategia de cobranza para este producto |
| 8 | Chocó y Amazonas: mayor deuda per cápita | Ajustar política de originación en estas regiones |
| 9 | App Móvil: 43.54% de transacciones | Invertir en mejoras de la app como canal principal |
| 10 | Usuarios bloqueados notificados automáticamente | Implementar flujo de desbloqueo digital sin llamar a la línea |