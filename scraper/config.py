import pandas as pd

# Leer el archivo Excel
rutas_df = pd.read_excel('rutas.xlsx')

# Asumimos que solo hay una fila en el archivo Excel con los datos necesarios
ruta = rutas_df.iloc[0]

# Convertir las fechas a cadenas en el formato adecuado
departure_date = pd.to_datetime(ruta['Fecha_salida']).strftime('%Y-%m-%d')
return_date = pd.to_datetime(ruta['Fecha_llegada']).strftime('%Y-%m-%d')

# Asignar valores desde el archivo Excel
ORIGIN = ruta['Salida']
DESTINATION = ruta['Llegada']
DEPARTURE_DATE = departure_date
RETURN_DATE = return_date

AIRLINES = {
    'LATAM': 'https://www.latamairlines.com/co/es/ofertas-vuelos?origin={origin}&inbound={return_date}&outbound={departure_date}&destination={destination}&adt=1&chd=0&inf=0&trip=RT&cabin=Economy&redemption=false&sort=RECOMMENDED',
    'Wingo': 'https://booking.wingo.com/en/search/{origin}/{destination}/{departure_date}/{return_date}/1/0/0/0/COP/0/0',
    'Avianca': 'https://www.avianca.com/es/booking/select/?origin1={origin}&destination1={destination}&departure1={departure_date}&adt1=1&tng1=0&chd1=0&inf1=0&origin2={destination}&destination2={origin}&departure2={return_date}&adt2=1&tng2=0&chd2=0&inf2=0&currency=COP&posCode=CO'
}
