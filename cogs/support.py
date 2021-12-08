import discord
from discord.ext import commands
from discord.ext.commands import Bot

class Support(commands.Cog):
	def __init__(self, client):
		self.client = client
		

	#Invite
	@commands.command(aliases=['пригласить'])
	@commands.guild_only()
	async def invite(self, ctx):
		emb = discord.Embed(title = "Добавить бота на свой сервер")
		emb.add_field(name=f'Приглашение Бота:',value="[Пригласить](https://discord.com/api/oauth2/authorize?client_id=892058044089909318&permissions=8&scope=bot)",inline=False)
		await ctx.send(embed = emb)


		
def setup(client):
	client.add_cog(Support(client))
	print('[Cog] Support загружен!')