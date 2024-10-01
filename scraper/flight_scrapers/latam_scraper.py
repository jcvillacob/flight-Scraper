from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.utils import parse_price
import time

def get_latam_flight_data(driver, origin, destination, departure_date, return_date):
    url_template = 'https://www.latamairlines.com/co/es/ofertas-vuelos?origin={origin}&inbound={return_date}&outbound={departure_date}&destination={destination}&adt=1&chd=0&inf=0&trip=RT&cabin=Economy&redemption=false&sort=RECOMMENDED'
    url = url_template.format(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date
    )

    driver.get(url)

    flights = {'outbound': [], 'return': []}

    # Esperar a que los elementos de vuelo estén presentes
    try:
        flight_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[id^="FlightInfoComponent"]'))
        )
    except Exception as e:
        print(f"Error al encontrar elementos de vuelo: {e}")
        return None

    for element in flight_elements:
        try:
            departure_time = element.find_element(By.CSS_SELECTOR, '[data-testid$="-origin"] .flightInfostyle__TextHourFlight-sc__sc-169zitd-4').text
            departure_city = element.find_element(By.CSS_SELECTOR, '[data-testid$="-origin"] .flightInfostyle__TextIATA-sc__sc-169zitd-5').text
            arrival_time = element.find_element(By.CSS_SELECTOR, '[data-testid$="-destination"] .flightInfostyle__TextHourFlight-sc__sc-169zitd-4').text
            arrival_city = element.find_element(By.CSS_SELECTOR, '[data-testid$="-destination"] .flightInfostyle__TextIATA-sc__sc-169zitd-5').text
            price_text = element.find_element(By.CSS_SELECTOR, '[data-testid$="-amount"] .displayCurrencystyle__CurrencyAmount-sc__sc-hel5vp-2').text

            price = parse_price(price_text, 'LATAM')

            flights['outbound'].append({
                'date': departure_date,
                'departure_time': departure_time,
                'departure_city': departure_city,
                'arrival_time': arrival_time,
                'arrival_city': arrival_city,
                'price': price
            })
        except Exception as e:
            print(f"Error al extraer datos de salida de LATAM: {e}")

    # Intentar hacer clic en el elemento del vuelo de salida con reintentos
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            outbound_flight = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[id^="FlightInfoComponent"]'))
            )
            outbound_flight.click()
            time.sleep(2)
            break
        except Exception as e:
            print(f"Intento {attempt}: Error al hacer clic en el vuelo de salida: {e}")
            if attempt < max_retries:
                time.sleep(2)
            else:
                print("No se pudo hacer clic en el vuelo de salida después de 3 intentos.")
                return None  # O maneja el error según corresponda

    # Intentar hacer clic en el primer botón con reintentos
    first_button_xpath = '/html/body/div[1]/div[1]/main/div/div/div/div/ol/li[1]/div/ol/li[1]/div/div[3]/div[3]/button'
    for attempt in range(1, max_retries + 1):
        try:
            first_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, first_button_xpath))
            )
            first_button.click()
            time.sleep(2)
            break
        except Exception as e:
            print(f"Intento {attempt}: Error al hacer clic en el primer botón: {e}")
            if attempt < max_retries:
                time.sleep(2)
            else:
                print("No se pudo hacer clic en el primer botón después de 3 intentos.")
                return None  # O maneja el error según corresponda

    # Intentar hacer clic en el segundo botón con reintentos
    second_button_xpath = '/html/body/div[1]/div[1]/main/div/div/div/div/ol/li[1]/dialog/div/div[1]/div[2]/li[1]/div/div[3]/div[2]/button'
    for attempt in range(1, max_retries + 1):
        try:
            second_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, second_button_xpath))
            )
            second_button.click()
            time.sleep(8)
            break
        except Exception as e:
            print(f"Intento {attempt}: Error al hacer clic en el segundo botón: {e}")
            if attempt < max_retries:
                time.sleep(2)
            else:
                print("No se pudo hacer clic en el segundo botón después de 3 intentos.")
                return None  # O maneja el error según corresponda

    # Esperar a que los elementos de vuelo de retorno estén presentes
    try:
        return_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[id^="FlightInfoComponent"]'))
        )
    except Exception as e:
        print(f"Error al encontrar elementos de vuelo de retorno: {e}")
        return None

    for element in return_elements:
        try:
            departure_time = element.find_element(By.CSS_SELECTOR, '[data-testid$="-origin"] .flightInfostyle__TextHourFlight-sc__sc-169zitd-4').text
            departure_city = element.find_element(By.CSS_SELECTOR, '[data-testid$="-origin"] .flightInfostyle__TextIATA-sc__sc-169zitd-5').text
            arrival_time = element.find_element(By.CSS_SELECTOR, '[data-testid$="-destination"] .flightInfostyle__TextHourFlight-sc__sc-169zitd-4').text
            arrival_city = element.find_element(By.CSS_SELECTOR, '[data-testid$="-destination"] .flightInfostyle__TextIATA-sc__sc-169zitd-5').text
            price_text = element.find_element(By.CSS_SELECTOR, '[data-testid$="-amount"] .displayCurrencystyle__CurrencyAmount-sc__sc-hel5vp-2').text

            price = parse_price(price_text, 'LATAM')
            flights['return'].append({
                'date': return_date,
                'departure_time': departure_time,
                'departure_city': departure_city,
                'arrival_time': arrival_time,
                'arrival_city': arrival_city,
                'price': price
            })
        except Exception as e:
            print(f"Error al extraer datos de retorno de LATAM: {e}")

    return {
        'airline': 'LATAM',
        'outbound': flights['outbound'],
        'return': flights['return']
    }
