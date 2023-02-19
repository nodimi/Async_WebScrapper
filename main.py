from requests_html import AsyncHTMLSession
import asyncio
import time
import httpx
from bs4 import BeautifulSoup

async def work(client, url):
    resp = await client.get(url)
    soup = resp.text
    # category1 = BeautifulSoup(resp.text, 'lxml').find('a', itemprop ='item')
    # print(category1)
    # price = soup.find('div', class_='row row-flex testing2')
    # data = []
    # for i in soup:
    #     category1 = i.findAllNext('h1').find('name')
    #     price = i.findAllNext('price')
    #     # print(desc)
    #
    #     data.append([category1, price])

    return soup

async def main():
    # s = AsyncHTMLSession()
    with open("links_test.txt", "r") as file:
        urls = [line.strip() for line in file.readlines()]
    async with httpx.AsyncClient() as client:
        tasks = []

        for url in urls:
            tasks.append(asyncio.create_task(work(client, url)))

        results = await asyncio.gather(*tasks)

    return results

if __name__ == '__main__':
    results = asyncio.run(main())

    print(results)


start = time.perf_counter()
# results = asyncio.run(main())
# print(results)
fin = time.perf_counter() - start
print(fin)