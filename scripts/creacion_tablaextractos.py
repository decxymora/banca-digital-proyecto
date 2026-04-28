import pandas as pd
import random
random.seed(42)
from datetime import date, timedelta

# Cargamos las tablas que necesitamos
producto_activo = pd.read_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_PRODUCTO_ACTIVO.csv')
clientes = pd.read_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_CLIENTES.csv')
ciudades = pd.read_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_CIUDADES_limpio.csv')

# Calcular edad de cada cliente
hoy = date(2025, 12, 31)
clientes['fecha_nacimiento'] = pd.to_datetime(clientes['fecha_nacimiento'])
clientes['edad'] = ((hoy - clientes['fecha_nacimiento'].dt.date).apply(lambda x: x.days) / 365.25).astype(int)

# Departamentos pobres — mayor probabilidad de mora en extractos
# Chocó (27), Vichada (99), Guainía (94), Vaupés (97), La Guajira (44)
deptos_pobres = [27, 99, 94, 97, 44]

# IDs de tarjetas de crédito — mayor probabilidad de mora que créditos
IDS_TARJETAS = [9, 10, 11]

# Ver cuántos productos activos tenemos
print("Total productos activos:", len(producto_activo))
print("Estados:", producto_activo['estado'].value_counts().to_dict())

# Unir producto_activo con clientes para tener edad y departamento
producto_activo = producto_activo.merge(
    clientes[['id_cliente', 'edad']],
    on='id_cliente',
    how='left'
)
producto_activo = producto_activo.merge(
    clientes[['id_cliente', 'id_ciudad']],
    on='id_cliente',
    how='left'
)
producto_activo = producto_activo.merge(
    ciudades[['id_ciudad', 'id_departamento']],
    on='id_ciudad',
    how='left'
)

extracto_rows = []
id_extracto  = 1
num_extracto = 200000

for _, prod in producto_activo.iterrows():

    fecha_inicio = pd.to_datetime(prod['fecha_inicio']).date()
    estado_prod  = prod['estado']
    id_pb        = prod['id_producto_banco']
    edad         = prod['edad']
    id_depto     = prod['id_departamento']
    es_tarjeta   = id_pb in IDS_TARJETAS

    # Fecha de cancelacion para productos cancelados
    if estado_prod == 'Cancelada' and pd.notna(prod['fecha_vencimiento']):
        fecha_fin = pd.to_datetime(prod['fecha_vencimiento']).date()
    else:
        fecha_fin = hoy

    # Iniciar en el primer mes del producto
    fecha_mes = fecha_inicio.replace(day=1)

    # Saldo acumulado para el efecto cascada
    saldo_acumulado = 0

    # CICLO: un extracto por mes desde inicio hasta fecha fin
    while fecha_mes <= fecha_fin:

        fecha_corte  = fecha_mes.replace(day=min(28, fecha_mes.day))
        fecha_limite = fecha_corte + timedelta(days=15)

        # Calcular saldo base del mes
        if es_tarjeta:
            # Tarjeta: saldo varía cada mes según el uso
            saldo_mes = round(
                random.uniform(100_000, prod['monto_aprobado'] * 0.8) / 1_000
            ) * 1_000
        else:
            # Crédito: cuota fija todos los meses
            saldo_mes = prod['valor_cuota_fija'] if pd.notna(prod['valor_cuota_fija']) else 0

        # Efecto cascada: si hay saldo acumulado de mora anterior se suma
        saldo_capital = round(saldo_mes + saldo_acumulado, 0)

        # Intereses del mes
        intereses = round(saldo_capital * prod['tasa_interes_mensual'] / 100, 0)

        # Cuota de manejo
        if es_tarjeta:
            cuota_manejo_e = random.choice([15_000, 18_000, 22_000])
        else:
            cuota_manejo_e = 0

        pago_total = round(saldo_capital + intereses + cuota_manejo_e, 0)
        pago_minimo = round(pago_total * random.uniform(0.05, 0.15), 0) if es_tarjeta else None

        # Definir probabilidades de estado de pago según reglas de negocio
        if estado_prod == 'Vigente':
            # Hipoteca tiene prioridad de pago — menos mora
            if id_pb == 6:
                pesos = [95, 5, 0, 0]
            else:
                pesos = [90, 10, 0, 0]

        elif estado_prod == 'En_Mora':
            pesos = [10, 30, 60, 40]  # Mora, Parcial, Pendiente base

            # Jóvenes menores de 25 tienen más mora
            if edad <= 25:
                pesos = [5, 20, 75, 0]

            # Departamentos pobres tienen más mora
            if id_depto in deptos_pobres:
                pesos[2] += 10
                pesos[0] -= 10

            # Tarjetas tienen más mora que créditos
            if es_tarjeta:
                pesos[2] += 5
                pesos[0] -= 5

        elif estado_prod == 'Cancelada':
            pesos = [100, 0, 0, 0]  # 100% Pagado

        else:  # Castigada
            pesos = [0, 0, 0, 100]  # 100% Mora

        estados_pago = ['Pagado', 'Pendiente', 'Parcial', 'Mora']
        estado_pago  = random.choices(estados_pago, weights=pesos)[0]

        # Efecto cascada: si no pagó se acumula el saldo para el próximo mes
        if estado_pago == 'Mora':
            # El saldo impago se acumula con interés de mora
            saldo_acumulado = round(
                saldo_capital * (1 + prod['tasa_interes_mora'] / 100), 0
            )
        elif estado_pago == 'Parcial':
            # Pagó una parte — se acumula solo la mitad
            saldo_acumulado = round(saldo_capital * 0.5, 0)
        else:
            # Pagó todo — se reinicia el saldo acumulado
            saldo_acumulado = 0

        extracto_rows.append({
            'id_extracto':             id_extracto,
            'id_producto_activo':      prod['id_producto_activo'],
            'numero_extracto':         f"EXT-{num_extracto}",
            'fecha_corte':             fecha_corte.strftime('%Y-%m-%d'),
            'fecha_limite_pago':       fecha_limite.strftime('%Y-%m-%d'),
            'saldo_capital_pendiente': saldo_capital,
            'intereses_mes':           intereses,
            'cuota_manejo':            cuota_manejo_e,
            'pago_total_mes':          pago_total,
            'pago_minimo':             pago_minimo,
            'estado_pago':             estado_pago
        })

        id_extracto  += 1
        num_extracto += 1

        # Avanzar al siguiente mes
        if fecha_mes.month == 12:
            fecha_mes = fecha_mes.replace(year=fecha_mes.year + 1, month=1)
        else:
            fecha_mes = fecha_mes.replace(month=fecha_mes.month + 1)

extracto = pd.DataFrame(extracto_rows)

# Verificar resultados
print("Total extractos generados:", len(extracto))
print("Estado pago:", extracto['estado_pago'].value_counts().to_dict())
print("Saldos negativos:", (extracto['pago_total_mes'] < 0).sum())

# Guardar el archivo
extracto.to_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_EXTRACTO.csv', index=False)

print("Archivo guardado correctamente")