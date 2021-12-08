import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect('DB/prefix/prefixes.db')
sql = db.cursor()
 
def prefix(guild):
 
	sql.execute(f"SELECT * FROM prefixes WHERE guild = '{guild.id}'")
 
	for prefix in sql.fetchall():
 
		return prefix[1]
 
class MyCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases=["Привет"])
	async def hello(self, ctx):
		await ctx.send(f"**Привет, {ctx.author.mention}! Мой префикс  '>' {prefix(ctx.guild)}")
	
	@commands.has_permissions(administrator = True)
	@commands.command()
	async def setprefix(self, ctx, prefix = None):
 
		if prefix is None:
			return await ctx.send(embed = discord.Embed(description = '>', colour = discord.Color.red()))
		
		sql.execute(f"SELECT prefix FROM prefixes WHERE guild = '{ctx.guild.id}'")
 
		if sql.fetchone() is None:
 
			sql.execute(f"INSERT INTO prefixes VALUES (?, ?)", (ctx.guild.id, prefix))
			db.commit()
		
		else:
 
			sql.execute(f"UPDATE prefixes SET prefix = '{prefix}' WHERE guild = '{ctx.guild.id}'")
			db.commit()
		
		await ctx.send(embed = discord.Embed(description = f'Новый префикс: {prefix} На сервере {ctx.guild}', colour = discord.Color.green()))
	
	@commands.has_permissions(administrator = True)
	@commands.command()
	async def delprefix(self, ctx):
 
		sql.execute(f"SELECT prefix FROM prefixes WHERE guild = '{ctx.guild.id}'")
 
		if sql.fetchone() is None:
 
			await ctx.send(embed = discord.Embed(description = 'Префикс не установлен!', colour = discord.Color.red()))
		
		else:
 
			sql.execute(f"DELETE FROM prefixes WHERE guild = '{ctx.guild.id}'")
			db.commit()
		
		await ctx.send(embed = discord.Embed(description = f'Вы удалили префикс, префикс бота На сервере {ctx.guild}: ">"', colour = discord.Color.green()))
 
def setup(bot):
	bot.add_cog(MyCog(bot))
	print('[Cog] Prefix загружен!')