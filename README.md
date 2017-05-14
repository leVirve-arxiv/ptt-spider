# PTT Spider

A super-efficient concurrent spider crawls data from PTT under asynchronous coroutines fast and furiously.

## Requirements
- Python 3.6+
    - At least `Python 3.4` for `aiohttp` and `asyncio.coroutine` features
    - At least `Python 3.5` for `async/await` syntax
    - At least `Python 3.6` for `Formatted string literals`
- `aiohttp`
- `lxml`

## Usage:

- You need create an asyncio event loop, and a helper function `coroutine_runner()` to execute the coroutine task.

```python
loop = asyncio.get_event_loop()

def coroutine_runner(coroutine):
    return loop.run_until_complete(coroutine)
```

- Build a spider in context-manager like to ensure the spider exits normally.

```python
num_page = 5  # collect how many page

with PTTSpider(board='movie', loop=loop) as spider:
    ''' get total page of board
        return: (number) `total_page` of current board
    '''
    total_pages = coroutine_runner(spider.get_total_page_num())


    ''' get pages of posts meta
        return: (list) pages of post `metas`
    '''
    pages = range(total_pages, total_pages - num_page, -1)
    coros = asyncio.gather(
        *(spider.get_meta(page) for page in pages))

    metas = coroutine_runner(coros)
    metas = list(itertools.chain.from_iterable(metas))

    ''' get posts content
        return: (list) lots of `posts` dict()
    '''
    coros = asyncio.gather(
        *(spider.get_post(meta['link']) for meta in metas))

    posts = coroutine_runner(coros)
```
