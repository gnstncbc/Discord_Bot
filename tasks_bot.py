import discord
from discord.ext import tasks, commands
import bot

@tasks.loop(seconds=5.0, count=5)
async def auto_send_message_tasks(client):
    kanal = client.get_channel(1231371511798042727)
    await kanal.send('slm')