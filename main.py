from bs4 import BeautifulSoup
import requests

main_endpoint = 'https://www.worldometers.info/coronavirus/{}'
def get_infections():
  url = main_endpoint.format('#countries')
  HTML = requests.get(url).content
  soup = BeautifulSoup(HTML,'html.parser')
  table_children = soup.select_one('#main_table_countries > tbody:nth-child(2)').find_all("tr")
  infections = {}
  for child in table_children :
    for index,td in enumerate(child.find_all('td')):
      if(index == 0):
        country_key = td.getText().lstrip(' ').rstrip(' ')
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
import discord
from discord.ext import commands
client = commands.Bot(command_prefix='c!', description='A COVID19 tracking bot' , activity=discord.Activity(type=discord.ActivityType.watching, name="corona updates"))
cr = "Powered by discord.py and Jake's brain"
@client.event
async def on_ready():
  print(f'Logged as {client.user.name}')
@client.command(brief='Search for an arg in the infected countries',description='Search for an arg in the infected countries , if no arg is given the list of infected countries is returned')
async def search_country(ctx,search_args:str=None):
      if (search_args == None):
        countries = get_infected_countries()
        countries.sort()
        embed = discord.Embed(title="Currently infected countries !" , description="**{}** \n **{} ** total results".format(str(countries).replace('[','').replace(']',''),str(len(countries))),  color=discord.Colour(value=16730698))
        embed.set_footer(text=cr,icon_url=client.user.avatar_url)      
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/686666564589846625/688494381027688480/caution-icon-png-14-original.png')
        await ctx.send(embed=embed)
        return
      else:
        countries = get_infected_countries()
        embed = discord.Embed(title="Searching for {}".format(search_args) ,  color=discord.Colour(value=16730698))
                
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/686666564589846625/688494381027688480/caution-icon-png-14-original.png')
        embed.set_footer(text=cr,icon_url=client.user.avatar_url)
        c = []
        for country in countries:
          if(search_args.lower() in country.lower()): 
            c.append(country)
        embed.description = '**{}** \n **{}** total results'.format('No results were found' if len(str(c).replace('[','').replace(']',''))<1 else str(c).replace('[','').replace(']',''),str(len(c)))

        await ctx.send(embed=embed) 
        return  
@client.command(brief='Get infections in a specific country',description='Get infections in a specific country')
async def covid(ctx,country:str=None):
    try:
      if(country == None):
        results= get_infections()
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
        embed.set_footer(text=cr,icon_url=client.user.avatar_url)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/686666564589846625/688494381027688480/caution-icon-png-14-original.png')
        file = discord.File("pie.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(embed=embed,file=file)
        return
      c = []
      countries = get_infected_countries()
      for countr in countries:
          if(country.lower() in countr.lower()): 
            c.append(countr)
      country = None if len(c) < 1 else c[0]
      results = get_infections_by_name(country)
      embed=discord.Embed(title="Infections in {}".format(country),description='**Total** : {}  \n **Deaths** : {} \n **Cured** : {} \n **New cases** : {} \n **Critical cases** : {} \n **New deaths** : {} \n **Active cases** : {}'.format(check_length(results[country]['total_cases']),check_length(results[country]['total_deaths'],format(int(results[country]['total_deaths'].replace(',',''))*100/int(results[country]['total_cases'].replace(',','')),'.2f') if not check_length(results[country]['total_deaths']) == 'None' else None),check_length(results[country]['total_recovered'],format(int(results[country]['total_recovered'].replace(',',''))*100/int(results[country]['total_cases'].replace(',','')),'.2f') if not check_length(results[country]['total_recovered']) == 'None' else None),check_length(results[country]['new_cases'],format(int(results[country]['new_cases'].replace(',','').replace('+',''))*100/int(results[country]['total_cases'].replace(',','')),'.2f') if not check_length(results[country]['new_cases']) == 'None' else None,True),check_length(results[country]['critical_cases'],format(int(results[country]['critical_cases'].replace(',',''))*100/int(results[country]['total_cases'].replace(',','')),'.2f') if not check_length(results[country]['critical_cases']) == 'None' else None),check_length(results[country]['new_deaths'],format(int(results[country]['new_deaths'].replace(',','').replace('+',''))*100/int(results[country]['total_deaths'].replace(',','')),'.2f') if not check_length(results[country]['new_deaths']) == 'None' else None,True),check_length(results[country]['active_cases'],format(int(results[country]['active_cases'].replace(',',''))*100/int(results[country]['total_cases'].replace(',','')),'.2f') if not check_length(results[country]['active_cases']) == 'None' else None)) ,  color=discord.Colour(value=16730698))
      embed.set_footer(text=cr,icon_url=client.user.avatar_url)
      embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/686666564589846625/688494381027688480/caution-icon-png-14-original.png'
      await ctx.send(embed=embed,file=file)
    except Exception as e:
      await ctx.send(str(e))

client.run('NTc2MTEzNjg5MzI1NzMxODky.Xm96Aw.TcQZx4WcGY3B_dXf8Fd4GMA3nRo')
