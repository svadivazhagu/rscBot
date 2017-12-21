# rscBot
A Discord bot written in Python that makes finding groups within a Discord server easier, using Discord.py.
This is how it works:
  it would look at how many people are currently in the voice comms, are part of the @ game role that we have set up (league, pubg, cs, etc) and then PM people who are signed up for the game we're trying to recruit a group for in this server, asking if they want to play
Commands:
  $create "name_of_game" = makes a game
  $add "name_of_game" = adds the user to the list of players that play that game
  $recruit "name_of_game" "num_people" = DM's however many users are inputted
  $remove "name_of_game" = removes a user from a game
  $deletegame "name_of_game" = deletes a particular game
