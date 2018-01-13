#firstbot

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import csv
import time

bot = commands.Bot(command_prefix='!')
client = discord.Client()


@bot.event
async def on_ready():
    print ('Ready when you are xd')
    print ("I am running on " + bot.user.name)
    print ("With the ID: " + bot.user.id)
@client.event
async def on_ready():
    print ('Ready when you are xd')
    print ("I am running on " + client.user.name)
    print ("With the ID: " + client.user.id)

@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say(":ping_pong: ping!    ! xSSS")
    print ("user has pinged")

@bot.command(pass_context=True)
async def hello(ctx):
    await bot.say("HELLO WORLD!")
    print("Hello World!")

@client.event
async def on_message(message):
    if message.content.startswith('$start'):
        await client.send_message(message.channel, 'Type $stop 4 times.')
        for i in range(4):
            msg = await client.wait_for_message(author=message.author, content='$stop')
            fmt = '{} left to go.' + message.author.id
            await client.send_message(message.channel, fmt.format(3 - i))

        await client.send_message(message.channel, 'Good job!')
@bot.command(pass_context=True)
async def myid(ctx):
    await bot.say("YOUR ID IS: " + ctx.author.id)
    print("Your ID is: " + ctx.author)

@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    await bot.say("The users name is: {}".format(user.name))
    await bot.say("The users ID is: {}".format(user.id))
    await bot.say("The users status is: {}".format(user.status))
    await bot.say("The users highest role is: \"{}\"".format(user.top_role))
    await bot.say("The user joined at: {}".format(user.joined_at))

@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    await bot.say(":boot: Cya, {}. Ya loser!".format(user.name))
    await bot.kick(user)

@bot.command(pass_context=True)
async def add(ctx, arg):
    word = arg
    await bot.say(word)

@bot.command(pass_context=True)
async def addGame(ctx, message):
    splitMsg = ctx.message.content.split(" ")
    with open("gameList.csv", "a") as csvfile:
        filewriter =csv.writer(csvfile, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([splitMsg[1]])
    await bot.say(splitMsg[1] + " has been added to the game list.")
#client.run('MzkyOTE3OTU1NDQ2MzA4ODY1.DRuPOw.Z3aGgdvDuKP8wAkHMt2vSPSEwZ4')
bot.run('MzkyOTE3OTU1NDQ2MzA4ODY1.DRuPOw.Z3aGgdvDuKP8wAkHMt2vSPSEwZ4')

#SURYA AUTH: MzkyOTE3OTU1NDQ2MzA4ODY1.DRuPOw.Z3aGgdvDuKP8wAkHMt2vSPSEwZ4
#DAN AUTH: NDAxNTM4OTU0NDg4MTg0ODMy.DTrriQ.y2QzATd4j8PVsHkuhlwv7Azmnyc
