import discord
from discord.ext import commands
from discord.ext.commands import Bot

# ------------------------ COGS ------------------------ #  

class Help(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.group()
	async def help(self, ctx):
		if ctx.invoked_subcommand == None:
			emb = discord.Embed(title= f"__**Список Команд Бота {self.client.user.name}**__", description = "**Для просмотра команд введите `>help <модуль>`**", color=0xdeaa0c)
			emb.add_field(name= "**>help moderation**", value= "**Команды модерации**",inline=False)
			emb.add_field(name= "**>help info**", value= "**Информационные команды**",inline=False)
			emb.add_field(name= "**>help fun**", value= "**Развлекательные команды**",inline=False)
			emb.add_field(name= "**>help premium**", value= "**Премиум команды**",inline=False)
			emb.add_field(name= "**>help settings**", value= "**settings команды(BETA)**",inline=False)
			emb.add_field(name= "**>help support**", value= "**Команды поддержки**",inline=False)
			emb.set_thumbnail(url=self.client.user.avatar_url)
			emb.add_field(name="**Разработчик :**", value=f"**Владельц** :**<@401080191054643200>", inline=False)
			emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
			await ctx.send(embed = emb)
			

	@help.command()
	async def moderation(self, ctx):
		emb = discord.Embed(title= "**Список Команд модерации**", color=0xdeaa0c)
		emb.add_field(name= "**`>бан <пинг участника> [причина]`**", value= "**Забанить участника на сервере**",inline=False)
		emb.add_field(name= "**`>удалить [кол-во сообщений(макс. 50)]`**", value= "**Очистить определённое кол-во сообщений**",inline=False)
		emb.add_field(name= "**`>кик <пинг участника> [причина]`**", value= "**Выгнать участника с сервера**",inline=False)
		emb.add_field(name= "**`>разбан <пинг участника> [причина]`**", value= "**Разбан участника на сервере**",inline=False)
		emb.add_field(name= "**`>слоумод`**", value= "**Установка времени**",inline=False)
		emb.set_thumbnail(url=self.client.user.avatar_url)
		emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
		await ctx.send(embed = emb)

	@help.command()
	async def info(self, ctx):
		emb = discord.Embed(title= "**Информационные команды**", color=0xdeaa0c)
		emb.add_field(name= "**`>бот`**", value= "**Узнать информацию о боте**",inline=False)
		emb.add_field(name= "**`>пинг`**", value= "**Узнать пинг бота**",inline=False)
		emb.add_field(name= "**`>сервер`**", value= "**Узнать информацию о сервере**", inline=False)
		emb.add_field(name= "**`>статус`**", value= "**Инфо о боте**",inline=False)
		emb.add_field(name= "**`>юзер`**", value= "**Узнать ниформацию о пользователе**",inline=False)
		emb.set_thumbnail(url=self.client.user.avatar_url)
		emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
		await ctx.send(embed = emb)

	@help.command()
	async def fun(self, ctx):
		emb = discord.Embed(title= "**Развлекательные команды**", color=0xdeaa0c)
		emb.add_field(name= "**`>кнб`**", value= "**Камень-Ножницы-Бумага**",inline=False)
		emb.add_field(name= "**`>ачивка`**", value= "**Достижение из Minecraft**",inline=False)
		emb.set_thumbnail(url=self.client.user.avatar_url)
		emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
		await ctx.send(embed = emb)

	@help.command()
	async def premium(self, ctx):
		emb = discord.Embed(title= "**Премиум команды**", color=0xdeaa0c)
		emb.add_field(name= "**`>донат`**", value= "**Оформить премиум подписку**",inline=False)
		emb.set_thumbnail(url=self.client.user.avatar_url)
		emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
		await ctx.send(embed = emb)

	@help.command()
	async def settings(self, ctx):
		emb = discord.Embed(title= "**Настройки(BETA)**", color=0xdeaa0c)
		emb.add_field(name= "**`>пригласить`**", value= "**Добавить бота на свой сервер**",inline=False)
		emb.add_field(name= "**`>setprefix`**", value="**Смена Префикса**",inline=False)
		emb.add_field(name= "**`>delprefix`**", value="**Удалить Префикс**",inline=False)
		emb.set_thumbnail(url=self.client.user.avatar_url)
		emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
		await ctx.send(embed = emb)

	@help.command()
	async def support(self, ctx):
		emb = discord.Embed(title= "**Команды поддержки(Скоро)**", color=0xdeaa0c)
		emb.set_thumbnail(url=self.client.user.avatar_url)
		emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
		await ctx.send(embed = emb)

	@help.command()
	async def admin(self, ctx):
		if ctx.author.id == 401080191054643200:
			emb = discord.Embed(title= "**Команды владельца**", color=0xdeaa0c)
			emb.add_field(name= "**`>aban <ID пользователя>`**", value= "**Добавить пользователя в ЧС бота**",inline=False)
			emb.add_field(name= "`>aunban <ID пользователя>`", value= "**Удалить пользователя из ЧС бота**",inline=False)
			emb.add_field(name= "`>reload <модуль>`", value= "**Перезагрузить модуль**",inline=False)
			emb.set_thumbnail(url=self.client.user.avatar_url)
			emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
			await ctx.send(embed = emb)
		else:
			await ctx.send(embed=discord.Embed(title= "Нет доступа!", description=f"Данная команда доступна только основателю бота!"))




# ------------------------ BOT ------------------------ #  

def setup(client):
	client.add_cog(Help(client))
	print('[Cog] Help загружен!')