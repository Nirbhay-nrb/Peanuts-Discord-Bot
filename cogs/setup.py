from discord.ext import commands
import discord
import asyncio
import json

file = './channels.txt'

def get_server_list():
    with open(file,'r') as f:
        x = f.read()
        try:
            server_channel = json.loads(x)
            return server_channel
        except:
            print('File is empty')

def add_to_file(server_channel):
    with open(file,'w') as f:
        json.dump(server_channel,f)

def add_server(guild_id , channel_id):
    server_channel = get_server_list()
    server_channel[guild_id] = channel_id
    add_to_file(server_channel)

class Setup(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def setup(self,ctx):
        # get guild id
        guild_id = ctx.guild.id
        # getting a list of channels
        channels = ctx.guild.text_channels
        list_of_channels = []
        for channel in channels:
            if channel.permissions_for(ctx.guild.me).send_messages:
                list_of_channels.append(channel)
        # embed
        embed = discord.Embed(title="Setup", description="Please select a channel to send messages to")
        count = 1
        for channel in list_of_channels:
            embed.add_field(name= str(count) +". " + channel.name, value=channel.id, inline=False)
            count += 1
        # send embed
        await ctx.send(embed=embed)

        # getting a response from the user
        def check(reply_user):
            return reply_user.author == ctx.author and reply_user.channel == ctx.channel

        # timeout error
        try:
            msg = await self.bot.wait_for('message',check=check, timeout=10) # timeout for 10 seconds
        except asyncio.TimeoutError:
            await ctx.send('Sorry, you didn\'t reply in time!')
            return
        
        # proceeding further according the response
        try:
            if int(msg.content) > len(list_of_channels) or int(msg.content) <= 0:
                await ctx.send('Invalid response! Please try again')
            else:
                channel_id = list_of_channels[int(msg.content)-1].id
                add_server(guild_id,channel_id)
                c = list_of_channels[int(msg.content)-1]
                await c.send('Get ready for daily comics!')
        except:
            await ctx.send('Invalid response! Please try again')


def setup(client):
    client.add_cog(Setup(client))