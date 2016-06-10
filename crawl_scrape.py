# Python 3.5 required for requests library

# End variable URLS with trailing slash

import asyncio
import aiohttp
import json
import datetime
import settings
import save

base_urls = settings.base_urls
limit = settings.limit

# TODO: crawl wiki


class Crawler():
    """
    Crawlers keep one node_list of all of the URL tails and GUIDs they encounter, which the scraper will go through to save pages.
    For API searches, a limit parameter is necessary for testing.

    URL tails:
    - Homepage content
    - Homepage links

    API searches:
    - Nodes
    - Users
    - Institutions

    The Crawler.crawl() function calls all of these piece crawls.

    """
    def __init__(self):
        global base_urls
        self.headers = {
            'User-Agent' : 'LinkedInBot/1.0 (compatible; Mozilla/5.0; Jakarta Commons-HttpClient/3.1 +http://www.linkedin.com)'
        }
        self.http_base = base_urls[0]
        self.api_base = base_urls[1]

        self.general_url_list = [self.http_base]
        self.node_url_list = []
        self.node_related_url_list = []
        self.user_url_list = []
        self.institution_url_list = []
        self.saver = save.Saver()

    def call_api_pages(self, site_aspect, pages=0):
        tasks = []
        for i in range(1, pages + 1):
            tasks.append(asyncio.ensure_future(self.call_and_parse_api_page(self.api_base + site_aspect + '/?page=' + str(i))))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

    async def call_and_parse_api_page(self, url):
        async with aiohttp.ClientSession() as s:
            response = await s.get(url)
            body = await response.read()
            response.close()
            json_body = json.loads(body.decode('utf-8'))
            data = json_body['data']
            for element in data:
                self.node_url_list.append(self.http_base + element['id'] + '/')

    def crawl_all_in_list(self, list):
        tasks = []
        print(self.node_url_list)
        for url in self.node_url_list:
            tasks.append(asyncio.ensure_future(self.crawl_page(url)))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    async def crawl_page(self, url):
        async with aiohttp.ClientSession() as s:
            response = await s.get(url, headers=self.headers)
            body = await response.read()
            response.close()
            print(url)
            if response.status == 200:
                self.saver.save_html(body, url)
                print("crawled: ", url)
            else:
                print ("ERROR: " + str(response.status))

a = datetime.datetime.now()

rosie = Crawler()
rosie.call_api_pages('nodes', pages=limit)
# rosie.call_
# areas = [rosie.general_url_list, rosie.node_url_list, rosie.node_related_url_list, rosie.user_url_list, rosie.institution_url_list]
# for area in areas:
#     rosie.crawl_all_in_list(area)
rosie.crawl_all_in_list(rosie.node_url_list)
b = datetime.datetime.now()
print(b - a)