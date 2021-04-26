# novaro-market-discord-bot
A Discord bot to search and warn about lower prices

This project was made using discord.py and pymongo

## Initial configuration

### `python3 -m venv env`

On Linux:
### `source env/bin/activate`

On Windows:
### `env/Scripts/activate.bat`

Install modules:
### `pip install -r requirements.txt`

Create a .env file:
### `touch .env`

Setup your TOKEN and MONGO env variables for Discord BOT token and mongo database url

Start the bot:
### `python3 main.py`


## How to use

Invite the bot to a discord server.

### Commands

To setup a watcher on a market item:
### `>warn <channel_name> <item_id>`

To undo a watcher:
### `>unwarn <channel_name> <item_id>`
