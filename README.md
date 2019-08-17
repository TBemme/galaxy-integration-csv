# galaxy-integration-csv
A Sony PlayStation Vita platform integration for Galaxy 2.0. Though mainly this is an experimental test for using a .csv file to provide the games list, and could be adapted for any platform.

## Features:
- Add PlayStation Vita games (by default configuration) to your Library, using a .csv file to provide individual game_ids, titles, and optionally paths.
- Easily customisable. Can have other fields, if Galaxy integration API might allow providing more information in the future.

## How to Install:

Download the repository, and put in into an appropriate folder in your GOG Galaxy custom plugins directory. Customise the `gameslist.csv`, `config.py` and `plugin.py` as desired. However, `manifest.json` will also need to be changed if you wish to change the platform.
