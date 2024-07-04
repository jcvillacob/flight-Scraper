import yagmail
import os

def send_email(recipient, subject, body):
    # Conectar con el servidor de Gmail
    yag = yagmail.SMTP('jucaviza6@gmail.com', 'your_password')
    yag.send(to=recipient, subject=subject, contents=body)

def send_flight_alert(combination):
    subject = f"Alerta de Vuelos Baratos - {combination['airline']}"
    body = (f"Vuelo de salida: {combination['outbound']}\n"
            f"Vuelo de regreso: {combination['return']}\n"
            f"Precio total: {combination['total_price']} COP")
    send_email(os.getenv('EMAIL'), subject, body)
