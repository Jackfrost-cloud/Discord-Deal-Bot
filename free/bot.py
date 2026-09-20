import discord
from discord import app_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import logging
import asyncio
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

from config import TIMEZONE, REPORT_HOUR, REPORT_MINUTE, CHANNEL_ID, MENTION_ROLE
TZ = ZoneInfo(TIMEZONE)
from database import init_db, clear_today, get_today_items, add_item, get_subscribers
from scrapers_promo_codes import scrape_promo_codes
from scrapers_free_games import scrape_free_games
from scrapers_exchange_codes import scrape_exchange_codes
from tasks_daily_report import send_daily_report

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class DealBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.scheduler = AsyncIOScheduler(timezone=TZ)

    async def setup_hook(self):
        await init_db()
        self.scheduler.add_job(
            self.run_collection,
            'interval',
            hours=1,
            start_date=datetime.now(TZ).replace(hour=6, minute=0, second=0, microsecond=0),
            end_date=datetime.now(TZ).replace(hour=23, minute=59, second=0, microsecond=0),
            next_run_time=datetime.now(TZ)
        )
        self.scheduler.add_job(
            send_daily_report,
            'cron',
            hour=3,
            minute=30,
            args=[self],
            kwargs={'show_subscribe': False},
            id='daily_report'
        )
        self.scheduler.start()
        await self.tree.sync()

    async def run_collection(self):
        logging.info("Démarrage de la collecte...")
        try:
            promo_task = scrape_promo_codes()
            games_task = scrape_free_games()
            codes_task = scrape_exchange_codes()

            promo_results, games_results, codes_results = await asyncio.gather(
                promo_task, games_task, codes_task, return_exceptions=True
            )

            if not isinstance(promo_results, Exception):
                for item in promo_results:
                    await add_item(item)
            if not isinstance(games_results, Exception):
                for item in games_results:
                    await add_item(item)
            if not isinstance(codes_results, Exception):
                for item in codes_results:
                    await add_item(item)

            logging.info("Collecte terminée")

            # Envoyer en MP à tous les abonnés
            subscribers = await get_subscribers()
            for user_id in subscribers:
                try:
                    user = await self.fetch_user(user_id)
                    dm = await user.create_dm()
                    await send_daily_report(self, channel_override=dm, show_subscribe=False)
                except Exception as e:
                    logging.error(f"Erreur envoi MP à {user_id}: {e}")

            # Envoyer aussi dans le channel principal
            await send_daily_report(self, show_subscribe=False)

        except Exception as e:
            logging.error(f"Erreur lors de la collecte: {e}")

client = DealBot()

@client.event
async def on_ready():
    logging.info(f'Bot connecté en tant que {client.user}')

@client.tree.command(name="status", description="Affiche le statut du bot")
async def status(interaction: discord.Interaction):
    now = datetime.now(TZ)
    next_collect = now.replace(hour=((now.hour - 8) // 2 + 1) * 2 + 8, minute=0, second=0)
    next_report = now.replace(hour=REPORT_HOUR, minute=REPORT_MINUTE, second=0)
    if next_report < now:
        next_report += timedelta(days=1)

    embed = discord.Embed(title="📊 Statut du Bot", color=0x00FF00)
    embed.add_field(name="Prochaine collecte", value=next_collect.strftime("%H:%M"), inline=True)
    embed.add_field(name="Prochain rapport", value=next_report.strftime("%H:%M"), inline=True)
    embed.add_field(name="Canal", value=f"<#{CHANNEL_ID}>", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.tree.command(name="rapport_now", description="Force l'envoi immédiat du rapport")
async def rapport_now(interaction: discord.Interaction):
    await interaction.response.send_message("Génération du rapport...", ephemeral=True)
    dm = await interaction.user.create_dm()
    await send_daily_report(client, channel_override=dm, show_subscribe=True)
    await interaction.followup.send("Rapport envoyé en MP !", ephemeral=True)

@client.tree.command(name="clear", description="Vide la base de données du jour")
async def clear(interaction: discord.Interaction):
    await clear_today()
    await interaction.response.send_message("Base de données vidée !", ephemeral=True)

client.run(TOKEN)