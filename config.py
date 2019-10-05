# .csv file containing all game information, one game per row. By default, it is using the following four columns:
# "serial" - provides game_id. Must be unique among the games you wish to add to your Library.
# "title" - title of the game, used to find a match in the GOG gamesdb. Make sure chosen file encoding supports all characters used.
# "path" - optional, expects full path to .bat or .exe
# "NPcommid" - optional, for trophy support. Currently only supports one for each game.
csv_list = r""

# .csv file containing trophy information. Export the tbl_trophy_flag table of your trophy_local.db
# Requires the following columns: "npcommid", "trophyid", "unlocked", "time_unlocked_uc", "title"
# Note that a lot of achievement information is provided by Galaxy. If something is missing, it may not be fixable by plugins/users.
trophy_list = r""

# Optional, pick a username. Displayed on the Settings Integration screen.
username = "Username"

# Version number
version = "0.0.2"