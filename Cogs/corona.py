import discord
from discord.ext import commands
from functions import get_overall_status , get_country_infections , get_percentage , NotFound 
import matplotlib.pyplot as plt
from datetime import datetime
plt.rcParams.update({'text.color' : "white",'axes.labelcolor' : "white"})
class Corona(commands.Cog):
	"""Corona cog"""
	def __init__(self, client):
		self.client = client
		self.info = {
		'footer_text' : 'Made possible by discord.py and Jake. {}',
		'colors' : {
		'red' : discord.Colour(value=16730698),
		'light_red' : '#ff5151',
		'light_green' : '#76ff46'
		}
		}
		self.errors = ['Not found']
	@commands.command(name='inf',brief='Get current infections worldwide or by country identifier' , description='Get current infections worldwide or by country name .  You can view the **country_list** command for the countries that you search for.',usage='infections [country_name]',client_permissions=['EMBED_LINKS','SEND_MESSAGES'],user_permissions=None)
	@commands.bot_has_permissions(**{'send_messages':True,'embed_links':True})
	async def infections(self,ctx,*,country_identifier:str or int=None):
		if country_identifier == None:
			data = get_overall_status()
			inf_embed = discord.Embed(title='Infections worldwide',color=self.info['colors']['red'])
			#inf_embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
			#inf_embed.set_footer(text=self.info['footer_text'].format('Last updated in {}'.format(datetime.now())))
			inf_embed.set_thumbnail(url=self.client.user.avatar_url)
			for elem in data:
				string = '{} ({} %)'.format(data[elem],get_percentage(data[elem],data['total']))
				inf_embed.add_field(name='{}:'.format(elem.capitalize().replace('_',' ')),value='`{}`'.format(string if elem in ['deaths','active','recovered'] else data[elem]))
			plt.pie([data['deaths'],data['recovered'],data['critical_condition']],explode=(0.1,0,0),colors=[self.info['colors']['light_red'],self.info['colors']['light_green'],'orange'],labels=['Deaths','Recovered' , 'Serious'],autopct='%1.1f%%',shadow=True)
			plt.savefig(transparent=True,fname='world_pie.png',bbox_inches='tight')
			world_pie = discord.File("world_pie.png",filename='world_pie.png')
			plt.clf()
			await ctx.send(file=world_pie)
			await ctx.send(embed=inf_embed)
		else:
			try:
				data = get_country_infections(country_identifier)
				inf_embed = discord.Embed(title='Infections in {}'.format(country_identifier),color=self.info['colors']['red'])
				#inf_embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
				#inf_embed.set_footer(text=self.info['footer_text'].format('Last updated in {}'.format(datetime.now())))
				inf_embed.set_thumbnail(url=self.client.user.avatar_url)
				for elem in data:
					inf_embed.add_field(name='{}:'.format(elem.capitalize().replace('_',' ')),value='`{}`'.format('{} ({} %)'.format(data[elem],get_percentage(data[elem],data['cases'])) if elem in ['deaths','active','recovered' , 'serious', 'mild_condition', 'critical_condition'] else data[elem]))
				plt.pie([data['deaths'],data['recovered'],data['active']],explode=(0,0,0),colors=[self.info['colors']['light_red'],self.info['colors']['light_green'],'#ffd73d'],labels=['Deaths','Recovered','Active cases' ],autopct='%1.1f%%',shadow=True)
				plt.savefig(transparent=True,fname='country_pie.png',bbox_inches='tight')
				country_pie = discord.File('country_pie.png',filename='country_pie.png')
				plt.clf()
				await ctx.send(file=country_pie)
				await ctx.send(embed=inf_embed)
			except NotFound as e:
				err_embed = discord.Embed(title='Error : {}'.format(self.errors[0]),color=self.info['colors']['red'],description=f'**{e}**')
				#err_embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
				#err_embed.set_footer(text=self.info['footer_text'].format('Last updated in {}'.format(datetime.now())))
				await ctx.send(embed=err_embed)
	#@commands.command(brief='Gets the list of infected countries that you can search for in the (infections) command.',description='Gets the list of infected countries that you can search for in the (infections) command.',usage='countries')
def setup(client):
	client.add_cog(Corona(client))
