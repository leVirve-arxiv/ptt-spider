import asyncio
import itertools
import pprint

from ptt.core import PTTSpider


loop = asyncio.get_event_loop()


def coroutine_runner(coroutine):
    return loop.run_until_complete(coroutine)


if __name__ == '__main__':

    num_page = 5  # collect how many page

    with PTTSpider(board='movie', loop=loop) as spider:
        ''' get total page of current board '''
        total_pages = coroutine_runner(spider.get_total_page_num())

        ''' get pages of posts meta '''
        pages = range(total_pages, total_pages - num_page, -1)

        coros = asyncio.gather(
            *(spider.get_meta(page) for page in pages))

        metas = coroutine_runner(coros)
        metas = list(itertools.chain.from_iterable(metas))

        pprint.pprint(metas)
        print('total meta:', len(metas))

        ''' get posts content '''
        coros = asyncio.gather(
            *(spider.get_post(meta['link']) for meta in metas))

        posts = coroutine_runner(coros)

        pprint.pprint(posts)

        print('Total posts:', len(posts))
