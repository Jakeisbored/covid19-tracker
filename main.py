import discord
from discord.ext import commands
import sys, traceback


def get_prefix(client, message):
    prefixes = ['covid ', 'c!']
    return commands.when_mentioned_or(*prefixes)(client, message)
initial_extensions = ['Cogs.corona']

client = commands.Bot(command_prefix=get_prefix, description='A covid 19 tracking bot')
client.remove_command('help')
# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

@client.event
async def on_ready():
    print(f'\n\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}\n')
    await client.change_presence(game=discord.Game(name='latest covid19 news', type=2))
    print(f'Successfully logged in and booted...!')

client.run('NTc2MTEzNjg5MzI1NzMxODky.Xm96Aw.TcQZx4WcGY3B_dXf8Fd4GMA3nRo')
