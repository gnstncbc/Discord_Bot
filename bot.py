import discord
from discord.ext import tasks, commands
import config
import commands as cmd
import scraper
import logger
import beautifier
import price_checker

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='?', intents=intents)
        self.channel_id = config.Config.CHANNEL_ID

    async def on_ready(self):
        print(f'{self.user} is now running!')
        self.send_trendyol_fiyat.start()

    async def on_message(self, message):
        if message.author == self.user:
            return
        await cmd.print_message(self, message)
        await cmd.handle_message(self, message)

    @tasks.loop(seconds=1.0, count = 1)
    async def send_logs(self):
        channel = self.get_channel(self.channel_id)
        logs = await logger.return_logs()
        await beautifier.log_beautify_and_send(logs,channel)

    @tasks.loop(minutes=120.0)
    async def send_trendyol_fiyat(self):
        change_detected = False
        channel = self.get_channel(self.channel_id)
        data = await scraper.scrape_trendyol()
        await logger.log_data(data, channel)
        logs = await logger.return_logs()

        if len(logs) < 2:
            print("logs is empty, probably first call")
            logs.at[0, 'Price'] = '44 TL'
            await beautifier.trendyol_beautify_and_send(data,channel,change_detected)
        else:
            changed_rows_df = await price_checker.check_price(data,logs)
            
            if changed_rows_df.empty:
                print("No changes detected.")
            else:
                change_detected = True
                await beautifier.trendyol_beautify_and_send(changed_rows_df,channel,change_detected)

bot = MyBot()
bot.run(config.Config.TOKEN)