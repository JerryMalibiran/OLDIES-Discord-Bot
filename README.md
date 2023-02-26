# OLDIES-Discord-Bot
## Discord bot utilizing OpenAI's API. Experimental.
Join our discord server at: https://discord.gg/WKutnmp6Dn

# Requirements
* Python
* discord.py[voice]
* openai
* python-dotenv
* yt-dlp

# Usage
1. Clone repository
2. pip install -r requirements.txt
3. Create a '.env' file and write your openai api key as well as your discord token in the format:
```
OPENAI-API-KEY = <YOUR-OPENAI-API-KEY>
DISCORD-TOKEN = <YOUR-DISCORD-TOKEN>
```
4. Download the FFMpeg executable files at https://ffmpeg.org/download.html then copy 'ffmpeg.exe' to project root directory.
4. run 'py run.py' command on your terminal

# Repl.it
For repl.it deployment, use their built-in 'Secrets' feature for environment variables and use this syntax for retrieving them:
```python
# run.py
import os

OPENAI_API_KEY = os.environ['OPENAI-API-KEY']
DISCORD_TOKEN = os.environ['DISCORD-TOKEN']
```

For some reason, Opus won't load on my replit. As a band-aid fix, download 'libopus.so' (libopus.so.0.x.x or similiar) online if you can find one and place it on to the root project directory and add this line of code on top of 'bot.py':

```python
import discord

discord.opus.load_opus('./libopus.so.0.x.x')
```

You won't need to do this once I'm able to find a fix for it. 
