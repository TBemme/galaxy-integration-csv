import asyncio
import json
import os
import subprocess
import sys
import csv
from datetime import datetime

import config
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.consts import Platform, LicenseType, LocalGameState
from galaxy.api.types import Achievement, Authentication, Game, LocalGame, LicenseInfo

class PlayStationVitaPlugin(Plugin):
	def __init__(self, reader, writer, token):
		super().__init__(Platform.PlayStationVita, config.version, reader, writer, token)
		self.games = []
		self.local_games_cache = self.local_games_list()


	async def authenticate(self, stored_credentials=None):
		usercred = {}
		username = config.username
		usercred["username"] = config.username
		self.store_credentials(usercred)

		return Authentication("PSVuserId", usercred["username"])
		
	async def launch_game(self, game_id):
		for game in self.games:
			if str(game[1]) == game_id:
				subprocess.Popen([game[0]])
				break
		return

	# async def install_game(self, game_id):
		# pass

	# async def uninstall_game(self, game_id):
		# pass
		
	def shutdown(self):
		pass

	def local_games_list(self):
		local_games = []
		
		for game in self.games:
			if os.path.exists(game[0]):
				local_games.append(
					LocalGame(
						str(game[1]),
						LocalGameState.Installed
					)
				)
		return local_games


	def tick(self):

		async def update_local_games():
			loop = asyncio.get_running_loop()
			new_local_games_list = await loop.run_in_executor(None, self.local_games_list)
			notify_list = get_state_changes(self.local_games_cache, new_local_games_list)
			self.local_games_cache = new_local_games_list
			for local_game_notify in notify_list:
				self.update_local_game_status(local_game_notify)

		asyncio.create_task(update_local_games())


	async def get_owned_games(self):
		self.games = get_games()
		owned_games = []
		
		for game in self.games:
			owned_games.append(
				Game(
					str(game[1]),
					game[2],
					None,
					LicenseInfo(LicenseType.SinglePurchase, None)
				)
			)
			
		return owned_games

	async def get_local_games(self):
		return self.local_games_cache
		
	async def get_unlocked_achievements(self, game_id: str, context: None):
		
		unlocked_achievements = []

		with open(trophy_list, encoding='utf-8') as f:
			reader = csv.DictReader(f)

			for game in gameresults:
				if game[1] == game_id:
					gamedata = game
					break
			if gamedata[3] != None:
				for row in reader:
					if row['npcommid'] == gamedata[3]:
						# print('1', row)
						if row['unlocked'] == '1':
							# print('2', row)
							unlock_time = datetime.strptime(row['time_unlocked_uc'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()
							achievement_id = row['npcommid'] + '_' + row['trophyid']
							achievement_name = row['title']
							# print(unlock_time, achievement_id, achievement_name)
							unlocked_achievements.append(
								Achievement(
									unlock_time,
									achievement_id,
									achievement_name
								)
							)
					else:
						pass
		
		return unlocked_achievements


def get_games():
	global gameresults
	results = []

	try:
		with open(csv_list) as csvlist:
			reader = csv.DictReader(csvlist)
			for row in reader:
				results.append(
						[row['path'], row['serial'], row['title'], row['NPcommid']]
					)
	except UnicodeDecodeError:
		with open(csv_list, encoding='utf-8') as csvlist:
			reader = csv.DictReader(csvlist)
			for row in reader:
				results.append(
						[row['path'], row['serial'], row['title'], row['NPcommid']]
					)	

	gameresults = results
	return results

def get_state_changes(old_list, new_list):
	old_dict = {x.game_id: x.local_game_state for x in old_list}
	new_dict = {x.game_id: x.local_game_state for x in new_list}
	result = []
	# removed games
	result.extend(LocalGame(id, LocalGameState.None_) for id in old_dict.keys() - new_dict.keys())
	# added games
	result.extend(local_game for local_game in new_list if local_game.game_id in new_dict.keys() - old_dict.keys())
	# state changed
	result.extend(LocalGame(id, new_dict[id]) for id in new_dict.keys() & old_dict.keys() if new_dict[id] != old_dict[id])
	return result

default_csv_list = os.environ['localappdata'] + '\\GOG.com\\Galaxy\\plugins\\installed\\psv_496fb3a2-56f9-4b33-8787-2580acb52e04\\gamelist.csv'	
if os.path.exists(config.csv_list) and os.path.isfile(config.csv_list):
	csv_list = config.csv_list
else:
	csv_list = default_csv_list
	
default_trophy_list = os.environ['localappdata'] + '\\GOG.com\\Galaxy\\plugins\\installed\\psv_496fb3a2-56f9-4b33-8787-2580acb52e04\\trophylist.csv'	
if os.path.exists(config.trophy_list) and os.path.isfile(config.trophy_list):
	trophy_list = config.trophy_list
else:
	trophy_list = default_trophy_list

def main():
	create_and_run_plugin(PlayStationVitaPlugin, sys.argv)


# run plugin event loop
if __name__ == "__main__":
	main()