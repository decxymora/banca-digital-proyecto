import pandas as pd

# Cargar el archivo de productos del banco
productos_banco = pd.read_csv(r'./datos_originales\bd_PRODUCTOS BANCO.csv', encoding='latin-1', sep=';')

# Ver cuántas filas y columnas tiene
print(productos_banco.shape)

# Ver los nombres de las columnas
print(productos_banco.columns.tolist())

# Ver todos los registros porque solo son 12
print(productos_banco)

# Verificar si hay valores nulos
print(productos_banco.isnull().sum())

# Verificar si hay filas duplicadas
print(productos_banco.duplicated().sum())

#Renombrar los atributos como en  el DDL 

productos_banco = productos_banco.rename(columns={
    'ID_producto_banco': 'id_producto_banco'
})

# Corregir mayúsculas en tipo_producto
# El ENUM  'Activo' y 'Pasivo' no 'ACTIVO' y 'PASIVO'
productos_banco['tipo_producto'] = productos_banco['tipo_producto'].str.capitalize()

# Verificar los cambios
print(productos_banco['tipo_producto'].unique())
print(productos_banco.columns.tolist())

# Guardar el archivo limpio
productos_banco.to_csv(r'./datos_limpios\bd_PRODUCTOS_BANCO.csv', index=False)

print("Archivo guardado correctamente")
