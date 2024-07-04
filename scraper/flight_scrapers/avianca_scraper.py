from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.utils import parse_price
import time

def get_avianca_flight_data(driver, origin, destination, departure_date, return_date):
    url_template = 'https://www.avianca.com/es/booking/select/?origin1={origin}&destination1={destination}&departure1={departure_date}&adt1=1&tng1=0&chd1=0&inf1=0&origin2={destination}&destination2={origin}&departure2={return_date}&adt2=1&tng2=0&chd2=0&inf2=0&currency=COP&posCode=CO'
    url = url_template.format(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date
    )

    driver.get(url)
    time.sleep(10)

    flights = {'outbound': [], 'return': []}

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking on cookies button: {e}")

    outbound_elements = driver.find_elements(By.CSS_SELECTOR, '.journey_inner')
    for element in outbound_elements:
        try:
            departure_time = element.find_element(By.CSS_SELECTOR, '.journey-schedule_time-departure').text.strip()
            arrival_time = element.find_element(By.CSS_SELECTOR, '.journey-schedule_time-return').text.strip()
            departure_city = element.find_element(By.CSS_SELECTOR, '.journey-schedule_station-departure .journey-schedule_station_code').text.strip()
            arrival_city = element.find_element(By.CSS_SELECTOR, '.journey-schedule_station-return .journey-schedule_station_code').text.strip()
            price_text = element.find_element(By.CSS_SELECTOR, '.journey_price_button .price').text.strip()

            if departure_time and arrival_time and departure_city and arrival_city and price_text:
                price = parse_price(price_text, 'Avianca')

                flights['outbound'].append({
                    'departure_time': departure_time,
                    'departure_city': departure_city,
                    'arrival_time': arrival_time,
                    'arrival_city': arrival_city,
                    'price': price
                })
        except Exception as e:
            print(f"Error extracting outbound data from Avianca: {e}")

    try:
        outbound_elements[0].click()
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking on outbound flight element: {e}")

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div/div[2]/div/div/journey-availability-select-container/div/price-journey-select-custom/div[2]/div[2]/div[1]/journey-control-custom/div/div/div[2]/div/div/div/div[1]/fare-control/div[2]/div[3]/button'))).click()
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking on first button: {e}")

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'cro-no-accept-upsell-button'))).click()
        time.sleep(8)
    except Exception as e:
        print(f"Error clicking on second button: {e}")

    return_elements = driver.find_elements(By.CSS_SELECTOR, '.journey_inner')
    for element in return_elements:
        try:
            departure_time = element.find_element(By.CSS_SELECTOR, '.journey-schedule_time-departure').text.strip()
            arrival_time = element.find_element(By.CSS_SELECTOR, '.journey-schedule_time-return').text.strip()
            departure_city = element.find_element(By.CSS_SELECTOR, '.journey-schedule_station-departure .journey-schedule_station_code').text.strip()
            arrival_city = element.find_element(By.CSS_SELECTOR, '.journey-schedule_station-return .journey-schedule_station_code').text.strip()
            price_text = element.find_element(By.CSS_SELECTOR, '.journey_price_button .price').text.strip()

            if departure_time and arrival_time and departure_city and arrival_city and price_text:
                price = parse_price(price_text, 'Avianca')

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
        'airline': 'Avianca',
        'outbound': flights['outbound'],
        'return': flights['return']
    }
