import pandas as pd

# Cargar el archivo de tipo de transacción
tipo_transaccion = pd.read_csv(r'./datos_originales\bd_TIPO DE TRANSACCION.csv', encoding='latin-1', sep=';')

# Ver cuántas filas y columnas tiene
print(tipo_transaccion.shape)

# Ver los nombres de las columnas
print(tipo_transaccion.columns.tolist())

# Ver todos los registros porque son pocos
print(tipo_transaccion)

# Verificar si hay valores nulos
print(tipo_transaccion.isnull().sum())

# Verificar si hay filas duplicadas
print(tipo_transaccion.duplicated().sum())

# Eliminar la columna descrpicion no esta en DDL

tipo_transaccion = tipo_transaccion.drop(columns=['Descripción o Ejemplo'])

# Renombrar los atributos como en  el DDL

# Renombrar columnas para que coincidan con el modelo SQL
tipo_transaccion = tipo_transaccion.rename(columns={
    'ID': 'id_tipo_transaccion',
    'Nombre de la Transacción': 'nombre_tipo',
    'Naturaleza': 'naturaleza'
})

# Corregir mayúsculas en naturaleza
# El modelo espera 'Entrada', 'Salida', 'Neutro' no 'ENTRADA', 'SALIDA', 'NEUTRO'
tipo_transaccion['naturaleza'] = tipo_transaccion['naturaleza'].str.capitalize()

# Verificar los cambios
print(tipo_transaccion.columns.tolist())
print(tipo_transaccion)

# Guardar el archivo limpio
tipo_transaccion.to_csv(r'./datos_limpios\bd_TIPO_TRANSACCION.csv', index=False)

print("Archivo guardado correctamente")
