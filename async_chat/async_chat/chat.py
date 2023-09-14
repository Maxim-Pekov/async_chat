import asyncio
import aiofiles

from datetime import datetime


async def write_into_file(data):
    async with aiofiles.open('x.txt', mode='a') as f:
        chat_text = f"{datetime.now().strftime('[%d.%m.%Y %I:%M]')} {data}"
        await f.write(chat_text)
        print(chat_text)


async def read_from_socket(reader):
    while True:
        data = await reader.read(512)
        if not data:
            break
        await write_into_file(data.decode("utf-8"))


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)
    await read_from_socket(reader)


asyncio.run(tcp_echo_client())
