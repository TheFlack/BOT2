import discord
from discord.ext import commands
from discord.ext.commands import Bot

import sqlite3

db = sqlite3.connect('DB/admin/aban.db')
cursor = db.cursor()


class Admin(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.guild_only()
	async def aban(self, ctx, member_id):
		if ctx.author.id == 401080191054643200:
			cursor.execute("""CREATE TABLE IF NOT EXISTS users(
				id INT
			)""")
			db.commit()
			cursor.execute(f"SELECT id FROM users WHERE id = '{member_id}'")
			if cursor.fetchone() is None:
				cursor.execute(f"INSERT INTO users VALUES (?)", [member_id])
				db.commit()
				await ctx.send(embed=discord.Embed(title= "Участник добавлен в ЧС", description=f"ID: {member_id} был успешно внесён в чёрный список Your Space"))
			else:
				await ctx.send("Пользователь уже есть в БД")
		else:
			await ctx.send(embed=discord.Embed(title= "Нет доступа!", description=f"Данная команда доступна только основателю бота!"))


	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		if cursor.execute(f"SELECT * from users WHERE id = {guild.owner.id}"):
			emb = discord.Embed(title=f"Ошибка!",description="К сожалению вы находитесь в ЧС Your Space")
			emb.set_thumbnail(url=self.client.user.avatar_url)
			emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
			await guild.text_channels[0].send(embed = emb)
			await guild.leave()


	@commands.command()
	@commands.guild_only()
	async def modules(self, ctx):
		if ctx.author.id == 401080191054643200:
			emb = discord.Embed(title= "Список модулей")
			emb.add_field(name='admin',value='Команды разработчика', inline=False)
			emb.add_field(name='errors',value='Оброботчик ошибок', inline=False)
			emb.add_field(name='fun',value='Развлекательные команды', inline=False)
			emb.add_field(name='help',value='Команда `-help`', inline=False)
			emb.add_field(name='information',value='Информационные команды', inline=False)
			emb.add_field(name='join',value='Приветствие бота', inline=False)
			emb.add_field(name='moderation',value='Команды модерации', inline=False)
			emb.add_field(name='premium',value='Премиум команды', inline=False)
			emb.add_field(name='status',value='Статус бота', inline=False)
			emb.add_field(name='support',value='Команды поддержки', inline=False)
			emb.add_field(name='utility',value='Утилиты', inline=False)
			emb.set_thumbnail(url=self.client.user.avatar_url)
			emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
			await ctx.send(embed = emb)
		else:
			await ctx.send(embed=discord.Embed(title= "Нет доступа!", description=f"Данная команда доступна только основателю бота!"))


def setup(client):
	client.add_cog(Admin(client))
	print('[Cog] Admin загружен!')