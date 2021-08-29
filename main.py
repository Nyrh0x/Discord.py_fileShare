
import discord
from discord.ext import commands
import smtplib, ssl
import asyncio
import threading
import csv
import string
import secrets
from cryptography.fernet import Fernet


prefix  = '--'
client = commands.Bot(command_prefix=prefix, help_command=None)
#client = discord.Client()
client.remove_command('help')

blue_color = discord.Color.blue()
blu_color = 0x3FA8DA
error_color = 0xFF5733
green_color = discord.Color.green()

db_name = 'db'

def update_sources():
    global codes, items
    codes = []
    items = []
    with open(f'{db_name}.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            codes.append(row[0])
            items.append(row[1])

def generate():
    def check():
        if x in codes:
            generate()

    N = 5

    x = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    check()
    return x

def add_item(code, file):
    with open(f'{db_name}.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([code, file])
    update_sources()

def get_item(code):
    try:
        local = codes.index(code)
        return items[local]
    except:
        return "1"

@client.event
async def on_ready():
    print("Online")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{prefix}help"))

@client.command()
async def upload(ctx):
    try:
        attachment = ctx.message.attachments[0]
        file = attachment.url
        code = generate()
        embed = discord.Embed(description=f"Code : {code}",
                              color=green_color)
        await ctx.send(embed=embed)
        add_item(code, file)
    except:
        embed = discord.Embed(description="File missing!",
                              color=error_color)
        await ctx.send(embed=embed)

@client.command()
async def get(ctx):
    msg = ctx.message.content
    msg = msg.split("/")
    msg = msg[len(msg) - 1].split(" ")
    msg.remove('!get')

    if len(msg) == 1:
        item = get_item(msg[0])
        if item == "1":
            embed = discord.Embed(description="Inaccessible file",
                                  color=error_color)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=item,
                                  color=green_color)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="Invalid Variables",
                              color=error_color)
        await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    help_options = '''
    • '''

    embed = discord.Embed(color=blu_color)
    embed.set_author(name="Discord File Share", icon_url="https://cdn.discordapp.com/attachments/862792318133469267/881305795684352060/document-file-icon.png")
    embed.add_field(name="General Commands", value=f" • {prefix}help : List commands\n"
                                                   f" • {prefix}upload : upload file\n"
                                                   f" • {prefix}get "+"{} : Download a file using it's code",
                    inline=False)
    embed.add_field(name="Bot options", value=f"[ Invite bot! ](https://discord.com/api/oauth2/authorize?client_id=881259301052768266&permissions=3072&scope=bot)",
                    inline=False)
    embed.set_footer(text="© Copyright 2021. Credits go to h4sh3d")
    await ctx.send(embed=embed)

update_sources()
client.run('')
