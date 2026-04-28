## PROYECRO INTEGRADOR - BANCA DIGITAL 
## ANALISIS EXPLORATORIO 

import pandas as pd 

# TABLA 1 DEPARTAMENTOS, ENCONDING POR SI TIENE TILDES O Ñ,

departamentos = pd.read_csv(r'./datos_originales\bd_DEPARTAMENTOS.csv', encoding='latin-1')

# Ver cuantas filas y columnas tiene
print(departamentos.shape)

# Ver los nombres de las columnas
print(departamentos.columns.tolist())

# Ver los primeros 5 registros
print(departamentos.head())

# Verificar si hay valores nulos
print(departamentos.isnull().sum())

# Verificar si hay filas duplicadas
print(departamentos.duplicated().sum())


# Renombrar las collumnas igual que en el DDL 

departamentos = departamentos.rename(columns={
    'Codigo Departamento': 'id_departamento',
    'Nombre Departamento': 'nombre_departamento'
})

# Verificar los cambios
print(departamentos.columns.tolist())

#GUARDAR EL ARCHIVO LIMPIO
departamentos.to_csv(r'./datos_limpios\bd_DEPARTAMENTOS_limpio.csv', index=False)

