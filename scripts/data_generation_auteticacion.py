## haslib es para encriptar contraseñas,
## random para generar números aleatorios y 
## el 42 la semilla para que los resultados sean reproducibles 

import pandas as pd
import hashlib
import random
random.seed(42)

# Cargamos clientes porque necesitamos los ids y los estados
clientes = pd.read_csv(r'./datos_limpios\bd_CLIENTES.csv')

# Ver cuántos clientes tenemos
print("Total clientes:", len(clientes))

# Generamos un usuario por cada cliente
# Regla de negocioun cliente = un usuario (relación 1 a 1)
auth_rows = []

for _, fila in clientes.iterrows():

    # Ciframos la contraseña con SHA-256
    # Se genera un texto base, que inclya mi_contra + id cliente +_banca2024,
    # para que cada contraseña sea única, aunque el formato sea el mismo.
    
    clave_hash = hashlib.sha256(
        f"mi_contra{fila['id_cliente']}_banca2024".encode()
    ).hexdigest()

    # El estado de autenticacion debe ser coherente con el estado de latabla cliente
    # Cliente Activo sera usuario Activo
    # Cliente Bloqueado sera usuario Bloqueado
    # Cliente Inactivo sera usuario Suspendido
    mapa_estado_auth = {
        'Activo': 'Activo',
        'Bloqueado': 'Bloqueado',
        'Inactivo': 'Suspendido'
    }
    estado = mapa_estado_auth[fila['estado']]

    # Si está bloqueado o suspendido tiene intentos fallidos registrados
    intentos = 0 if estado == 'Activo' else random.randint(3, 5)

    auth_rows.append({
        'id_usuario':        fila['id_cliente'],
        'id_cliente':        fila['id_cliente'],
        'nombre_usuario':    f"user_{fila['id_cliente']}",
        'clave_hash':        clave_hash,
        'tipo_mfa':          random.choice(['SMS', 'App', 'Correo']),
        'estado':            estado,
        'intentos_fallidos': intentos,
        'ultimo_ingreso':    f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d} {random.randint(6,22):02d}:{random.randint(0,59):02d}:00"
    })

autenticacion = pd.DataFrame(auth_rows)

# Verificar cómo quedó
print(autenticacion.shape)
print(autenticacion.head())
print(autenticacion['estado'].value_counts())

# Guardar el archivo
autenticacion.to_csv(r'./datos_limpios\bd_AUTENTICACION_CLIENTE.csv', index=False)

print("Archivo guardado correctamente")