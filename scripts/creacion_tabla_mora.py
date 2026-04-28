import pandas as pd
import random
random.seed(42)
from datetime import date

# Cargamos las tablas que necesitamos
extracto        = pd.read_csv(r'./datos_limpios\bd_EXTRACTO.csv')
producto_activo = pd.read_csv(r'./datos_limpios\bd_PRODUCTO_ACTIVO.csv')
clientes        = pd.read_csv(r'./datos_limpios\bd_CLIENTES.csv')
ciudades        = pd.read_csv(r'./datos_limpios\bd_CIUDADES_limpio.csv')

hoy = date(2025, 12, 31)

# Departamentos pobres — más moras activas
# Chocó (27), Vichada (99), Guainía (94), Vaupés (97), La Guajira (44)
deptos_pobres = [27, 99, 94, 97, 44]

# Calcular edad de cada cliente
clientes['fecha_nacimiento'] = pd.to_datetime(clientes['fecha_nacimiento'])
clientes['edad'] = ((hoy - clientes['fecha_nacimiento'].dt.date).apply(lambda x: x.days) / 365.25).astype(int)

# Unir producto_activo con clientes y ciudades
producto_activo = producto_activo.merge(
    clientes[['id_cliente', 'edad']], on='id_cliente', how='left'
)
producto_activo = producto_activo.merge(
    clientes[['id_cliente', 'id_ciudad']], on='id_cliente', how='left'
)
producto_activo = producto_activo.merge(
    ciudades[['id_ciudad', 'id_departamento']], on='id_ciudad', how='left'
)

# Eliminar duplicados antes de crear el índice
producto_activo = producto_activo.drop_duplicates(subset='id_producto_activo')

# Crear índice rápido de producto_activo
prod_idx = producto_activo.set_index('id_producto_activo')

# Filtrar extractos en mora
extractos_mora = extracto[extracto['estado_pago'] == 'Mora'].copy()

# Filtrar solo productos En_Mora o Castigada
ids_prod_mora = set(
    producto_activo[
        producto_activo['estado'].isin(['En_Mora', 'Castigada'])
    ]['id_producto_activo'].tolist()
)

# Solo extractos cuyo producto está en mora o castigado
extractos_mora = extractos_mora[
    extractos_mora['id_producto_activo'].isin(ids_prod_mora)
]

print("Extractos en mora:", len(extractos_mora))
print("Productos en mora o castigados:", len(ids_prod_mora))

mora_rows = []
id_mora = 30001

for _, ext in extractos_mora.iterrows():

    id_prod = ext['id_producto_activo']

    if id_prod not in prod_idx.index:
        continue

    prod = prod_idx.loc[id_prod]

    if isinstance(prod, pd.DataFrame):
        prod = prod.iloc[0]

    estado_prod = str(prod['estado']).strip()
    edad        = prod['edad']
    id_depto    = prod['id_departamento']

    fecha_limite   = pd.to_datetime(ext['fecha_limite_pago']).date()
    fecha_ini_mora = fecha_limite + pd.Timedelta(days=1)
    if hasattr(fecha_ini_mora, 'date'):
        fecha_ini_mora = fecha_ini_mora.date()

    dias_mora = (hoy - fecha_ini_mora).days
    if dias_mora < 0:
        continue

    tasa_mora    = prod['tasa_interes_mora']
    interes_mora = round(
        ext['saldo_capital_pendiente'] * tasa_mora / 100 * dias_mora / 30, 0
    )

    # Estado de mora según reglas de negocio
    if estado_prod == 'Castigada':
        estado_mora = 'Activa'
    elif estado_prod == 'En_Mora':
        pesos = [50, 35, 15]
        if edad <= 25:
            pesos = [65, 25, 10]
        if id_depto in deptos_pobres:
            pesos[0] += 10
            pesos[2] -= 10
        estado_mora = random.choices(
            ['Activa', 'En Gestión', 'Liquidada'],
            weights=pesos
        )[0]
    else:
        estado_mora = 'Activa'

    mora_rows.append({
        'id_mora':            id_mora,
        'id_producto_activo': id_prod,
        'id_extracto':        ext['id_extracto'],
        'fecha_inicio_mora':  fecha_ini_mora.strftime('%Y-%m-%d'),
        'dias_mora':          dias_mora,
        'capital_vencido':    ext['saldo_capital_pendiente'],
        'interes_mora':       max(0, interes_mora),
        'estado_mora':        estado_mora
    })
    id_mora += 1

mora = pd.DataFrame(mora_rows)

# Verificar resultados
print("Total registros mora:", len(mora))
print("Estado mora:", mora['estado_mora'].value_counts().to_dict())
print("Días mora promedio:", mora['dias_mora'].mean().round(0))
print("Días mora máximo:", mora['dias_mora'].max())

# Guardar el archivo
mora.to_csv(r'./datos_limpios\bd_MORA.csv', index=False)

print("Archivo guardado correctamente")