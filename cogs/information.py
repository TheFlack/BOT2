import discord
from discord.ext import commands
from discord.ext.commands import Bot


class Information(commands.Cog):
	def __init__(self, client):
		self.client = client


	#Info
	@commands.command(aliases=['бот'])
	@commands.guild_only()
	async def info(self, ctx):

		guild_count = len(self.client.guilds)

		emb = discord.Embed(title=f"{self.client.user.name}#{self.client.user.discriminator}",description="Информация о боте **Your Space**.\n", color=0xdeaa0c)
		emb.add_field(name=f'Бота создал:', value="<@401080191054643200>", inline=True)
		emb.add_field(name=f'Серверов:', value=f"{guild_count}", inline=True)
		emb.add_field(name=f'Префикс бота:', value=">", inline=True)
		emb.add_field(name=f'Бот написан на:', value="Discord.py", inline=True)
		emb.add_field(name=f'Версия бота:', value="1.5", inline=True)
		emb.add_field(name=f'Язык бота:', value="Русский", inline=True)
		emb.add_field(name=f'Приглашение Бота:',value="[Пригласить](https://discord.com/api/oauth2/authorize?client_id=892058044089909318&permissions=8&scope=bot)",inline=True)
		emb.add_field(name=f'Сервер GameCord:', value="[Вступить](https://discord.gg/NwvhBpVN3x)",inline=True)
		emb.add_field(name=f'Полезные ссылки:', value="[Сервер поддержки](https://discord.gg/NwvhBpVN3x)\n)",inline=True)
		emb.set_thumbnail(url=self.client.user.avatar_url)
		emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
		await ctx.send(embed = emb)
		
def setup(client):
	client.add_cog(Information(client))
	print('[Cog] Information загружен!')