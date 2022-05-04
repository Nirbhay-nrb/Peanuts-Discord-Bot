import discord
from discord.ext import commands
import os

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def help(self,ctx):
        # a dictionary of all the commands with there use
        prefix = os.environ.get('PREFIX')
        commands = {f'``{prefix}setup``' : 'Setup a channel to send daily comics',
                f'```{prefix}random```' : 'Get a random Peanuts comic',
                f'```{prefix}help```' : 'Displays this message',
                }
        # embedding the dictionary in embed format
        embed = discord.Embed(title='List of commands: ',description='These are the commands to use with this bot')
        count = 1
        for command in commands:
            embed.add_field(name=str(count)+'. '+command, value=commands[command],inline=False)
            count += 1
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
