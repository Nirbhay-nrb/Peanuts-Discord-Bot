from discord.ext import commands
from discord.ext import tasks
import requests
import discord
from bs4 import BeautifulSoup
from datetime import date
import json

file = './channels.txt'

def todays_comic():
    todays_date = date.today()
    year = todays_date.year
    month = todays_date.month
    day = todays_date.day
    s = f'{year}/{month}/{day}'
    url = f'https://www.gocomics.com/peanuts/{s}'
    print('Website link =',url)
    html = requests.get(url)
    soup = BeautifulSoup(html.text , 'html.parser')
    tag = soup('img',class_='lazyload img-fluid')[1]
    imageUrl = tag.get('src',None)
    print('image Url = ',imageUrl)
    return (imageUrl , s)

def get_server_list():
    server_channel = {}
    with open(file,'r') as f:
        x = f.read()
        try:
            server_channel = json.loads(x)
            print(server_channel)
            return server_channel
        except:
            print('File is empty')
            s = {}
            return s

class Periodic(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        task = self.sendComic.start()

    @tasks.loop(hours=24)
    async def sendComic(self):
        # getting todays comic
        x = todays_comic()
        url = x[0]
        date = x[1]
        embed = discord.Embed(title=f'Peanuts on {date}')
        embed.set_image(url=url)
        # getting the list of all servers and channels to send the message
        server_channel = get_server_list()
        if server_channel is not None:
            for guild_id,channel_id in server_channel.items():
                # sending message to each channel
                try:
                    channel = await self.bot.fetch_channel(channel_id)
                    await channel.send(embed=embed)
                except:
                    print('Couldnt send message to this channel')
                    continue

def setup(client):
    client.add_cog(Periodic(client))