
import aiohttp
import asyncio
import hashlib
import json
from bs4 import BeautifulSoup

YC_URL = "https://www.ycombinator.com/companies"

async def fetch_companies():
    async with aiohttp.ClientSession() as session:
        async with session.get(YC_URL) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")

    companies = []

    for card in soup.select("a._company"):
        name = card.text.strip()
        domain = card.get("href")
        companies.append({
            "name": name,
            "domain": domain
        })

    return companies


def compute_hash(data):
    return hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()