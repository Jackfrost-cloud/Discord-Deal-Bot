import aiohttp
import feedparser
import random
import asyncio
from config import GENSIN_API_URL
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

async def fetch_html(url):
    await asyncio.sleep(random.uniform(1, 3))
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": USER_AGENT}) as response:
            return await response.text()

async def scrape_genshin_api():
    async with aiohttp.ClientSession() as session:
        async with session.get(GENSIN_API_URL) as response:
            data = await response.json()
    items = []
    for code in data.get('data', []):
        items.append({
            'title': 'Genshin Impact',
            'type': 'code',
            'code': code['cdkey'],
            'reward': code['reward'],
            'url': f"https://genshin.hoyoverse.com/fr/gift?code={code['cdkey']}",
            'source': 'Hoyoverse API'
        })
    return items

async def scrape_reddit_feed(feed_url, source_name, game_name):
    feed = feedparser.parse(feed_url)
    items = []
    for entry in feed.entries[:3]:
        if 'code' in entry.title.lower() or 'redeem' in entry.title.lower():
            items.append({
                'title': game_name,
                'type': 'code',
                'code': None,
                'reward': entry.title,
                'url': entry.link,
                'source': source_name
            })
    return items

async def scrape_exchange_codes():
    tasks = [
        scrape_genshin_api(),
        scrape_reddit_feed("https://www.reddit.com/r/GenshinImpactTips.rss", "Reddit", "Genshin Impact"),
        scrape_reddit_feed("https://www.reddit.com/r/hoyolab.rss", "Reddit", "Hoyolab"),
        scrape_reddit_feed("https://www.reddit.com/r/pokemongo.rss", "Reddit", "Pokemon GO"),
        scrape_reddit_feed("https://www.reddit.com/r/leagueoflegends.rss", "Reddit LoL", "League of Legends")
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    items = []
    for result in results:
        if not isinstance(result, Exception):
            items.extend(result)
    return items