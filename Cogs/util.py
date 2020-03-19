import discord
from discord.ext import commands
cr = "Powered by discord.py and Jake's brain"
class Util(commands.Cog):
  def __init__(self,client):
    self.client = client
  @commands.command()
  async def help(self,ctx,*cog):
      """Gets all cogs and commands of mine."""
      try:
          if not cog:
              halp=discord.Embed(title='Listing Commands', description='Use `c!help *cog*` to find out more about them!\n(BTW, the Cog Name Must Be in Title Case, Just Like this Sentence.)',color=discord.Colour(value=16730698))
              cmds_desc = ''
              for y in self.client.walk_commands():
                 cmds_desc += '\n {} - {}'.format(y.name,y.description)
              halp.add_field(name='Commands',value=cmds_desc if len(cmds_desc) >1 else 'مافي كومندات او انتا غلطان يا مغفل',inline=False)
              halp.set_footer(text=cr,icon_url=self.client.user.avatar_url)
              await ctx.send('',embed=halp)
          else:
              if len(cog) > 1:
                  halp = discord.Embed(title='Error!',description='That is way too many cogs!',color=discord.Colour(value=16730698))
                  halp.set_footer(text=cr,icon_url=self.client.user.avatar_url)
                  await ctx.send('',embed=halp)
              else:
                  found = False
                  for x in self.client.cogs:
                      for y in cog:
                          if x == y:
                              halp=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[cog[0]].__doc__,color=discord.Colour(value=16730698))
                              halp.set_footer(text=cr,icon_url=self.client.user.avatar_url)
                              for c in self.client.get_cog(y).get_commands():
                                  if not c.hidden:
                                      halp.add_field(name=c.name,value=c.help,inline=False)
                                      halp.set_footer(text=cr,icon_url=self.client.user.avatar_url)
                              found = True
                  if not found:
                      halp = discord.Embed(title='Error!',description='How do you even use "'+cog[0]+'"?',color=discord.Colour(value=16730698))
                      halp.set_footer(text=cr,icon_url=self.client.user.avatar_url)
                  else:
                      await ctx.send('',embed=halp)
      except Exception as e:
          raise e
def setup(client):
  client.add_cog(Util(client))
