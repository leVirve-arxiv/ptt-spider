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
        print(self.board.post(link))
        data = await self.get(self.board.post(link))
        return parser.post_content(data)

    async def get_meta(self, page):
        data = await self.get(self.board.page(page))
        return parser.post_metas(data)

    async def get_total_page_num(self):
        data = await self.get(self.board.index())
        return parser.previous_page_number(data) + 1

    async def get(self, url):
        async with self.session.get(url, headers=self.headers) as resp:
            return await resp.text()

    async def close(self):
        await self.session.close()
