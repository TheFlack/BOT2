import discord
from discord.ext import commands


class User(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.command(aliases = ['аватар'])
	async def avatar(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member

		emb = discord.Embed(colour = 0xee3c00)
		emb.set_author(name = f'{member}', icon_url = member.avatar_url)
		emb.set_image(url = member.avatar_url)
		emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
		await ctx.send(embed = emb)


def setup(client):
	client.add_cog(User(client))
	print('[Cog] Avatar загружен!')