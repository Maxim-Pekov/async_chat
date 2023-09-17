import asyncio
import pathlib

import aiofiles
import configargparse
import contextvars
import logging

from datetime import datetime


async def tcp_echo_client(message=""):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    data = await reader.read(100)
    logging.info(f'Received: {data.decode()!r}')

    print(f'Send: {message!r}')
    writer.write("dfaab544-5414-11ee-aae7-0242ac110002\n".encode())
    await writer.drain()

    data = await reader.read(100)
    logging.info(f'Received: {data.decode()!r}')


    writer.write("Всем привет!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n".encode())
    await writer.drain()

    data = await reader.read(100)
    logging.info(f'Received: {data.decode()!r}')


    writer.write("\n".encode())
    await writer.drain()

    data = await reader.read(100)
    logging.info(f'Received: {data.decode()!r}')


    print('Close the connection________________________________________________________________________')
    writer.close()
    await writer.wait_closed()


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %I:%M:%S %p',
        level=logging.CRITICAL
    )
    asyncio.run(tcp_echo_client())


if __name__ == "__main__":
    logger = logging.getLogger(__file__)
    main()
