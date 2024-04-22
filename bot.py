# bot.py

import discord
from discord.ext import tasks, commands
import config
import commands as cmd
import scraper
import logger

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='?', intents=intents)

    async def on_ready(self):
        print(f'{self.user} is now running!')
        self.send_fiyat.start()

    async def on_message(self, message):
        if message.author == self.user:
            return
        await cmd.handle_message(message, self)

    @tasks.loop(minutes=120.0)
    async def send_fiyat(self):
        channel_id = config.Config.CHANNEL_ID
        channel = self.get_channel(channel_id)
        if channel is None:
            print("Channel not found!")
            return
        data = await scraper.scrape_trendyol()
        await logger.log_data(data, channel)

bot = MyBot()
bot.run(config.Config.TOKEN)
