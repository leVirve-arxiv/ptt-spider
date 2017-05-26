import urllib.parse
import aiohttp

from ptt import parser
from ptt import settings


class Board():

    base_url = 'https://www.ptt.cc/bbs'
    endpoint = 'index.html'

    def __init__(self, name):
        self.name = name

    def index(self):
        return f'{self.base_url}/{self.name}/{self.endpoint}'

    def page(self, num):
        endpoint = f'index{num}.html'
        return f'{self.base_url}/{self.name}/{endpoint}'

    def post(self, link):
        return urllib.parse.urljoin(self.base_url, link)


class PTTSpider():

    headers = {
        'user-agent': settings.USER_AGENT,
    }

    def __init__(self, board, loop):
        self.session = aiohttp.ClientSession(loop=loop)
        self.loop = loop
        self.board = Board(board)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.loop.run_until_complete(self.close())

    async def get_post(self, link):
        return await self.get(self.board.post(link), 'post_content')

    async def get_meta(self, page):
        return await self.get(self.board.page(page), 'post_metas')

    async def get_total_page_num(self):
        return await self.get(self.board.index(), 'previous_page_number') + 1

    async def get(self, url, parser_name):
        async with self.session.get(url, headers=self.headers) as resp:
            data = await resp.text()
            data_parser = getattr(parser, parser_name)
            return data_parser(data)

    async def close(self):
        await self.session.close()
