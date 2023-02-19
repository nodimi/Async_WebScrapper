from requests_html import AsyncHTMLSession
import asyncio
import time
import httpx
from bs4 import BeautifulSoup


async def work(client, url):
    resp = await client.get(url)
    data = []
    if resp.status_code != 200:
        pass

    else:
        soup = BeautifulSoup(resp.text, 'lxml')
        category1 = soup.find('div', class_='breadcrumbs').findAll('a')[1].get('title').strip()
        category2 = soup.find('div', class_='breadcrumbs').findAll('a')[2].get('title').strip()

        data.append([category1, category2])


    return data


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