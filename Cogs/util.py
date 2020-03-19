import discord
from discord.ext import commands


cr = "Powered by discord.py and Jake's brain"
class Util(commands.Cog):
  def __init__(self,client):
    self.client = client
  @commands.command()
  async def help(self,ctx,*cog):
    user = self.client.get_user("480407581085532180")
    if not cog:
       help=discord.Embed(title='Listing Commands', description='Hi , im `{}` made by `{}` . My prefixes are `c!`,`covid ` and `bot mention` . Here is a list of my commands :'.format(self.client.user.name,user.name),color=discord.Colour(value=16730698))
       cmds_desc = ''
       for y in self.client.walk_commands():
          cmds_desc += '\n `{}` : ***{}***'.format(y.name,y.description if len(y.description) > 1 else 'No description found')
       help.description = help.description + cmds_desc
       help.set_footer(text=cr,icon_url=self.client.user.avatar_url)
       await ctx.send('',embed=help)

def setup(client):
  client.add_cog(Util(client))
