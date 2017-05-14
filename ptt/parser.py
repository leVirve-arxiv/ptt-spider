import re

from lxml import html


def previous_page_number(text):
    doc = html.fromstring(text)
    prev = doc.xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]')[0]
    match = re.findall('index(\d+)', prev.get('href'))
    return int(match[0])


def post_metas(text):
    doc = html.fromstring(text)
    post_lines = doc.xpath('//div[@class="r-ent"]')

    def text(elem):
        elem = xpath0(elem)
        return elem.text.strip() if elem is not None and elem.text else None

    def xpath0(elem):
        return elem[0] if len(elem) else None

    metas = [
        {'push': text(line.xpath('div[@class="nrec"]/span')),
         'mark': text(line.xpath('div[@class="mark"]')),
         'title': text(line.xpath('div[@class="title"]/a')),
         'date': text(line.xpath('div[@class="meta"]/div[@class="date"]')),
         'author': text(line.xpath('div[@class="meta"]/div[@class="author"]')),
         'link': xpath0(line.xpath('div[@class="title"]/a//@href')),
         }
        for line in post_lines
    ]
    return metas


def post_content(text):
    doc = html.fromstring(text)
    try:
        main = doc.xpath('//*[@id="main-content"]')[0]
        metaline = main.xpath('div[@class="article-metaline"]')

        author = metaline[0].xpath('span')[1].text
        title = metaline[1].xpath('span')[1].text
        datetime = metaline[2].xpath('span')[1].text
        content = doc.xpath(
            '//div[@id="main-content"]'
            '/text()['
            'not(contains(@class, "push")) and '
            'not(contains(@class, "article-metaline")) and '
            'not(contains(@class, "f2"))'
            ']')
        ip_span = main.xpath('span[contains(text(),"發信站: 批踢踢實業坊(ptt.cc)")]')
        url_span = main.xpath('span[contains(text(),"※ 文章網址:")]/a//@href')

        ip = re.findall('\d+.\d+.\d+.\d+', ip_span[0].text)[0]
        url = url_span[0]
        content = ''.join(content)
        comments = []

        for push in main.xpath('div[@class="push"]'):
            spans = push.xpath('span')
            comments.append({
                'push': spans[0].text.strip(),
                'user': spans[1].text,
                'comment': spans[2].text[1:].strip(),
                'datetime': spans[3].text.strip()})
        return {'author': author,
                'title': title,
                'datetime': datetime,
                'content': content,
                'ip': ip,
                'comments': comments,
                'url': url}
    except IndexError:
        return {}
