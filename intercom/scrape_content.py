import requests
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch_html(session, url):
    async with session.get(url) as response:
        print(f'fetched: {url}')
        return await response.text()

def scrape_post_content(html, url):
    soup = BeautifulSoup(html, 'html.parser')

    content = {
        'url': url,
        'title': '',
        'description': '',
        'sections': [],
    }

    content['title'] = soup.find('h1').string

    content['description'] = soup.select('.article__desc')[0].get_text()

    for para in soup.select('.article p'):
    for node in soup.findChildren('.article', recursive=False)
        try:
            text = ''.join(node.strings)

            if text and text != '\n\n':
                content['sections'].append(text)
        except:
            print('No string content for:', node.name)


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

# asyncio.run(main())

async def test():
    content = await get_post_content('https://www.intercom.com/help/en/articles/323-intercom-s-inbox-explained')

    print(json.dumps(content, indent=4))

asyncio.run(test())
