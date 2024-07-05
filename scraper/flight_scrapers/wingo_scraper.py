from selenium.webdriver.common.by import By
from scraper.utils import parse_price
import time

def get_wingo_flight_data(driver, origin, destination, departure_date, return_date):
    url_template = 'https://booking.wingo.com/en/search/{origin}/{destination}/{departure_date}/{return_date}/1/0/0/0/COP/0/0'
    url = url_template.format(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date
    )

    driver.get(url)
    time.sleep(10)

    flights = {'outbound': [], 'return': []}

    outbound_elements = driver.find_elements(By.CSS_SELECTOR, '#departure-fligth [id^="flight-"]')
    for element in outbound_elements:
        try:
            departure_time = element.find_element(By.CSS_SELECTOR, '.col-4.text-start p.font-gray.font-weight-bold').text
            departure_city = element.find_element(By.CSS_SELECTOR, '.col-4.text-start p.date-info-airport').text.split(' ')[0]
            arrival_time = element.find_element(By.CSS_SELECTOR, '.col-4.text-end p.font-gray.font-weight-bold').text
            arrival_city = element.find_element(By.CSS_SELECTOR, '.col-4.text-end p.date-info-airport').text.split(' ')[0]
            price_text = element.find_element(By.CSS_SELECTOR, '.col-9 p.font-weight-bold').text

            price = parse_price(price_text, 'Wingo')

            flights['outbound'].append({
                'date': departure_date,
                'departure_time': departure_time,
                'departure_city': departure_city,
                'arrival_time': arrival_time,
                'arrival_city': arrival_city,
                'price': price
            })
        except Exception as e:
            print(f"Error extracting outbound data from Wingo: {e}")

    return_elements = driver.find_elements(By.CSS_SELECTOR, '#return-fligth [id^="flight-"]')
    for element in return_elements:
        try:
            departure_time = element.find_element(By.CSS_SELECTOR, '.col-4.text-start p.font-gray.font-weight-bold').text
            departure_city = element.find_element(By.CSS_SELECTOR, '.col-4.text-start p.date-info-airport').text.split(' ')[0]
            arrival_time = element.find_element(By.CSS_SELECTOR, '.col-4.text-end p.font-gray.font-weight-bold').text
            arrival_city = element.find_element(By.CSS_SELECTOR, '.col-4.text-end p.date-info-airport').text.split(' ')[0]
            price_text = element.find_element(By.CSS_SELECTOR, '.col-9 p.font-weight-bold').text

            price = parse_price(price_text, 'Wingo')

            flights['return'].append({
                'date': return_date,
                'departure_time': departure_time,
                'departure_city': departure_city,
                'arrival_time': arrival_time,
                'arrival_city': arrival_city,
                'price': price
            })
        except Exception as e:
            print(f"Error extracting return data from Wingo: {e}")

    return {
        'airline': 'Wingo',
        'outbound': flights['outbound'],
        'return': flights['return']
    }
