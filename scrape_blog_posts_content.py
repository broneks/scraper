import requests
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch_html(session, url):
    async with session.get(url) as response:
        print(f'fetched: {url}')
        return await response.text()

def scrape_blog_post_content(html, url):
    soup = BeautifulSoup(html, 'html.parser')

    content = {
        'url': url,
        'title': '',
        'paragraphs': [],
    }

    content['title'] = soup.find('h1').string

    for para in soup.select('.entry-content .tba-listicle-content'):
        text = ''.join(para.strings)

        if text and text != '\n\n':
            content['paragraphs'].append(text)

    return content

async def get_blog_post_content(url):
    headers = {'User-Agent': 'Mozilla/5.0'}

    async with aiohttp.ClientSession(headers=headers) as session:
        html = await fetch_html(session, url)
        content = scrape_blog_post_content(html, url)

        return content

    # Write the HTML of the entire page to a file
def write_to_file(output):
    with open(f'./output/blog-posts-content.json', 'w') as file:
        json.dump(output, file, indent=2, ensure_ascii=False)

async def main():
    f = open('./output/the-blonde-abroad-blog-links.json')
    blog_links_json = json.load(f)

    output = {
        'blog_posts': [],
    }

    for page in blog_links_json['blog_links']:
        for url in page:
            content = await get_blog_post_content(url)
            output['blog_posts'].append(content)

    write_to_file(output)

def run():
    asyncio.run(main())
