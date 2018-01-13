# rscBot, the solution for manual gathering of friends to play games with on the VoIP app Discord

# Created by Surya Vadivazhagu (svadivazhagu on Github) & Daniel McDonough (Mcdonoughd) for the Hack @ WPI 2018 Hackathon

import csv
import numpy as np
import discord
from discord.ext import commands
import os
import time

bot = commands.Bot(command_prefix='!')
global gameList
global userList
global binary

#Import the csv of Game Names into a 1 x G matrix (G = # of Games
def import_gameList(filename='gameList.csv'):
    if os.stat(filename).st_size != 0:
        f = open(filename, "r")
        gameList = np.genfromtxt(filename, dtype='str', delimiter=' ')
        f.close()
        return gameList

#Import the csv of User IDs into a 1 x U matrix (U = # of users)
def import_userList(filename='userList.csv'):
    if os.stat(filename).st_size != 0:
        f = open(filename, "r")
        userList = np.genfromtxt(filename, dtype='str', delimiter=' ')
        #print(userList)
        f.close()
        return userList

'''
Import the csv of User IDs into a G x U  binary matrix where
1 = they have the game
0 = dont have the game
'''
def import_binary(filename='Bmatrix.csv'):
    if os.stat(filename).st_size != 0:
        f = open(filename, "r")
        binaryMatrix = np.genfromtxt(filename, dtype='int', delimiter=' ')
        #print(binaryMatrix)
        f.close()
        return binaryMatrix

gameList = import_gameList('gameList.csv')
binary = import_binary('Bmatrix.csv')
userList = import_userList('userList.csv')

#returns game index from a string
def findGameIndex(game_name):
    gameList = import_gameList()
    if type(gameList) != type(None):
        for i in range(len(gameList)):
            if gameList[i] == game_name:
                return i

#returns game name from a index
def findGameName(index):
    gameList = import_gameList()
    if type(gameList) != type(None):
        if len(gameList) <= index:
            return gamelist[index]

@bot.event
async def on_ready():
    #on start up ge list of all members and add them to the matrix
    print(gameList)
    print(userList)
    print('Ready when you are, with username: ' + bot.user.name + " and the ID: " + bot.user.id)

@bot.event
async def on_member_join(member):
    print(member.id)

@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say(":ping_pong: pong!")
    print("user has pinged")


@bot.command(pass_context=True)
async def hello(ctx):
    await bot.say("HELLO WORLD!")
    print("Hello World!")

# Client event commented out for now, as bot commands seem to be more efficient for our tasks.
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




@bot.command(pass_context=True)
async def recruit(ctx):
    await bot.send_message(discord.User(id = ctx.message.author.id), 'Type yes if you can join; no if you cannot.')
    userDecision = await bot.wait_for_message(timeout = 5, author=ctx.message.author)
    if type(userDecision) == type(None):
        await bot.send_message(discord.User(id=ctx.message.author.id), "You didn't make it in time!")
        await bot.say(ctx.message.author.display_name + " didn't respond in time.")
    elif str(userDecision.content) == "no":
        await bot.say(ctx.message.author.display_name + " is not going to join.")
    else:
        await bot.say(ctx.message.author.display_name + " is going to join!")

@bot.command(pass_context=True)
async def recruitUser(ctx, user: discord.Member):
    await bot.send_message(discord.User(id=user.id), 'Type yes if you can join; no if you cannot.')
    userDecision = await bot.wait_for_message(timeout=5, author=user)
    if type(userDecision) == type(None):
        await bot.send_message(discord.User(id=user.id), "You didn't make it in time!")
        await bot.say(user.display_name + " didn't respond in time.")
    elif str(userDecision.content) == "no":
        await bot.say(user.display_name + " is not going to join.")
    else:
        await bot.say(user.display_name + " is going to join!")

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


# Kicks Users. IDK why this is here.
@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    await bot.say(":boot: Cya, {}. Ya loser!".format(user.name))
    await bot.kick(user)

# Adds user ID under game entry in CSV file
@bot.command(pass_context=True)
async def add(ctx):
    splitMsg = ctx.message.content.split(" ")[1].lower()
    userid = ctx.message.author.id
    game = ''.join(ctx.message.content.split(" ")[1])
    with open(userList, "a") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([userid])
    await bot.say(game + " has been added to your game list.")

'''
# Adds user ID in new column game entry in CSV file when they play the game with discord running in the background
@bot.event
async def on_member_update():
    This checks updates for one user (ie games)
'''

# Adds user to specific instance of a game
@bot.command(pass_context=True)
async def join(ctx):
    await bot.say("YOU RAN JOIN")
    splitMsg = ctx.message.content.split(" ")[1].lower()



# Adds Game entry in CSV file
@bot.command(pass_context=True)
async def create(ctx):
    splitMsg = ctx.message.content.split(" ")[1].lower()
    fullWord = ''.join(ctx.message.content.split(" ")[1])

    with open('gameList.csv', "a") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([splitMsg])
    await bot.say(fullWord + " has been added to the game list.")


# Lists all games added in the csv file
@bot.command(pass_context=True)
async def gamelist(ctx):
    gameList = import_gameList()
    if type(gameList) != type(None):
        #print(type(gameList))
        await bot.say("We got:")
        for i in range(len(gameList)):
            #print(i)
            #print(gameList[i])
            await bot.say(gameList[i])
    else:
        await bot.say("Game List is empty")

@bot.command(pass_context=True)
async def onlineCheck(ctx):
   # print(bot.get_all_members())
    for server in bot.servers:
        for member in server.members:
            if member.status == discord.Status.online:
                await bot.say(member)


# client.run('MzkyOTE3OTU1NDQ2MzA4ODY1.DRuPOw.Z3aGgdvDuKP8wAkHMt2vSPSEwZ4')
bot.run('NDAxNjM3MTIzNzgzOTE3NTY4.DTtFPQ.t9TTZ5qM2KNoDXr87LpvxVxqMgc')

# SURYA AUTH: NDAxNjM3MTIzNzgzOTE3NTY4.DTtFPQ.t9TTZ5qM2KNoDXr87LpvxVxqMgc
# DAN AUTH: NDAxNTM4OTU0NDg4MTg0ODMy.DTrriQ.y2QzATd4j8PVsHkuhlwv7Azmnyc
