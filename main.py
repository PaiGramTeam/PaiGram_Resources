import asyncio
import aiofiles
import os

from pathlib import Path
from dotenv import load_dotenv
from httpx import AsyncClient

# Load .env file
load_dotenv()

FILE_PATH = os.getenv('FILE_PATH')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44"
}
if GITHUB_TOKEN:
    HEADER["Authorization"] = f"token {GITHUB_TOKEN}"
client = AsyncClient(headers=HEADER)


async def get_file_content(path: str) -> str:
    url = FILE_PATH.format(PATH=path)
    print(url)
    resp = await client.get(url)
    return resp.text.replace("\r\n", "\n")


async def save_file(file_name: str) -> None:
    file_text = await get_file_content(file_name)
    file_path = Path(f"Resources/{file_name}")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        await f.write(file_text)


async def save_file_list() -> None:
    async with aiofiles.open("src/files.txt", "r", encoding="utf-8") as f:
        file_list = (await f.read()).splitlines()

    tasks = [save_file(file) for file in file_list]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(save_file_list())
