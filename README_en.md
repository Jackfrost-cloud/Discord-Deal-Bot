# Discord Deal Bot

[svg](https://github.com/Jackfrost-cloud/Discord-Deal-Bot#discord-deal-bot)

Discord bot that automatically collects promo codes, free games, and redeemable codes.

## Installation

[svg](https://github.com/Jackfrost-cloud/Discord-Deal-Bot#installation)

1. **Clone the project**

   ```
   git clone https://github.com/Jackfrost-cloud/Discord-Deal-Bot.git
   cd discord_deal_bot
   ```
2. **Create a `.env` file**

   ```
   DISCORD_TOKEN=your_token_here
   CHANNEL_ID=123456789012345678
   REPORT_HOUR=20
   REPORT_MINUTE=0
   TIMEZONE=Europe/Paris
   MENTION_ROLE=@everyone
   ```
3. **Install the dependencies**

   ```
   pip install -r requirements.txt
   ```
4. **Start the bot**

   ```
   python bot.py
   ```

## Commands

[svg](https://github.com/Jackfrost-cloud/Discord-Deal-Bot#commands)

* `/status` - View the bot status
* `/rapport_now` - Force the report to be sent
* `/clear` - Clear the database

## How It Works

[svg](https://github.com/Jackfrost-cloud/Discord-Deal-Bot#how-it-works)

* Collects deals every 2 hours from 8 AM to 8 PM
* Daily report at 8 PM (Paris time)
* Automatically filters out duplicates
* Stores data in SQLite
