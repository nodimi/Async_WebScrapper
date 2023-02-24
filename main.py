import asyncio
import time
import httpx
from bs4 import BeautifulSoup
import pandas as pd


start = time.perf_counter()
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
data = []

async def work(client, url):
    resp = await client.get(url, headers=headers)
    if resp.status_code != 200:
        pass
    else:
        soup = BeautifulSoup(resp.text, 'lxml')
        try:
            category1 = soup.find('div', class_='breadcrumbs').findAll('a')[1].get('title').strip()
        except:
            category1 = 'None'
        try:
            category2 = soup.find('div', class_='breadcrumbs').findAll('a')[2].get('title').strip()
        except:
            category2 = 'None'
        try:
            category3 = soup.find('div', class_='breadcrumbs').findAll('a')[3].get('title').strip()
        except:
            category3 = 'None'
        try:
            category4 = soup.find('div', class_='breadcrumbs').findAll('a')[4].get('title').strip()
        except:
            category4 = 'None'
        try:
            name = soup.find('h1', itemprop='name').text.strip()
        except:
            name = 'None'
        if soup.find('div', class_='inline_price').find('span', class_='price has-marketing-price'):
            try:
                price = soup.find('div', class_='inline_price').find('span',
                                                                     class_='marketing-price has-super-price').text.split()
            except:
                pass
        else:
            try:
                price = soup.find('div', class_='row row-flex testing2').find('span', id='js_price').find('span', class_='price').text.split()
            except:
                price = 'Nonee'
        try:
            manufacturer = soup.findAll('span', class_='param-value__value')[0].find('a').text.strip()
        except:
            manufacturer = 'None'
        try:
            country = soup.findAll('span', class_='param-value__value')[0].text.split()[-1]
            if country != country.upper():
                country = 'None'
        except:
            country = 'None'

        data.append([category1,
                     category2,
                     category3,
                     category4,
                     name,
                     ''.join(price[0:-1]),
                     manufacturer,
                     country,
                     url])


    return data


async def main():
    timeout = httpx.Timeout(20.0, pool=20.0)
    limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)

    # Choose txt file with urls for wab scraping
    with open("links7.txt", "r") as file:
        urls = [line.strip() for line in file.readlines()]
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        # sleep(2)
        tasks = []


        for url in urls:

            tasks.append(asyncio.create_task(work(client, url)))

        results = await asyncio.gather(*tasks)

    return results

# записываем полученные данные в CSV


if __name__ == '__main__':
    results = asyncio.run(main())

    # print(results)

#Put data to csv
header = ['category1',
          'category2',
          'category3',
          'category4',
          'name',
          'price',
          'manufacturer',
          'country',
          'url']

df = pd.DataFrame(data, columns=header)
df.to_csv(f'D:\MyPython\WebScrapers\Async\Trapeza_Async7.csv',sep=';', encoding='cp1251', errors='ignore')



fin = time.perf_counter() - start
print(fin)