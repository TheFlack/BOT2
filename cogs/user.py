import discord
from discord.ext import commands
import datetime
import time
from loguru import logger


class user(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def member(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		statuses = {
		"online": "> Онлайн (<:online:798637933439352852>)",
		"dnd": "> Не беспокоить (<:dnd:798637933401210920>)",
		"idle": "> Не на месте (<:odle:798637933305397289>)",
		"offline": "> Оффлайн (<:offline:798637933384040528>)"
		}
		member_age = (ctx.message.created_at - member.created_at).days
		roles_information = ' '.join([role.mention for role in ctx.author.roles if role != ctx.guild.default_role])
		embed = discord.Embed(color = 0xee3c00)
		embed.add_field(name = '`ID:`', value = f'{member.id}', inline = True)
		embed.add_field(name = '`Дискриминатор:`', value = f'{member.name}#{member.discriminator}', inline = True)
		embed.add_field(name = '`Дата регистрации:`', value = f"{member.created_at.strftime('%d.%m.%Y %H:%M:%S')}\nЭто {member_age} дней назад", inline = False)
		embed.add_field(name = '`Присоединился:`', value = member.joined_at.strftime('%d.%m.%Y %H:%M:%S'), inline = True)
		embed.add_field(name = '`Высшая роль:`', value = member.top_role.mention, inline = True)
		embed.add_field(name = '`Все роли:`', value = (roles_information), inline = False)
		embed.add_field(name = '`Отображаемое имя:`', value = member.display_name, inline = True)
		embed.add_field(name = '`Статус:`', value = statuses[member.status.name], inline = True)
		if member.activity is None:
			embed.add_field(name = '`Пользовательский статус:`', value = f'> Нету', inline = True)
			if member.activity == True:
				embed.add_field(name = '`Пользовательский статус:`', value = f'> {member.activity}', inline = True)
		embed.set_thumbnail(url = member.avatar_url)
		embed.set_footer(text = f"Время: {time.strftime('%H:%M:%S')}")
		await ctx.send(embed = embed)

def setup(client):
	client.add_cog(user(client))
	print('[Cog] User загружен!')