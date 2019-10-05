# galaxy-integration-csv
A Sony PlayStation Vita platform integration for Galaxy 2.0. Though mainly this is an experimental test for using a .csv file to provide the games list information, and could be adapted for any platform. This branch is for trophy support.

## Features:
- Add PlayStation Vita games (by default configuration) to your Library, using a .csv file to provide individual game_ids, titles, and optionally paths.
- Easily customisable. Can have other fields, if Galaxy integration API might allow providing more information in the future.
- Adds your trophies from offline/local storage (Note: this currently does not work, likely a Galaxy-side issue)

## How to Install:

Download the repository, and put it into an appropriate folder in your GOG Galaxy community integrations directory. Customise the `gameslist.csv`, `config.py` and `plugin.py` as desired. However, `manifest.json` will also need to be changed if you wish to change the platform.

For your trophy list, if you have access to your Vita's filesystem, export the tbl_trophy_flag table of the trophy_local.db to a .csv file. It will have all the required columns. The one included in this repo has been stripped down for clarity and to remove any potentially identifying information.

### A note
Each platform's game_ids get added to GOG's gamesdb once matched, and cannot be removed by the user or plugin. Please be aware of this if you plan to use this tool.

## Trophy Support

See [Issue #1](https://github.com/TBemme/galaxy-integration-csv/issues/1) for current status/To-Do list
