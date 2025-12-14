# Lua Obfuscator Discord Bot

A Discord bot that obfuscates Lua scripts using multi-stage obfuscation techniques.

## Features

- Multi-stage Lua obfuscation (compression, encryption, VM encoding)
- Anti-tamper and anti-debug protections
- Variable renaming and control flow obfuscation
- Accepts Lua code via messages or file uploads
- Returns obfuscated code as text or file attachment

## Deployment to Render

### Prerequisites

1. A Discord bot token from [Discord Developer Portal](https://discord.com/developers/applications)
2. A GitHub account
3. A Render account (free tier available)

### Steps

1. **Create a Discord Bot**
   - Go to https://discord.com/developers/applications
   - Click "New Application" and give it a name
   - Go to the "Bot" section and click "Add Bot"
   - Enable "Message Content Intent" under Privileged Gateway Intents
   - Copy the bot token (you'll need this for Render)

2. **Deploy to Render**
   - Push this repository to your GitHub account
   - Go to https://render.com and sign in
   - Click "New +" and select "Background Worker"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: lua-obfuscator-bot (or any name)
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python bot.py`
   - Add environment variable:
     - **Key**: `DISCORD_BOT_TOKEN`
     - **Value**: Your Discord bot token
   - Click "Create Background Worker"

3. **Invite Bot to Server**
   - Go back to Discord Developer Portal
   - Go to OAuth2 > URL Generator
   - Select scopes: `bot`
   - Select bot permissions: `Send Messages`, `Read Messages/View Channels`, `Attach Files`
   - Copy the generated URL and open it in your browser
   - Select your server and authorize the bot

## Usage

Send Lua code to the bot in any of these formats:

1. **Plain text**: Just paste your Lua code
2. **Code block**: 
   ```lua
   local x = 10
   print(x)
   ```
3. **File upload**: Upload a `.lua` or `.txt` file

The bot will respond with the obfuscated Lua code.

## Environment Variables

- `DISCORD_BOT_TOKEN`: Your Discord bot token (required)

## License

MIT
