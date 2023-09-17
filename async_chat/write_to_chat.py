import asyncio
import pathlib

import aiofiles
import configargparse
import contextvars
import logging
import json

from datetime import datetime


async def check_token(reader, writer, token):
    writer.write(token.encode())
    await writer.drain()
    data = await reader.read(100)
    logging.info(f'Received: {data.decode()!r}')
    if json.loads(data.decode().split('\n')[0]) is None:
        logging.info('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        return False
    return True

async def tcp_echo_client(message=""):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    data = await reader.read(100)
    logging.info(f'Received: {data.decode()!r}')

    is_token_approve = await check_token(reader, writer, "dfaab544-5414-11ee-aae7-0242ac110002_\n")

    if not is_token_approve:
        logging.info(f'Введите ваше имя')
        name = input()
        writer.write(f"{name}\n".encode())
        await writer.drain()

    data = await reader.read(100)
    logging.info(f'5Received: {data.decode()!r}')


    writer.write("Всем привет!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n".encode())
    await writer.drain()

    data = await reader.read(100)
    logging.info(f'6Received: {data.decode()!r}')


    # writer.write("\n".encode())
    # await writer.drain()

    data = await reader.read(100)
    logging.info(f'Received: {data.decode()!r}')


    print('Close the connection________________________________________________________________________')
    writer.close()
    await writer.wait_closed()


def main():
    logging.basicConfig(
        format='%(name)s - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %I:%M:%S %p',
        level=logging.INFO
    )
    asyncio.run(tcp_echo_client())


if __name__ == "__main__":
    logger = logging.getLogger('writer')
    main()
