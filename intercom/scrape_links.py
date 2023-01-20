import requests
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

base_url = 'https://www.intercom.com/help/en/collections/2094730-the-inbox-legacy'

async def fetch_html(session):
    async with session.get(base_url) as response:
        print(f'fetched: {base_url}')
        return await response.text()

def scrape_page_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    for anchor in soup.select('.paper__article-preview'):
        href = anchor['href']
        if href:
            links.append(f'https://www.intercom.com{href}')

    return links

async def get_links(session):
    html = await fetch_html(session)
    links = scrape_page_links(html)

    return links

async def get_all_links():
    headers = {'User-Agent': 'Mozilla/5.0'}

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []

        print(f'fetching links...')

        tasks.append(asyncio.ensure_future(get_links(session)))
        await asyncio.sleep(1) # just to be nice

        links = await asyncio.gather(*tasks)

        return links

def write_to_file(output):
    with open(f'./output/intercom-links.json', 'w') as file:
        json.dump(output, file, indent=2, ensure_ascii=False)

async def main():
    output = {
        'links': [],
    }
    output['links'] = await get_all_links()

    write_to_file(output)

asyncio.run(main())
