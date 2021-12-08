import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Cog

from sqlite3 import connect
from asyncio import get_event_loop # for run create_tables function


# database
async def _autoroles(r_type, request, save=False):
    connection = connect('DB/autorole/autorole.db')
    if r_type == 'request' and save:
        connection.cursor().execute(request)
        connection.commit()
    elif r_type == 'request': return connection.cursor().execute(request)
    elif r_type == 'fetchall': return connection.cursor().execute(request).fetchall()
    elif r_type == 'fetchone': return connection.cursor().execute(request).fetchone()\

async def create_tables():
    await _autoroles('request', "CREATE TABLE IF NOT EXISTS roles (guild BIGINT, role BIGINT)", save=True)

get_event_loop().run_until_complete(create_tables()) # Running create_tables function

class AutoRoles(Cog):
    def __init__(self, bot):
        self.bot = bot

        self._checking_roles.start() # Ignore an error here
    
    @tasks.loop(minutes=2)
    async def _checking_roles(self):
        for item in await _autoroles("fetchall", "SELECT * FROM roles"):
            guild = self.bot.get_guild(item[0])
            if guild:
                role = guild.get_role(item[1])
                if not role: await _autoroles('request', f"DELETE FROM roles WHERE guild = '{item[0]}' AND role = '{item[1]}'", save=True)
    
    @Cog.listener()
    async def on_member_join(self, member):
        for _role in await _autoroles("fetchall", f"SELECT role FROM roles WHERE guild = '{member.guild.id}'"):
            role = member.guild.get_role(_role[0])
            if role: await member.add_roles(role)
    
    @commands.command(name='add-role',usage='add-role @role')
    @commands.guild_only()
    async def _add_role(self, ctx, role:discord.Role):
        if await _autoroles('fetchone', f"SELECT * FROM roles WHERE guild = '{ctx.guild.id}' AND role = '{role.id}'"):
            return await ctx.send("❌ Данная роль уже есть в базе данных")
        if ctx.author != ctx.guild.owner:
            return await ctx.send("❌ Данную команду может выполнять только создатель сервера")
        await _autoroles('request', f"INSERT INTO roles VALUES ({ctx.guild.id}, {role.id})", save=True)
        await ctx.send(f"✅ Роль `@{role}` успешно добавлена в базу данных")
    
    @commands.command(name='remove-role',usage='remove-role @role')
    @commands.guild_only()
    async def _remove_role(self, ctx, role:discord.Role):
        if not await _autoroles('fetchone', f"SELECT * FROM roles WHERE guild = '{ctx.guild.id}' AND role = '{role.id}'"):
            return await ctx.send("❌ Данной роли нет в базе данных")
        if ctx.author != ctx.guild.owner:
            return await ctx.send("❌ Данную команду может выполнять только создатель сервера")
        await _autoroles('request', f"DELETE FROM roles WHERE guild = '{ctx.guild.id}' AND role = '{role.id}'", save=True)
        await ctx.send(f"✅ Роль `@{role}` успешно удалена из базы данных")

def setup(client):
    client.add_cog(AutoRoles(client))
    print('[Cog] AutoRoles загружен!')