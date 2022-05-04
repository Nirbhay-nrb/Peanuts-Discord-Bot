import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# getting data from .env file
token = os.environ.get('TOKEN')
prefix = os.environ.get('PREFIX')

# initialising the bot
client = commands.Bot(command_prefix=prefix,help_command=None)

# list of all cogs
cogs=['cogs.random','cogs.setup','cogs.help','cogs.periodic']

# loading the cogs
for cog in cogs:
    client.load_extension(cog)

# what to do when the bot switches on
@client.event
async def on_ready():
    print('Bot switched on : {}'.format(client.user.name))
    print('Bot id : {}'.format(client.user.id))

# sending a message when a server is joined
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(f'Please run the command ``{prefix}setup`` to fix a channel for sending daily comics')
            break

client.run(token)