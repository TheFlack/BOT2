import discord
from discord.ext import commands


class Server_info(commands.Cog):
 

	def __init__(self, client):
		self.client = client

	@commands.command(aliases=['сервер'])
	@commands.guild_only()
	async def server(self, ctx):
		emb = discord.Embed(title = f"Информация о сервере **{ctx.guild.name}**")
		emb.add_field(name="ID:", value=f"{ctx.guild.id}", inline=False)
		emb.add_field(name="Владелец:", value=f"{ctx.guild.owner}", inline = False)
		emb.set_thumbnail(url=ctx.guild.icon_url)
		emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
		await ctx.send(embed = emb)

def setup(client):
	client.add_cog(Server_info(client))
	print('[Cog] Server загружен!')