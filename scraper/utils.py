from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def send_recommendation_to_api(rec, api_url):
    recommendation = {
        'airline': rec['airline'],
        'outbound_date': rec['outbound']['date'],
        'outbound_departure_time': rec['outbound']['departure_time'],
        'outbound_departure_city': rec['outbound']['departure_city'],
        'outbound_arrival_time': rec['outbound']['arrival_time'],
        'outbound_arrival_city': rec['outbound']['arrival_city'],
        'return_date': rec['return']['date'],
        'return_departure_time': rec['return']['departure_time'],
        'return_departure_city': rec['return']['departure_city'],
        'return_arrival_time': rec['return']['arrival_time'],
        'return_arrival_city': rec['return']['arrival_city'],
        'total_price': rec['total_price']
    }
    try:
        response = requests.post(api_url, json=recommendation)
        if response.status_code in (200, 201):
            print("Recomendación enviada exitosamente.")
        else:
            print(f"Error al enviar la recomendación: {response.status_code}")
            print(f"Detalle del error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Excepción al enviar la recomendación: {e}")

def save_flights_to_excel(flights_data):
    writer = pd.ExcelWriter('output/flights_data.xlsx', engine='openpyxl')

    for airline_data in flights_data:
        airline = airline_data['airline']
        all_flights = []

        for flight in airline_data['outbound']:
            flight['type'] = 'outbound'
            all_flights.append(flight)

        for flight in airline_data['return']:
            flight['type'] = 'return'
            all_flights.append(flight)

        df = pd.DataFrame(all_flights)
        df.to_excel(writer, sheet_name=airline, index=False)

    writer.close()

def save_recommendations_to_excel(recommendations):
    writer = pd.ExcelWriter('output/recommendations.xlsx', engine='openpyxl')

    formatted_recommendations = []
    for rec in recommendations:

        formatted_recommendations.append({
            'airline': rec['airline'],
            'outbound_date': rec['outbound']['date'],
            'outbound_departure_time': rec['outbound']['departure_time'],
            'outbound_departure_city': rec['outbound']['departure_city'],
            'outbound_arrival_time': rec['outbound']['arrival_time'],
            'outbound_arrival_city': rec['outbound']['arrival_city'],
            'return_date': rec['return']['date'],
            'return_departure_time': rec['return']['departure_time'],
            'return_departure_city': rec['return']['departure_city'],
            'return_arrival_time': rec['return']['arrival_time'],
            'return_arrival_city': rec['return']['arrival_city'],
            'total_price': rec['total_price']
        })

    df = pd.DataFrame(formatted_recommendations)
    df.to_excel(writer, sheet_name='Recommendations', index=False)

    writer.close()

def initialize_browser():
    options = Options()
    options.add_argument("--start-maximized")
    # Elimina la ruta manual al chromedriver y utiliza ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def parse_price(price_text, airline):
    price = re.sub(r'\D', '', price_text)
    #if airline == 'LATAM':
    #    price = price[:-2]
    return int(price)

def find_best_combinations(flights_data):
    best_combinations = []

    for data in flights_data:
        airline = data['airline']

        outbound_flights = sorted(data['outbound'], key=lambda x: x['price'])
        return_flights = sorted(data['return'], key=lambda x: x['price'])

        if not outbound_flights or not return_flights:
            print(f"No hay vuelos disponibles para la aerolínea: {airline}")
            continue

        min_price_outbound = outbound_flights[0]['price']
        cheapest_outbound_flights = [f for f in outbound_flights if f['price'] == min_price_outbound]

        min_price_return = return_flights[0]['price']
        cheapest_return_flights = [f for f in return_flights if f['price'] == min_price_return]

        for outbound in cheapest_outbound_flights:
            for return_flight in cheapest_return_flights:
                total_price = outbound['price'] + return_flight['price']
                best_combinations.append({
                    'airline': airline,
                    'outbound': outbound,
                    'return': return_flight,
                    'total_price': total_price
                })

    best_combinations = sorted(best_combinations, key=lambda x: x['total_price'])
    return best_combinations
