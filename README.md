# rscBot
A Discord bot written in making finding groups to play games within a Discord server easier, using Discord.py.

## Overview
Users can add games to a file and then add their Discord User ID under the game's entry, allowing for easy recruiting for games by automating DMing users to play. A timed response component is included to ensure that users
are present.

### Commands
  1. !create "name_of_game" = makes a game entry within the gameList.csv file (file itself created if not already present)
  2. !add "name_of_game" = adds the user to the list of players that play that game (TBD)
  4. !recruit "name_of_game" = DM's **online** users who a part of a game, asking if they'd like to play, with a timed response factor enabled to guarantee presence. (TBD)
  5. !remove "name_of_game" = removes a user from a game (TBD)
  6. !delete "name_of_game" = deletes a particular game (TBD)

#### Things to Remember
1. When adding rscBot to your server, make sure your permissions in the invite link is set to 392192 (allowing for message
manipulation by the bot.)