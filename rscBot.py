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

        return gameList
    else:
        gameList = np.empty((1, 1), dtype='str')
        return gameList


# Import the csv of User IDs into a 1 x U matrix (U = # of users)
def import_userList(filename='userlist.csv'):
    # check for empty file
    if os.stat(filename).st_size != 0:
        f = open(filename, "r")
        userList = np.genfromtxt(filename, dtype='str', delimiter=' ')
        f.close()
        return userList


    else:
        userList = np.empty((1, 1), dtype='str')
        return userList


def loadUsers(filename='userlist.csv'):
    # load all users
    for server in bot.servers:
        for member in server.members:
            # print(type(userList))
            if userList.size >= 2:
                if member.id in userList:
                    print(member.id + " Was found")  # they are already in the file
                else:  # add them
                    with open(filename, "a") as csvfile:
                        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        filewriter.writerow([member.id,][member.display_name])
            else:
                if userList:  # check if user list is empty
                    print(member.id)
                    # if not empty then check ids with current file
                    if member.id == userList[0]:
                        print(member.id + " Was found")  # they are already in the file
                    else:  # add them
                        with open(filename, "a") as csvfile:
                            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                            filewriter.writerow([member.id][ member.display_name])
                else:  # file is empty, add all users to file
                    print(member.id)
                    with open(filename, "a") as csvfile:
                        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        filewriter.writerow([member.id][ member.display_name])


# gets the size of a list
def List_Size(alist):
    if alist.size >= 2:
        return alist.size
    else:
        if alist:  # check if user list is empty
            return 1
        else:
            return 0


# Import the csv of User IDs into a G x U  binary matrix where
# 1 = they have the game
# 0 = they do not have the game
def import_binary(filename='Bmatrix.csv'):
    print("Number of games is")
    print(List_Size(gameList))
    print("number of users is")
    print(List_Size(userList))
    if List_Size(userList) + List_Size(gameList) > 0:
        binary = np.zeros((List_Size(gameList), List_Size(userList)), dtype=int)

    # print(np.count_nonzero(binary))
    if os.stat(filename).st_size != 0:
        f = open(filename, "r")
        binfile = np.genfromtxt(filename, dtype='int', delimiter=' ')
        if binfile.all():
            binary = binfile
            print("binfile all")
        f.close()
        return binary

    return binary


# returns game index from a string
def findGameIndex(game_name):
    global gameList
    gameList = import_gameList()
    if List_Size(gameList):
        for i in range(0, List_Size(gameList) + 1):
            if gameList[i] == game_name:
                return i
        return -1
    return 0


# returns game name from a index
def findGameName(index):
    global gameList
    gameList = import_gameList()
    if List_Size(gameList):
        if List_Size(gameList) <= index:
            return gamelist[index]
    return None


def findUserIndex(user_id):
    global userList
    userList = import_userList()
    if List_Size(userList):
        for i in range(List_Size(userList)):
            if userList[i] == user_id:
                return i
    return None


def findUserId(index):
    global userList
    userList = import_userList()
    if List_Size(userList):
        if List_Size(userList) <= index:
            return userList[index]
    return 0


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
    loadUsers()  # load any new users
    print(userList)
    print('Loading Binary Relations...')
    global binary
    binary = import_binary()
    print('Ready when you are, with username: ' + bot.user.name + " and the ID: " + bot.user.id)


@bot.event
async def on_member_join(member):
    if userList.size >= 2:
        if member.id in userList:
            print(member.id + " Was found")  # they are already in the file
        else:  # add them
            with open('userlist.csv', "a") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([member.id][ member.display_name])
    else:
        if userList:  # check if user list is empty
            print(member.id)
            # if not empty then check ids with current file
            if member.id == userList[0]:
                print(member.id + " Was found")  # they are already in the file
            else:  # add them
                with open('userlist.csv', "a") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([member.id][ member.display_name])
        else:  # file is empty, add all users to file
            print(member.id)
            with open('userlist.csv', "a") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([member.id][ member.display_name])


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
    with open(ctx.message.content.split(" ")[1].lower() + ".txt", "r", newline="\n") as file_handler:

        while True:
            line = file_handler.readline()
            line = line.rstrip()
            await bot.say(line)
            embed = discord.Embed(title="Let's Game!",
                                  description=ctx.message.author.display_name + " requests your holy presence!",
                                  color=0x00ffff)
            if type(ctx.message.author.voice.voice_channel) == type(None):
                print(ctx.message.author.voice.voice_channel)
                embed.add_field(name="In Server: ",
                                value=ctx.message.author.server.name)
            else:
                embed.add_field(name="In Server: " + ctx.message.author.server.name,
                                value="Voice Channel: " + ctx.message.author.voice.voice_channel.name)
            embed.add_field(name="Please reply with:", value="yes if you would like to play, and no if you cannot.",
                            inline=True)
            embed.add_field(name="Time Requirement! :timer:", value="Please respond to this message within 60 seconds.")
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            await bot.send_message(discord.User(id=line), embed=embed)
            userDecision = await bot.wait_for_message(timeout=60, author=bot.get_user_info(line))
            if type(userDecision) == type(None):
                await bot.send_message(discord.User(id=line), "You didn't make it in time!")
                await bot.say(line + " didn't respond in time.")
            elif str(userDecision.content) == "no":
                await bot.say(line + " is not going to join.")
            else:
                await bot.say(line + " is going to join!")
            if not line:
                break


@bot.command(pass_context=True)
async def recruitUser(ctx, user: discord.Member):
    embed = discord.Embed(title="Let's Game!",
                          description=ctx.message.author.display_name + " requests your holy presence!", color=0x00ffff)
    if type(ctx.message.author.voice.voice_channel) == type(None):
        print(ctx.message.author.voice.voice_channel)
        embed.add_field(name="In Server: ",
                        value=ctx.message.author.server.name)
    else:
        embed.add_field(name="In Server: " + ctx.message.author.server.name,
                        value="Voice Channel: " + ctx.message.author.voice.voice_channel.name)
    embed.add_field(name="Please reply with:", value="yes if you would like to play, and no if you cannot.",
                    inline=True)
    embed.add_field(name="Time Requirement! :timer:", value="Please respond to this message within 60 seconds.")
    embed.set_thumbnail(url=user.avatar_url)
    await bot.send_message(discord.User(id=user.id), embed=embed)
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
    binary = import_binary()  # load the binary
    print(binary.shape)
    intoData = ctx.message.content.split(" ")[1].lower()

    useridindex = findUserIndex(ctx.message.author.id)
    print(useridindex)

    game_index = findGameIndex(intoData)
    if game_index == -1:
        await bot.say("Game has not been created yet")
        return
    print(game_index)
    binary[game_index][useridindex] = 1
    np.savetxt("Bmatrix.csv", binary, delimiter=" ")
    print(binary)
    await bot.say("User " + ctx.message.author.display_name + " has added game " + intoData + " to their list.")


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
    # global gameList
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


@bot.command(pass_context=True)
async def userGames(ctx, user: discord.Member):
    index = findUserIndex(user.id)
    await bot.say(binary[:, index])
    print(index)
    print(binary[:, index])


@bot.command(pass_context=True)
async def addGame(ctx):
    with open(ctx.message.content.split(" ")[1].lower() + ".txt", "a", newline="\n") as file_handler:
        # shortWord = ctx.message.content.split(" ")[1].lower()
        shortWord = []
        shortWord.append(ctx.message.author.id)
        for item in shortWord:
            file_handler.write("%s\n" % item)

    file_handler.close()
    await bot.say(shortWord)


bot.run(TOKEN_GOES_HERE)

