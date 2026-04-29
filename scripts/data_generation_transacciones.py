import pandas as pd
import random
random.seed(42)
from datetime import date, timedelta, datetime

# Cargamos las tablas que necesitamos
clientes        = pd.read_csv(r'./datos_limpios\bd_CLIENTES.csv')
producto_activo = pd.read_csv(r'./datos_limpios\bd_PRODUCTO_ACTIVO.csv')
producto_pasivo = pd.read_csv(r'./datos_limpios\bd_PRODUCTO_PASIVO.csv')
tipo_trans      = pd.read_csv(r'./datos_limpios\bd_TIPO_TRANSACCION.csv')
extracto        = pd.read_csv(r'./datos_limpios\bd_EXTRACTO.csv')
ciudades        = pd.read_csv(r'./datos_limpios\bd_CIUDADES_limpio.csv')

hoy = date(2025, 12, 31)

# Calcular edad de cada cliente
clientes['fecha_nacimiento'] = pd.to_datetime(clientes['fecha_nacimiento'])
clientes['edad'] = ((hoy - clientes['fecha_nacimiento'].dt.date).apply(lambda x: x.days) / 365.25).astype(int)

# Departamentos grandes — más transacciones y montos más altos
# Antioquia (5), Bogotá (11), Valle del Cauca (76), Santander (68)
deptos_grandes = [5, 11, 76, 68]

# Departamentos pobres — más retiros en corresponsal, menos App
# Chocó (27), Vichada (99), Guainía (94), Vaupés (97), La Guajira (44)
deptos_pobres = [27, 99, 94, 97, 44]

# Ver cuántos clientes tenemos por estado
print("Clientes por estado:", clientes['estado'].value_counts().to_dict())
print("Total productos pasivos:", len(producto_pasivo))
print("Total productos activos:", len(producto_activo))
print("Tipos de transaccion:", tipo_trans[['id_tipo_transaccion','nombre_tipo','naturaleza']].to_string())

# Descripciones por tipo de transaccion
descripciones = {
    1:  ['Transferencia a familiar', 'Pago arriendo', 'Pago proveedor', 'Envío dinero'],
    2:  ['Transferencia cuenta propia', 'Traslado entre cuentas', 'Pago interno'],
    3:  ['Transfiya familiar', 'Transfiya pago servicio', 'Transfiya emergencia'],
    4:  ['Pago EPM', 'Pago ETB', 'Pago Claro', 'Pago Movistar', 'Pago Gas Natural', 'Pago Acueducto'],
    5:  ['Retiro Corresponsal Efecty', 'Retiro Corresponsal Supergiros', 'Retiro Corresponsal Bancolombia'],
    6:  ['Retiro Cajero ATH', 'Retiro Cajero Bancolombia', 'Retiro Cajero Davivienda'],
    7:  ['Cobro GMF 4x1000'],
    8:  ['Compra Supermercado Éxito', 'Compra Rappi', 'Pago Netflix', 'Compra Falabella',
         'Compra Homecenter', 'Compra Decathlon', 'Compra H&M', 'Pago Spotify'],
    9:  ['Avance Tarjeta Oro', 'Avance Tarjeta Platinum', 'Avance Tarjeta Black'],
    10: ['Abono Nómina empresa', 'Pago honorarios', 'Comisiones ventas', 'Pago freelance'],
    11: ['Transferencia recibida familiar', 'Pago recibido cliente', 'Transferencia recibida ACH'],
    12: ['Consignación efectivo ventanilla', 'Depósito cheque', 'Consignación empresarial'],
    13: ['Pago cuota crédito', 'Pago mínimo tarjeta', 'Abono extraordinario'],
    14: ['Ahorro meta viaje', 'Ahorro emergencias', 'Ahorro educación', 'Bolsillo navidad']
}

# Canales con distribución realista
# Departamentos pobres usan más corresponsal y menos App
canales_normales = ['App Móvil', 'Web', 'Cajero Automático', 'Corresponsal Bancario', 'Oficina']
pesos_normales   = [45, 25, 15, 10, 5]
canales_pobres   = ['App Móvil', 'Web', 'Cajero Automático', 'Corresponsal Bancario', 'Oficina']
pesos_pobres     = [20, 15, 20, 40, 5]

# Índices rápidos
mapa_pasivos  = producto_pasivo.groupby('id_cliente')['id_producto_pasivo'].apply(list).to_dict()
mapa_activos  = producto_activo.groupby('id_cliente')['id_producto_activo'].apply(list).to_dict()
mapa_saldo    = producto_pasivo.set_index('id_producto_pasivo')['saldo_actual'].to_dict()
mapa_cupo     = producto_activo.set_index('id_producto_activo')['cupo_disponible'].to_dict()
mapa_cuota    = producto_activo.set_index('id_producto_activo')['valor_cuota_fija'].to_dict()
mapa_apertura = producto_pasivo.set_index('id_producto_pasivo')['fecha_apertura'].to_dict()

# Unir clientes con ciudades para obtener departamento
clientes = clientes.merge(ciudades[['id_ciudad', 'id_departamento']], on='id_ciudad', how='left')

# Extractos pagados para referenciar en pagos de obligacion
ext_pagados = extracto[extracto['estado_pago'].isin(['Pagado', 'Parcial'])][
    ['id_extracto', 'id_producto_activo', 'pago_total_mes', 'pago_minimo']
].copy()
ext_por_prod = ext_pagados.groupby('id_producto_activo').apply(
    lambda x: x.to_dict('records')
).to_dict()

print("Índices creados correctamente")
print("Clientes con productos pasivos:", len(mapa_pasivos))
print("Clientes con productos activos:", len(mapa_activos))

trans_rows = []
id_trans   = 100001
TOTAL      = 400_000

# Separar clientes por estado
clientes_activos   = clientes[clientes['estado'] == 'Activo']
clientes_inactivos = clientes[clientes['estado'] == 'Inactivo']

# Distribución de transacciones
# Activos reciben la mayoría — inactivos solo 2 cada uno
trans_inactivos = len(clientes_inactivos) * 2
trans_activos   = TOTAL - trans_inactivos
trans_por_activo = trans_activos // len(clientes_activos)
sobrante         = trans_activos % len(clientes_activos)

print(f"Transacciones para activos: {trans_activos}")
print(f"Transacciones para inactivos: {trans_inactivos}")
print(f"Promedio por cliente activo: {trans_por_activo}")

# Meses con más transacciones por temporada o nómina
def get_peso_mes(mes):
    if mes == 12:
        return 1.20   # Diciembre — temporada navideña
    elif mes == 1:
        return 0.90   # Enero — menos movimiento
    else:
        return 1.00

def fecha_aleatoria(fecha_apertura_str):
    fecha_apertura = pd.to_datetime(fecha_apertura_str).date()
    inicio         = max(fecha_apertura, date(2024, 1, 1))
    dias_disponibles = (hoy - inicio).days
    if dias_disponibles <= 0:
        return hoy
    # Quincenas tienen más probabilidad
    dia_random = random.randint(0, dias_disponibles)
    fecha      = inicio + timedelta(days=dia_random)
    # Si cae cerca del 15 o 30 hay más probabilidad de transaccion
    if random.random() < 0.15:
        fecha = fecha.replace(day=random.choice([15, min(30, 28)]))
    hora   = random.randint(6, 22)
    minuto = random.randint(0, 59)
    return datetime(fecha.year, fecha.month, fecha.day, hora, minuto)

def generar_transaccion(id_cli, id_depto, edad, n_trans):
    pasivos = mapa_pasivos.get(id_cli, [])
    activos = mapa_activos.get(id_cli, [])
    if not pasivos:
        return []

    trans_cliente = []
    for _ in range(n_trans):
        id_prod_pas = None
        id_prod_act = None
        id_ext      = None
        id_tipo     = None
        monto       = 0
        descripcion = ''

        # Elegir tipo de transaccion según naturaleza
        tipo_grupo = random.choices(
            ['salida', 'entrada', 'neutro'],
            weights=[55, 40, 5]
        )[0]

        if tipo_grupo == 'salida':
            id_prod_pas = random.choice(pasivos)
            saldo       = mapa_saldo.get(id_prod_pas, 0)
            id_tipo     = random.choices(
                [1, 2, 3, 4, 5, 6, 7, 8, 13],
                weights=[10, 8, 8, 15, 10, 12, 5, 20, 12]
            )[0]

            if id_tipo == 1:
                monto = round(random.uniform(50_000, min(50_000_000, saldo)) / 1_000) * 1_000
            elif id_tipo == 2:
                monto = round(random.uniform(50_000, min(20_000_000, saldo)) / 1_000) * 1_000
            elif id_tipo == 3:
                monto = round(random.uniform(10_000, min(3_000_000, saldo)) / 1_000) * 1_000
            elif id_tipo == 4:
                monto = round(random.uniform(50_000, 500_000) / 1_000) * 1_000
            elif id_tipo == 5:
                monto = round(random.uniform(10_000, min(2_000_000, saldo)) / 1_000) * 1_000
            elif id_tipo == 6:
                monto = round(random.uniform(100_000, min(2_000_000, saldo)) / 1_000) * 1_000
            elif id_tipo == 7:
                monto = round(random.uniform(5_000, 50_000) / 1_000) * 1_000
            elif id_tipo == 8:
                # Compra tarjeta debito — jóvenes compran más entretenimiento
                if edad <= 30:
                    descripcion = random.choice(['Compra Rappi', 'Pago Netflix', 'Pago Spotify', 'Compra H&M'])
                else:
                    descripcion = random.choice(['Compra Supermercado Éxito', 'Compra Homecenter', 'Compra Falabella', 'Compra Decathlon'])
                monto = round(random.uniform(10_000, min(5_000_000, saldo)) / 1_000) * 1_000
            elif id_tipo == 13:
                # Pago obligacion — referenciar extracto
                if activos:
                    id_prod_act = random.choice(activos)
                    registros   = ext_por_prod.get(id_prod_act, [])
                    if registros:
                        ext_sel = random.choice(registros)
                        id_ext  = ext_sel['id_extracto']
                        pago_min = ext_sel.get('pago_minimo')
                        cuota    = mapa_cuota.get(id_prod_act)
                        if pago_min and not pd.isna(pago_min):
                            monto = round(float(pago_min), 0)
                        elif cuota and not pd.isna(cuota):
                            monto = round(float(cuota), 0)
                        else:
                            monto = round(random.uniform(100_000, 2_000_000) / 1_000) * 1_000

        elif tipo_grupo == 'entrada':
            id_prod_pas = random.choice(pasivos)
            id_tipo     = random.choices(
                [9, 10, 11, 12],
                weights=[15, 35, 30, 20]
            )[0]

            if id_tipo == 9:
                # Avance tarjeta credito — no supera cupo disponible
                if activos:
                    id_prod_act = random.choice(activos)
                    cupo        = mapa_cupo.get(id_prod_act)
                    if cupo and not pd.isna(cupo) and cupo > 0:
                        monto = round(random.uniform(100_000, float(cupo)) / 1_000) * 1_000
                    else:
                        monto = round(random.uniform(100_000, 1_000_000) / 1_000) * 1_000
            elif id_tipo == 10:
                # Nómina — adultos tienen salarios más altos
                if edad >= 40:
                    monto = round(random.uniform(5_000_000, 15_000_000) / 1_000) * 1_000
                else:
                    monto = round(random.uniform(1_000_000, 8_000_000) / 1_000) * 1_000
            elif id_tipo == 11:
                monto = round(random.uniform(50_000, 50_000_000) / 1_000) * 1_000
            elif id_tipo == 12:
                monto = round(random.uniform(100_000, 100_000_000) / 1_000) * 1_000

        else:
            # Neutro — bolsillo ahorro
            id_prod_pas = random.choice(pasivos)
            id_tipo     = 14
            monto       = round(random.uniform(50_000, 2_000_000) / 1_000) * 1_000

        # Garantizar monto positivo
        if monto <= 0:
            monto = 10_000

        # Descripcion si no fue asignada
        if not descripcion:
            descripcion = random.choice(descripciones.get(id_tipo, ['Transacción bancaria']))

        # Fecha de transaccion
        if id_prod_pas and id_prod_pas in mapa_apertura:
            fecha_trans = fecha_aleatoria(mapa_apertura[id_prod_pas])
        else:
            fecha_trans = datetime(2024, random.randint(1,12), random.randint(1,28),
                                   random.randint(6,22), random.randint(0,59))

        # Canal según departamento
        if id_depto in deptos_pobres:
            canal = random.choices(canales_pobres, weights=pesos_pobres)[0]
        else:
            canal = random.choices(canales_normales, weights=pesos_normales)[0]

        ip = f"192.168.{random.randint(1,254)}.{random.randint(1,254)}"

        trans_cliente.append({
            'id_transaccion':      None,
            'id_producto_pasivo':  id_prod_pas,
            'id_producto_activo':  id_prod_act,
            'id_tipo_transaccion': id_tipo,
            'id_extracto':         id_ext,
            'monto':               monto,
            'descripcion':         descripcion,
            'fecha_transaccion':   fecha_trans.strftime('%Y-%m-%d %H:%M:%S'),
            'canal':               canal,
            'ip_origen':           ip
        })
    return trans_cliente

# Generar transacciones para clientes activos
print("Generando transacciones para clientes activos...")
ids_activos = clientes_activos['id_cliente'].tolist()
random.shuffle(ids_activos)

for i, id_cli in enumerate(ids_activos):
    fila    = clientes_activos[clientes_activos['id_cliente'] == id_cli].iloc[0]
    id_depto = fila['id_departamento']
    edad     = fila['edad']
    n_trans  = trans_por_activo + (1 if i < sobrante else 0)

    # Departamentos grandes tienen más transacciones
    if id_depto in deptos_grandes:
        n_trans = int(n_trans * 1.2)

    trans_rows.extend(generar_transaccion(id_cli, id_depto, edad, n_trans))

# Generar transacciones para clientes inactivos
print("Generando transacciones para clientes inactivos...")
for _, fila in clientes_inactivos.iterrows():
    id_cli   = fila['id_cliente']
    id_depto = fila['id_departamento']
    edad     = fila['edad']
    trans_rows.extend(generar_transaccion(id_cli, id_depto, edad, 2))

# Convertir a tabla y asignar IDs
transacciones = pd.DataFrame(trans_rows)
transacciones['id_transaccion'] = range(100001, 100001 + len(transacciones))

# Verificar resultados
print(f"Total transacciones generadas: {len(transacciones)}")
print(f"Montos negativos o cero: {(transacciones['monto'] <= 0).sum()}")
print(f"Monto promedio: ${transacciones['monto'].mean():,.0f}")
print(f"Canal más usado: {transacciones['canal'].value_counts().index[0]}")
print(f"Tipo transaccion más frecuente: {transacciones['id_tipo_transaccion'].value_counts().index[0]}")

# Guardar el archivo
transacciones.to_csv(r'./datos_limpios\bd_TRANSACCIONES.csv', index=False)

print("Archivo guardado correctamente")