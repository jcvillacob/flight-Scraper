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
    time.sleep(10)

    flights = {'outbound': [], 'return': []}

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

            price = parse_price(price_text, 'LATAM')

            flights['outbound'].append({
                'departure_time': departure_time,
                'departure_city': departure_city,
                'arrival_time': arrival_time,
                'arrival_city': arrival_city,
                'price': price
            })
        except Exception as e:
            print(f"Error extracting outbound data from LATAM: {e}")

    try:
        flight_elements[0].click()
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking on outbound flight element: {e}")

    try:
        driver.find_element(By.XPATH,
                            '/html/body/div[1]/div[1]/main/div/div/div/div/ol/li[1]/div/ol/li[1]/div/div[3]/div[3]/button').click()
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking on first button: {e}")

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                    '/html/body/div[1]/div[1]/main/div/div/div/div/ol/li[1]/div/ol/li[1]/div/div[3]/div[3]/dialog/div/div[1]/ul/li[1]/div/div[3]/div[2]/button'))).click()
        time.sleep(8)
    except Exception as e:
        print(f"Error clicking on second button: {e}")

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

            price = parse_price(price_text, 'LATAM')

            flights['return'].append({
                'departure_time': departure_time,
                'departure_city': departure_city,
                'arrival_time': arrival_time,
                'arrival_city': arrival_city,
                'price': price
            })
        except Exception as e:
            print(f"Error extracting return data from LATAM: {e}")

    return {
        'airline': 'LATAM',
        'outbound': flights['outbound'],
        'return': flights['return']
    }
