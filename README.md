# rscBot
A Discord bot written in making finding groups to play games within a Discord server easier, using Discord.py.

## Overview
Users can add games to a file and then add their Discord User ID under the game's entry, allowing for easy recruiting for games by automating DMing users to play. A timed response component is included to ensure that users
are present.

### Commands
  1. $create "name_of_game" = makes a game entry within the gameList.csv file (file itself created if not already present)
  2. $add "name_of_game" = adds the user to the list of players that play that game
  4. $recruit "name_of_game" "num_people" = DM's however many users are inputted
  5. $remove "name_of_game" = removes a user from a game
  6. $deletegame "name_of_game" = deletes a particular game
