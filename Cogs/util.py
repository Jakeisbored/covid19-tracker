import discord
from discord.ext import commands


cr = "Powered by discord.py and Jake's brain"
class Util(commands.Cog):
  def __init__(self,client):
    self.client = client
  @commands.command()
  async def help(self,ctx,*cmd):
    user = self.client.get_user("480407581085532180")
    if not cmd:
       help=discord.Embed(title='Help menu',color=discord.Colour(value=16730698))
       cmds_desc = ''
       for y in self.client.walk_commands():
          print(y.cog)
          cmds_desc += '\n `{}` : ***{}*** : *{}*'.format(y.name,y.brief if y.brief else 'No brief description found',y.cog.name)
       help.add_field(name='Introduction:',value='Hi , im `{}` made by `{}` . My prefixes are `c!`,`covid ` and `bot mention` . View the commands in the next segment.'.format(self.client.user.name,'Jake'))
       help.add_field(name='Commands:',value=cmds_desc)
       help.set_footer(text='add a command name after the help to view more about a certain command',icon_url=self.client.user.avatar_url)
       await ctx.send(embed=help)

def setup(client):
  client.add_cog(Util(client))
