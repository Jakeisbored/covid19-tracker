import discord
from discord.ext import commands


cr = "Powered by discord.py and Jake's brain"
class Util(commands.Cog):
  def __init__(self,client):
    self.client = client
  @commands.command()
  async def help(self,ctx,cmd:str=None):
    user = self.client.get_user("480407581085532180")
    if cmd == None:
       help=discord.Embed(title='Help menu',color=discord.Colour(value=16730698))
       cmds_desc = ''
       for y in self.client.walk_commands():
          cmds_desc += '\n `{}` : ***{}*** : *{}*'.format(y.name,y.brief if y.brief else 'No brief description found',y.cog_name)
       help.add_field(name='Introduction:',value='Hi , im `{}` made by `{}` . My prefixes are `c!`,`covid ` and `@COVID19-Tracker#9817` . View the commands in the next segment.'.format(self.client.user.name,'Jake'))
       help.add_field(name='Commands:',value=cmds_desc)
       help.set_footer(text='add a command name after the help to view more about a certain command',icon_url=self.client.user.avatar_url)
       await ctx.send(embed=help)
    else:
       for y in self.client.walk_commands():
          if y.name == cmd:
             help=discord.Embed(title='Showing info about : {}'.format(cmd),description='Full Description : **{}**\n Brief Description : **{}** \n Usage : **{}**'.format(y.description if y.description else 'No full description was found',y.brief if y.brief else 'No brief description was found',y.usage if y.usage else 'No proper usage was found'),color=discord.Colour(value=16730698))
             help.set_footer(text=cr,icon_url=self.client.user.avatar_url)
             await ctx.send(embed=help)
             return
       error = discord.Embed(title='Error : Invalid command',description='Command **{}** doesnt exist fool.'.format(cmd),color=discord.Colour(value=16730698))
       error.set_footer(text=cr,icon_url=self.client.user.avatar_url)
       await ctx.send(embed=error)  
def setup(client):
  client.add_cog(Util(client))
