import pandas as pd
import random
random.seed(42)

# Cargamos las tablas que necesitamos
clientes = pd.read_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_CLIENTES.csv')
productos_banco = pd.read_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_PRODUCTOS_BANCO.csv')
ciudades = pd.read_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_CIUDADES_limpio.csv')

# Calcular edad de cada cliente
from datetime import date
hoy = date(2025, 12, 31) ##fecha de cierre contable para los calculos
clientes['fecha_nacimiento'] = pd.to_datetime(clientes['fecha_nacimiento'])
clientes['edad'] = ((hoy - clientes['fecha_nacimiento'].dt.date).apply(lambda x: x.days) / 365.25).astype(int)

# Departamentos grandes — clientes con saldos más altos
# Antioquia (5), Bogotá (11), Valle del Cauca (76), Santander (68)
deptos_grandes = [5, 11, 76, 68]

# Departamentos pobres — clientes con saldos más bajos
# Chocó (27), Vichada (99), Guainía (94), Vaupés (97), La Guajira (44)
# Son los departamentos con menor desarrollo econmico de Colombia
deptos_pobres = [27, 99, 94, 97, 44]

# IDs de productos pasivos según el catálogo del banco
# Regla: solo se asignan productos pasivos — no activos
ID_AHORROS          = 1  # Cuenta de Ahorros 
ID_CUENTA_CORRIENTE = 3  # Cuenta Corriente — saldos más altos
ID_CUENTA_DIGITAL   = 4  # Cuenta Digital — sin cuota de manejo, saldos bajos

# Solo productos pasivos del catálogo
prod_pasivos = productos_banco[productos_banco['tipo_producto'] == 'Pasivo']
print("Productos pasivos disponibles:")
print(prod_pasivos)

# Ver cuántos clientes tenemos
print("\nTotal clientes:", len(clientes))
print(clientes['estado'].value_counts())

from datetime import timedelta

prod_pas_rows = []
id_producto_pasivo = 20000
num_cuenta = 4093550000000000

for _, cliente in clientes.iterrows():

    edad      = cliente['edad']
    id_cli    = cliente['id_cliente']
    id_ciudad = cliente['id_ciudad']
    estado    = cliente['estado']

    # Obtener el departamento del cliente
    id_depto = ciudades[ciudades['id_ciudad'] == id_ciudad]['id_departamento'].values
    id_depto = id_depto[0] if len(id_depto) > 0 else 0

    # Todos los clientes tienen entre 1 y 2 cuentas
    # Regla: máximo 2 productos pasivos por cliente
    n_cuentas = random.randint(1, 2)

    # Productos disponibles para este cliente
    productos_disponibles = [1, 2, 3, 4]
    random.shuffle(productos_disponibles)
    seleccionados = productos_disponibles[:n_cuentas]

    for id_pb in seleccionados:

        # Fecha de apertura aleatoria entre 2023 y 2024
        dias_apertura  = random.randint(0, 720)
        fecha_apertura = date(2023, 1, 1) + timedelta(days=dias_apertura)

        # Cuota de manejo según tipo de cuenta
        # Regla: cuenta digital no tiene cuota de manejo
        if id_pb == ID_CUENTA_DIGITAL:
            cuota_manejo = 0
        elif id_pb == ID_CUENTA_CORRIENTE:
            cuota_manejo = 15000
        else:
            cuota_manejo = random.choice([0, 8_900])

        # Saldo base según tipo de cuenta
        # Regla: cuenta corriente tiene saldos más altos
        if id_pb == ID_CUENTA_CORRIENTE:
            saldo_min = 10000000
            saldo_max = 400000000
        elif id_pb == ID_CUENTA_DIGITAL:
            saldo_min = 10000
            saldo_max = 5000000
        else:
            saldo_min = 1000000
            saldo_max = 50000000

        # Ajuste por departamento
        # Regla: departamentos grandes tienen saldos más altos
        if id_depto in deptos_grandes:
            saldo_max = saldo_max * 1.5
        elif id_depto in deptos_pobres:
            saldo_max = saldo_max * 0.3
            saldo_min = saldo_min * 0.1

        # Ajuste por edad
        # Regla: mayores de 37 años tienen más dinero acumulado
        if edad >= 37:
            saldo_min = saldo_min * 1.5
            saldo_max = saldo_max * 2
        elif edad < 30:
            saldo_max = saldo_max * 0.4

        # Ajuste por estado del cliente
        # Regla: inactivos tienen saldos muy bajos, bloqueados saldos congelados
        if estado == 'Inactivo':
            saldo_min = 1000
            saldo_max = 500000
        elif estado == 'Bloqueado':
            saldo_min = 100000
            saldo_max = 5000000

        saldo = round(random.uniform(saldo_min, saldo_max) / 1_000) * 1_000

        prod_pas_rows.append({
            'id_producto_pasivo': id_producto_pasivo,
            'id_producto_banco':  id_pb,
            'id_cliente':         id_cli,
            'numero_cuenta':      str(num_cuenta),
            'saldo_actual':       saldo,
            'cuota_manejo':       cuota_manejo,
            'fecha_apertura':     fecha_apertura.strftime('%Y-%m-%d %H:%M:%S')
        })

        id_producto_pasivo += 1
        num_cuenta += random.randint(1, 9_999)

producto_pasivo = pd.DataFrame(prod_pas_rows)

# Verificar resultados
print("Total productos pasivos:", len(producto_pasivo))
print("Máximo cuentas por cliente:", producto_pasivo.groupby('id_cliente').size().max())
print("Promedio cuentas por cliente:", producto_pasivo.groupby('id_cliente').size().mean().round(1))
print("Saldos negativos:", (producto_pasivo['saldo_actual'] < 0).sum())
print("Saldo promedio:", f"${producto_pasivo['saldo_actual'].mean():,.0f}")
print("Cuota manejo:", producto_pasivo['cuota_manejo'].value_counts().to_dict())

# Guardar el archivo
producto_pasivo.to_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_PRODUCTO_PASIVO.csv', index=False)

print("Archivo guardado correctamente")