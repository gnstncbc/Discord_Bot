# logger.py

import datetime

async def log_data(data, channel):
    formatted_local_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for product_name, brand, price in data:
        log_message = f"Marka : {brand}\nÜrün : {product_name}\nFiyat : {price}\nSorgu Zamanı : {formatted_local_datetime}\n----------------"
        await channel.send(log_message)

    total_queries = len(data)
    total_queries_message = f"**Toplam sorgu sayısı: {total_queries}**"
    await channel.send(total_queries_message)
