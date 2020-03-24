import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
main_endpoint = 'https://www.worldometers.info/coronavirus/{}'
cr = "Powered by discord.py and Jake's brain"
def get_stats(type):
  if(type == 'deaths'):
    url = main_endpoint.format('coronavirus-death-toll/')
    HTML = requests.get(url).content
    soup = BeautifulSoup(HTML,'html.parser')
    data = {
      'overall' : soup.select_one('p').getText(),
      'death_log' : {
        'total' : {

        },
        'daily' : {

        }
      }
    }
    table_children = soup.find_all('tbody')[0].find_all('tr')
    for child in table_children:
      for index,td in enumerate(child.find_all('td')):
        if index == 0:
          key = td.getText().replace('\xa0','').strip()
          data['death_log']['total'][key] = {}
        elif index == 1:
          data['death_log']['total'][key]['total_deaths'] = td.getText()
        elif index == 2:
          data['death_log']['total'][key]['total_change'] = td.getText()
        elif index == 3:
          data['death_log']['total'][key]['total_change_percentage'] = td.getText()
    table_children1 = soup.find_all('tbody')[1].find_all('tr')
    for child in table_children1:
      for index,td in enumerate(child.find_all('td')):
        if index == 0:
          key = td.getText().replace('\xa0','').strip()
          data['death_log']['daily'][key] = {}
        elif index == 1:
          data['death_log']['daily'][key]['total_deaths'] = td.getText()
        elif index == 2:
          data['death_log']['daily'][key]['total_change'] = td.getText()
        elif index == 3:
          data['death_log']['daily'][key]['total_change_percentage'] = td.getText()
    return data
def get_latest_info():
  url = main_endpoint.format('')
  HTML = requests.get(url).content
  soup = BeautifulSoup(HTML,'html.parser')
  from datetime import datetime
  x = 'newsdate'+datetime.today().strftime('%Y-%m-%d')
  info = soup.find('div' , {"id":x}).getText()
  return {
    'info' : info,
    'date' : datetime.today().strftime('%Y-%m-%d')
  }
def get_infections():
  url = main_endpoint.format('#countries')
  HTML = requests.get(url).content
  soup = BeautifulSoup(HTML,'html.parser')
  table_children = soup.find('tbody').find_all("tr")
  infections = {}
  for child in table_children :
    for index,td in enumerate(child.find_all('td')):
      if(index == 0):
        country_key = td.getText().strip()
        infections[country_key] = {
            'total_cases' : '',
            'new_cases' : '',
            'total_deaths' : '',
            'new_deaths' : '',
            'total_recovered' : '',
            'active_cases' : '',
            'critical_cases' : ''
        }
      elif (index == 1):
        infections[country_key]['total_cases'] = td.getText()
      elif (index == 2):
          infections[country_key]['new_cases'] = td.getText()
      elif (index == 3):
          infections[country_key]['total_deaths'] = td.getText()
      elif (index == 4):
          infections[country_key]['new_deaths'] = td.getText()
      elif (index == 5):
          infections[country_key]['total_recovered'] = td.getText()
      elif (index == 6):
          infections[country_key]['active_cases'] = td.getText()
      elif (index == 7):
          infections[country_key]['critical_cases'] = td.getText()
  return {
     'worldwide_cases' : {
        'total_cases' : {
          'infected' : soup.select('#maincounter-wrap > div > span')[0].getText(),
          'deaths' : soup.select('#maincounter-wrap > div > span')[1].getText(),
          'cured' : soup.select('#maincounter-wrap > div > span')[2].getText(),
          'active_cases' : {
            'mid_condition' : soup.select_one('div.number-table-main').getText(),
            'critical_condition' : soup.select_one('div.panel_front > div:nth-child(3) > div:nth-child(2) > span').getText()
          },
          'closed_cases' : {
            'recovered' : soup.select_one(' div.panel_front > div:nth-child(3) > div:nth-child(1) > span').getText(),
            'deaths' : soup.select_one('div.panel_front > div:nth-child(3) > div:nth-child(2) > span').getText()
          }
        }
      },
      'infections' : infections
    }
def get_infections_by_name(country_name=None):
  if(country_name == None):
    raise Exception('You must specify a country name')
  response = get_infections()
  try:
    
    return {
      country_name : response['infections'][country_name]
      }
  except Exception:
    raise Exception('Seems like you entered a wrong country name')
def get_infected_countries():
  data = get_infections()
  countries = []
  for country in data['infections']:
    countries.append(country)
  return countries
def check_length(query , extra=None , special=False):
  if not query.replace(' ',''):
    return 'None'
  else:
    if extra == None:
      return query
    else:
      if special == True:
        return query + ' ({} % addition rate)'.format(extra)
      else:
        return query + ' ({} % )'.format(extra)
class Corona(commands.Cog):
  def __init__(self, client):
     self.client = client
     self.info = {
	'footer_text' : f'Made by',
	'colors' : {
	 'red' : discord.Colour(value=16730698),
	 'light_red' : '#ff5151',
	 'light_green' : '#76ff46'
	           }
	}
  @commands.command(brief='Get current infections worldwide or by country identifier' , description='Get current infections worldwide or by country identifier , a country identifier is either a country code (DZ) , id (1) or a country name (Algeria) . Ids and country codes can be viewed in the **country_key** command.',usage='infections [country_identifier]')
  async def test(self,ctx,country_identifier:str or int=None):
    data = get_world_infections()
    inf_embed = discord.Embed(title='Infections worldwide',color=self.info['colors']['red'])
    inf_embed.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
	#inf_embed.set_footer(text=f'Issued by {ctx.message.author.user.name}',icon_url=ctx.message.author.user.avatar_url)
    for elem in data['latest']:
       inf_embed.add_field(name=f'{elem}:',value='`{}`'.format(data['latest'][elem]) , inline=True)
    await ctx.send(embed=inf_embed)
  @commands.command(brief='Search for an arg in the infected countries',description='Search for an arg in the infected countries , if no arg is given the list of infected countries is returned' , usage='search_country [country_name]' , aliases=['sc','search'])
  async def search_country(self,ctx,search_args:str=None):
        sep = ' , '
        if (search_args == None):
          countries = get_infected_countries()
          countries.sort()
          embed = discord.Embed(title="Currently infected countries !" , description="**{} ...** \n **{}** total countries".format(sep.join(countries)[:2000],str(len(countries))),  color=discord.Colour(value=16730698))
          embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)      
          embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/686666564589846625/688494381027688480/caution-icon-png-14-original.png')
          await ctx.send(embed=embed)
          return
        else:
          countries = get_infected_countries()
          embed = discord.Embed(title="Searching for {}".format(search_args) ,  color=discord.Colour(value=16730698))
          embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/686666564589846625/688494381027688480/caution-icon-png-14-original.png')
          embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
          c = []
          for country in countries:
            if(search_args.lower() in country.lower()): 
              c.append(country)
          embed.description = '**{}** \n **{}** total results'.format('No results were found' if len(c)<1 else sep.join(c)[:2000],str(len(c)))
          await ctx.send(embed=embed) 
          return  
  @commands.command(brief='Get symptoms of COVID19',description='Get symptoms of COVID19' , usage='symptoms')
  async def symptoms(self,ctx):
      embed=discord.Embed(title="COVID19 Symptoms")
      embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
      embed.set_image(url='https://www.worldometers.info/img/coronavirus--symptoms-table-wang-jama-02072020-reduced.png')
      await ctx.send(embed=embed)
  @commands.command(brief='Get infections in a specific country',description='Get infections in a specific country , if no arg is given the world sum is returned',usage='infections [country_name]',aliases=['inf'])
  async def infections(self,ctx,country:str=None):
        if(country == None):
          results= get_infections()
          async with ctx.typing():
              import matplotlib.pyplot as plt
              plt.rcParams.update({'text.color' : "white",'axes.labelcolor' : "white"})
              labels = 'Deaths', 'Cured' , 'Mid condition'
              sizes = [int(results['worldwide_cases']['total_cases']['deaths'].replace(',','')),int(results['worldwide_cases']['total_cases']['cured'].replace(',','')),int(results['worldwide_cases']['total_cases']['active_cases']['mid_condition'].replace(',',''))]
              colors = ['#ff5151', '#76ff46' , 'orange']
              explode = (0, 0 , 0) 
              plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.0f%%')
              plt.axis('equal')
              plt.savefig('pie.png', bbox_inches='tight' , transparent=True)
              embed=discord.Embed(title="Infections worldwide",description='**Total** : {}  \n **Deaths** : {} \n **Cured** : {} \n **Active Cases** : \n > Mid Condition : {} \n > Critical condition : {}'.format(check_length(results['worldwide_cases']['total_cases']['infected']),check_length(results['worldwide_cases']['total_cases']['deaths'],format(int(results['worldwide_cases']['total_cases']['deaths'].replace(',',''))*100/int(results['worldwide_cases']['total_cases']['infected'].replace(',','')),'.2f') if not check_length(results['worldwide_cases']['total_cases']['deaths']) == 'None' else None),check_length(results['worldwide_cases']['total_cases']['cured'],format(int(results['worldwide_cases']['total_cases']['cured'].replace(',',''))*100/int(results['worldwide_cases']['total_cases']['infected'].replace(',','')),'.2f') if not check_length(results['worldwide_cases']['total_cases']['cured']) == 'None' else None),check_length(results['worldwide_cases']['total_cases']['active_cases']['mid_condition'],format(int(results['worldwide_cases']['total_cases']['active_cases']['mid_condition'].replace(',',''))*100/int(results['worldwide_cases']['total_cases']['infected'].replace(',','')),'.2f') if not check_length(results['worldwide_cases']['total_cases']['active_cases']['mid_condition']) == 'None' else None),check_length(results['worldwide_cases']['total_cases']['active_cases']['critical_condition'],format(int(results['worldwide_cases']['total_cases']['active_cases']['critical_condition'].replace(',',''))*100/int(results['worldwide_cases']['total_cases']['infected'].replace(',','')),'.2f') if not check_length(results['worldwide_cases']['total_cases']['active_cases']['critical_condition']) == 'None' else None)) ,  color=discord.Colour(value=16730698))
              embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
              embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/686666564589846625/688494381027688480/caution-icon-png-14-original.png')
              file = discord.File("pie.png", filename="image.png")
              embed.set_image(url="attachment://image.png")
              await ctx.send(embed=embed,file=file)
              plt.clf()
              return
        async with ctx.typing():
          c = []
          countries = get_infected_countries()
          for countr in countries:
              if(country.lower() in countr.lower()): 
                c.append(countr)
          country = country if len(c) < 1 else c[0]
          try:
            results = get_infections_by_name(country)
          except Exception as e:
            embed=discord.Embed(title="Error : Not found",description='**{}** was not found on the infected countries'.format(country),  color=discord.Colour(value=16730698))
            embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
            return
          import matplotlib.pyplot as plt
          plt.rcParams.update({'text.color' : "white",'axes.labelcolor' : "white"})
          labels = 'Deaths', 'Cured' , 'Critical condition'
          sizes = [int(results[country]['total_deaths'].replace(',','')),int(results[country]['total_recovered'].replace(',','')),int(results[country]['critical_cases'].replace(',',''))]
          colors = ['#ff5151', '#76ff46' , 'orange']
          explode = (0, 0 , 0) 
          plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.0f%%')
          plt.axis('equal')
          plt.savefig('country_pie.png', bbox_inches='tight' , transparent=True)
          embed=discord.Embed(title="Infections in {}".format(country),description='**Total** : {}  \n **Deaths** : {} \n **Cured** : {} \n **New cases** : {} \n **Critical cases** : {} \n **New deaths** : {} \n **Active cases** : {}'.format(check_length(results[country]['total_cases']),check_length(results[country]['total_deaths'],format(int(results[country]['total_deaths'].replace(',',''))*100/int(results[country]['total_cases'].replace(',','')),'.2f') if not check_length(results[country]['total_deaths']) == 'None' else None),check_length(results[country]['total_recovered'],format(int(results[country]['total_recovered'].replace(',',''))*100/int(results[country]['total_cases'].replace(',','')),'.2f') if not check_length(results[country]['total_recovered']) == 'None' else None),check_length(results[country]['new_cases'],format(int(results[country]['new_cases'].replace(',','').replace('+',''))*100/int(results[country]['total_cases'].replace(',','')),'.2f') if not check_length(results[country]['new_cases']) == 'None' else None,True),check_length(results[country]['critical_cases'],format(int(results[country]['critical_cases'].replace(',',''))*100/int(results[country]['total_cases'].replace(',','')),'.2f') if not check_length(results[country]['critical_cases']) == 'None' else None),check_length(results[country]['new_deaths'],format(int(results[country]['new_deaths'].replace(',','').replace('+',''))*100/int(results[country]['total_deaths'].replace(',','')),'.2f') if not check_length(results[country]['new_deaths']) == 'None' else None,True),check_length(results[country]['active_cases'],format(int(results[country]['active_cases'].replace(',',''))*100/int(results[country]['total_cases'].replace(',','')),'.2f') if not check_length(results[country]['active_cases']) == 'None' else None)) ,  color=discord.Colour(value=16730698))
          embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
          embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/686666564589846625/688494381027688480/caution-icon-png-14-original.png')
          file = discord.File("country_pie.png", filename="image.png")
          embed.set_image(url="attachment://image.png")
          await ctx.send(embed=embed,file=file)
          plt.clf()
          return

  @commands.command(brief='Get latest info about COVID19 (Updates every 24 hours)',description='Get latest info about COVID19 (Updates every 24 hours)', usage='latest_news' , aliases=['ln','latest_info','news'])
  async def latest_news(self,ctx):
        async with ctx.typing():
          out = [(get_latest_info()['info'][i:i+2048]) for i in range(0, len(get_latest_info()['info']), 2048)]
          for index,chunk in enumerate(out):
            if index == 0:
              embed=discord.Embed(title="COVID19 Latest news : {}".format(get_latest_info()['date']),description="**{}**".format(chunk.replace('\xa0','\n').replace('[source]','')),  color=discord.Colour(value=16730698))
              embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
              await ctx.send(embed=embed)
            else :
              embed=discord.Embed(description="**{}**".format(chunk.replace('\xa0','\n').replace('[source]','')),  color=discord.Colour(value=16730698))
              embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
              await ctx.send(embed=embed)
  @commands.command(usage='death_log <daily/total>[-text]',brief='Get the deaths log starting from the outbreak day',description='Get the deaths log starting from the outbreak day')
  async def death_log(self,ctx,type:str='None'):
      if type.replace('-text','') == 'daily':
        if type.endswith('-text'):
          async with ctx.typing():
            days = []
            msg = 'Daily deaths log :'
            for day in get_stats('deaths')['death_log']['daily'] :
              msg = msg + '\n **{}** : **__{}__** : **{}** \n'.format(day,get_stats('deaths')['death_log']['daily'][day]['total_deaths'],get_stats('deaths')['death_log']['daily'][day]['total_change_percentage'])
            out = [(msg[i:i+2040]) for i in range(0, len(msg), 2040)]
            for index,chunk in enumerate(out):
              if index == 0:
                embed=discord.Embed(description="{}".format(chunk),  color=discord.Colour(value=16730698))
                embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
              else :
                embed=discord.Embed(description="{}".format(chunk),  color=discord.Colour(value=16730698))
                embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
        else:
          async with ctx.typing():
            change = []
            for day in get_stats('deaths')['death_log']['daily'] :
              change.append(int(get_stats('deaths')['death_log']['daily'][day]['total_change'].replace(',','')))
            import matplotlib.pyplot as plt
            plt.plot(change,change, color='red')
            plt.xlabel('Days')
            plt.ylabel('Daily deaths')
            plt.title('Daily deaths in the days following the outbreak')
            plt.savefig('line.png', bbox_inches='tight')
            file = discord.File("line.png", filename="line.png")
            embed=discord.Embed(description="This simple **chart** represents the daily deaths in the last days , You can recieve the data in text with appending **-text** to the arg",  color=discord.Colour(value=16730698))
            embed.set_image(url="attachment://line.png")
            embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed,file=file)
      elif type.replace('-text','') == 'total':
        if type.endswith('-text'):
          async with ctx.typing():
            days = []
            msg = 'Total deaths log :'
            for day in get_stats('deaths')['death_log']['total'] :
              msg = msg + '\n **{}** : **__{}__** : **{}** \n'.format(day,get_stats('deaths')['death_log']['total'][day]['total_deaths'],get_stats('deaths')['death_log']['total'][day]['total_change_percentage'])
            out = [(msg[i:i+2040]) for i in range(0, len(msg), 2040)]
            for index,chunk in enumerate(out):
              if index == 0:
                embed=discord.Embed(description="{}".format(chunk),  color=discord.Colour(value=16730698))
                embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
              else :
                embed=discord.Embed(description="{}".format(chunk),  color=discord.Colour(value=16730698))
                embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
        else:
          async with ctx.typing():
            change = []
            for day in get_stats('deaths')['death_log']['total'] :
              change.append(int(get_stats('deaths')['death_log']['total'][day]['total_change'].replace(',','')))
            import matplotlib.pyplot as plt
            plt.plot(change,change, color='red')
            plt.xlabel('Days')
            plt.ylabel('Total deaths')
            plt.title('Total deaths in the days following the outbreak')
            plt.savefig('line.png', bbox_inches='tight')
            file = discord.File("line.png", filename="line.png")
            embed=discord.Embed(description="This simple **chart** represents the total deaths in the last days , You can recieve the data in text with appending **-text** to the arg",  color=discord.Colour(value=16730698))
            embed.set_image(url="attachment://line.png")
            embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed,file=file)
      else:
        for y in self.client.walk_commands():
          if y.name == 'death_log':
            embed=discord.Embed(title='Error : Invalid usage',description='**{}**'.format(y.usage),color=discord.Colour(value=16730698))
            embed.set_footer(text=cr,icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
def setup(client):
  client.add_cog(Corona(client))
