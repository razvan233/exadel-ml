import asyncio
import pandas as pd
import aiohttp
from fake_useragent import UserAgent


async def is_url_accessible(session: aiohttp.ClientSession, url, max_wait=2, max_retries=2):
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}

    for _ in range(max_retries):
        try:
            async with session.get(url, headers=headers, ssl=False) as response:
                if response.status == 200:
                    return True
        except aiohttp.ClientError as err:
            return err
        await asyncio.sleep(max_wait)

    return False


async def process_csv(input_csv, output_xlsx):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        data = pd.read_csv(input_csv, header=None, names=['URL'])
        tasks = []

        for url in data['URL']:
            task = is_url_accessible(session, url)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        data['IsAccessible'] = results
        data.to_excel(output_xlsx, index=False)

if __name__ == "__main__":
    input_csv_file = "furniture_stores_pages.csv"
    output_xlsx_file = "result.xlsx"

    asyncio.run(process_csv(input_csv_file, output_xlsx_file))

    print(f"Results saved to {output_xlsx_file}")
