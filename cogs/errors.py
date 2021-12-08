import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import errors



class Errors(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		if isinstance(err, errors.CommandNotFound):
			await ctx.send(embed=discord.Embed(title= "Команда не найдена!", description=f"Для просмотра доступных команд введите >help"))
		elif isinstance(err, errors.MissingPermissions):
			await ctx.send(embed=discord.Embed(title= "Недостаточно прав!", description=f"У вас недостаточно прав для запуска этой команды!"))
			await ctx.send(embed=discord.Embed(title= "У вас кулдаун!", description=f"У вас не прошёл кулдаун! Попробуйте позже!"))
		else:
			await ctx.send(embed=discord.Embed(title= "Неизвестная ошибка!", description=f"Произошла неизвестная ошибка: `{err}`\nПожалуйста, свяжитесь с разработчиками для исправления этой ошибки"))

def setup(client):
	client.add_cog(Errors(client))
	print('[Cog] Errors загружен!')