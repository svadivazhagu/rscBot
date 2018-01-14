# rscBot, the solution for manual gathering of friends to play games with on the VoIP app Discord

# Created by Surya Vadivazhagu (svadivazhagu on Github) & Daniel McDonough (Mcdonoughd) for the Hack @ WPI 2018 Hackathon

import csv
import numpy as np
import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!')

global gameList
global userList
global binary
# Load the csv of Game Names into a 1 x G matrix (G = # of Games)
def import_gameList(filename='gameList.csv'):

    if os.stat(filename).st_size != 0:
        f = open(filename, "r")
        gameList = np.genfromtxt(filename, dtype='str', delimiter=' ')
        f.close()
        print(type(gameList))
        #gameList.shape = (1, len(gameList))
        print(gameList.shape)
        print(gameList.size)
        print(gameList)
        return gameList
    else:
        gameList = np.empty((1, 1), dtype='str')
        return gameList


# Import the csv of User IDs into a 1 x U matrix (U = # of users)
def import_userList(filename='userList.csv'):
    # check for empty file
    if os.stat(filename).st_size != 0:
        print("HELLO!")
        f = open(filename, "r")
        userList = np.genfromtxt(filename, dtype='str', delimiter=' ')
        f.close()
        userList.shape = (1, len(userList))
        print(userList.shape)
        print(type(userList))
        # load all users
        for server in bot.servers:
            for member in server.members:
                print(type(userList))
                if type(userList) != type(None):  # check if user list is empty
                    # if not empty then check ids with current file
                    for i in range(len(userList)):
                        print(member.id)
                        print(userList[i])
                        if member.id == userList[i]:
                            print(member.id + "Was found")  # they are already in the file
                        else:  # add them
                            with open(filename, "a") as csvfile:
                                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                                                        quoting=csv.QUOTE_MINIMAL)
                                filewriter.writerow([member.id])
                else:  # add all users to file
                    print(member.id)
                    with open(filename, "a") as csvfile:
                        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        filewriter.writerow([member.id])

        print(userList.shape)
        print(userList)
        return userList


# Import the csv of User IDs into a G x U  binary matrix where
# 1 = they have the game
# 0 = they do not have the game

def import_binary(filename='Bmatrix.csv'):
    global binary
    if os.stat(filename).st_size != 0:
        f = open(filename, "r")
        binary = np.genfromtxt(filename, dtype='int', delimiter=' ')
        # print(binaryMatrix)
        # load lists
        userList = import_userList()
        gameList = import_gameList()
        # check if any list is empty
        if type(userList) != type(None) & type(gameList) != type(None) & type(binary) != type(None):
            binary.shape = (len(gameList), len(userList))
            print(binary.shape)
            print(binary)

        elif type(userList) != type(None) & type(gameList) != type(None):
            binary = np.zeros((len(gameList), len(userList)), dtype=int)
            print(binary)

        else:
            binary = np.zeros((1, 1), dtype=int)
            print(binary)

        f.close()
        return binary


# returns game index from a string
def findGameIndex(game_name):
    global gameList
    gameList = import_gameList()
    if type(gameList) != type(None):
        for i in range(len(gameList)):
            if gameList[i] == game_name:
                return i
    return None


# returns game name from a index
def findGameName(index):
    global gameList
    gameList = import_gameList()
    if type(gameList) != type(None):
        if len(gameList) <= index:
            return gamelist[index]
    return None


def findUserIndex(user_id):
    global userList
    userList = import_userList()
    if type(userList) != type(None):
        for i in range(len(userList)):
            if userList[i] == user_id:
                return i
    return None


def findUserId(index):
    global userList
    userList = import_userList()
    if userList != type(None):
        if len(userList) <= index:
            return userList[index]
    return None


@bot.event
async def on_ready():
    #
    # on start up get list of all members and add them to the matrix
    print('Loading Game List...')
    global gameList
    gameList = import_gameList()
    print('Loading User List...')
    global userList
    userList = import_userList()
    # loadUsers(userList)  # load any new users
    print('Loading Binary Relations...')
    global binary
    print('Ready when you are, with username: ' + bot.user.name + " and the ID: " + bot.user.id)


'''
@bot.event
async def on_member_join(member):
    if type(userList) != type(None):  # check if user list is empty
        # if not empty then check ids with current file
        if member.id in userList:
            print(member.id + "Was found")  # they are already in the file
        else:  # add them
            with open('userlist.csv', "a") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([member.id])
    else:  # add all users to file
        with open('userlist.csv', "a") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow([member.id])
'''


@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say(":ping_pong: pong!")
    print("user has pinged")


@bot.command(pass_context=True)
async def hello(ctx):
    await bot.say("HELLO WORLD!")
    print("Hello World!")


@bot.command(pass_context=True)
async def recruit(ctx):
    await bot.send_message(discord.User(id=ctx.message.author.id),
                           'Type yes if you can join, no if you cannot. You have one minute to respond.')
    userDecision = await bot.wait_for_message(timeout=60, author=ctx.message.author)
    if type(userDecision) == type(None):
        await bot.send_message(discord.User(id=ctx.message.author.id), "You didn't make it in time!")
        await bot.say(ctx.message.author.display_name + " didn't respond in time.")
    elif str(userDecision.content) == "no":
        await bot.say(ctx.message.author.display_name + " is not going to join.")
    else:
        await bot.say(ctx.message.author.display_name + " is going to join!")


@bot.command(pass_context=True)
async def recruitUser(ctx, user: discord.Member):
    await bot.send_message(discord.User(id=user.id), 'Type yes if you can join; no if you cannot. You have one  minute')
    userDecision = await bot.wait_for_message(timeout=60, author=user)
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
    binary = import_binary()
    fullWord = ''.join(ctx.message.content.split(" ")[1])
    game = ''.join(ctx.message.content.split(" ")[1])
    userid = findUserIndex(ctx.message.author.id)
    game_index = findGameIndex(fullWord)
    binary[game_index][userid] = 1
    await bot.say(game + " has been added to your game list.")


'''
# Adds user ID in new column game entry in CSV file when they play the game with discord running in the background
@bot.event
async def on_member_update():
    This checks updates for one user (ie games)
'''


# Adds Game entry in CSV file
@bot.command(pass_context=True)
async def create(ctx):
    intoData = ctx.message.content.split(" ")[1].lower()
    fullWord = ''.join(intoData)
    with open('gameList.csv', "a") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([intoData])
    await bot.say(fullWord + " has been added to the game list.")


# Lists all games added in the csv file
@bot.command(pass_context=True)
async def gamelist(ctx):
    #global gameList
    gameList = import_gameList()
    if gameList.size >= 2:
        await bot.say("We got:")
        await bot.say(', '.join(gameList))
    else:
        if gameList:
            await bot.say("We got:")
            await bot.say(gameList)
        else:
            await bot.say("Game List is empty")


@bot.command(pass_context=True)
async def onlineCheck(ctx):
    for server in bot.servers:
        for member in server.members:
            if member.status == discord.Status.online:
                await bot.say(member)


# client.run('MzkyOTE3OTU1NDQ2MzA4ODY1.DRuPOw.Z3aGgdvDuKP8wAkHMt2vSPSEwZ4')
bot.run('NDAxNTM4OTU0NDg4MTg0ODMy.DTrriQ.y2QzATd4j8PVsHkuhlwv7Azmnyc')

# SURYA AUTH: NDAxNjM3MTIzNzgzOTE3NTY4.DTtFPQ.t9TTZ5qM2KNoDXr87LpvxVxqMgc
# DAN AUTH: NDAxNTM4OTU0NDg4MTg0ODMy.DTrriQ.y2QzATd4j8PVsHkuhlwv7Azmnyc
