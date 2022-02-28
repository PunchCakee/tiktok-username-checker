from io import TextIOWrapper
import httpx
import time
import sys
from colorama import Fore
import asyncio


async def ping(client: httpx.AsyncClient, url: str, line: str, hits: TextIOWrapper):
    response = await client.get(url)

    if response.status_code == 404:
        print(Fore.GREEN + f"{line}")
        hits.write(f"{line}")
    else:
        print(Fore.RED + f"{line}")


async def tiktok_pinger():
    users = open("userlist.txt", "r")
    hits = open("hits.txt", "w")
    async with httpx.AsyncClient(follow_redirects=True, timeout=1000) as client:
        batch = []
        cap = 700
        for index, line in enumerate(users):
            if index < cap:
                batch.append(
                    [
                        "https://www.tiktok.com/@" + str(line.strip()),
                        line,
                    ]
                )
            else:
                cap += 700
                await asyncio.gather(
                    *[ping(client, url, line, hits) for url, line in batch]
                )
                batch = []

    hits.close()


asyncio.run(tiktok_pinger())