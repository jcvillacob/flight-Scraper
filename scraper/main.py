from scraper.utils import initialize_browser, save_flights_to_excel, save_recommendations_to_excel, \
    find_best_combinations
from scraper.config import AIRLINES, ORIGIN, DESTINATION, DEPARTURE_DATE, RETURN_DATE
from scraper.flight_scrapers.latam_scraper import get_latam_flight_data
from scraper.flight_scrapers.wingo_scraper import get_wingo_flight_data
from scraper.flight_scrapers.avianca_scraper import get_avianca_flight_data
import os
from scraper.email_notifications import send_flight_alert



def main():
    driver = initialize_browser()
    all_flights = []

    for airline in AIRLINES.keys():
        if airline == 'LATAM':
            flights = get_latam_flight_data(driver, ORIGIN, DESTINATION, DEPARTURE_DATE, RETURN_DATE)
        elif airline == 'Wingo':
            flights = get_wingo_flight_data(driver, ORIGIN, DESTINATION, DEPARTURE_DATE, RETURN_DATE)
        elif airline == 'Avianca':
            flights = get_avianca_flight_data(driver, ORIGIN, DESTINATION, DEPARTURE_DATE, RETURN_DATE)

        all_flights.append(flights)

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

        # Comando para bloquear el equipo en Windows
    os.system("rundll32.exe user32.dll,LockWorkStation")

if __name__ == "__main__":
    main()
