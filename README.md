# OLDIES-Discord-Bot
## Discord bot utilizing OpenAI's API. Experimental.
Join our discord server at: https://discord.gg/WKutnmp6Dn

# Requirements
* Python
* discord
* openai
* python-dotenv

# Usage
1. Clone repository
2. pip install -r requirements.txt
3. Create a '.env' file and write your openai api key as well as your discord token in the format:
```
OPENAI-API-KEY = <YOUR-OPENAI-API-KEY>
DISCORD-TOKEN = <YOUR-DISCORD-TOKEN>
```
4. run 'py run.py' command on your terminal

# Repl.it
For repl.it deployment, use their built-in 'Secrets' feature for environment variables and use this syntax for retrieving them:
```python
# run.py
import os

OPENAI_API_KEY = os.environ['OPENAI-API-KEY']
DISCORD_TOKEN = os.environ['DISCORD-TOKEN']
```
