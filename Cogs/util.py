import discord
from discord.ext import commands
cr = "Powered by discord.py and Jake's brain"
class Util(commands.Cog):
  def __init__(self,client):
    self.client = client
  @commands.command()
  async def help(self,ctx,*cog):
    if not cog:
       help=discord.Embed(title='Listing Commands', description='Use `c!help *cog*` to find out more about them! ',color=discord.Colour(value=16730698))
       cmds_desc = ''
       for y in self.client.walk_commands():
          cmds_desc += '\n **{}** : ***{}***'.format(y.name,y.description)
       help.description = help.description + cmds_desc
       help.set_footer(text=cr,icon_url=self.client.user.avatar_url)
       await ctx.send('',embed=help)

def setup(client):
  client.add_cog(Util(client))
