import requests
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

base_url = 'https://www.theblondeabroad.com/travel-blog'

def get_page_url(page):
    return '%s/page/%s' % (base_url, page)

async def fetch_blog_page(session, url):
    async with session.get(url) as response:
        return await response.text()

def parse_blog_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    for blog_anchor in soup.select('.entry-content .more-link'):
        href = blog_anchor['href']
        if href:
            links.append(href)

    return links

async def get_blog_links(session, url):
    html = await fetch_blog_page(session, url)
    links = parse_blog_links(html)

    return links

async def scan_blog_pages(start, end):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for page in range(start, end + 1):
            page_url = get_page_url(page)
            tasks.append(asyncio.ensure_future(get_blog_links(session, page_url)))

        blog_links = await asyncio.gather(*tasks)

        print(blog_links)

asyncio.run(scan_blog_pages(1, 3))
