import discord
from discord.ext import commands
from urllib.parse import urlparse
from discord import utils
import datetime
import asyncio
import random
import pip  
import os
import io
import json

answer5 = ['Вы не можете выгнать пользователя с такой же ролью!', 'Ваши роли одинаковы, я не могу так сделать!', 'Вы не можете выгнать такого же модератора как и вы!']
answer4 = ['Это невозможно сделать, так как выгнать меня может только основатель сервера!', 'Это может сделать только основатель сервера', 'Так сделать невозможно!', 'Увы, меня нельзя так остранить...']
answer3 = ['У вас не хватает прав!', 'Его роль стоит выше вашей!', 'Это нельзя сделать!', 'Ваша роль менее значима, чем этого пользователя!']
answer2 = ['Ты быканул на основателя сервера, или мне показалось?', 'Что он такого плохого тебе сделал?', 'При всём уважении к тебе я так не могу сделать!', 'Ах если бы я так мог...', 'Я не буду этого делать!', 'Сорян, но не в моих это силах!']
answer = ['Самоубийство не приведёт ни к чему хорошему!', 'Напомню: суицид - не выход!', 'Увы, я не могу этого сделать!', 'Самоубийство - не выход!', 'Не надо к себе так относиться!', 'Я не сделаю этого!', 'Я не буду это делать!', 'Я не выполню это действие', 'Не заставляй меня это сделать!']
class модерация(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['очистить','удалить','cleanup','delete'])
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    async def clean(self, ctx, amount : int):
        await ctx.message.delete()
        deleted = await ctx.channel.purge( limit = amount )
        emb = discord.Embed(colour=discord.Color.green())
        emb.add_field(name=':broom: Очистка:', value = f'очищено сообщений: {len(deleted)}' )
        await ctx.send( embed = emb, delete_after = 30 )

    @clean.error
    async def clear_error( self, ctx, error ):
        if isinstance( error, commands.CommandOnCooldown):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':broom: Очистка:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb, delete_after = 10 ) 
        if isinstance( error, commands.BadArgument ):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':broom: Очистка:', value = 'Укажите число!' )
            await ctx.send( embed = emb, delete_after = 30 )
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            await ctx.message.delete()
            emb = discord.Embed()
            emb.add_field( name = ':broom: Очистка:', value = 'Использование команды: `>clean [кол-во сообщений]`' )
            await ctx.send( embed = emb, delete_after = 30 )
        if isinstance( error, commands.errors.MissingPermissions ):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':broom: Очистка:', value = 'У вас не хватает прав!' )
            await ctx.send( embed = emb, delete_after = 30 )


    @commands.command(aliases=['кик'])
    @commands.has_permissions( kick_members = True )
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await ctx.message.delete()

        if ctx.author.top_role == member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer5))
            await ctx.send(embed=emb, delete_after=30)

            return


        elif member == ctx.bot.user:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer4))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif ctx.author.top_role < member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer3))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif member == ctx.author:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif member == ctx.guild.owner:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer2))
            await ctx.send(embed=emb, delete_after=30)

            return

        emb = discord.Embed()
        emb.add_field(name=':leg: Кик:', value = f'Вы уверены, что хотите кикнуть `{member.name}`?')
        emb.set_footer(text='Не нажимайте на галочку, если это ошибка!')
        msg = await ctx.send(embed=emb, delete_after = 30)
        await msg.add_reaction('✅')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check = check)
        except asyncio.TimeoutError:
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=':leg: Кик:', value = 'Действие отменнено!')
            await ctx.send(embed = emb, delete_after=30 )
        else:
            if reason == None:
                try:

                    emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                    emb.add_field( name = ':leg: Кик:', value = f'Вы, `{member.name}` кикнуты с сервера `{ ctx.guild.name }`!', inline = False)
                    emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                    await member.send( embed = emb)

                    await member.kick(reason=reason)
                except:
                    success = False
                else:
                    success = True

                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':leg: Кик:', value = f'`{member.name}` кикнут!', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                await ctx.send(embed=emb)

                return
            try:

                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':leg: Кик:', value = f'Вы, `{member.name}` кикнуты с сервера `{ ctx.guild.name }`!', inline = False)
                emb.add_field( name = 'По причине:', value = reason, inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                await member.send( embed = emb)

                await member.kick(reason=reason)
            except:
                success = False
            else:
                success = True
 
            emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
            emb.add_field( name = ':leg: Кик:', value = f'`{member.name}` кикнут!', inline = False)
            emb.add_field( name = 'По причине:', value = reason, inline = False)
            emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

            await ctx.send(embed=emb)

    @kick.error
    async def clear_error(self, ctx, error):
        if isinstance( error, commands.CommandOnCooldown):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Кик:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb, delete_after = 10 )
        if isinstance(error, commands.BadArgument):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Кик:', value = 'Пользователь не найден!', inline = False)
            await ctx.send( embed = emb, delete_after=30 )

        if isinstance( error, commands.errors.MissingRequiredArgument ):
            await ctx.message.delete()
            emb = discord.Embed()
            emb.add_field( name = ':x: Кик:', value = 'Использование команды: `>kick [пользователь] <причина>`' )
            await ctx.send( embed = emb, delete_after=30 )

        if isinstance( error, commands.errors.MissingPermissions ):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Кик:', value = 'У вас не хватает прав!' )
            await ctx.send( embed = emb, delete_after=30 )

    @commands.command(aliases=['бан'])
    @commands.has_permissions( kick_members = True )
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await ctx.message.delete()
        if ctx.author.top_role == member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer5))
            await ctx.send(embed=emb, delete_after=30)

            return


        elif member == ctx.bot.user:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':hammer: Бан:', value = random.choice(answer4))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif ctx.author.top_role < member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':hammer: Бан:', value = random.choice(answer3))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif member == ctx.author:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':hammer: Бан:', value = random.choice(answer))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif member == ctx.guild.owner:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':hammer: Бан:', value = random.choice(answer2))
            await ctx.send(embed=emb, delete_after=30)

            return
        emb = discord.Embed()
        emb.add_field(name=':hammer: Бан:', value = f'Вы уверены, что хотите забанить `{member.name}`?')
        emb.set_footer(text='Не нажимайте на галочку, если это ошибка!')
        msg = await ctx.send(embed=emb, delete_after = 30)
        await msg.add_reaction('✅')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check = check)
        except asyncio.TimeoutError:
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=':hammer: Бан:', value = 'Действие отменнено!')
            await ctx.send(embed = emb, delete_after=30 )
        else:

            if reason == None:

                try:

                    emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                    emb.add_field( name = ':hammer: Бан:', value = f'Вы, `{member.name}` забаннены на сервере `{ ctx.guild.name }`!', inline = False)
                    emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                    await member.send( embed = emb)

                    await member.ban(reason=None)
                except:
                    success = False
                else:
                    success = True

                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':hammer: Бан:', value = f'Участник `{member.name}` забаннен!', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')


                await ctx.send(embed=emb)

                return

            try:

                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':hammer: Бан:', value = f'Вы, `{member.name}` забаннены на сервере `{ ctx.guild.name }`!', inline = False)
                emb.add_field( name = 'По причине:', value = reason, inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                await member.send( embed = emb)

                await member.ban(reason=reason)
            except:
                success = False
            else:
                success = True

            emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
            emb.add_field( name = ':hammer: Бан:', value = f'Участник `{member.name}` забаннен!', inline = False)
            emb.add_field( name = 'По причине:', value = reason, inline = False)
            emb.add_field( name = 'Модератор:', value = f'{ctx.author}')


            await ctx.send(embed=emb)

    @ban.error
    async def clear_error( self, ctx, error ):
        if isinstance( error, commands.CommandOnCooldown):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Бан:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb, delete_after = 10 )
        if isinstance( error, commands.BadArgument ):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Бан:', value = 'Вы указали что-то не то!' )
            await ctx.send( embed = emb, delete_after=30 )
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            await ctx.message.delete()
            emb = discord.Embed()
            emb.add_field( name = ':x: Бан:', value = 'Использование команды: `>ban [пользователь] <причина>`' )
            await ctx.send( embed = emb, delete_after=30 )
        
        if isinstance( error, commands.errors.MissingPermissions ):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Бан:', value = 'У вас не хватает прав!' )
            await ctx.send( embed = emb, delete_after=30 )


    @commands.command(aliases=['мьют'])
    @commands.has_permissions( kick_members = True )
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    async def mute(self, ctx, member:discord.Member, duration=None, *, reason=None):
        await ctx.message.delete()
        if ctx.author.top_role == member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':shushing_face: Мьют:', value = random.choice(answer5))
            await ctx.send(embed=emb, delete_after=30)

            return


        elif member == ctx.bot.user:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':shushing_face: Мьют:', value = random.choice(answer4))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif ctx.author.top_role < member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':shushing_face: Мьют:', value = random.choice(answer3))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif member == ctx.author:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':shushing_face: Мьют:', value = random.choice(answer))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif member == ctx.guild.owner:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':shushing_face: Мьют:', value = random.choice(answer2))
            await ctx.send(embed=emb, delete_after=30)

            return
        emb = discord.Embed()
        emb.add_field(name=':shushing_face: Мьют:', value = f'Вы уверены, что хотите замьютить `{member.name}`?')
        emb.set_footer(text='Не нажимайте на галочку, если это ошибка!')
        msg = await ctx.send(embed=emb, delete_after = 30)
        await msg.add_reaction('✅')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check = check)
        except asyncio.TimeoutError:
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=':shushing_face: Мьют:', value = 'Действие отменнено!')
            await ctx.send(embed = emb, delete_after=30 )
        else:

            if duration == None:
                if reason == None:
                    try:
                        progress = await ctx.send('Мьючу пользователя!', delete_after = 5)
 
                        emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                        emb.add_field( name = ':shushing_face: Мьют:', value = f'Участник `{member.name}` замьючен!\nОн не выйдет из мута, пока его не размьютят!', inline = False)
                        emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                        await ctx.send( embed = emb)
   

                        for channel in ctx.guild.text_channels:
                            await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
    
                        for channel in ctx.guild.voice_channels:
                            await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
                    except:
                        success = False
                    else:
                        success = True

                    emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                    emb.add_field( name = ':shushing_face: Мут:', value = f'Вы, `{member.name}` замьючены на сервере `{ ctx.guild.name }`!\nВы не выйдете из мьюта, пока вас не размутят!', inline = False)
                    emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                    await member.send( embed = emb)


                    return


                try:
                    progress = await ctx.send('Мьючу пользователя!', delete_after = 5)

                    emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                    emb.add_field( name = ':shushing_face: Мьют:', value = f'Участник `{member.name}` замьючен!\nОн не выйдет из мьюта, пока его не размутят!', inline = False)
                    emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                    await ctx.send( embed = emb)
  

                    for channel in ctx.guild.text_channels:
                        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
   
                    for channel in ctx.guild.voice_channels:
                        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
                except:
                    success = False
                else:
                    success = True

                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':shushing_face: Мьют:', value = f'Вы, `{member.name}` замьючены на сервере `{ ctx.guild.name }`!\nВы не выйдете из мута, пока вас не размутят!', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                await member.send( embed = emb)

                return


            unit = duration[-1]
            if unit == 'с':
                time = int(duration[:-1])
                longunit = 'секунд'
            elif unit == 's':
                time = int(duration[:-1])
                longunit = 'секунд'
            elif unit == 'м':
                time = int(duration[:-1]) * 60
                longunit = 'минуту/минут'
            elif unit == 'm':
                time = int(duration[:-1]) * 60
                longunit = 'минуту/минут'
            elif unit == 'ч':
                time = int(duration[:-1]) * 60 * 60
                longunit = 'час/часов'
            elif unit == 'h':
                time = int(duration[:-1]) * 60 * 60
                longunit = 'час/часов'
            elif unit == 'д':
                time = int(duration[:-1]) * 60 * 60 *24
                longunit = 'день/дней'
            elif unit == 'd':
                time = int(duration[:-1]) * 60 * 60 *24
                longunit = 'день/дней'
            else:
                await ctx.send('Неправильное написание времени!', delete_after = 30)
                return

            if reason == None:
                try:
                    progress = await ctx.send('Мьючу пользователя!', delete_after = 5)
 
                    emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                    emb.add_field( name = ':shushing_face: Мьют:', value = f'Участник `{member.name}` замучен!\nОн выйдет из мьюта через: {str(duration[:-1])} {longunit}', inline = False)
                    emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                    await ctx.send( embed = emb)

  
                    for channel in ctx.guild.text_channels:
                        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)

                    for channel in ctx.guild.voice_channels:
                        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
                except:
                    success = False
                else:
                    success = True

                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':shushing_face: Мьют:', value = f'Вы, `{member.name}` замьючены на сервере `{ ctx.guild.name }`!\nВы выйдете из мьюта через: {str(duration[:-1])} {longunit}', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                await member.send( embed = emb)
    
                await asyncio.sleep(time)
                try:
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(member, overwrite=None, reason=reason)
                except:
                    pass
 
                return
  
            try:
                progress = await ctx.send('Мьючу пользователя!', delete_after = 5)

                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':shushing_face: Мьют:', value = f'Участник `{member.name}` замьючен!\nОн выйдет из мьюта через: {str(duration[:-1])} {longunit}', inline = False)
                emb.add_field( name = 'По причине:', value = reason, inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                await ctx.send( embed = emb)


                for channel in ctx.guild.text_channels:
                    await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)

                for channel in ctx.guild.voice_channels:
                    await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
            except:
                success = False
            else:
                success = True

            emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
            emb.add_field( name = ':shushing_face: Мьют:', value = f'Вы, `{member.name}` замьючены на сервере `{ ctx.guild.name }`!\nВы выйдете из мьюта через: {str(duration[:-1])} {longunit}', inline = False)
            emb.add_field( name = 'По причине:', value = reason, inline = False)
            emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
  
            await member.send( embed = emb)
    
            await asyncio.sleep(time)
            try:
                for channel in ctx.guild.channels:
                    await channel.set_permissions(member, overwrite=None, reason=reason)
            except:
                pass


    @mute.error
    async def clear_error( self, ctx, error ):
        if isinstance( error, commands.CommandOnCooldown):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Мут:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb, delete_after = 10 )
        if isinstance( error, commands.BadArgument ):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Мут:', value = 'Вы что-то указали не то!' )
            await ctx.send( embed = emb, delete_after=30 )
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            await ctx.message.delete()
            emb = discord.Embed()
            emb.add_field( name = ':x: Мут:', value = 'Использование команды: `>mute [пользователь] <время> <причина>`' )
            await ctx.send( embed = emb, delete_after=30)
        if isinstance( error, commands.errors.MissingPermissions ):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Мут:', value = 'У вас не хватает прав!' )
            await ctx.send( embed = emb, delete_after=30 )
        
    @commands.command(aliases=['размьют'])
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    @commands.has_permissions( kick_members = True )
    async def unmute(self, ctx, member:discord.Member, *, reason=None):
        await ctx.message.delete()

        if ctx.author.top_role == member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':smiley: Размьют:', value = random.choice(answer5))
            await ctx.send(embed=emb, delete_after=30)

            return
        elif member == ctx.bot.user:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':smiley: Размьют:', value = random.choice(answer4))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif ctx.author.top_role < member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':smiley: Размьют:', value = random.choice(answer3))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif member == ctx.author:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':smiley: Размьют:', value = random.choice(answer))
            await ctx.send(embed=emb, delete_after=30)

            return

        elif member == ctx.guild.owner:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':smiley: Размьют:', value = random.choice(answer2))
            await ctx.send(embed=emb, delete_after=30)

            return
        emb = discord.Embed()
        emb.add_field(name=':smiley: Размьют:', value = f'Вы уверены, что хотите размьютить `{member.name}`?')
        emb.set_footer(text='Не нажимайте на галочку, если это ошибка!')
        msg = await ctx.send(embed=emb, delete_after = 30)
        await msg.add_reaction('✅')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check = check)
        except asyncio.TimeoutError:
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=':smiley: Размьют:', value = 'Действие отменнено!')
            await ctx.send(embed = emb, delete_after=30 )
        else:
            await ctx.send('Размучиваю пользователя', delete_after = 5)
            try:
                for channel in ctx.message.guild.channels:
                    await channel.set_permissions(member, overwrite=None, reason=reason)
            except:
                success = False
            else:
                success = True

            if reason == None:
                emb = discord.Embed( colour = discord.Color.green(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':smiley: Размьют:', value = f'Вы, `{member.name}` размьючены на сервере `{ ctx.guild.name }`!', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')

                await member.send( embed = emb)
            
                emb = discord.Embed( colour = discord.Color.green(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':smiley: Размьют:', value = f'Участник `{member.name}` размьючен!', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
                await ctx.send( embed = emb)

                return

            emb = discord.Embed( colour = discord.Color.green(), timestamp = ctx.message.created_at)
            emb.add_field( name = ':smiley: Размьют:', value = f'Вы, `{member.name}` размьючены на сервере `{ ctx.guild.name }`!', inline = False)
            emb.add_field( name = 'По причине:', value = reason, inline = False)
            emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
  
            await member.send( embed = emb)
            
            emb = discord.Embed( colour = discord.Color.green(), timestamp = ctx.message.created_at)
            emb.add_field( name = ':smiley: Размьют:', value = f'Участник `{member.name}` размьючен!', inline = False)
            emb.add_field( name = 'По причине:', value = reason, inline = False)
            emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
            await ctx.send( embed = emb)

    @unmute.error
    async def clear_error( self, ctx, error ):
        if isinstance( error, commands.CommandOnCooldown):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Размьют:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb, delete_after = 10 )
        if isinstance( error, commands.BadArgument ):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Размьют:', value = 'Вы указали что-то не то!' )
            await ctx.send( embed = emb, delete_after=30 )
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            await ctx.message.delete()
            emb = discord.Embed()
            emb.add_field( name = ':x: Размьют:', value = 'Использование команды: `>unmute [пользователь] <причина>`' )
            await ctx.send( embed = emb, delete_after=30 )
        if isinstance( error, commands.errors.MissingPermissions ):
            await ctx.message.delete()
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Размут:', value = 'У вас не хватает прав!' )
            await ctx.send( embed = emb, delete_after=30 )


def setup(client):
    client.add_cog(модерация(client))