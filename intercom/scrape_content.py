import requests
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch_html(session, url):
    async with session.get(url) as response:
        print(f'fetched: {url}')
        return await response.text()

def process_text(text):
    if not text:
        return text

    return text.strip().replace('\u2019', "'").replace('\u00a0', ' ')

def get_sections(soup, html):
    sections = []
    stats = {}

    def add_section(name, content):
        stats[name] = stats.get(name, 0) + 1
        sections.append([name, process_text(content)])

    for node in soup.find('article').find_all(recursive=False):
        try:
            text = ''.join(node.strings)

            if node.name == 'div' and node.contents[0]:
                child = node.contents[0]
                add_section(child.name, child['src'])
            elif text and text != '\n\n':
                add_section(node.name, text)
        except:
            pass

    return sections, stats

def scrape_post_content(html, url):
    soup = BeautifulSoup(html, 'html.parser')

    content = {
        'url': url,
        'author': '',
        'stats': {},
        'title': '',
        'description': '',
        'sections': [],
    }

    try:
        content['author'] = process_text(soup.select('.avatar__info')[0].get_text())
    except:
        pass

    content['title'] = process_text(soup.find('h1').string)

    content['description'] = process_text(soup.select('.article__desc')[0].get_text())

    content['sections'], content['stats'] = get_sections(soup, html)

    return content

async def get_post_content(url):
    headers = {'User-Agent': 'Mozilla/5.0'}

    async with aiohttp.ClientSession(headers=headers) as session:
        html = await fetch_html(session, url)
        content = scrape_post_content(html, url)

        return content

    # Write the HTML of the entire page to a file
def write_to_file(output):
    with open(f'./output/intercom-content.json', 'w') as file:
        json.dump(output, file, indent=2, ensure_ascii=False)

async def main():
    try:
        f = open('./output/intercom-links.json')
    except:
        print('links file does not exist.')

    links_json = json.load(f)

    output = {
        'content': [],
    }

    for page in links_json['links']:
        for url in page:
            content = await get_post_content(url)
            output['content'].append(content)

    write_to_file(output)

asyncio.run(main())
