import sys 
from datetime import datetime, timedelta
import httpx
import asyncio
import ssl
import certifi
import platform
import json


class HttpError(Exception):
    pass

def print_exchange_rates(data):
    print(json.dumps(data, indent=4))

async def request(url: str):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == 200:
            result = r.json()
            return result
        else:
            raise HttpError(f"Error status: {r.status_code} for {url}")



        
async def main(index_day):
    d = datetime.now() - timedelta(days=int(index_day))
    shift = d.strftime("%d.%m.%Y")

    ten_days_ago = datetime.now() - timedelta(days=10)
    if d < ten_days_ago:
        raise ValueError("The date must be within the last 10 days.")

    try:
        response = await request(f'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid={shift}')
        print_exchange_rates(response)
    except HttpError as err:
        print(err)
        return None

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        print (sys.argv)
    r = asyncio.run(main(sys.argv[1]))
    print(r)
