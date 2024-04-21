import discord
import responses
from discord.ext import tasks, commands
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import random

# Initialize an empty DataFrame to store product data
df = pd.DataFrame(columns=['Product', 'Brand', 'Price'])

# Send messages
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = ''
    utc = datetime.timezone.utc
    time = datetime.time(hour=00, minute=32, tzinfo=utc)

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        send_fiyat.start()

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f"{username} said: '{user_message}' ({channel})")
        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
        if user_message == 'eyv':
            raise SystemExit
        if user_message == 'fiyat':
            send_fiyat.start()

    @tasks.loop(seconds=5.0, count=5)
    async def auto_send_message():
        kanal = client.get_channel(1231371511798042727)
        await kanal.send('slm')

    @tasks.loop(seconds=5.0, count=1)
    async def send_fiyat():
        global df  # Declare df as global to access and modify it
        print("çalıştım")
        kanal = client.get_channel(1231371511798042727)
        random_number = random.randint(1,2)
        print(random_number)
        if random_number == 1:
            url = 'https://www.trendyol.com/sr?q=English%20Home%20Tuberose%203%27l%C3%BC%20Kokulu%20Kese%20%C5%9Eeffaf&qt=English%20Home%20Tuberose%203%27l%C3%BC%20Kokulu%20Kese%20%C5%9Eeffaf&st=English%20Home%20Tuberose%203%27l%C3%BC%20Kokulu%20Kese%20%C5%9Eeffaf&os=1'
        else:
            url = 'https://www.trendyol.com/sr?q=English%20Home%20tobacco%203%27l%C3%BC%20Kokulu%20Kese%20%C5%9Eeffaf&qt=English%20Home%20tobacco%203%27l%C3%BC%20Kokulu%20Kese%20%C5%9Eeffaf&st=English%20Home%20tobacco%203%27l%C3%BC%20Kokulu%20Kese%20%C5%9Eeffaf&os=1'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_elements = soup.find_all('div', class_='prc-box-dscntd')
        name_elements = soup.find_all('div', class_='prdct-desc-cntnr')

        new_data = []  # Store new data temporarily
        if len(price_elements) == len(name_elements):
            for price_element, name_element in zip(price_elements, name_elements):
                price = price_element.text.strip()
                spans = name_element.find_all('span')
                if len(spans) >= 2:
                    brand = spans[0].text.strip()
                    product_name = spans[1].text.strip()
                    new_data.append((product_name, brand, price))
        else:
            print("Error: Number of prices and names do not match.")

        new_df = pd.DataFrame(new_data, columns=['Product', 'Brand', 'Price'])

        if not df.empty and not new_df.equals(df):  # Check if the new data is different from the previous one
            # Update the DataFrame with new data
            df = new_df
            message_to_send = "Data has been updated:\n" + df.to_string(index=False)
            await kanal.send(message_to_send)
        elif df.empty:  # If DataFrame is empty, populate it with new data
            df = new_df
            message_to_send = "Initial data:\n" + df.to_string(index=False)
            await kanal.send(message_to_send)

    client.run(TOKEN)

run_discord_bot()
