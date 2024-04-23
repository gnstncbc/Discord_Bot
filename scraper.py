# scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import config

async def scrape_trendyol():
    url = config.Config.TRENDYOL_URL

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    price_elements = soup.find_all('div', class_='prc-box-dscntd')
    name_elements = soup.find_all('div', class_='prdct-desc-cntnr')

    data = []
    if len(price_elements) == len(name_elements):
        for price_element, name_element in zip(price_elements, name_elements):
            price = price_element.text.strip()
            spans = name_element.find_all('span')
            if len(spans) >= 2:
                brand = spans[0].text.strip()
                product_name = spans[1].text.strip()
                data.append({'Product': product_name, 'Brand': brand, 'Price': price})

    df = pd.DataFrame(data)
    return df
