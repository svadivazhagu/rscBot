#rscBot, the solution for manual gathering of friends to play games with on the VoIP app Discord

#Created by Surya Vadivazhagu (svadivazhagu on Github) & Daniel McDonough (Mcdonoughd) for the Hack @ WPI 2018 Hackathon

import csv

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print ('Ready when you are, with username: ' + bot.user.name + " and the ID: " + bot.user.id)

@bot.command(pass_context=True)
async def pingPongGame(ctx):
    await bot.say(":ping_pong: ping!")
    print ("user has pinged")

@bot.command(pass_context=True)
async def hello(ctx):
    await bot.say("HELLO WORLD!")
    print("Hello World!")

#Client event commented out for now, as bot commands seem to be more efficient for our tasks.
# @client.event
# async def on_message(message):
#     if message.content.startswith('$start'):
#         await client.send_message(message.channel, 'Type $stop 4 times.')
#         for i in range(4):
#             msg = await client.wait_for_message(author=message.author, content='$stop')
#             fmt = '{} left to go.' + message.author.id
#             await client.send_message(message.channel, fmt.format(3 - i))
#
#         await client.send_message(message.channel, 'Good job!')


# IF I FORGET THIS IS HOW TO FETCH USER ID STRAIGHT OFF THEIR MESSAGE
@bot.command(pass_context=True)
async def myid(ctx):
    await bot.say(ctx.message.author.nick + "'s User ID: " + ctx.message.author.id)
    print("User " + ctx.message.author.nick + " requested their User ID, which is " + ctx.message.author.id)
    await bot.send_message(discord.User(id=ctx.message.author.id), "testing")


@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x00ffff)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

#Kicks Users. IDK why this is here.
@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    await bot.say(":boot: Cya, {}. Ya loser!".format(user.name))
    await bot.kick(user)

#Adds user ID under game entry in CSV file
@bot.command(pass_context=True)
async def add(ctx):
    word = arg
    await bot.say(word)

#Adds Game entry in CSV file
@bot.command(pass_context=True)
async def create(ctx, message):
    splitMsg = ctx.message.content.split(" ")[1].lower()
    fullWord = ''.join(ctx.message.content.split(" ")[1])

    with open("gameList.csv", "a") as csvfile:
        filewriter =csv.writer(csvfile, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([splitMsg])
    await bot.say(fullWord + " has been added to the game list.")

#client.run('MzkyOTE3OTU1NDQ2MzA4ODY1.DRuPOw.Z3aGgdvDuKP8wAkHMt2vSPSEwZ4')
bot.run('NDAxNjM3MTIzNzgzOTE3NTY4.DTtFPQ.t9TTZ5qM2KNoDXr87LpvxVxqMgc')

#SURYA AUTH: NDAxNjM3MTIzNzgzOTE3NTY4.DTtFPQ.t9TTZ5qM2KNoDXr87LpvxVxqMgc
#DAN AUTH: NDAxNTM4OTU0NDg4MTg0ODMy.DTrriQ.y2QzATd4j8PVsHkuhlwv7Azmnyc
