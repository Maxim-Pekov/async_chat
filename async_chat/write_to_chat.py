import asyncio
import pathlib

import aiofiles
import configargparse
import contextvars
import logging
import json

from datetime import datetime


async def authorise(reader, writer, token):
    writer.write(token.encode())
    await writer.drain()
    data = await reader.readline()
    logging.debug(f'Received: {data.decode()!r}')
    if json.loads(data.decode().split('\n')[0]) is None:
        logging.info('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        return False
    return True


async def registration(reader, writer):
    logging.info(f'Введите ваше имя')
    name = input()
    name = name.replace('\n', '\\n')
    writer.write(f"{name}\n".encode())
    await writer.drain()
    await reader.readuntil(separator=b'\n')
    data = await reader.readline()
    logging.debug(f'Received: {data.decode()}')
    async with aiofiles.open('token.txt', mode='w') as f:
        token = json.loads(data.decode().split('\n')[0])['account_hash']
        await f.write(token)
        logging.debug(f'token: {token}')
    writer.close()
    await writer.wait_closed()


async def submit_message(reader, writer, message=''):
    data = await reader.readline()
    logging.info(data.decode())

    writer.write(f"{message}\n\n".encode())
    await writer.drain()

    data = await reader.readline()
    logging.info(data.decode())


async def tcp_echo_client(message=""):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    data = await reader.readline()
    logging.debug(f'111-----Received: {data.decode()!r}')

    is_token_approve = await authorise(reader, writer, "dfaab544-5414-11ee-aae7-0242ac110002+\n")

    if not is_token_approve:
        await registration(reader, writer)

    await submit_message(reader, writer, 'Hii \n everybody'.replace('\n', '\\n'))

    logging.info('Close the connection')
    writer.close()
    await writer.wait_closed()


def main():
    logging.basicConfig(
        format='%(name)s - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %I:%M:%S %p',
        level=logging.DEBUG
    )
    try:
        asyncio.run(tcp_echo_client())
    except ConnectionResetError:
        logging.info(
            f'Спасибо за регистрацию, ваш токен записан в файл token.txt, запустите программу с правильным токеном.')


if __name__ == "__main__":
    logger = logging.getLogger('writer')
    main()
