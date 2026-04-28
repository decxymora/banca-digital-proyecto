import pandas as pd

# Cargar el archivo de ciudades
ciudades = pd.read_csv(r'./datos_originales\bd_CIUDADES.csv', encoding='latin-1')

# Ver cuántas filas y columnas tiene
print(ciudades.shape)

# Ver los nombres de las columnas
print(ciudades.columns.tolist())

# Ver los primeros 5 registros
print(ciudades.head())

# Verificar si hay valores nulos
print(ciudades.isnull().sum())

# Verificar si hay filas duplicadas
print(ciudades.duplicated().sum())

#Renombrar las columnas igual que en el DDL

# Renombrar columnas para que coincidan con el modelo SQL
ciudades = ciudades.rename(columns={
    'ID_CIUDAD': 'id_ciudad',
    'ID_DEPARTAMENTO': 'id_departamento',
    'CIUDAD': 'nombre_ciudad'
})

# Verificar que el cambio quedó bien
print(ciudades.columns.tolist())

# Guardar el archivo limpio
ciudades.to_csv(r'./datos_limpios\bd_CIUDADES_limpio.csv', index=False)

print("Archivo guardado correctamente")