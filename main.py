from covid import get_infections , get_infections_by_name , get_infected_countries , check_length , get_latest_info , get_stats
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
@client.command(brief='Get symptoms of COVID19',description='Get symptoms of COVID19')
async def symptoms(ctx):
    embed=discord.Embed(title="COVID19 Symptoms")
    embed.set_footer(text=cr,icon_url=client.user.avatar_url)
    embed.set_image(url='https://www.worldometers.info/img/coronavirus--symptoms-table-wang-jama-02072020-reduced.png')
    await ctx.send(embed=embed)
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
      embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/686666564589846625/688494381027688480/caution-icon-png-14-original.png')
      await ctx.send(embed=embed)
      return
    except Exception as e:
      await ctx.send(str(e))
@client.command(brief='Get latest info about COVID19 (Updates every 24 hours)',description='Get latest info about COVID19 (Updates every 24 hours)')
async def latest_news(ctx):
      out = [(get_latest_info()['info'][i:i+2048]) for i in range(0, len(get_latest_info()['info']), 2048)]
      for index,chunk in enumerate(out):
        if index == 0:
          embed=discord.Embed(title="COVID19 Latest news : {}".format(get_latest_info()['date']),description="**{}**".format(chunk.replace('\xa0','\n').replace('[source]','')),  color=discord.Colour(value=16730698))
          embed.set_footer(text=cr,icon_url=client.user.avatar_url)
          await ctx.send(embed=embed)
        else :
          embed=discord.Embed(description="**{}**".format(chunk.replace('\xa0','\n').replace('[source]','')),  color=discord.Colour(value=16730698))
          embed.set_footer(text=cr,icon_url=client.user.avatar_url)
          await ctx.send(embed=embed)
@client.command(brief='Get the deaths log starting from the outbreak day',description='Get the deaths log starting from the outbreak day')
async def death_log(ctx):
  days = []
  for day in get_stats('deaths')['death_log']['daily']:
    days.append(int(get_stats('deaths')['death_log']['daily'][day]['total_deaths'].replace(',','')))
  import matplotlib.pyplot as plt
  print(plt.rcParams.keys())
  plt.rcParams.update({'text.color' : "white",'axes.labelcolor' : "white",'axes.color' : "white"})
  plt.plot(days,days, color='red')
  plt.xlabel('Days')
  plt.ylabel('Daily deaths')
  plt.title('Daily deaths in the days following the outbreak')
  plt.savefig('line.png', bbox_inches='tight' , transparent=True)
  file = discord.File("line.png", filename="line.png")
  embed=discord.Embed(description="This simple **chart** represents the daily deaths in the last days , You can recieve the data in dms with appending **-dms** to the arg",  color=discord.Colour(value=16730698))
  embed.set_image(url="attachment://line.png")
  embed.set_footer(text=cr,icon_url=client.user.avatar_url)
  await ctx.send(embed=embed,file=file)
client.run('NTc2MTEzNjg5MzI1NzMxODky.Xm96Aw.TcQZx4WcGY3B_dXf8Fd4GMA3nRo')
