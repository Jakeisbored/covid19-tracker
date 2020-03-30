import discord
from discord.ext import commands
from functions import info , get_overall_status , get_country_infections , get_percentage , NotFound , get_country_list , construct_embed
import matplotlib.pyplot as plt
plt.rcParams.update({'text.color' : "white",'axes.labelcolor' : "white"})
class Corona(commands.Cog):
	"""Corona cog"""
	def __init__(self, client):
		self.client = client
		self.info = info
		self.errors = ['Not found']

	@commands.command(name='inf',brief='Get current infections worldwide or by country identifier' , description='Get current infections worldwide or by country name .  You can view the **country_list** command for the countries that you search for.',usage='infections [country_name]',client_permissions=['EMBED_LINKS','SEND_MESSAGES'],user_permissions=None)
	@commands.bot_has_permissions(**{'send_messages':True,'embed_links':True})
	async def infections(self,ctx,*,country_identifier:str or int=None):
		if country_identifier == None:
			data = get_overall_status()
			plt.pie([data['deaths'],data['recovered'],data['critical_condition']],explode=(0.1,0,0),colors=[self.info['colors']['light_red'],self.info['colors']['light_green'],'orange'],labels=['Deaths','Recovered' , 'Serious'],autopct='%1.1f%%',shadow=True)
			plt.savefig(transparent=True,fname='world_pie.png',bbox_inches='tight')
			world_pie = discord.File("world_pie.png",filename='world_pie.png')
			plt.clf()
			await ctx.send(embed=construct_embed(discord.Embed,title='Infections worldwide',fields=[{'name' : '{}:'.format(elem.capitalize().replace('_',' ')) , 'value' : '`{}`'.format('{} ({} %)'.format(data[elem],get_percentage(data[elem],data['total'])) if elem in ['deaths','active','recovered'] else data[elem]) , 'inline' : True} for elem in data]))
			await ctx.send(file=world_pie)
		else:
			try:
				data = get_country_infections(country_identifier)
				plt.pie([data['deaths'],data['recovered'],data['active']],explode=(0,0,0),colors=[self.info['colors']['light_red'],self.info['colors']['light_green'],'#ffd73d'],labels=['Deaths','Recovered','Active cases' ],autopct='%1.1f%%',shadow=True)
				plt.savefig(transparent=True,fname='country_pie.png',bbox_inches='tight')
				country_pie = discord.File('country_pie.png',filename='country_pie.png')
				plt.clf()
				await ctx.send(embed=construct_embed(discord.Embed,title='Infections in {}'.format(country_identifier),fields=[{'name' : '{}:'.format(elem.capitalize().replace('_',' ')) , 'value' : '{} ({} %)'.format(data[elem],get_percentage(data[elem],data['cases'])) if elem in ['deaths','active','recovered' , 'serious', 'mild_condition', 'critical_condition'] else data[elem] , 'inline' : True} for elem in data]))
				await ctx.send(file=country_pie)
			except NotFound as e:
				await ctx.send(embed=construct_embed(discord.Embed,'Error : {}'.format(self.errors[0]),f'**{e}**'))
	@commands.command(brief='Gets the list of infected countries that you can search for in the (infections) command.',description='Gets the list of infected countries that you can search for in the (infections) command.',usage='countries')
	async def countries(self,ctx ,*,country:str=None):
		sep = ' - '
		if country == None:
			await ctx.send(embed=construct_embed(discord.Embed,'Country list :','`{}` \n A total of **{}** countries'.format(sep.join(get_country_list())[:2000],len(get_country_list()))))
		else:
			search_results = []
			for e in get_country_list():
				if country.lower() in e.lower():
					search_results.append(e)
			await ctx.send(embed=construct_embed(discord.Embed,'Search results :','`{}` \n A total of **{}** countries'.format(sep.join(search_results)[:2000],len(search_results))))
def setup(client):
	client.add_cog(Corona(client))
