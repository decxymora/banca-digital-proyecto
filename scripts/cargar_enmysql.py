
import pandas as pd
from sqlalchemy import create_engine

# Configuración de conexión a MySQL
# Cambia la contraseña si ninguna funciona
USUARIO    = 'root'
CONTRASENA = 'root'       # Prueba primero con esta
HOST       = 'localhost'
PUERTO     = '3306'
BD         = 'BANCA_DIGITAL'

# Crear conexión
engine = create_engine(f'mysql+pymysql://{USUARIO}:{CONTRASENA}@{HOST}:{PUERTO}/{BD}')

# Verificar conexión
try:
    with engine.connect() as conn:
        print("Conexión exitosa a MySQL")
except Exception as e:
    print("Error de conexión:", e)
    print("Intenta cambiar CONTRASENA a '1234'")

    # Ruta de los archivos limpios
RUTA = r'C:\Users\angie\OneDrive\Escritorio\Proyecto_ banca\datos_limpios\\'

# Orden de carga — respeta las dependencias entre tablas
# Las tablas que tienen FK deben cargarse después de sus tablas padre
tablas = [
    ('departamentos',          'bd_DEPARTAMENTOS_limpio.csv'),
    ('ciudades',               'bd_CIUDADES_limpio.csv'),
    ('productos_banco',        'bd_PRODUCTOS_BANCO.csv'),
    ('tipo_transaccion',       'bd_TIPO_TRANSACCION.csv'),
    ('cliente',                'bd_CLIENTES.csv'),
    ('autenticacion_cliente',  'bd_AUTENTICACION_CLIENTE.csv'),
    ('producto_activo',        'bd_PRODUCTO_ACTIVO.csv'),
    ('producto_pasivo',        'bd_PRODUCTO_PASIVO.csv'),
    ('extracto',               'bd_EXTRACTO.csv'),
    ('transacciones',          'bd_TRANSACCIONES.csv'),
    ('mora',                   'bd_MORA.csv'),
    ('gestion_cobranza',       'bd_GESTION_COBRANZA.csv'),
]

for nombre_tabla, archivo in tablas:
    try:
        df = pd.read_csv(RUTA + archivo)
        df.to_sql(
            name=nombre_tabla,
            con=engine,
            if_exists='append',   # Agrega los datos sin borrar la tabla
            index=False
        )
        print(f"✓ {nombre_tabla}: {len(df)} filas cargadas")
    except Exception as e:
        print(f"✗ {nombre_tabla}: ERROR — {e}")

print("\nCarga completada")