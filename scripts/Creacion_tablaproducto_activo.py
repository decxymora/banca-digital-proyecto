import pandas as pd
import numpy as np
import random
import string
from datetime import date, timedelta
random.seed(42)
np.random.seed(42)

# Cargar las tablas que necesitamos
clientes = pd.read_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_CLIENTES.csv')
productos_banco = pd.read_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_PRODUCTOS_BANCO.csv')
ciudades = pd.read_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_CIUDADES_limpio.csv')

# Calcular la edad de cada cliente
# HOY = (31 DE DICIEMBRE DE 2025 POR QUE ES CIERRE DE AÑO)

hoy = date(2025, 12, 31)
clientes['fecha_nacimiento'] = pd.to_datetime(clientes['fecha_nacimiento'])
clientes['edad'] = ((hoy - clientes['fecha_nacimiento'].dt.date).apply(lambda x: x.days) / 365.25).astype(int)

# Ver distribución de edades
print("Distribución de edades:")
print(clientes['edad'].describe())

# Ver cuántos clientes hay por tipo de documento
print("\nClientes por tipo de documento:")
print(clientes['tipo_documento'].value_counts())

# Ver productos activos disponibles
prod_activos = productos_banco[productos_banco['tipo_producto'] == 'Activo']
print("\nProductos activos disponibles:")
print(prod_activos)

# Definir los que clientes pueden tener productos activos
# Solo clientes Activos pueden tener productos activos
clientes_activos = clientes[clientes['estado'] == 'Activo'].copy()

# Departamentos con más productos (ciudades grandes) Logica de negocio
# Los clientes de estos departamentos tienen más acceso a productos activos

deptos_grandes = [5, 11, 76, 68]  # Antioquia, Bogotá, Vall del Cauca, Santander

# Departamentos pobres con más mora
deptos_pobres = [27, 99, 94, 97, 44]  # Chocó, Vichada, Guainía, Vaupés, La Guajira

# IDs de productos por categoría
ID_LIBRE_INVERSION = 5
ID_HIPOTECARIO     = 6
ID_AUTOMOTRIZ      = 7
ID_ESTUDIOS        = 8
ID_TC_ORO          = 9
ID_TC_PLATINUM     = 10
ID_TC_BLACK        = 11
# ID 12 Empresarial no se asigna a nadie (solo hay clientes naturales)

# Verificar cuántos clientes activos tenemos
print("Clientes activos disponibles:", len(clientes_activos))
print("Clientes sin productos activos (inactivos + bloqueados):", len(clientes) - len(clientes_activos))

# Lista donde guardaremos todos los productos activos generados
prod_act_rows = []
id_producto_activo = 10000
INICIO = date(2023, 1, 1)

# Función para generar número de contrato aleatorio con letras y números
def generar_contrato():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=6))
    return f"{letras}-{numeros}"

# Recorremos solo los clientes activos
for _, cliente in clientes_activos.iterrows():

    edad        = cliente['edad']
    id_cli      = cliente['id_cliente']
    id_ciudad   = cliente['id_ciudad']

    # Obtener el departamento del cliente para aplicar intencionalidad
    id_depto = ciudades[ciudades['id_ciudad'] == id_ciudad]['id_departamento'].values
    id_depto = id_depto[0] if len(id_depto) > 0 else 0

    # Clientes en departamentos grandes tienen más productos
    if id_depto in deptos_grandes:
        n_productos = random.randint(2, 5)
    else:
        n_productos = random.randint(1, 3)

    # Definir qué productos puede tener según la edad
    productos_disponibles = []

    # Entre 20 y 27 años: solo tarjeta Oro con montos bajos
    if 20 <= edad <= 27:
        productos_disponibles = [ID_TC_ORO]
        n_productos = 1

    # Entre 28 y 35 años: tarjetas y créditos de libre inversión y estudios
    elif 28 <= edad <= 35:
        productos_disponibles = [
            ID_TC_ORO, ID_TC_PLATINUM, ID_TC_BLACK,
            ID_LIBRE_INVERSION, ID_ESTUDIOS
        ]

    # Mayores de 35: todos los productos incluida hipoteca desde los 37
    elif edad > 35:
        productos_disponibles = [
            ID_TC_ORO, ID_TC_PLATINUM, ID_TC_BLACK,
            ID_LIBRE_INVERSION, ID_ESTUDIOS, ID_AUTOMOTRIZ
        ]
        if edad >= 37:
            productos_disponibles.append(ID_HIPOTECARIO)

    if not productos_disponibles:
        continue

    # Seleccionar productos sin repetir
    random.shuffle(productos_disponibles)
    seleccionados      = []
    tiene_hipotecario  = False
    tiene_tarjetas     = 0

    for id_pb in productos_disponibles:
        if len(seleccionados) >= n_productos:
            break
        if id_pb == ID_HIPOTECARIO:
            # Solo el 18% de clientes elegibles tendrá hipoteca
            if tiene_hipotecario or random.random() > 0.18:
                continue
            tiene_hipotecario = True
        if id_pb in [ID_TC_ORO, ID_TC_PLATINUM, ID_TC_BLACK]:
            if tiene_tarjetas >= 2:
                continue
            tiene_tarjetas += 1
        seleccionados.append(id_pb)

    # Generar datos de cada producto seleccionado
    for id_pb in seleccionados:

        # Fecha inicio aleatoria entre 2023 y 2024
        dias_inicio  = random.randint(0, 730)
        fecha_inicio = INICIO + timedelta(days=dias_inicio)

        # Montos según tipo de producto y edad
        if id_pb == ID_TC_ORO and edad <= 27:
            monto = round(random.uniform(800000, 3000000) / 100000) * 100000
        elif id_pb == ID_TC_ORO:
            monto = round(random.uniform(2000000, 8000000) / 100000) * 100000
        elif id_pb == ID_TC_PLATINUM:
            monto = round(random.uniform(5000000, 15000000) / 100000) * 100000
        elif id_pb == ID_TC_BLACK:
            monto = round(random.uniform(10000000, 30000000) / 100000) * 100000
        elif id_pb == ID_LIBRE_INVERSION:
            monto = round(random.uniform(3000000, 80000000) / 100000) * 100000
        elif id_pb == ID_HIPOTECARIO:
            monto = round(random.uniform(50000000, 500000000) / 100000) * 100000
        elif id_pb == ID_AUTOMOTRIZ:
            monto = round(random.uniform(15000000, 120000000) / 10000) * 100000
        elif id_pb == ID_ESTUDIOS:
            monto = round(random.uniform(2000000, 40000000) / 100000) * 100000
        else:
            monto = round(random.uniform(1000000, 10000000) / 100000) * 100000   

        # Tasas legales Colombia — a mayor monto menor tasa
        if id_pb in [ID_TC_ORO, ID_TC_PLATINUM, ID_TC_BLACK]:
            # Tarjetas: entre 1.8% y 2.8% mensual
            factor = 1 - (monto / 30_000_000) * 0.3
            tasa_mensual = round(random.uniform(1.8, 2.8) * max(0.7, factor), 2)
            tasa_mora    = round(tasa_mensual * random.uniform(1.2, 1.4), 2)
        elif id_pb == ID_HIPOTECARIO:
            # Hipotecario: entre 0.9% y 1.4% mensual
            tasa_mensual = round(random.uniform(0.9, 1.5), 2)
            tasa_mora    = round(tasa_mensual * random.uniform(1.2, 1.3), 2)
        elif id_pb == ID_LIBRE_INVERSION:
            # Libre inversión: entre 1.6% y 2.5% mensual
            factor = 1 - (monto / 80_000_000) * 0.3
            tasa_mensual = round(random.uniform(1.6, 2.5) * max(0.7, factor), 2)
            tasa_mora    = round(tasa_mensual * random.uniform(1.2, 1.4), 2)
        else:
            tasa_mensual = round(random.uniform(1.0, 2.0), 2)
            tasa_mora    = round(tasa_mensual * random.uniform(1.2, 1.3), 2)

        # Campos específicos para créditos vs tarjetas
        es_tarjeta = id_pb in [ID_TC_ORO, ID_TC_PLATINUM, ID_TC_BLACK]

        if es_tarjeta:
            numero_cuotas   = None
            valor_cuota     = None
            fecha_venc      = None
            cupo_disponible = round(monto * random.uniform(0.3, 1.0) / 100000) * 100000
            dia_corte       = random.choice([2, 15])
        else:
            # Cuotas según tipo de crédito
            if id_pb == ID_HIPOTECARIO:
                numero_cuotas = random.choice(range(84, 241, 12))
            elif id_pb == ID_LIBRE_INVERSION:
                numero_cuotas = random.choice(range(48, 91, 6))
            elif id_pb == ID_AUTOMOTRIZ:
                numero_cuotas = random.choice(range(24, 73, 12))
            else:
                numero_cuotas = random.choice(range(12, 49, 6))

            # Fórmula de amortización bancaria real
            i = tasa_mensual / 100
            valor_cuota = round(
                monto * (i * (1 + i)**numero_cuotas) / ((1 + i)**numero_cuotas - 1), 0
            )

            fecha_venc      = fecha_inicio + timedelta(days=numero_cuotas * 30)
            cupo_disponible = None
            dia_corte       = None

        # Estado coherente con fecha y edad del cliente
        # Mora concentrada en jóvenes y departamentos pobres
        prob_mora = 0.12
        if edad <= 25:
            prob_mora = 0.30
        if id_depto in deptos_pobres:
            prob_mora += 0.15

        if not es_tarjeta and fecha_venc and fecha_venc < hoy:
            estado = random.choices(['Cancelada', 'Castigada'], weights=[85, 15])[0]
        else:
            estado = random.choices(
                ['Vigente', 'En_Mora', 'Cancelada', 'Castigada'],
                weights=[
                    1 - prob_mora - 0.15 - 0.03,
                    prob_mora,
                    0.15,
                    0.03
                ]
            )[0]

        prod_act_rows.append({
            'id_producto_activo':   id_producto_activo,
            'id_producto_banco':    id_pb,
            'id_cliente':           id_cli,
            'numero_contrato':      generar_contrato(),
            'monto_aprobado':       monto,
            'tasa_interes_mensual': tasa_mensual,
            'tasa_interes_mora':    tasa_mora,
            'fecha_inicio':         fecha_inicio.strftime('%Y-%m-%d'),
            'fecha_vencimiento':    fecha_venc.strftime('%Y-%m-%d') if fecha_venc else None,
            'estado':               estado,
            'numero_cuotas':        numero_cuotas,
            'valor_cuota_fija':     valor_cuota,
            'cupo_disponible':      cupo_disponible,
            'dia_corte':            dia_corte
        })
        id_producto_activo += 1

# Convertir a tabla
producto_activo = pd.DataFrame(prod_act_rows)

# Verificar resultados
print("Total productos activos generados:", len(producto_activo))
print("Máximo productos por cliente:", producto_activo.groupby('id_cliente').size().max())
print("Promedio productos por cliente:", producto_activo.groupby('id_cliente').size().mean().round(1))
print("Estados:", producto_activo['estado'].value_counts().to_dict())
print("Tasas máximas:", producto_activo['tasa_interes_mensual'].max())
print("Vencimiento antes del inicio:", (pd.to_datetime(producto_activo['fecha_vencimiento'], errors='coerce') < pd.to_datetime(producto_activo['fecha_inicio'])).sum())

# Guardar el archivo
producto_activo.to_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_PRODUCTO_ACTIVO.csv', index=False)

print("Archivo guardado correctamente")