import threading
import time
import os

from scraper.utils import initialize_browser, save_flights_to_excel, save_recommendations_to_excel, find_best_combinations
from scraper.config import AIRLINES, rutas
from scraper.flight_scrapers.latam_scraper import get_latam_flight_data
from scraper.flight_scrapers.wingo_scraper import get_wingo_flight_data
from scraper.flight_scrapers.avianca_scraper import get_avianca_flight_data
import pyautogui

def move_mouse():
    while not stop_mouse_thread:
        pyautogui.moveRel(0, 1)  # Mover el mouse 1 píxel hacia abajo
        pyautogui.moveRel(0, -1)  # Mover el mouse 1 píxel hacia arriba
        time.sleep(10)  # Esperar 10 segundos antes de moverlo nuevamente

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

    if best_combinations:
        best = best_combinations[0]
        print(f"Aerolínea: {best['airline']}")
        print(f"  Vuelo de salida: {best['outbound']}")
        print(f"  Vuelo de regreso: {best['return']}")
        print(f"  Precio total: {best['total_price']} COP")
        # send_flight_alert(best)
    else:
        print("No se encontraron combinaciones de vuelos.")

    # Detener el hilo de mover el mouse
    stop_mouse_thread = True
    mouse_thread.join()

    # Comando para bloquear el equipo en Windows
    os.system("rundll32.exe user32.dll,LockWorkStation")

if __name__ == "__main__":
    main()
