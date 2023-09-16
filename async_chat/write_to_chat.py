import asyncio
import pathlib

import aiofiles
import configargparse
import contextvars

from datetime import datetime


async def tcp_echo_client(message=""):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print(f'Send: {message!r}')
    writer.write("dfaab544-5414-11ee-aae7-0242ac110002\n".encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    writer.write("Всем привет!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n".encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    writer.write("\n".encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection________________________________________________________________________')
    writer.close()
    await writer.wait_closed()


def main():
    asyncio.run(tcp_echo_client())


if __name__ == "__main__":
    main()
