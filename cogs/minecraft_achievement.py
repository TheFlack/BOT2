import discord
import random
from discord.ext import commands

class Minecraft_achievement(commands.Cog):
    """Shows minecraft achievement with your text"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['Achievement', 'achievement', 'Mine_achievement', 'mine_achievement', 'Mcach' ,'mcach', 'Ачивка', 'ачивка', 'Достижение', 'достижение', 'Майн_ачивка', 'майн_ачивка'])
    async def __minecraft_achievement(self, ctx, *, name:str = None):
        auth = ctx.message.author
        if name != None:
            a = random.randint(1, 40)
            name2 = name.replace(' ', '+')
            url = f'https://minecraftskinstealer.com/achievement/{a}/Achievement+Get%21/{name2}'
            emb = discord.Embed(title="Minecert Achievement", description = f'[Достижение!]({url})', colour = 0xee3c00)
            emb.set_footer(icon_url = self.client.user.avatar_url)
            emb.set_image(url = url)
            emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
            await ctx.send(embed = emb)
            print(f'[Logs:utils] Майнкрафт достижение было успешно создано | >achievement')
        else:
            emb = discord.Embed(colour = 0xee3c00)
            emb.add_field(name = "Ошибка:warning:", value = "Вы должны написать какой-нибудь текст, {}".format(auth.mention))
            emb.set_footer(text = f'{self.client.user.name} © 2021 | Все права защищены', icon_url = self.client.user.avatar_url)
            await ctx.send(embed = emb)
def setup(client):
    client.add_cog(Minecraft_achievement(client))
    print('[Cog] minecraft загружен!')