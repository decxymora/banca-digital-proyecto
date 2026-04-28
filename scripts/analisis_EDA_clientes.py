import pandas as pd

# Cargar el archivo de clientes
clientes = pd.read_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_originales\bd_CLIENTES.csv', encoding='latin-1')

# Ver cuántas filas y columnas tiene
print(clientes.shape)

# Ver los nombres de las columnas
print(clientes.columns.tolist())

# Ver los primeros 5 registros
print(clientes.head())

# Verificar si hay valores nulos
print(clientes.isnull().sum())

# Verificar si hay filas duplicadas
print(clientes.duplicated().sum())

# Ver qué valores tiene tipo_documento
print(clientes['TIPO_DOCUMENTO'].value_counts())

# Ver qué valores tiene estado
print(clientes['ESTADO'].value_counts())

# Verificar emails duplicados
print("Emails duplicados:", clientes['EMAIL'].duplicated().sum())

##CAMBIAR EL NOMBRE DE LOS ATRIBUTOS

# Renombrar columnas para que coincidan con el modelo DDL

clientes = clientes.rename(columns={
    'ID_CLIENTE': 'id_cliente',
    'ID_CIUDAD': 'id_ciudad',
    'NOMBRE': 'nombre',
    'APELLIDOS': 'apellido',
    'TIPO_DOCUMENTO': 'tipo_documento',
    'NO_DOCUMENTO': 'numero_documento',
    'FECHA_NACIMIENTO': 'fecha_nacimiento',
    'DIRECCION': 'direccion',
    'EMAIL': 'email',
    'TELEFONO': 'telefono',
    'ESTADO': 'estado'
})

# Verificar que los nombres quedaron bien
print(clientes.columns.tolist())

## Importar random para corregir los datos de tipo_documento
## y estado con distribuciones mas realistas, y para corregir los duplciaods 
## El (42) es la semilla es para reproducibilidad. 
## No nos cambia el resultado cada que se ejecuta

import random
random.seed(42) 

# CORRECCION 1 tipo_documento
# No hay menores de edad en los datos eliminamos TI
# Distribución realista para un banco digital colombiano
# CC 86%, CE 9%, Pasaporte 5%

total = len(clientes)
tipos = (
    ['CC'] * int(total * 0.86) +
    ['CE'] * int(total * 0.09) +
    ['Pasaporte'] * (total - int(total * 0.86) - int(total * 0.09))
)
random.shuffle(tipos)
clientes['tipo_documento'] = tipos

# Ver nueva distribución
print(clientes['tipo_documento'].value_counts())

# CORRECCIÓN 2 estado del cliente
# Distribución Activo 86%, Inactivo 9%, Bloqueado 5%
estados = (
    ['Activo'] * int(total * 0.86) +
    ['Inactivo'] * int(total * 0.09) +
    ['Bloqueado'] * (total - int(total * 0.86) - int(total * 0.09))
)
random.shuffle(estados)
clientes['estado'] = estados

# Verificar distribución
print(clientes['estado'].value_counts())

# CORRECCIÓN 3 emails duplicados
# Si el email ya existe le agregamos el id del cliente

emails_vistos = set() ## no permite duplicados los set
emails_corregidos = [] ## lista pa almacenar los emails corregidos
for _, fila in clientes.iterrows():
    email = str(fila['email']).lower().strip()
    if email in emails_vistos:
        base, dominio = email.split('@')
        email = f"{base}_{fila['id_cliente']}@{dominio}"
    emails_vistos.add(email)
    emails_corregidos.append(email)
clientes['email'] = emails_corregidos

# Verificar que ya no hay duplicados
print("Emails duplicados después de corrección:", clientes['email'].duplicated().sum())

#Tabla final

print(clientes.head())

# Guardar el archivo limpio
clientes.to_csv(r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\bd_CLIENTES.csv', index=False)

print("Archivo guardado correctamente")