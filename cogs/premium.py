import discord
from discord.ext import commands
from discord.ext.commands import Bot


import sqlite3

db = sqlite3.connect('DB/premium/premium.db')
cursor = db.cursor()


class Premium(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases=['донат'])
	@commands.guild_only()
	async def donate(self, ctx):
		emb = discord.Embed(title = f'**Поддержка донатом**')
		emb.add_field(name=f'Полезные ссылки:', value="[**Донат**](https://www.donationalerts.com/r/kreativniy)", inline=True)
		emb.set_thumbnail(url=self.client.user.avatar_url)
		emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
		await ctx.send(embed = emb)

def setup(client):
	client.add_cog(Premium(client))
	print('[Cog] Premium загружен!')