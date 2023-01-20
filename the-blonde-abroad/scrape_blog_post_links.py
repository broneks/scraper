import requests
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

base_url = 'https://www.theblondeabroad.com/travel-blog'
page_start = 1
page_end = 500

def get_page_url(page):
    return '%s/page/%s' % (base_url, page)

async def fetch_html(session, url):
    async with session.get(url) as response:
        print(f'fetched: {url}')
        return await response.text()

def scrape_page_blog_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    for blog_anchor in soup.select('.entry-content .more-link'):
        href = blog_anchor['href']
        if href:
            links.append(href)

    return links

async def get_blog_links_for_page(session, url):
    html = await fetch_html(session, url)
    links = scrape_page_blog_links(html)

    return links

async def get_blog_links_for_pages(start, end):
    headers = {'User-Agent': 'Mozilla/5.0'}

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []

        print(f'fetching {end} pages...')

        for page in range(start, end + 1):
            page_url = get_page_url(page)
            tasks.append(asyncio.ensure_future(get_blog_links_for_page(session, page_url)))
            await asyncio.sleep(1) # just to be nice

        links = await asyncio.gather(*tasks)

        return links

def write_to_file(output):
    with open(f'./output/the-blonde-abroad-blog-links.json', 'w') as file:
        json.dump(output, file, indent=2, ensure_ascii=False)

async def main():
    output = {
        'blog_links': [],
    }
    output['blog_links'] = await get_blog_links_for_pages(page_start, page_end)

    write_to_file(output)

asyncio.run(main())
