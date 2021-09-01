# bot.py
import os

import discord
from dotenv import load_dotenv, main
from discord.ext import tasks
import io
import aiohttp

from project.scrapper import Scrapper

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
target_channel_id = 882678542759002152

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@tasks.loop(seconds=5.0)
async def printer():

    channel = client.get_channel(882678542759002152)
    if channel:
        scrapper = Scrapper()
        figures = scrapper.run()
        for figure in figures:
            print(figure.image)
            await channel.send(f"\n{figure.name} - {figure.price}")
            await channel.send(f"\n{figure.url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(figure.image) as resp:
                    if resp.status != 200:
                        return await channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await channel.send(file=discord.File(data, f'{figure.name}.jpg'))
    else:
        print('channel no encontrado')

printer.start()

client.run(TOKEN)