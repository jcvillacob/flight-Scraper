from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re


def initialize_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def parse_price(price_text, airline):
    # Eliminar todos los caracteres no numéricos
    price = re.sub(r'\D', '', price_text)
    # Si es LATAM, eliminar los dos últimos dígitos (decimales)
    if airline == 'LATAM':
        price = price[:-2]
    return int(price)


def get_flight_data(driver, url, airline):
    driver.get(url)
    time.sleep(10)

    flights = {
        'outbound': [],
        'return': []
    }

    if airline == 'LATAM':
        # Extraer datos de los vuelos de salida
        flight_elements = driver.find_elements(By.CSS_SELECTOR, '[id^="FlightInfoComponent"]')
        for element in flight_elements:
            try:
                departure_time = element.find_element(By.CSS_SELECTOR,
                                                      '[data-testid$="-origin"] .flightInfostyle__TextHourFlight-sc__sc-169zitd-4').text
                departure_city = element.find_element(By.CSS_SELECTOR,
                                                      '[data-testid$="-origin"] .flightInfostyle__TextIATA-sc__sc-169zitd-5').text
                arrival_time = element.find_element(By.CSS_SELECTOR,
                                                    '[data-testid$="-destination"] .flightInfostyle__TextHourFlight-sc__sc-169zitd-4').text
                arrival_city = element.find_element(By.CSS_SELECTOR,
                                                    '[data-testid$="-destination"] .flightInfostyle__TextIATA-sc__sc-169zitd-5').text
                price_text = element.find_element(By.CSS_SELECTOR,
                                                  '[data-testid$="-amount"] .displayCurrencystyle__CurrencyAmount-sc__sc-hel5vp-2').text

                # Convertir precio a número
                price = parse_price(price_text, airline)

                flights['outbound'].append({
                    'departure_time': departure_time,
                    'departure_city': departure_city,
                    'arrival_time': arrival_time,
                    'arrival_city': arrival_city,
                    'price': price
                })
            except Exception as e:
                print(f"Error extracting outbound data from LATAM: {e}")

        # Dar click en cualquier elemento de los vuelos de salida
        try:
            flight_elements[0].click()
            time.sleep(2)  # Esperar que se abra el detalle
        except Exception as e:
            print(f"Error clicking on outbound flight element: {e}")

        # Dar click en el primer botón
        try:
            driver.find_element(By.XPATH,
                                '/html/body/div[1]/div[1]/main/div/div/div/div/ol/li[1]/div/ol/li[1]/div/div[3]/div[3]/button').click()
            time.sleep(2)  # Esperar que se abra el siguiente detalle
        except Exception as e:
            print(f"Error clicking on first button: {e}")

        # Dar click en el segundo botón
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/main/div/div/div/div/ol/li[1]/div/ol/li[1]/div/div[3]/div[3]/dialog/div/div[1]/ul/li[1]/div/div[3]/div[2]/button'))
            ).click()
            time.sleep(8)  # Esperar que se carguen los vuelos de regreso
        except Exception as e:
            print(f"Error clicking on second button: {e}")

        # Extraer datos de los vuelos de regreso
        return_elements = driver.find_elements(By.CSS_SELECTOR, '[id^="FlightInfoComponent"]')
        for element in return_elements:
            try:
                departure_time = element.find_element(By.CSS_SELECTOR,
                                                      '[data-testid$="-origin"] .flightInfostyle__TextHourFlight-sc__sc-169zitd-4').text
                departure_city = element.find_element(By.CSS_SELECTOR,
                                                      '[data-testid$="-origin"] .flightInfostyle__TextIATA-sc__sc-169zitd-5').text
                arrival_time = element.find_element(By.CSS_SELECTOR,
                                                    '[data-testid$="-destination"] .flightInfostyle__TextHourFlight-sc__sc-169zitd-4').text
                arrival_city = element.find_element(By.CSS_SELECTOR,
                                                    '[data-testid$="-destination"] .flightInfostyle__TextIATA-sc__sc-169zitd-5').text
                price_text = element.find_element(By.CSS_SELECTOR,
                                                  '[data-testid$="-amount"] .displayCurrencystyle__CurrencyAmount-sc__sc-hel5vp-2').text

                # Convertir precio a número
                price = parse_price(price_text, airline)

                flights['return'].append({
                    'departure_time': departure_time,
                    'departure_city': departure_city,
                    'arrival_time': arrival_time,
                    'arrival_city': arrival_city,
                    'price': price
                })
            except Exception as e:
                print(f"Error extracting return data from LATAM: {e}")

    elif airline == 'Wingo':
        # Extraer datos de vuelos de salida de Wingo
        outbound_elements = driver.find_elements(By.CSS_SELECTOR, '#departure-fligth [id^="flight-"]')
        for element in outbound_elements:
            try:
                departure_time = element.find_element(By.CSS_SELECTOR,
                                                      '.col-4.text-start p.font-gray.font-weight-bold').text
                departure_city = element.find_element(By.CSS_SELECTOR, '.col-4.text-start p.date-info-airport').text.split(' ')[0]
                arrival_time = element.find_element(By.CSS_SELECTOR,
                                                    '.col-4.text-end p.font-gray.font-weight-bold').text
                arrival_city = element.find_element(By.CSS_SELECTOR, '.col-4.text-end p.date-info-airport').text.split(' ')[0]
                price_text = element.find_element(By.CSS_SELECTOR, '.col-9 p.font-weight-bold').text

                # Convertir precio a número
                price = parse_price(price_text, airline)

                flights['outbound'].append({
                    'departure_time': departure_time,
                    'departure_city': departure_city,
                    'arrival_time': arrival_time,
                    'arrival_city': arrival_city,
                    'price': price
                })
            except Exception as e:
                print(f"Error extracting outbound data from Wingo: {e}")

        # Extraer datos de vuelos de regreso de Wingo
        return_elements = driver.find_elements(By.CSS_SELECTOR, '#return-fligth [id^="flight-"]')
        for element in return_elements:
            try:
                departure_time = element.find_element(By.CSS_SELECTOR,
                                                      '.col-4.text-start p.font-gray.font-weight-bold').text
                departure_city = element.find_element(By.CSS_SELECTOR, '.col-4.text-start p.date-info-airport').text.split(' ')[0]
                arrival_time = element.find_element(By.CSS_SELECTOR,
                                                    '.col-4.text-end p.font-gray.font-weight-bold').text
                arrival_city = element.find_element(By.CSS_SELECTOR, '.col-4.text-end p.date-info-airport').text.split(' ')[0]
                price_text = element.find_element(By.CSS_SELECTOR, '.col-9 p.font-weight-bold').text

                # Convertir precio a número
                price = parse_price(price_text, airline)

                flights['return'].append({
                    'departure_time': departure_time,
                    'departure_city': departure_city,
                    'arrival_time': arrival_time,
                    'arrival_city': arrival_city,
                    'price': price
                })
            except Exception as e:
                print(f"Error extracting return data from Wingo: {e}")


    elif airline == 'Avianca':

        # Hacer clic en el botón de cookies si está presente

        try:

            WebDriverWait(driver, 10).until(

                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))

            ).click()

            time.sleep(2)  # Esperar que desaparezca el mensaje de cookies

        except Exception as e:

            print(f"Error clicking on cookies button: {e}")

        # Extraer datos de vuelos de salida de Avianca

        outbound_elements = driver.find_elements(By.CSS_SELECTOR, '.journey_inner')

        for element in outbound_elements:

            try:

                departure_time = element.find_element(By.CSS_SELECTOR,

                                                      '.journey-schedule_time-departure').text.strip()

                arrival_time = element.find_element(By.CSS_SELECTOR,

                                                    '.journey-schedule_time-return').text.strip()

                departure_city = element.find_element(By.CSS_SELECTOR,

                                                      '.journey-schedule_station-departure .journey-schedule_station_code').text.strip()

                arrival_city = element.find_element(By.CSS_SELECTOR,

                                                    '.journey-schedule_station-return .journey-schedule_station_code').text.strip()

                price_text = element.find_element(By.CSS_SELECTOR,

                                                  '.journey_price_button .price').text.strip()

                if departure_time and arrival_time and departure_city and arrival_city and price_text:
                    # Convertir precio a número

                    price = parse_price(price_text, airline)

                    flights['outbound'].append({

                        'departure_time': departure_time,

                        'departure_city': departure_city,

                        'arrival_time': arrival_time,

                        'arrival_city': arrival_city,

                        'price': price

                    })

            except Exception as e:

                print(f"Error extracting outbound data from Avianca: {e}")

        # Dar click en el primer elemento de los vuelos de salida

        try:

            outbound_elements[0].click()

            time.sleep(2)  # Esperar que se abra el detalle

        except Exception as e:

            print(f"Error clicking on outbound flight element: {e}")

        # Dar click en el primer botón

        try:

            WebDriverWait(driver, 10).until(

                EC.element_to_be_clickable((By.XPATH,

                                            '/html/body/div[1]/main/div/div[2]/div/div/journey-availability-select-container/div/price-journey-select-custom/div[2]/div[2]/div[1]/journey-control-custom/div/div/div[2]/div/div/div/div[1]/fare-control/div[2]/div[3]/button'))

            ).click()

            time.sleep(2)  # Esperar que se abra el siguiente detalle

        except Exception as e:

            print(f"Error clicking on first button: {e}")

        # Verificar y hacer clic en el segundo botón

        try:

            WebDriverWait(driver, 10).until(

                EC.element_to_be_clickable((By.CLASS_NAME, 'cro-no-accept-upsell-button'))

            ).click()

            time.sleep(8)  # Esperar que se carguen los vuelos de regreso

        except Exception as e:

            print(f"Error clicking on second button: {e}")

        # Extraer datos de los vuelos de regreso de Avianca

        return_elements = driver.find_elements(By.CSS_SELECTOR, '.journey_inner')

        for element in return_elements:

            try:

                departure_time = element.find_element(By.CSS_SELECTOR,

                                                      '.journey-schedule_time-departure').text.strip()

                arrival_time = element.find_element(By.CSS_SELECTOR,

                                                    '.journey-schedule_time-return').text.strip()

                departure_city = element.find_element(By.CSS_SELECTOR,

                                                      '.journey-schedule_station-departure .journey-schedule_station_code').text.strip()

                arrival_city = element.find_element(By.CSS_SELECTOR,

                                                    '.journey-schedule_station-return .journey-schedule_station_code').text.strip()

                price_text = element.find_element(By.CSS_SELECTOR,

                                                  '.journey_price_button .price').text.strip()

                if departure_time and arrival_time and departure_city and arrival_city and price_text:
                    # Convertir precio a número

                    price = parse_price(price_text, airline)

                    flights['return'].append({

                        'departure_time': departure_time,

                        'departure_city': departure_city,

                        'arrival_time': arrival_time,

                        'arrival_city': arrival_city,

                        'price': price

                    })

            except Exception as e:

                print(f"Error extracting return data from Avianca: {e}")

    return {
        'airline': airline,
        'outbound': flights['outbound'],
        'return': flights['return']
    }


def find_best_combinations(flights_data):
    best_combinations = []

    for data in flights_data:
        airline = data['airline']
        outbound_flights = sorted(data['outbound'], key=lambda x: x['price'])
        return_flights = sorted(data['return'], key=lambda x: x['price'])

        combinations = []
        for outbound in outbound_flights[:5]:
            for return_flight in return_flights[:5]:
                total_price = outbound['price'] + return_flight['price']
                combinations.append({
                    'airline': airline,
                    'outbound': outbound,
                    'return': return_flight,
                    'total_price': total_price
                })

        best_combinations.extend(sorted(combinations, key=lambda x: x['total_price'])[:5])

    return best_combinations
