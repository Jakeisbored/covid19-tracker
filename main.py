# Modules
import os
import discord
from discord.ext import commands
# Prefix getter
def get_prefix(client,message):
	prefixes = ['c!','covid ']
	return commands.when_mentioned_or(*prefixes)(client,message)
# Client and removing the default help
client= commands.Bot(description='A COVID19 tracking bot !',command_prefix=get_prefix)
client.remove_command('help')
# Importing the cogs
cogs = ['Cogs.corona','Cogs.util']
for cog in cogs:
	if __name__ == '__main__':
		client.load_extension(cog)
# Ready event
@client.event
async def on_ready():
	print(f'{client.user.name}#{client.user.discriminator} is up and runing')
	await client.change_presence(activity=discord.Game('c!help'))
# Login
client.run(os.environ['token'])
