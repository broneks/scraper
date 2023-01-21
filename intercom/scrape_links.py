import requests
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

urls = [
    'https://www.intercom.com/help/en/collections/382-what-is-intercom',
    'https://www.intercom.com/help/en/collections/2094822-installing-intercom',
    'https://www.intercom.com/help/en/collections/1865264-getting-started-with-intercom',
    'https://www.intercom.com/help/en/collections/2094808-the-intercom-platform',
    'https://www.intercom.com/help/en/collections/2094767-the-messenger',
    'https://www.intercom.com/help/en/collections/3497068-next-gen-inbox',
    'https://www.intercom.com/help/en/collections/3659257-tickets',
    'https://www.intercom.com/help/en/collections/2094730-the-inbox-legacy',
    'https://www.intercom.com/help/en/collections/2091449-outbound-messages-campaigns',
    'https://www.intercom.com/help/en/collections/2091464-outbound-chats-posts-banners',
    'https://www.intercom.com/help/en/collections/2091415-outbound-emails',
    'https://www.intercom.com/help/en/collections/3537227-news',
    'https://www.intercom.com/help/en/collections/2094721-custom-bots',
    'https://www.intercom.com/help/en/collections/2094707-product-tours',
    'https://www.intercom.com/help/en/collections/3599910-tooltips',
    'https://www.intercom.com/help/en/collections/3331979-surveys',
    'https://www.intercom.com/help/en/collections/3512215-2-way-sms',
    'https://www.intercom.com/help/en/collections/2549823-series',
    'https://www.intercom.com/help/en/collections/2094785-articles',
    'https://www.intercom.com/help/en/collections/2094854-operator-task-bots',
    'https://www.intercom.com/help/en/collections/2094839-resolution-bot',
    'https://www.intercom.com/help/en/collections/3510275-custom-actions-and-objects',
    'https://www.intercom.com/help/en/collections/3385793-switch',
    'https://www.intercom.com/help/en/collections/2094752-reporting',
    'https://www.intercom.com/help/en/collections/2094798-intercom-in-your-mobile-app',
    'https://www.intercom.com/help/en/collections/2094744-apps-integrations',
    'https://www.intercom.com/help/en/collections/2847869-f-a-qs-from-the-community',
    'https://www.intercom.com/help/en/collections/2493871-intercom-academy',
    'https://www.intercom.com/help/en/collections/384-privacy-terms',
    'https://www.intercom.com/help/en/collections/515-switching-to-intercom',
    'https://www.intercom.com/help/en/collections/3679054-checklists',
]

async def fetch_html(session, url):
    async with session.get(url) as response:
        print(f'fetched: {url}')
        return await response.text()

def scrape_page_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    for anchor in soup.select('.paper__article-preview'):
        href = anchor['href']
        if href:
            links.append(f'https://www.intercom.com{href}')

    return links

async def get_links(session, url):
    html = await fetch_html(session, url)
    links = scrape_page_links(html)

    return links

async def get_all_links():
    headers = {'User-Agent': 'Mozilla/5.0'}

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []

        print(f'fetching links...')

        for url in urls:
            tasks.append(asyncio.ensure_future(get_links(session, url)))
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
