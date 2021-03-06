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
from discord_components import *
import time



intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
DiscordComponents(bot)

dick = {}

def load_storage():
    with open('storage.json') as data:
        storage = json.load(data)
    return storage

def dump_storage(storage):
    with open('storage.json', 'w') as data:
        json.dump(storage, data)

@bot.event
async def on_ready():
    print(bot.user.id)
    print("Success")

#Member Accept
@bot.event
async def on_member_join(member):
    storage = load_storage()
    guild = member.guild
    channel = await bot.fetch_channel(865525769623175168)
    #Create Embed
    current_time = time.strftime('%Y.%m.%d | %X')
    embed = discord.Embed(title = 'New Member Joined', color=0x000000)
    embed.add_field(name='Name', value=member.mention, inline=False)
    embed.add_field(name='Sign up', value=current_time, inline=False)
    #Send a new message with Buttons (for admin)
    message = await channel.send(
        embed=embed, 
        components = 
            ActionRow([
                Button(label = 'User', style = ButtonStyle.green),
                Button(label = 'Guest', style = ButtonStyle.grey),
                Button(label = 'Kick', style = ButtonStyle.red)
        ])
        )
    storage['member_join_messages'][str(message.id)] = member.id
    dump_storage(storage)
    while 1:
        interaction = await bot.wait_for("button_click")
        storage = load_storage()
        member_id = storage['member_join_messages'][str(interaction.message.id)]
        member = guild.get_member(member_id)
        if member != None:
            current_time = time.strftime('%Y.%m.%d | %X')
            disable_components = [row.disable_components() for row in interaction.message.components]
            
            #Choose what role to give / Kick
            if interaction.component.label == 'User':
                role = discord.utils.get(guild.roles, name = 'User')
                embed = discord.Embed(title = 'New **Member** Joined', color=0x08FF00)
                embed.add_field(name='Name', value=member.mention, inline=False)
                embed.add_field(name='Sign up', value=current_time, inline=False)
                await interaction.edit_origin(embed = embed, components = disable_components)
            elif interaction.component.label == 'Guest':
                role = discord.utils.get(guild.roles, name = 'Guest')
                embed = discord.Embed(title = 'New Member Joined', color=0x7C7C7C)
                embed.add_field(name='Name', value=member.mention, inline=False)
                embed.add_field(name='Sign up', value=current_time, inline=False)
                await interaction.edit_origin(embed = embed, components = disable_components)
            elif interaction.component.label == 'Kick':
                await member.kick()
                role = None
                embed = discord.Embed(title = 'New Member Joined', color=0xFF0000)
                embed.add_field(name='Name', value=member.mention, inline=False)
                embed.add_field(name='Sign up', value=current_time, inline=False)
                await interaction.edit_origin(embed = embed, components = disable_components)
            
            #Give roles
            if role != None:
                await member.add_roles(role)
            del(storage['member_join_messages'][str(interaction.message.id)])
            with open('storage.json', 'w') as data:
                json.dump(storage, data)
        else:
            embed = discord.Embed(title = 'Member Not Found', color = 0x000000)
            await interaction.edit_origin(embed = embed, delete_after = 3)

# ?????? : ???????????? ????????? https://docs.python.org/ko/3/library/asyncio-task.html
async def channel_good(ctx):
    if ctx.channel.id != 909803903627984896:
        a = await ctx.reply("<#909803903627984896> ???????????? ?????????????????? !")
        await asyncio.sleep(5)
        await a.delete()
        await ctx.message.delete()
        return 0
    else:
        return 1

@bot.command(aliases=['random','??????','?????????'])
async def random_(ctx,*temp):
    if await channel_good(ctx) == 0: return 0

    result = random.choice(temp)
    await ctx.reply(f"{result} ???(???) ????????? ??????")

@bot.command(aliases=['?????????','?????????'])
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
        embed = discord.Embed(title = '??? ??????'   , color=color)
        embed.add_field(name='rank', value=result, inline=False)
        await ctx.reply(embed = embed)
    except:
        await ctx.reply("`Unrank` ????????? **???????????? ??????** ???????????????.")

@bot.command(aliases=['????????????','????????????'])
async def love_(ctx):
    if await channel_good(ctx) == 0: return 0

    result = round(random.uniform(0, 100),2)   
    await ctx.reply(f"{ctx.author.mention} ?????? ??????????????? `{str(result)}%` ?????????.")

@bot.command(aliases=['?????????','?????????','dice'])
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
        with open('storage.json') as data:
            storage = json.load(data)
        for i in storage['creation_channels']:
            await ctx.send(f'<#{i}>')
    else:
        #Add the channel_id to storage.json
        with open('storage.json') as data:
            storage = json.load(data)
        if str(channel_id) not in storage['creation_channels']:
            storage['creation_channels'].append(channel_id)
            #Return a confirm message
            return_message = f'<#{channel_id}> added to the list'
            await ctx.send(return_message)
        else:
            #Return an error message
            return_message = f'<#{channel_id}> is already in the list'
            await ctx.send(return_message)
        with open('storage.json', 'w') as data:
            json.dump(storage, data)

@commands.has_permissions(administrator=True)
@bot.command(aliases = ['joinheredel', 'joinchanneldel', 'creationchanneldel'])
async def del_creation_channel(ctx, channel_id :int):
    #Remove the channel_id from storage.json
    with open('storage.json') as data:
        storage = json.load(data)
    if channel_id in storage['creation_channels']:
        storage['creation_channels'].remove(channel_id)
        #Return a confirm message
        return_message = f'<#{channel_id}> removed from the list'
        await ctx.send(return_message)
    else:
        #Return an error message
        return_message = f'<#{channel_id}> is not in the list'
        await ctx.send(return_message)
    with open('storage.json', 'w') as data:
        json.dump(storage, data)
    
 
@bot.event
async def on_voice_state_update(user, before, after):
    with open('storage.json') as data:
        storage = json.load(data)
    #Delete Channel
    if before.channel == None:
        pass
    elif before.channel.id in storage['created_channels'] and str(before.channel.members).count('bot=False') == 0:
        await before.channel.delete()
        storage['created_channels'].remove(before.channel.id)
        with open('storage.json', 'w') as data:
            json.dump(storage, data)
    #Create Channel
    if after.channel == None:
        pass
    elif after.channel.id in storage['creation_channels']:
        guild = user.guild
        channel = await guild.create_voice_channel(f"{user.display_name}'s channel", category = after.channel.category, bitrate = after.channel.bitrate, user_limit = after.channel.user_limit)
        await user.move_to(channel)
        if channel.id not in storage['created_channels']:
            storage['created_channels'].append(channel.id)
        with open('storage.json', 'w') as data:
            json.dump(storage, data)

@commands.has_permissions(administrator=True)
@bot.command(aliases=['clear','??????'])
async def clear_(ctx, li):
    await ctx.channel.purge(limit = int(li) + 1)
    a = await ctx.send(f"{ctx.author.mention}, {int(li)}?????? ????????? ??????.")
    await asyncio.sleep(3)
    await a.delete()

@bot.command(aliases=['?????????','timer'])
async def timer_(ctx,arg):
    if await channel_good(ctx) == 0: return 0

    if arg.isdecimal() == False:
        await ctx.reply('????????? ???????????? ????????? ?????????.')
        return 0

    await ctx.reply(f'{arg}??? ???????????? ???????????????. ????????? Dm?????? ???????????????.')
    await asyncio.sleep(int(arg)*60)
    try:
        await ctx.author.send(f'{arg}??? ???????????? ???????????? !')
    except:
        await ctx.reply(f'{arg}??? ???????????? ???????????? ! \n`???????????? ???????????? ?????? ????????? ????????? ?????? ????????? ????????? ????????????`')

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
