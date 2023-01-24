from os import name
from typing import DefaultDict
from aiohttp.client import request
from asyncio.tasks import sleep
import discord
from discord import member
from discord.ext import commands
from discord.utils import get
import datetime
import random
import requests
from bs4 import BeautifulSoup
import asyncio
import json
from discord.ui import Button, View
import time



intents = discord.Intents.all()
#intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

dick = {}

def load_storage():
    with open('storage.json') as data:
        storage = json.load(data)
    return storage

def dump_storage(storage):
    with open('storage.json', 'w') as data:
        json.dump(storage, data)

storage = load_storage()

@bot.event
async def on_ready():
    print(bot.user.id)
    print("Success")

#Member Accept
@bot.event
async def on_member_join(member):
    user_button = Button(label = 'User', style = discord.ButtonStyle.green, custom_id = 'user')
    #guest_button = Button(label = 'Guest', style = discord.ButtonStyle.grey, custom_id = 'guest')
    kick_button = Button(label = 'Kick', style = discord.ButtonStyle.red, custom_id = 'kick')

    storage = load_storage()
    guild = member.guild
    channel = await bot.fetch_channel(865525769623175168)
    #Create Embed
    current_time = time.strftime('%Y.%m.%d | %X')
    embed = discord.Embed(title = 'New Member Joined', color=0x000000)
    embed.add_field(name='Name', value=member.mention, inline=False)
    embed.add_field(name='Joined', value=current_time, inline=False)
    #Send a new message with Buttons (for admin)
    async def callback(interaction):
        if member != None:
            nonlocal embed
            user_button.disabled = kick_button.disabled = True
            message = interaction.message
            await message.edit(embed = embed, view = view)

            if interaction.data['custom_id'] == 'user':
                approve_time = time.strftime('%Y.%m.%d | %X')
                role = discord.utils.get(guild.roles, name = 'User')
                embed.color = 0x00FF00
                embed.add_field(name = 'Approved', value = approve_time, inline = False)
                await member.add_roles(role)
            # elif interaction.data['custom_id'] == 'guest':
            #     role = discord.utils.get(guild.roles, name = 'Guest')
            #     embed = discord.Embed(title = 'New Guest Joined', color = 0x7C7C7C)
            #     embed.add_field(name='Name', value=member.mention, inline=False)
            #     embed.add_field(name='Sign up', value=current_time, inline=False)
            elif interaction.data['custom_id'] == 'kick':
                kick_time = time.strftime('%Y.%m.%d | %X')
                embed.title = f'{member.name}#{member.discriminator} Kicked'
                embed.color = 0xFF0000
                embed.add_field(name = 'Kicked', value = kick_time, inline = False)
                await member.kick()
            await interaction.response.edit_message(embed = embed)
        else:
            embed = discord.Embed(title = 'Member Not Found', color = 0x000000)
            await interaction.response.edit_message(embed = embed)
        storage
    user_button.callback = kick_button.callback = callback
    view = View()
    view.add_item(user_button)
    #view.add_item(guest_button)
    view.add_item(kick_button)
    await channel.send(embed = embed, view = view)

    # storage['member_join_messages'][str(message.id)] = member.id
    # dump_storage(storage)   

# 참고 : 코루틴과 태스크 https://docs.python.org/ko/3/library/asyncio-task.html
async def channel_good(ctx):
    if ctx.channel.id != 909803903627984896:
        a = await ctx.reply("<#909803903627984896> 채널에서 사용해주세요 !")
        await asyncio.sleep(5)
        await a.delete()
        await ctx.message.delete()
        return 0
    else:
        return 1

@bot.command(aliases=['random','랜덤','골라줘'])
async def random_(ctx,*temp):
    if await channel_good(ctx) == 0: return 0

    result = random.choice(temp)
    await ctx.reply(f"{result} 을(를) 뽑았지 뭐얌")

@bot.command(aliases=['ㄹㅈㅈ','롤전적'])
async def lolhistory_(ctx, p_name):
    if await channel_good(ctx) == 0: return 0

    rankcolor = {
        "iorn": 0x3b3537,
        "bronze": 0x5d3a27,
        "silver": 0x3f4a50,
        "gold": 0xcfbf83,
        "platinum": 0x385455,
        "diamond": 0x5660a7,
        "master":0xd1aee6,
        "grandmaster":0xcb585d,
        "challenger": 0xfcd39d
    }
    try:
        webpage = requests.get(f"http://fow.kr/find/{p_name}")
        soup = BeautifulSoup(webpage.content, "html.parser")
        result = soup.select_one(".table_summary > div:nth-child(2) > div:nth-child(2) > b:nth-child(5) > font:nth-child(1)").get_text()
        temp = result.split(" ")
        color = int(rankcolor[temp[0].lower()])
        embed = discord.Embed(title = '롤 전적'   , color=color)
        embed.add_field(name='rank', value=result, inline=False)
        await ctx.reply(embed = embed)
    except:
        await ctx.reply("`Unrank` 이거나 **존재하지 않는** 계정입니다.")

@bot.command(aliases=['연애확률','ㅇㅇㅎㄹ'])
async def love_(ctx):
    if await channel_good(ctx) == 0: return 0

    result = round(random.uniform(0, 100),2)   
    await ctx.reply(f"{ctx.author.mention} 님의 연애확률은 `{str(result)}%` 입니다.")

@bot.command(aliases=['주사위','ㅈㅅㅇ','dice'])
async def dice_(ctx):
    if await channel_good(ctx) == 0: return 0
    
    dice = {
        "1": "https://cdn.discordapp.com/attachments/906931181843546122/906936759567388712/dice-six-faces-one.png",
        "2": "https://cdn.discordapp.com/attachments/906931181843546122/906936763648475237/dice-six-faces-two.png",
        "3": "https://cdn.discordapp.com/attachments/906931181843546122/906936762104950814/dice-six-faces-three.png",
        "4": "https://cdn.discordapp.com/attachments/906931181843546122/906936758061629490/dice-six-faces-four.png",
        "5": "https://cdn.discordapp.com/attachments/906931181843546122/906936756249722880/dice-six-faces-five.png",
        "6": "https://cdn.discordapp.com/attachments/906931181843546122/906936760884416552/dice-six-faces-six.png"
    }
    result = str(random.randint(1,6))
    #await ctx.send(dice[result])
    await ctx.send(dice[result])


@commands.has_permissions(administrator=True)
@bot.command(aliases = ['joinhere', 'joinchannel', 'creationchannel'])
async def add_creation_channel(ctx, channel_id: int = None):
    if channel_id == None:
        await ctx.send('List of *Join to Create* Channels\n')
        for i in storage['creation_channels']:
            await ctx.send(f'<#{i}>')
    else:
        #Add the channel_id to storage.json
        if channel_id not in storage['creation_channels']:
            storage['creation_channels'].append(channel_id)
            #Return a confirm message
            return_message = f'<#{channel_id}> added to the list'
            await ctx.send(return_message)
        else:
            #Return an error message
            return_message = f'<#{channel_id}> is already in the list'
            await ctx.send(return_message)
        dump_storage(storage)

@commands.has_permissions(administrator=True)
@bot.command(aliases = ['joinheredel', 'joinchanneldel', 'creationchanneldel'])
async def del_creation_channel(ctx, channel_id :int):
    #Remove the channel_id from storage.json
    if channel_id in storage['creation_channels']:
        storage['creation_channels'].remove(channel_id)
        #Return a confirm message
        return_message = f'<#{channel_id}> removed from the list'
        await ctx.send(return_message)
    else:
        #Return an error message
        return_message = f'<#{channel_id}> is not in the list'
        await ctx.send(return_message)
    dump_storage(storage)
    
 
@bot.event
async def on_voice_state_update(member: member, before, after):
    #Delete Channel
    try:
        if before.channel.id in storage['created_channels'] and len([i for i in before.channel.members if i.bot == False]) == 0:
            storage['created_channels'].remove(before.channel.id)
            await before.channel.delete()
            dump_storage(storage)
    except:
        pass

    #Create Channel
    try:
        if before.channel != after.channel and after.channel.id in storage['creation_channels']:
            guild = member.guild

            v_channel = await guild.create_voice_channel(f"{random.randint(1,100)}", category = after.channel.category, bitrate = after.channel.bitrate, user_limit = after.channel.user_limit)
            storage['created_channels'].append(v_channel.id)

            dump_storage(storage)
            await member.move_to(v_channel)
    except:
        pass

@commands.has_permissions(administrator=True)
@bot.command(aliases=['clear','청소'])
async def clear_(ctx, li):
    await ctx.channel.purge(limit = int(li) + 1)
    a = await ctx.send(f"{ctx.author.mention}, {int(li)}개의 메세지 삭제.", delete_after = 3)

@bot.command(aliases=['타이머','timer'])
async def timer_(ctx,arg):
    if await channel_good(ctx) == 0: return 0

    if arg.isdecimal() == False:
        await ctx.reply('숫자는 자연수로 입력해 주세요.')
        return 0

    await ctx.reply(f'{arg}분 타이머를 시작합니다. 끝나면 Dm으로 알려줄게요.')
    await asyncio.sleep(int(arg)*60)
    try:
        await ctx.author.send(f'{arg}분 타이머가 끝났어요 !')
    except:
        await ctx.reply(f'{arg}분 타이머가 끝났어요 ! \n`디엠으로 받으려면 서버 멤버가 보내는 개인 메세지 허용을 켜주세요`')

@bot.command(aliases=['lolnk'])
async def nickfind_(ctx, *arg):
    if await channel_good(ctx) == 0: return 0

    count = 0
    rt = []
    print(len(arg))
    for i in arg:
        url = 'http://fow.kr/find/' + i
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            result = soup.select_one(".small > span:nth-child(1)").get_text()
        except:
            rt.append(i)
            count += 1

    await ctx.reply(f'found {count} \n{rt}')
    print(f'found {count}')

@bot.command()
async def dm(ctx, arg1, arg2):
    a = await bot.fetch_user(arg1)
    await a.send(arg2)


with open('token.txt', 'r') as f:
    token = f.readline()
print(token)
bot.run(token)
