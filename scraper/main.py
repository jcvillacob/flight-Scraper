from scraper.utils import initialize_browser, get_flight_data, find_best_combinations
from scraper.config import AIRLINES, DEPARTURE_DATE, RETURN_DATE

def main():
    driver = initialize_browser()
    all_flights = []

    # Solo procesar Avianca
    airline = 'Avianca'
    url_template = AIRLINES[airline]
    url = url_template.format(DEPARTURE_DATE, RETURN_DATE)

    flights = get_flight_data(driver, url, airline)
    all_flights.append(flights)

    # Código comentado para las demás aerolíneas
    """
    for airline, url_template in AIRLINES.items():
        if airline in ['LATAM']:
            url = url_template.format(RETURN_DATE + "T12%3A00%3A00.000Z", DEPARTURE_DATE + "T12%3A00%3A00.000Z")
        elif airline == 'Wingo':
            url = url_template.format(DEPARTURE_DATE, RETURN_DATE)

        flights = get_flight_data(driver, url, airline)
        all_flights.append(flights)
    """

    driver.quit()

    best_combinations = find_best_combinations(all_flights)

    for combination in best_combinations:
        print(f"Aerolínea: {combination['airline']}")
        print(f"  Vuelo de salida: {combination['outbound']}")
        print(f"  Vuelo de regreso: {combination['return']}")
        print(f"  Precio total: {combination['total_price']} COP")

if __name__ == "__main__":
    main()
