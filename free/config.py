import os
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('TOKEN_DISCORD')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
REPORT_HOUR = int(os.getenv('REPORT_HOUR', 20))
REPORT_MINUTE = int(os.getenv('REPORT_MINUTE', 0))
TIMEZONE = os.getenv('TIMEZONE', 'Europe/Paris')
MENTION_ROLE = os.getenv('MENTION_ROLE', '@everyone')
DB_PATH = 'deals.db'
GENSIN_API_URL = 'https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey'