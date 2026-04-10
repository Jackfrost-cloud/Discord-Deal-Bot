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

async def scrape_dealabs():
    html = await fetch_html("https://www.dealabs.com/hot-deals")
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    for deal in soup.select('.thread--deal')[:5]:
        title = deal.select_one('.thread-title').text.strip()
        url = "https://www.dealabs.com" + deal.select_one('a')['href']
        items.append({
            'title': title,
            'type': 'promo',
            'url': url,
            'source': 'Dealabs'
        })
    return items

async def scrape_ma_reduc():
    html = await fetch_html("https://www.ma-reduc.com/")
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    for promo in soup.select('.promo-box')[:5]:
        title = promo.select_one('.promo-title').text.strip()
        code = promo.select_one('.promo-code').text.strip() if promo.select_one('.promo-code') else None
        url = promo.select_one('a')['href']
        items.append({
            'title': title,
            'type': 'promo',
            'code': code,
            'url': url,
            'source': 'Ma-Reduc'
        })
    return items

async def scrape_rss_feed(feed_url, source_name):
    feed = feedparser.parse(feed_url)
    items = []
    for entry in feed.entries[:5]:
        items.append({
            'title': entry.title,
            'type': 'promo',
            'url': entry.link,
            'source': source_name
        })
    return items

async def scrape_promo_codes():
    tasks = [
        scrape_dealabs(),
        scrape_ma_reduc(),
        scrape_rss_feed("https://www.hotukdeals.com/feed", "HotUKDeals"),
        scrape_rss_feed("https://slickdeals.net/newsearch.php?mode=frontpage&sk=tos3&src=frontpage", "SlickDeals")
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    items = []
    for result in results:
        if not isinstance(result, Exception):
            items.extend(result)
    return items