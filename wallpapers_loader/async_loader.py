import aiohttp
import aiofiles
import asyncio
import os


async def download_file_async(url, dst_dir):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                filename = os.path.basename(url)
                filepath = os.path.join(dst_dir, filename)
                f = await aiofiles.open(filepath, "wb")
                await f.write(await response.read())
                await f.close()
                return filepath


def download_files(urls, dst_dir):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([download_file_async(url, dst_dir) for url in urls]))

