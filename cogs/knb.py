import discord
from discord.ext import commands
import random
import asyncio


class Games(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.command(aliases = ['кнб'])
	async def rps(self, ctx):
		def check_win(p, b):
			if p=='🌑':
				return False if b=='📄' else True
			if p=='📄':
				return False if b=='✂' else True
			return False if b=='🌑' else True

		async with ctx.typing():
			reactions = ['🌑', '📄', '✂']
			message = await ctx.send("**Камень ножницы Бумага**\nСделай выбор!", delete_after=18.0)
			for reaction in reactions:
				await message.add_reaction(reaction)
			knb_emoji = random.choice(reactions)

		def check(reaction, user):
			return user != self.client.user and user == ctx.author and (str(reaction.emoji) == '🌑' or '📄' or '✂')
		try:
			reaction, _ = await self.client.wait_for('reaction_add', timeout=10.0, check=check)

		except asyncio.TimeoutError:
			await ctx.send("Время вышло! :stopwatch:")

		else:
			await ctx.send(f"**Твой выбор:\t{reaction.emoji}\n:robot: :\t{knb_emoji}**")

			if str(reaction.emoji) == knb_emoji:
				await ctx.send("**Ничья! :ribbon:**")
			elif check_win(str(reaction.emoji), knb_emoji):
				await ctx.send("**Ты победил! :sparkles:**")
			else:
				await ctx.send("**Я победил! :robot:**")
								

def setup(client):
	client.add_cog(Games(client))
	print('[Cog] KNB загружен!')