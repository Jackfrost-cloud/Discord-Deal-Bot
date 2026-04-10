import aiohttp
from bs4 import BeautifulSoup
import feedparser
import random
import asyncio
from datetime import datetime

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

async def fetch_html(url):
    await asyncio.sleep(random.uniform(1, 3))
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": USER_AGENT}) as response:
            return await response.text()

async def scrape_epic_games():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=fr&country=FR&allowCountries=FR"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    items = []
    for game in data['data']['Catalog']['searchStore']['elements']:
        if game.get('promotions', {}).get('promotionalOffers'):
            items.append({
                'title': game['title'],
                'type': 'game',
                'platform': 'Epic Games',
                'url': f"https://store.epicgames.com/product/{game['id']}",
                'source': 'Epic Games'
            })
    return items

async def scrape_steam():
    html = await fetch_html("https://store.steampowered.com/search/?maxprice=free&specials=1")
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    for game in soup.select('.search_result_row')[:5]:
        title = game.select_one('.title').text.strip()
        url = "https://store.steampowered.com" + game.select_one('a')['href']
        items.append({
            'title': title,
            'type': 'game',
            'platform': 'Steam',
            'url': url,
            'source': 'Steam'
        })
    return items

async def scrape_gog():
    html = await fetch_html("https://www.gog.com/fr/games?sort=popularity&price=free")
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    for game in soup.select('.product-tile')[:5]:
        title = game.select_one('.product-tile__title').text.strip()
        url = "https://www.gog.com" + game.select_one('a')['href']
        items.append({
            'title': title,
            'type': 'game',
            'platform': 'GOG',
            'url': url,
            'source': 'GOG'
        })
    return items

async def scrape_rss_feed(feed_url, source_name, platform):
    feed = feedparser.parse(feed_url)
    items = []
    for entry in feed.entries[:3]:
        items.append({
            'title': entry.title,
            'type': 'game',
            'platform': platform,
            'url': entry.link,
            'source': source_name
        })
    return items

async def scrape_free_games():
    tasks = [
        scrape_epic_games(),
        scrape_steam(),
        scrape_gog(),
        scrape_rss_feed("https://www.reddit.com/r/FreeGamesOnSteam.rss", "Reddit", "Steam"),
        scrape_rss_feed("https://www.reddit.com/r/freegames.rss", "Reddit", "Multi")
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    items = []
    for result in results:
        if not isinstance(result, Exception):
            items.extend(result)
    return items