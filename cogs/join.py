import discord
from discord.ext import commands
from discord.ext.commands import Bot



class Join(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		emb = discord.Embed(title=f"Флэки",description="Привет! Спасибо, что добавил меня на своё сервер. Для просмотра команд введите `>help`. Удачи!")
		emb.set_thumbnail(url=self.client.user.avatar_url)
		emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
		await guild.text_channels[0].send(embed = emb)

def setup(client):
    client.add_cog(Join(client))
    print('[Cog] Join загружен!')