import pandas as pd
import random
random.seed(42)
from datetime import date, timedelta

# Cargamos las tablas que necesitamos
mora            = pd.read_csv(r'./datos_limpios\bd_MORA.csv')
producto_activo = pd.read_csv(r'./datos_limpios\bd_PRODUCTO_ACTIVO.csv')
clientes        = pd.read_csv(r'./datos_limpios\bd_CLIENTES.csv')
ciudades        = pd.read_csv(r'./datos_limpios\bd_CIUDADES_limpio.csv')

hoy = date(2025, 12, 31)

# Departamentos pobres — más gestiones porque son más difíciles de cobrar
# Chocó (27), Vichada (99), Guainía (94), Vaupés (97), La Guajira (44)
deptos_pobres = [27, 99, 94, 97, 44]

# Calcular edad de cada cliente
clientes['fecha_nacimiento'] = pd.to_datetime(clientes['fecha_nacimiento'])
clientes['edad'] = ((hoy - clientes['fecha_nacimiento'].dt.date).apply(lambda x: x.days) / 365.25).astype(int)

# Unir mora con producto_activo, clientes y ciudades
mora = mora.merge(producto_activo[['id_producto_activo', 'id_cliente']], on='id_producto_activo', how='left')
mora = mora.merge(clientes[['id_cliente', 'edad', 'id_ciudad']], on='id_cliente', how='left')
mora = mora.merge(ciudades[['id_ciudad', 'id_departamento']], on='id_ciudad', how='left')

# Solo moras Activa y En Gestión generan gestiones
# Las Liquidadas ya se cerraron
moras_gestionables = mora.copy()
print("Moras gestionables:", len(moras_gestionables))

# Resultados posibles por tipo de contacto — coherentes con la realidad
resultados_por_tipo = {
    'SMS': [
        'SMS enviado exitosamente',
        'Cliente responde confirmando pago próximo',
        'Número no recibe SMS'
    ],
    'Correo': [
        'Correo enviado sin respuesta',
        'Cliente responde solicitando plazo adicional',
        'Correo rebotado — dirección inválida',
        'Cliente confirma recepción y promete pago'
    ],
    'Llamada': [
        'Cliente no contesta',
        'Cliente promete pagar en 5 días',
        'Buzón de voz — se deja mensaje',
        'Cliente solicita refinanciación',
        'Cliente reconoce deuda sin fecha de pago'
    ],
    'Visita Domiciliaria': [
        'Cliente no se encontraba en domicilio',
        'Cliente recibe notificación de cobro',
        'Se deja aviso de cobro en puerta',
        'Cliente firma acuerdo de pago'
    ]
}

gest_rows = []
id_gestion = 40001

for _, fila_mora in moras_gestionables.iterrows():

    dias_mora = fila_mora['dias_mora']
    edad      = fila_mora['edad']
    id_depto  = fila_mora['id_departamento']

    # Más gestiones para jóvenes y departamentos pobres
    # porque son más difíciles de cobrar
    if edad <= 25 or id_depto in deptos_pobres:
        n_gestiones = random.randint(3, 4)
    else:
        n_gestiones = random.randint(1, 3)

    fecha_base = pd.to_datetime(fila_mora['fecha_inicio_mora']).date()

    for g in range(n_gestiones):

        # Gestiones espaciadas entre 5 y 10 días
        dias_offset = random.randint(g * 5, g * 5 + 10)
        fecha_gest  = fecha_base + timedelta(days=dias_offset)

        # No generar gestiones en el futuro
        if fecha_gest > hoy:
            break

        # Escalada de contacto según días de mora
        # 1 a 30 días → SMS y Correo primero
        # 31 a 90 días → Llamadas
        # Más de 90 días → Visita Domiciliaria
        if dias_mora <= 30:
            tipo_contacto = random.choices(
                ['SMS', 'Correo', 'Llamada'],
                weights=[50, 30, 20]
            )[0]
        elif dias_mora <= 90:
            tipo_contacto = random.choices(
                ['Llamada', 'Correo', 'SMS'],
                weights=[60, 25, 15]
            )[0]
        else:
            tipo_contacto = random.choices(
                ['Visita Domiciliaria', 'Llamada', 'Correo'],
                weights=[40, 40, 20]
            )[0]

        resultado = random.choice(resultados_por_tipo[tipo_contacto])

        gest_rows.append({
            'id_gestion':        id_gestion,
            'id_mora':           fila_mora['id_mora'],
            'fecha_gestion':     fecha_gest.strftime('%Y-%m-%d %H:%M:%S'),
            'tipo_contacto':     tipo_contacto,
            'resultado_gestion': resultado
        })
        id_gestion += 1

gestion_cobranza = pd.DataFrame(gest_rows)

# Verificar resultados
print("Total gestiones:", len(gestion_cobranza))
print("Tipo contacto:", gestion_cobranza['tipo_contacto'].value_counts().to_dict())

# Guardar el archivo
gestion_cobranza.to_csv(r'./datos_limpios\bd_GESTION_COBRANZA.csv', index=False)

print("Archivo guardado correctamente")