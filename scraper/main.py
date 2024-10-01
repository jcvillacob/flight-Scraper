import threading
import time
import os

from scraper.utils import initialize_browser, save_flights_to_excel, save_recommendations_to_excel, find_best_combinations, send_recommendation_to_api
from scraper.config import AIRLINES, rutas
from scraper.flight_scrapers.latam_scraper import get_latam_flight_data
from scraper.flight_scrapers.wingo_scraper import get_wingo_flight_data
from scraper.flight_scrapers.avianca_scraper import get_avianca_flight_data
import pyautogui

API_URL = "http://localhost:4000/api/v1/pruebas/vuelos/"

def move_mouse():
    while not stop_mouse_thread:
        pyautogui.moveRel(0, 1)
        pyautogui.moveRel(0, -1)
        time.sleep(10)

# Variable global para controlar el hilo del mouse
stop_mouse_thread = False

def main():
    global stop_mouse_thread

    # Iniciar el hilo para mover el mouse
    mouse_thread = threading.Thread(target=move_mouse)
    mouse_thread.start()

    driver = initialize_browser()
    all_flights = []

    for ruta in rutas:
        ORIGIN = ruta['Salida']
        DESTINATION = ruta['Llegada']
        DEPARTURE_DATE = ruta['Fecha_salida']
        RETURN_DATE = ruta['Fecha_llegada']

        for airline in AIRLINES.keys():
            if airline == 'LATAM':
                flights = get_latam_flight_data(driver, ORIGIN, DESTINATION, DEPARTURE_DATE, RETURN_DATE)
            elif airline == 'Wingo':
                flights = get_wingo_flight_data(driver, ORIGIN, DESTINATION, DEPARTURE_DATE, RETURN_DATE)
            elif airline == 'Avianca':
                flights = get_avianca_flight_data(driver, ORIGIN, DESTINATION, DEPARTURE_DATE, RETURN_DATE)

            all_flights.append({
                'airline': airline,
                'outbound': flights['outbound'],
                'return': flights['return']
            })

    driver.quit()

    best_combinations = find_best_combinations(all_flights)
    save_flights_to_excel(all_flights)
    save_recommendations_to_excel(best_combinations)

    # Filtrar las combinaciones por debajo de 400,000 COP
    filtered_combinations = [comb for comb in best_combinations if comb['total_price'] < 100000]

    # Enviar todas las recomendaciones filtradas al API
    for recommendation in filtered_combinations:
        send_recommendation_to_api(recommendation, API_URL)
        print(f"Aerolínea: {recommendation['airline']}")
        print(f"  Vuelo de salida: {recommendation['outbound']}")
        print(f"  Vuelo de regreso: {recommendation['return']}")
        print(f"  Precio total: {recommendation['total_price']} COP")

    if not filtered_combinations:
        print("No se encontraron combinaciones de vuelos por debajo de 100,000 COP.")

    # Detener el hilo de mover el mouse
    stop_mouse_thread = True
    mouse_thread.join()

if __name__ == "__main__":
    main()
