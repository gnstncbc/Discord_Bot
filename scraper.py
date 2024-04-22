# scraper.py

import requests
from bs4 import BeautifulSoup

async def scrape_trendyol():
    url = 'https://www.trendyol.com/sr?q=Tuberose%203%27l%C3%BC%20Kokulu%20Kese%20%C5%9Eeffaf&qt=Tuberose%203%27l%C3%BC%20Kokulu%20Kese%20%C5%9Eeffaf&st=Tuberose%203%27l%C3%BC%20Kokulu%20Kese%20%C5%9Eeffaf&os=1'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    price_elements = soup.find_all('div', class_='prc-box-dscntd')
    name_elements = soup.find_all('div', class_='prdct-desc-cntnr')

    new_data = []
    if len(price_elements) == len(name_elements):
        for price_element, name_element in zip(price_elements, name_elements):
            price = price_element.text.strip()
            spans = name_element.find_all('span')
            if len(spans) >= 2:
                brand = spans[0].text.strip()
                product_name = spans[1].text.strip()
                new_data.append((product_name, brand, price))
    return new_data
